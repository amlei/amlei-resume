# 主题 · 国企 / 银行正式风（`soe-formal`）

> 单栏 · 藏青（navy）单色 · 证件照 · **基本信息表（含政治面貌 / 籍贯 / 民族 / 出生年月）** · 描边 SVG 图标 · `•` 列表符 · 简介带左竖条。
> 适用于国企 / 银行 / 央企 / 公职 / 体制内。
>
> **用法**：渲染时把"完整 `<style>`"整段作为产物开头，再按骨架用组件装配。HTML 一律从本文件取。

## 设计变量速查表

| 变量 | 值 | 用途 |
|------|-----|------|
| `--bg` | `oklch(93% .003 250)` | 舞台底色 |
| `--paper` | `oklch(100% 0 0)` | A4 纸张（纯白） |
| `--ink` | `oklch(20% .018 255)` | 正文 |
| `--muted` / `--faint` | `oklch(45% .018 255)` / `oklch(55% .014 255)` | 次要 / 弱 |
| `--rule` / `--hair` / `--border` | `oklch(84% .012 255)` / `oklch(90% .008 255)` / `oklch(88% .01 255)` | 表格线 / 发丝 / 边框 |
| `--navy` | `oklch(31% .058 258)` | **唯一**点缀色（藏青，本主题用 navy 而非 accent） |
| `--navy-deep` / `--navy-soft` | `oklch(24% .06 258)` / `oklch(95% .012 258)` | 深藏青字色 / 浅藏青底 |

## 完整 `<style>`（渲染时整段贴在产物最前）

```html
<style>
  :root{
    --bg:oklch(93% .003 250);--paper:oklch(100% 0 0);--ink:oklch(20% .018 255);--muted:oklch(45% .018 255);
    --faint:oklch(55% .014 255);--rule:oklch(84% .012 255);--hair:oklch(90% .008 255);--border:oklch(88% .01 255);
    --navy:oklch(31% .058 258);--navy-deep:oklch(24% .06 258);--navy-soft:oklch(95% .012 258);
    --font-sans:'PingFang SC','HarmonyOS Sans SC','Microsoft YaHei','Hiragino Sans GB',-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;
    --font-mono:'JetBrains Mono','SF Mono',ui-monospace,Menlo,Consolas,monospace;
  }
  body{background:var(--bg);color:var(--ink);font-family:var(--font-sans);font-size:14px;line-height:1.6;-webkit-font-smoothing:antialiased;font-feature-settings:'tnum' on;text-rendering:optimizeLegibility}
  .page{background:var(--paper)}
  .resume-header{display:grid;grid-template-columns:1fr auto;gap:22px;align-items:start;padding-bottom:12px;border-bottom:2.5px solid var(--navy)}
  .name-block .cn{font-weight:900;font-size:32px;color:var(--navy-deep);letter-spacing:.14em;line-height:1}
  .name-block .en{font-weight:500;font-size:11px;color:var(--faint);letter-spacing:.32em;margin-top:6px}
  .name-block .intent{margin-top:11px;font-size:13px;color:var(--ink)}
  .name-block .intent b{color:var(--navy-deep);font-weight:700}
  .name-block .intent .sep{color:var(--faint);margin:0 8px}
  .photo{width:27mm;height:38mm;border:1px solid var(--rule);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5px;color:var(--faint);overflow:hidden}
  .photo img{width:100%;height:100%;object-fit:cover;display:block}
  .photo svg{width:26px;height:26px;opacity:.5}
  .photo span{font-size:10px;letter-spacing:.1em}
  .bio-form{display:grid;grid-template-columns:repeat(4,1fr);border:1px solid var(--rule);border-right:0;border-bottom:0;margin-top:12px}
  .bio-form>div{display:flex;gap:6px;padding:6px 11px;border-right:1px solid var(--rule);border-bottom:1px solid var(--rule);font-size:12.5px;align-items:baseline}
  .bio-form .k{color:var(--faint);font-size:11px;flex-shrink:0;letter-spacing:.04em}
  .bio-form .v{color:var(--ink);font-weight:500}
  .sec-head{display:flex;align-items:center;gap:9px;margin-top:18px;margin-bottom:10px}
  .sec-head .ico{width:15px;height:15px;color:var(--navy);flex-shrink:0}
  .sec-head h2{font-weight:700;font-size:15px;color:var(--navy-deep);letter-spacing:.1em}
  .sec-head h2 .en{font-weight:400;font-size:10px;color:var(--faint);letter-spacing:.22em;text-transform:uppercase;margin-left:7px}
  .sec-head::after{content:"";flex:1;height:1px;background:var(--hair)}
  .entry{margin-bottom:11px}
  .entry-main{display:grid;grid-template-columns:1fr auto;align-items:baseline;gap:14px}
  .entry-title{display:flex;align-items:baseline;gap:9px;flex-wrap:wrap}
  .entry-title .org,.entry-title .proj{font-weight:700;font-size:14px}
  .entry-title .role{font-size:13px;color:var(--navy-deep)}
  .entry-title .badge{font-size:10.5px;color:var(--navy-deep);background:var(--navy-soft);padding:1.5px 7px;letter-spacing:.04em}
  .entry-date{font-family:var(--font-mono);font-size:11px;color:var(--faint);white-space:nowrap}
  .entry-meta{margin-top:2px;font-size:11.5px;color:var(--muted);display:flex;gap:14px;flex-wrap:wrap}
  .entry-meta b{color:var(--ink);font-weight:600}
  .entry-list{list-style:none;margin-top:5px}
  .entry-list li{position:relative;padding-left:13px;font-size:12.5px;line-height:1.72;color:var(--ink);margin-bottom:2px;text-align:justify;text-wrap:pretty}
  .entry-list li::before{content:"•";position:absolute;left:1px;top:6px;color:var(--navy);font-size:10px;line-height:1}
  .entry-list .num{font-family:var(--font-mono);color:var(--navy-deep);font-weight:600}
  .awards{display:grid;grid-template-columns:1fr 1fr;gap:3px 24px}
  .award{display:grid;grid-template-columns:40px 1fr auto;gap:8px;align-items:baseline;font-size:12.5px;padding:4px 0;border-bottom:1px dashed var(--hair)}
  .award .yr{font-family:var(--font-mono);font-size:11px;color:var(--navy)}
  .award .lvl{font-size:11px;color:var(--navy-deep);font-weight:600}
  .skills{display:flex;flex-direction:column}
  .skills .row{display:grid;grid-template-columns:78px 1fr;gap:12px;padding:5px 0;border-bottom:1px dashed var(--hair)}
  .skills .cat{font-weight:700;font-size:12.5px;color:var(--navy-deep);letter-spacing:.04em}
  .skills .tags{font-size:12.5px;color:var(--ink)}
  .skills .tags b{color:var(--navy-deep);font-weight:600}
  .summary p{font-size:13px;line-height:1.82;color:var(--ink);text-align:justify;text-wrap:pretty;border-left:3px solid var(--navy-soft);padding-left:11px}
  .summary p b{color:var(--navy-deep)}
</style>
```

## 组件库（带 `{{占位符}}`）

### 1. Header（姓名块 + 证件照 + 基本信息表，**含政治面貌/籍贯**）
```html
<header class="resume-header">
  <div class="name-block">
    <div class="cn">{{name}}</div>
    <div class="en">{{CHEN SIYUAN}} · {{学位}}</div>
    <div class="intent">求职意向：<b>{{银行管培生 / 央企储备干部}}</b><span class="sep">·</span>期望地 {{city}}<span class="sep">·</span>到岗 {{time}}</div>
  </div>
  {{photo}}
  <div class="bio-form" style="grid-column:1 / -1">
    <div><span class="k">性别</span><span class="v">{{gender}}</span></div>
    <div><span class="k">出生年月</span><span class="v">{{birth}}</span></div>
    <div><span class="k">政治面貌</span><span class="v">{{political}}</span></div>
    <div><span class="k">籍贯</span><span class="v">{{hometown}}</span></div>
    <div><span class="k">民族</span><span class="v">{{ethnicity}}</span></div>
    <div><span class="k">学历</span><span class="v">{{education-level}}</span></div>
    <div><span class="k">电话</span><span class="v">{{phone}}</span></div>
    <div><span class="k">邮箱</span><span class="v">{{email}}</span></div>
  </div>
</header>
```
`bio-form` **8 格两行**（`grid-column:1 / -1` 满宽）。self-intro 里给政治面貌/籍贯/民族/出生年月就填，没给就留占位提示用户补——**国企风这些字段通常必备**。

### 2. SectionHead（中文 + 可选英文小标签）
```html
<div class="sec-head" data-stick="1">{{icon}}<h2>{{title}}<span class="en">{{EDUCATION}}</span></h2></div>
```

### 3. Entry（教育 / 实习 / 课题 / 校园；项目/课题用 `.proj` + `.badge`）
```html
<div class="entry">
  <div class="entry-main"><div class="entry-title"><span class="org">{{org}}</span><span class="role">{{role}}</span></div><span class="entry-date">{{date}}</span></div>
  <div class="entry-meta"><span>{{meta，关键 <b>}}</span></div>
  <ul class="entry-list"><li>{{bullet，数字 <span class="num">}}</li></ul>
</div>
```
课题/学生工作用 `<span class="proj">{{项目/组织}}</span>` + 可选 `<span class="badge">{{课题主笔 / 党支部书记}}</span>`。

### 4. Awards（荣誉奖项，按年份；含「优秀共产党员」等）
```html
<div class="awards"><div class="award"><span class="yr">{{year}}</span><span>{{name}}</span><span class="lvl">{{level}}</span></div></div>
```

### 5. Skills（技能与证书，类别 + 标签）
```html
<div class="skills">
  <div class="row"><span class="cat">{{专业技能}}</span><span class="tags"><b>{{财务建模}}</b> · {{估值分析}} · …</span></div>
  <div class="row"><span class="cat">{{资格证书}}</span><span class="tags"><b>{{证券从业}}</b> · <b>{{基金从业}}</b> · …</span></div>
</div>
```
资格证书单独一行，已取得的用 `<b>`。

### 6. Summary（自我评价，左竖条引用块，**放末尾**）
```html
<div class="summary"><p>{{自我评价，关键 <b>}}</p></div>
```

## 简历骨架
Header（含基本信息表）→ 教育背景 → 实习经历 → 课题与研究项目 → 校园经历与学生工作 → 荣誉奖项 → 技能与证书 → 自我评价（末尾）。

## MD → 组件映射
`# self-intro`→Header（`political/birth/hometown/ethnicity` 等填进 `bio-form`）；`# 教育背景`等→SectionHead；`## org|role`→Entry；`date:/meta:/- bullet`→Entry 内；`年份|name|level`→`.award`；`类别: 值`→`.skills .row`；`# 自我评价`→末尾 Summary 引用块。
