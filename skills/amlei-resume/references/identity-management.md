# 身份管理（identity）

amlei-resume 是 amlei-profile 的**消费者**。一个用户可有多个职业身份（如后端、AI Agent、全栈），每个身份是基于同一份事实层 `_shared/` 的不同视角，对应 `identities/{identity-id}/` 目录。

本文件定义身份的创建、切换、删除，以及强调层（emphasis）的维护。

## 身份目录结构

```
identities/{identity-id}/
├── target.json               # 方向定义 + 求职偏好 + 目标公司
├── emphasis/                 # 强调层（4 文件，按 fact 类型拆）
│   ├── projects.json         # 选中 + framing（bullet 重写）
│   ├── experiences.json      # 选中 + 排序 + headline
│   ├── capabilities.json     # 选中 + skill_axis 归类
│   └── narrative.json        # 自述 / self-intro
└── resumes/
    └── {app-id}/             # 一次具体投递的快照（不可变）
        ├── 简历.md
        ├── _meta.json
        ├── jd.md
        └── materials.md
```

## 创建新身份（投影，非复制）

**关键**：新身份不是从已有身份复制，而是从 `_shared/` 事实层**投影**。

流程：

1. **读事实层**：`_shared/experiences.json` + `_shared/capabilities.json` + `_shared/identity.json`
2. **打分**：对每个 project、experience、capability，按 `target.target_role_tags` 与 JD 的相关性打分
3. **生成雏形**：
   - `emphasis/projects.json`：选 top-K 项目（默认 5-8 个），每个项目初版 framing 用 fact 层 `granularity[milestone]` 的 text 作为 bullet 起步（用户可后续重写）
   - `emphasis/experiences.json`：所有经历选中（个人经历 + 公司经历）
   - `emphasis/capabilities.json`：相关 capability 选中，按方向归类到 skill_axis
   - `emphasis/narrative.json`：根据方向起草 pitch
   - `excluded[]`：记录未选项目 + 原因
4. **⏸ 用户确认**：展示雏形，用户调整选材、重写 framing、改 narrative
5. **写入**：`identities/{slug}/target.json` + `emphasis/*.json`

### slug 命名

`identity-id` 用方向名 slugify（如 "AI Agent开发" → `ai-agent`，"后端开发" → `backend`）。重名时加后缀（`backend-2024`、`backend-2025`）。

### 投影的关键判断

- **跨方向复用**：fact 层有但当前身份未选的项目，记录到 `excluded[]` 而非删除。换方向时可能复用
- **同一项目不同 framing**：fact 层 granularity 提供多档客观描述，emphasis 选哪档 + 怎么改写是 per-identity 决策。**不修改 fact 层的 granularity text**
- **capabilities 的 skill_axis 归类可跨身份不同**：cap_03（并发系统设计）在后端身份归"后端工程化"，在 AI Agent 身份可归"推理服务部署"——两类说法都对

## exp_standalone：独立项目的合成宿主

事实层的 `experiences.json` 是树形（经历 → 项目）。但**个人项目 / 业余作品没有公司归属**——它们不属于任何真实经历，但仍是有效的项目事实。

规则：**所有"非公司雇佣关系下"的项目，统一挂到合成经历 `exp_standalone` 下**。这是事实层的兜底容器，对应简历里的"个人项目"模块。

何时自动建 `exp_standalone`：

| 场景 | 行为 |
|---|---|
| 用户说"我个人做过 / 业余做过 / 自己搞了个 X" | 评估通过后，若 `exp_standalone` 不存在则 `experience add --id exp_standalone --company "（独立项目 / 个人作品）"`，再 `project add --experience exp_standalone ...` |
| GitHub 仓库 / 个人博客 / Vercel 部署等"非公司地址" | 同上，归 `exp_standalone` |
| 用户提供旧简历里有"个人项目"模块 | 同上 |

何时**不**归 `exp_standalone`：

- 公司项目（哪怕是外包到第三方）→ 归真实经历。例如字节外包到某部属实验室，归字节经历而非 standalone
- 学校课程项目 / 实训 → 视为学校经历（建 `exp_school_<学校>` 或并入教育经历的扩展字段）

**判别测试**：问"这是在雇佣关系下做的吗？"——是 → 真实经历；否 → `exp_standalone`。

投影时不强制选 `exp_standalone`——它和别的经历一样，按 target JD 打分后决定是否进 `emphasis/experiences.json.selected[]`。简历里"个人项目"模块通常单独成节，渲染顺序在公司项目之后（详见 [write-revise.md](write-revise.md) 的"项目经历"定义）。

## 切换身份

操作前先确认当前在哪个身份。读 `identities/` 列出所有身份：

```
identities/
├── backend-2024/
├── ai-agent-2025/
└── fullstack/
```

切换 = 接下来所有操作（读 emphasis、写简历）都基于选中的 `{identity-id}` 目录。

## 删除身份

```
identities/{identity-id}/   ← 整个目录删除
```

**不会**删除事实层 `_shared/`（事实层是共享的）。删除身份 = 删除该方向的强调视角 + 所有已渲染的简历快照。

慎用——已投递的简历快照丢失就找不回了。建议改为"归档"（重命名目录加 `.archived` 后缀）。

## emphasis 维护

### 修改 framing

直接编辑 `emphasis/projects.json.framing[prj_id].bullet`。这是强调层产物，**不会触发**对事实层的任何修改。

### 修改选材

- 加入某项目：移到 `selected[]`，加 framing；从 `excluded[]` 删除
- 移除某项目：从 `selected[]` 移到 `excluded[]`，记录原因

### 修改 skill_axis

`emphasis/capabilities.json.skill_axis` 是 per-identity 的能力归类。可自由重组：把 cap_03 从"后端工程化"挪到"服务性能优化"，不影响事实层和其他身份。

## target.json 维护

- `direction` / `target_role_tags` 改变 → 影响新简历的投影打分（已有 emphasis 不会自动重投影，需手动或显式触发"重新投影"）
- `preferences`（投递偏好：城市/薪资/规模等）改了不影响已渲染简历，只影响下次创建新 resume 时的市场调研
- `target_companies` 是关注的公司清单 + JD 锚点

## needs_review 处理

事实层更新后，引用了变更 fact 的 emphasis 条目和该身份下所有 snapshot 的 `_meta.needs_review` 翻为 `true`。

打开某身份时检查 `emphasis/*.json._meta.needs_review`：

- 全 false：正常工作
- 有 true：提示用户"底层事实 [list] 变了，要不要看"
- 用户审阅后：决定改/不改 framing；即使不改，也可手动清 `needs_review` 并把 `_meta.facts_version_at_last_sync` 推到当前

详见 [snapshot-fork.md](snapshot-fork.md)。
