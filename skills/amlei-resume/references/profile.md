# 个人资料（素材库）

个人资料是由 `scripts/profile.py` 管理，位置优先项目级、否则用户根目录：

- 项目级：`<项目>/.amlei-skill/resume-gen/profile.json`
- 根目录：`~/.amlei-skill/resume-gen/profile.json`

全部命令见 `python3 scripts/profile.py --help`，每条 `<命令> --help` 看参数。

**关键命令：**
- `profile` — 姓名 / 联系方式等基本信息
- `preference` — 求职偏好（城市、职位类型、薪资、经验、学历、公司规模、行业）
- `target` — 在投岗位（城市、年限、标签）
- `company` — 关注的公司及 JD（公司名、行业、岗位、JD 描述、链接）
- `add` / `update` / `find` — 能力与项目条目的增改查

**写简历前必须先有个人资料**——`path` 查不到就问用户选项目级 / 根目录，`init` 创建后再引导补充；没有个人资料不往下走。写简历时从 `profile` 取姓名 / 联系方式填 self-intro；`target list` 看在投哪几岗，生成 / 换岗按对应 target 的城市 / 年限 / tags 来。

个人资料可包含用户感兴趣的公司及 JD（`company add --key 公司名 --position 岗位 --industry 行业 --jd "JD描述" --url 链接`），作为写简历时对标调研的锚点。

## 写入个人资料：独立评估 agent + 用户确认

用户每次补充个人信息，**写入前先派一个独立评估 agent 判断「值不值得记」**（独立上下文、避免自评偏袒），再由用户确认才写：

- 用你当前环境里「创建子 agent」的方式，起一个**独立上下，zhu yi a文**的评估 agent——**具体调用哪个工具不在本规则里固定**（不同 Agent 平台机制不同，由 LLM 自行选用），目的是拿到一个不带自评偏袒的独立判断。
- 评估标准、输入与输出格式见 [memory-evaluator.md](memory-evaluator.md)（四条：硬/软实力、长期价值、岗位核心、是否过时；外加防过度包装、数字待确认等把关）。
- **评估通过且用户确认后**，才调 `profile.py add` / `update`；不通过就告诉用户为什么不记。

> 脚本写入前会自动备份（带时间戳，保留最近 10 份）；但个人资料不可撤回，仍以「评估 agent + 用户确认」双保险为准。
