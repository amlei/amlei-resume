# AGENTS.md

本仓库是 **Agent Skill 包**（[agentskills.io](https://agentskills.io) 规范，作为 Claude Code 插件与 WorkBuddy 专家包发布），不是应用。
没有 build / test / lint / dev server——`package.json` 的 `scripts` 为空，CI 已移除（发布是手动 `npm publish`）。
"验证一个改动" = 跑相关 `python3 scripts/*.py --help`，或用 `skills/amlei-resume/references/sample-resume.md` 走一遍导出流程。

## 两个 skill 的分层（改内容前必读）

| skill | 拥有的内容 | 消费关系 |
|-------|-----------|---------|
| `amlei-resume` | 记忆底座 `profile.md`（事实层）+ `materials/`（跨方向证据池）+ `identities/{id}/` 各方向简历产物（组织层） | 自包含；参考文件入口 `references/index.md`，事实写入规则在 `references/profile.md`，整个目录与材料池规范在 `references/file.md`，简历 DSL 在 `references/resume-format.md` |
| `amlei-portfolio` | 简历数据根 `portfolio/` 下的 `{identity-id}-作品集.md` 与跨方向共用素材 | 入口 `SKILL.md`，作品集格式与目录规范在 `references/portfolio-format.md`；Skill 定义和 reference 独立，但作品集运行数据归属于简历数据根 |

WorkBuddy 专家包的根目录是**仓库根**：`.codebuddy-plugin/plugin.json`（市场清单）+ `agents/amlei-resume.md`（统一人设，只写人设不复制技能规则）+ `avatars/expert.png`（512×512 头像）+ `skills/`（两个独立技能本体）。市场要求的 skills 字段格式「./skills/<name>」从仓库根解析正好指向对应技能。打市场包：仓库根执行 `zip -r amlei-resume.zip .codebuddy-plugin agents avatars skills README.md LICENSE -x "*.DS_Store"`。

岗位调研不单独成 skill——agent 自带搜索，需要时按 `references/job-research.md` 联网调研。

改简历内容时，记忆判别在 `skills/amlei-resume/SKILL.md` 的「记忆与材料」一节：原始素材先落 `materials/`；只有"未来简历会用到 + 有证据 + 跨方向不变"的客观事实进 `profile.md`；具体求职范围进 `target.json`；简历措辞、投递局部信息不写回。

改作品集内容时，定位、案例、结果、证据和发布信息都直接写入 `.amlei-skill/resume/portfolio/{identity-id}-作品集.md`；图片与视频放在同根、跨方向共用的 `assets/`。作品集 Skill 不复制或修改 `profile.md`、`target.json` 与简历正文，也不复用简历 Skill 的 reference。

**SKILL 写的是通用场景，不绑定某个专业领域。** 规则、易错点、追问钩子都要写成领域无关的抽象表述；某项确需举例说明时，措辞为「以**领域为例」（如「以计算机领域为例」「以运营领域为例」），不能把整条规则围绕单一领域写死——否则换领域的人读到会觉得"这不适用于我"。

## 判断类内容的写法

筛选、选材和表达等开放判断应围绕一个核心决策问题展开，用"需要什么判断 → 凭什么相信 → 证据不足时如何行动"的链条推导，不要堆成互不关联的检查清单。

具体指标、工具或案例只能作为领域示例，不能升级为所有用户都必须满足的标准。格式、安全、隐私和权限仍用明确规则表达。

独立判断模块必须由主流程明确引用并说明执行时机，避免成为 Agent 不知道何时使用的孤立章节。同一判断只保留一个执行点；每轮已经自问，就不再增加重复的终审步骤。

## 脚本与外部依赖

脚本在 `skills/amlei-resume/scripts/`，直接可用，不依赖 CLI：

- `wrap_preview.py`：把渲染好的简历正文包进 A4 预览壳（Paged.js 分页）。
- `export_long_image.py`：导出简历长图（招聘平台聊天框发送用）。
- `extract_avatar.py`：从旧简历提取证件照。

外部依赖（非 stdlib，只在对应脚本需要——别装全量）：

| 脚本 | 依赖 |
|------|------|
| `wrap_preview.py` | 仅 stdlib |
| `export_long_image.py` | `pip install playwright Pillow && playwright install chromium` |
| `extract_avatar.py` | `opencv-python` `numpy`（首次运行下载 YuNet 人脸模型到 `~/.cache/resume-design/`） |

## 简历 DSL

简历是一份有硬规则的 Markdown：`# self-intro` 必须是首个 `#`；模块出现顺序 = 简历顺序；经历用 `## 机构 | 角色`。完整规范在 `skills/amlei-resume/references/resume-format.md`，读取入口是 `references/index.md`，范例是 `skills/amlei-resume/references/sample-resume.md`——改装配逻辑前先对齐它。

## 作品集格式

作品集归属于简历数据根：当前工作区使用 `.amlei-skill/resume/portfolio/`，否则回退到 `~/.amlei-skill/resume/portfolio/`。每个方向使用 `{identity-id}-作品集.md`，跨方向素材放在共用 `assets/`。作品集不提供本地导出，发布载体就是在线页面；格式见 `skills/amlei-portfolio/references/portfolio-format.md`。

## 哪些是源、哪些是运行时数据（gitignored）

- **源**：`skills/`、`.claude-plugin/plugin.json`、`.codebuddy-plugin/plugin.json`（WorkBuddy 专家清单）、`agents/`（WorkBuddy 人设）、`avatars/`（WorkBuddy 头像）、`README.md`、`assets/`（README 用的预览图 + 一份特例放行的 A4 PDF）。
- **运行时用户数据（别提交）**：`.amlei-skill/`、`resume/`、`*.docx`、`*.pdf` 全在 `.gitignore`。仓库根那几个 `.pdf` / `.docx` 是本地测试简历，不是源。
