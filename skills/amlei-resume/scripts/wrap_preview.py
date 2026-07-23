#!/usr/bin/env python3
"""把渲染好的简历正文（<style> + 原子）包进带「导出 PDF」工具条的 A4 预览页。

主题无关的机械包装：产物开头的 <style> 注入外壳 <head>、其余原子注入 #source；姓名 / 岗位自动抽取做文件名与 document.title。按钮 / 分页 JS / 打印规则都在外壳里——导出的 A4 / PDF 不含工具条。默认输出 resume/<姓名>/<求职岗位>/预览.html（自动建目录）。
"""

import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SHELL = os.path.normpath(os.path.join(HERE, "..", "assets", "preview-shell.html"))

STYLE_RE = re.compile(r"^\s*(<style\b[^>]*>.*?</style>)\s*(.*)", re.I | re.S)
NAME_RE = re.compile(r'class="(?:name|cn)"[^>]*>\s*([^<]+?)\s*<', re.I)
ROLE_RE = re.compile(r'class="role"[^>]*>\s*([^<]+?)\s*<', re.I)
PLACEHOLDER_RE = re.compile(r"\{\{[^}]+\}\}")
UNSAFE_FS = re.compile(r'[\\/:*?"<>|\s]+')


def derive_name(body_html, fallback):
    """取 <span class="name"> / .cn 里的姓名；否则用文件名。"""
    m = NAME_RE.search(body_html)
    return m.group(1).strip() if m and m.group(1).strip() else fallback


def _clean_role(raw):
    """把 role 文本清洗成简短岗位名（用于文件名）：去"意向岗位/求职意向"等前缀、
    取首段（/ · — , 前）、去尾部括注、去空格。"""
    raw = re.sub(r"^(意向岗位|求职意向|目标岗位|申请方向)\s*[：:·.\-\s]*", "", raw.strip())
    raw = re.split(r"\s*[/·—,，]\s*", raw)[0]
    raw = re.sub(r"[（(][^）)]*[）)]\s*$", "", raw).strip()
    return raw.replace(" ", "").strip()


def derive_role(body_html):
    m = ROLE_RE.search(body_html)
    return _clean_role(m.group(1)) if m else ""


def main():
    ap = argparse.ArgumentParser(description="把简历正文包进 A4 预览外壳（带导出 PDF）。")
    ap.add_argument("body", help="渲染产物 HTML（开头 <style> + 原子）路径")
    ap.add_argument("output", nargs="?", help="输出路径，默认 <body>_预览.html")
    ap.add_argument("--name", help="覆盖 document.title（= PDF 默认文件名）；默认自动取 姓名-求职岗位")
    args = ap.parse_args()

    if not os.path.isfile(args.body):
        print(f"✗ 找不到文件: {args.body}")
        sys.exit(1)
    if not os.path.isfile(SHELL):
        print(f"✗ 找不到预览外壳: {SHELL}")
        sys.exit(1)

    content = open(args.body, encoding="utf-8").read().strip()
    shell = open(SHELL, encoding="utf-8").read()

    # 1) 拆出开头的 <style>（主题样式）和正文原子
    m = STYLE_RE.match(content)
    if m:
        style_html, body_html = m.group(1), m.group(2).strip()
    else:
        style_html, body_html = "", content

    if not body_html:
        print("✗ 正文为空：渲染产物里没有除 <style> 以外的内容")
        sys.exit(1)

    # 2) 姓名 / 求职岗位：从产物自动抽取；--name 仅覆盖 document.title（PDF 默认文件名）
    fallback = re.sub(r"[_-](body|正文|atoms)$", "",
                      os.path.splitext(os.path.basename(args.body))[0], flags=re.I)
    name = derive_name(body_html, fallback)
    role = derive_role(body_html)
    safe_name = UNSAFE_FS.sub("", name) or "resume"
    safe_role = UNSAFE_FS.sub("", role)
    title = args.name or (f"{name}-{role}" if role else name)

    # 3) 注入三个槽位
    out = (shell
           .replace("<!--RESUME_STYLE-->", style_html)
           .replace("<!--RESUME_BODY-->", body_html)
           .replace("{{TITLE}}", title))

    leftover = PLACEHOLDER_RE.findall(out)
    if leftover:
        print(f"⚠️  预览页里仍有 {len(leftover)} 处未填充占位符 {set(leftover)}——"
              f"检查未填充的 {{...}} 占位符")

    # 4) 输出路径：默认 resume/<姓名>/<求职岗位>/预览.html（证件照/MD 也放该目录）
    if args.output:
        out_path = args.output
    elif safe_role:
        out_path = os.path.join("resume", safe_name, safe_role, "预览.html")
    else:
        out_path = os.path.join("resume", safe_name, "预览.html")
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    open(out_path, "w", encoding="utf-8").write(out)
    print(f"✓ 已生成 A4 预览页: {out_path}")
    print(f"  目录 = resume/<姓名>/<求职岗位>/；document.title = {title}（PDF 默认文件名）。")


if __name__ == "__main__":
    main()
