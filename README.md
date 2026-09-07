# amlei-resume

写简历最浪费的地方，是每投一个方向，都要把自己重讲一遍。

amlei-resume 是一组装进 AI 助手的 [Agent Skill](https://agentskills.io)：你的经历和能力只沉淀一次，之后想投哪个方向，就把这份档案投影成那个方向的简历。支持 Claude Code、Cursor、Codex、Gemini CLI、OpenCode、Copilot。

## 它是什么

三个词：**记得住、分得清、管到底**。

- **记得住**——你聊过的经历、项目、能力，沉淀成一份跨会话的长期档案。下次打开，不用从头讲起。
- **分得清**——「做过什么」是事实，全局只记一遍；「怎么讲」是强调，每个求职方向各有一版。换岗不是重写，是重新选材。
- **管到底**——从市场调研、挖素材、写改润色、六维评估，到导出矢量 A4 PDF、生成招聘平台招呼语，一条流程走完。

## 核心设计：事实与讲法分离

```
事实层（全局一份）      你做过什么——经历、项目、能力，条条带证据，跨会话累积
       ↓ 投影
强调层（每个方向一份）   这份简历要突出哪一面——选材、排序、措辞
       ↓ 装配
快照层（每次投递一份）   定稿的简历本体 + 导出产物，各次投递互不干扰
```

判断标准只有一个：**两次不同方向的面试里，这件事你会讲得不一样吗？** 不会变的进档案；会变的，才属于某一份简历。

## 写简历的过程是什么样的

你跟它聊。聊目标方向、聊做过的事、聊那些你自己都没当回事的细节——它会带着推理去读你给的资料，把疑点追问出来，而不是照单全收。聊出的客观事实经你确认后进入档案；写出的文案先过它自己的六维评估，不合格就回炉重改。

也可以直接丢一份旧简历（.docx / .pdf）进来，它负责解析、重排模块、抽出证件照，转成能继续打磨的底稿。

每一步都有人工卡点：**你没说「可以」之前，它一个字也不会写进你的简历。**

## 导出效果：矢量 A4 简历 PDF

一份简单的 Markdown，渲染成矢量 A4 简历，所见即所得：

![简历导出预览](assets/resume-preview.png)

> 想看 PDF 版？打开 [A4 预览 PDF](assets/张昀-计算机科学直博%20·%20简历%20A4%20预览.pdf)。

源文件就是朴素的 Markdown——模块顺序即简历顺序，写完选主题、一键导出：

```md
# self-intro

name: 张昀
role: 申请方向 · 计算机科学 直博（PhD）

# 科研经历

## 微软亚洲研究院（MSRA） | 自然语言计算组 · 研究实习生
date: 2025.04 — 2025.11

- 提出基于过程奖励的 RLHF 改进算法……
```

预览页还能就地改：改字、删加技能条，自动重排分页，改完一键导回 Markdown：

![预览页可就地编辑](assets/edit-preview.png)

六套主题，同一份内容换皮：

| 学术 / 科研 | 技术密排 | 内容运营 |
|:--:|:--:|:--:|
| ![学术 / 科研](assets/theme-samples/academic.png) | ![技术密排](assets/theme-samples/tech-dense.png) | ![内容运营](assets/theme-samples/content-green.png) |

| 外企 / 英文 | 侧栏创意 | 国企 / 正式 |
|:--:|:--:|:--:|
| ![外企 / 英文](assets/theme-samples/english-mnc.png) | ![侧栏创意](assets/theme-samples/sidebar-creative.png) | ![国企 / 正式](assets/theme-samples/soe-formal.png) |

> 整页预览：[学术 / 科研](assets/theme-samples/academic.html) · [技术密排](assets/theme-samples/tech-dense.html) · [内容运营](assets/theme-samples/content-green.html) · [外企 / 英文](assets/theme-samples/english-mnc.html) · [侧栏创意](assets/theme-samples/sidebar-creative.html) · [国企 / 正式](assets/theme-samples/soe-formal.html)

同一份简历还能换 **8 套点缀配色**，预览页选好，导出 PDF 沿用：

![8 套点缀配色](assets/color-schemes.png)

## 四个 skill，一条流水线

| 角色 | skill | 干什么 |
|------|-------|--------|
| 侦察 | `amlei-job-market-research` | 拉指定岗位 + 城市的行情：薪资、能力要求、技术栈 |
| 档案 | `amlei-profile` | 维护你的长期事实档案，独立于任何求职方向 |
| 执笔 | `amlei-resume` | 把档案投影成具体方向的简历：写 / 改 / 换岗 / 评估 / 导出 |
| 打磨 | `amlei-text-polish` | 逐行润色，不改原意，让表达更清晰有力 |

> 想 diy 或看内部机制，每个 skill 的 `SKILL.md` 和 `references/` 里有完整说明。

## 上手

**1. 安装**（以 Claude Code 为例）

```sh
claude plugin add amlei/amlei-resume
```

**2. 开聊**。一句话就能开始——

- 「做了三年后端，想转 AI Agent 方向，这是我的旧简历，帮我重新讲一版。」
- 「简历定稿了，导出 A4 PDF，再帮我写几条 Boss 直聘的开场白。」

更建议把目标、经历、材料来源一次说全，它就能照着画像开工。说漏了也没关系，细节是边聊边冒出来的。

## 几条较真的原则

- **能力必须有证据**——写进档案的每条能力，都要能指回证明它的项目；举不出证据的，只能算讲法。
- **写「做到什么」，不写「怎么做到的」**——bullet 落在结果，做法细节是面试官的常识，写出来只会稀释重点。
- **事实更新只提醒，不动你的文案**——底层事实变了，它标记出来等你决定，绝不自动改写你敲定的措辞。
