# 共享组件库（component-library）

> 5 个单栏主题（`academic` / `tech-dense` / `content-green` / `english-mnc` / `soe-formal`）**共用**的基准组件库：基准组件 HTML、简历骨架、MD→组件映射。
> 每个主题文件只含三节：设计变量速查表 + 完整 `<style>` + 「主题差异」（相对本库的增删改变体）。装配 = 本库基准组件 + 主题差异覆盖。
> `sidebar-creative` 是双栏单页特殊主题，**自包含**，不使用本库。

## 硬约束（所有单栏主题遵守）

- **class 命名不可随意改**：预览外壳 `assets/preview-shell.html` 按 class 识别原子、分页行为与行内编辑（`.sec-head` / `.entry` / `.bullet` / `.skills-row` / `.stack-row` / `.pubs li` / `.award` 等）。本文的命名即 canonical 命名，主题 `<style>` 向它对齐。
- `data-stick="1"` 是旧版手动分页遗留，现由外壳 CSS `break-*` 按 class 自动处理；模板里保留、照抄无害。
- **bullet 原子化**：每条 `- bullet` 拆成独立 `.bullet` 兄弟节点，不包进 Entry / `<ul>`（分页原子）。
- **项目经历三段式单行**：`.proj`（左）· `.company`（居中，是 `.entry-main` 的直接子节点，不包进 `.entry-title`）· `.entry-date`（右），**无任何符号、无 `.role`**——职责由下方 bullet 体现。
- **行内强调统一用 `<b>`**（转强调字色）；关键数字用 `<span class="num">`（等宽 + 强调色）。
- **单点缀色**：一个 accent + 同色系更深强调字色；姓名 24–28px（非巨标题）；分割线用 1px 发丝 / 虚线。
- **联系方式占位符全主题统一命名**：核心三元组顺序固定 `{{location}}` → `{{phone}}` → `{{email}}`；链接类字段统一写 `<a href="{{x-url}}">{{x}}</a>`（x = `github` / `site` / `linkedin` …）；其余扩展字段（`{{gender}}` / `{{age}}` / `{{political}}` / `{{platform}}` / `{{relocation}}` …）统一小写，gender 类前置、其余追加在尾部。具体放哪些字段 = 主题差异节的「默认字段集」∧ `self-intro` 实际字段；字段间用 `<span class="sep">·</span>`，缺失字段连同它的 `sep` 一起删，不留空段。
- `{{education}}` 单独一行（`education:` 字段，子项 ` · ` 拼接），无则删整行。
- `{{photo}}`：有真实头像用 `<div class="photo"><img src="{{avatar}}" alt="证件照"></div>`；没有用 [icons.md](icons.md) 的证件照占位（`{{photo}}` 处放占位组件）。

## 基准组件（带 `{{占位符}}`，class 与主题 `<style>` 对应）

### 1. Header —— `# self-intro` 模块用它（不渲染 SectionHead）

```html
<header class="resume-header">
  <div class="ident">
    <div class="name-row"><span class="name">{{name}}</span><span class="role">{{role}}</span></div>
    <div class="edu-line">{{education}}</div>
    <div class="contact">{{location}}<span class="sep">·</span>{{phone}}<span class="sep">·</span>{{email}}</div>
  </div>
  {{photo}}
</header>
```

- `{{role}}` = 求职/申请方向，无则连同 `<span class="role">` 一起删。
- contact 行的默认字段集见各主题差异节（命名与顺序规则见硬约束）。

### 2. SectionHead（图标 + 标题 + 发丝线；英文小标签可选）

```html
<div class="sec-head" data-stick="1">{{icon}}<h2>{{title}}<span class="en">{{en}}</span></h2></div>
```

- `{{icon}}`：按模块语义从 [icons.md](icons.md) 选一个 `<svg class="ico" …>…</svg>`。
- `{{en}}`：英文小标签（可选），无则连 `<span class="en">` 一起删。

### 3. Summary（个人简介段落）

```html
<div class="summary"><p>{{text}}</p></div>
```

段落里 1–3 个最关键短语用 `<b>…</b>` 加重。

### 4. Interests（方向标签行，可选）

```html
<div class="interests"><span class="it">{{tag1}}</span><span class="it">{{tag2}}</span><span class="it">{{tag3}}</span></div>
```

每个标签一个 `<span class="it">`，按 MD 里给的标签数量增减。

### 5. Entry header —— `##` 子标题用它

```html
<div class="entry" data-stick="1">
  <div class="entry-main"><div class="entry-title"><span class="org">{{org}}</span><span class="role">{{role}}</span><span class="badge">{{badge}}</span></div><span class="entry-date">{{date}}</span></div>
  <div class="entry-meta"><span>{{meta}}</span></div>
</div>
```

- `{{org}}` = `##` 标题 `|` 左侧；`{{role}}` = `|` 右侧；无 `|` 则 `{{role}}` 连 `<span class="role">` 删。
- `.badge`（可选）：头衔/职务徽标；无则删。
- `{{date}}` 来自 `##` 下 `date:` 行，无则删 `.entry-date`。
- `.entry-meta` 来自 `meta:` 行或 GPA/排名等，关键数字 `<b>`；无 meta 整个 div 删。
- 项目经历 → 三段式单行（见硬约束）：

  ```html
  <div class="entry" data-stick="1">
    <div class="entry-main">
      <span class="proj">{{项目名}}</span>
      <span class="company">{{公司/项目类型}}</span>
      <span class="entry-date">{{date}}</span>
    </div>
  </div>
  ```

### 6. Bullet（单条经历要点 — 独立原子，自由换页）

```html
<div class="bullet">{{text}}</div>
```

每条 `- bullet` 拆一个独立原子；STAR 法则、量化结果；数字用 `<span class="num">`，关键术语用 `<b>`。

### 7. Pubs（论文发表，可选）—— 论文模块用

```html
<ul class="pubs">
  <li><span class="tag">[C]</span> {{authors}} <b>{{title}}</b> <span class="ven">{{venue}}</span>, <span class="yr">{{year}}.</span></li>
</ul>
```

- `{{tag}}` 类型标：`[C]` 会议 / `[J]` 期刊 / `[W]` Workshop / `[P]` 专利（可选）。
- 本人名字用 `<span class="me">…</span>` 加下划线（可选）；共一/一作用括注。
- 每篇一个 `<li>`。

### 8. Awards（奖项，可选）—— 获奖模块用

```html
<div class="awards">
  <div class="award"><span class="yr">{{year}}</span><span>{{name}}</span><span class="lvl">{{level}}</span></div>
</div>
```

每项一个 `.award`；`{{level}}` = 国家级/省级/校级/金牌 等，无则删 `.lvl`。首格 `.yr` 默认放年份；竞赛/类别分组的用法在该格放竞赛或类别名（样式由主题 `<style>` 保证）。

### 9. Skills（类别 + 等级词文本行）

```html
<div class="skills">
  <div class="skills-row"><span class="cat">{{category}}</span><span class="tags"><b>精通 {{skill}}</b>（{{方向/细分}}）· <b>熟悉 {{skill}}</b> · 了解 {{skill}}</span></div>
</div>
```

- 每类一个 `.skills-row`；技能描述 = 等级词 + 技能名（括号补具体方向/细分），按等级从高到低；`<b>` 只加粗「等级词 + 技能名」。不使用标签/chip/进度条。
- 双列布局变体：容器 `.skills` 直接设两列 grid（样式差异见主题文件），行结构不变。
- 技术栈模块也用本组件（HTML 不变）；mono 字体、双列等视觉差异全部由主题 `<style>` 实现，前置与否由骨架决定。

## 简历骨架（装配顺序）

```
<header class="resume-header"> … </header>          ← 由 self-intro 装配（姓名/方向/联系方式/证件照）
（按简历 MD 里 # 模块的顺序，每个模块依次：）
  <div class="sec-head" data-stick="1"> … </div>     ← SectionHead（icon 按模块语义选）
  <该模块的正文组件>                                  ← Summary / Interests / Entry×N / Bullet×N / Pubs / Awards / Skills
```

- **模块顺序 = MD 里 `#` 出现的顺序**（self-intro 永远第一，渲染成 Header 而非 SectionHead）。
- 每个 `# 模块` 都先出 SectionHead，再出该模块的正文组件。
- `## 子标题`：Entry header 一条；`- bullet` 每条独立 `.bullet` 原子。
- 骨架顺序调整（技术栈前置、自我评价放末尾等）见各主题差异节。

## MD → 组件映射（基准）

| 简历 MD 元素 | 组件 | 备注 |
|------|------|------|
| `# self-intro`（首个，key:value） | Header（1.） | name/role/联系方式/photo → Header 各槽位；不渲染 SectionHead |
| `# 其它模块标题` | SectionHead（2.） | icon 按语义选；英文标签可选 |
| 模块下纯文本段 | Summary（3.） | 关键短语 `<b>` |
| 模块下「标签, 标签, 标签」单行 | Interests（4.） | 方向/兴趣标签 |
| `## org \| role` | Entry header（5.）org/role | `\|` 分割；无 `\|` 则只有 org |
| `## 项目名 \| 公司/项目类型` | Entry 三段式 proj/company | 无符号、无 `.role`；见组件 5. 示例 |
| `##` 下 `date: …` | Entry 的 `.entry-date` | |
| `##` 下 `meta: …` | Entry 的 `.entry-meta` | 关键数字 `<b>` |
| `##` 下 `- bullet` | 独立 Bullet（6.） | 每条一条；STAR + 量化；`.num` |
| 论文条目 | Pubs（7.） | 类型标/venue/年份/本人下划线（均可选） |
| 获奖条目 | Awards（8.） | 年/名/级别 |
| `类别: 精通 A（…）· 熟悉 B`（技能 / 技术栈） | Skills（9.）的 `.skills-row` | 等级词文本；技术栈前置与否由骨架决定 |

> `##` 下的描述段（项目说明）→ 渲染成主题差异节指定的描述段组件（如 `.summary`），作为独立原子放在 Entry 之后，不塞进 Entry。
