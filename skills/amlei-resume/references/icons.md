# SVG 图标库（所有主题共用）

> 简历模块标题（SectionHead）左侧的小图标。**全部 24×24、`fill="none" stroke="currentColor" stroke-width="1.6"` 描边风格**，靠 `color` 继承主题 `--accent`，所以换主题不用换图标。
>
> **怎么选**：按**模块的语义**（不是标题里的字）从下表挑一个；中英文关键词任一命中即用。拿不准就用末尾的默认图标 `star`。图标整段 `<svg class="ico" …>…</svg>` 原样贴进 SectionHead 的 `{{icon}}` 槽位。

## 图标 → 语义对照

| 语义 | 关键词（命中即用） | SVG（贴进 `<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">…</svg>` 的内部） |
|------|------|-----|
| 个人简介 / 自我介绍 | 简介 / 个人简介 / profile / about / summary / 自我评价 | `<circle cx="12" cy="8" r="3.4"/><path d="M5.5 19.5c0-3.3 2.9-6 6.5-6s6.5 2.7 6.5 6"/>` |
| 教育 / 学历 | 教育 / 学历 / education / 学校 / 学习 | `<path d="M2 9.5l10-4 10 4-10 4z"/><path d="M6 11.3v3.7c0 1.6 2.7 3 6 3s6-1.4 6-3v-3.7"/><path d="M22 9.5v4"/>` |
| 实习 / 工作 / 经历 | 实习 / 工作 / 职业 / 经历 / experience / intern / career / work | `<rect x="3" y="7.5" width="18" height="12.5" rx="1.6"/><path d="M9 7.5V6a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v1.5"/><path d="M3 12.5h18"/>` |
| 科研 / 研究 | 科研 / 研究 / research / 课题 | `<path d="M9 3.5h6"/><path d="M10 3.5v5.5L5.5 17a2 2 0 0 0 1.8 3h9.4a2 2 0 0 0 1.8-3L14 9V3.5"/><path d="M7.8 14h8.4"/>` |
| 项目 / 工程 | 项目 / 工程 / project / 开源 | `<path d="M8.5 7.5l-4.5 4.5 4.5 4.5"/><path d="M15.5 7.5l4.5 4.5-4.5 4.5"/>` |
| 技能 / 技术栈 | 技能 / 技术栈 / 技术 / skill / stack / tech | `<circle cx="12" cy="12" r="3"/><path d="M12 2.5v2.5M12 19v2.5M21.5 12H19M5 12H2.5M18.3 5.7l-1.7 1.7M7.4 16.6l-1.7 1.7M18.3 18.3l-1.7-1.7M7.4 7.4 5.7 5.7"/>` |
| 论文 / 发表 | 论文 / 发表 / 著作 / publication / paper | `<path d="M6.5 3.5h7l4 4v13a1 1 0 0 1-1 1H6.5a1 1 0 0 1-1-1V4.5a1 1 0 0 1 1-1z"/><path d="M13 3.5v4h4"/><path d="M8 13h8M8 16.5h5"/>` |
| 获奖 / 荣誉 | 获奖 / 荣誉 / 奖学金 / award / honor | `<circle cx="12" cy="9" r="5"/><path d="M9 13.5l-2.2 6.5 5.2-3 5.2 3-2.2-6.5"/>` |
| 证书 / 资质 | 证书 / 资格 / 资质 / certificate / cert / 执业 | `<circle cx="12" cy="9" r="5"/><path d="M8.5 13l-1.5 6 5-2.2 5 2.2-1.5-6"/>` |
| 兴趣 / 方向 | 兴趣 / 研究方向 / 爱好 / interest | `<path d="M9 18h6"/><path d="M10 21h4"/><path d="M12 3a6 6 0 0 0-4 10.5c.8.8 1.3 1.8 1.5 3h5c.2-1.2.7-2.2 1.5-3A6 6 0 0 0 12 3z"/>` |
| 自我评价（引号） | 自我评价 / 评价 / 寄语 | `<path d="M7 7h4v6c0 2-1.5 3.5-4 4M13 7h4v6c0 2-1.5 3.5-4 4"/>` |
| 默认（无匹配） | —— | `<path d="M12 3l2.6 5.6 6.1.7-4.5 4.2 1.2 6L12 16.8 6.6 19.5l1.2-6L3.3 9.3l6.1-.7z"/>` |

## 证件照占位图标（Header 用，无真实头像时）

贴进 Header 的 `{{photo}}` 槽位（不带真实照片时）：

```html
<div class="photo" aria-label="证件照占位">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8.5" r="3.5"/><path d="M5 20c0-3.6 3.1-6 7-6s7 2.4 7 6"/></svg>
  <span>证件照</span>
</div>
```

> 有真实头像时改成 `<div class="photo"><img src="{{avatar}}" alt="证件照"></div>`（路径来自 `self-intro` 的 `avatar:` 字段）。
