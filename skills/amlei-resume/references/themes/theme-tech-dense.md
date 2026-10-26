# 主题 · 互联网技术硬核风（`tech-dense`）

> 单栏 · 高密度 · 工程蓝单点缀色 · 技术栈前置（mono 等级词文本行）· 描边 SVG 图标 · `•` 列表符。
> 适用于互联网技术 / 算法 / 后端 / 基础架构 / AI 工程校招。
>
> **用法**：基准组件（Header/SectionHead/Summary/Entry/Bullet 等）读 [component-library.md](component-library.md)，本文只含本主题的设计令牌、`<style>` 与差异。渲染时把"完整 `<style>`"整段作为产物开头，再按共享库骨架用基准组件 + 本文差异装配。HTML 一律从文件取，不要凭记忆手写。

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
| `--accent-soft` | `oklch(95% .03 242)` | 强调浅底（role 胶囊） |

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
  .summary p b{color:var(--accent-ink);font-weight:600}
  /* Skills（技术栈 mono 文本行：分类行内顶格，续行自然顶格） */
  .skills{display:flex;flex-direction:column;gap:6px}
  .skills-row{font-family:var(--font-mono);font-size:11.5px;color:var(--ink);line-height:1.7}
  .skills-row .cat{color:var(--accent);letter-spacing:.04em}
  .skills-row .tags{color:var(--ink)}
  .skills-row .tags b{color:var(--accent-ink);font-weight:600}
  /* Entry */
  .entry{margin-bottom:10px}
  .entry-main{display:flex;align-items:baseline;justify-content:space-between;gap:14px;flex-wrap:nowrap}
  .entry-title{display:flex;align-items:baseline;gap:9px;flex-wrap:wrap}
  .entry-title .org{font-size:14px;font-weight:700}
  .entry-main .proj{font-size:14.5px;font-weight:700;letter-spacing:.01em}
  .entry-main .company{font-family:var(--font-mono);font-size:11.5px;color:var(--muted);font-weight:500;letter-spacing:.02em}
  .entry-secondary .role,.entry-title .role{font-size:13px;color:var(--accent-ink);font-weight:500}
  .entry-secondary .badge,.entry-title .badge{font-family:var(--font-mono);font-size:10.5px;color:var(--accent-ink);border:1px solid var(--accent);padding:1px 6px}
  .entry-date{font-family:var(--font-mono);font-size:11px;color:var(--faint);white-space:nowrap;letter-spacing:.02em}
  .entry-meta{margin-top:2px;font-size:11.5px;color:var(--muted);display:flex;gap:12px;flex-wrap:wrap}
  .entry-meta b{color:var(--ink);font-weight:600}
  .entry-list{list-style:none;margin-top:4px}
  .entry-list li{position:relative;padding-left:13px;font-size:12.5px;line-height:1.68;color:var(--ink);margin-bottom:2px;text-align:justify;text-wrap:pretty}
  .entry-list li::before{content:"•";position:absolute;left:1px;top:5px;color:var(--accent);font-size:10px;line-height:1}
  .entry-list .num{font-family:var(--font-mono);color:var(--accent-ink);font-weight:600}
  /* Bullet（独立原子，自由换页） */
  .bullet{position:relative;padding-left:13px;font-size:12.5px;line-height:1.68;color:var(--ink);margin-bottom:2px;text-align:justify;text-wrap:pretty}
  .bullet::before{content:"•";position:absolute;left:1px;top:5px;color:var(--accent);font-size:10px;line-height:1}
  .bullet .num{font-family:var(--font-mono);color:var(--accent-ink);font-weight:600}
  .bullet strong,.bullet b{color:var(--accent-ink);font-weight:600}
  /* 论文 / 竞赛 */
  .pubs{list-style:none}
  .pubs li{font-size:12.5px;line-height:1.55;padding:4px 0;border-bottom:1px dashed var(--hair)}
  .pubs li .ven{font-style:italic;color:var(--accent-ink)}
  .pubs li .yr{font-family:var(--font-mono);color:var(--faint);font-size:11px;margin-left:6px}
  .awards{display:grid;grid-template-columns:1fr 1fr;gap:2px 22px;margin-top:4px}
  .award{display:grid;grid-template-columns:54px 1fr auto;gap:7px;align-items:baseline;font-size:12.5px;padding:3px 0;border-bottom:1px dashed var(--hair)}
  .award .yr{font-family:var(--font-mono);font-size:10.5px;color:var(--accent)}
  .award .lvl{font-size:11px;color:var(--accent-ink);font-weight:600}
</style>
```

> 不含 `.viewport/.page 尺寸/#source/@media print`（归预览外壳）。`.page-content` 在此覆写为 `13mm 15mm`（技术岗更密）。

## 主题差异（相对共享组件库）

- **启用组件**：Header / SectionHead / Summary / Entry / Bullet / Pubs / Awards / Skills；**不用** Interests。
- **Header 默认字段集**：`{{gender}}` · `{{location}}` · `{{phone}}` · `{{email}}` · `<a href="{{github-url}}">{{github}}</a>`；`{{role}}` = 求职意向（本主题带浅底胶囊，style 已实现）。
- **Skills = 技术栈**（技术栈模块用，**骨架前置**）：HTML 与共享库完全一致（`.skills-row`，分类行内顶格——cat 与描述同行、续行自然顶格，不用分类栅格列）；句读式排版（条目间「；」、行末「。」）；mono 字体纯文本行由本主题 style 实现，程度词规则同共享库。不使用 chip/标签。
- **SectionHead**：无英文标签。
- **Entry**：项目 `.company` 用 mono（工程感）；个人项目可写「个人项目」或留空删 `.company`。
- **Bullet**：数字 `<span class="num">`（mono 由 style 实现），术语 `<b>`。
- **Pubs**：简化形态——无类型标、无 `.me`：`<li>{{authors}} <span class="ven">{{venue}}</span> {{note}}<span class="yr">{{year}}</span></li>`。
- **Awards**：首格 `.yr` 放竞赛/类别名（分组用法，mono 蓝色由 style 实现）。
- **骨架**：Header → 技术栈（Skills，**前置**）→ 个人简介 → 教育/实习/项目（按 MD 模块顺序）→ 论文与竞赛。每模块先 SectionHead 再正文组件。
