# 事实层维护（facts）

`_shared/` 是用户跨会话的**唯一长期真相源**。简历、portfolio、面试准备都消费它。本文件定义事实层的读写、评估、传播流程。

## 两条铁律

- **读取记忆**：每次进入 skill 先读 `_shared/` 的相关文件，基于已有事实工作，不重复追问已记录的信息。
- **回写记忆（强制，最易遗漏）**：本次任务中挖到的任何新事实（来自用户口述、项目资料分析、链接探索、改简历时浮现的细节），都必须评估 + 用户确认后写回。**只写进任务局部的 materials.md / 分析.md 不算数**——下次会话你只会读 `_shared/`。

## 四类事实

### identity.json（身份事实）

姓名、性别、联系方式、**常驻地**（city_base，事实）、社交链接、avatar 引用、教育背景。1:1 与用户，跨所有身份共享。`profile.city` 的歧义在本 schema 中消解——常驻城市在 identity，投递目标城市在 amlei-resume 的 `target.json.preferences.city`。

### experiences.json（经历事实，树形）

数组 `items[]`，每条经历下嵌套 `projects[]`。每条经历字段：`id` / `company` / `position` / `period` / `industry` / `team_context` / `projects` / `cross_project_refs` / `source_refs`。

**树形规则**：项目物理住在"主经历"下。若某项目跨多个经历（实习开始 + 转正延续），其他经历通过 `cross_project_refs: ["prj_xxx"]` 引用 id，不重复嵌套。

**项目字段**：`id` / `name` / `my_role` / `tech_stack[]` / `outcome_metrics{}`（键值对量化）/ `granularity[]`（多粒度，见下）/ `source_refs[]`。

**granularity 多粒度**：每个 project 存多档客观描述：
```json
"granularity": [
  { "grain": "project",   "text": "为字节算法服务设计 OCR 多模型调度..." },
  { "grain": "milestone", "text": "基于 etcd 实现故障转移，P99 从 800ms 降到 200ms" },
  { "grain": "technique", "text": "Redis ZSET 加权轮询，etcd watch 触发降级" }
]
```
`text` 是中性客观描述，**不是简历 bullet**——不嵌 JD 关键词、不加修辞。简历 bullet 在 amlei-resume 的 emphasis 层重写，引用 `source_grain_index`。

### capabilities.json（能力证明，独立）

数组 `items[]`，每条：`id` / `claim`（能力声明，中粒度）/ `proven_by[]`（**至少一个 project id，必填**）/ `evidence_grain`（证据所在档位）。

**强制规则**：`proven_by` 不能为空。空数组在 schema 层即被拒绝。无证据的能力 claim 是强调层产物，写进 amlei-resume 的 `emphasis/capabilities.json.skill_axis`，不进事实层。

**为什么独立而非内嵌进 projects**：能力是跨项目抽象——"并发系统设计"可能由 3 个不同项目共同证明。内嵌进任何一个 project 都不对称。`proven_by` 是多对多关系。

### files/（原始素材存档）

用户提供的所有原始文件永久存档于此。详细流程见 [ingestion.md](ingestion.md)。

## 写入流程

### 直接写入（绕过评估）

markitdown 从 docx/pdf 提取的**基础信息**（姓名、电话、邮箱、教育、性别）可直接写入 `identity.json`——这是从用户已有材料机械提取，不需评估。

### 评估 + 确认后写入

其余所有"挖出来的"事实——分析项目资料发现的能力、聊出的成果、链接探索后的发现——**必须**走评估 agent：

1. 起一个**独立上下文**的评估 agent（具体调用哪个工具由 LLM 选，目的是拿到不带自评偏袒的独立判断）
2. 评估标准见 [fact-evaluator.md](fact-evaluator.md)
3. **评估通过且用户确认**后，才调 `profile.py` 写入
4. 不通过就告诉用户为什么不记

> 脚本写入前会自动备份（带时间戳，保留最近 10 份）。

## 读取流程

每次进入 amlei-profile 操作前：

1. `python3 scripts/profile.py path` 确认事实层位置；不存在则 `init` 创建
2. 读 `identity.json` 全量（小文件）
3. 按需读 `experiences.json` / `capabilities.json`（评估某能力时读 capabilities；讨论某项目时读 experiences）
4. 基于已有事实工作，不重复追问

## 事实更新与传播（R4）

当事实层某条记录被 update（如修正 metric、补充 granularity、补 proven_by）：

1. `_meta.facts_version` 时间戳更新到当前
2. 调用 `profile.py propagate <fact_id>`，扫描 `identities/*/emphasis/*.json` 中引用该 fact 的条目，翻 `_meta.needs_review = true`
3. 同步扫描 `identities/*/resumes/*/_meta.json`，翻 `needs_review = true`
4. **不改任何 bullet 文案、不改任何已交付的简历.md**

下次用户打开某身份，系统提示"底层事实变了，要看吗"，由用户决定是否更新对应 emphasis 条目。用户审阅后即使决定不改文案，也可手动清 `needs_review` 并更新 `_meta.facts_version_at_last_sync` 到当前。

## 与 amlei-resume 的协作

- amlei-resume 在创建新身份时调本 skill 做"投影"——读所有事实，按 target JD 打分，生成 emphasis 雏形
- amlei-resume 的 emphasis 文件通过 `fact_id` 引用本 skill 的事实
- 本 skill 不知道 amlei-resume 的存在——单向被消费
- 本 skill 改 schema 时，amlei-resume 的引用可能断裂；同 repo 同步发布可避免

## 永不写入事实层的情况

| 情况 | 为什么 | 该写哪 |
|------|------|------|
| 用户的目标岗位、求职偏好、目标公司 | 是强调（per-identity） | amlei-resume 的 `target.json` |
| 简历 bullet 文案、自我介绍、技能标签归类 | 是强调（per-identity） | amlei-resume 的 `emphasis/*.json` |
| 评估报告、市场调研、JD | 任务局部产物 | 任务局部文件 |
| 无证据的能力 claim | 不满足事实层规则 R1 | amlei-resume 的 `emphasis/capabilities.json.skill_axis` |
| 一次性细节（"那次开会具体讲了啥"） | 无长期复用价值 | materials.md（任务局部） |
