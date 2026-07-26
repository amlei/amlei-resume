#!/usr/bin/env python3
"""amlei-resume 统一 CLI（三层模型单一入口）。

职责分界：
  · 事实层（_shared/）：shell-out 给 amlei-profile/scripts/profile.py
  · 强调层（identities/{id}/emphasis/）：本脚本直接维护，schema 校验 + 时间戳备份
  · 快照层（identities/{id}/resumes/{app}/_meta.json）：本脚本维护，含 fork + fact diff

设计原则：
  · 所有写入前 schema 校验（轻量内联，无外部依赖）
  · 写前自动时间戳备份（保留最近 10 份）
  · 强调层写入触发对应 _meta.facts_version_at_last_sync 检查（不自动改，仅元数据）
  · fork 时计算 fact diff（基于 needs_review 状态 + 版本戳比较），不自动应用

退出码：0 正常；1 不存在 / 已存在不覆盖 / 参数错 / 校验失败。

用法：见 `resume_cli.py --help` 或 `<子命令> --help`。
"""

import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime

KEEP_BACKUPS = 10
PROFILE_PY = os.path.join(os.path.dirname(__file__), "..", "..", "amlei-profile", "scripts", "profile.py")

ID_PATTERNS = {
    "exp": re.compile(r"^exp_[a-z0-9_]+$"),
    "prj": re.compile(r"^prj_[a-z0-9_]+$"),
    "cap": re.compile(r"^cap_[a-z0-9_]+$"),
}
IDENTITY_SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def _now():
    return datetime.now().isoformat(timespec="seconds")


def _stamp():
    return datetime.now().strftime("%Y%m%dT%H%M%S%f")


def _base_paths():
    return {
        "project": os.path.join(os.getcwd(), ".amlei-skill", "resume"),
        "root": os.path.join(os.path.expanduser("~"), ".amlei-skill", "resume"),
    }


def resolve_base():
    """返回 resume base 目录（含 _shared/ 或 identities/）。不存在返 None。"""
    for key in ("project", "root"):
        base = _base_paths()[key]
        if os.path.isdir(os.path.join(base, "_shared")) or os.path.isdir(os.path.join(base, "identities")):
            return base
    return None


def require_base():
    base = resolve_base()
    if not base:
        print("✗ resume base 不存在。先 init --location project|root 创建。")
        sys.exit(1)
    return base


def _shared_paths(base):
    s = os.path.join(base, "_shared")
    return {
        "shared": s,
        "identity": os.path.join(s, "identity.json"),
        "experiences": os.path.join(s, "experiences.json"),
        "capabilities": os.path.join(s, "capabilities.json"),
        "identities": os.path.join(base, "identities"),
    }


def _load(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"✗ 文件不存在：{path}")
        sys.exit(1)


def _save(path, data, bump_facts_version=False):
    """原子写 + 时间戳备份。bump_facts_version 仅对事实层文件有效。"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.isfile(path):
        bak = f"{path}.bak.{_stamp()}"
        shutil.copy2(path, bak)
        baks = sorted(glob.glob(f"{path}.bak.*"))
        for old in baks[:-KEEP_BACKUPS]:
            try:
                os.remove(old)
            except OSError:
                pass
    if bump_facts_version and isinstance(data, dict) and "_meta" in data:
        data["_meta"]["facts_version"] = _now()
    tmp = f"{path}.tmp.{os.getpid()}"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


# ─── 校验 ──────────────────────────────────────────────────────────────────

def _validate_id(kind, x):
    if not ID_PATTERNS[kind].match(x or ""):
        print(f"✗ id 不合法（{kind}_<小写字母数字下划线>）：{x!r}")
        sys.exit(1)


def _validate_slug(slug):
    if not IDENTITY_SLUG_RE.match(slug or ""):
        print(f"✗ identity slug 不合法（kebab-case）：{slug!r}")
        sys.exit(1)


def _all_fact_ids(base, kind):
    """返回 _shared 里某类 fact 的所有 id。"""
    sp = _shared_paths(base)
    if kind == "experience":
        data = _load(sp["experiences"])
        return [it["id"] for it in data["items"]]
    if kind == "project":
        data = _load(sp["experiences"])
        return [prj["id"] for exp in data["items"] for prj in exp.get("projects", [])]
    if kind == "capability":
        data = _load(sp["capabilities"])
        return [it["id"] for it in data["items"]]
    return []


def _check_fact_exists(base, kind, fid):
    if fid not in _all_fact_ids(base, kind):
        print(f"✗ {kind} 不存在：{fid}")
        sys.exit(1)


# ─── fact 层：shell-out 给 amlei-profile/scripts/profile.py ────────────────

def _profile_py_path():
    p = os.path.abspath(PROFILE_PY)
    if not os.path.isfile(p):
        print(f"✗ 找不到 amlei-profile/scripts/profile.py：{p}")
        print("  请确认 amlei-profile skill 已安装")
        sys.exit(1)
    return p


def cmd_identities(args):
    """列出所有身份。"""
    base = require_base()
    idir = _shared_paths(base)["identities"]
    if not os.path.isdir(idir):
        print("（暂无身份）")
        return
    slugs = sorted(d for d in os.listdir(idir)
                    if os.path.isdir(os.path.join(idir, d)) and not d.startswith("."))
    if not slugs:
        print("（暂无身份）")
        return
    for slug in slugs:
        target_path = os.path.join(idir, slug, "target.json")
        if os.path.isfile(target_path):
            t = _load(target_path)
            print(f"  · {slug}  方向={t.get('direction','-')}  tags={','.join(t.get('target_role_tags',[])) or '-'}")
        else:
            print(f"  · {slug}  （无 target.json）")


# ─── identity（强调层意义上的"身份目录"） ──────────────────────────────────

def _identity_dir(base, slug):
    return os.path.join(base, "identities", slug)


def cmd_new_identity(args):
    """新建身份：写 target.json + 空 emphasis/* 骨架。"""
    base = require_base()
    _validate_slug(args.slug)
    idir = _identity_dir(base, args.slug)
    if os.path.isdir(idir):
        print(f"✗ 身份已存在：{args.slug}")
        sys.exit(1)
    os.makedirs(os.path.join(idir, "emphasis"), exist_ok=True)
    os.makedirs(os.path.join(idir, "resumes"), exist_ok=True)
    # target.json
    target = {
        "identity_id": args.slug,
        "direction": args.direction or args.slug,
        "target_role_tags": (args.tag.split(",") if args.tag else []),
        "preferences": {},
        "target_companies": [],
        "created_from_projection": {
            "projected_at": _now(),
            "jd_basis": args.jd_basis or "（手工创建）",
        },
    }
    _save(os.path.join(idir, "target.json"), target)
    # 空 emphasis 骨架
    fv = _now()
    _save(os.path.join(idir, "emphasis", "projects.json"), {
        "_meta": {"facts_version_at_last_sync": fv, "needs_review": False},
        "selected": [], "framing": {}, "excluded": [],
    })
    _save(os.path.join(idir, "emphasis", "experiences.json"), {
        "_meta": {"facts_version_at_last_sync": fv, "needs_review": False},
        "selected": [], "ordering": [], "framing": {},
    })
    _save(os.path.join(idir, "emphasis", "capabilities.json"), {
        "_meta": {"facts_version_at_last_sync": fv, "needs_review": False},
        "selected": [], "skill_axis": [],
    })
    _save(os.path.join(idir, "emphasis", "narrative.json"), {
        "_meta": {"needs_review": False},
        "self_intro": {"role": args.direction or args.slug, "pitch": "", "tags": []},
    })
    print(f"✓ 已创建身份：{args.slug}")
    print(f"  target.json + emphasis/*.json 空骨架已就位")
    print(f"  下一步：select {args.slug} project prj_XXX 选项目；或让 LLM 投影")


def cmd_rm_identity(args):
    base = require_base()
    _validate_slug(args.slug)
    idir = _identity_dir(base, args.slug)
    if not os.path.isdir(idir):
        print(f"✗ 身份不存在：{args.slug}")
        sys.exit(1)
    if not args.force:
        # 二次确认
        resumes_dir = os.path.join(idir, "resumes")
        if os.path.isdir(resumes_dir) and any(os.scandir(resumes_dir)):
            print(f"⚠ 身份 {args.slug} 下有简历快照，删除会丢失归档。")
            print(f"  加 --force 强制删除；或建议改为归档（mv identities/{args.slug} identities/{args.slug}.archived）")
            sys.exit(1)
    shutil.rmtree(idir)
    print(f"✓ 已删除身份：{args.slug}")


# ─── emphasis: projects ────────────────────────────────────────────────────

def _load_emphasis(base, slug, fname):
    idir = _identity_dir(base, slug)
    path = os.path.join(idir, "emphasis", fname)
    return path, _load(path)


def cmd_select(args):
    """选中某 fact 到对应 emphasis 文件。kind: project|experience|capability。"""
    base = require_base()
    _validate_slug(args.slug)
    fname_map = {"project": "projects.json", "experience": "experiences.json", "capability": "capabilities.json"}
    fname = fname_map[args.kind]
    path, data = _load_emphasis(base, args.slug, fname)
    # 校验 fact 存在
    _check_fact_exists(base, args.kind, args.id)
    sel = data.setdefault("selected", [])
    if args.id in sel:
        print(f"✓ {args.id} 已在 selected")
        return
    sel.append(args.id)
    # 从 excluded 移除（如果在那）
    if args.kind == "project":
        data["excluded"] = [x for x in data.get("excluded", []) if x.get("id") != args.id]
    _save(path, data)
    print(f"✓ {args.slug}/emphasis/{fname} 选中 {args.id}")


def cmd_unselect(args):
    base = require_base()
    _validate_slug(args.slug)
    fname_map = {"project": "projects.json", "experience": "experiences.json", "capability": "capabilities.json"}
    fname = fname_map[args.kind]
    path, data = _load_emphasis(base, args.slug, fname)
    sel = data.get("selected", [])
    if args.id not in sel:
        print(f"✓ {args.id} 不在 selected（无需操作）")
        return
    sel.remove(args.id)
    _save(path, data)
    print(f"✓ {args.slug}/emphasis/{fname} 取消选中 {args.id}")


def cmd_set_framing(args):
    """设置某 project 的 framing（source_grain_index + bullet）。"""
    base = require_base()
    _validate_slug(args.slug)
    _validate_id("prj", args.id)
    _check_fact_exists(base, "project", args.id)
    path, data = _load_emphasis(base, args.slug, "projects.json")
    framing = data.setdefault("framing", {})
    entry = framing.get(args.id, {})
    if args.grain is not None:
        # 校验 grain index 在 fact 层 granularity 数组范围内
        exp_data = _load(_shared_paths(base)["experiences"])
        prj = None
        for exp in exp_data["items"]:
            for p in exp.get("projects", []):
                if p["id"] == args.id:
                    prj = p
                    break
            if prj:
                break
        if not prj:
            print(f"✗ project 不存在：{args.id}")
            sys.exit(1)
        grains = prj.get("granularity", [])
        if args.grain < 0 or args.grain >= len(grains):
            print(f"✗ source_grain_index 越界：project {args.id} 有 {len(grains)} 档 granularity（0..{len(grains)-1}）")
            sys.exit(1)
        entry["source_grain_index"] = args.grain
    if args.bullet is not None:
        entry["bullet"] = args.bullet
    if args.skill_attribution is not None:
        attrs = [x.strip() for x in args.skill_attribution.split(",") if x.strip()]
        for a in attrs:
            _validate_id("cap", a)
            _check_fact_exists(base, "capability", a)
        entry["skill_attribution"] = attrs
    if "source_grain_index" not in entry or "bullet" not in entry:
        print("✗ framing 必须同时有 source_grain_index 和 bullet")
        print("  首次设置时两者都要给；之后可单独更新其一")
        sys.exit(1)
    framing[args.id] = entry
    _save(path, data)
    print(f"✓ {args.slug}/emphasis/projects.json 的 {args.id} framing 已更新")


def cmd_exclude(args):
    """把某 project 显式标为排除（带原因）。"""
    base = require_base()
    _validate_slug(args.slug)
    _validate_id("prj", args.id)
    _check_fact_exists(base, "project", args.id)
    path, data = _load_emphasis(base, args.slug, "projects.json")
    excluded = data.setdefault("excluded", [])
    # 移除已存在
    excluded[:] = [x for x in excluded if x.get("id") != args.id]
    excluded.append({"id": args.id, "reason": args.reason or "（未注明）"})
    # 从 selected 移除
    if args.id in data.get("selected", []):
        data["selected"].remove(args.id)
    # 删 framing
    data.get("framing", {}).pop(args.id, None)
    _save(path, data)
    print(f"✓ {args.slug} 已排除 {args.id}（原因：{args.reason or '未注明'}）")


# ─── emphasis: experiences ─────────────────────────────────────────────────

def cmd_set_headline(args):
    """设置某 experience 的 headline / summary。"""
    base = require_base()
    _validate_slug(args.slug)
    _validate_id("exp", args.id)
    _check_fact_exists(base, "experience", args.id)
    path, data = _load_emphasis(base, args.slug, "experiences.json")
    framing = data.setdefault("framing", {})
    entry = framing.get(args.id, {})
    if args.headline is not None:
        entry["headline"] = args.headline
    if args.summary is not None:
        entry["summary"] = args.summary
    framing[args.id] = entry
    _save(path, data)
    print(f"✓ {args.slug}/emphasis/experiences.json 的 {args.id} framing 已更新")


def cmd_order(args):
    """设置 experiences 的渲染顺序（逗号分隔的 exp_id 列表）。"""
    base = require_base()
    _validate_slug(args.slug)
    path, data = _load_emphasis(base, args.slug, "experiences.json")
    ids = [x.strip() for x in args.order.split(",") if x.strip()]
    for x in ids:
        _validate_id("exp", x)
        _check_fact_exists(base, "experience", x)
    data["ordering"] = ids
    # 若 selected 不含这些，自动加入
    sel = data.setdefault("selected", [])
    for x in ids:
        if x not in sel:
            sel.append(x)
    _save(path, data)
    print(f"✓ ordering 已设：{' → '.join(ids)}")


# ─── emphasis: capabilities + skill_axis ───────────────────────────────────

def cmd_skill_axis(args):
    """管理 skill_axis。action: add/rm。"""
    base = require_base()
    _validate_slug(args.slug)
    path, data = _load_emphasis(base, args.slug, "capabilities.json")
    axis = data.setdefault("skill_axis", [])
    if args.action == "add":
        if not args.label:
            print("✗ --label 必填")
            sys.exit(1)
        refs = [x.strip() for x in (args.refs or "").split(",") if x.strip()]
        if not refs:
            print("✗ --refs 必填（至少一个 capability id）")
            sys.exit(1)
        for r in refs:
            _validate_id("cap", r)
            _check_fact_exists(base, "capability", r)
        # 找是否已有同 label
        existing = next((a for a in axis if a.get("label") == args.label), None)
        if existing:
            for r in refs:
                if r not in existing["capability_refs"]:
                    existing["capability_refs"].append(r)
        else:
            axis.append({"label": args.label, "capability_refs": refs})
        # 同步加到 selected
        sel = data.setdefault("selected", [])
        for r in refs:
            if r not in sel:
                sel.append(r)
        _save(path, data)
        print(f"✓ skill_axis 已加：{args.label} → {refs}")
    elif args.action == "rm":
        if not args.label:
            print("✗ --label 必填")
            sys.exit(1)
        before = len(axis)
        axis[:] = [a for a in axis if a.get("label") != args.label]
        if len(axis) == before:
            print(f"✗ 没有这个 skill_axis label：{args.label}")
            sys.exit(1)
        _save(path, data)
        print(f"✓ skill_axis 已移除：{args.label}")


def cmd_set_narrative(args):
    """设置自述。"""
    base = require_base()
    _validate_slug(args.slug)
    path, data = _load_emphasis(base, args.slug, "narrative.json")
    si = data.setdefault("self_intro", {})
    if args.role is not None:
        si["role"] = args.role
    if args.pitch is not None:
        si["pitch"] = args.pitch
    if args.tag is not None:
        si["tags"] = [x.strip() for x in args.tag.split(",") if x.strip()]
    _save(path, data)
    print(f"✓ {args.slug}/emphasis/narrative.json 已更新")


# ─── snapshot ──────────────────────────────────────────────────────────────

def _resume_dir(base, slug, app_id):
    return os.path.join(_identity_dir(base, slug), "resumes", app_id)


def cmd_new_snapshot(args):
    """新建 snapshot 的 _meta.json（不含 简历.md，那是 LLM 写的）。"""
    base = require_base()
    _validate_slug(args.slug)
    if not re.match(r"^[a-z0-9][a-z0-9_\-]*$", args.app_id or ""):
        print(f"✗ app_id 不合法（小写字母数字下划线连字符）：{args.app_id!r}")
        sys.exit(1)
    rdir = _resume_dir(base, args.slug, args.app_id)
    if os.path.isdir(rdir):
        print(f"✗ snapshot 已存在：{args.slug}/resumes/{args.app_id}")
        sys.exit(1)
    os.makedirs(rdir, exist_ok=True)
    # 当前 facts_version
    exp_data = _load(_shared_paths(base)["experiences"])
    facts_version = exp_data["_meta"]["facts_version"]
    # 当前 emphasis 版本（取最晚的 facts_version_at_last_sync）
    emph_dir = os.path.join(_identity_dir(base, args.slug), "emphasis")
    emph_version = facts_version
    if os.path.isdir(emph_dir):
        versions = []
        for fname in ("projects.json", "experiences.json", "capabilities.json"):
            fpath = os.path.join(emph_dir, fname)
            if os.path.isfile(fpath):
                versions.append(_load(fpath).get("_meta", {}).get("facts_version_at_last_sync", ""))
        if versions:
            emph_version = max(versions)
    meta = {
        "app_id": args.app_id,
        "created_at": _now(),
        "facts_version_at_creation": facts_version,
        "emphasis_version_at_creation": emph_version,
        "source_operation": args.operation,
        "forked_from": None,
        "delivered": False,
        "delivered_at": None,
        "needs_review": False,
    }
    _save(os.path.join(rdir, "_meta.json"), meta)
    print(f"✓ snapshot 已建：{args.slug}/resumes/{args.app_id}")
    print(f"  source_operation={args.operation}")
    print(f"  facts_version_at_creation={facts_version}")
    print(f"  下一步：LLM 渲染 简历.md + jd.md + materials.md 到此目录")


def cmd_fork(args):
    """fork 一个已有 snapshot：复制 简历.md 等 + 写新 _meta + 计算 fact diff。"""
    base = require_base()
    _validate_slug(args.slug)
    src_dir = _resume_dir(base, args.slug, args.source_app)
    if not os.path.isdir(src_dir):
        print(f"✗ 源 snapshot 不存在：{args.slug}/resumes/{args.source_app}")
        sys.exit(1)
    if not re.match(r"^[a-z0-9][a-z0-9_\-]*$", args.new_app or ""):
        print(f"✗ new_app 不合法：{args.new_app!r}")
        sys.exit(1)
    new_dir = _resume_dir(base, args.slug, args.new_app)
    if os.path.isdir(new_dir):
        print(f"✗ snapshot 已存在：{args.slug}/resumes/{args.new_app}")
        sys.exit(1)
    # 复制源的内容（除 _meta.json 和 .bak.* 备份）
    os.makedirs(new_dir, exist_ok=True)
    copied = []
    for fn in os.listdir(src_dir):
        if fn == "_meta.json" or fn.startswith(".") or ".bak." in fn:
            continue
        s = os.path.join(src_dir, fn)
        d = os.path.join(new_dir, fn)
        if os.path.isdir(s):
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)
        copied.append(fn)
    # 读源 meta
    src_meta = _load(os.path.join(src_dir, "_meta.json"))
    src_facts_version = src_meta.get("facts_version_at_creation")
    # 当前 facts_version
    exp_data = _load(_shared_paths(base)["experiences"])
    current_facts_version = exp_data["_meta"]["facts_version"]
    facts_changed = src_facts_version != current_facts_version
    # 找出 needs_review 的 emphasis 条目（这是 fact 变更的强信号，比时间戳更可靠）
    # 不管 facts_changed 都扫，因为时间戳可能因秒级精度碰撞而漏报
    emph_dir = os.path.join(_identity_dir(base, args.slug), "emphasis")
    changed_refs = []
    if os.path.isdir(emph_dir):
        for fname in ("projects.json", "experiences.json", "capabilities.json"):
            fpath = os.path.join(emph_dir, fname)
            if not os.path.isfile(fpath):
                continue
            edata = _load(fpath)
            if edata.get("_meta", {}).get("needs_review"):
                # 这个 emphasis 文件有 needs_review，列出 selected
                for fid in edata.get("selected", []):
                    changed_refs.append({"kind": fname.replace(".json", ""), "id": fid})
    has_diff = facts_changed or bool(changed_refs) or src_meta.get("needs_review", False)
    # 写新 meta
    new_meta = {
        "app_id": args.new_app,
        "created_at": _now(),
        "facts_version_at_creation": current_facts_version,
        "emphasis_version_at_creation": src_meta.get("emphasis_version_at_creation"),
        "source_operation": "fork",
        "forked_from": args.source_app,
        "delivered": False,
        "delivered_at": None,
        "needs_review": False,  # fork 起步默认 false；下面若有 diff 翻 true
    }
    if has_diff:
        new_meta["needs_review"] = True
    _save(os.path.join(new_dir, "_meta.json"), new_meta)
    print(f"✓ fork 完成：{args.source_app} → {args.new_app}")
    print(f"  复制了 {len(copied)} 个文件：{copied}")
    if has_diff:
        print(f"\n⚠ 事实层在源快照之后有变化：")
        if facts_changed:
            print(f"   源 facts_version: {src_facts_version}")
            print(f"   当前 facts_version: {current_facts_version}")
        if src_meta.get("needs_review"):
            print(f"   源 snapshot 自身被标过 needs_review")
        if changed_refs:
            print(f"   引用了变更 fact 的 emphasis 条目（{len(changed_refs)} 个）：")
            for r in changed_refs:
                print(f"     - {r['kind']}/{r['id']}")
        print(f"\n   下一步：人工审阅这些条目，决定哪些 bullet 要根据新事实重写。")
        print(f"   系统不会自动改——只提示。")
    else:
        print(f"  无 fact diff（时间戳与 needs_review 均无变化）")


def cmd_deliver(args):
    """标记 snapshot 为已投递（delivered=true 后 简历.md 不可变）。"""
    base = require_base()
    _validate_slug(args.slug)
    meta_path = os.path.join(_resume_dir(base, args.slug, args.app_id), "_meta.json")
    if not os.path.isfile(meta_path):
        print(f"✗ snapshot 不存在：{args.slug}/resumes/{args.app_id}")
        sys.exit(1)
    meta = _load(meta_path)
    if meta.get("delivered"):
        print(f"✓ 已是 delivered 状态（{meta.get('delivered_at','-')}）")
        return
    meta["delivered"] = True
    meta["delivered_at"] = _now()
    _save(meta_path, meta)
    print(f"✓ {args.slug}/resumes/{args.app_id} → delivered=true")
    print(f"  从此刻起 简历.md 内容不可变；事实层更新只会翻 needs_review")


def cmd_clear_review(args):
    """清除 needs_review（用户审阅后决定不改文案）。"""
    base = require_base()
    _validate_slug(args.slug)
    # snapshot
    if args.app_id:
        meta_path = os.path.join(_resume_dir(base, args.slug, args.app_id), "_meta.json")
        meta = _load(meta_path)
        if not meta.get("needs_review"):
            print(f"✓ snapshot 已是 needs_review=false")
            return
        meta["needs_review"] = False
        _save(meta_path, meta)
        print(f"✓ snapshot {args.app_id} → needs_review=false（用户已审阅，认可当前文案）")
        return
    # emphasis 全部
    emph_dir = os.path.join(_identity_dir(base, args.slug), "emphasis")
    if not os.path.isdir(emph_dir):
        print(f"✗ 身份 {args.slug} 无 emphasis 目录")
        sys.exit(1)
    # 同步到当前 facts_version
    exp_data = _load(_shared_paths(base)["experiences"])
    current_fv = exp_data["_meta"]["facts_version"]
    cleared = 0
    for fname in ("projects.json", "experiences.json", "capabilities.json"):
        fpath = os.path.join(emph_dir, fname)
        if not os.path.isfile(fpath):
            continue
        data = _load(fpath)
        if data.get("_meta", {}).get("needs_review"):
            data["_meta"]["needs_review"] = False
            data["_meta"]["facts_version_at_last_sync"] = current_fv
            _save(fpath, data)
            cleared += 1
    print(f"✓ {args.slug} 的 emphasis 已清 needs_review（{cleared} 个文件），")
    print(f"  facts_version_at_last_sync 同步到 {current_fv}")


def cmd_snapshots(args):
    """列出某身份的所有 snapshot。"""
    base = require_base()
    _validate_slug(args.slug)
    rdir = os.path.join(_identity_dir(base, args.slug), "resumes")
    if not os.path.isdir(rdir):
        print(f"（{args.slug} 暂无 snapshot）")
        return
    apps = sorted(d for d in os.listdir(rdir)
                  if os.path.isdir(os.path.join(rdir, d)) and not d.startswith("."))
    if not apps:
        print(f"（{args.slug} 暂无 snapshot）")
        return
    for app in apps:
        meta_path = os.path.join(rdir, app, "_meta.json")
        if os.path.isfile(meta_path):
            m = _load(meta_path)
            flag = "  ⚠ needs_review" if m.get("needs_review") else ""
            delivered = "  ✓ delivered" if m.get("delivered") else ""
            fork = f"  (fork from {m.get('forked_from')})" if m.get("forked_from") else ""
            print(f"  · {app}  op={m.get('source_operation','-')}{delivered}{flag}{fork}")
        else:
            print(f"  · {app}  （无 _meta.json）")


# ─── init / path ───────────────────────────────────────────────────────────

def cmd_path(args):
    base = resolve_base()
    print(base if base else "NOT FOUND（用 init --location project|root 创建）")


def cmd_init(args):
    """bootstrap _shared/ + identities/。委托给 profile.py init。"""
    profile = _profile_py_path()
    cmd = [sys.executable, profile, "init", "--location", args.location]
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


# ─── main ──────────────────────────────────────────────────────────────────

PASSTHROUGH_CMDS = {"identity", "experience", "project", "capability",
                    "find", "batch", "propagate", "time"}


def main():
    # fact-layer 子命令直接转给 profile.py，不经 argparse（避免 --opt 被吃掉）
    if len(sys.argv) > 1 and sys.argv[1] in PASSTHROUGH_CMDS:
        profile = _profile_py_path()
        cmd = [sys.executable, profile] + sys.argv[1:]
        result = subprocess.run(cmd)
        sys.exit(result.returncode)

    ap = argparse.ArgumentParser(
        description="amlei-resume 统一 CLI（三层模型）。",
        epilog="事实层子命令（identity/experience/project/capability/find/batch/propagate/time）"
               "会转给 amlei-profile/scripts/profile.py。"
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    # ─ 本 CLI 自己的命令 ─
    s = sub.add_parser("path"); s.set_defaults(func=cmd_path)
    s = sub.add_parser("init")
    s.add_argument("--location", choices=["project", "root"], required=True)
    s.set_defaults(func=cmd_init)

    # 身份管理
    s = sub.add_parser("identities", help="列出所有身份"); s.set_defaults(func=cmd_identities)
    s = sub.add_parser("new-identity", help="新建身份（投影骨架）")
    s.add_argument("slug")
    s.add_argument("--direction")
    s.add_argument("--tag", help="逗号分隔的方向 tag")
    s.add_argument("--jd-basis", help="投影所基于的 JD / 方向描述")
    s.set_defaults(func=cmd_new_identity)
    s = sub.add_parser("rm-identity", help="删除身份（连同 emphasis + snapshots）")
    s.add_argument("slug")
    s.add_argument("--force", action="store_true", help="即使有 snapshots 也强删")
    s.set_defaults(func=cmd_rm_identity)

    # emphasis: 通用 select / unselect
    s = sub.add_parser("select", help="选中某 fact 到对应 emphasis")
    s.add_argument("slug")
    s.add_argument("kind", choices=["project", "experience", "capability"])
    s.add_argument("id")
    s.set_defaults(func=cmd_select)
    s = sub.add_parser("unselect", help="取消选中")
    s.add_argument("slug")
    s.add_argument("kind", choices=["project", "experience", "capability"])
    s.add_argument("id")
    s.set_defaults(func=cmd_unselect)

    # emphasis: projects
    s = sub.add_parser("set-framing", help="设置 project framing（grain index + bullet）")
    s.add_argument("slug"); s.add_argument("id")
    s.add_argument("--grain", type=int, help="granularity 数组下标")
    s.add_argument("--bullet")
    s.add_argument("--skill-attribution", help="逗号分隔的 cap_id")
    s.set_defaults(func=cmd_set_framing)
    s = sub.add_parser("exclude", help="把 project 显式标为排除")
    s.add_argument("slug"); s.add_argument("id"); s.add_argument("--reason")
    s.set_defaults(func=cmd_exclude)

    # emphasis: experiences
    s = sub.add_parser("set-headline", help="设置 experience 的 headline/summary")
    s.add_argument("slug"); s.add_argument("id")
    s.add_argument("--headline"); s.add_argument("--summary")
    s.set_defaults(func=cmd_set_headline)
    s = sub.add_parser("order", help="设 experiences 渲染顺序")
    s.add_argument("slug"); s.add_argument("order", help="逗号分隔的 exp_id")
    s.set_defaults(func=cmd_order)

    # emphasis: capabilities
    s = sub.add_parser("skill-axis", help="管理 skill_axis")
    s.add_argument("slug")
    s.add_argument("action", choices=["add", "rm"])
    s.add_argument("--label", required=True)
    s.add_argument("--refs", help="逗号分隔的 cap_id（add 时必填）")
    s.set_defaults(func=cmd_skill_axis)
    s = sub.add_parser("set-narrative", help="设置自述")
    s.add_argument("slug")
    s.add_argument("--role"); s.add_argument("--pitch"); s.add_argument("--tag")
    s.set_defaults(func=cmd_set_narrative)

    # snapshot
    s = sub.add_parser("new-snapshot", help="新建 snapshot _meta.json")
    s.add_argument("slug"); s.add_argument("app_id")
    s.add_argument("--operation", choices=["new_from_projection", "new_from_emphasis", "fork"],
                    default="new_from_emphasis")
    s.set_defaults(func=cmd_new_snapshot)
    s = sub.add_parser("fork", help="fork 已有 snapshot + 计算 fact diff")
    s.add_argument("slug"); s.add_argument("source_app"); s.add_argument("new_app")
    s.set_defaults(func=cmd_fork)
    s = sub.add_parser("deliver", help="标记 snapshot 为已投递")
    s.add_argument("slug"); s.add_argument("app_id")
    s.set_defaults(func=cmd_deliver)
    s = sub.add_parser("clear-review", help="清除 needs_review（snapshot 或 emphasis 全部）")
    s.add_argument("slug")
    s.add_argument("--app-id", help="指定 snapshot；不给则清所有 emphasis")
    s.set_defaults(func=cmd_clear_review)
    s = sub.add_parser("snapshots", help="列出某身份的所有 snapshot")
    s.add_argument("slug")
    s.set_defaults(func=cmd_snapshots)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
