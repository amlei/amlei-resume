#!/usr/bin/env python3
"""Boss直聘 自动化 — 基于 CloakBrowser Python SDK。

每个命令独立启动浏览器，通过 storage_state 持久化登录态。
供 Agent 以 subprocess 方式复用。

用法:
   boss_zhipin.py login                        登录 → APP 扫码 → 保存状态
   boss_zhipin.py resume-session               恢复会话
   boss_zhipin.py check-messages               检查消息回复
   boss_zhipin.py fetch-jd <名称> <job_id> [目录]  抓取完整 JD（含薪资）
  boss_zhipin.py batch-jds <目录> <名称:job_id>... 批量抓取
  boss_zhipin.py search <关键词> [--city ...] [--salary ...]  搜索岗位
  boss_zhipin.py state-path                     打印状态文件路径
  状态文件：<cwd>/.amlei-skill/resume/boss_state.json 或 ~/.amlei-skill/resume/
"""

import argparse
import json
import os
import random
import re
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    from cloakbrowser import launch_context
except ImportError:
    print("✗ 缺少 cloakbrowser。运行: pip install cloakbrowser", file=sys.stderr)
    sys.exit(1)

# playwright is required by cloakbrowser - install: pip install playwright && playwright install chromium

_SCRIPT_DIR = Path(__file__).parent.resolve()

def _find_state():
    """优先项目级，否则用户根目录（与 profile.py 统一）。"""
    for base in (Path.cwd(), Path.home()):
        p = base / ".amlei-skill" / "resume" / "boss_state.json"
        if p.exists():
            return p
    return Path.cwd() / ".amlei-skill" / "resume" / "boss_state.json"

STATE_FILE = _find_state()

# ── 招呼语（在脚本里直接修改，不由 CLI 传入） ──────────────────────────
# 点击「立即沟通」后自动发送这条消息给对方。
GREETING = "您好，看到您在招这个岗位，我最近在做 AI Agent 相关的开发，对方向很感兴趣，希望能聊聊看有没有合作的机会。"

# ── 拟人化延时范围（秒） ────────────────────────────────────────────
# 每个操作在 [min, max] 区间内随机等待，避免固定间隔被风控。
SLEEP_NAV = (2, 5)       # 页面导航 → 交互
SLEEP_BEFORE_CLICK = (0.5, 1.5)  # 点击前停留（模拟阅读/寻找）
SLEEP_AFTER_CLICK = (1, 3)       # 点击后等待响应
SLEEP_TYPE = (0.02, 0.08)        # 每个字符的键入间隔
SLEEP_AFTER_TYPE = (0.5, 1.5)    # 键入完成 → 点击发送
SLEEP_BATCH_GAP = (2, 5)         # 批量操作之间的间隔
SCROLL_PAUSE = (0.3, 0.8)        # 每次滚动后的停顿

# ── 筛选参数字典（Boss直聘 URL query 参数值） ────────────────────────
CITY = {
    "全国": "", "北京": "101010100", "上海": "101020100", "广州": "101280100",
    "深圳": "101280600", "杭州": "101210100", "成都": "101270100", "南京": "101190100",
    "武汉": "101200100", "西安": "101110100", "长沙": "101250100",
}
JOB_TYPE = {"全职": 1901, "兼职": 1902, "实习": 1903}
EXP = {
    "不限": "", "应届": 101, "1年以下": 102, "1-3年": 103, "3-5年": 104,
    "5-10年": 105, "10年以上": 106,
}
DEGREE = {
    "不限": "", "初中及以下": 201, "高中": 202, "中专/中技": 203,
    "大专": 204, "本科": 205, "硕士": 206, "博士": 207,
}
SALARY = {
    "不限": "", "2K以下": 401, "2K-5K": 402, "5K-10K": 403,
    "10K-15K": 404, "15K-20K": 405, "20K-30K": 406, "30K-50K": 407, "50K以上": 408,
}
SCALE = {
    "不限": "", "0-20人": 301, "20-99人": 302, "100-499人": 303,
    "500-999人": 304, "1000-9999人": 305, "10000人以上": 306,
}


def die(msg: str):
    print(f"✗ {msg}", file=sys.stderr)
    sys.exit(1)


def _ensure_state_or_login():
    if STATE_FILE.exists():
        return
    print("⚠ 未检测到登录状态，即将打开浏览器扫码登录...", file=sys.stderr)
    cmd_login()


def _sleep(lo: float, hi: float):
    time.sleep(random.uniform(lo, hi))


def _rand_scroll(page):
    """模拟浏览行为：随机滚动到几个位置，每步停顿随机时长。"""
    for _ in range(random.randint(2, 5)):
        target = random.randint(100, 1200)
        page.evaluate(f"window.scrollTo({{top: {target}, behavior: 'smooth'}})")
        _sleep(*SCROLL_PAUSE)


def _rand_hover(page):
    """在几个随机可见元素上悬停，模拟鼠标移动。"""
    els = page.query_selector_all("a, button, .job-card, .job-list-item, .job-title")
    if not els:
        return
    targets = random.sample(els, min(random.randint(1, 3), len(els)))
    for el in targets:
        try:
            if el.is_visible():
                el.hover()
                _sleep(0.1, 0.3)
        except Exception:
            pass


def humanize(page):
    """一次拟人化动作：随机滚动 + 悬停。"""
    _rand_scroll(page)
    _rand_hover(page)


def _decode_boss_text(text: str) -> str:
    """Boss直聘用 U+E030-U+E039 编码数字，转回 ASCII 数字 '0'-'9'。"""
    return "".join(
        chr(ord(c) - 0xE030 + 0x30) if 0xE030 <= ord(c) <= 0xE039 else c
        for c in text
    )


def _extract_search_results(page) -> list[dict]:
    """从搜索列表页提取岗位卡片，返回结构化列表。"""
    cards = page.query_selector_all(".job-card-box")
    results = []
    for c in cards:
        try:
            name_el = c.query_selector(".job-name")
            salary_el = c.query_selector(".job-salary")
            tags_el = c.query_selector_all(".tag-list li")
            company_el = c.query_selector(".boss-name")
            area_el = c.query_selector(".company-location")
            href = name_el.get_attribute("href") if name_el else ""
            job_id = ""
            if href:
                m = re.search(r"/(\w+)\.html", href)
                if m:
                    job_id = m.group(1)
            results.append({
                "name": _decode_boss_text(name_el.inner_text().strip()) if name_el else "",
                "salary": _decode_boss_text(salary_el.inner_text().strip()) if salary_el else "",
                "company": company_el.inner_text().strip() if company_el else "",
                "area": area_el.inner_text().strip() if area_el else "",
                "tags": [_decode_boss_text(t.inner_text().strip()) for t in tags_el],
                "job_id": job_id,
            })
        except Exception:
            continue
    return results


_JD_SKIP_REGEX = (
    "感兴趣",
    "立即沟通",
    "继续沟通",
    "完善在线简历",
    "上传附件简历",
    "查看全部职位",
    "下载App, 不错过Boss每一条消息",
    "微信扫码",
    "扫码分享",
)


def _skip_line(s: str) -> bool:
    if not s.strip():
        return True
    if len(s) == 1:
        return True
    if s in ("收藏", "举报", "分享"):
        return True
    for p in _JD_SKIP_REGEX:
        if p in s:
            return True
    return False
_JD_END = {"竞争力分析", "BOSS 安全提示", "工商信息", "更多职位", "看过该职位的人还看了",
           "精选职位", "页面更新时间", "城市招聘", "热门职位", "推荐公司"}

_ACTIVE_MARKERS = ("3日内活跃", "今日活跃", "本周活跃", "刚刚活跃", "本月活跃")


def _extract_jd_md(page) -> str:
    text = _decode_boss_text(page.inner_text("body"))
    lines = text.split("\n")

    # 找到首个含薪资的行 → 内容起点
    start = -1
    for i, line in enumerate(lines):
        if any(k in line for k in ("K", "面议", "元/天")):
            start = i
            break
    if start < 0:
        return text

    # 收集行，跳过噪声，在终点标记处截断
    buf = []
    for line in lines[start:]:
        s = line.strip()
        if _skip_line(s):
            continue
        if any(k in s for k in _JD_END):
            break
        buf.append(s)

    # ── 分区块 ──
    header_buf = []
    desc_buf = []
    company_buf = []
    active = ""
    state = "header"

    for s in buf:
        if s == "职位描述":
            state = "desc"
            continue
        if s == "公司基本信息":
            state = "company"
            company_buf.append("")
            company_buf.append("**公司基本信息**")
            continue
        if any(m in s for m in _ACTIVE_MARKERS):
            active = s
            continue

        if state == "header":
            header_buf.append(s)
        elif state == "desc":
            desc_buf.append(s)
        elif state == "company":
            company_buf.append(s)

    # ── 清理描述末尾的招聘者信息 ──
    while len(desc_buf) >= 3:
        n1, n2, n3 = desc_buf[-3:]
        if (2 <= len(n1) <= 4 and all('\u4e00' <= c <= '\u9fff' for c in n1)
                and any(k in n2 for k in ("公司", "有限", "集团", "股份"))
                and len(n3) >= 2):
            desc_buf = desc_buf[:-3]
        else:
            break

    # ── 组装 ──
    out = []

    # Header: 重组为「## 公司、岗位」+ 「岗位、薪资、地区、学历」
    h = " ".join(header_buf)
    for token in ("查看所有职位", "感兴趣", "立即沟通", "继续沟通"):
        h = h.replace(token, "")
    h = re.sub(r"\s+", " ", h).strip()

    sal = ""
    m = re.search(r"([\d.]+[Kk]?[-~到][\d.]+[Kk]?(?:·\d+薪)?)", h)
    if m:
        sal = m.group(1)

    # 提取字段
    area = ""
    for a in ("深圳", "广州", "北京", "上海", "杭州", "成都", "武汉", "南京", "西安", "长沙"):
        if a in h:
            area = a
            break
    # 子区域（带 · 的详细地址）
    area_detail = ""
    for part in h.split():
        if "·" in part and any(c in part for c in ("区", "街", "路", "道", "镇", "乡")):
            area_detail = part
            break

    tags = [t for t in h.split() if any(k in t for k in ("年", "历", "届", "在读", "以下", "不限", "博士", "硕士", "本科", "大专"))]

    # 公司名从 company_buf 取（页面底部公司信息区域）
    company = ""
    for s in company_buf:
        if any(k in s for k in ("公司", "有限", "集团", "股份")) and not s.startswith("**"):
            company = s
            break
    # fallback: 从 header 尾部取含公司的词段
    if not company:
        for part in reversed(h.split()):
            if any(k in part for k in ("公司", "有限", "集团", "股份")):
                company = part
                break

    # 岗位名 = h 中第一个薪资之前的连续文本
    before_sal = h.split(sal)[0].strip() if sal else h
    title = re.sub(r"\s+", " ", before_sal).strip()
    if not title:
        title = h.split()[0] if h.split() else ""

    section = company or title
    if section:
        out.append(f"# {section}")
        out.append("")
    if company:
        out.append(f"公司: {company}")
    if title:
        out.append(f"岗位: {title}")
    if sal:
        out.append(f"薪资: {sal}")
    if area:
        out.append(f"地点: {area}")
    for t in tags:
        out.append(f"学历: {t}")
    # 公司规模 / 行业 / 活跃状态（从 company_buf 提取）
    info_lines = [s for s in company_buf if s and not s.startswith("**") and s != company]
    for s in info_lines:
        if s.endswith("人"):
            out.append(f"规模: {s}")
        elif any('\u4e00' <= c <= '\u9fff' for c in s):
            out.append(f"行业: {s}")
    if active:
        out.append(f"活跃: {active}")

    if desc_buf:
        out.append("")
        out.append("# 职位描述")
        out.append("")
        out.append("\n".join(desc_buf))

    return "\n".join(out).strip()


# ── 命令 ──────────────────────────────────────────────────────────────────

def cmd_state_path():
    print(STATE_FILE.resolve())


def cmd_login():
    ctx = launch_context(headless=False)
    try:
        page = ctx.new_page()
        page.goto("https://www.zhipin.com/web/user/?ka=header-login", wait_until="domcontentloaded", timeout=60000)
        _sleep(*SLEEP_NAV)
        page.eval_on_selector(".btn-sign-switch.ewm-switch", "el => el.click()")
        _sleep(*SLEEP_AFTER_CLICK)

        print("\n" + "=" * 60)
        print("  二维码已显示在浏览器窗口中。")
        print("  请打开手机 Boss 直聘 APP 扫码登录。")
        print("=" * 60 + "\n")

        # Stage 1: 等待扫码完成
        print("⏳ 等待扫码...", file=sys.stderr)
        for _ in range(100):
            time.sleep(3)
            scanned = page.query_selector(".login-step-box")
            if scanned:
                title_el = scanned.query_selector(".login-step-title")
                if title_el and "扫描成功" in (title_el.inner_text() or ""):
                    print("✓ 扫码成功，请在手机上确认登录...", file=sys.stderr)
                    _sleep(*SLEEP_AFTER_CLICK)
                    break
        else:
            die("扫码超时（5 分钟）。")

        # Stage 2: 等待确认登录（页面跳离 /user/）
        for _ in range(100):
            time.sleep(3)
            if "user" not in page.url:
                break
        else:
            die("登录确认超时（5 分钟）。")

        humanize(page)
        ctx.storage_state(path=str(STATE_FILE))
        print(f"✓ 登录成功！{page.url}")
        print(f"✓ 状态已保存: {STATE_FILE.resolve()}")
    finally:
        ctx.close()


def cmd_resume_session():
    _ensure_state_or_login()

    ctx = launch_context(storage_state=str(STATE_FILE))
    try:
        page = ctx.new_page()
        page.goto("https://www.zhipin.com/web/geek/job-recommend", wait_until="domcontentloaded", timeout=60000)
        _sleep(*SLEEP_NAV)
        humanize(page)
        print(f"✓ 会话已恢复（{page.url}）")
    finally:
        ctx.close()


def cmd_fetch_jd(name: str, job_id: str, out_dir: str = "."):
    _ensure_state_or_login()

    url = f"https://www.zhipin.com/job_detail/{job_id}/"
    ctx = launch_context(storage_state=str(STATE_FILE))
    try:
        print(f"› 抓取: {name}", file=sys.stderr)
        page = ctx.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        _sleep(*SLEEP_NAV)
        humanize(page)
        _sleep(*SLEEP_AFTER_CLICK)

        jd = _extract_jd_md(page)

        path = Path(out_dir) / f"{name}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f"# {name}\n\n{jd}\n\n---\n"
            f"_source: {url}\n"
            f"_fetched: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
            encoding="utf-8",
        )
        print(f"✓ 已保存: {path}", file=sys.stderr)
        print(f"--- {name} ---\n{jd}\n")
    finally:
        ctx.close()


def cmd_batch_jds(out_dir: str, entries: list[str]):
    for e in entries:
        if ":" not in e:
            print(f"✗ 跳过: {e}（格式 name:job_id）", file=sys.stderr)
            continue
        name, job_id = e.split(":", 1)
        cmd_fetch_jd(name, job_id, out_dir)
        _sleep(*SLEEP_BATCH_GAP)


def cmd_search(keyword: str, city: str, job_type: str, salary: str,
               exp: str, degree: str, scale: str, industry: str):
    _ensure_state_or_login()

    params = [f"query={keyword}"]
    city_code = CITY.get(city, "")
    if city_code:
        params.append(f"city={city_code}")
    if job_type:
        params.append(f"jobType={JOB_TYPE.get(job_type, '')}")
    if salary:
        params.append(f"salary={SALARY.get(salary, '')}")
    if exp:
        params.append(f"experience={EXP.get(exp, '')}")
    if degree:
        params.append(f"degree={DEGREE.get(degree, '')}")
    if scale:
        params.append(f"scale={SCALE.get(scale, '')}")
    if industry:
        params.append(f"industry={industry}")

    url = "https://www.zhipin.com/web/geek/jobs?" + "&".join(params)
    print(f"› {url}", file=sys.stderr)

    ctx = launch_context(storage_state=str(STATE_FILE))
    try:
        page = ctx.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        _sleep(*SLEEP_NAV)
        humanize(page)

        results = _extract_search_results(page)
        if not results:
            print("(无匹配岗位)", file=sys.stderr)
            return
        print(json.dumps(results, ensure_ascii=False, indent=2))
    finally:
        ctx.close()


def _handle_startchat_dialog(page):
    """处理首次沟通弹窗：textarea + 发送按钮 + 右侧微信二维码。"""
    dialog = page.query_selector(".dialog-container")
    if not dialog or not dialog.is_visible():
        return False

    textarea = page.query_selector("textarea.input-area")
    if not textarea:
        return False

    # 填入招呼语并触发 input 事件解除 disable
    textarea.click()
    page.evaluate("document.querySelector('textarea.input-area').value = ''")
    for ch in GREETING:
        page.evaluate(f"document.querySelector('textarea.input-area').value += {ch!r}")
        page.evaluate("document.querySelector('textarea.input-area').dispatchEvent(new Event('input', {bubbles: true}))")
        _sleep(*SLEEP_TYPE)
    _sleep(*SLEEP_AFTER_TYPE)

    # 点发送
    send_btn = page.query_selector("div.send-message")
    if send_btn and send_btn.is_visible():
        send_btn.hover()
        _sleep(0.2, 0.4)
        send_btn.click()
        _sleep(*SLEEP_AFTER_CLICK)
    return True


def cmd_chat(job_id: str):
    """打开岗位详情 → 点「立即沟通」/「继续沟通」→ 发送招呼语。"""
    _ensure_state_or_login()

    url = f"https://www.zhipin.com/job_detail/{job_id}/"
    ctx = launch_context(storage_state=str(STATE_FILE), headless=False)
    try:
        page = ctx.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        _sleep(*SLEEP_NAV)

        # 浏览岗位描述（模拟阅读）
        humanize(page)
        _sleep(*SLEEP_BEFORE_CLICK)

        # 找沟通按钮（首次：「立即沟通」；已沟通过：「继续沟通」）
        for text in ("立即沟通", "继续沟通"):
            btn = page.query_selector(f"text={text}")
            if btn and btn.is_visible():
                break
        else:
            die("页面上没找到「立即沟通」或「继续沟通」按钮。")

        btn.hover()
        _sleep(0.2, 0.5)
        btn.click()
        _sleep(*SLEEP_AFTER_CLICK)

        # 检测是弹窗还是直开聊天面板
        if not _handle_startchat_dialog(page):
            # 直开面板：等待 .chat-input
            chat_input = None
            for _ in range(10):
                chat_input = page.query_selector(".chat-input")
                if chat_input and chat_input.is_visible():
                    break
                _sleep(0.5, 1.5)
            else:
                die("聊天面板未出现。")

            # 逐字键入招呼语
            chat_input.click()
            page.evaluate("document.querySelector('.chat-input').innerText = ''")
            for ch in GREETING:
                page.evaluate(f"document.querySelector('.chat-input').innerText += {ch!r}")
                page.evaluate("document.querySelector('.chat-input').dispatchEvent(new Event('input', {bubbles: true}))")
                _sleep(*SLEEP_TYPE)
            _sleep(*SLEEP_AFTER_TYPE)

            # 点「发送」按钮
            send_btn = page.query_selector("button.btn-send")
            if send_btn and send_btn.is_visible():
                send_btn.hover()
                _sleep(0.2, 0.4)
                send_btn.click()
            else:
                die("没找到「发送」按钮。")

        _sleep(*SLEEP_AFTER_CLICK)
        print(f"✓ 招呼已发送至 {url}")

    finally:
        ctx.close()


# ── 主入口 ────────────────────────────────────────────────────────────────

def cmd_check_messages():
    """检查消息列表，检测谁回复了。"""
    _ensure_state_or_login()

    ctx = launch_context(storage_state=str(STATE_FILE), headless=False)
    try:
        page = ctx.new_page()
        page.goto("https://www.zhipin.com/web/geek/chat", wait_until="domcontentloaded", timeout=60000)
        _sleep(*SLEEP_NAV)
        humanize(page)
        _sleep(*SLEEP_AFTER_CLICK)

        conversations = page.evaluate("""
            Array.from(document.querySelectorAll('.friend-content')).map(el => {
                const nameEl = el.querySelector('.name-text');
                const lastMsgText = el.querySelector('.last-msg-text');
                const statusEl = el.querySelector('.message-status.status-delivery');
                const vline = el.querySelector('.vline');
                const timeEl = el.querySelector('.time');

                let company = '';
                if (vline && vline.nextSibling) {
                    company = (vline.nextSibling.textContent || '').trim();
                }

                return {
                    name: nameEl ? nameEl.innerText.trim() : '',
                    company: company,
                    lastMessage: lastMsgText ? lastMsgText.innerText.trim() : '',
                    hasReply: !statusEl,
                    time: timeEl ? timeEl.innerText.trim() : '',
                };
            })
        """)

        if not conversations:
            print(json.dumps({"total": 0, "replied": [], "waiting": []}, ensure_ascii=False, indent=2), file=sys.stderr)
            return

        replied = [c for c in conversations if c.get("hasReply")]
        sent = [c for c in conversations if not c.get("hasReply")]

        result = {
            "total": len(conversations),
            "replied": replied,
            "waiting": sent,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    finally:
        ctx.close()

def main():
    ap = argparse.ArgumentParser(description="Boss直聘 × CloakBrowser")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("login")
    sub.add_parser("resume-session")
    sub.add_parser("state-path")
    sub.add_parser("check-messages", help="检查消息列表，检测谁回复了")

    p = sub.add_parser("chat")
    p.add_argument("job_id")

    p = sub.add_parser("fetch-jd")
    p.add_argument("name")
    p.add_argument("job_id")
    p.add_argument("out_dir", nargs="?", default=".")

    p = sub.add_parser("batch-jds")
    p.add_argument("out_dir")
    p.add_argument("entries", nargs="+")

    p = sub.add_parser("search", help="搜索岗位，支持多条件筛选")
    p.add_argument("keyword", help="搜索关键词")
    p.add_argument("--city", default="深圳", help=f"城市: {' / '.join(CITY)}")
    p.add_argument("--job-type", choices=list(JOB_TYPE), help=f"职位类型: {' / '.join(JOB_TYPE)}")
    p.add_argument("--salary", choices=list(SALARY), help=f"薪资: {' / '.join(k for k in SALARY if k)}")
    p.add_argument("--exp", choices=list(EXP), help=f"经验: {' / '.join(k for k in EXP if k)}")
    p.add_argument("--degree", choices=list(DEGREE), help=f"学历: {' / '.join(k for k in DEGREE if k)}")
    p.add_argument("--scale", choices=list(SCALE), help=f"公司规模: {' / '.join(k for k in SCALE if k)}")
    p.add_argument("--industry", help="行业编码（如 10001 互联网）")

    args = ap.parse_args()

    {"login": cmd_login, "resume-session": cmd_resume_session,
     "state-path": cmd_state_path,
     "check-messages": cmd_check_messages,
     "chat": lambda: cmd_chat(args.job_id),
     "fetch-jd": lambda: cmd_fetch_jd(args.name, args.job_id, args.out_dir),
     "batch-jds": lambda: cmd_batch_jds(args.out_dir, args.entries),
     "search": lambda: cmd_search(args.keyword, args.city, args.job_type,
                                  args.salary, args.exp, args.degree,
                                  args.scale, args.industry)}[args.cmd]()


if __name__ == "__main__":
    main()
