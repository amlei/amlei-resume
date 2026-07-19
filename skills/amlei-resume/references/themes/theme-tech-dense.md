# 主题 · 互联网技术硬核风（`tech-dense`）

> 单栏 · 高密度 · 工程蓝单点缀色 · 技术栈前置（mono chips）· 描边 SVG 图标 · `•` 列表符。
> 适用于互联网技术 / 算法 / 后端 / 基础架构 / AI 工程校招。
>
> **用法**：渲染时把"完整 `<style>`"整段作为产物开头，再按"简历骨架"用各组件（带 `{{占位符}}`）装配正文原子。HTML 一律从本文件取。

## 设计变量速查表

| 变量 | 值 | 用途 |
|------|-----|------|
| `--bg` | `oklch(94% .004 240)` | 视口舞台底色 |
| `--paper` | `oklch(99.4% .002 240)` | A4 纸张面 |
| `--ink` | `oklch(19% .015 240)` | 正文 |
| `--muted` | `oklch(43% .013 240)` | 次要文字 |
| `--faint` | `oklch(55% .011 240)` | 日期 |
| `--border` / `--hair` | `oklch(87% .008 240)` / `oklch(90% .006 240)` | 边框 / 发丝线 |
| `--accent` | `oklch(46% .17 242)` | **唯一**点缀色（工程蓝） |
| `--accent-ink` | `oklch(38% .15 242)` | 强调字色 |
| `--accent-soft` | `oklch(95% .03 242)` | 强调浅底（role 胶囊 / strong chip） |

## 完整 `<style>`（渲染时整段贴在产物最前）

```html
<style>
  :root{
    --bg:oklch(94% .004 240);--paper:oklch(99.4% .002 240);--ink:oklch(19% .015 240);--muted:oklch(43% .013 240);
    --faint:oklch(55% .011 240);--border:oklch(87% .008 240);--hair:oklch(90% .006 240);
    --accent:oklch(46% .17 242);--accent-ink:oklch(38% .15 242);--accent-soft:oklch(95% .03 242);
    --font-sans:'PingFang SC','HarmonyOS Sans SC','Microsoft YaHei','Hiragino Sans GB',-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;
    --font-mono:'JetBrains Mono','SF Mono',ui-monospace,'SFMono-Regular',Menlo,Consolas,monospace;
  }
  body{background:var(--bg);color:var(--ink);font-family:var(--font-sans);font-size:14px;line-height:1.58;-webkit-font-smoothing:antialiased;font-feature-settings:'tnum' on;text-rendering:optimizeLegibility}
  .page{background:var(--paper)}
  .page-content{padding:13mm 15mm 13mm}                 /* 比外壳默认更紧，技术岗高密度 */
  /* Header */
  .resume-header{display:grid;grid-template-columns:1fr auto;gap:18px;align-items:center;padding-bottom:12px;border-bottom:2px solid var(--ink)}
  .name-row{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
  .name-row .name{font-weight:700;font-size:26px;letter-spacing:.04em}
  .name-row .role{font-size:13px;font-weight:600;color:var(--accent-ink);background:var(--accent-soft);padding:3px 9px}
  .contact{margin-top:8px;font-family:var(--font-mono);font-size:11px;color:var(--muted)}
  .contact .sep{color:var(--accent);margin:0 6px}
  .contact a{color:var(--accent-ink);text-decoration:none}
  .edu-line{margin-top:6px;font-family:var(--font-sans);font-size:12px;color:var(--accent-ink);font-weight:500}
  .photo{width:26mm;height:36mm;border:1px solid var(--border);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5px;color:var(--faint);overflow:hidden}
  .photo img{width:100%;height:100%;object-fit:cover;display:block}
  .photo svg{width:26px;height:26px;opacity:.45}
  .photo span{font-size:10px;letter-spacing:.1em}
  /* SectionHead（无英文标签） */
  .sec-head{display:flex;align-items:center;gap:8px;margin-top:15px;margin-bottom:8px}
  .sec-head .ico{width:15px;height:15px;color:var(--accent);flex-shrink:0}
  .sec-head h2{font-size:14px;font-weight:700;letter-spacing:.16em;color:var(--ink)}
  .sec-head::after{content:"";flex:1;height:1px;background:var(--hair)}
  .summary p{font-size:13px;line-height:1.7;text-align:justify;text-wrap:pretty}
  .summary p strong{color:var(--accent-ink);font-weight:600}
  /* 技术栈 chips */
  .stack{display:flex;flex-direction:column;gap:6px}
  .stack-row{display:grid;grid-template-columns:64px 1fr;gap:10px;align-items:start}
  .stack-row .cat{font-family:var(--font-mono);font-size:11px;color:var(--accent);padding-top:3px;letter-spacing:.04em}
  .chips{display:flex;flex-wrap:wrap;gap:4px}
  .chip{font-family:var(--font-mono);font-size:11.5px;color:var(--ink);border:1px solid var(--border);padding:1.5px 7px}
  .chip.strong{color:var(--accent-ink);background:var(--accent-soft);border-color:oklch(80% .04 242);font-weight:600}
  /* Entry */
  .entry{margin-bottom:10px}
  .entry-main{display:grid;grid-template-columns:1fr auto;align-items:baseline;gap:14px}
  .entry-title{display:flex;align-items:baseline;gap:9px;flex-wrap:wrap}
  .entry-title .org,.entry-title .proj{font-size:14px;font-weight:700}
  .entry-title .role{font-size:13px;color:var(--accent-ink);font-weight:500}
  .entry-title .badge{font-family:var(--font-mono);font-size:10.5px;color:var(--accent-ink);border:1px solid var(--accent);padding:1px 6px}
  .entry-date{font-family:var(--font-mono);font-size:11px;color:var(--faint);white-space:nowrap}
  .entry-meta{margin-top:2px;font-size:11.5px;color:var(--muted);display:flex;gap:12px;flex-wrap:wrap}
  .entry-meta b{color:var(--ink);font-weight:600}
  .entry-list{list-style:none;margin-top:4px}
  .entry-list li{position:relative;padding-left:13px;font-size:12.5px;line-height:1.68;color:var(--ink);margin-bottom:2px;text-align:justify;text-wrap:pretty}
  .entry-list li::before{content:"•";position:absolute;left:1px;top:5px;color:var(--accent);font-size:10px;line-height:1}
  .entry-list .num,.entry-list .kw{font-family:var(--font-mono);color:var(--accent-ink);font-weight:600}
  /* Bullet（独立原子，自由换页） */
  .bullet{position:relative;padding-left:13px;font-size:12.5px;line-height:1.68;color:var(--ink);margin-bottom:2px;text-align:justify;text-wrap:pretty}
  .bullet::before{content:"•";position:absolute;left:1px;top:5px;color:var(--accent);font-size:10px;line-height:1}
  .bullet .num,.bullet .kw{font-family:var(--font-mono);color:var(--accent-ink);font-weight:600}
  /* 论文 / 竞赛 */
  .pub{font-size:12.5px;line-height:1.55;padding:4px 0;border-bottom:1px dashed var(--hair)}
  .pub .ven{font-style:italic;color:var(--accent-ink)}
  .pub .yr{font-family:var(--font-mono);color:var(--faint);font-size:11px;margin-left:6px}
  .awards{display:grid;grid-template-columns:1fr 1fr;gap:2px 22px;margin-top:4px}
  .award{display:grid;grid-template-columns:54px 1fr auto;gap:7px;align-items:baseline;font-size:12.5px;padding:3px 0;border-bottom:1px dashed var(--hair)}
  .award .tag{font-family:var(--font-mono);font-size:10.5px;color:var(--accent)}
  .award .lvl{font-size:11px;color:var(--accent-ink);font-weight:600}
</style>
```

> 不含 `.viewport/.page 尺寸/#source/@media print`（归预览外壳）。`.page-content` 在此覆写为 `13mm 15mm`（技术岗更密）。

## 组件库（带 `{{占位符}}`）

### 1. Header
```html
<header class="resume-header">
  <div class="ident">
    <div class="name-row"><span class="name">{{name}}</span><span class="role">{{role}}</span></div>
    <div class="edu-line">{{education}}</div>
    <div class="contact">{{gender}}<span class="sep">·</span>{{location}}<span class="sep">·</span>{{phone}}<span class="sep">·</span>{{email}}<span class="sep">·</span><a href="{{github-url}}">{{github}}</a></div>
  </div>
  {{photo}}
</header>
```
`{{role}}` = 求职意向（带浅底胶囊）。`{{education}}` 单独一行，来自 `education:` 字段（如学校 · 专业 · 学历 · 届）。联系方式按 self-intro 实际字段拼，字段间用 `<span class="sep">·</span>`，缺的字段连同 sep 删。

### 2. SectionHead（无英文标签）
```html
<div class="sec-head" data-stick="1">{{icon}}<h2>{{title}}</h2></div>
```

### 3. Summary
```html
<div class="summary"><p>{{text}}</p></div>
```
关键短语用 `<strong>`（转强调字色）。

### 4. 技术栈 Stack（mono chips，技术栈模块用它，**前置**）
```html
<div class="stack">
  <div class="stack-row"><span class="cat">{{category}}</span><div class="chips"><span class="chip strong">{{skill}}</span><span class="chip">{{skill}}</span></div></div>
</div>
```
最熟的技能加 `class="chip strong"`。每类一个 `.stack-row`。

### 5. Entry header（教育 / 实习 / 工作头；项目用 `.proj` + `.badge`）
```html
<div class="entry" data-stick="1">
  <div class="entry-main"><div class="entry-title"><span class="org">{{org}}</span><span class="role">{{role}}</span></div><span class="entry-date">{{date}}</span></div>
  <div class="entry-meta"><span>{{meta}}</span></div>
</div>
```
项目经历把 `<span class="org">` 换成 `<span class="proj">{{项目名}}</span>`，并加 `<span class="badge">{{开源 · 1.2k★}}</span>`（无可删）。`data-stick="1"` 让 header 和第一条 bullet 同页不分家。

### 6. Bullet（单条经历要点 — 独立原子，自由换页）
```html
<div class="bullet">{{text}}</div>
```
数字/术语用 `<span class="num">` 或 `<span class="kw">`。每条 `- bullet` 拆一个独立原子。

### 7. Pub（论文，单行 div）
```html
<div class="pub">{{authors}} <span class="ven">{{venue}}</span> {{note}}<span class="yr">{{year}}</span></div>
```

### 8. Awards（竞赛 / 证书，按 tag 分组）
```html
<div class="awards"><div class="award"><span class="tag">{{ACM-ICPC}}</span><span>{{name}}</span><span class="lvl">{{level}}</span></div></div>
```

## 简历骨架
Header → 技术栈（**建议前置**）→ 个人简介 → 教育/实习/项目（按 MD 模块顺序）→ 论文与竞赛。每模块先 SectionHead 再正文组件。

## MD → 组件映射
`# self-intro`→Header；`# 技术栈`下`类别: A, B, C`→`.stack-row`（最熟项标 strong）；`# 个人简介`→Summary；`## org|role`→Entry header（`data-stick="1"`）；`date:/meta:`→Entry 内；`- bullet`→每条独立 `.bullet`；论文行→`.pub`；`tag | name | level`→`.award`。
