# 🎨 Text to Icons

#### Convert text descriptions into uniform linear SVG icons, one-click copy to PPT / design tools

Input a few industry names or concept keywords, and the AI automatically matches **6 semantically relevant linear icons** from **Feather · Lucide · IconPark · Iconoir** — four open-source icon libraries — laid out in an interactive HTML page. Each icon has a one-click "Copy SVG" button. Paste into PPT / Figma with consistent size and stroke weight.

---

## 📋 Index

| Name | Description |
|------|-------------|
| 🎨 **text-to-icons** | Convert concepts/steps/keywords into uniform linear icons, supports 4-library mixing, one-click SVG copy to PPT |

---

## 📦 Installation

In Agent supporting Skills (Claude Code, Codex, Cursor, etc.), just say:

```
Install this skill: https://github.com/xuhuai713/text-to-icons-skill/tree/main/text-to-icons
```

The Agent will clone it automatically. Or install manually:

```bash
git clone https://github.com/xuhuai713/text-to-icons-skill.git
cp -r text-to-icons-skill/text-to-icons ~/.workbuddy/skills/
```

---

## ✨ Skill

### 🎨 text-to-icons

> _"Keeping icon styles consistent in PPT used to mean manually searching and manually aligning stroke widths. Now it's one sentence."_

Input a few text items (industry names, process steps, feature modules, etc.), and the AI will:

1. **Match icons** — For each item, pick 6 semantically matching linear icons from Feather, Lucide, IconPark, and Iconoir
2. **Unify styles** — All icons use uniform 24×24 viewBox, 0.5pt stroke, regardless of source library
3. **Generate page** — Output an interactive HTML with "Copy SVG" buttons on every icon
4. **One-click copy** — Copied SVGs include `width="24pt" height="24pt"` — paste into PPT with perfect size and stroke consistency

**How to trigger**

```
把这些内容转成图标：电信 金融 健康 政务
给这几个步骤配上图标：注册 登录 付费 使用
convert this text to icons: search, profile, settings, logout
```

→ [SKILL.md](text-to-icons/SKILL.md)

---

## ⚙️ Technical Details

- **Libraries**: Feather (MIT) · Lucide (ISC) · IconPark (Apache 2.0) · Iconoir (MIT)
- **Format**: 24×24 viewBox · 0.5pt stroke · `stroke-linecap="round"` · `stroke-linejoin="round"`
- **Output**: Single HTML file · Tailwind CSS CDN · Native JS clipboard API
- **IconPark scaling**: 48×48 → `<g transform="scale(0.5)" stroke-width="1">` → 24×24

---

## 🌟 About

The most annoying thing about creating icons for PPT / articles is keeping the style consistent across different sources. This skill automates cross-library mixing, stroke unification, and the copy-paste workflow end to end.

Feedback and suggestions welcome in Issues.

---

## License

MIT
