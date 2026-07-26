# amlei-resume

简历全流程 Claude Code skill —— 从事实沉淀到 A4 PDF 导出的完整工作流。

拆自 [`amlei-skills`](https://github.com/amlei/amlei-skills)（后者现只保留可复用 utility skill）。这是一个**独立产品**：三层模型 + Paged.js 装配 + 评估闭环，不是单一 utility。

## 两个 skill

| skill | 职责 |
|-------|------|
| `amlei-profile` | **事实层**：跨会话的个人能力记忆（身份 / 经历 / 项目 / 能力四类事实），独立于任何求职方向 |
| `amlei-resume` | **强调层 + 快照层**：消费 profile 的事实，投影成具体方向的简历，装配 HTML → A4 PDF |

`amlei-resume` 是 `amlei-profile` 的消费者；用 resume 前会先加载 profile。

## 能力

- 三层模型：事实层（profile）→ 强调层（按身份选材 + framing）→ 快照层（一次投递的不可变快照）
- 多身份：同一份事实投影出后端 / AI Agent / 全栈等不同方向的简历
- Paged.js 装配：MD → 主题组件 → A4 多页 HTML，浏览器「导出 PDF」出矢量 PDF
- 6 套主题（academic / tech-dense / content-green / english-mnc / sidebar-creative / soe-formal）
- 6 维度评估闭环 + 润色（调 amlei-text-polish）
- Boss 直聘搜岗（`boss_zhipin.py`）+ 求职招呼语

## 安装

```sh
claude plugin add amlei/amlei-resume
```

> 工作流里的润色（amlei-text-polish）和就业市场调研（amlei-job-market-research）是 **companion utility skill**，装在 [`amlei-skills`](https://github.com/amlei/amlei-skills) 里；要用满全流程，两个 plugin 都装上。

## 用法

跟 Claude 说「写简历 / 改简历 / 换岗 / 把简历导出成 A4 PDF」即可触发。详细工作流见各 `SKILL.md` 与 `references/`。

## 相关

- Utility skill 仓库：[amlei/amlei-skills](https://github.com/amlei/amlei-skills)
