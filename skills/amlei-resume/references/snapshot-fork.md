# 快照与 fork

`identities/{id}/resumes/{app-id}/` 是一次具体投递的快照。每个快照有自己的 `_meta.json` 记录血缘、版本戳、交付状态。

## 三种快照创建方式

| source_operation | 含义 | 何时用 |
|---|---|---|
| `new_from_projection` | 新身份刚投影出第一份 | 创建新身份后立即写第一份简历 |
| `new_from_emphasis` | 已有身份下，基于当前 emphasis 渲染 | 同身份下投不同公司，每家一份 |
| `fork` | 基于旧 snapshot 复制起步 | "5 月那版基础上改改" |

## 快照不可变（R7）

`_meta.delivered: true` 后，`简历.md` **永不修改**——包括事实层更新、emphasis 编辑、系统维护都不能改它。这是为了已投出的简历可复现。

事实层变化时，`_meta.needs_review` 翻 `true`（不改文件内容）；emphasis 变化时也不动 snapshot。

## fork 流程

用户说"在 X 那版基础上改改"，触发 fork：

```
1. 源：identities/{id}/resumes/{source-app}/
2. 目标：identities/{id}/resumes/{new-app}/
3. 复制 简历.md（连同 materials.md / jd.md，按需）
4. 写 _meta.json：
     source_operation: "fork"
     forked_from: "{source-app}"
     facts_version_at_creation: <当前 _shared/_meta.facts_version>
     created_at: <now>
     delivered: false
     needs_review: <见下>
5. 计算 fact diff，提示用户（见下）
```

### fact diff 计算

```
当前 facts_version   = _shared/_meta.facts_version
快照创建时版本       = source.facts_version_at_creation
```

若两者不同（事实层在快照创建后更新过）：

1. 找出**变了**的 fact（哪些 project / experience / capability 在 source.facts_version_at_creation 之后修改过）
2. 对每个变的 fact，检查源快照简历.md 是否引用（通过 emphasis/projection 间接引用，或 bullet 文本匹配）
3. 输出 diff 提示：

```
⚠ 源快照之后事实层有更新：
  - prj_014（OCR 调度）的 p99_latency：源快照写"200ms"，事实层当前"150ms"
  - cap_03（并发系统设计）的 proven_by 增加了 prj_022
要不要把更新套进新版本？逐条确认。
```

4. 用户对每条 diff 决定：吸收（重写 bullet）/ 不吸收（保留旧措辞）
5. **系统永不自动应用 diff**——只提示

### fork 后 needs_review

- 若源快照 `_meta.needs_review: true`，新 fork 也初始为 `true`（继承未审阅状态）
- 若用户在 fork 过程中审阅并吸收了所有 diff，可手动清 `needs_review`
- 若 fork 时无 diff（facts_version 相同），新 fork 初始 `needs_review: false`

## 投递（delivered）

用户决定投出某份简历时：

```bash
# 通过脚本（待 amlei-resume v2 提供）
# 或直接编辑 _meta.json
```

```json
{
  "delivered": true,
  "delivered_at": "<now>"
}
```

`delivered: true` 后：
- `简历.md` 不可变
- 事实层后续变化只触发 `_meta.needs_review`，不改文件内容
- 若想改投出版本，必须 fork 出新版本

## needs_review 的清除

用户审阅了某 emphasis 条目或 snapshot 的 needs_review 提示后，决定不改文案：

```json
{
  "_meta": {
    "needs_review": false,
    "facts_version_at_last_sync": "<当前 _shared/_meta.facts_version>"
  }
}
```

这只是元数据修复（不调脚本备份），表示"用户看过了，认可当前文案"。下次事实再变还会再翻位。

## lineage 追溯

通过 `_meta.json` 可追溯：

- `source_operation` 告诉这份简历怎么来的
- `forked_from` 指向源 snapshot（若 fork）
- `facts_version_at_creation` 记录创建时事实层版本
- `emphasis_version_at_creation` 记录创建时 emphasis 状态

支持"这份简历基于哪个版本的事实 + 哪个版本的强调"完整还原。
