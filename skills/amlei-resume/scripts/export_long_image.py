#!/usr/bin/env python3
"""简历长图导出：把预览 HTML 里每个 A4 页（`.pagedjs_sheet`）逐页截图后纵向拼成一张长图 PNG。

渲染 HTML/CSS 必须经过浏览器引擎，纯 Python 无法实现，故依赖 Playwright。

依赖：
  pip install playwright Pillow
  playwright install chromium      # 首次需装浏览器

用法：
  python3 scripts/export_long_image.py <预览.html> [输出.png] [--selector '.pagedjs_sheet'] [--scale 2]

- 默认输出 `<预览>_长图.png`（与输入同目录）
- `--selector` 默认 `.pagedjs_sheet`（Paged.js 分页后每个 A4 页的卡片容器）
- `--scale` 默认 2（retina；越大越清晰、文件越大）

产物是一张纵向长图：发招聘平台聊天框比 PDF 少一次"点击下载"，HR 可直接滑着看完。
"""

import argparse
import io
import pathlib
import sys

from PIL import Image
from playwright.sync_api import sync_playwright


def stack_vertical(images):
    width = max(im.width for im in images)
    padded = []
    for im in images:
        if im.width < width:
            bg = Image.new("RGB", (width, im.height), "white")
            bg.paste(im, (0, 0))
            im = bg
        padded.append(im.convert("RGB"))
    height = sum(im.height for im in padded)
    out = Image.new("RGB", (width, height), "white")
    y = 0
    for im in padded:
        out.paste(im, (0, y))
        y += im.height
    return out


def main():
    ap = argparse.ArgumentParser(description="把简历预览 HTML 的各 A4 页拼成一张纵向长图 PNG。")
    ap.add_argument("html", help="预览 HTML 路径（wrap_preview.py 的产物）")
    ap.add_argument("output", nargs="?", help="输出 PNG 路径，默认 <html>_长图.png")
    ap.add_argument("--selector", default=".pagedjs_sheet", help="页容器选择器，默认 '.pagedjs_sheet'（Paged.js 产物）")
    ap.add_argument("--scale", type=int, default=2, help="device scale factor，默认 2（retina）")
    args = ap.parse_args()

    html_path = pathlib.Path(args.html).resolve()
    if not html_path.is_file():
        sys.exit(f"✗ 找不到 HTML：{html_path}")
    out_path = (
        pathlib.Path(args.output).resolve()
        if args.output
        else html_path.with_name(f"{html_path.stem}_长图.png")
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            ctx = browser.new_context(
                device_scale_factor=args.scale,
                viewport={"width": 794, "height": 1123},
            )
            page = ctx.new_page()
            page.goto(html_path.as_uri())
            page.wait_for_selector(args.selector, timeout=20000)
            # 等 Paged.js 分页完成（rvInfo 写成"共 N 页"），再给布局留余量稳定
            try:
                page.wait_for_function(
                    "/共 \\d+ 页/.test((document.getElementById('rvInfo')||{}).textContent||'')",
                    timeout=20000,
                )
            except Exception:
                pass
            try:
                page.evaluate("document.fonts && document.fonts.ready")
            except Exception:
                pass
            page.wait_for_timeout(600)

            # 截图前藏掉工具条/提示：element.screenshot() 截的是 bbox 区域，会把
            # position:sticky 的工具栏像素一起截进去（盖在第 1 页顶部）。藏掉只影响截图，不影响页面本身。
            page.add_style_tag(content=".rv-toolbar,.rv-toast{display:none!important}")
            page.wait_for_timeout(150)

            handles = page.query_selector_all(args.selector)
            if not handles:
                sys.exit(f"✗ 选择器 {args.selector} 未匹配到任何页")
            shots = []
            for h in handles:
                png = h.screenshot(type="png")
                shots.append(Image.open(io.BytesIO(png)))
        finally:
            browser.close()

    long_img = stack_vertical(shots)
    long_img.save(out_path, "PNG", optimize=True)
    print(f"✓ 简历长图：{long_img.size[0]}×{long_img.size[1]}（{len(shots)} 页 · {args.scale}x）-> {out_path}")


if __name__ == "__main__":
    main()
