---
name: amlei-profile
description: 用户的个人能力记忆——跨会话认识用户的长期事实档案。管理身份/经历/项目（多粒度）/能力证明（带证据）四类事实，独立于任何具体求职方向存在。当用户需要"记住我做过 X""更新我的资料""我有哪些能力""提取简历里的信息""分析这个项目然后记下来"时使用。简历、portfolio、面试准备等都消费这份事实层。
---

# amlei-profile

事实层（`_shared/`）是你跨会话认识用户的**唯一长期真相源**。简历只是它的消费者之一——portfolio、面试准备、个人作品集都会读它。

**核心判别：事实 vs 强调**

每收到一条用户信息，问一个问题：**"用户在两次不同方向的面试里，会对这件事讲不同的故事吗？"**

- **不会，它就是那样发生的** → **事实**（写入 `_shared/`，本 skill 拥有）
- **会** → **强调**（写入 `identities/{id}/emphasis/`，amlei-resume 拥有）

举例：在字节做过 OCR 调度、用了 Go+Redis+K8s、P99 从 800ms 降到 200ms——这些**不会变**，是事实。但"为主导高并发后端设计"vs"为将 OCR 抽象为 Agent 可编排能力"——同一事实的两种讲法，是强调。

**使用本 SKILL 时必须先加载**：
- [references/facts.md](references/facts.md)（事实层维护流程：读取/写入/评估/传播）
- [references/ingestion.md](references/ingestion.md)（原始素材提取流程）
- [references/fact-evaluator.md](references/fact-evaluator.md)（评估 agent：判断"值不值得进事实层"）

amlei-resume 是消费者——它通过 `identities/{id}/emphasis/` 引用本 skill 的事实。加载顺序：先 amlei-profile，再 amlei-resume。

## 数据布局

```
~/.amlei-skill/resume/                # 或 <项目>/.amlei-skill/resume/
├── _shared/                          ← 本 skill 拥有（事实层）
│   ├── identity.json                 # 身份事实（1:1，姓名/联系方式/教育等）
│   ├── experiences.json              # 经历事实（树形：经历→项目）
│   ├── capabilities.json             # 能力证明（带 proven_by 引用）
│   └── files/                        # 原始素材存档（docx/pdf/转换md）
└── identities/                       ← amlei-resume 拥有（强调层 + 快照）
    └── {identity-id}/
        ├── target.json
        ├── emphasis/
        └── resumes/
```

事实层的 4 个文件 + 它们的 schema 见 `assets/schemas/`。每文件 `_meta.facts_version`（ISO 8601 时间戳）随每次写入更新；schema_version 当前为 2。

## 事实的四类

| 类 | 文件 | 关键约束 |
|---|---|---|
| 身份事实 | `identity.json` | 1:1 与用户。姓名/性别/联系方式/常驻地/链接/avatar/教育 |
| 经历事实 | `experiences.json` | 树形：每个经历内嵌 projects。项目 id 全局唯一；跨经历项目用 `cross_project_refs` |
| 能力证明 | `capabilities.json` | **每条必须有 `proven_by` 至少一个 project id**——无证据的能力不下沉到事实层 |
| 原始素材 | `files/` | docx/pdf/pptx 等永久存档；markitdown 转换结果同目录 |

## 关键规则

### R1：能力必须有证据

`capabilities.json` 每条 `proven_by` 不能为空。LLM 提出能力 claim 时必须同时给出"由哪个项目证明"。无法举证的 claim 是强调层产物（写进 emphasis/capabilities.json 的 skill_axis），不是事实。

### R2：项目存储多粒度

每个 project 在 `granularity[]` 数组里存多档客观描述（project / milestone / technique / module / version），text 是**中性描述**，不是简历 bullet。简历 bullet 在 amlei-resume 的 `emphasis/projects.json` 重写，可自由嵌关键词、调语序。事实层只保证"发生过、客观、可验证"。

### R3：写入前评估（除直接提取外）

从项目资料分析、链接探索、对话挖出的"新事实"——**必须派独立评估 agent 判断"值不值得进事实层"**（独立上下文，避免自评偏袒），通过 + 用户确认后才写。从 markitdown 直接提取的姓名/电话等基础信息可绕过评估。流程见 [references/fact-evaluator.md](references/fact-evaluator.md)。

### R4：事实更新只标 needs_review，不改下游文案

事实层更新（如某项目 metric 改了）→ 扫描所有 `identities/*/emphasis/*.json` 和 `identities/*/resumes/*/_meta.json` 中引用该 fact 的条目 → 翻 `needs_review: true`。**永不自动改 bullet 文案**——文案是用户精心措辞的产物。下次用户打开该身份时提示"底层事实变了，要看吗"，由用户决定吸收与否。

### R5：透明维护

用户**不直接编辑 JSON**。所有事实维护通过自然语言交互：聊到新东西 → 评估 + 确认 → 写入；事实变了 → 提示用户。用户感知是"我聊着聊着，它就记住我了"。脚本（`scripts/profile.py`）是后端工具，不是用户界面。

## 触发写入 fact 层的时机

| 场景 | 行为 |
|------|------|
| markitdown 提取的基础信息（姓名/电话/教育） | 直接写入（绕过评估） |
| **分析项目资料/链接/文档后发现的能力与成果** | 评估 agent + 用户确认后写入（**最常被遗漏**） |
| 聊出可跨方向复用的事实 | 评估 agent + 用户确认后写入 |
| 用户主动"帮我记一下" | 评估 agent + 用户确认后写入 |
| 事实层已有条目的字段需要修正 | 直接 update（脚本自动备份） |

## 脚本

`python3 scripts/profile.py --help`。子命令按 4 个事实文件组织：`identity` / `experience` / `project` / `capability` / `find` / `batch` / `path` / `init`。位置优先项目级、否则用户根目录（同旧版）。每次写入自动时间戳备份。
