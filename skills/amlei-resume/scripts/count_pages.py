#!/usr/bin/env python3
"""只用现有预览壳 + Paged.js 统计简历页数，不生成 PDF。

输入是已经装配好的 body HTML（开头可以是主题 <style>，后面是简历原子），
与 wrap_preview.py 的输入相同。脚本输出只有页数；临时预览文件在结束时删除。
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def _run_preview_wrapper(body_path: Path, preview_path: Path) -> None:
    wrapper = Path(__file__).with_name("wrap_preview.py")
    result = subprocess.run(
        [sys.executable, str(wrapper), str(body_path), str(preview_path)],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        detail = (result.stderr or result.stdout or "").strip()
        raise RuntimeError(detail or "wrap_preview.py 执行失败")


def _count_with_playwright(preview_path: Path, timeout_seconds: int) -> int:
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:
        raise RuntimeError(
            "缺少 playwright。请安装：pip install playwright && playwright install chromium"
        ) from exc

    with sync_playwright() as p:
        browser = _launch_browser(p)
        page = browser.new_page()
        try:
            page.goto(preview_path.as_uri(), wait_until="load")
            page.wait_for_function(
                """() => {
                    const el = document.getElementById('rvInfo');
                    return !!el && /共\\s*\\d+\\s*页/.test(el.textContent || '');
                }""",
                timeout=timeout_seconds * 1000,
            )
            count = page.locator(".pagedjs_sheet").count()
            if count == 0:
                count = page.locator(".pagedjs_page").count()
            if count == 0:
                text = page.locator("#rvInfo").inner_text()
                match = re.search(r"共\s*(\d+)\s*页", text)
                count = int(match.group(1)) if match else 0
            if count < 1:
                raise RuntimeError("Paged.js 已完成，但没有找到有效页数")
            return count
        finally:
            browser.close()


def _browser_candidates() -> list[Path]:
    candidates = [
        Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
        Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    ]
    for command in ("google-chrome", "chromium", "chromium-browser", "msedge"):
        found = shutil.which(command)
        if found:
            candidates.append(Path(found))
    return candidates


def _launch_browser(playwright):
    try:
        return playwright.chromium.launch(headless=True)
    except Exception as bundled_error:
        for candidate in _browser_candidates():
            if candidate.is_file():
                try:
                    return playwright.chromium.launch(
                        headless=True, executable_path=str(candidate)
                    )
                except Exception:
                    continue
        raise RuntimeError(
            "找不到可用 Chromium。请安装 Playwright Chromium（playwright install chromium），"
            "或安装 Google Chrome / Microsoft Edge。"
        ) from bundled_error


def main() -> int:
    parser = argparse.ArgumentParser(
        description="读取装配好的简历 body HTML，只返回 A4 页数；不生成 PDF。"
    )
    parser.add_argument("body", help="装配好的 body HTML（<style> + 原子）路径")
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="等待 Paged.js 完成的最长秒数，默认 30",
    )
    args = parser.parse_args()

    body_path = Path(args.body).expanduser().resolve()
    if not body_path.is_file():
        print(f"找不到 body HTML：{body_path}", file=sys.stderr)
        return 1

    # 临时预览放在 body 同目录，避免头像/图片等相对资源断链影响分页。
    fd, temp_name = tempfile.mkstemp(
        prefix=".page-count-", suffix=".html", dir=str(body_path.parent)
    )
    os.close(fd)
    Path(temp_name).unlink(missing_ok=True)
    preview_path = Path(temp_name)

    try:
        _run_preview_wrapper(body_path, preview_path)
        pages = _count_with_playwright(preview_path, args.timeout)
        print(pages)
        return 0
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    finally:
        preview_path.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
