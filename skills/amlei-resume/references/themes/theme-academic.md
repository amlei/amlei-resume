# 主题 · 学术 / 科研 CV（`academic`）

> 单栏 · 墨蓝单点缀色 · 证件照 · 描边 SVG 图标 · `•` 列表符 · 论文列表 · 奖项网格。
> 适用于升学 / PhD 申请 / 科研岗。
>
> **用法**：渲染时把下面"完整 `<style>`"整段作为产物开头，再按"简历骨架"用各组件（带 `{{占位符}}`）装配正文原子。HTML 一律从本文件取，不要凭记忆手写。

## 设计变量速查表

| 变量 | 值 | 用途 |
|------|-----|------|
| `--bg` | `oklch(94% .003 255)` | 视口舞台底色 |
| `--paper` | `oklch(99.4% .002 255)` | A4 纸张面 |
| `--ink` (`--fg`) | `oklch(19% .015 255)` | 正文 / 姓名 |
| `--muted` | `oklch(43% .012 255)` | 次要文字（联系方式 / meta） |
| `--faint` | `oklch(55% .010 255)` | 日期 / 英文标签 |
| `--border` | `oklch(87% .008 255)` | 证件照边框 / 标签边框 |
| `--hair` | `oklch(90% .006 255)` | 发丝分割线 / 虚线 |
| `--accent` | `oklch(33% .05 258)` | **唯一**点缀色（墨蓝） |
| `--accent-ink` | `oklch(26% .05 258)` | 强调字色（role / 数字 / 斜体） |
| `--font-sans` | 苹方系 | 正文 |
| `--font-mono` | JetBrains Mono / SF Mono | 日期 / 数字 / 联系方式 |

> 想换配色只改 `--accent` / `--accent-ink`，其余保持。

## 完整 `<style>`（渲染时整段贴在产物最前）

```html
<style>
  :root{
    --bg:oklch(94% .003 255);--paper:oklch(99.4% .002 255);--ink:oklch(19% .015 255);--muted:oklch(43% .012 255);
    --faint:oklch(55% .010 255);--border:oklch(87% .008 255);--hair:oklch(90% .006 255);
    --accent:oklch(33% .05 258);--accent-ink:oklch(26% .05 258);
    --font-sans:'PingFang SC','HarmonyOS Sans SC','Microsoft YaHei','Hiragino Sans GB',-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;
    --font-mono:'JetBrains Mono','SF Mono',ui-monospace,Menlo,Consolas,monospace;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:var(--bg);color:var(--ink);font-family:var(--font-sans);font-size:14px;line-height:1.58;-webkit-font-smoothing:antialiased;font-feature-settings:'tnum' on;text-rendering:optimizeLegibility}
  /* Header */
  .resume-header{display:grid;grid-template-columns:1fr auto;gap:18px;align-items:center;padding-bottom:12px;border-bottom:1.5px solid var(--ink)}
  .name-row{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
  .name-row .name{font-weight:700;font-size:26px;letter-spacing:.04em}
  .name-row .role{font-size:13px;font-weight:600;color:var(--accent-ink)}
  .contact{margin-top:8px;font-family:var(--font-mono);font-size:11px;color:var(--muted)}
  .contact .sep{color:var(--accent);margin:0 6px}
  .contact a{color:var(--accent-ink);text-decoration:none}
  .edu-line{margin-top:5px;font-family:var(--font-sans);font-size:12px;color:var(--accent-ink);font-weight:500}
  .photo{width:26mm;height:36mm;border:1px solid var(--border);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5px;color:var(--faint);overflow:hidden}
  .photo img{width:100%;height:100%;object-fit:cover;display:block}
  .photo svg{width:26px;height:26px;opacity:.45}
  .photo span{font-size:10px;letter-spacing:.1em}
  /* SectionHead */
  .sec-head{display:flex;align-items:center;gap:9px;margin-top:15px;margin-bottom:8px}
  .sec-head .ico{width:15px;height:15px;color:var(--accent);flex-shrink:0}
  .sec-head h2{font-weight:700;font-size:14px;color:var(--ink);letter-spacing:.1em}
  .sec-head h2 .en{font-weight:400;font-size:11px;color:var(--faint);letter-spacing:.12em;margin-left:6px}
  .sec-head::after{content:"";flex:1;height:1px;background:var(--hair)}
  /* Summary / Interests */
  .summary p{font-size:13px;line-height:1.75;text-align:justify;text-wrap:pretty}
  .summary p b,.summary p strong{color:var(--accent-ink);font-weight:600}
  .interests{display:flex;flex-wrap:wrap;gap:6px;margin-top:4px}
  .interests .it{font-size:12.5px;color:var(--accent-ink);background:oklch(95% .01 258);border:1px solid var(--border);padding:2px 8px}
  /* Entry */
  .entry{margin-bottom:8px}
  .entry-main{display:grid;grid-template-columns:1fr auto;align-items:baseline;gap:14px}
  .entry-title{display:flex;align-items:baseline;gap:9px;flex-wrap:wrap}
  .entry-title .org,.entry-title .proj{font-weight:700;font-size:14px}
  .entry-title .role{font-size:13px;color:var(--accent-ink)}
  .entry-date{font-family:var(--font-mono);font-size:11px;color:var(--faint);white-space:nowrap}
  .entry-meta{margin-top:2px;font-size:11.5px;color:var(--muted);display:flex;gap:14px;flex-wrap:wrap}
  .entry-meta b{color:var(--ink);font-weight:600}
  .entry-list{list-style:none;margin-top:4px}
  .entry-list li{position:relative;padding-left:13px;font-size:12.5px;line-height:1.62;color:var(--ink);margin-bottom:2px;text-align:justify;text-wrap:pretty}
  .entry-list li::before{content:"•";position:absolute;left:1px;top:5px;color:var(--accent);font-size:10px;line-height:1}
  .entry-list .num{font-family:var(--font-mono);color:var(--accent-ink);font-weight:600}
  /* Bullet（独立原子，自由换页） */
  .bullet{position:relative;padding-left:13px;font-size:12.5px;line-height:1.62;color:var(--ink);margin-bottom:2px;text-align:justify;text-wrap:pretty}
  .bullet::before{content:"•";position:absolute;left:1px;top:5px;color:var(--accent);font-size:10px;line-height:1}
  .bullet .num{font-family:var(--font-mono);color:var(--accent-ink);font-weight:600}
  /* Pubs */
  .pubs{list-style:none}
  .pubs li{font-size:12.5px;line-height:1.6;padding:5px 0 5px 26px;border-bottom:1px dashed var(--hair);position:relative;text-align:justify;text-wrap:pretty}
  .pubs li .tag{position:absolute;left:0;top:6px;font-family:var(--font-mono);font-size:10.5px;color:var(--accent-ink);font-weight:600}
  .pubs li .ven{font-style:italic;color:var(--accent-ink)}
  .pubs li .yr{font-family:var(--font-mono);color:var(--faint)}
  .pubs li .me{text-decoration:underline;text-decoration-color:var(--accent);text-underline-offset:2px}
  /* Awards */
  .awards{display:grid;grid-template-columns:1fr 1fr;gap:2px 22px}
  .award{display:grid;grid-template-columns:42px 1fr auto;gap:8px;align-items:baseline;font-size:12.5px;padding:3px 0;border-bottom:1px dashed var(--hair)}
  .award .yr{font-family:var(--font-mono);font-size:10.5px;color:var(--accent)}
  .award .lvl{font-size:11px;color:var(--accent-ink);font-weight:600}
  /* Skills */
  .skills-row{display:grid;grid-template-columns:84px 1fr;gap:12px;padding:4px 0;border-bottom:1px dashed var(--hair)}
  .skills-row .cat{font-size:12.5px;font-weight:600;color:var(--muted)}
  .skills-row .tags{font-size:12.5px;color:var(--ink)}
  .skills-row .tags b{color:var(--accent-ink)}
</style>
```

> 上面**不含** `.viewport / .page / #source / @media print`——那些归预览外壳 `assets/preview-shell.html`，`wrap_preview.py` 会把本 `<style>` 注入到 `<head>`。

## 组件库（带 `{{占位符}}`，class 与上面 `<style>` 对应）

### 1. Header（姓名 / 方向 / 教育 / 联系方式 / 证件照）—— `self-intro` 模块用它

```html
<header class="resume-header">
  <div class="ident">
    <div class="name-row"><span class="name">{{name}}</span><span class="role">{{role}}</span></div>
    <div class="edu-line">{{education}}</div>
    <div class="contact">{{gender}}<span class="sep">·</span>{{location}}<span class="sep">·</span>{{phone}}<span class="sep">·</span>{{email}}<span class="sep">·</span><a href="{{site-url}}">{{site}}</a></div>
  </div>
  {{photo}}
</header>
```

- `{{role}}` = 求职/申请方向（如"申请方向 · 计算机科学 直博"），无则连同 `<span class="role">` 一起删。
- `{{education}}` 单独一行（如"学校 · 专业 · 学历 · 届"），来自 `education:` 字段，无则删整行。
- `{{photo}}`：有真实头像用 `<div class="photo"><img src="{{avatar}}" alt="证件照"></div>`；没有用 [icons.md](icons.md) 里的证件照占位。
- 联系方式字段**按 `self-intro` 里实际有的拼**，字段之间用 `<span class="sep">·</span>` 分隔；没有的字段（如无 site）连同它的 `sep` 一起删，不要留空段。

### 2. SectionHead（模块标题：图标 + 中文 + 可选英文 + 发丝线）

```html
<div class="sec-head" data-stick="1">{{icon}}<h2>{{title}}<span class="en">{{en}}</span></h2></div>
```

- `data-stick="1"` **必带**——让分页 JS 不把标题和它下一条目拆到两页。
- `{{icon}}`：按模块语义从 [icons.md](icons.md) 选一个 `<svg class="ico" …>…</svg>`。
- `{{en}}`：英文小标签（可选），无则连 `<span class="en">` 一起删。

### 3. Summary（个人简介段落）

```html
<div class="summary"><p>{{text}}</p></div>
```

段落里 1–3 个最关键短语用 `<b>…</b>` 加重（转成强调字色）；`{{text}}` 是 `self-intro` 之后的"个人简介"模块正文。

### 4. Interests（研究兴趣 / 方向标签，可选）

```html
<div class="interests"><span class="it">{{tag1}}</span><span class="it">{{tag2}}</span><span class="it">{{tag3}}</span></div>
```

（每个标签一个 `<span class="it">`，按 MD 里给的标签数量增减。）

### 5. Entry header（教育 / 科研 / 实习 / 工作头）—— `##` 子标题用它

```html
<div class="entry" data-stick="1">
  <div class="entry-main">
    <div class="entry-title"><span class="org">{{org}}</span><span class="role">{{role}}</span></div>
    <span class="entry-date">{{date}}</span>
  </div>
  <div class="entry-meta"><span>{{meta-item-1}}</span><span>{{meta-item-2}}</span></div>
</div>
```

- `{{org}}` = `##` 标题里 `|` 左侧（机构/公司/学校）；`{{role}}` = `|` 右侧（岗位/方向/学位）。`##` 不含 `|` 时 `{{role}}` 连 `<span class="role">` 删除。
- `{{date}}` 来自 `##` 下的 `date:` 行；没有则删 `.entry-date`。
- `.entry-meta`：来自 `meta:` 行或 GPA/排名等；关键数字用 `<b>`，无 meta 整个 div 删。
- `data-stick="1"` 让 header 和第一条 bullet 同页不分家。

### 6. Bullet（单条经历要点 — 独立原子，自由换页）

```html
<div class="bullet">{{text}}</div>
```

每条 `- bullet` 拆一个独立原子。STAR 法则、量化结果，关键数字/术语用 `<span class="num">…</span>` 加重（等宽 + 强调色）。

### 7. Pubs（论文发表，可选）—— 论文模块用

```html
<ul class="pubs">
  <li><span class="tag">[C]</span> {{authors}} <b>{{title}}</b> <span class="ven">{{venue}}</span>, <span class="yr">{{year}}.</span></li>
</ul>
```

- `{{tag}}` 类型标：`[C]` 会议 / `[J]` 期刊 / `[W]` Workshop / `[P]` 专利。
- 本人名字用 `<span class="me">…</span>` 加下划线；共一/一作用括注。
- 每篇一个 `<li>`。

### 8. Awards（荣誉奖项网格，可选）—— 获奖模块用

```html
<div class="awards">
  <div class="award"><span class="yr">{{year}}</span><span>{{name}}</span><span class="lvl">{{level}}</span></div>
</div>
```

每项一个 `.award`；`{{level}}` = 国家级/省级/校级/金牌 等，无则删 `.lvl`。

### 9. Skills（技能 / 英语，类别 + 标签）

```html
<div class="skills">
  <div class="skills-row"><span class="cat">{{category}}</span><span class="tags">{{tags}}</span></div>
</div>
```

每类一个 `.skills-row`；`{{tags}}` 里最熟的几项用 `<b>` 加重（如 `<b>PyTorch</b> · JAX · …`）。

## 简历骨架（装配顺序）

```
<header class="resume-header"> … </header>          ← 由 self-intro 装配（姓名/方向/联系方式/证件照）
（按简历 MD 里 # 模块的顺序，每个模块依次：）
  <div class="sec-head" data-stick="1"> … </div>     ← SectionHead（icon 按模块语义选）
  <该模块的正文组件>                                  ← Summary / Interests / Entry×N / Bullet×N / Pubs / Awards / Skills
```

- **模块顺序 = MD 里 `#` 出现的顺序**（self-intro 永远第一，且不渲染成 SectionHead，而是渲染成 Header）。
- 每个 `# 模块` 都先出 SectionHead，再出该模块的正文组件。
- `## 子标题`：header（`.entry`）一条，`- bullet` 每条独立 `.bullet` 原子。

## Markdown → 组件映射规则表

| 简历 MD 元素 | 组件 | 备注 |
|------|------|------|
| `# self-intro`（首个，key:value） | Header（1.） | `name/role/gender/location/phone/email/site/avatar` → Header 各槽位；不渲染 SectionHead |
| `# 其它模块标题` | SectionHead（2.） | icon 按模块语义从 icons.md 选；英文标签可选 |
| 模块下纯文本段 | Summary（3.） | 关键短语 `<b>` |
| 模块下"标签, 标签, 标签"单行 | Interests（4.） | 研究兴趣/方向 |
| `## org \| role` | Entry header（5.）的 org/role | `|` 分割；无 `|` 则只有 org |
| `##` 下 `date: …` | Entry 的 `.entry-date` | |
| `##` 下 `meta: …` | Entry 的 `.entry-meta` | 关键数字 `<b>` |
| `##` 下 `- bullet` | 独立 Bullet（6.） | 每条一条；STAR + 量化；数字 `<span class="num">` |
| 论文模块条目 | Pubs（7.） | 类型标/venue/年份/本人下划线 |
| 获奖模块条目 | Awards（8.） | 年/名/级别 |
| `- 类别: 值`（技能） | Skills（9.）的 `.skills-row` | cat + tags |

## 配色约束（本主题已遵守，换色时保持）

- **唯一点缀色** `--accent` 墨蓝；强调字 `--accent-ink` 同色系更深。**不引第二个彩色**。
- 姓名 25px（正常简历字号，**不是报头巨标题**）；无首字下沉、无杂志编号、无 masthead。
- 单栏；分割线只用 1px 发丝 / 虚线，不堆色块。
