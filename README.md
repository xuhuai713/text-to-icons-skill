# 🎨 Text to Icons

#### 把文本描述转成风格统一的线性 SVG 图标，一键复制到 PPT / 设计工具

输入几个行业名称或概念关键词，AI 自动从 **Feather · Lucide · IconPark · Iconoir** 四个开源图标库中匹配 6 个语义对应的线性图标，排版为交互式 HTML 页面，每个图标带一键 "复制 SVG" 按钮，粘贴到 PPT / Figma 等工具尺寸描边完全一致。

---

## 📋 目录

| 名字 | 一句话 |
|------|--------|
| 🎨 **text-to-icons** | 把概念/步骤/关键词转成风格统一的线性图标，支持四库混编、一键复制 SVG 到 PPT |

---

## 📦 安装方式

在 Claude Code、Codex、Cursor 等支持 Skill 的 Agent 里，直接说：

```
帮我安装这个 skill：https://github.com/xuhuai713/text-to-icons-skill/tree/main/text-to-icons
```

Agent 会自己 clone 到对应目录。或手动安装：

```bash
# 克隆到 WorkBuddy skills 目录
git clone https://github.com/xuhuai713/text-to-icons-skill.git
cp -r text-to-icons-skill/text-to-icons ~/.workbuddy/skills/
```

---

## ✨ Skill

### 🎨 text-to-icons

> _"PPT 里图标风格统一这件事，以前靠手动搜然后手动调描边对齐。现在一句话搞定。"_

输入几个文本条目（行业名称、步骤环节、功能模块等），AI 会自动：

1. **匹配图标** — 每个条目从 Feather、Lucide、IconPark、Iconoir 四个库中挑选 6 个语义匹配的线性图标
2. **统一风格** — 所有图标统一 24×24 viewBox、0.5pt 描边，无论原始来自哪个库
3. **生成页面** — 输出一个交互式 HTML，每个图标都附带「复制 SVG」按钮
4. **一键复制** — 复制出的 SVG 包含 `width="24pt" height="24pt"`，粘贴到 PPT 中尺寸和描边完全一致

**IconPark 转换规则**

IconPark 原始数据使用 48×48 viewBox + 三色填充模式。转换为线性风格时：

- **提取所有元素类型** — 不只搜 `<path>` 的 `d=`，还要提取 `<rect>` 和 `<circle>` 标签
- **fill → stroke 转换** — 图纸中的 `colors[1]`（主体填充）和 `colors[2]`（装饰填充）全部转为 `fill="none" stroke="#000000"`
- **填充型路径替换** — 面部嘴部等依赖 fill 渲染的复杂路径，替换为等效的贝塞尔描边曲线

**怎么触发**

```
把这些内容转成图标：电信 金融 健康 政务
给这几个步骤配上图标：注册 登录 付费 使用
convert this text to icons: search, profile, settings, logout
```

→ [SKILL.md](text-to-icons/SKILL.md)

---

## ⚙️ 技术细节

- **图标库**：Feather (MIT) · Lucide (ISC) · IconPark (Apache 2.0) · Iconoir (MIT)
- **格式**：24×24 viewBox · 0.5pt 描边 · `stroke-linecap="round"` · `stroke-linejoin="round"`
- **输出**：单 HTML 文件 · Tailwind CSS CDN · 原生 JS 剪贴板 API
- **IconPark 缩放**：48×48 → `<g transform="scale(0.5)" stroke-width="1">` → 24×24

---

## 🌟 关于

日常给 PPT / 文章配图标时，图标风格不统一是最烦人的事。这个 skill 自动帮你搞定库间混编、描边统一、复制粘贴的全流程。

有问题或建议，欢迎在 Issues 里说一声。

---

## License

MIT
