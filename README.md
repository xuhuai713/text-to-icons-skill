<p align="center">
  <img src="https://em-content.zobj.net/source/apple/391/artist-palette_1f3a8.png" width="100" />
</p>

<h1 align="center">🎨 Text to Icons</h1>

<p align="center">
  <strong>从文本描述到统一风格的线性图标，一键复制到 PPT / Figma / 飞书文档</strong>
</p>

<p align="center">
  <a href="https://github.com/xuhuai713/text-to-icons-skill/stargazers"><img src="https://img.shields.io/github/stars/xuhuai713/text-to-icons-skill?style=flat&color=yellow" alt="Stars"></a>
  <a href="https://github.com/xuhuai713/text-to-icons-skill/commits/main"><img src="https://img.shields.io/github/last-commit/xuhuai713/text-to-icons-skill?style=flat" alt="Last Commit"></a>
  <a href="https://github.com/xuhuai713/text-to-icons-skill/blob/main/LICENSE"><img src="https://img.shields.io/github/license/xuhuai713/text-to-icons-skill?style=flat" alt="License"></a>
</p>

<p align="center">
  <a href="#-问题">问题</a> •
  <a href="#-解决方案">解决方案</a> •
  <a href="#-快速上手">快速上手</a> •
  <a href="#-对比">对比</a> •
  <a href="#%EF%B8%8F-功能特性">功能特性</a> •
  <a href="#-使用示例">使用示例</a>
</p>

---

## 🧨 问题

> **给 PPT / 文章 / 飞书文档配图标时，最烦人的不是找不到图标，而是找齐了之后风格不统一。**

- Feather 的描边是 1.5px，IconPark 是 4px，放在一起粗细参差不齐
- 同一个页面里图标 viewBox 大小不一，视觉重心东倒西歪
- 好不容易排好版，复制到 PPT 里尺寸又变了，重新调半天
- 从不同库搜图 → 手动对齐描边 → 逐个复制 → 微调尺寸……**一次 10 个图标就要浪费 20 分钟**

---

## ✅ 解决方案

**text-to-icons** 是一个 AI Skill，你只需要输入几个关键词，它自动完成：

<table>
<tr>
<td width="50%">

### 输入
> 线索挖掘，商机洞察，客户拜访，营销推荐，方案报价

</td>
<td width="50%">

### 输出
一个交互式 HTML 页面，每个条目 **6 个风格统一的线性图标**，一键「复制 SVG」直接粘贴到目标工具

</td>
</tr>
</table>

**所有图标统一规格：**
- ✅ 24×24 viewBox — 视觉大小完全一致
- ✅ 0.5pt 描边 — 粗细均匀，不分来源
- ✅ `stroke-linecap="round"` — 圆角端点，专业质感
- ✅ 复制出的 SVG 含 `width="24pt" height="24pt"` — 粘贴到 PPT 尺寸自动匹配

---

## ⚡ 快速上手

### 安装

支持 AI Skill 的 Agent 中直接运行：

```bash
# Claude Code / Codex / Cursor / WorkBuddy 等
npx skills@latest add xuhuai713/text-to-icons-skill
```

或手动安装：

```bash
git clone https://github.com/xuhuai713/text-to-icons-skill.git
cp -r text-to-icons-skill/text-to-icons ~/.workbuddy/skills/
```

### 触发

在对话中输入任意以下指令：

```
把这些内容转成图标：电信 金融 健康 政务
给这几个步骤配上图标：注册 登录 付费 使用
convert this text to icons: search, profile, settings, logout
```

---

## 📊 对比

| 场景 | 手动操作 | 使用本 Skill |
|------|---------|------------|
| 从 4 个图标库各搜 6 个图标 | 逐个搜索，反复切换页面 | 一句话输入关键词 |
| 统一描边（Feather 1.5px vs IconPark 4px） | 手动调整每条 SVG | 自动统一为 0.5pt |
| 统一 viewBox | 手动改写每个 SVG 的 viewBox | 自动缩放处理 |
| 复制到 PPT | 导出 PNG / 逐个复制 | 一键「复制 SVG」，含尺寸属性 |
| 总耗时（10 个条目） | ~20 分钟 | ~1 分钟（含生成+确认时间） |

---

## 🖼️ 真实输出效果

```
┌──────────────────────────────────────────────────┐
│                                                  │
│  线索挖掘                                        │
│  🔍 [复制]  📈 [复制]  🎯 [复制]                  │
│  🔎 [复制]  📡 [复制]  📋 [复制]                  │
│                                                  │
│  商机洞察                                        │
│  💼 [复制]  👁️ [复制]  📊 [复制]                  │
│  💡 [复制]  📈 [复制]  🎯 [复制]                  │
│                                                  │
│  ... 更多条目 ...                                │
│                                                  │
└──────────────────────────────────────────────────┘
```

> 每个图标独立「复制 SVG」按钮，点击即复制完整 SVG 代码，粘贴即用。

---

## ⚙️ 功能特性

| 特性 | 说明 |
|------|------|
| **多库混编** | 从 IconPark · Feather · Lucide · Huge Icons 四大库按优先级自动匹配语义对应的图标 |
| **风格统一** | 无论来源，统一 24×24 viewBox + 0.5pt 描边 |
| **本地缓存优先** | 随包附带 `icon-cache.json`（全量图标 inner-SVG），生成时本地读取，无需联网，秒级出图 |
| **一键复制** | 原生 JS 剪贴板 API，复制结果含完整尺寸属性 |
| **交互式页面** | 单 HTML 文件输出，Tailwind CSS 渲染，浏览器直接打开 |
| **IconPark 转换** | 48×48 三色填充 → 24×24 线性描边，含 fill→stroke 自动转换 |
| **来源标注** | 每个图标卡片标注来源库（IconPark / Feather 等），透明度高 |

---

## 💡 使用示例

### 场景 1：PPT 图标配图

```
给这 5 个流程步骤配上图标：市场调研 产品设计 开发测试 上线发布 数据复盘
```

→ 生成 HTML 页面 → 逐个点击「复制 SVG」→ 粘贴到 PPT

### 场景 2：产品功能图标

```
给这几个功能模块配图标：用户管理 权限控制 数据报表 消息通知 系统设置
```

→ 自动从多个库匹配最合适的图标 → 风格统一

### 场景 3：行业方案图标

```
把以下行业转成图标：金融 医疗 教育 零售 制造 能源
```

→ 每个行业 6 个语义关联图标，用于方案封面或展示页

---

## 🧠 技术内幕

- **图标源**：IconPark (Apache 2.0) · Feather (MIT) · Lucide (ISC) · Huge Icons (MIT)
- **本地缓存**：`assets/icon-cache.json` 预置全量图标 inner-SVG，`scripts/precache.py` 可刷新
- **输出格式**：单 HTML 文件，Tailwind CSS CDN，零外部依赖
- **IconPark 缩放**：48×48 → `<g transform="scale(0.5)" stroke-width="3">` → 24×24（显示有效描边 1.5）
- **复制实现**：`XMLSerializer().serializeToString()` → `navigator.clipboard.writeText()`
- **描边控制**：所有来源统一 `stroke-width="0.5"`，复制时明确写入

> 详细的 Skill 指令规范参见 [SKILL.md](text-to-icons/SKILL.md)

---

## 📚 相关资源

- [Skill 完整文档](text-to-icons/SKILL.md) — AI 执行时读取的完整规则
- [图标参考目录](text-to-icons/references/icon-sources.md) — 按语义分类的图标路径数据

---

## 📄 License

MIT

---

<p align="center">
  <sub>
    日常配图标最烦风格不统一？这个 Skill 帮你一次搞定。<br/>
    Star ⭐ 让更多人知道。
  </sub>
</p>
