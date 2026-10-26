#!/usr/bin/env python3
"""把渲染好的简历正文（<style> + 原子）包进带「导出 PDF」工具条的 A4 预览页。

分页由 Paged.js 行级断行完成（替代旧版 JS 手动量原子高度装箱——后者会把整条 bullet
搬页造成 ~10 行留白）。本脚本只做机械包装：
  · 产物开头的 <style>（第一个是主题样式，后续可放产物定制样式）
    → 按「主题 → 共享 refinement → 产物定制」顺序注入外壳 B) <style> 的 <!--RESUME_STYLE-->
  · 其余原子 → 注入 #source 的 <!--RESUME_BODY-->（外层 .resume-root 已在外壳里）
  · scripts/paged.polyfill.js → 内联进 <!--PAGEDJS-->，使预览页自包含 / 离线可用
姓名 / 岗位自动抽取做 document.title（= PDF 默认文件名）。默认输出与 body.html 同目录的
预览.html；--output 覆盖。
"""

import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SHELL = os.path.join(HERE, "preview-shell.html")
PAGEDJS = os.path.join(HERE, "paged.polyfill.js")
REFINEMENT = os.path.join(HERE, "theme-refinement.css")

# 捕获产物开头的连续 <style ...>CSS</style>，group(2) = 内联 CSS 文本
STYLE_RE = re.compile(r"^\s*(<style\b[^>]*>)(.*?)</style>\s*", re.I | re.S)
NAME_RE = re.compile(r'class="(?:name|cn)"[^>]*>\s*([^<]+?)\s*<', re.I)
ROLE_RE = re.compile(r'class="role"[^>]*>\s*([^<]+?)\s*<', re.I)
PLACEHOLDER_RE = re.compile(r"\{\{[^}]+\}\}")
UNSAFE_FS = re.compile(r'[\\/:*?"<>|\s]+')


def derive_name(body_html, fallback):
    m = NAME_RE.search(body_html)
    return m.group(1).strip() if m and m.group(1).strip() else fallback


def _clean_role(raw):
    raw = re.sub(r"^(意向岗位|求职意向|目标岗位|申请方向)\s*[：:·.\-\s]*", "", raw.strip())
    raw = re.split(r"\s*[/·—,，]\s*", raw)[0]
    raw = re.sub(r"[（(][^）)]*[）)]\s*$", "", raw).strip()
    return raw.replace(" ", "").strip()


def derive_role(body_html):
    m = ROLE_RE.search(body_html)
    return _clean_role(m.group(1)) if m else ""


def split_leading_styles(content):
    """Return (CSS blocks in source order, remaining body HTML)."""
    styles = []
    body_html = content.strip()
    while True:
        m = STYLE_RE.match(body_html)
        if not m:
            return styles, body_html.strip()
        styles.append(m.group(2).strip())
        body_html = body_html[m.end():]


def main():
    ap = argparse.ArgumentParser(description="把简历正文包进 Paged.js A4 预览外壳（带导出 PDF）。")
    ap.add_argument("body", help="渲染产物 HTML（开头 <style> + 原子）路径")
    ap.add_argument("output", nargs="?", help="输出路径，默认 <body 同目录>/预览.html")
    ap.add_argument("--name", help="覆盖 document.title（= PDF 默认文件名）；默认自动取 姓名-求职岗位")
    ap.add_argument("--no-inline-js", action="store_true",
                    help="不内联 paged.polyfill.js，改为相对引用同目录文件（用于仓库内的参考 sample）")
    args = ap.parse_args()

    for f in (args.body, SHELL, PAGEDJS, REFINEMENT):
        if not os.path.isfile(f):
            print(f"✗ 找不到文件: {f}")
            sys.exit(1)

    content = open(args.body, encoding="utf-8").read().strip()
    shell = open(SHELL, encoding="utf-8").read()

    # 1) 拆出开头的连续 <style> 和正文原子。第一个是主题样式，
    #    其余是当前产物的定制覆盖；共享 refinement 固定在二者之间。
    styles, body_html = split_leading_styles(content)
    theme_css = styles[0] if styles else ""
    custom_css = "\n".join(styles[1:])
    refinement_css = open(REFINEMENT, encoding="utf-8").read().strip()
    style_css = "\n\n".join(part for part in (theme_css, refinement_css, custom_css) if part)

    if not body_html:
        print("✗ 正文为空：渲染产物里没有除 <style> 以外的内容")
        sys.exit(1)

    # 2) 姓名 / 求职岗位：从产物自动抽取；--name 仅覆盖 document.title
    fallback = re.sub(r"[_-](body|正文|atoms)$", "",
                      os.path.splitext(os.path.basename(args.body))[0], flags=re.I)
    name = derive_name(body_html, fallback)
    role = derive_role(body_html)
    safe_name = UNSAFE_FS.sub("", name) or "resume"
    safe_role = UNSAFE_FS.sub("", role)
    title = args.name or (f"{name}-{role}" if role else name)

    # 3) 输出路径：默认 <body 同目录>/预览.html；--output 覆盖（须先定，供下方算 vendor 相对路径）
    out_path = args.output or os.path.join(os.path.dirname(args.body) or ".", "预览.html")

    # 4) Paged.js：默认内联（预览页自包含 / 离线可用）；--no-inline-js 改相对引用（仓库参考 sample 用）
    if args.no_inline_js:
        rel = os.path.relpath(PAGEDJS, start=os.path.dirname(out_path) or ".")
        pagedjs_html = f'<script src="{rel}"></script>'
    else:
        pagedjs_js = open(PAGEDJS, encoding="utf-8").read()
        pagedjs_html = f"<script>{pagedjs_js}</script>"

    # 5) 注入四个槽位
    out = (shell
           .replace("<!--RESUME_STYLE-->", style_css)
           .replace("<!--RESUME_BODY-->", body_html)
           .replace("<!--PAGEDJS-->", pagedjs_html)
           .replace("{{TITLE}}", title))

    leftover = PLACEHOLDER_RE.findall(out)
    if leftover:
        print(f"⚠️  预览页里仍有 {len(leftover)} 处未填充占位符 {set(leftover)}")

    # 6) 写出
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    open(out_path, "w", encoding="utf-8").write(out)
    size_kb = len(out.encode("utf-8")) // 1024
    print(f"✓ 已生成 A4 预览页: {out_path}  ({size_kb} KB)")
    print(f"  document.title = {title}（PDF 默认文件名）。")


if __name__ == "__main__":
    main()
