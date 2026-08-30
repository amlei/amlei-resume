# 主题 · English / MNC 外企风（`english-mnc`）

> 单栏 · 英文 · 酒红（burgundy）单点缀色 · UPPERCASE 章节标题 · 斜体 role · `•` bullets · key:value skill lines。
> 适用于外企管培 / BA / 咨询 / 英文简历。
>
> **语言**：本主题正文用**英文**。`.sec-head h2` 自动 `text-transform:uppercase`——直接写正常大小写（如 `Education`）即可，不要自己全大写。
>
> **用法**：基准组件（Header/SectionHead/Summary/Entry/Bullet 等）读 [component-library.md](component-library.md)，本文只含本主题的设计令牌、`<style>` 与差异。渲染时把"完整 `<style>`"整段作为产物开头，再按共享库骨架用基准组件 + 本文差异装配。HTML 一律从文件取，不要凭记忆手写。

## 设计变量速查表

| 变量 | 值 | 用途 |
|------|-----|------|
| `--bg` | `oklch(93% .004 30)` | 舞台底色 |
| `--paper` | `oklch(99.5% .002 40)` | A4 纸张 |
| `--ink` | `oklch(20% .014 30)` | 正文 |
| `--muted` / `--faint` | `oklch(44% .012 30)` / `oklch(55% .010 30)` | 次要 / 日期 |
| `--border` / `--hair` | `oklch(88% .010 30)` / `oklch(91% .008 30)` | 边框 / 发丝线 |
| `--accent` | `oklch(40% .13 25)` | **唯一**点缀色（酒红） |
| `--accent-ink` / `--accent-soft` | `oklch(33% .12 25)` / `oklch(95% .022 25)` | 强调字色 / 浅底 |

## 完整 `<style>`（渲染时整段贴在产物最前）

```html
<style>
  :root{
    --bg:oklch(93% .004 30);--paper:oklch(99.5% .002 40);--ink:oklch(20% .014 30);--muted:oklch(44% .012 30);
    --faint:oklch(55% .010 30);--border:oklch(88% .010 30);--hair:oklch(91% .008 30);
    --accent:oklch(40% .13 25);--accent-ink:oklch(33% .12 25);--accent-soft:oklch(95% .022 25);
    --font-sans:'PingFang SC','HarmonyOS Sans SC',-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue','Roboto',system-ui,sans-serif;
    --font-mono:'JetBrains Mono','SF Mono',ui-monospace,Menlo,Consolas,monospace;
  }
  body{background:var(--bg);color:var(--ink);font-family:var(--font-sans);font-size:14px;line-height:1.55;-webkit-font-smoothing:antialiased;font-feature-settings:'tnum' on;text-rendering:optimizeLegibility}
  .page{background:var(--paper)}
  .resume-header{display:grid;grid-template-columns:1fr auto;gap:18px;align-items:center;padding-bottom:13px;border-bottom:2px solid var(--ink)}
  .name-row{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
  .name-row .name{font-weight:700;font-size:28px;letter-spacing:.01em}
  .name-row .role{font-size:13px;font-weight:600;color:var(--accent-ink)}
  .contact{margin-top:8px;font-family:var(--font-mono);font-size:11px;color:var(--muted)}
  .contact .sep{color:var(--accent);margin:0 6px}
  .edu-line{margin-top:5px;font-family:var(--font-sans);font-size:12px;color:var(--accent-ink);font-weight:500}
  .photo{width:26mm;height:36mm;border:1px solid var(--border);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5px;color:var(--faint);overflow:hidden}
  .photo img{width:100%;height:100%;object-fit:cover;display:block}
  .photo svg{width:26px;height:26px;opacity:.45}
  .photo span{font-size:10px;letter-spacing:.1em}
  .sec-head{display:flex;align-items:center;gap:9px;margin-top:16px;margin-bottom:8px}
  .sec-head .ico{width:15px;height:15px;color:var(--accent);flex-shrink:0}
  .sec-head h2{font-size:13px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:var(--ink)}
  .sec-head::after{content:"";flex:1;height:1px;background:var(--hair)}
  .summary p{font-size:13px;line-height:1.7;text-align:justify;text-wrap:pretty}
  .summary p b{color:var(--accent-ink);font-weight:600}
  .entry{margin-bottom:11px}
  .entry-main{display:flex;align-items:baseline;justify-content:space-between;gap:14px;flex-wrap:nowrap}
  .entry-title{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}
  .entry-title .org{font-size:14.5px;font-weight:700;letter-spacing:.01em}
  .entry-main .proj{font-size:14.5px;font-weight:700;letter-spacing:.01em}
  .entry-main .company{font-size:11.5px;color:var(--muted);font-weight:500;letter-spacing:.03em}
  .entry-title .role{font-size:13px;color:var(--accent-ink);font-style:italic}
  .entry-date{font-family:var(--font-mono);font-size:10.5px;color:var(--faint);white-space:nowrap;letter-spacing:.04em}
  .entry-list{list-style:none;margin-top:4px}
  .entry-list li{position:relative;padding-left:13px;font-size:12.5px;line-height:1.48;color:var(--ink);margin-bottom:2px;text-align:justify;text-wrap:pretty}
  .entry-list li::before{content:"•";position:absolute;left:1px;top:4px;color:var(--accent);font-size:10px;line-height:1}
  .entry-list .num{font-family:var(--font-mono);color:var(--accent-ink);font-weight:600}
  .entry-list b{color:var(--ink);font-weight:600}
  /* Bullet（独立原子，自由换页） */
  .bullet{position:relative;padding-left:13px;font-size:12.5px;line-height:1.48;color:var(--ink);margin-bottom:2px;text-align:justify;text-wrap:pretty}
  .bullet::before{content:"•";position:absolute;left:1px;top:4px;color:var(--accent);font-size:10px;line-height:1}
  .bullet .num{font-family:var(--font-mono);color:var(--accent-ink);font-weight:600}
  .bullet b{color:var(--ink);font-weight:600}
  /* Skills（双列 key:value 行） */
  .skills{display:grid;grid-template-columns:1fr 1fr;gap:3px 22px}
  .skills-row{display:grid;grid-template-columns:96px 1fr;gap:10px;padding:3px 0;border-bottom:1px dashed var(--hair);font-size:12.5px}
  .skills-row .cat{font-weight:600;color:var(--accent-ink)}
</style>
```

## 主题差异（相对共享组件库）

- **内容全部写英文**（self-intro 中文内容译成英文）；SectionHead 写正常大小写，CSS 自动全大写。
- **启用组件**：Header / SectionHead / Summary / Entry / Bullet / Skills（双列）；**不用** Interests、Pubs、Awards（奖项内容并入 Experience/Skills）。
- **Header 默认字段集**：`{{location}}` · `{{phone}}` · `{{email}}` · `<a href="{{linkedin-url}}">{{linkedin}}</a>` · `{{relocation}}`（值如 "Open to relocation"）；name 行 = `{{name}}`（英文姓名）· `{{中文名}}`；`{{photo}}` 占位 span 写 `PHOTO`（大写）。
- **Entry**：role 斜体（style 已实现）；entry-title 内三段 `<span class="org">{{Org}}</span><span class="company">{{Company short}}</span><span class="role">{{Role — detail}}</span>`；**无 meta 行**——GPA 等放进首条 bullet 用 `<b>`；日期写英文月份（`Sep 2024 — Dec 2024`）。项目经历仍走共享库三段式（`.proj`/`.company`/`.entry-date`）。
- **Bullet**：数字 → `<span class="num">`，关键术语 → `<b>`。
- **Skills**：容器 `.skills` 两列 grid（style 已实现），行结构同共享库 `.skills-row`（cat + tags）：

  ```html
  <div class="skills">
    <div class="skills-row"><span class="cat">{{Analytics}}</span><span class="tags"><b>Proficient in {{SQL}}</b> ({{complex queries, reporting}}) · familiar with {{Tableau}}</span></div>
  </div>
  ```

  值 = 英文等级词（Proficient in / Skilled in / Familiar with / Working knowledge of，按程度从高到低）+ 技能名（括号补方向）；「等级词 + 技能名」用 `<b>` 加重。不用 chip。
- **骨架**：Header → Profile → Education → Experience → Leadership & Projects → Skills & Languages（按 MD 模块顺序）。
