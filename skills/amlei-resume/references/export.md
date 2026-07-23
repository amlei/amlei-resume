# 预览与导出

用户要求导出 PDF 时执行。装配 HTML，套预览壳导出。

## 产物目录

所有产物归集到 `resume/{姓名}/{求职岗位}/`——相对引用不会断、换岗位/换照片互不干扰。

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

1. `# self-intro` → **Header** 组件（name/role/education/contact/photo；不渲染成 SectionHead）。`education:` 字段单独一行 `.edu-line`，子项用 ` · ` 拼接（如「学校 · 专业 · 学历 · 届」），不在 contact 行混排。
2. 每个 `# 模块` → **SectionHead**（icon 按 icons.md 选，`data-stick="1"` 必带）+ 模块正文组件。
3. `## 机构 | 角色` → **Entry**（加 `data-stick="1"`，防末尾孤立）；
   `- bullet` → 每条拆成独立 **Bullet** 原子（不再包在 Entry 内）。
   `##` 下的描述段（项目说明文字）→ `<p class="desc">` **放在 Entry 内**（与 header 同原子），不单独置于外部。
4. 行内强调：`**词**` → 强调字色；关键数字 → 等宽强调（如 `<span class="num">`）。

产物 = `<style>…</style>` + 各原子，**不要**包 `<!DOCTYPE>/<html>/<head>/<body>`（预览壳负责）。

## 装配后审查

读取产物 HTML 和 `简历.md`，逐模块对比结构、模块标题、bullet 内容，确认无遗漏、无顺序错乱。发现缺失回「装配 HTML」修复，通过才走下一步。

## 套预览壳

用 `scripts/wrap_preview.py`（`--help` 看参数）。产出 `resume/{姓名}/{求职岗位}/预览.html`（自动建目录，带「导出 PDF」工具条 + A4 自动分页），`document.title` = `姓名-岗位`（=「另存为 PDF」默认文件名）；用 `--name` 覆盖。

**预览后检查**：

1. **打开浏览器预览页**（可用 Playwright 自动化检查）。
2. **确认 bullet 已原子化**：`#source` 里每一条 `- bullet` 是独立 `.bullet` 原子，而非包在 `<ul>` 内。若未拆分，先拆再继续。
3. **检查页数**：Playwright 统计 `#scaler .page` 个数和每页填充率。参考标准：
   - 应届/初级：≤ 2 页
   - 有经验/资深：≤ 3 页
4. **检查末页填充率**：
   - ≥ 50% → 合理
   - 30–50% → 可接受
   - < 30% → 精简 bullet 内容重装（不调 spacing）
5. **检查行尾空白**（逐条 bullet 扫描）：单行 bullet `getClientRects()` 填充率 < 55% 视为过短，合并相邻短 bullet 或补全内容后重装。

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
