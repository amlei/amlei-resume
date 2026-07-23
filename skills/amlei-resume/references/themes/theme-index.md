# 简历主题索引（theme-index）

> **主题信息的单一来源**。每个"主题"= 一套完整组件库（设计令牌 + 各组件 HTML + 简历骨架 + MD→组件映射），文件在 `references/theme-{标识}.md`。选题、登记、回归都以本表为准。
>
> 每个主题是一套**自包含**的组件库（设计令牌 + `<style>` + 组件 + 骨架 + MD→组件映射），不依赖外部源文件。**想看某主题效果**：用 `assets/sample-resume.md` 渲染该主题（→ `wrap_preview.py`）生成预览 HTML 即可。

## 主题清单

| 主题 | 标识 | 主色 | 适用场景 | 组件库文件 |
|------|------|------|----------|-----------|
| 学术 / 科研 CV | `academic` | 墨蓝 `oklch(33% .05 258)` | 升学 / PhD 申请 / 科研岗；含论文、奖项、研究兴趣；单栏、证件照 | [theme-academic.md](theme-academic.md) |
| 技术密排 | `tech-dense` | 工程蓝 `oklch(46% .17 242)` | 互联网技术 / 算法 / 后端 / 基础架构岗；技术栈前置 chips、项目数据导向 | [theme-tech-dense.md](theme-tech-dense.md) |
| 内容运营·绿 | `content-green` | 深森林绿 `oklch(40% .06 155)` | 内容 / 运营 / 增长 / 新媒体 / 内容产品岗 | [theme-content-green.md](theme-content-green.md) |
| 外企 / 英文 MNC | `english-mnc` | 酒红 `oklch(40% .13 25)` | 外企管培 / BA / 咨询；**英文**、UPPERCASE 标题 | [theme-english-mnc.md](theme-english-mnc.md) |
| 侧栏创意 | `sidebar-creative` | 暖珊瑚 `oklch(56% .15 38)` | 创意 / UI·UX / 视觉 / 设计岗；**双栏单页**（特殊结构，见主题文件） | [theme-sidebar-creative.md](theme-sidebar-creative.md) |
| 国企 / 正式 | `soe-formal` | 藏青 `oklch(31% .058 258)` | 国企 / 银行 / 央企 / 公职；含政治面貌/籍贯/民族基本信息表 | [theme-soe-formal.md](theme-soe-formal.md) |

## 选题规则（据目标岗位 / 行业）

- **用户已指定主题** → 直接用，不问。
- **升学 / 科研 / PhD / 有论文奖项** → `academic`
- **互联网技术 / 算法 / 后端 / 数据** → `tech-dense`
- **内容 / 运营 / 增长 / 新媒体** → `content-green`
- **外企 / 英文岗 / 跨国公司** → `english-mnc`
- **创意 / 设计 / 品牌** → `sidebar-creative`
- **国企 / 银行 / 公职 / 央企** → `soe-formal`
- **无明显倾向** → 默认 `academic`（单栏、克制、最通用）。
- **`sidebar-creative` 是特殊的单页双栏主题**：正文只有一个 `.two-col` 原子、内容必须进一页 A4；内容多、要分页的简历不要选它（详见其主题文件）。其余 5 个都是单栏多页、自动分页。

> 主题切换 = 换组件库文件，**不改**预览外壳 / 脚本。换主题时整篇只用该主题那一套组件，不跨主题混用。

## 添加 / 转换新主题的规范

新主题以 `references/theme-{英文标识}.md` 命名，必须包含：

1. **设计变量速查表**（主色 / 浅底 / 深字 / 正文色 / 发丝线色 / 字体）
2. **完整 `<style>` 块**（设计令牌 `:root` + 各组件 class 样式；**不含** `.viewport/.page/#source/@media print`——那些归预览外壳）
3. **各组件完整 HTML**（带 `{{占位符}}`，class 与 `<style>` 对应）
4. **简历骨架**（组件装配顺序：Header → 按 MD 模块顺序的各 Section）
5. **Markdown → 组件映射规则表**

新主题可直接编写，或从一份参考简历 HTML 转换而来（把它的 `<style>` 里 `:root` + 组件 class 抽成主题 `<style>`——剔除外壳负责的舞台/分页/打印规则；把各原子抽成带 `{{占位符}}` 的组件；记录骨架顺序与 MD→组件映射）。无论哪种方式：

1. 写成 `references/theme-{标识}.md`，含上面 5 个部分。
2. 在本表登记一行（主题 / 标识 / 主色 / 适用场景 / 文件）。
3. **查看效果 = 用 `assets/sample-resume.md` 渲染该主题 → `wrap_preview.py` → 浏览器打开预览**，确认可用。
