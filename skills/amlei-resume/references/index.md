# References 索引

这是 AI 读取 references 的唯一入口。**先判断当前任务，再打开需要的文件；不要一次读完所有 reference。**

## 任务 → 读取顺序

| 任务 | 读取顺序 |
|------|----------|
| 首次确认目标岗位 / 换岗 / 目标范围变化 | `job-research.md` → `screening.md` → `content-packaging.md` → `resume-format.md`；需要落盘时再读 `file.md` |
| 岗位不变，只整理或改写现有简历 | `screening.md` → `content-packaging.md` → `resume-format.md`；需要落盘时再读 `file.md` |
| 第一次建立或整理 `profile.md` | `profile.md`（模板） |
| 归档素材、迁移目录、清理重复材料 | `file.md` |
| 导出 PDF / HTML | `export.md` → `themes/theme-index.md` → 选定主题文件 + `themes/component-library.md` → 需要图标时 `icons.md` |
| 单独查询岗位、行业、公司或市场行情 | `job-research.md` |
| 新增主题 | `themes/theme-index.md` → 选定主题文件 → `themes/component-library.md` |

## 文件清单

| 文件 | 用途 | 什么时候读 |
|------|------|------------|
| `index.md` | 本索引 | 每次需要 reference 时先读 |
| `screening.md` | 招聘方初筛字段、ATS 与页面注意力研究 | 选材、定模块顺序前 |
| `content-packaging.md` | 面向目标岗位的内容包装、程度校准与事实边界 | 选好证据、开始表达前 |
| `resume-format.md` | `简历.md` 的 DSL、模块顺序、字段与格式易错点 | 写或改简历前 |
| `sample-resume.md` | 简历 DSL 的完整示例 | 需要对照写法时 |
| `file.md` | `.amlei-skill/resume/` 的目录、命名、材料池、隐私与迁移规则 | 落盘、归档、迁移前 |
| `profile.md` | `profile.md` 的内容模板与熟练度四档 | 建立或整理画像时 |
| `export.md` | A4 预览、HTML 装配、分页检查与导出流程 | 导出 PDF / HTML 时 |
| `job-research.md` | JD 收集、岗位分层、行业/公司差异、薪酬与简历映射 | 定位岗位或核对市场依据时 |
| `icons.md` | 图标与无照片头像占位 SVG | 装配 HTML 且需要占位图时 |
| `themes/theme-index.md` | 六套主题的定位、选择规则与新增流程 | 选主题或加主题时 |
| `themes/component-library.md` | 主题组件、占位符与装配基准 | 装配 HTML 时 |
| `themes/theme-academic.md` | 学术 / 科研主题的字段映射 | 选中该主题时 |
| `themes/theme-content-green.md` | 内容运营主题的字段映射 | 选中该主题时 |
| `themes/theme-english-mnc.md` | 外企 / 英文主题的字段映射 | 选中该主题时 |
| `themes/theme-sidebar-creative.md` | 侧栏创意主题的字段映射 | 选中该主题时 |
| `themes/theme-soe-formal.md` | 国企 / 正式主题的字段映射 | 选中该主题时 |
| `themes/theme-tech-dense.md` | 技术密排主题的字段映射 | 选中该主题时 |

## 维护规则

- 新增、删除或重命名 reference 时，同步更新本索引。
- `SKILL.md` 只指向本索引，不逐条列出 reference。
- 本索引只写“读什么、何时读”，不复制各文件的正文。
