# 主题 · 学术 / 科研 CV（`academic`）

> 单栏 · 墨蓝单点缀色 · 证件照 · 描边 SVG 图标 · `•` 列表符 · 论文列表 · 奖项网格。
> 适用于升学 / PhD 申请 / 科研岗。
>
> **用法**：基准组件（Header/SectionHead/Summary/Entry/Bullet 等）读 [component-library.md](component-library.md)，本文只含本主题的设计令牌、`<style>` 与差异。渲染时把"完整 `<style>`"整段作为产物开头，再按共享库骨架用基准组件 + 本文差异装配。HTML 一律从文件取，不要凭记忆手写。

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
  .summary p b{color:var(--accent-ink);font-weight:600}
  .interests{display:flex;flex-wrap:wrap;gap:6px;margin-top:4px}
  .interests .it{font-size:12.5px;color:var(--accent-ink);background:oklch(95% .01 258);border:1px solid var(--border);padding:2px 8px}
  /* Entry */
  .entry{margin-bottom:8px}
  .entry-main{display:flex;align-items:baseline;justify-content:space-between;gap:14px;flex-wrap:nowrap}
  .entry-title{display:flex;align-items:baseline;gap:9px;flex-wrap:wrap}
  .entry-title .org{font-weight:700;font-size:14px}
  .entry-main .proj{font-weight:700;font-size:14.5px;letter-spacing:.01em}
  .entry-main .company{font-size:11.5px;color:var(--muted);font-weight:500;letter-spacing:.02em}
  .entry-title .role{font-size:13px;color:var(--accent-ink)}
  .entry-date{font-family:var(--font-mono);font-size:11px;color:var(--faint);white-space:nowrap;letter-spacing:.02em}
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
  .bullet strong,.bullet b{color:var(--accent-ink);font-weight:600}
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
  /* Skills（分类行内顶格，续行自然顶格） */
  .skills-row{padding:4px 0;border-bottom:1px dashed var(--hair);font-size:12.5px;color:var(--ink)}
  .skills-row .cat{font-weight:600;color:var(--muted)}
  .skills-row .tags{color:var(--ink)}
  .skills-row .tags b{color:var(--accent-ink)}
</style>
```

> 上面**不含** `.viewport / .page / #source / @media print`——那些归预览外壳 `../../scripts/preview-shell.html`，`wrap_preview.py` 会把本 `<style>` 注入到 `<head>`。

## 主题差异（相对共享组件库）

本主题的 class 命名即共享库的 canonical 命名，`<style>` 无需映射。

- **启用组件**：全部基准组件，含可选 **Interests**（研究兴趣/方向标签）与 **Pubs**（论文列表）。
- **Header 默认字段集**：`{{gender}}` · `{{location}}` · `{{phone}}` · `{{email}}` · `<a href="{{site-url}}">{{site}}</a>`（个人主页/Google Scholar）。
- **`{{role}}`** = 求职/申请方向（如「申请方向 · 计算机科学 直博」）。
- **SectionHead**：可带 `.en` 英文小标签（如 EDUCATION），无则删。
- **Pubs**：用全量形态——类型标 `[C]`/`[J]`/`[W]`/`[P]` + `.me` 本人下划线（共一/一作括注）。
- **Entry**：meta 常放 GPA/排名，关键数字 `<b>`。
- **骨架**：共享库标准顺序。
- **配色约束**（换色时保持）：唯一点缀色 `--accent` 墨蓝，强调字 `--accent-ink` 同色系更深，**不引第二个彩色**；姓名 26px（正常简历字号，非报头巨标题），无首字下沉、无杂志编号、无 masthead；单栏；分割线只用 1px 发丝 / 虚线，不堆色块。
