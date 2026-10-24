# 文件规范（.amlei-skill/resume/）

本文件是整个数据目录的唯一路径与落盘规范。`SKILL.md` 负责流程，[profile.md](profile.md)、[export.md](export.md)、[job-research.md](job-research.md) 负责各自内容；路径、命名、目录归属以本文件为准，其他 reference 不重复定义目录树。

## 目录结构

```text
~/.amlei-skill/resume/                  # 或 <项目>/.amlei-skill/resume/
├── questions.md                        # 跨会话 grill 问题与决策日志（只增不删）
├── profile.md                          # 已确认、跨方向稳定的短事实
├── avatar.png                          # 默认证件照
├── materials/                          # 跨方向、跨载体的证据池
│   ├── index.md                        # 来源台账
│   └── {material-id}/                  # 一份材料一个文件夹
│       ├── material.md                 # 材料正文（必需）
│       └── originals/                  # 原件（可选）
└── identities/
    └── {identity-id}/
        ├── target.json                 # 方向定义、求职偏好、目标公司
        ├── _meta.json                  # 当前版本元数据（可选）
        ├── 简历.md                     # 当前版本
        ├── avatar.png                  # 简历引用的证件照
        ├── files/                      # 当前方向复用附件
        ├── research/                   # jd.md / jd-{company}.md / 市场报告.md / 分析.md / 选材.md
        ├── review/                     # 分页检查截图 / 用户要求的分析 / 历史产物
        ├── export/                     # 自包含导出产物
        └── archive/                    # 旧版本快照（不复制 files/）
            └── {version}/
```

目录只表达“这是哪份材料/哪个方向”；材料类型、状态、敏感级别全部放在 `index.md` 的字段里，不用目录名分类。

## 每个位置放什么

| 位置 | 放什么 | 不放什么 |
|------|--------|----------|
| `questions.md` | 跨会话的 grill 问题、用户回答、决策、状态、影响与后续动作 | 长文材料、简历措辞、已删除问题的空缺 |
| `profile.md` | 已确认、跨方向稳定的短事实 | 长文、导出、逐条证据、未确认数字 |
| `materials/index.md` | 来源台账：ID、来源、日期、类型、状态、敏感级别 | 材料正文、长摘要 |
| `materials/{material-id}/material.md` | 可读、可检索的材料正文：摘录、链接、来源、版本、待确认 | 简历措辞、公开页面最终文案 |
| `materials/{material-id}/originals/` | 必须长期保存的原件：旧简历、签章 PDF、截图、设计稿、二进制 | 可以稳定引用的普通 URL/路径 |
| `identities/{identity-id}/target.json` | 方向定义与求职偏好 | 某次投递的临时信息 |
| `identities/{identity-id}/_meta.json` | 当前版本的时间与来源信息 | 简历正文 |
| `identities/{identity-id}/简历.md` | 当前方向的表达 | 未经确认的素材原文 |
| `identities/{identity-id}/files/` | 当前方向复用的附件 | 每次投递再复制一套 |
| `identities/{identity-id}/research/` | 当前方向的目标公司与选材摘要；多份 JD 用 `jd-{company}.md` | 主素材副本 |
| `identities/{identity-id}/review/` | 分页检查截图、用户要求的分析及历史产物 | 导出成品 |
| `identities/{identity-id}/export/` | 预览 HTML、PDF、长图、头像副本 | 可继续编辑的源文件 |
| `identities/{identity-id}/archive/{version}/` | 旧版本简历与结果 | `files/` 的复制品 |

`research/` 引用材料时用 `material-id#section`，不复制长原文。

## 命名

- `material-id`、`identity-id`、`version` 用英文小写 kebab-case，稳定、简短、可读。
- 一份材料一个文件夹：`materials/lixianglin/material.md`、`materials/workflow-skills/material.md`。
- 材料正文固定叫 `material.md`。
- 原件放对应材料的 `originals/`，保留原文件名；同一材料内重名时加日期或序号，不覆盖。
- 用户可见的产物可以保留中文名，如 `简历.md`、`市场报告.md`、`分析.md`。

## 材料接入

### 默认落盘

用户提供文章、工作记录、项目文档、笔记导出、仓库或作品链接时，先写入对应材料的 `material.md`，并在 `index.md` 登记来源、日期和状态。落盘是过程记录，不需要再问一次。

### 什么进材料池

- 用户自己的文章、复盘、作品记录、笔记导出、仓库、项目文档。
- 旧简历、作品集草稿等可复用证据。
- 用户作为可复用证据提供的自包含长叙述。

### 什么不进材料池

- JD、公司介绍、招聘页面 → 本次 `research/`。
- 一条已确认的短事实 → `profile.md`。
- 临时讨论、未授权保存的聊天细节 → 不落盘。
- 凭据、密钥、会话 Token、支付信息 → 永不落盘。

### 原件与转换

- 路径/URL 稳定时，只在 `index.md` 记录 `source_key` / `source_refs`，不复制原件。
- 原件会失效、版式/签章本身是证据、或需要长期回溯时，复制到 `materials/{material-id}/originals/`。
- 原始文件不写临时目录；转换中间产物可以放临时目录，完成后删除。
- `.docx` / `.pdf` / `.pptx` / `.xlsx` 用 markitdown 转成 Markdown，整理进 `material.md`；只有转换生成的 Markdown 不留在 `originals/`，原件仍按上面的规则保留。
- 代码、配置、数据、设计稿直接读源内容，不靠文件名或摘要猜测。
- 网页、仓库、目录要下钻读实际内容，不能只读 README、landing page 或目录列表。
- 转换失败时保留原件、向用户说明错误，并尝试其他读取方式；彻底读不出时在 `material.md` 标记「不可读」和已尝试的方法。
- 旧简历含照片时，用 `scripts/extract_avatar.py` 抽到 `avatar.png`；抽不到就留空，不瞎填路径。

## index.md 模板

索引只登记来源和状态，不复制正文。一个导出文件、一个仓库、一组同源链接各算一条材料，不按其中每一条 memo 拆行。

| 字段 | 取值 |
|------|------|
| `material_id` | 对应 `materials/{material-id}/` 的文件夹名 |
| `source_key` | 规范化后的路径/URL，用于去重 |
| `source_refs` | 其他载体、镜像、别名，可多个 |
| `type` | `article` / `note-export` / `work-record` / `repo` / `document` / `url-set` 等 |
| `captured_at` | 首次进入材料池的日期 |
| `extract` | `unread` / `partial` / `extracted` |
| `verification` | `unconfirmed` / `confirmed` / `conflict` |
| `lifecycle` | `active` / `stale` / `superseded` / `unavailable` |
| `sensitivity` | `public` / `private` / `third-party-confidential` / `secret` |
| `summary` | 100–200 字，写材料里有什么、已提炼到哪 |
| `identities` | 适用方向，如 `ai-pm`、`backend`；不绑定具体投递 |
| `review_after` | 可选复查日期，如 `2027-01`；只用于会变化的数字、版本或行情 |

示例：

| material_id | source_key | type | captured_at | extract | verification | lifecycle | sensitivity | summary | identities | review_after |
|-------------|------------|------|-------------|---------|--------------|-----------|-------------|---------|------------|--------------|
| `lixianglin` | `materials/lixianglin/material.md` | `work-record` | 2026-10-20 | `extracted` | `confirmed` | `active` | `private` | 教育、工作、项目与内容数据汇总；已提炼事实见 `profile.md` | `ai-pm` | — |

规则：

- 先成功写 `material.md`，再更新 `index.md`；不要并行写同一个索引。
- `summary` 只写短摘要和锚点，不复制完整提炼结果。
- 索引软上限约 200–300 行；超过后按主题分片，并在 `index.md` 保留分片入口。
- 历史经历不会自然过期；`stale` 只用于统计数字、版本、行情等会变化的信息。

## material.md 模板

```markdown
# {name} · 材料

> 这是证据池，不是简历文案。已确认的短事实见 `../../profile.md`。
> 来源与状态见 `../index.md`。敏感内容标 `[私密]`，不得自动用于公开输出。

## 来源与版本
- 来源：
- 获取日期：
- 内容哈希 / revision：

## 时间线

## 工作经历

## 项目

## 内容与作品

## 个人表达

## 待确认

## 索引锚点
```

章节标题保持稳定，便于按 `material-id#section` 只读一段。新内容默认追加到对应主题下；用户纠正、撤回或要求删除时直接改写，并记录 `replaces` / `superseded_by`。

## 去重与版本

- `source_key` 先规范化：去掉 URL 跟踪参数和末尾斜杠；只对 scheme/host 转小写，保留路径大小写；能取到内容时再记哈希。
- 同一来源只记一条；多个载体写进 `source_refs`，不重复追加正文。
- 同一 URL 内容更新时记 `revision`；路径变化用别名修复，不新建材料。
- 持续追加会让去重退化为 `O(N²)`；用规范化 key 和哈希映射，批量导入保持近似 `O(N+B)`。

## 隐私与删除

- `public`：可公开引用。
- `private`：个人隐私，留在本地；进入公开输出前逐次确认。
- `third-party-confidential`：客户、公司或第三人数据；只写安全摘要，原件保存前先问。
- `secret`：凭据、密钥、Token、支付信息；不落盘。
- 用户要求删除时，同时删除 `materials/{material-id}/`（含 `originals/`）、索引行、research 引用、导出副本和未经确认的派生副本；已提升进 `profile.md` 的事实逐条确认是否删除。

## 渐进读取

1. 会话开始读取 `questions.md` 与 `profile.md`；优先使用已确认结论，只对仍待确认且会影响本轮任务的问题追问。
2. 需要证据时先读 `materials/index.md`，按方向、状态、主题筛选。
3. 用 `rg` 定位 `material-id#section`，只读对应 `material.md` 的相关章节。
4. 不自动读取 `originals/`、整个笔记导出或全部工作记录。

## 问题集维护

- `questions.md` 是持续追问与决策记录，不是只用来保存问题的待办清单。
- 每次对话中形成的新问题或未确认事实，立即写入 `questions.md`；如果它会影响当前判断或简历表述，同时向用户提问。
- 问题应围绕具体判断或拟写入简历的表述展开，询问真实动作、范围、结果、数字口径、公开边界和反例；一次聚焦一个主题，答案模糊时继续追问。
- 会话开始时读取相关未解决问题并在对应当前任务时继续追问；不重复已确认事项，也不一次性倾倒全部历史问题。
- 每个问题使用稳定 ID，记录状态、类型、范围、问题、当前结论、影响、后续动作和来源。
- 已回答、已确认或已否决的问题默认不删除，只更新状态与结论；问题失效时标为「已失效」，并用 `superseded_by` 指向替代问题。
- 用户回答后立即更新原问题；形成取舍、边界或偏好时，在当前结论中明确记录决策。
- 用户没有回答时保持「待确认」，不得自行补成事实。
- 只有用户明确要求清除问题时才删除；执行前确认范围，并同步检查简历、画像与材料中的派生引用。

读取成本与材料总量 `S` 和索引行数 `N` 成正比；按来源建索引、按章节懒加载，避免把数百条记录一次性送入上下文。

## 导出与备份

- `identities/{identity-id}/export/` 必须自包含：把 `avatar.png` 复制进 `export/`，保证 `预览.html` 头像不断链。
- 简历和 `avatar.png` 本体留在 `identities/{identity-id}/` 根目录，导出目录只放派生文件。
- 覆盖 `简历.md` 前，把需要保留的旧版移入 `archive/{version}/`；`.bak.*` 只用于临时回滚，确认后清理，不长期留存。
- 导出流程见 [export.md](export.md)；本文件只规定路径。

## 迁移旧数据

- 迁移旧数据时，把 `_shared/` 与旧目录中的材料并入 `materials/`；新数据直接按本规范写入，不新建 `_shared/`。
- 旧的 `materials/{name}-material.md` 迁移为 `materials/{material-id}/material.md`，比较迁移前后的哈希与行数。
- 旧 `sources/` 迁移为 `materials/{material-id}/originals/`。
- 旧 `files/` 只作为兼容读取；可跨投递复用的材料迁入 `materials/`。
- 旧的 `identities/{identity-id}/resumes/{app-id}/`：最新版本提升到 `identities/{identity-id}/` 根目录，旧版本移到 `archive/{app-id}/`；`files/` 只保留一份，按哈希去重。
- 迁移后同步更新 `index.md` 的 `source_key` / `source_refs` 和 `profile.md` 的材料索引指针；删除旧路径前用 `rg` 确认没有残留引用。
- 发现重复原件时先生成 manifest 核对；合并或删除需要用户明确确认。

## 检查清单

- 没有把原始文件写进临时目录后忘记归档。
- 没有同一材料的多个正文副本。
- 没有把长原文复制进 `research/`。
- 没有把 `[私密]` 内容带进简历、作品集或导出。
- 没有把 `index.md` 当成正文使用。
- 没有在 `materials/` 下创建未登记的 `material.md`。
- 没有为同一个 identity 复制第二套 `files/`；旧版本只放 `archive/`，不复制附件。
