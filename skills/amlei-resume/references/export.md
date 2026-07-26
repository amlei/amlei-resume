# 预览与导出

用户要求导出 PDF 时执行。装配 HTML，套预览壳导出。

## 产物目录

所有产物归集到 `identities/{identity-id}/resumes/{app-id}/`——相对引用不会断、换身份/换照片互不干扰。

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
2. 每个 `# 模块` → **SectionHead**（icon 按 icons.md 选）+ 模块正文组件。
3. `## 机构 | 角色` → **Entry**（只含 header：org/proj/company/role/date/meta）；
   `- bullet` → 每条拆成独立 **Bullet** 原子（兄弟节点，不再包在 Entry 内）。
   `##` 下的描述段（项目说明）→ 渲染成主题的描述段落组件（academic 用 `.summary`，部分主题有 `.desc`），**作为独立原子放在 Entry 之后**，不塞进 Entry。
4. 行内强调：`**词**` → 强调字色；关键数字 → 等宽强调（如 `<span class="num">`）。

> **不要再加 `data-stick="1"`**——旧版手动分页用它防"标题孤立页底"，新版由预览壳的 CSS `break-*` 规则按 class（`.sec-head`/`.entry`）自动处理，加了也是 no-op。主题模板里若仍带着，照抄无害、不强制。

产物 = `<style>…</style>` + 各原子，**不要**包 `<!DOCTYPE>/<html>/<head>/<body>`（预览壳负责），也**不要**外层包 `.resume-root`（`wrap_preview.py` 会自动包）。

## 装配后审查

读取产物 HTML 和 `简历.md`，逐模块对比结构、模块标题、bullet 内容，确认无遗漏、无顺序错乱。发现缺失回「装配 HTML」修复，通过才走下一步。

## 套预览壳

用 `scripts/wrap_preview.py`（`--help` 看参数）。产出 `identities/{identity-id}/resumes/{app-id}/预览.html`（自动建目录），`document.title` = `姓名-岗位`（=「另存为 PDF」默认文件名）；用 `--name` 覆盖。

外壳（[assets/preview-shell.html](../assets/preview-shell.html)）做的事：
- **Paged.js 行级分页**（vendor 在 `assets/vendor/paged.polyfill.js`，`wrap_preview.py` 默认内联进产物，使预览页自包含 / 离线可用；`--no-inline-js` 改相对引用，仓库内参考 sample 用）。
- 主题 `<style>` 注入被 Paged.js 处理的 `<style>` 槽（`@page{size:A4;margin:14mm 16mm 13mm}` + 分页规则 + 主题 CSS）。
- chrome（工具条 / 舞台 / 页间距 / 打印开关）放 `<style data-pagedjs-ignore>` 绕过 polisher，由浏览器直套——Paged.js 会剥掉针对 `.pagedjs_*` 的用户规则，故页间距等必须放这段。

> **核心：分页交给 Paged.js，不要手动量高度装箱。** Paged.js 在行级断行——长段落 / bullet 可跨页，每页填到页脚，不再有"整条 bullet 被搬页留 10 行白"的旧问题。`.sec-head`/`.entry`/`.bullet` 等小单元由外壳的 `break-inside:avoid` 保持不拆，`.summary` 等长文不设 avoid 以便跨页。

**预览后检查**（可用 Playwright 自动化）：

1. **打开浏览器预览页**，等工具条右上角显示「共 N 页」（`document.getElementById('rvInfo')`）——这是 Paged.js 分页完成的信号。
2. **确认 bullet 已原子化**：`#source` 里每条 `- bullet` 是独立 `.bullet` 兄弟节点，而非包在 `<ul>`/Entry 内。若未拆分，先拆再继续。
3. **检查页数**：统计 `.pagedjs_sheet` 个数。参考标准：
   - 应届/初级：≤ 2 页
   - 有经验/资深：≤ 3 页
4. **检查末页填充**：Paged.js 会把每页填满（无需手动调 spacing）。末页若 < 30% 才考虑精简 bullet 内容重装——分页本身已无留白问题。
5. **确认无重复源**：`#source` 在分页后应 `display:none`，页面下方不应出现第二份未分页副本（外壳已处理）。

参考产物：[sample-preview.html](../assets/sample-preview.html)（academic 主题渲染 sample-resume.md）、[sample-body.html](../assets/sample-body.html)（装配后 body 样例）。

> 预览页自带「✏️ 编辑」按钮（草稿视图改文字 + 完成后重排、「📝 导出 Markdown」回写 `.md`）——这是预览壳的 UI 能力，用户在页面上直接用，无需在这里记流程。

## 配色方案

预览页工具条「配色」下拉：8 套点缀色（墨蓝 / 工程蓝 / 森林绿 / 酒红 / 藏青 / 紫 / 琥珀 / 石墨黑）+「主题原色」。选择记在 localStorage，「导出 PDF」沿用——同一份简历可出多套配色。

## A4 与 PDF 导出

- Paged.js 把内容流式排进 A4 内容区，生成离散 `.pagedjs_page`（每页严格 A4）。
- 「导出 PDF」走浏览器原生打印：工具条自动隐藏、页间距清零，每个 `.pagedjs_page` 1:1 对应一个 PDF 页（外壳在渲染后追加 `@page{margin:0}` 覆盖，避免浏览器再叠 margin 导致翻倍分页）。**屏幕预览 = 打印输出**。

## 简历长图

PDF 导出后，再导出一张简历长图，用于招聘平台（Boss / 拉勾 / 智联 / 前程无忧）聊天框发送——图片比 PDF 少一次「点击下载」，首轮即可发，HR 可直接滑着看完，常与求职招呼语一起发出。

- 调 `scripts/export_long_image.py <预览.html>`，返回 `<预览>_长图.png` 路径。
- 脚本默认截 `.pagedjs_sheet`（每个 A4 页），截图前自动藏掉工具条（否则 sticky 工具条像素会盖进第 1 页顶部），等「共 N 页」出现再逐页截图纵向拼接。
- 同时保留 A4 PDF（正式投递 / 邮件用），两份并行交付。

## 视觉红线

- **不做报刊排版**：无首字下沉、无报头巨标题；姓名 ≈24–26px。
- **单点缀色**：一个 `--accent` + 同色系强调字色。
- **默认单栏**；sidebar-creative 用侧栏双栏。
- **可扫描层级**：SectionHead 用发丝线；经历条目三段对齐；bullet 用 `•`。
- **量化成就**：经历 bullet 带数字结果，关键数字用强调样式。
