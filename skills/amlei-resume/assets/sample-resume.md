# self-intro

name: 张昀
role: 申请方向 · 计算机科学 直博（PhD）
gender: 男
location: 北京
phone: 139-0108-2025
email: zhangyun@example.com
site: yunzhang.io
avatar:

# 个人简介

清华大学计算机科学实验班（姚班）本科四年级，连续三年专业第 1。专注**大模型对齐与多模态学习**方向，以**共一 / 一作**在 NeurIPS、ICLR、CVPR 发表论文 4 篇；曾在微软亚洲研究院与 Google DeepMind 实习，主导 RLHF 算法改进与多模态检索框架设计。擅长从理论分析到工程落地的全链路研究，希望加入顶尖科研团队攻读博士学位，在**可信大模型**方向做出系统性贡献。

# 研究兴趣

大模型对齐与 RLHF, 多模态学习, 高效预训练, 检索增强生成

# 教育背景

## 清华大学 | 计算机科学实验班（姚班）· 本科
date: 2022.09 — 2026.06
meta: GPA 3.97/4.0 · 专业排名 1/60 · 核心课：机器学习(97)、深度学习(98)、凸优化(96)

# 科研经历

## 微软亚洲研究院（MSRA） | 自然语言计算组 · 研究实习生
date: 2025.04 — 2025.11

- 提出基于过程奖励的 RLHF 改进算法，将奖励模型分解为"步骤级正确性"信号，在数学推理任务上胜率较基线提升 9.2%，成果投递 NeurIPS 2025。
- 构建 2 万条高质量过程标注数据，设计半自动标注管线将人工成本降低 60%，开源内部评测基准被组内 3 个项目复用。
- 与资深研究员合作完成从 idea 到论文的全流程，独立负责实验设计、训练调度（DeepSpeed ZeRO-3）与 ablation 分析。

## Google DeepMind | Multimodal Perception 组 · 研究实习生
date: 2024.06 — 2024.12

- 主导视觉-语言对齐框架设计，提出基于对比-生成混合损失的训练目标，在 VQAv2 与 GQA 上分别超过 SOTA 1.4 / 1.1 个点，论文被 ICLR 2025 录用（共一）。
- 复现并改进 LLaVA 系列基线，定位数据配比与分辨率对下游推理能力的影响，沉淀为组内多模态训练手册。
- 远程协作完成 3 轮 rebuttal，独立撰写 method 与 appendix 共 4 页。

## 清华大学交互式人工智能组 | 本科科研助理 · 导师：Y 教授
date: 2023.09 — 至今

- 主导多模态检索增强框架设计与实验，提出动态路由的检索头使模型按问题难度自适应调用外部知识，论文被 CVPR 2024 Workshop 录用（一作）。
- 指导 2 名低年级本科生完成子课题，其中 1 人以二作身份在 ACL Workshop 发表论文。

# 项目经历

## 开源多模态评测工具包 MM-Eval | 个人项目 · 维护者
date: 2024.03 — 至今

- 从零搭建覆盖 12 个多模态基准的统一评测框架，支持一键复现与分布式评测，GitHub 收获 1.2k stars，被 5 个研究组作为标准评测工具采用。
- 设计插件化数据集接口，使新增基准的接入成本从 2 天降到 2 小时；编写完整文档与 CI，累计接受外部 PR 40+。

## 高效推理内核 lite-attn | 实验室项目 · 核心贡献者
date: 2024.09 — 2025.02

- 实现 FlashAttention-2 的 Triton 移植与 int8 量化变体，在 A100 上对 7B 模型推理吞吐提升 38%，显存占用降低 31%。
- 通过算子融合与 KV-cache 重排消除 4 个冗余内核，端到端延迟下降 22%。

# 论文发表

[C] Yun Zhang*, H. Li, X. Wang, et al. Process-Reward RLHF for Faithful Mathematical Reasoning. Advances in Neural Information Processing Systems (NeurIPS), 2025. (*共一)
[C] Yun Zhang*, M. Chen, et al. Hybrid Contrastive-Generative Alignment for Vision-Language Models. International Conference on Learning Representations (ICLR), 2025. (*共一)
[W] Yun Zhang, X. Wang. Adaptive Multimodal Retrieval for Open-Domain VQA. CVPR Workshop on Vision-Language Models, 2024. (一作)
[W] Yun Zhang, T. Liu. On the Stability of Step-level Reward in RLHF. NeurIPS Workshop on Alignment, 2024. (一作)

# 荣誉与奖项

2024 | 国家奖学金 | 国家级
2024 | 清华大学特等奖学金 | 提名
2023 | ACM-ICPC 亚洲区域赛 | 金牌
2024 | 全国大学生数学竞赛 | 一等奖
2024 | NeurIPS Scholar Award | 国际
2023 | 清华大学优秀学生 | 校级
2023 | 字节跳动奖学金 | 企业级
2022 | 高考省理科前 10 / 姚班录取 | 省级

# 学术服务

- 担任 NeurIPS 2025、ICLR 2025、ACL 2025 审稿人，累计审稿 8 篇。
- 担任 MM-Eval 开源社区维护者，主持每月线上技术分享 6 期。

# 技能与英语

科研工具: PyTorch · JAX · HuggingFace · DeepSpeed · CUDA · LaTeX · Linux · Git
编程语言: Python · C++ · Julia · SQL · Rust
英语: TOEFL 112（口语 26）· GRE 328（V158 Q170）· 可全英文科研交流
