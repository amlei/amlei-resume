# 预览与导出

用户要求导出 PDF 时执行。先校验格式，再装配 HTML。

## 产物目录

所有产物归集到 `resume/{姓名}/{求职岗位}/`——相对引用不会断、换岗位/换照片互不干扰。

## 校验

用 `scripts/validate_resume.py <简历.md>` 校验，ERROR 清零才算通过。校验不过不往下走。校验项：self-intro 首模块 / name 必填 / 标题层级 / 空模块 / date 格式。

## 选主题

读 [themes/theme-index.md](themes/theme-index.md)，据目标岗位 / 行业推荐最契合的主题：
- 用户已指定主题 → 直接用。
- 岗位有明确契合 → 推荐 + 1~2 个备选让用户选。
- 无明显倾向 → 默认 `academic`。
- `sidebar-creative` 是双栏单页，内容多不要选。

## 读组件库

读所选主题的 `references/theme-{标识}.md` + 共用的 [icons.md](icons.md)（按模块语义选 SVG 图标）。**装配 HTML 一律从所选主题的组件库取，不凭记忆手写。**

## 装配 HTML

按主题库的简历骨架装配：主题 `<style>`（整段照抄）放最前，再依次：

1. `# self-intro` → **Header** 组件（name/role/contact/photo；不渲染成 SectionHead）。
2. 每个 `# 模块` → **SectionHead**（icon 按 icons.md 选，`data-stick="1"` 必带）+ 模块正文组件。
3. `## 机构 | 角色` → **Entry**；其下 `date:` / `meta:` / `- bullets` 收进同一个 Entry。
4. 行内强调：`**词**` → 强调字色；关键数字 → 等宽强调（如 `<span class="num">`）。

产物 = `<style>…</style>` + 各原子，**不要**包 `<!DOCTYPE>/<html>/<head>/<body>`（预览壳负责）。

## 套预览壳

用 `scripts/wrap_preview.py`（`--help` 看参数）。产出 `resume/{姓名}/{求职岗位}/预览.html`（自动建目录，带「导出 PDF」工具条 + A4 自动分页），`document.title` = `姓名-岗位`（=「另存为 PDF」默认文件名）；用 `--name` 覆盖。

## 交付

打开 `resume/{姓名}/{求职岗位}/预览.html` →「导出 PDF」→ 浏览器选「另存为 PDF」即得 A4 简历。换主题：回「选主题」重选，重新装配 + 校验 + 套壳。

参考产物：[sample-preview.html](../assets/sample-preview.html)（academic 主题渲染 sample-resume.md）。

## 配色方案

预览页工具条「配色」下拉：8 套点缀色（墨蓝 / 工程蓝 / 森林绿 / 酒红 / 藏青 / 紫 / 琥珀 / 石墨黑）+「主题原色」。选择记在 localStorage，「导出 PDF」沿用——同一份简历可出多套配色。

## A4 与 PDF 导出

- 分页自动：内容超出 A4 自动溢出。
- 「导出 PDF」走浏览器原生打印：工具条自动隐藏，输出像素级 A4。

## 视觉红线

- **不做报刊排版**：无首字下沉、无报头巨标题；姓名 ≈24–26px。
- **单点缀色**：一个 `--accent` + 同色系强调字色。
- **默认单栏**；sidebar-creative 用侧栏双栏。
- **可扫描层级**：SectionHead 用发丝线；经历条目三段对齐；bullet 用 `•`。
- **量化成就**：经历 bullet 带数字结果，关键数字用强调样式。
