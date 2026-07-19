# 个人资料（素材库）

个人资料是由 `scripts/profile.py` 管理，位置优先项目级、否则用户根目录：

- 项目级：`<项目>/.amlei-skill/resume-gen/profile.json`
- 根目录：`~/.amlei-skill/resume-gen/profile.json`

全部命令见 `python3 scripts/profile.py --help`，每条 `<命令> --help` 看参数。

**关键命令：**
- `profile` — 姓名 / 联系方式等基本信息
- `preference` — 求职偏好（城市、职位类型、薪资、经验、学历、公司规模、行业）
- `target` — 在投岗位（城市、年限、标签）
- `company` — 关注的目标公司及 JD（作为调研锚点）
- `experience` — 工作过的公司（公司名、岗位、时间段、行业）
- `add` / `update` / `find` — 能力与项目条目的增改查
- `batch` — **(优先使用)** 批量操作（传 `--json` 字符串或 stdin），一次保存一份备份

**写简历前必须先有个人资料**——`path` 查不到就问用户选项目级 / 根目录，`init` 创建后再引导补充；没有个人资料不往下走。写简历时从 `profile` 取姓名 / 联系方式填 self-intro；`target list` 看在投哪几岗，生成 / 换岗按对应 target 的城市 / 年限 / tags 来。

个人资料可包含用户感兴趣的公司及 JD（`company add --key 公司名 --position 岗位 --industry 行业 --jd "JD描述" --url 链接`），作为写简历时对标调研的锚点。工作过的公司用 `experience add --key 公司名 --position 岗位 --period "2024.07 — 2025.03" --industry 行业` 记录。

## 触发写入 profile 的时机

| 场景 | 行为 |
|------|------|
| 导入旧简历（.docx/.pdf） | 直接写入（证件照/基本信息/技能列表，不经过评估 agent） |
| 讨论项目聊出可跨岗位复用的能力/成果 | 评估 agent + 用户确认后写入 |
| 用户主动说"帮我记一下" | 评估 agent + 用户确认后写入 |
| 改完简历发现 profile 里没有的新素材 | 问用户"要不要同步进 profile？"→ 用户同意后评估 + 写入 |

## 写入流程

用户补充个人信息（含软实力自我评价），**写入前先派一个独立评估 agent 判断「值不值得进 profile」**（独立上下文、避免自评偏袒），再由用户确认才写：

- 用你当前环境里「创建子 agent」的方式，起一个**独立上下文**的评估 agent——**具体调用哪个工具不在本规则里固定**（不同 Agent 平台机制不同，由 LLM 自行选用），目的是拿到一个不带自评偏袒的独立判断。
- 评估标准、输入与输出格式见 [profile-evaluator.md](profile-evaluator.md)。
- **评估通过且用户确认后**，才调 `profile.py add` / `update`；不通过就告诉用户为什么不记。

> 脚本写入前会自动备份（带时间戳，保留最近 10 份）。
