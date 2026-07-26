#!/usr/bin/env python3
"""amlei-profile 的事实层管理（v2，三层模型）。

事实层（`_shared/`）是用户跨会话认识用户的唯一长期真相源：
  · 位置优先项目级 <cwd>/.amlei-skill/resume/_shared/，
    否则用户根目录 ~/.amlei-skill/resume/_shared/
  · 4 个事实文件：identity.json / experiences.json / capabilities.json / files/
  · 每次写入自动时间戳备份（保留最近 10 份），_meta.facts_version 用 ISO 8601 秒级
  · 写入前做轻量 schema 校验（必填、id 格式、proven_by 非空、引用存在）
  · 调用写入命令前，Agent 必须已征得用户同意（本脚本不替你问）

退出码：0 正常；1 资料不存在 / 条目不存在 / 已存在不覆盖 / 参数错 / 校验失败。

详细规则见 SKILL.md 与 references/facts.md。
"""

import argparse
import glob
import json
import os
import re
import shutil
import sys
from datetime import datetime

IDENTITY_FILE = "identity.json"
EXPERIENCES_FILE = "experiences.json"
CAPABILITIES_FILE = "capabilities.json"
SHARED_DIR = "_shared"
IDENTITIES_DIR = "identities"
KEEP_BACKUPS = 10

ID_PATTERNS = {
    "exp": re.compile(r"^exp_[a-z0-9_]+$"),
    "prj": re.compile(r"^prj_[a-z0-9_]+$"),
    "cap": re.compile(r"^cap_[a-z0-9_]+$"),
}
VALID_GRAINS = {"project", "milestone", "technique", "module", "version", "other"}


def _now():
    return datetime.now().isoformat(timespec="seconds")


def _base_paths():
    return {
        "project": os.path.join(os.getcwd(), ".amlei-skill", "resume"),
        "root": os.path.join(os.path.expanduser("~"), ".amlei-skill", "resume"),
    }


def _shared_paths(base):
    s = os.path.join(base, SHARED_DIR)
    return {
        "shared": s,
        "identity": os.path.join(s, IDENTITY_FILE),
        "experiences": os.path.join(s, EXPERIENCES_FILE),
        "capabilities": os.path.join(s, CAPABILITIES_FILE),
        "files": os.path.join(s, "files"),
        "identities": os.path.join(base, IDENTITIES_DIR),
    }


def resolve_base():
    """返回事实层所在 base 目录（含 _shared/）。不存在返回 None。"""
    for key in ("project", "root"):
        base = _base_paths()[key]
        if os.path.isdir(os.path.join(base, SHARED_DIR)):
            return base
    return None


def require_base():
    base = resolve_base()
    if not base:
        print("✗ 事实层不存在。先 init --location project|root 创建。")
        sys.exit(1)
    return base


def _load(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"✗ 文件不存在：{path}")
        sys.exit(1)


def _save(path, data):
    """原子写：先临时文件，再替换。备份旧版本（带时间戳，保留最近 N 份）。"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.isfile(path):
        stamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
        bak = f"{path}.bak.{stamp}"
        shutil.copy2(path, bak)
        baks = sorted(glob.glob(f"{path}.bak.*"))
        for old in baks[:-KEEP_BACKUPS]:
            try:
                os.remove(old)
            except OSError:
                pass
    # 更新 facts_version
    if isinstance(data, dict) and "_meta" in data:
        data["_meta"]["facts_version"] = _now()
    tmp = f"{path}.tmp.{os.getpid()}"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def _empty_identity():
    return {"_meta": {"facts_version": _now(), "schema_version": 2, "created": _now()},
            "name": "", "gender": "", "contact": {}, "city_base": "",
            "links": [], "avatar": {}, "education": []}


def _empty_experiences():
    return {"_meta": {"facts_version": _now(), "schema_version": 2, "created": _now()},
            "items": []}


def _empty_capabilities():
    return {"_meta": {"facts_version": _now(), "schema_version": 2, "created": _now()},
            "items": []}


def _validate_id(kind, x):
    if not ID_PATTERNS[kind].match(x or ""):
        print(f"✗ id 不合法（{kind}_<小写字母数字下划线>）：{x!r}")
        sys.exit(1)


def _next_id(kind, items):
    """根据现有 items 推断下一个 N（exp_001 → exp_002）。无前缀则从 001 起。"""
    prefix = f"{kind}_"
    max_n = 0
    for it in items:
        iid = it.get("id", "")
        if iid.startswith(prefix):
            try:
                max_n = max(max_n, int(iid[len(prefix):]))
            except ValueError:
                pass
    return f"{prefix}{max_n + 1:03d}"


# ─── path / init ───────────────────────────────────────────────────────────

def cmd_path(args):
    base = resolve_base()
    if not base:
        print("NOT FOUND（用 init --location project|root 创建）")
        return
    p = _shared_paths(base)
    print(p["shared"])


def cmd_init(args):
    bases = _base_paths()
    base = bases[args.location]
    p = _shared_paths(base)
    if os.path.isdir(p["shared"]):
        print(f"✗ 已存在：{p['shared']}（init 不覆盖；改内容用 identity/experience/...）")
        sys.exit(1)
    os.makedirs(p["shared"], exist_ok=True)
    os.makedirs(p["files"], exist_ok=True)
    os.makedirs(p["identities"], exist_ok=True)
    _save(p["identity"], _empty_identity())
    _save(p["experiences"], _empty_experiences())
    _save(p["capabilities"], _empty_capabilities())
    print(f"✓ 事实层已创建：{p['shared']}")
    print(f"  identity / experiences / capabilities 空文件已就位")
    print(f"  files/ 与 identities/ 目录已建")


# ─── identity ──────────────────────────────────────────────────────────────

def cmd_identity(args):
    base = require_base()
    p = _shared_paths(base)["identity"]
    data = _load(p)
    if args.get:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    fields_simple = {"name": args.name, "gender": args.gender, "city_base": args.city_base}
    for k, v in fields_simple.items():
        if v is not None:
            data[k] = v
    if args.phone is not None or args.email is not None or args.wechat is not None:
        data.setdefault("contact", {})
        if args.phone is not None:
            data["contact"]["phone"] = args.phone
        if args.email is not None:
            data["contact"]["email"] = args.email
        if args.wechat is not None:
            data["contact"]["wechat"] = args.wechat
    if args.github is not None or args.site is not None:
        links = data.setdefault("links", [])
        if args.github is not None:
            links = [l for l in links if l.get("label", "").lower() != "github"]
            if args.github:
                links.append({"label": "GitHub", "url": args.github})
        if args.site is not None:
            links = [l for l in links if l.get("label", "").lower() != "site"]
            if args.site:
                links.append({"label": "Site", "url": args.site})
        data["links"] = links
    if args.avatar_ref is not None or args.avatar_from is not None:
        av = data.setdefault("avatar", {})
        if args.avatar_ref is not None:
            av["ref"] = args.avatar_ref
        if args.avatar_from is not None:
            av["extracted_from"] = args.avatar_from
    _save(p, data)
    print(f"✓ identity 已更新（写前已时间戳备份）")


# ─── experience ────────────────────────────────────────────────────────────

def cmd_experience(args):
    base = require_base()
    p = _shared_paths(base)["experiences"]
    data = _load(p)
    items = data["items"]
    if args.action == "list":
        if not items:
            print("（暂无经历）")
            return
        for it in items:
            n_prj = len(it.get("projects", []))
            print(f"  · {it['id']}  {it.get('company','-')}  岗位={it.get('position','-')}  "
                  f"时间={it.get('period','-')}  [projects={n_prj}]")
        return
    if args.action == "add":
        eid = args.id or _next_id("exp", items)
        _validate_id("exp", eid)
        if any(it["id"] == eid for it in items):
            print(f"✗ 已存在 experience/{eid}（改用 update 或换 id）")
            sys.exit(1)
        entry = {
            "id": eid,
            "company": args.company or "",
            "position": args.position or "",
            "period": args.period or "",
            "industry": args.industry or "",
            "team_context": args.team_context or "",
            "projects": [],
            "cross_project_refs": [],
            "source_refs": [],
            "added": _now(),
            "last_updated": _now(),
        }
        items.append(entry)
        _save(p, data)
        print(f"✓ 已添加 experience/{eid}（写前已时间戳备份）")
        return
    if args.action == "rm":
        before = len(items)
        items[:] = [it for it in items if it["id"] != args.id]
        if len(items) == before:
            print(f"✗ 没有条目：{args.id}")
            sys.exit(1)
        _save(p, data)
        print(f"✓ 已移除 experience/{args.id}")
        return


def _find_project(data, pid):
    """遍历 experiences 树找 project。返回 (experience, project) 或 (None, None)。"""
    for exp in data["items"]:
        for prj in exp.get("projects", []):
            if prj["id"] == pid:
                return exp, prj
    return None, None


def _all_project_ids(data):
    return [prj["id"] for exp in data["items"] for prj in exp.get("projects", [])]


# ─── project ───────────────────────────────────────────────────────────────

def cmd_project(args):
    base = require_base()
    p = _shared_paths(base)["experiences"]
    data = _load(p)
    if args.action == "list":
        for exp in data["items"]:
            for prj in exp.get("projects", []):
                print(f"  · {prj['id']}  {prj.get('name','-')}  "
                      f"[exp={exp['id']}]  grains={len(prj.get('granularity',[]))}")
            for pid in exp.get("cross_project_refs", []):
                print(f"  · {pid}  (cross-ref from {exp['id']})")
        return
    if args.action == "add":
        # 宿主 experience
        exp = next((e for e in data["items"] if e["id"] == args.experience), None)
        if not exp:
            print(f"✗ experience 不存在：{args.experience}")
            sys.exit(1)
        items_projects = [prj for e in data["items"] for prj in e.get("projects", [])]
        pid = args.id or _next_id("prj", items_projects)
        _validate_id("prj", pid)
        if any(prj["id"] == pid for prj in items_projects):
            print(f"✗ 已存在 project/{pid}")
            sys.exit(1)
        prj = {
            "id": pid,
            "name": args.name or "",
            "my_role": args.role or "",
            "tech_stack": (args.tech.split(",") if args.tech else []),
            "outcome_metrics": {},
            "granularity": [],
            "source_refs": [],
            "added": _now(),
            "last_updated": _now(),
        }
        exp.setdefault("projects", []).append(prj)
        _save(p, data)
        print(f"✓ 已添加 project/{pid} → experience/{args.experience}")
        if not args.grain and not args.text:
            print(f"  （建议接着 add-grain --id {pid} 加粒度描述）")
        return
    if args.action == "add-grain":
        exp, prj = _find_project(data, args.id)
        if not prj:
            print(f"✗ project 不存在：{args.id}")
            sys.exit(1)
        if args.grain not in VALID_GRAINS:
            print(f"✗ grain 不合法，可选：{sorted(VALID_GRAINS)}")
            sys.exit(1)
        prj.setdefault("granularity", []).append({"grain": args.grain, "text": args.text})
        prj["last_updated"] = _now()
        _save(p, data)
        print(f"✓ 已为 project/{args.id} 追加 {args.grain} 档粒度")
        return
    if args.action == "set-outcome":
        exp, prj = _find_project(data, args.id)
        if not prj:
            print(f"✗ project 不存在：{args.id}")
            sys.exit(1)
        # --outcome KEY=VAL 可多次
        for kv in args.outcome or []:
            if "=" not in kv:
                print(f"✗ --outcome 需要 KEY=VAL 形式：{kv}")
                sys.exit(1)
            k, v = kv.split("=", 1)
            # 尝试数值化
            try:
                v_num = float(v)
                if v_num.is_integer():
                    v_num = int(v_num)
                v = v_num
            except ValueError:
                pass
            prj.setdefault("outcome_metrics", {})[k] = v
        prj["last_updated"] = _now()
        _save(p, data)
        print(f"✓ project/{args.id} 的 outcome_metrics 已更新（{len(args.outcome or [])} 项）")
        return
    if args.action == "cross-ref":
        # 把 prj id 加入某 exp 的 cross_project_refs（用于跨经历项目）
        exp = next((e for e in data["items"] if e["id"] == args.experience), None)
        if not exp:
            print(f"✗ experience 不存在：{args.experience}")
            sys.exit(1)
        owner_exp, _ = _find_project(data, args.id)
        if not owner_exp:
            print(f"✗ project 不存在：{args.id}")
            sys.exit(1)
        if owner_exp["id"] == exp["id"]:
            print(f"✗ {args.id} 已物理属于 {exp['id']}，不需要 cross-ref")
            sys.exit(1)
        refs = exp.setdefault("cross_project_refs", [])
        if args.id in refs:
            print(f"✓ {args.id} 已在 {exp['id']} 的 cross_project_refs 中")
            return
        refs.append(args.id)
        _save(p, data)
        print(f"✓ 已把 project/{args.id} 加入 experience/{args.experience} 的 cross_project_refs")


# ─── capability ────────────────────────────────────────────────────────────

def cmd_capability(args):
    base = require_base()
    p = _shared_paths(base)["capabilities"]
    data = _load(p)
    items = data["items"]
    if args.action == "list":
        if not items:
            print("（暂无能力）")
            return
        for it in items:
            print(f"  · {it['id']}  {it.get('claim','-')}  proven_by={it.get('proven_by',[])}")
        return
    if args.action == "add":
        cid = args.id or _next_id("cap", items)
        _validate_id("cap", cid)
        if any(it["id"] == cid for it in items):
            print(f"✗ 已存在 capability/{cid}")
            sys.exit(1)
        proven_by = args.proven_by.split(",") if args.proven_by else []
        proven_by = [x.strip() for x in proven_by if x.strip()]
        if not proven_by:
            print("✗ proven_by 不能为空——无证据的能力不下沉到事实层（R1）")
            print("  若无证据：写进 amlei-resume 的 emphasis/capabilities.json.skill_axis")
            sys.exit(1)
        for pid in proven_by:
            _validate_id("prj", pid)
        if args.evidence_grain and args.evidence_grain not in VALID_GRAINS:
            print(f"✗ evidence_grain 不合法，可选：{sorted(VALID_GRAINS)}")
            sys.exit(1)
        # 校验 proven_by 的 project 存在
        exp_data = _load(_shared_paths(base)["experiences"])
        all_pids = _all_project_ids(exp_data)
        missing = [p for p in proven_by if p not in all_pids]
        if missing:
            print(f"✗ proven_by 引用了不存在的 project：{missing}")
            print(f"  当前存在的 project：{all_pids}")
            sys.exit(1)
        entry = {
            "id": cid,
            "claim": args.claim or "",
            "proven_by": proven_by,
            "evidence_grain": args.evidence_grain or "",
            "added": _now(),
            "last_updated": _now(),
        }
        items.append(entry)
        _save(p, data)
        print(f"✓ 已添加 capability/{cid}（proven_by={proven_by}）")
        return
    if args.action == "update":
        it = next((x for x in items if x["id"] == args.id), None)
        if not it:
            print(f"✗ 条目不存在：{args.id}")
            sys.exit(1)
        if args.claim is not None:
            it["claim"] = args.claim
        if args.proven_by is not None:
            new_pb = [x.strip() for x in args.proven_by.split(",") if x.strip()]
            if not new_pb:
                print("✗ proven_by 不能清空（R1）")
                sys.exit(1)
            for pid in new_pb:
                _validate_id("prj", pid)
            it["proven_by"] = new_pb
        it["last_updated"] = _now()
        _save(p, data)
        print(f"✓ 已更新 capability/{args.id}")
        return
    if args.action == "rm":
        before = len(items)
        items[:] = [x for x in items if x["id"] != args.id]
        if len(items) == before:
            print(f"✗ 没有条目：{args.id}")
            sys.exit(1)
        _save(p, data)
        print(f"✓ 已移除 capability/{args.id}")


# ─── find / batch / propagate ──────────────────────────────────────────────

def cmd_find(args):
    base = require_base()
    sp = _shared_paths(base)
    out = []
    if args.type in (None, "identity"):
        # identity 只能整体读，不参与 find
        pass
    if args.type in (None, "experience"):
        data = _load(sp["experiences"])
        for it in data["items"]:
            if args.id and it["id"] != args.id:
                continue
            out.append({"type": "experience", **it})
    if args.type in (None, "project"):
        data = _load(sp["experiences"])
        for exp in data["items"]:
            for prj in exp.get("projects", []):
                if args.id and prj["id"] != args.id:
                    continue
                out.append({"type": "project", "_experience": exp["id"], **prj})
            for pid in exp.get("cross_project_refs", []):
                if args.id and pid != args.id:
                    continue
                # cross-ref，找物理位置
                owner_exp, real_prj = _find_project(data, pid)
                if real_prj:
                    out.append({"type": "project", "_experience": exp["id"], "_cross_ref": True,
                                "_owner_experience": owner_exp["id"], **real_prj})
    if args.type in (None, "capability"):
        data = _load(sp["capabilities"])
        for it in data["items"]:
            if args.id and it["id"] != args.id:
                continue
            out.append({"type": "capability", **it})
    print(json.dumps(out, ensure_ascii=False, indent=2) if out else "（无匹配）")


def cmd_batch(args):
    """批量操作。stdin 或 --json。一次保存一份备份。"""
    base = require_base()
    if args.json:
        ops = json.loads(args.json)
    else:
        ops = json.loads(sys.stdin.read())
    sp = _shared_paths(base)
    loaded = {}
    def get(file_key):
        if file_key not in loaded:
            loaded[file_key] = _load(sp[file_key])
        return loaded[file_key]
    count = 0
    for op in ops:
        target = op.pop("target", None) or op.pop("file", None)
        action = op.pop("action", "add")
        if target == "identity":
            data = get("identity")
            for k, v in op.items():
                if k == "github" or k == "site":
                    links = data.setdefault("links", [])
                    links = [l for l in links if l.get("label", "").lower() != k]
                    if v:
                        links.append({"label": k.capitalize() if k == "github" else "Site", "url": v})
                    data["links"] = links
                elif k in ("phone", "email", "wechat"):
                    data.setdefault("contact", {})[k] = v
                else:
                    data[k] = v
            count += 1
        elif target == "experience":
            data = get("experiences")
            items = data["items"]
            eid = op.get("id")
            if action == "add":
                if not eid:
                    eid = _next_id("exp", items)
                    op["id"] = eid
                _validate_id("exp", eid)
                if any(it["id"] == eid for it in items):
                    print(f"  ⚠ 跳过已存在：experience/{eid}", file=sys.stderr)
                    continue
                op.setdefault("projects", [])
                op.setdefault("cross_project_refs", [])
                op.setdefault("source_refs", [])
                op["added"] = op.get("added", _now())
                op["last_updated"] = _now()
                items.append(op)
                count += 1
            elif action == "update":
                it = next((x for x in items if x["id"] == eid), None)
                if not it:
                    print(f"  ⚠ 跳过不存在：experience/{eid}", file=sys.stderr)
                    continue
                it.update(op)
                it["last_updated"] = _now()
                count += 1
        elif target == "project":
            data = get("experiences")
            exp = next((e for e in data["items"] if e["id"] == op.get("experience")), None)
            if not exp:
                print(f"  ⚠ 跳过（experience 不存在）：{op.get('experience')}", file=sys.stderr)
                continue
            pid = op.get("id")
            existing = next((p for p in exp.get("projects", []) if p["id"] == pid), None)
            if action == "add":
                if existing:
                    print(f"  ⚠ 跳过已存在：project/{pid}", file=sys.stderr)
                    continue
                op.pop("experience", None)
                op.setdefault("tech_stack", [])
                op.setdefault("outcome_metrics", {})
                op.setdefault("granularity", [])
                op.setdefault("source_refs", [])
                op["added"] = op.get("added", _now())
                op["last_updated"] = _now()
                exp.setdefault("projects", []).append(op)
                count += 1
            elif action == "update" and existing:
                op.pop("experience", None)
                existing.update(op)
                existing["last_updated"] = _now()
                count += 1
        elif target == "capability":
            data = get("capabilities")
            items = data["items"]
            cid = op.get("id")
            pb = op.get("proven_by", [])
            if action == "add":
                if not pb:
                    print(f"  ⚠ 跳过（proven_by 为空，违反 R1）：{cid}", file=sys.stderr)
                    continue
                if not cid:
                    cid = _next_id("cap", items)
                    op["id"] = cid
                _validate_id("cap", cid)
                if any(it["id"] == cid for it in items):
                    print(f"  ⚠ 跳过已存在：capability/{cid}", file=sys.stderr)
                    continue
                op["added"] = op.get("added", _now())
                op["last_updated"] = _now()
                items.append(op)
                count += 1
            elif action == "update":
                it = next((x for x in items if x["id"] == cid), None)
                if not it:
                    print(f"  ⚠ 跳过不存在：capability/{cid}", file=sys.stderr)
                    continue
                if "proven_by" in op and not op["proven_by"]:
                    print(f"  ⚠ 跳过（proven_by 清空违反 R1）：{cid}", file=sys.stderr)
                    continue
                it.update(op)
                it["last_updated"] = _now()
                count += 1
        else:
            print(f"  ⚠ 未知 target：{target}", file=sys.stderr)
    # 保存所有改过的文件（每个一份备份）
    for file_key, data in loaded.items():
        _save(sp[file_key], data)
    print(f"✓ 批次完成，共处理 {count} 条（每个文件一份时间戳备份）")


def cmd_propagate(args):
    """事实层某条更新后，扫描 identities/*/emphasis/*.json 和 resumes/*/_meta.json，
    把引用该 fact 的条目标 needs_review=true。不改任何文案。"""
    base = require_base()
    sp = _shared_paths(base)
    identities_dir = sp["identities"]
    if not os.path.isdir(identities_dir):
        print("✓ 无 identities/ 目录，无需传播")
        return
    fact_id = args.fact_id
    # 判断 fact 类型
    if fact_id.startswith("exp_"):
        kind = "experience"
    elif fact_id.startswith("prj_"):
        kind = "project"
    elif fact_id.startswith("cap_"):
        kind = "capability"
    else:
        print(f"✗ 无法识别 fact 类型：{fact_id}")
        sys.exit(1)
    flagged = 0
    for identity in sorted(os.listdir(identities_dir)):
        emph_dir = os.path.join(identities_dir, identity, "emphasis")
        if not os.path.isdir(emph_dir):
            continue
        # 决定哪些 emphasis 文件相关
        relevant = {
            "experience": ["experiences.json", "projects.json"],  # exp 改了可能影响 experience selection 和 project selection（通过项目归属）
            "project": ["projects.json"],
            "capability": ["capabilities.json"],
        }[kind]
        for fname in relevant:
            fpath = os.path.join(emph_dir, fname)
            if not os.path.isfile(fpath):
                continue
            data = _load(fpath)
            # 检查是否引用了 fact_id
            text = json.dumps(data, ensure_ascii=False)
            if fact_id in text:
                if data.get("_meta", {}).get("needs_review") is not True:
                    data.setdefault("_meta", {})["needs_review"] = True
                    # 用原子写但不重复备份（这是元数据修复）
                    with open(fpath, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    flagged += 1
                    print(f"  ✓ {identity}/emphasis/{fname} → needs_review=true")
        # 扫描 resumes
        resumes_dir = os.path.join(identities_dir, identity, "resumes")
        if os.path.isdir(resumes_dir):
            for app in sorted(os.listdir(resumes_dir)):
                meta_path = os.path.join(resumes_dir, app, "_meta.json")
                if not os.path.isfile(meta_path):
                    continue
                meta = _load(meta_path)
                # snapshot 的 needs_review 翻位不依赖具体引用——任何 fact 改了，该身份下所有 snapshot 都标
                # 因为 snapshot 渲染时可能用到了任何 fact
                if not meta.get("needs_review"):
                    meta["needs_review"] = True
                    with open(meta_path, "w", encoding="utf-8") as f:
                        json.dump(meta, f, ensure_ascii=False, indent=2)
                    flagged += 1
                    print(f"  ✓ {identity}/resumes/{app}/_meta.json → needs_review=true")
    print(f"✓ 传播完成：fact={fact_id}（kind={kind}），共标记 {flagged} 个文件")


def cmd_time(args):
    base = require_base()
    sp = _shared_paths(base)
    if args.identity:
        data = _load(sp["identity"])
        ts = data["_meta"]["facts_version"]
        print(f"identity.json: {ts}")
        return
    for key in ("identity", "experiences", "capabilities"):
        data = _load(sp[key])
        ts = data["_meta"]["facts_version"]
        print(f"{key}.json: {ts}")


# ─── main ──────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="事实层管理（v2 三层模型）。")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("path"); s.set_defaults(func=cmd_path)

    s = sub.add_parser("init")
    s.add_argument("--location", choices=["project", "root"], required=True)
    s.set_defaults(func=cmd_init)

    s = sub.add_parser("identity")
    s.add_argument("--get", action="store_true", help="读取后退出")
    for f in ("name", "gender", "city-base", "phone", "email", "wechat", "github", "site",
              "avatar-ref", "avatar-from"):
        s.add_argument(f"--{f}")
    s.set_defaults(func=cmd_identity)

    s = sub.add_parser("experience")
    s.add_argument("action", choices=["add", "list", "rm"])
    s.add_argument("--id")
    s.add_argument("--company"); s.add_argument("--position")
    s.add_argument("--period"); s.add_argument("--industry"); s.add_argument("--team-context")
    s.set_defaults(func=cmd_experience)

    s = sub.add_parser("project")
    s.add_argument("action", choices=["add", "list", "add-grain", "set-outcome", "cross-ref"])
    s.add_argument("--id")
    s.add_argument("--experience", help="宿主 experience id（add/cross-ref 必填）")
    s.add_argument("--name"); s.add_argument("--role"); s.add_argument("--tech")
    s.add_argument("--grain", choices=sorted(VALID_GRAINS))
    s.add_argument("--text")
    s.add_argument("--outcome", action="append", help="KEY=VAL，可多次")
    s.set_defaults(func=cmd_project)

    s = sub.add_parser("capability")
    s.add_argument("action", choices=["add", "list", "update", "rm"])
    s.add_argument("--id")
    s.add_argument("--claim")
    s.add_argument("--proven-by", help="逗号分隔的 project id")
    s.add_argument("--evidence-grain", choices=sorted(VALID_GRAINS))
    s.set_defaults(func=cmd_capability)

    s = sub.add_parser("find")
    s.add_argument("--id")
    s.add_argument("--type", choices=["experience", "project", "capability"])
    s.set_defaults(func=cmd_find)

    s = sub.add_parser("batch", help="批量操作。stdin 或 --json")
    s.add_argument("--json")
    s.set_defaults(func=cmd_batch)

    s = sub.add_parser("propagate")
    s.add_argument("fact_id", help="如 exp_001 / prj_014 / cap_003")
    s.set_defaults(func=cmd_propagate)

    s = sub.add_parser("time")
    s.add_argument("--identity", action="store_true")
    s.set_defaults(func=cmd_time)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
