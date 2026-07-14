<p align="center">
  <img src="https://em-content.zobj.net/source/apple/391/artist-palette_1f3a8.png" width="100" />
</p>

<h1 align="center">🎨 Text to Icons</h1>

<p align="center">
  <strong>Turn text descriptions into uniform linear SVG icons — one-click copy to PPT / Figma / docs</strong>
</p>

<p align="center">
  <a href="https://github.com/xuhuai713/text-to-icons-skill/stargazers"><img src="https://img.shields.io/github/stars/xuhuai713/text-to-icons-skill?style=flat&color=yellow" alt="Stars"></a>
  <a href="https://github.com/xuhuai713/text-to-icons-skill/commits/main"><img src="https://img.shields.io/github/last-commit/xuhuai713/text-to-icons-skill?style=flat" alt="Last Commit"></a>
  <a href="https://github.com/xuhuai713/text-to-icons-skill/blob/main/LICENSE"><img src="https://img.shields.io/github/license/xuhuai713/text-to-icons-skill?style=flat" alt="License"></a>
</p>

<p align="center">
  <a href="#-the-problem">The Problem</a> •
  <a href="#-the-solution">The Solution</a> •
  <a href="#%EF%B8%8F-quickstart">Quickstart</a> •
  <a href="#-comparison">Comparison</a> •
  <a href="#%EF%B8%8F-features">Features</a> •
  <a href="#-examples">Examples</a>
</p>

---

## 🧨 The Problem

> **The most annoying thing about adding icons to PPT / articles / docs isn't finding them — it's making them look consistent.**

- Feather uses 1.5px stroke, IconPark uses 4px — put them side by side and it looks sloppy
- Different icon libraries have different viewBox sizes — visual centers are all over the place
- After painstaking alignment, pasting into PPT changes the size — adjust it all over again
- Search across libraries → manually align stroke widths → copy one by one → tweak sizes… **20 minutes wasted for 10 icons**

---

## ✅ The Solution

**text-to-icons** is an AI Skill. You type a few keywords, it does the rest:

<table>
<tr>
<td width="50%">

### Input
> lead mining, opportunity insight, customer visit, marketing recommendation, proposal pricing

</td>
<td width="50%">

### Output
An interactive HTML page with **6 uniform linear icons** per entry. One-click "Copy SVG" — paste and go.

</td>
</tr>
</table>

**Every icon shares the same spec:**
- ✅ 24×24 viewBox — identical visual size
- ✅ 0.5pt stroke — uniform weight regardless of source
- ✅ `stroke-linecap="round"` — professional round endpoints
- ✅ Copied SVG includes `width="24pt" height="24pt"` — perfect PPT fit on paste

---

## ⚡ Quickstart

### Install

In any Skill-compatible Agent:

```bash
# Claude Code / Codex / Cursor / WorkBuddy etc.
npx skills@latest add xuhuai713/text-to-icons-skill
```

Or manually:

```bash
git clone https://github.com/xuhuai713/text-to-icons-skill.git
cp -r text-to-icons-skill/text-to-icons ~/.workbuddy/skills/
```

### Trigger

Just say:

```
convert this text to icons: telecom, finance, healthcare, government
turn these steps into icons: register, login, pay, use
把这些内容转成图标：搜索 资料 设置 退出
```

---

## 📊 Comparison

| Scenario | Manual | With This Skill |
|----------|--------|----------------|
| Search 6 icons × 4 libraries | Open 4 tabs, search one by one | One sentence input |
| Unify stroke widths (1.5px vs 4px) | Manually edit each SVG | Auto-unified to 0.5pt |
| Unify viewBox sizes | Edit each SVG's viewBox | Auto-scaled |
| Copy to PPT/design tools | Export PNG or copy individually | One-click "Copy SVG" with size attrs |
| Total time (10 entries) | ~20 min | ~1 min |

---

## 🖼️ How It Looks

```
┌──────────────────────────────────────────────────┐
│                                                  │
│  Lead Mining                                     │
│  🔍 [Copy]  📈 [Copy]  🎯 [Copy]                │
│  🔎 [Copy]  📡 [Copy]  📋 [Copy]                │
│                                                  │
│  Opportunity Insight                             │
│  💼 [Copy]  👁️ [Copy]  📊 [Copy]                │
│  💡 [Copy]  📈 [Copy]  🎯 [Copy]                │
│                                                  │
│  ... more entries ...                           │
│                                                  │
└──────────────────────────────────────────────────┘
```

> Each icon has an independent "Copy SVG" button. Click, paste, done.

---

## ⚙️ Features

| Feature | Description |
|---------|-------------|
| **4-library mixing** | Auto-matches icons from Feather · Lucide · IconPark · Huge Icons |
| **Uniform style** | 24×24 viewBox + 0.5pt stroke, regardless of source library |
| **One-click copy** | Native JS clipboard API, copied SVG includes full size attributes |
| **Interactive page** | Single self-contained HTML, Tailwind CSS, open in any browser |
| **IconPark conversion** | 48×48 3-color fill → 24×24 linear stroke, with fill→stroke auto-conversion |
| **Source badge** | Each icon card shows its library origin (Feather / IconPark etc.) |

---

## 💡 Examples

### Scenario 1: PPT icons for a process flow

```
Turn these 5 steps into icons: market research, product design, dev & test, launch, data review
```

→ Generates HTML → click "Copy SVG" on each → paste into PPT

### Scenario 2: Feature module icons

```
Match these modules with icons: user management, permissions, reports, notifications, settings
```

→ Auto-matches best icons from multiple libraries → uniform style

### Scenario 3: Industry solution icons

```
Convert these industries into icons: finance, healthcare, education, retail, manufacturing, energy
```

→ 6 semantically relevant icons per industry, ready for solution decks

---

## 🧠 Technical Details

- **Icon sources**: Feather (MIT) · Lucide (ISC) · IconPark (Apache 2.0) · Huge Icons (MIT)
- **Output format**: Single HTML file, Tailwind CSS CDN, zero external dependencies
- **IconPark scaling**: 48×48 → `<g transform="scale(0.5)" stroke-width="1">` → 24×24
- **Copy mechanism**: `XMLSerializer().serializeToString()` → `navigator.clipboard.writeText()`
- **Stroke control**: All sources unified to `stroke-width="0.5"`, explicitly written on copy

> Detailed skill specification: [SKILL.md](text-to-icons/SKILL.md)

---

## 📚 Resources

- [Full Skill Documentation](text-to-icons/SKILL.md) — Complete rules the AI reads at runtime
- [Icon Reference Catalog](text-to-icons/references/icon-sources.md) — Path data organized by semantic category

---

## 📄 License

MIT

---

<p align="center">
  <sub>
    Tired of inconsistent icon styles? This Skill solves it in one shot.<br/>
    ⭐ Star this repo to help others find it.
  </sub>
</p>
