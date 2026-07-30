# AGENTS.md

本仓库是 **Agent Skill 包**（[agentskills.io](https://agentskills.io) 规范，作为 Claude Code 插件发布），不是应用。
没有 build / test / lint / dev server——`package.json` 的 `scripts` 为空，CI 已移除（发布是手动 `npm publish`）。
"验证一个改动" = 跑相关 `python3 scripts/*.py --help`，或用 `skills/amlei-resume/assets/sample-resume.md` 走一遍导出流程。

## 四个 skill 的分层（改内容前必读）

| skill | 拥有的层 | 消费关系 |
|-------|---------|---------|
| `amlei-profile` | 事实层 `_shared/`（identity/experiences/capabilities） | 被 resume 消费；加载顺序：**先 profile 再 resume** |
| `amlei-resume` | 强调层 `identities/{id}/emphasis/` + 快照层 `identities/{id}/resumes/` | 消费 profile；bullet 文案是强调层产物，**不写回 `_shared/`** |
| `amlei-text-polish` / `amlei-job-market-research` | 无状态 helper | resume 以 subagent 方式调用 |

改 resume 的 SKILL 内容时，"事实 vs 强调" 的判别在 `skills/amlei-profile/SKILL.md` 顶部——别把 framing 规则塞进事实层。

**SKILL 写的是通用场景，不绑定某个专业领域。** 规则、易错点、追问钩子都要写成领域无关的抽象表述；某项确需举例说明时，措辞为「以**领域为例」（如「以计算机领域为例」「以运营领域为例」），不能把整条规则围绕单一领域写死——否则换领域的人读到会觉得"这不适用于我"。

## 脚本：统一 CLI + 外部依赖

两个 CLI 都按 `~/.amlei-skill/resume/` → 否则 `<cwd>/.amlei-skill/resume/` 解析数据目录（均 gitignored）。写前自动时间戳备份（留最近 10 份），退出码 1 = 校验失败 / 不存在。

- **`skills/amlei-resume/scripts/resume_cli.py`** = 三层模型统一入口（事实层子命令会 shell-out 调 `profile.py`）。**别直接调 profile.py 做事实层 CRUD，走 resume_cli.py。**
- **`skills/amlei-profile/scripts/profile.py`** = 事实层后端（resume_cli.py 调它）。
- **`skills/amlei-resume/scripts/wrap_preview.py`** = 把渲染好的正文包进 A4 预览壳（Paged.js 行级分页）。

外部依赖（非 stdlib，只在对应脚本需要——别装全量）：

| 脚本 | 依赖 |
|------|------|
| `resume_cli.py` / `profile.py` / `wrap_preview.py` | 仅 stdlib |
| `export_long_image.py` | `pip install playwright Pillow && playwright install chromium` |
| `extract_avatar.py` | `opencv-python` `numpy`（首次运行下载 YuNet 人脸模型到 `~/.cache/resume-design/`） |
| `boss_zhipin.py` | `pip install cloakbrowser`（+ playwright + chromium） |

## 简历 DSL

简历是一份有硬规则的 Markdown：`# self-intro` 必须是首个 `#`；模块出现顺序 = 简历顺序；经历用 `## 机构 | 角色`。完整规范在 `skills/amlei-resume/SKILL.md` 的"简历格式"表，范例是 `skills/amlei-resume/assets/sample-resume.md`——改装配逻辑前先对齐它。

## 哪些是源、哪些是运行时数据（gitignored）

- **源**：`skills/`、`.claude-plugin/plugin.json`、`README.md`、`assets/`（README 用的预览图 + 一份特例放行的 A4 PDF）。
- **运行时用户数据（别提交）**：`.amlei-skill/`、`resume/`、`*.docx`、`*.pdf`、`boss_state.json` 全在 `.gitignore`。仓库根那几个 `.pdf` / `.docx` 是本地测试简历，不是源。
