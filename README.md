# amlei-resume

简历全流程 Claude Code skill —— 从事实沉淀到 A4 PDF 导出的完整工作流。

## Skills

| skill | 说明 |
|-------|------|
| `amlei-profile` | 用户的个人能力记忆——跨会话认识用户的长期事实档案（身份 / 经历 / 项目 / 能力四类事实），独立于任何求职方向 |
| `amlei-resume` | 简历全流程：0→1 写/改/换岗/迭代 + Boss直聘搜岗 + 装配 HTML 导出 A4 PDF |
| `amlei-text-polish` | 润色文本——逐行分析上下文，根据润色目标选用合适的词语和描述，在不改变原意的前提下让文字更清晰有力 |
| `amlei-job-market-research` | 收集指定岗位和城市的就业市场信息——薪资范围、能力要求、技术栈、软硬技能概览、行业趋势与最新动向 |

## 能力

- 三层模型：事实层（profile）→ 强调层（按身份选材 + framing）→ 快照层（一次投递的不可变快照）
- 多身份：同一份事实投影出后端 / AI Agent / 全栈等不同方向的简历
- Paged.js 装配：MD → 主题组件 → A4 多页 HTML，浏览器「导出 PDF」出矢量 PDF
- 6 套主题（academic / tech-dense / content-green / english-mnc / sidebar-creative / soe-formal）
- 6 维度评估闭环 + 润色
- Boss 直聘搜岗（`boss_zhipin.py`）+ 求职招呼语

## 安装

```sh
claude plugin add amlei/amlei-resume
```

## 用法

跟 Claude 说「写简历 / 改简历 / 换岗 / 把简历导出成 A4 PDF」即可触发。详细工作流见各 `SKILL.md` 与 `references/`。
