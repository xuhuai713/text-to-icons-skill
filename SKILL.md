---
name: text-to-icons
description: "Convert user-provided text into matching linear icons. Output is a single self-contained HTML file using a data-driven template (icons-template.html). All icon data lives in the ICON_GROUPS JS array; the template renders cards dynamically. Uniform 24×24 viewBox, 0.5pt stroke for both display and clipboard. Core source: IconPark (Apache 2.0). Additional sources: Feather/MIT, Lucide/ISC, Phosphor/MIT, Iconoir/MIT, Huge Icons/MIT."
agent_created: true
---

# Text to Icons — 文本转图标

## Overview

This skill transforms structured text (process steps, feature lists, categories, slide titles) into matching linear/outline icons and renders them as a single self-contained HTML file. Each text item maps to **6 matching icons** drawn from a curated set of free, commercially-usable icon libraries. The HTML includes one-click "Copy SVG" buttons.

## 🔑 Critical Quality Rules — MUST FOLLOW

Every icon in the output MUST pass ALL these checks:

1. **Instantly recognizable** — The average person understands the icon within 1 second. No squinting required.
2. **No abstract metaphors** — Only universally understood visual symbols: magnifying glass = search (good); abstract curves labeled "handshake" (bad — looks like random squiggles).
3. **Must decode without labels** — Remove the text label; the icon should still be obvious.
4. **Vet SVG paths** — Before including any icon, mentally trace the paths to confirm they actually draw the intended shape.
5. **No repetitions** — Within the same group's 6 icons, avoid visually similar variants. Also avoid reusing the same icon across different groups more than 2 times.
6. **Path density check** — Max 6 path elements (paths/lines/circles/rects/polylines) unless every element is clearly distinguishable at 28×28px.
7. **Shape integrity check** — Reject squashed circles, mismatched corners, disconnected lines, unintentional overlapping (杂糅).
8. **Visual weight balance** — Strokes must be evenly distributed across the 24×24 viewBox. Reject icons where >70% of strokes cram into one corner.

## When to Use

- User provides steps, stages, phases (business process flow, product roadmap, project lifecycle)
- User provides feature names, module names, category labels needing matching icons
- User says "帮我把这些内容转成图标" / "给这些步骤配上图标" / "convert this text to icons"
- User wants copyable SVG icons for design tools or frontend projects
- User requests linear/outline icons with consistent stroke style

## Icon Source Reference

Always load `references/icon-sources.md` into context. It contains the full catalog organized by semantic category with SVG path data for rapid lookup without external fetching.

Six active sources. Distribute selections across at least 3 libraries per group, prefer 2-3 from IconPark, 2-3 from Feather/Lucide, and 1-2 from the remaining sources:

| Source | License | Icons | viewBox | Default Stroke | Fetch Method |
|--------|---------|-------|---------|----------------|--------------|
| **IconPark** ⭐ (core) | Apache 2.0 | 2600+ | 48×48 | 4 | `unpkg.com/@icon-park/svg@1.4.2/es/icons/<PascalCase>.js`; scale(0.5), strip stroke-width |
| **Feather Icons** | MIT | 286 | 24×24 | 1.5 | Reference catalog in `icon-sources.md` |
| **Lucide Icons** | ISC | 1400+ | 24×24 | 2 | `unpkg.com/lucide-static@latest/icons/<kebab-name>.svg`; strip stroke-width="2" |
| **Phosphor Icons** | MIT | 9000+ | 24×24 | 1.5 | Reference catalog in `icon-sources.md` |
| **Iconoir** | MIT | 1600+ | 24×24 | 1.5 | `cdn.jsdelivr.net/npm/iconoir@7.11.0/icons/regular/<kebab-name>.svg`; convert currentColor→#000000 |
| **Huge Icons** (free) | MIT | 5400+ | 24×24 | 1.5 | `cdn.jsdelivr.net/npm/@hugeicons/core-free-icons@4.2.2/dist/esm/<PascalCase>Icon.js`; read as tuple array, convert to inner SVG paths |

## Workflow

### Step 1: Parse the Input

Extract all discrete items from the user's text. Separators: newlines, numbered/bulleted lists, commas, table rows. Preserve original order. Output a numbered list for user confirmation.

### Step 2: Map Each Item to 6 Matching Icons

For each item, painstakingly hand-pick 6 icons that pass ALL 8 quality rules. This is the most critical step.

**Icon selection process:**
1. Identify the core concept (e.g., "线索挖掘" = search/discovery)
2. Look up the reference catalog; mentally verify each candidate
3. Reject any icon whose meaning is not instantly clear
4. Select exactly 6 icons with DISTINCT visual forms
5. Distribute across at least 3 libraries (prefer 2-3 IconPark, 2-3 Feather/Lucide, 1-2 from others)

**Selection quality benchmarks:**

| Category | GOOD (instantly recognizable) | BAD (REJECT) |
|----------|-------------------------------|--------------|
| Search / Discovery | magnifying glass, compass, binoculars | abstract circles, squiggly lines |
| Data / Analysis | bar chart, line chart, pie chart, eye | brain, abstract geometry |
| People / User / Visit | single person, two people, door, phone | abstract "handshake" curves |
| Marketing / Promotion | megaphone, trophy, star, gift, thumbs-up | abstract badges |
| Price / Money / Quotation | dollar sign, coins, credit card, tag, wallet | abstract symbols |
| Contract / Document / Sign | file text, pen, clipboard, folder, book | ambiguous scroll shapes |
| Project / Task / Implement | clipboard check, flag, layers, target, check circle | abstract branching lines |
| Product / Config / Setup | box, gear, wrench, sliders, grid | abstract lattice |
| Activation / Launch | zap, play, power, plus, rocket | ambiguous arrows |
| Billing / Invoice | monitor, printer, bar chart, receipt | abstract file shapes |
| Settlement / Cart | shopping cart, check, x mark, trash, ban | complex checkout flows |
| Completion / Done | check circle, award, archive, smile | ambiguous checkmarks |
| Service / Maintenance | wrench, tool, terminal, code | abstract gear-only |
| Risk / Security / Audit | shield, lock, warning, alert | abstract polygons |
| Training / Learning | book open, graduation cap, presentation | abstract head shapes |

For each item, pick 6 icons covering distinct visual forms:
- **Literal symbols** (2-3): The most direct, obvious representation
- **Action/outcome** (2): Something related to the action or result
- **Tool/related object** (1-2): A commonly associated tool

**CRITICAL: Before finalizing any icon, mentally trace its SVG paths.** Confirm the paths actually draw what is intended.

### Step 3: Fetch SVG Paths from Icon Sources

For each icon needed, fetch SVG path data from the appropriate source.

#### A) IconPark (Core Source — Apache 2.0, 48×48 → 24×24 scaled)

```bash
curl -sL "https://unpkg.com/@icon-park/svg@1.4.2/es/icons/<PascalCaseName>.js"
```

- Names are PascalCase (e.g., `ProcessLine`, `DataServer`, `CodeComputer`)
- Search: `grep -i '<keyword>'` on the icons directory listing fetched via curl

**Conversion from 48×48 JS module to inner SVG paths:**

The JS module exports a tuple array: `[elementType, attributes][]`.

```javascript
// Example: ProcessLine icon module content
const ProcessLine = [
  ["rect", { fill: "colors[1]", stroke: "colors[0]", strokeWidth: 4, ... }],
  ["path", { fill: "colors[2]", ... }],
  // ...
];
```

**Rules for conversion (MUST follow exactly):**

1. **Extract ALL element types** — not just `<path>`. The JS module contains `<rect>`, `<circle>`, `<path>`, `<polyline>`, `<line>`. Read the full module and enumerate all elements manually.

2. **Every element MUST have `fill="none"` explicitly** — Three color slots to convert:
   - `colors[0]` → stroke color (convert to `#000000`)
   - `colors[1]` → primary fill (set `fill="none" stroke="#000000"`)
   - `colors[2]` → secondary fill (set `fill="none" stroke="#000000"`)

3. **Wrap in `<g transform="scale(0.5)">`** — Put the 48×48 paths inside a group with `transform="scale(0.5)"` for 24×24 viewBox compatibility.

4. **⚠️ CRITICAL: Strip ALL `stroke-width` from child elements** — IconPark children have `stroke-width="4"`. Remove with regex:
   ```python
   inner = re.sub(r'\s+stroke-width="\d+"', '', inner)
   ```
   After stripping, children inherit `stroke-width="1"` from the `<g>` wrapper. With `scale(0.5)`, effective stroke = 0.5 units, matching Feather/Lucide.

5. **Fill-dependent complex paths MUST be replaced** — Some paths (facial features, smile arcs, filled shapes) produce garbled thin lines when `fill="none"`. Detection criteria:
   - Path uses `V` (vertical-to) and `Z` (close) commands referencing unrelated coordinates
   - Multiple disjoint subpaths forming a fill-only shape
   - **Fix**: Replace with a simple bezier curve:
     ```html
     <!-- WRONG: fill-dependent smile -->
     <path d="M20 32C18.8954 32 18 32.8954 18 34C18 35.1046...Z"/>
     <!-- RIGHT: stroke-only smile -->
     <path d="M17 34C20 37 28 37 31 34"/>
     ```

6. **Pre-verification**: Before adding any IconPark icon, trace EACH element. The safest approach: read the full JS source (curl without grep filter) and manually list all SVG elements before writing the HTML.

**Final format for the `paths` field in ICON_GROUPS:**
```javascript
{ paths: '<g transform="scale(0.5)"><path d="..."/><circle cx="..." r="..."/></g>', source: "IconPark" }
```

#### B) Feather Icons (MIT, 24×24, stroke=1.5)

Use the reference catalog in `icon-sources.md`. Feather paths are directly usable as-is.

**Final format:**
```javascript
{ paths: '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>', source: "Feather" }
```

#### C) Lucide Icons (ISC, 24×24, stroke=2)

```bash
curl -sL "https://unpkg.com/lucide-static@latest/icons/<kebab-name>.svg"
```

- Names are kebab-case (e.g., `search.svg`, `user-circle.svg`, `file-text.svg`)
- Default SVG: viewBox="0 0 24 24", stroke-width="2"
- Search available icon names: `curl -sL "https://unpkg.com/lucide-static@latest/" | grep -o 'icons/[a-z-]*\.svg' | sort -u`

**Conversion required:**
1. Read the raw SVG file
2. Extract inner elements (<path>, <circle>, <rect>, <line>, <polyline>, <polygon>)
3. **Strip `stroke-width="2"` from child elements** — Let the template's wrapper SVG (`stroke-width="1.5"`) control the stroke. The clipboard copy function will use the correct 0.5pt.

```python
# Strip explicit stroke-width from Lucide children
inner = re.sub(r'\s+stroke-width="2"', '', inner)
```

**Final format:**
```javascript
{ paths: '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.34-4.34"/>', source: "Lucide" }
```

#### D) Phosphor Icons (MIT, 24×24, stroke=1.5)

Paths are directly usable from the reference catalog. Phosphor uses 24×24 viewBox with stroke-width="1.5".

**Final format:**
```javascript
{ paths: '<path d="..."/>', source: "Phosphor" }
```

#### E) Iconoir (MIT, 24×24, stroke=1.5)

```bash
curl -sL "https://cdn.jsdelivr.net/npm/iconoir@7.11.0/icons/regular/<kebab-name>.svg"
```

- Names are kebab-case (e.g., `bright-star.svg`, `book-stack.svg`)
- Search: `curl -sL "https://unpkg.com/iconoir@7.11.0/icons/regular/" | grep -o 'href="[^"]*\.svg"' | sort -u`

**Conversion required:**
1. Fetch the raw SVG file
2. Extract inner elements
3. Convert `stroke="currentColor"` to `stroke="#000000"` in inner elements (the template handles the wrapper SVG's stroke)
4. Strip the original `<svg>` opening tag entirely — use regex `re.sub(r'<svg[^>]*>', '', svg_content)` because attribute order varies across icons
5. Strip `stroke-width="1.5"` from child elements for consistency

```python
inner = re.sub(r'<svg[^>]*>', '', svg_content)
inner = re.sub(r'</svg>', '', inner)
inner = inner.replace('stroke="currentColor"', 'stroke="#000000"')
inner = re.sub(r'\s+stroke-width="1.5"', '', inner)
```

**Verify** that every resulting Iconoir icon entry has no extraneous attributes.

**Final format:**
```javascript
{ paths: '<path d="..."/><circle cx="..." cy="..." r="..."/>', source: "Iconoir" }
```

#### F) Huge Icons — Free Pack (MIT, 24×24, stroke=1.5)

```bash
curl -sL "https://cdn.jsdelivr.net/npm/@hugeicons/core-free-icons@4.2.2/dist/esm/<PascalCase>Icon.js"
```

- Names are PascalCase with "Icon" suffix (e.g., `Home01Icon`, `Search01Icon`, `UserIcon`, `AiSearchIcon`)
- 5400+ free icons (Stroke Rounded style)
- Package: `@hugeicons/core-free-icons` — MIT License
- Search available icon names: `curl -sL "https://cdn.jsdelivr.net/npm/@hugeicons/core-free-icons@4.2.2/dist/types/index.d.ts" | grep -oE 'declare const [A-Za-z0-9]+Icon' | sed 's/declare const //' | sort -u`

**Data format (tuple array):**
```javascript
// Raw output from the JS module
const Search01Icon = [
  ["path", { d: "M...", stroke: "currentColor", strokeWidth: "1.5", strokeLinecap: "round", strokeLinejoin: "round", key: "0" }],
  ["circle", { cx: "11", cy: "11", r: "8", stroke: "currentColor", strokeWidth: "1.5", strokeLinecap: "round", strokeLinejoin: "round", key: "1" }]
];
```

**Conversion from tuple array to inner SVG paths:**

1. Parse each tuple `[elementType, attributes]`:
   - `elementType` is the SVG tag name (e.g., "path", "circle", "rect", "line", "polyline", "polygon")
   - `attributes` is a plain object with key-value pairs

2. Convert each tuple to an SVG element string:
   - Drop the `key` attribute (internal Hugeicons tracking, not valid SVG)
   - Convert `strokeWidth` → `stroke-width`, `strokeLinecap` → `stroke-linecap`, `strokeLinejoin` → `stroke-linejoin` (camelCase to kebab-case)
   - Convert boolean or numeric values to strings as needed

3. **Strip `stroke-width="1.5"` from all child elements** — Let the template wrapper control it
4. **Change `stroke="currentColor"` to `stroke="#000000"`** on child elements for static rendering

```python
# Example Python conversion
import re
import json

raw = [
  ["path", {"d": "M...", "stroke": "currentColor", "strokeWidth": "1.5", "strokeLinecap": "round", "strokeLinejoin": "round"}],
  ["circle", {"cx": "11", "cy": "11", "r": "8", "stroke": "currentColor", "strokeWidth": "1.5"}]
]

def to_svg(element):
  tag, attrs = element
  # Remove internal keys
  attrs.pop('key', None)
  # Convert camelCase to kebab-case
  kebab = {}
  for k, v in attrs.items():
    kebab_key = re.sub(r'([a-z])([A-Z])', r'\1-\2', k).lower()
    if kebab_key == 'stroke-width':
      continue  # Let template control stroke width
    if kebab_key == 'stroke' and v == 'currentColor':
      v = '#000000'
    kebab[kebab_key] = str(v)
  attrs_str = ' '.join(f'{k}="{v}"' for k, v in kebab.items())
  if tag in ('circle', 'rect', 'ellipse', 'line'):
    return f'<{tag} {attrs_str}/>'
  else:  # path, polyline, polygon
    return f'<{tag} {attrs_str}/>'

paths_inner = ''.join(to_svg(e) for e in raw)
# Result: '<path d="M..." stroke="#000000" stroke-linecap="round" stroke-linejoin="round"/><circle cx="11" cy="11" r="8" stroke="#000000"/>'
```

**Alternatively** for manual conversion (simpler approach):
1. Read the JS file
2. Extract each tuple's element type and attributes
3. Write as SVG elements with camelCase→kebab-case conversion
4. Remove `key` attributes, `strokeWidth`, and convert `stroke="currentColor"` to `stroke="#000000"`

**Final format:**
```javascript
{ paths: '<path d="M..."/><circle cx="11" cy="11" r="8"/>', source: "Huge Icons" }
```

### Step 4: Build the ICON_GROUPS Data Array

**Do NOT generate a full HTML file from scratch.** Use the canonical template `assets/icons-template.html`. Copy it to a new file, then edit only three sections:

1. `PAGE_TITLE` — Set to a descriptive title
2. `ICON_COLOR` — Default `'#000000'`; change only if user requests a specific color
3. `ICON_GROUPS` — The data array (see below)

**Template structure — do NOT modify rendering code or copy functions:**

```javascript
const ICON_GROUPS = [
  {
    name: "组名",                          // Section heading
    icons: [
      {                                    // 1-6 icons per group
        paths: '<circle cx="12" cy="12" r="10"/>...',  // SVG inner HTML (no <svg> wrapper)
        source: "Feather"                               // Source badge text
      },
      // ...
    ]
  },
  // ...
];
```

**Rules:**
- Each `paths` value is the **inner HTML** of the SVG — just the element tags, no `<svg>` wrapper
- Each icon MUST pass all 8 quality rules
- For IconPark (48×48 scaled): wrap in `<g transform="scale(0.5)">` with stroke-width stripped
- For Lucide: strip `stroke-width="2"` from children
- For Huge Icons: convert tuple array to SVG element strings, strip `strokeWidth`, convert `currentColor`→`#000000`
- Aim for 6 icons per group. Min 1, max 6.

### Step 5: Deliver

1. Copy `assets/icons-template.html` to a new file (e.g., `icons.html`)
2. Edit the copy: fill `PAGE_TITLE` and `ICON_GROUPS`
3. Open in browser to verify rendering
4. Present the file to the user

## Multiple Source Distribution Rule

When building ICON_GROUPS, ensure each group's 6 icons draw from at least 3 different sources. This maximizes visual diversity and reduces the chance of duplicate-looking icons. Preferred distribution: 2-3 IconPark + 2-3 Feather/Lucide + 1-2 from the remaining 3 sources.

## Fallback Behavior

- No obvious icon match → use generic icons (star, heart, bookmark, circle-dot) as the last option
- Fewer than 4 items → still generate 6 icons per item
- More than 20 items → warn and ask to split into batches of 10

## Resources

### references/
- `icon-sources.md` — Full icon catalog organized by semantic category with SVG path data. Load this into context before executing the skill.

### assets/
- `icons-template.html` — Canonical data-driven template file. Copy this to start a new icon set, then edit `ICON_GROUPS` and `PAGE_TITLE`. Do NOT modify the rendering code or copy functions.

### scripts/
- (Empty — all icon mapping is done via reference catalog lookup and CDN fetch)
