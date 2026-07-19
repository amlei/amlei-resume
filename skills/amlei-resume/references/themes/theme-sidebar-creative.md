# 主题 · 双栏侧边栏创意风（`sidebar-creative`）

> **双栏（64mm 侧栏 + 主体）· 暖珊瑚单点缀色 · 固定单页 · 仅建议创意岗**。
> 适用于 UI/UX / 视觉 / 交互 / 工业设计 / 创意岗。
>
> ⚠️ **本主题是特殊的"单页双栏"结构**，与其余单栏多页主题不同：
> - 正文原子是**唯一一个** `<div class="two-col">`（包住整页：左 `<aside class="sidebar">` + 右 `<main class="main">`）。**不要再放第二个原子**。
> - 内容**必须能放进一页 A4**（创意简历本就精简）。超出会被裁切（`.page{overflow:hidden}`），不会自动分页。
> - 章节标题用 `.sec-h`（不是 `.sec-head`），姓名区用 `.head`（不是 `.resume-header`）。
>
> **用法**：渲染时把"完整 `<style>`"整段作为产物开头，正文只放一个 `.two-col`。HTML 一律从本文件取。

## 设计变量速查表

| 变量 | 值 | 用途 |
|------|-----|------|
| `--bg` | `oklch(93% .004 40)` | 舞台底色 |
| `--paper` / `--sidebar` | `oklch(99.5% .002 60)` / `oklch(96.5% .012 40)` | 纸张 / 侧栏底色 |
| `--ink` | `oklch(22% .012 40)` | 正文 |
| `--muted` / `--faint` | `oklch(45% .012 40)` / `oklch(55% .010 40)` | 次要 / 弱 |
| `--border` / `--hair` | `oklch(88% .010 40)` / `oklch(90% .008 40)` | 边框 / 发丝线 |
| `--accent` | `oklch(56% .15 38)` | **唯一**点缀色（暖珊瑚） |
| `--accent-ink` / `--accent-soft` | `oklch(44% .14 38)` / `oklch(94% .03 40)` | 强调字色 / 浅底 |

## 完整 `<style>`（渲染时整段贴在产物最前）

```html
<style>
  :root{
    --bg:oklch(93% .004 40);--paper:oklch(99.5% .002 60);--sidebar:oklch(96.5% .012 40);
    --ink:oklch(22% .012 40);--muted:oklch(45% .012 40);--faint:oklch(55% .010 40);--border:oklch(88% .010 40);--hair:oklch(90% .008 40);
    --accent:oklch(56% .15 38);--accent-ink:oklch(44% .14 38);--accent-soft:oklch(94% .03 40);
    --font-sans:'PingFang SC','HarmonyOS Sans SC','Microsoft YaHei','Hiragino Sans GB',-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;
    --font-mono:'JetBrains Mono','SF Mono',ui-monospace,Menlo,Consolas,monospace;
  }
  body{background:var(--bg);color:var(--ink);font-family:var(--font-sans);font-size:14px;line-height:1.6;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
  .page{background:var(--paper)}
  .page-content{padding:0 !important}                 /* 覆写外壳内边距，让 two-col 满铺整页 */
  .two-col{position:absolute;inset:0;display:grid;grid-template-columns:64mm 1fr}
  .sidebar{background:var(--sidebar);padding:15mm 9mm 15mm;border-right:1px solid var(--border);display:flex;flex-direction:column;gap:16px}
  .photo{width:100%;aspect-ratio:3/4;border:1px solid var(--border);background:var(--paper);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;color:var(--faint);overflow:hidden}
  .photo img{width:100%;height:100%;object-fit:cover;display:block}
  .photo svg{width:34px;height:34px;opacity:.4}
  .photo span{font-size:10px;letter-spacing:.1em}
  .side-block h3{font-size:12px;font-weight:700;letter-spacing:.2em;color:var(--accent-ink);margin-bottom:9px}
  .side-block .row{font-size:13px;color:var(--ink);line-height:1.8}
  .side-block .row .k{color:var(--faint);font-size:12px;margin-right:5px}
  .side-block .row a{color:var(--accent-ink);text-decoration:none}
  .tools{display:flex;flex-wrap:wrap;gap:5px}
  .tools .t{font-size:12.5px;color:var(--ink);background:var(--paper);border:1px solid var(--border);padding:3px 8px}
  .main{padding:15mm 14mm 15mm}
  .head{padding-bottom:13px;border-bottom:2px solid var(--ink);margin-bottom:14px}
  .head .name{font-size:29px;font-weight:700;letter-spacing:.04em}
  .head .role{font-size:14px;font-weight:600;color:var(--accent-ink);margin-top:4px}
  .head .one{font-size:13px;color:var(--muted);margin-top:6px}
  .head .edu-line{font-size:13px;color:var(--accent-ink);font-weight:500;margin-top:4px}
  .sec-h{display:flex;align-items:center;gap:9px;margin-top:17px;margin-bottom:9px}
  .sec-h .ico{width:15px;height:15px;color:var(--accent);flex-shrink:0}
  .sec-h h2{font-size:14px;font-weight:700;letter-spacing:.14em;color:var(--ink)}
  .sec-h::after{content:"";flex:1;height:1px;background:var(--hair)}
  .summary{font-size:13px;line-height:1.8;text-align:justify;text-wrap:pretty}
  .summary b{color:var(--accent-ink)}
  .entry{margin-bottom:13px}
  .entry-main{display:grid;grid-template-columns:1fr auto;align-items:baseline;gap:10px}
  .entry-title{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}
  .entry-title .org,.entry-title .proj{font-size:14px;font-weight:700}
  .entry-title .role{font-size:13px;color:var(--accent-ink)}
  .entry-date{font-family:var(--font-mono);font-size:11px;color:var(--faint);white-space:nowrap}
  .entry-meta{font-size:12px;color:var(--muted);margin-top:2px}
  .entry-meta b{color:var(--ink)}
  .entry-list{list-style:none;margin-top:4px}
  .entry-list li{position:relative;padding-left:13px;font-size:12.5px;line-height:1.7;margin-bottom:2px;text-align:justify;text-wrap:pretty}
  .entry-list li::before{content:"•";position:absolute;left:1px;top:5px;color:var(--accent);font-size:10px;line-height:1}
  .entry-list .num{font-family:var(--font-mono);color:var(--accent-ink);font-weight:600}
  /* Bullet（此主题不原子化——保留以供引用；实际渲染不拆分） */
  .bullet{position:relative;padding-left:13px;font-size:12.5px;line-height:1.7;margin-bottom:2px;text-align:justify;text-wrap:pretty}
  .bullet::before{content:"•";position:absolute;left:1px;top:5px;color:var(--accent);font-size:10px;line-height:1}
  .bullet .num{font-family:var(--font-mono);color:var(--accent-ink);font-weight:600}
</style>
```

## 组件库（带 `{{占位符}}`）—— 全部包在唯一一个 `.two-col` 里

### 0. Two-col 整页骨架（正文只有这一个原子）
```html
<div class="two-col">
  <aside class="sidebar">
    {{photo-full}}
    <div class="side-block">…</div>   <!-- 联系方式 -->
    <div class="side-block">…</div>   <!-- 设计工具 -->
    <div class="side-block">…</div>   <!-- 设计理念 / 语言 / 基本信息，按需 -->
  </aside>
  <main class="main">
    <div class="head">…</div>
    <div class="sec-h">…</div><div class="summary">…</div>
    <!-- 教育 / 实习 / 项目 / 获奖，每个先 .sec-h 再内容 -->
  </main>
</div>
```

### 侧栏 · photo（满宽 3:4）
```html
<div class="photo">{{有头像: <img src="{{avatar}}" alt="证件照"> / 无: <svg …>占位</svg> + <span>证件照</span>}}</div>
```

### 侧栏 · side-block（标题 + 若干 row）
```html
<div class="side-block">
  <h3>{{联系方式}}</h3>
  <div class="row"><span class="k">{{城市}}</span>{{value}}</div>
  <div class="row"><span class="k">{{电话}}</span>{{phone}}</div>
  <div class="row"><a href="{{url}}">{{link}}</a></div>
</div>
```

### 侧栏 · tools（工具标签）
```html
<div class="side-block"><h3>{{设计工具}}</h3><div class="tools"><span class="t">{{Figma}}</span><span class="t">{{Sketch}}</span></div></div>
```

### 主体 · head（姓名 / 方向 / 教育 / 一句话）
```html
<div class="head">
  <div class="name">{{name}}</div>
  <div class="role">{{求职意向 · UI/UX 交互设计师}}</div>
  <div class="edu-line">{{education}}</div>
  <div class="one">{{学校 · 专业 · 一两句亮点}}</div>
</div>
```
`{{education}}` 可选单独行（来自 `education:` 字段），无则删整行。

### 主体 · sec-h（章节标题，注意是 `.sec-h`）
```html
<div class="sec-h">{{icon}}<h2>{{title}}</h2></div>
```

### 主体 · summary（直接文本，非 `<p>`）
```html
<div class="summary">{{text，关键短语用 <b>}}</div>
```

### 主体 · entry / entry-list（同单栏结构；项目用 `.proj`）
```html
<div class="entry">
  <div class="entry-main"><div class="entry-title"><span class="org">{{org}}</span><span class="role">{{role}}</span></div><span class="entry-date">{{date}}</span></div>
  <ul class="entry-list"><li>{{bullet，数字用 <span class="num">}}</li></ul>
</div>
```

### 获奖（本主题用 `.entry-list` 列表，不用网格）
```html
<ul class="entry-list" style="margin-top:2px">
  <li>{{红点设计概念奖}} · <span class="num">{{2024}}</span></li>
</ul>
```

## 简历骨架（单页！精简）
侧栏：photo → 联系方式 → 设计工具 → 设计理念 → 语言 → 基本信息。
主体：head → 个人简介 → 教育背景 → 实习经历 → 项目作品 → 获奖与荣誉。
**控制总量在一页 A4 内**；放不下就删次要模块或精简 bullet。

## MD → 组件映射
`# self-intro`→侧栏 photo + 联系方式 side-block + 基本信息 side-block；`name/role`→主体 `.head`；`# 模块`→主体 `.sec-h` + 内容；`## org|role`→`.entry`；`- bullet`→`.entry-list li`；设计工具/技能→侧栏 `.tools`；获奖→主体 `.entry-list`。
