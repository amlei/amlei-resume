---
name: amlei-resume
description: 当用户需要写简历、改简历、投简历、换岗，或把简历导出为 A4 PDF 时使用。涵盖从就业市场调研、项目分析、素材挖掘、质量评估到装配 HTML 导出的完整流程，并在定稿后输出可直接用于招聘平台（Boss 直聘等）的求职招呼语。
---

# amlei-resume

**前置依赖**：使用本 SKILL 前，必须先加载 `amlei-profile` skill。amlei-profile 拥有事实层（`_shared/`：身份/经历/项目/能力），本 skill 只负责把它们渲染成具体方向的简历（强调层 + 快照层）。

amlei-resume 是**消费者**。一个用户可有多个职业身份（后端 / AI Agent / 全栈…），每个身份是基于同一份事实层的不同视角，对应 `identities/{identity-id}/` 目录。

核心原则：**不直接问"你要改哪"——通过聊项目、聊做事方式、聊自我认知，帮用户挖出他们自己都忘了的亮点，再落成简历文字。用户给的资料要带推理去读：从中发现角色越界、时间转折、规模暗示等疑点，转成问题去问，而不是照单全收（详见 [references/projects.md](references/projects.md)）。用户没提供的信息直接问，不猜测、不编造。**

**关键约束**：事实归 amlei-profile（事实层），framing 归 amlei-resume（强调层）。详细判别与流程见 amlei-profile 的 SKILL.md。本 skill 的所有 bullet 文案、技能归类、自述都是强调层产物，**不写回 `_shared/`**——只有挖到新客观事实时才回写（走 amlei-profile 的评估流程）。

## 输入

1. **身份信息**：从 amlei-profile 的 `_shared/identity.json` 取（姓名、性别、联系方式、教育）。首次使用时主动问；后续操作从 identity 读，不重复追问。**隐私数据（手机/邮箱/微信）必须问——用户不提供才 Mock 占位**（如 `<手机号>`、`<邮箱>`），由用户自行填入 `简历.md`。不要因为"隐私"而不问。
2. **目标方向**：本次写哪个身份的简历？已有身份（切换）还是新建（投影）？见 [references/identity-management.md](references/identity-management.md)。
3. **目标公司 / JD**：本次投递的具体目标（→ 该身份的 `target_companies[]` / 本次 resume 的 `jd.md`），用作投影打分和评估的镜子。
4. **事实素材（按需索取，不空等）**：聊到项目时主动要材料——
   - 项目资料文件（.docx / .pdf / .pptx / README / 设计稿等）
   - 项目地址（GitHub / 博客 / 飞书文档 / 作品集链接）
   - 工作经历的补充口述（公司 / 岗位 / 时间段 / 量化结果）

   **这些不是直接喂给简历的输入**，而是 amlei-profile 提取事实的原料：用户给 → 走 ingestion → 评估 agent + 用户确认 → 写入 `_shared/experiences.json` → 本 skill 再投影到 emphasis。流程见 amlei-profile 的 [references/ingestion.md](../../amlei-profile/references/ingestion.md) 与 [references/facts.md](../../amlei-profile/references/facts.md)。

   没材料时跟用户聊（按 [references/projects.md](references/projects.md) 的 STAR 框架），聊出的客观事实同样回写 amlei-profile。

## 工作流程

先用 Todo 列出所有步骤、预期产物和注意事项，逐条推进，完成一项标记一项。

**写/改简历：**

> 详细流程见 [references/write-revise.md](references/write-revise.md)。
> 换岗本质相同——投影出新的身份，基于已有事实 + 新岗位重新选材与 framing。

1. 收集就业市场信息（以 subagent 方式，输入岗位+城市 → 市场报告：该岗位需要的能力/技术/软硬技能概览）
2. 分析用户项目资料（以 subagent 方式 → 分析报告：做过什么、成果是什么。**回写 amlei-profile 事实层**）
3. ⏸️ **人工确认**：用户确认分析报告准确性
4. 讨论补充（Human-in-loop：围绕"想呈现怎样的自己"，聊能力/方向/思路/经历，不断补充细节）
5. 共创/迭代改写（逐节或整篇）
6. 润色（以 subagent 方式调用 amlei-text-polish skill）
7. 评估迭代（以 subagent 方式）→ 不通过回到 5
8. ⏸️ **人工确认**：评估通过后，展示评估结果，等用户确认后再保存
9. 用户确认保存 → 写入 `identities/{identity-id}/resumes/{app-id}/简历.md` + `_meta.json`
10. 导出（如需）
11. ⏸️ **求职招呼语**：简历定稿 / 导出后**不要直接结束**——输出 3–5 条不同方向的招呼语供用户复制到招聘平台（详见 [求职招呼语](#求职招呼语) 与 [references/greeting.md](references/greeting.md)）

**导出 PDF：**

1. 选主题
2. 读组件库
3. 装配 HTML
4. 审查 → 不通过回到 3
5. 套预览壳
6. 检查分页留白 → 不均回 3 调整
7. 交付（PDF）
8. 导出简历长图：调 `scripts/export_long_image.py <预览.html>`，返回 `<预览>_长图.png` 路径（用于招聘平台聊天框发送）

### 检查现有简历

检查 `identities/{identity-id}/resumes/{app-id}/简历.md` 是否存在：

- **存在** → 问用户基于当前版本需要做哪些调整；或基于此 fork 新版本（见 [references/snapshot-fork.md](references/snapshot-fork.md)）
- **不存在** → 从零开始。用户提供 .docx / .pdf 文件时走 amlei-profile 的[格式转换](#格式转换)

## 身份与快照管理

### 目录结构

```
~/.amlei-skill/resume/                  # 或 <项目>/.amlei-skill/resume/
├── _shared/                            ← amlei-profile 拥有（事实层）
└── identities/                         ← amlei-resume 拥有（强调层 + 快照）
    └── {identity-id}/
        ├── target.json                 # 方向定义 + 求职偏好 + 目标公司
        ├── emphasis/                   # 强调层（4 文件，按 fact 类型拆）
        │   ├── projects.json
        │   ├── experiences.json
        │   ├── capabilities.json
        │   └── narrative.json
        └── resumes/{app-id}/           # 一次具体投递的快照
            ├── 简历.md
            ├── _meta.json
            ├── jd.md
            └── materials.md
```

身份的创建/切换/删除、emphasis 维护、needs_review 处理详见 [references/identity-management.md](references/identity-management.md)。快照的 fork / fact diff / 不可变性详见 [references/snapshot-fork.md](references/snapshot-fork.md)。

**用户没说"可以/就这样"之前，绝不写入 `简历.md`。**

### 格式转换

用户提供的 `.docx` / `.pdf` 文件（旧简历、项目文档等），**走 amlei-profile 的 ingestion 流程**：

- 原始文件存档到 `_shared/files/`
- markitdown 转换结果同目录
- 抽取出的基础信息写入 `_shared/identity.json`
- 项目内容写入 `_shared/experiences.json` 的项目条目

转换后必做（**本 skill 负责**）：

1. **就地重排导出文件**：在 markitdown 导出的 `.md`（`_shared/files/` 里）上重排内容——按 `# self-intro` / `# 个人简介` / `# 专业技能` / `# 实习经历` / `# 项目经历` 等模块归类，原内容对号入座，不凭空重写、不漏。
2. **提取证件照**（旧简历含照片时必须做）：`python3 scripts/extract_avatar.py <原始文件> _shared/files/avatar.png`，抽到人脸就放进事实层 files 目录，并让 amlei-profile 写 `identity.json.avatar.ref`。
3. **渲染时引用**：写 `avatar: avatar.png` 到 self-intro；没照片则留空，不要瞎填路径。

### 简历格式

简历格式的硬规则：

| 元素 | 写法 |
|------|------|
| 首模块 | `# self-intro`（必须是第一个 `#`），下用 `key: value` 放 name / role / gender / location / phone / email / avatar / links 等。多值字段（links、education）用缩进子项：<br>`links:`<br>`- GitHub: url`<br>`education:`<br>`- 学校: xxx`<br>`- 专业: xxx` |
| 模块 | `# 模块名`（出现顺序 = 简历模块顺序） |
| 简介 | 模块下纯文本段 |
| 标签 | 模块下「标签, 标签」单行（研究兴趣 / 方向） |
| 经历 | `## 机构 \| 角色/方向`（无 `\|` 则只有机构名） |
| 项目经历标题 | `## 项目名 \| 公司(简称) \| 角色`（三段式，公司可省：`## 项目名 \| 角色`）。**公司一律用简称**（如「广州蚁群」而非「广州蚁群信息科技有限公司」）；简称取自 emphasis/experiences.json 的 `company_display`，没设则取 experience.company 的核心词 |
| 经历/项目日期 | `date: 2024.07 — 2025.03`（经历级用 experience.period；项目级用 project.period，没设则继承父经历） |
| 经历补充 | `meta: GPA 3.9/4.0 · 排名 1/60`（关键数字用 `**`） |
| 经历要点 | `- 成就（STAR + 量化）` |
| 技能 | `- 类别: 值` 或 `类别: A · B · C`。类别须按专业领域拆分（如 AI/Agent、编程语言、框架、数据存储、工程化各独立一类），不能跨域混放 |

`name:` 必填；`avatar:` 给照片相对路径；`links` 放可线上展示自己的链接，如个人博客、飞书文档、作品集等（key: value）。完整范例：[sample-resume.md](assets/sample-resume.md)。

## 质量保障

### 润色

共创/改写完成后，**必须以 subagent 方式调用 amlei-text-polish skill 执行润色**——不要自己随手改。把 `简历.md` 交给 amlei-text-polish（输入：文件路径 + 润色目标，如“更简洁有力、量化突出”），由它逐行优化语言表达、修正语法、强化用词、消除冗余，在不改变原意的前提下让文字更清晰有力。

### 简历评估

润色完成后，**必须以 subagent 方式执行** [references/resume-evaluator.md](references/resume-evaluator.md) 的 6 维度评估流程，根据结果迭代修改直到所有维度通过。评估报告写入 `identities/{identity-id}/resumes/{app-id}/评估.md`。

**⏸️ 人工确认**：评估通过后，展示评估报告，等用户确认后才保存简历并进入导出。

### 易错点

- **残留 `{{占位符}}`**：组件模板占位符必须全替换。
- **`# self-intro` 必须是首个 `#`**，渲染成 Header 而非 SectionHead。
- **`data-stick="1"` 别漏**：SectionHead 必带。
- **联系方式按实际字段拼**：没有的字段连同分隔符一起删。
- **`avatar:` 有就 `<img>`**：没照片用 icons.md 占位 SVG。
- **整篇只用所选主题的组件**，不从别的主题借。
- **标题层级只用 `#`/`##`**。
- **公司项目别全塞进实习 bullet**：公司项目要有独立的 `# 项目经历` 条目（公司项目在前、个人项目在后）；实习经历只放基本盘（总体职责 + 协调 / 运维）+ 1-2 高光，核心技术攻坚（带量化与闭环）抽成公司项目单独立项，避免内容重复又无重点。
- **导入旧简历别漏证件照**：用 `extract_avatar.py` 抽出 `avatar.png` 放进简历目录，并在 self-intro 写 `avatar: avatar.png`；漏了简历就没头像。
- **技能区写"能力"不写"工具"**：技能点列的是可迁移的能力/范式（Agent Loop/ReAct、推理服务部署、OCR 选型与调度、全栈落地…），不是工具名（LangChain、Docker、Playwright、Redis、Shadcn UI…）。工具是"用过"不是"会"——照文档就能跑起来的东西当技能点，既是评估环节的"背单词"反模式，也容易被面试官一句"这个具体怎么用"问翻。工具名作为**证据**下沉到项目 bullet 里（在真实业务语境中比堆 chip 更有说服力，ATS 关键词照样能命中）。判断标准：写每条技能前先问"这是能力还是工具名？"——是工具就移到项目里，技能区只留能力。语言（Go/Python…）可作技能维度，但框架/中间体/CLI（FastAPI、ent、K3s、Playwright…）一律不算技能。

## 预览与导出

用户要求导出 PDF 时执行。详细流程见 [references/export.md](references/export.md)。

## 求职招呼语

简历定稿 / 导出后**不要直接结束**——按 [references/greeting.md](references/greeting.md) 生成 **3–5 条不同方向的招呼语**（默认含「务实匹配 + 成果数字」两型），让用户挑一条复制到招聘平台，建议配导出阶段生成的简历长图一起发。招呼语写法、方向模板、输出结构、自检清单、发送时机与薪资策略见 greeting.md。

## 添加新主题

新主题可直接编写或从参考简历 HTML 转换（规范见 [references/themes/theme-index.md](references/themes/theme-index.md) 末尾）。写完用 `assets/sample-resume.md` 渲染 → 校验 → 套壳 → 浏览器打开预览核对，确认后登记到 theme-index。

## 脚本

`python3 scripts/resume_cli.py --help`。**统一入口**——三层模型的所有 CRUD 都走它：

- **事实层**（转给 amlei-profile/scripts/profile.py）：`identity` / `experience` / `project` / `capability` / `find` / `batch` / `propagate` / `time`
- **强调层**（本 skill 直接维护）：`identities` / `new-identity` / `rm-identity` / `select` / `unselect` / `set-framing` / `exclude` / `set-headline` / `order` / `skill-axis` / `set-narrative`
- **快照层**：`new-snapshot` / `fork` / `deliver` / `clear-review` / `snapshots`

每次写入自动时间戳备份（保留最近 10 份）；事实层写入触发 schema 校验（id 格式 / proven_by 非空 / 引用存在）；事实层更新后调 `propagate <fact_id>` 把下游 emphasis + snapshots 的 `needs_review` 翻位（不改文案）。fork 时基于 `needs_review` + 版本戳检测 fact diff，提示用户但不自动应用。
