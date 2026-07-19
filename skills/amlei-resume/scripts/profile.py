#!/usr/bin/env python3
"""amlei-resume 的个人资料管理（KV 存储）。

个人资料是简历生成的素材库——所以：
  · 位置优先项目级 <cwd>/.amlei-skill/resume/profile.json，
    否则用户根目录 ~/.amlei-skill/resume/profile.json。
   · **优先使用 batch**（单次保存一份备份）；add/update 单条命令也保留但每次各写一份备份。
   · init 不覆盖已有；add/update/profile/preference/target/experience/education 写前自动备份**带时间戳**，保留最近 N 份。
  · 调用写入命令前，Agent 必须已征得用户同意（本脚本不替你问）。

退出码：0 正常；1 资料不存在 / 条目不存在 / 已存在不覆盖 / 参数错。
"""

import argparse
import glob
import json
import os
import shutil
import sys
from datetime import datetime

FILE = "profile.json"
KEEP_BACKUPS = 10


def _paths():
    return {
        "project": os.path.join(os.getcwd(), ".amlei-skill", "resume", FILE),
        "root": os.path.join(os.path.expanduser("~"), ".amlei-skill", "resume", FILE),
    }


def resolve():
    p = _paths()
    if os.path.isfile(p["project"]):
        return p["project"]
    if os.path.isfile(p["root"]):
        return p["root"]
    return None


def require():
    p = resolve()
    if not p:
        print("✗ profile 不存在。先 init --location project|root 创建。")
        sys.exit(1)
    return p


def _load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _save(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.isfile(path):
        stamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")  # 带微秒，每次写入独立备份
        shutil.copy2(path, f"{path}.bak.{stamp}")          # 带时间戳备份
        baks = sorted(glob.glob(f"{path}.bak.*"))
        for old in baks[:-KEEP_BACKUPS]:                    # 只留最近 N 份
            try:
                os.remove(old)
            except OSError:
                pass
    data["_meta"]["last_updated"] = datetime.now().isoformat(timespec="seconds")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _empty():
    now = datetime.now().isoformat(timespec="seconds")
    return {"_meta": {"created": now, "last_updated": now},
            "profile": {}, "preferences": {}, "targets": {}, "target_companies": {},
            "experiences": {}, "educations": {}, "abilities": {}, "projects": {}}


def _section(data, type_):
    return data["abilities"] if type_ == "ability" else data["projects"]


def cmd_path(args):
    p = resolve()
    print(p if p else "NOT FOUND（用 init --location project|root 创建）")


def cmd_init(args):
    p = _paths()[args.location]
    if os.path.isfile(p):
        print(f"✗ 已存在：{p}（init 不覆盖；改内容用 add/update/profile/target）")
        sys.exit(1)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(_empty(), f, ensure_ascii=False, indent=2)
    print(f"✓ 已创建 profile：{p}")


def cmd_profile(args):
    p = require()
    data = _load(p)
    fields = {"name": args.name, "gender": args.gender, "phone": args.phone,
              "email": args.email, "city": args.city, "github": args.github,
              "site": args.site, "avatar": args.avatar}
    given = {k: v for k, v in fields.items() if v is not None}
    if not given:                                  # 只读
        print(json.dumps(data.get("profile", {}), ensure_ascii=False, indent=2))
        return
    data.setdefault("profile", {}).update(given)
    _save(p, data)
    print(f"✓ profile 已更新字段：{', '.join(given)}（写前已时间戳备份）")


def cmd_education(args):
    p = require()
    data = _load(p)
    data.setdefault("educations", {})
    now = datetime.now().isoformat(timespec="seconds")
    if args.action == "list":
        if not data["educations"]:
            print("（暂无教育经历）")
        else:
            for k, v in data["educations"].items():
                deg = v.get("degree", "")
                grad = v.get("graduation", "")
                major = v.get("major", "")
                print(f"  · {k}  {deg}{' · '+major if major else ''}  {grad}")
    elif args.action == "add":
        if not args.key:
            print("✗ education add 需要学校名"); sys.exit(1)
        entry = {"degree": args.degree or "", "major": args.major or "",
                 "graduation": args.graduation or "",
                 "added": data["educations"].get(args.key, {}).get("added", now),
                 "last_updated": now}
        data["educations"][args.key] = entry
        _save(p, data)
        print(f"✓ 已添加教育经历：{args.key}（写前已时间戳备份）")
    elif args.action == "rm":
        if args.key not in data["educations"]:
            print(f"✗ 没有这所学校：{args.key}"); sys.exit(1)
        del data["educations"][args.key]
        _save(p, data)
        print(f"✓ 已移除教育经历：{args.key}（写前已时间戳备份）")


def cmd_preference(args):
    p = require()
    data = _load(p)
    fields = {"city": args.city, "job_type": args.job_type,
              "salary": args.salary, "exp": args.exp, "degree": args.degree,
              "scale": args.scale, "industry": args.industry}
    given = {k: v for k, v in fields.items() if v is not None}
    if not given:
        print(json.dumps(data.get("preferences", {}), ensure_ascii=False, indent=2))
        return
    data.setdefault("preferences", {}).update(given)
    _save(p, data)
    print(f"✓ 求职偏好已更新字段：{', '.join(given)}（写前已时间戳备份）")


def cmd_target(args):
    p = require()
    data = _load(p)
    data.setdefault("targets", {})
    now = datetime.now().isoformat(timespec="seconds")
    if args.action == "list":
        if not data["targets"]:
            print("（暂无在投岗位）")
        else:
            for k, v in data["targets"].items():
                print(f"  · {k}  城市={v.get('city','-')}  年限={v.get('years','-')}  tags={','.join(v.get('tags',[])) or '-'}")
    elif args.action == "add":
        if not args.position:
            print("✗ target add 需要岗位名"); sys.exit(1)
        entry = {"city": args.city, "years": args.years,
                 "tags": (args.tags.split(",") if args.tags else []),
                 "added": data["targets"].get(args.position, {}).get("added", now),
                 "last_updated": now}
        data["targets"][args.position] = entry
        _save(p, data)
        print(f"✓ 已标记在投岗位：{args.position}（写前已时间戳备份）")
    elif args.action == "rm":
        if args.position not in data["targets"]:
            print(f"✗ 没有这个岗位：{args.position}"); sys.exit(1)
        del data["targets"][args.position]
        _save(p, data)
        print(f"✓ 已移除岗位：{args.position}（写前已时间戳备份）")


def cmd_company(args):
    p = require()
    data = _load(p)
    data.setdefault("target_companies", {})
    now = datetime.now().isoformat(timespec="seconds")
    if args.action == "list":
        if not data["target_companies"]:
            print("（暂无关注公司）")
        else:
            for k, v in data["target_companies"].items():
                jd = v.get("jd", "")[:60]
                print(f"  · {k}  行业={v.get('industry','-')}  岗位={v.get('position','-')}  JD={jd}{'...' if len(v.get('jd','')) > 60 else ''}")
    elif args.action == "add":
        if not args.key:
            print("✗ company add 需要公司名"); sys.exit(1)
        entry = {"position": args.position or "", "industry": args.industry or "",
                 "jd": args.jd or "", "url": args.url or "",
                 "added": data["target_companies"].get(args.key, {}).get("added", now),
                 "last_updated": now}
        data["target_companies"][args.key] = entry
        _save(p, data)
        print(f"✓ 已添加关注公司：{args.key}（写前已时间戳备份）")
    elif args.action == "rm":
        if args.key not in data["target_companies"]:
            print(f"✗ 没有这家公司：{args.key}"); sys.exit(1)
        del data["target_companies"][args.key]
        _save(p, data)
        print(f"✓ 已移除公司：{args.key}（写前已时间戳备份）")


def _age(iso):
    """用脚本的真实时钟算距今多久——判过时不依赖模型的时间感。"""
    try:
        d = (datetime.now() - datetime.fromisoformat(iso)).days
    except Exception:
        return "?"
    if d <= 0:
        return "今天"
    if d < 30:
        return f"{d} 天前"
    if d < 365:
        return f"{d // 30} 个月前"
    return f"{d // 365} 年前"


def cmd_time(args):
    p = require()
    data = _load(p)
    if args.key:
        for t in ("ability", "project"):
            sec = _section(data, t)
            if args.key in sec:
                ts = sec[args.key].get("last_updated", "?")
                print(f"{ts}  （{_age(ts)}）")
                return
        print(f"✗ 条目不存在：{args.key}")
        sys.exit(1)
    ts = data["_meta"]["last_updated"]
    print(f"{ts}  （{_age(ts)}）")


def cmd_experience(args):
    p = require()
    data = _load(p)
    data.setdefault("experiences", {})
    now = datetime.now().isoformat(timespec="seconds")
    if args.action == "list":
        if not data["experiences"]:
            print("（暂无工作经历）")
        else:
            for k, v in data["experiences"].items():
                print(f"  · {k}  岗位={v.get('position','-')}  时间={v.get('period','-')}")
    elif args.action == "add":
        if not args.key:
            print("✗ experience add 需要公司名"); sys.exit(1)
        entry = {"position": args.position or "", "period": args.period or "",
                 "industry": args.industry or "",
                 "added": data["experiences"].get(args.key, {}).get("added", now),
                 "last_updated": now}
        data["experiences"][args.key] = entry
        _save(p, data)
        print(f"✓ 已添加工作经历：{args.key}（写前已时间戳备份）")
    elif args.action == "rm":
        if args.key not in data["experiences"]:
            print(f"✗ 没有这家公司：{args.key}"); sys.exit(1)
        del data["experiences"][args.key]
        _save(p, data)
        print(f"✓ 已移除工作经历：{args.key}（写前已时间戳备份）")


def cmd_find(args):
    p = require()
    data = _load(p)
    out = []
    types = [args.type] if args.type else ["ability", "project"]
    for t in types:
        sec = _section(data, t)
        for k, v in sec.items():
            if args.key and k != args.key:
                continue
            if args.category and v.get("category") != args.category:
                continue
            if args.tag and args.tag not in (v.get("tags") or []):
                continue
            out.append({"type": t, "key": k, **v, "age": _age(v.get("last_updated", ""))})
    print(json.dumps(out, ensure_ascii=False, indent=2) if out else "（无匹配）")


def cmd_batch(args):
    """批量写入多条条目，一次保存（一份备份）。"""
    import json as _json
    p = require()
    data = _load(p)

    if args.json:
        entries = _json.loads(args.json)
    else:
        entries = _json.loads(sys.stdin.read())

    now = datetime.now().isoformat(timespec="seconds")
    count = 0
    for entry in entries:
        action = entry.pop("action", "add")
        type_ = entry.pop("type", "ability")
        key = entry.pop("key", "")
        if not key:
            continue
        sec = _section(data, type_)
        if action == "add":
            if key in sec:
                print(f"  ⚠ 跳过已存在：{type_}/{key}", file=sys.stderr)
                continue
            entry.setdefault("last_updated", now)
            sec[key] = entry
        elif action == "update":
            if key not in sec:
                print(f"  ⚠ 跳过不存在：{type_}/{key}", file=sys.stderr)
                continue
            field = entry.pop("field", "")
            if field:
                val = entry.pop("value", "")
                if field in ("tags", "tech"):
                    val = val.split(",")
                elif field == "long_term":
                    val = val.lower() in ("true", "1", "yes", "y")
                sec[key][field] = val
            else:
                sec[key].update(entry)
            sec[key]["last_updated"] = now
        count += 1
    _save(p, data)
    print(f"✓ 批次完成，共处理 {count} 条（写前已时间戳备份）")


def cmd_add(args):
    p = require()
    data = _load(p)
    sec = _section(data, args.type)
    if args.key in sec:
        print(f"✗ 已存在 {args.type}/{args.key}（改用 update）")
        sys.exit(1)
    now = datetime.now().isoformat(timespec="seconds")
    entry = {"value": args.value,
             "tags": (args.tags.split(",") if args.tags else []),
             "long_term": args.long_term, "last_updated": now}
    if args.type == "ability":
        entry["category"] = args.category or "hard"
    else:
        entry["tech"] = (args.tech.split(",") if args.tech else [])
        if args.url:
            entry["url"] = args.url
        if args.role:
            entry["role"] = args.role
        if args.outcome:
            entry["outcome"] = args.outcome
    sec[args.key] = entry
    _save(p, data)
    print(f"✓ 已新增 {args.type}/{args.key}（写前已时间戳备份）")


def cmd_update(args):
    p = require()
    data = _load(p)
    sec = _section(data, args.type)
    if args.key not in sec:
        print(f"✗ 条目不存在：{args.type}/{args.key}")
        sys.exit(1)
    entry = sec[args.key]
    field = args.field
    if field in ("tags", "tech"):
        val = args.value.split(",")
    elif field == "long_term":
        val = args.value.lower() in ("true", "1", "yes", "y")
    else:
        val = args.value
    entry[field] = val
    entry["last_updated"] = datetime.now().isoformat(timespec="seconds")
    _save(p, data)
    print(f"✓ 已更新 {args.type}/{args.key}.{field}（写前已时间戳备份）")


def main():
    ap = argparse.ArgumentParser(description="个人资料管理（KV）。")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("path"); s.set_defaults(func=cmd_path)

    s = sub.add_parser("init")
    s.add_argument("--location", choices=["project", "root"], required=True)
    s.set_defaults(func=cmd_init)

    s = sub.add_parser("profile")
    for f in ("name", "gender", "phone", "email", "city", "github", "site", "avatar"):
        s.add_argument(f"--{f}")
    s.set_defaults(func=cmd_profile)

    s = sub.add_parser("preference")
    for f in ("city", "job_type", "salary", "exp", "degree", "scale", "industry"):
        s.add_argument(f"--{f}")
    s.set_defaults(func=cmd_preference)

    s = sub.add_parser("target")
    s.add_argument("action", choices=["add", "list", "rm"])
    s.add_argument("position", nargs="?")
    s.add_argument("--city"); s.add_argument("--years"); s.add_argument("--tags")
    s.set_defaults(func=cmd_target)

    s = sub.add_parser("target-company", help="管理目标公司 target_companies")
    s.add_argument("action", choices=["add", "list", "rm"])
    s.add_argument("--key"); s.add_argument("--position"); s.add_argument("--industry")
    s.add_argument("--jd"); s.add_argument("--url")
    s.set_defaults(func=cmd_company)

    s = sub.add_parser("experience")
    s.add_argument("action", choices=["add", "list", "rm"])
    s.add_argument("--key"); s.add_argument("--position"); s.add_argument("--period")
    s.add_argument("--industry")
    s.set_defaults(func=cmd_experience)

    s = sub.add_parser("education")
    s.add_argument("action", choices=["add", "list", "rm"])
    s.add_argument("--key"); s.add_argument("--degree"); s.add_argument("--major")
    s.add_argument("--graduation")
    s.set_defaults(func=cmd_education)

    s = sub.add_parser("time"); s.add_argument("--key"); s.set_defaults(func=cmd_time)

    s = sub.add_parser("find")
    s.add_argument("--key"); s.add_argument("--tag")
    s.add_argument("--category", choices=["hard", "soft"])
    s.add_argument("--type", choices=["ability", "project"])
    s.set_defaults(func=cmd_find)

    s = sub.add_parser("batch", help="(优先) 批量处理多条操作，一次保存。传 --json 字符串或 stdin 管道")
    s.add_argument("--json", help="JSON 字符串（不传则读 stdin）")
    s.set_defaults(func=cmd_batch)

    s = sub.add_parser("add")
    s.add_argument("--type", choices=["ability", "project"], required=True)
    s.add_argument("--key", required=True); s.add_argument("--value", required=True)
    s.add_argument("--category", choices=["hard", "soft"])
    s.add_argument("--tags"); s.add_argument("--long-term", action="store_true")
    s.add_argument("--url"); s.add_argument("--tech"); s.add_argument("--role"); s.add_argument("--outcome")
    s.set_defaults(func=cmd_add)

    s = sub.add_parser("update")
    s.add_argument("--type", choices=["ability", "project"], required=True)
    s.add_argument("--key", required=True); s.add_argument("--field", required=True)
    s.add_argument("--value", required=True)
    s.set_defaults(func=cmd_update)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
