---
name: amlei-resume
description: 简历全流程：和用户一起 0→1 写/改局部/换岗位重定向/迭代，再选主题装配 HTML 导出 PDF 打印。触发：写简历/设计简历/改简历/投简历/简历排版/简历导出 PDF/resume。
argument-hint: "[求职岗位] [意向城市] [工作年限]"
---

# amlei-resume

和用户一起写、改、迭代简历内容，再装配 HTML 导出 PDF。**个人资料**是素材库（多查、写入谨慎）；**简历**是工作产物（项目级持久化、可反复改）。

核心原则：**不直接问"你要改哪"——通过聊项目、聊做事方式、聊自我认知，帮用户挖出他们自己都忘了的亮点，再落成简历文字。**

**JD 调研（通用）**：让用户给出想去的公司/部门/招聘JD，基于JD联网搜索岗位能力需求、候选人画像。JD原文立即落盘到 `resume/{姓名}/{求职岗位}/jd.md`，写入后禁止修改——防止对话长后出现幻觉。写/改前都先做这一步，摸清"对方要什么人"。

## 能力

- **写（0→1）**：从零跟用户一起写目标岗位简历。详见 [references/write-resume.md](references/write-resume.md)。
- **改**：通过聊经历、项目故事来激发补充、挖掘沉默亮点。详见 [references/revise-resume.md](references/revise-resume.md)。
- **资料联动**：个人资料一更新，**主动**告诉用户「要不要把它补进 X 岗位简历」——确认才动。
- **联网索迹**：根据JD联网搜索岗位能力需求、候选人画像、隐性要求——先摸清"对方要什么人"。
- **导出**：用户要求导出时，校验格式 → 选主题 → 装配 HTML → 导出 PDF。

## 简历存储

简历是普通 Markdown，持久化在项目级，**不进根目录、不用脚本**——直接读写：

```
resume/{姓名}/{求职岗位}/简历.md
```

改简历就读这份；换岗就开新的 `{求职岗位}/` 目录存新版（原岗版本保留）。

## 个人资料

详见 [references/profile.md](references/profile.md)。

## 简历格式

校验脚本会查的硬规则：

| 元素 | 写法 |
|------|------|
| 首模块 | `# self-intro`（必须是第一个 `#`），下用 `key: value` 放 name / role / gender / location / phone / email / avatar / links 等 |
| 模块 | `# 模块名`（出现顺序 = 简历模块顺序） |
| 简介 | 模块下纯文本段 |
| 标签 | 模块下「标签, 标签」单行（研究兴趣 / 方向） |
| 经历 | `## 机构 \| 角色/方向`（无 `\|` 则只有机构名） |
| 经历日期 | `date: 2024.07 — 2025.03` |
| 经历补充 | `meta: GPA 3.9/4.0 · 排名 1/60`（关键数字用 `**`） |
| 经历要点 | `- 成就（STAR + 量化）` |
| 技能 | `- 类别: 值` 或 `类别: A · B · C` |

`name:` 必填；`avatar:` 给照片相对路径；`links` 用于 Github、博客等额外链接（key: value）。完整范例：[sample-resume.md](assets/sample-resume.md)。

## 源文档 → 简历素材

用户给 `.docx` / `.pdf` 旧简历：转成纯文本 → 重排成上面格式 → 写到 `resume/{姓名}/{求职岗位}/简历.md`（自动建目录）。证件照用 `scripts/extract_avatar.py` 抽取放进同目录，MD 用 `avatar:` 引用。若要写入个人资料走「评估 + 确认」。

## 预览与导出

用户要求导出 PDF 时执行。先校验格式，再装配 HTML。

### 校验

用 `scripts/validate_resume.py <简历.md>` 校验，ERROR 清零才算通过。校验不过不往下走。校验项：self-intro 首模块 / name 必填 / 标题层级 / 空模块 / date 格式。

### 选主题

读 [theme-index.md](references/theme-index.md)，据目标岗位 / 行业推荐最契合的主题：
- 用户已指定主题 → 直接用。
- 岗位有明确契合 → 推荐 + 1~2 个备选让用户选。
- 无明显倾向 → 默认 `academic`。
- `sidebar-creative` 是双栏单页，内容多不要选。

### 读组件库

读所选主题的 `references/theme-{标识}.md` + 共用的 [icons.md](references/icons.md)（按模块语义选 SVG 图标）。**装配 HTML 一律从所选主题的组件库取，不凭记忆手写。**

### 装配 HTML

按主题库的简历骨架装配：主题 `<style>`（整段照抄）放最前，再依次：

1. `# self-intro` → **Header** 组件（name/role/contact/photo；不渲染成 SectionHead）。
2. 每个 `# 模块` → **SectionHead**（icon 按 icons.md 选，`data-stick="1"` 必带）+ 模块正文组件。
3. `## 机构 | 角色` → **Entry**；其下 `date:` / `meta:` / `- bullets` 收进同一个 Entry。
4. 行内强调：`**词**` → 强调字色；关键数字 → 等宽强调（如 `<span class="num">`）。

产物 = `<style>…</style>` + 各原子，**不要**包 `<!DOCTYPE>/<html>/<head>/<body>`（预览壳负责）。

### 套预览壳

用 `scripts/wrap_preview.py`（`--help` 看参数）。产出 `resume/{姓名}/{求职岗位}/预览.html`（自动建目录，带「导出 PDF」工具条 + A4 自动分页），`document.title` = `姓名-岗位`（=「另存为 PDF」默认文件名）；用 `--name` 覆盖。

### 交付

打开 `resume/{姓名}/{求职岗位}/预览.html` →「导出 PDF」→ 浏览器选「另存为 PDF」即得 A4 简历。换主题：回「选主题」重选，重新装配 + 校验 + 套壳。

参考产物：[sample-preview.html](assets/sample-preview.html)（academic 主题渲染 sample-resume.md）。

## 产物目录

所有产物归集到 `resume/{姓名}/{求职岗位}/`——相对引用不会断、换岗位/换照片互不干扰。

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

## 易错点

- **残留 `{{占位符}}`**：组件模板占位符必须全替换（校验兜底）。
- **`# self-intro` 必须是首个 `#`**，渲染成 Header 而非 SectionHead。
- **`data-stick="1"` 别漏**：SectionHead 必带。
- **联系方式按实际字段拼**：没有的字段连同分隔符一起删。
- **`avatar:` 有就 `<img>`**：没照片用 icons.md 占位 SVG。
- **整篇只用所选主题的组件**，不从别的主题借。
- **标题层级只用 `#`/`##`**。

## 添加新主题

新主题可直接编写或从参考简历 HTML 转换（规范见 [theme-index.md](references/theme-index.md) 末尾）。写完用 `assets/sample-resume.md` 渲染 → 校验 → 套壳 → 浏览器打开预览核对，确认后登记到 theme-index。
