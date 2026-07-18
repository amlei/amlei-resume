# 主题 · 内容 / 媒体风（`content-green`）

> 单栏 · 深森林绿单点缀色 · 证件照 · 描边 SVG 图标 · `•` 列表符 · 技能用浅底标签。
> 适用于内容 / 运营 / 增长 / 新媒体 / 产品（内容向）。
>
> **用法**：渲染时把"完整 `<style>`"整段作为产物开头，再按骨架用组件装配。HTML 一律从本文件取。

## 设计变量速查表

| 变量 | 值 | 用途 |
|------|-----|------|
| `--bg` | `oklch(94% .003 155)` | 舞台底色 |
| `--paper` | `oklch(99.3% .003 90)` | A4 纸张（微暖） |
| `--ink` | `oklch(20% .012 155)` | 正文 |
| `--muted` / `--faint` | `oklch(44% .012 155)` / `oklch(55% .010 155)` | 次要 / 日期 |
| `--border` / `--hair` | `oklch(88% .008 155)` / `oklch(91% .006 155)` | 边框 / 发丝线 |
| `--accent` | `oklch(40% .06 155)` | **唯一**点缀色（深森林绿） |
| `--accent-ink` / `--accent-soft` | `oklch(30% .05 155)` / `oklch(95% .022 155)` | 强调字色 / 浅底 |

## 完整 `<style>`（渲染时整段贴在产物最前）

```html
<style>
  :root{
    --bg:oklch(94% .003 155);--paper:oklch(99.3% .003 90);--ink:oklch(20% .012 155);
    --muted:oklch(44% .012 155);--faint:oklch(55% .010 155);--border:oklch(88% .008 155);--hair:oklch(91% .006 155);
    --accent:oklch(40% .06 155);--accent-ink:oklch(30% .05 155);--accent-soft:oklch(95% .022 155);
    --font-sans:'PingFang SC','HarmonyOS Sans SC','Microsoft YaHei','Hiragino Sans GB',-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;
    --font-mono:'JetBrains Mono','SF Mono',ui-monospace,'SFMono-Regular',Menlo,Consolas,monospace;
  }
  body{background:var(--bg);color:var(--ink);font-family:var(--font-sans);font-size:14px;line-height:1.6;-webkit-font-smoothing:antialiased;font-feature-settings:'tnum' on;text-rendering:optimizeLegibility}
  .page{background:var(--paper)}
  .resume-header{display:grid;grid-template-columns:1fr auto;gap:18px;align-items:center;padding-bottom:13px;border-bottom:1.5px solid var(--ink)}
  .name-row{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
  .name-row .name{font-weight:700;font-size:28px;letter-spacing:.04em}
  .name-row .role{font-size:13px;font-weight:600;color:var(--accent-ink)}
  .contact{margin-top:8px;font-family:var(--font-mono);font-size:11px;color:var(--muted)}
  .contact .sep{color:var(--accent);margin:0 6px}
  .photo{width:26mm;height:36mm;border:1px solid var(--border);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5px;color:var(--faint);overflow:hidden}
  .photo img{width:100%;height:100%;object-fit:cover;display:block}
  .photo svg{width:26px;height:26px;opacity:.45}
  .photo span{font-size:10px;letter-spacing:.1em}
  .sec-head{display:flex;align-items:center;gap:8px;margin-top:16px;margin-bottom:9px}
  .sec-head .ico{width:15px;height:15px;color:var(--accent);flex-shrink:0}
  .sec-head h2{font-size:14px;font-weight:700;letter-spacing:.12em;color:var(--ink)}
  .sec-head::after{content:"";flex:1;height:1px;background:var(--hair)}
  .summary p{font-size:13px;line-height:1.8;text-align:justify;text-wrap:pretty}
  .summary p strong{color:var(--accent-ink);font-weight:600}
  .entry{margin-bottom:11px}
  .entry-main{display:grid;grid-template-columns:1fr auto;align-items:baseline;gap:14px}
  .entry-title{display:flex;align-items:baseline;gap:9px;flex-wrap:wrap}
  .entry-title .org,.entry-title .proj{font-size:14px;font-weight:700}
  .entry-title .role{font-size:13px;font-weight:500;color:var(--accent-ink)}
  .entry-title .badge{font-size:11px;font-weight:600;color:var(--accent-ink);background:var(--accent-soft);padding:2px 7px}
  .entry-date{font-family:var(--font-mono);font-size:11px;color:var(--faint);white-space:nowrap}
  .entry-meta{margin-top:3px;font-size:11.5px;color:var(--muted);display:flex;gap:14px;flex-wrap:wrap}
  .entry-meta b{color:var(--ink);font-weight:600}
  .entry-list{list-style:none;margin-top:5px}
  .entry-list li{position:relative;padding-left:13px;font-size:12.5px;line-height:1.58;color:var(--ink);margin-bottom:2px;text-align:justify;text-wrap:pretty}
  .entry-list li::before{content:"•";position:absolute;left:1px;top:5px;color:var(--accent);font-size:10px;line-height:1}
  .entry-list .num{font-family:var(--font-mono);color:var(--accent-ink);font-weight:600}
  .awards{display:grid;grid-template-columns:1fr 1fr;gap:3px 24px}
  .award{display:grid;grid-template-columns:38px 1fr auto;gap:8px;align-items:baseline;font-size:12.5px;padding:4px 0;border-bottom:1px dashed var(--hair)}
  .award .yr{font-family:var(--font-mono);font-size:10.5px;color:var(--accent)}
  .award .lvl{font-size:11px;color:var(--accent-ink);font-weight:600}
  .skills{display:flex;flex-direction:column;gap:6px}
  .skill-row{display:grid;grid-template-columns:78px 1fr;gap:12px;align-items:start}
  .skill-row .cat{font-size:12.5px;font-weight:600;color:var(--muted);padding-top:2px}
  .skill-row .tags{display:flex;flex-wrap:wrap;gap:5px}
  .skill-row .tag{font-size:12.5px;color:var(--ink);border:1px solid var(--border);padding:2px 8px}
  .skill-row .tag.strong{color:var(--accent-ink);background:var(--accent-soft);border-color:var(--accent-soft);font-weight:600}
</style>
```

## 组件库（带 `{{占位符}}`）

### 1. Header
```html
<header class="resume-header">
  <div class="ident">
    <div class="name-row"><span class="name">{{name}}</span><span class="role">{{role}}</span></div>
    <div class="contact">{{location}}<span class="sep">·</span>{{phone}}<span class="sep">·</span>{{email}}<span class="sep">·</span>{{platform}}<span class="sep">·</span>{{age}} 岁<span class="sep">·</span>{{political}}</div>
  </div>
  {{photo}}
</header>
```
按实际字段拼；`{{platform}}` 可放小红书/公众号等，`{{political}}` 政治面貌（中共党员等，没有就删）。

### 2. SectionHead（无英文标签）
```html
<div class="sec-head" data-stick="1">{{icon}}<h2>{{title}}</h2></div>
```

### 3. Summary
```html
<div class="summary"><p>{{text}}</p></div>
```
关键短语用 `<strong>`。

### 4. Entry（教育 / 实习 / 项目；项目用 `.proj`，可加 `.badge`）
```html
<div class="entry">
  <div class="entry-main"><div class="entry-title"><span class="org">{{org}}</span><span class="role">{{role}}</span><span class="badge">{{badge}}</span></div><span class="entry-date">{{date}}</span></div>
  <div class="entry-meta"><span>{{meta}}</span></div>
  <ul class="entry-list"><li>{{bullet}}</li></ul>
</div>
```
项目用 `<span class="proj">{{项目名}}</span>`；`.badge`（如「辅修 交互设计」「产品负责人」）可加可不加。数字用 `<span class="num">`。

### 5. Awards（获奖与证书，按年份）
```html
<div class="awards"><div class="award"><span class="yr">{{year}}</span><span>{{name}}</span><span class="lvl">{{level}}</span></div></div>
```

### 6. Skills（相关技能，浅底标签）
```html
<div class="skills">
  <div class="skill-row"><span class="cat">{{category}}</span><div class="tags"><span class="tag strong">{{skill}}</span><span class="tag">{{skill}}</span></div></div>
</div>
```
最熟的加 `class="tag strong"`。

## 简历骨架
Header → 个人简介 → 教育背景 → 实习经历 → 项目经历 → 获奖与证书 → 相关技能（按 MD 模块顺序）。

## MD → 组件映射
`# self-intro`→Header；`# 个人简介`→Summary；`## org|role`→Entry（项目用 proj+badge）；`- bullet`→`.entry-list li`；`年份 | name | level`→`.award`；`类别: A, B`→`.skill-row`（最熟标 strong）。
