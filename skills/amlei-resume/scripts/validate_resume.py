#!/usr/bin/env python3
"""简历格式校验器（确定性兜底）。按扩展名自动判断：.md 校验简历 MD 格式（self-intro 首模块 / 必填字段 / 标题层级 / 空模块 / date 格式）；.html 校验渲染产物（无残留 {{占位符}} / 有 Header / 有分节）。退出码：1 = 有 ERROR；0 = 通过。
"""

import argparse
import os
import re
import sys

# —— 简历 MD 规则 ——
SELF_INTRO_SLUGS = {"self-intro", "self_intro", "selfintro", "self intro", "个人信息", "基本信息"}
REQUIRED_INTRO_KEYS = ["name"]            # self-intro 必填
KNOWN_INTRO_KEYS = {                      # 已知键（出现未知键只提示）
    "name", "role", "gender", "location", "phone", "phone-number",
    "email", "site", "github", "csdn", "blog", "website", "linkedin",
    "portfolio", "avatar", "age", "birth", "political", "hometown",
    "ethnicity", "education-level", "platform",
}
H1_RE = re.compile(r"^#\s+(.+?)\s*$")
H2_RE = re.compile(r"^##\s+(.+?)\s*$")
H_DEEP_RE = re.compile(r"^#{3,}\s+")      # ### 及更深：只支持 # 和 ##
DATE_RE = re.compile(r"^date:\s*(\d{4}\.\d{2})\s*[-—–]\s*(\d{4}\.\d{2}|至今)\s*$")
KV_RE = re.compile(r"^([A-Za-z一-龥][\w一-龥\-]*)\s*:\s*(.+)$")

# —— 渲染产物 HTML 规则 ——
PLACEHOLDER_RE = re.compile(r"\{\{[^}]+\}\}")


def validate_md(text, name):
    errors, warnings = [], []

    lines = text.splitlines()
    h1_idx = [i for i, ln in enumerate(lines) if H1_RE.match(ln)]
    if not h1_idx:
        errors.append("没有任何 `# 一级标题`——至少要有 `# self-intro` 首模块")
        return errors, warnings

    first = H1_RE.match(lines[h1_idx[0]]).group(1).strip().lower()
    if first not in SELF_INTRO_SLUGS:
        errors.append(
            f"第一个一级标题必须是 `# self-intro`（当前是「{lines[h1_idx[0]].strip()}」）")

    # —— self-intro 块：从首个 # 到下一个 # 之间 ——
    intro_end = h1_idx[1] if len(h1_idx) > 1 else len(lines)
    intro_lines = lines[h1_idx[0] + 1:intro_end]
    intro_kv = {}
    for ln in intro_lines:
        m = KV_RE.match(ln.strip())
        if m:
            intro_kv[m.group(1).lower()] = m.group(2).strip()
    for k in REQUIRED_INTRO_KEYS:
        if k not in intro_kv or not intro_kv[k]:
            errors.append(f"self-intro 缺必填字段 `name:`（简历必须有姓名）")
            break
    unknown = sorted(set(intro_kv) - KNOWN_INTRO_KEYS)
    if unknown:
        warnings.append(f"self-intro 有未知字段 {unknown}（不影响，仅提示）")

    avatar = intro_kv.get("avatar", "").strip()
    if avatar:
        base_dir = os.path.dirname(os.path.abspath(name)) if name != "<stdin>" else "."
        if not os.path.isfile(os.path.join(base_dir, avatar)):
            warnings.append(f"self-intro 的 avatar 路径不存在: {avatar}")

    # —— 标题层级 / 空标题 ——
    for i, ln in enumerate(lines):
        if H_DEEP_RE.match(ln):
            warnings.append(f"第 {i + 1} 行出现 `###`+ 深标题，本格式只支持 `#`/`##`：{ln.strip()}")
        m = H1_RE.match(ln) or H2_RE.match(ln)
        if m and not m.group(1).strip():
            errors.append(f"第 {i + 1} 行标题为空：{ln}")

    # —— 空模块：某 `#` 到下一个 `#`/`##` 之间没有任何非空非注释正文 ——
    h_starts = [i for i, ln in enumerate(lines) if H1_RE.match(ln)]
    h_starts.append(len(lines))
    for a, b in zip(h_starts[:-1], h_starts[1:]):
        has_sub = any(H2_RE.match(lines[j]) for j in range(a + 1, b))
        has_body = any(lines[j].strip() and not H2_RE.match(lines[j])
                       for j in range(a + 1, b))
        title = H1_RE.match(lines[a]).group(1).strip()
        if not has_sub and not has_body and title.lower() not in SELF_INTRO_SLUGS:
            warnings.append(f"模块「{title}」是空模块（标题下没有任何内容）")

    # —— date 格式校验 ——
    for i, ln in enumerate(lines):
        if ln.strip().startswith("date:"):
            if not DATE_RE.match(ln.strip()):
                errors.append(
                    f"第 {i + 1} 行 date 格式错误：{ln.strip()}。"
                    "正确格式：date: 2024.07 — 2025.03 或 date: 2024.07 — 至今")

    return errors, warnings


def validate_html(text):
    errors, warnings = [], []
    leftover = PLACEHOLDER_RE.findall(text)
    if leftover:
        sample = ", ".join(sorted(set(leftover)))
        errors.append(f"产物里有 {len(leftover)} 处未填充占位符（{sample}）——"
                      "把组件模板里的 {{...}} 全部换成真实内容")
    if not re.search(r'class="name"|class="cn"|<header', text, re.I):
        errors.append("产物里没有 Header（姓名区 .name / .cn / <header>）——self-intro 应渲染成 Header")
    n_sec = len(re.findall(r'class="sec-h(?:ead)?"', text))
    if n_sec == 0:
        warnings.append("产物里没有任何章节标题（.sec-head / .sec-h）——至少要有一个 `# 模块`")
    if "<style" not in text.lower():
        warnings.append("产物里没有 <style>——主题样式缺失，wrap_preview 会得到无样式预览")
    return errors, warnings


def report(name, errors, warnings):
    print(f"📋 简历校验: {name}")
    if errors:
        print(f"\n❌ ERROR ×{len(errors)}（必须修复）:")
        for e in errors:
            print(f"   • {e}")
    if warnings:
        print(f"\n⚠️  WARNING ×{len(warnings)}（建议检查）:")
        for w in warnings:
            print(f"   • {w}")
    if not errors and not warnings:
        print("\n✅ 通过，无问题")
    elif not errors:
        print("\n✅ 无致命问题（warning 请人工确认）")


def main():
    ap = argparse.ArgumentParser(description="简历 MD / 渲染产物 HTML 校验。")
    ap.add_argument("file", nargs="?", help=".md 或 .html 文件路径")
    ap.add_argument("--md", action="store_true", help="强制按 MD 校验（支持 stdin）")
    ap.add_argument("--html", action="store_true", help="强制按 HTML 校验（支持 stdin）")
    args = ap.parse_args()

    if args.md or args.html:
        text = sys.stdin.read()
        name = "<stdin>"
        mode = "md" if args.md else "html"
    else:
        if not args.file:
            ap.error("请给文件路径，或用 --md/--html 从标准输入读")
        with open(args.file, encoding="utf-8", errors="replace") as f:
            text = f.read()
        name = args.file
        mode = "md" if args.file.lower().endswith(".md") else "html"

    if mode == "md":
        errors, warnings = validate_md(text, name)
    else:
        errors, warnings = validate_html(text)

    report(name, errors, warnings)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
