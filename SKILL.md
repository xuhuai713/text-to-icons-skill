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
9. **⚠️ Stroke uniformity across sources** — All icons in the same HTML file must render at visually identical stroke thickness. The template wrapper uses `stroke-width="1.5"` for display and `COPY_STROKE_WIDTH="0.5"` for clipboard. Each source must follow its specific conversion to match:
   - **IconPark (scaled)**: `<g transform="scale(0.5)" stroke-width="3">` → effective display stroke = 3 × 0.5 = 1.5 (matches template). See Step 3(A) for details.
   - **Feather/Huge/Phosphor (native 24×24)**: strip explicit stroke-width from children, let template wrapper control (inherit 1.5 for display, 0.5 for clipboard).
   - **Lucide/Iconoir (native 24×24)**: strip explicit stroke-width from children (Lucide=2, Iconoir=1.5), let template wrapper control.
   - **Verification**: After building ICON_GROUPS, visually scan the rendered page — if any icon appears visibly thinner or thicker, check its g wrapper and child stroke-width.

## When to Use

- User provides steps, stages, phases (business process flow, product roadmap, project lifecycle)
- User provides feature names, module names, category labels needing matching icons
- User says "帮我把这些内容转成图标" / "给这些步骤配上图标" / "convert this text to icons"
- User wants copyable SVG icons for design tools or frontend projects
- User requests linear/outline icons with consistent stroke style

## ⚙️ Icon Source Priority Hierarchy (MUST FOLLOW)

每次生成图标时，严格按以下优先级选择图标源，**不允许随机取样或随意分配**：

| 层级 | 源 | 许可证 | 图标数 | 使用条件 |
|------|---|--------|--------|---------|
| **Tier 1 ⭐** | **IconPark** (核心) | Apache 2.0 | 2600+ | **默认首选**。先搜索 IconPark 是否有匹配的图标。每个组至少 3 个 IconPark 图标 |
| **Tier 2** | **Feather Icons** | MIT | 286 | IconPark 无匹配或不符合质量规则时使用。每个组最多 2 个 |
| **Tier 2** | **Huge Icons** (free) | MIT | 5400+ | IconPark 无匹配时使用。与 Feather 同级，优先选视觉差异更大的 |
| **Tier 3** | **Lucide Icons** | ISC | 1400+ | Tier 1+2 均不满足时最后使用。Lucide 是 Feather 衍生，仅作补充 |
| **Tier 3** | **Phosphor Icons** | MIT | 9000+ | 特殊形状需求时使用 |
| **Tier 3** | **Iconoir** | MIT | 1600+ | 特殊形状需求时使用 |

**判断流程：**
1. 对每个概念，先在 IconPark 中搜索 3-4 个匹配图标
2. 如果 IconPark 匹配不足（无对应图标或路径密度超标/视觉失衡），从 Tier 2（Feather / Huge Icons）补齐
3. 仅当 Tier 1+2 仍不足 6 个时，才从 Tier 3 中选取
4. 同一组内确保 3 个不同层级以上的来源（如：IconPark ×3 + Feather ×2 + Lucide ×1）

## Icon Source Reference

Always load `references/icon-sources.md` into context. It contains the full catalog organized by semantic category with SVG path data for rapid lookup without external fetching.

| Source | License | Icons | viewBox | Default Stroke | Fetch Method |
|--------|---------|-------|---------|----------------|--------------|
| **IconPark** ⭐ (core) | Apache 2.0 | 2600+ | 48×48 | 4 | `unpkg.com/@icon-park/svg@1.4.2/es/icons/<PascalCase>.js`; scale(0.5), stroke-width=3 on g |
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

**Icon selection process — strict priority order (not random):**
1. Identify the core concept (e.g., "线索挖掘" = search/discovery)
2. **First**: Search IconPark catalog for matching icons → select 3-4 candidates
3. **Second**: If more icons needed, search Feather catalog and Huge Icons for best matches → select 1-2
4. **Third**: Only if still short of 6, search Lucide/Phosphor/Iconoir → select 1
5. Reject any candidate that fails quality rules; if rejected, move to next source in hierarchy
6. Select exactly 6 icons with DISTINCT visual forms
7. Ensure at least 3 different sources are represented (but always favor higher-tier sources)

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

##### Single icon fetch (curl):

```bash
curl -sL "https://unpkg.com/@icon-park/svg@1.4.2/es/icons/<PascalCaseName>.js"
```

- Names are PascalCase (e.g., `ProcessLine`, `DataServer`, `CodeComputer`)
- Search: `curl -sL "https://unpkg.com/@icon-park/svg@1.4.2/es/icons/" | grep -oP 'href="[^"]+\.js"' | sed 's|.*/||;s/\.js"//' | sort -u`

##### Batch fetch + conversion (Python — preferred for ≥5 icons):

For larger icon sets, use this Python script structure that fetches all modules, evaluates the JS template literals, and converts to SVG paths in one pass:

```python
import re, urllib.request, json

BASE = "https://unpkg.com/@icon-park/svg@1.4.2/es/icons/{}.js"

def fetch(name):
    url = BASE.format(name)
    with urllib.request.urlopen(url, timeout=20) as r:
        return r.read().decode("utf-8")

def convert(js):
    # Extract the return expression from the JS module
    m = re.search(r"return (.+?);\s*\}\);", js, re.DOTALL)
    if not m:
        m = re.search(r"return (.+);", js, re.DOTALL)
    if not m:
        return None
    expr = m.group(1)
    # Replace all props.* template variables with static values
    for a, b in [
        ('props.colors[0]', '"#000000"'),   # stroke color
        ('props.colors[1]', '"#000000"'),   # primary fill → stroke
        ('props.colors[2]', '"#000000"'),   # secondary fill → stroke
        ('props.colors[3]', '"#000000"'),   # tertiary fill → stroke
        ('props.strokeWidth', '"4"'),
        ('props.size', '"48"'),
        ('props.strokeLinecap', '"round"'),
        ('props.strokeLinejoin', '"round"'),
    ]:
        expr = expr.replace(a, b)
    # Evaluate as Python string concatenation to get the SVG
    svg = eval(expr)
    # Clean up
    svg = re.sub(r'<\?xml[^>]+\?>', '', svg)
    inner = re.sub(r'<svg[^>]*>', '', svg)
    inner = re.sub(r'</svg>', '', inner)
    # Convert fills to linear strokes
    inner = inner.replace('fill="#000000"', 'fill="none" stroke="#000000"')
    inner = inner.replace('stroke="#000000" stroke="#000000"', 'stroke="#000000"')
    inner = inner.replace('fill="none" stroke="#000000" stroke="#000000"', 'fill="none" stroke="#000000"')
    # Strip all child stroke-width (they inherit from g wrapper)
    inner = re.sub(r'\s+stroke-width="\d+"', '', inner)
    return '<g transform="scale(0.5)" stroke-width="3">' + inner.strip() + '</g>'

# Usage:
ip_names = ["People", "Camera", "Phone", "Comment", "Search"]  # etc.
ip_data = {}
for name in ip_names:
    js = fetch(name)
    ip_data[name] = convert(js)
```

This approach is faster and more reliable than manually converting each icon.

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

2. **Color slot conversion (handles 3 color slots):**
   - `colors[0]` → stroke color → replace with `#000000` (appears in `stroke=` attribute)
   - `colors[1]` → primary fill (body rects, large shapes) → replace with `#000000`, then for elements using `fill="#000000"`, convert to `fill="none" stroke="#000000"`
   - `colors[2]` → secondary fill (decorative dots/lines) → replace with `#000000`, same fill→stroke conversion
   - **⚠️ Exception**: `colors[2]` may appear in `stroke=` attribute (not `fill=`) — this is correct as-is: `stroke="#000000"`
   - **⚠️ Edge case**: Some icons use `colors[3]` (e.g., Cpu icon's inner square) — treat same as `colors[1]`/`[2]`: convert to `#000000` then `fill="none" stroke="#000000"`

3. **Wrap in `<g transform="scale(0.5)" stroke-width="3">`** — Put the 48×48 paths inside a group with `transform="scale(0.5)"` AND explicit `stroke-width="3"`. This ensures:
   - **Display rendering**: children use stroke-width=3 through inheritance. After scale(0.5), effective stroke = 3 × 0.5 = **1.5 units**, matching Feather/Huge Icons exactly (they inherit 1.5 from template wrapper with no scaling)
   - **Clipboard copy**: children inherit 3 from `<g>`, effective = 3 × 0.5 = 1.5. Feather clipboard = 0.5. Accept this trade-off (display uniformity > clipboard uniformity). If user requests uniform clipboard, strip g's stroke-width during copy.

4. **⚠️ CRITICAL: Strip ALL `stroke-width` from child elements** — IconPark children have `stroke-width="4"`. Remove with regex:
   ```python
   inner = re.sub(r'\s+stroke-width="\d+"', '', inner)
   ```
   After stripping, children inherit `stroke-width="3"` from the `<g>` wrapper. See rule 3 for effective stroke calculation.

5. **Fill-to-stroke conversion for `colors[1]`/`colors[2]`/`colors[3]`:**
   ```python
   # After replacing color variables with '#000000':
   # Elements that had fill="colors[1]" now have fill="#000000"
   # Convert them to linear style:
   inner = inner.replace('fill="#000000"', 'fill="none" stroke="#000000"')
   # Clean up duplicate stroke attributes (when element had both fill and stroke originally):
   inner = inner.replace('fill="none" stroke="#000000" stroke="#000000"', 'fill="none" stroke="#000000"')
   inner = inner.replace('stroke="#000000" stroke="#000000"', 'stroke="#000000"')
   ```

6. **Fill-dependent complex paths MUST be replaced** — Some paths (facial features, smile arcs, filled shapes) designed as filled areas may produce garbled thin lines when `fill="none"`. Detection criteria:
   - Path uses `V` (vertical-to) and `Z` (close) commands referencing unrelated coordinates
   - Multiple disjoint subpaths forming a fill-only shape
   - **Fix**: Replace with a simple bezier curve:
     ```html
     <!-- WRONG: fill-dependent smile -->
     <path d="M20 32C18.8954 32 18 32.8954 18 34C18 35.1046...Z"/>
     <!-- RIGHT: stroke-only smile -->
     <path d="M17 34C20 37 28 37 31 34"/>
     ```

7. **Pre-verification**: Before adding any IconPark icon, trace EACH element. The safest approach: read the full JS source (curl without grep filter) and manually list all SVG elements before writing the HTML.

**Final format for the `paths` field in ICON_GROUPS:**
```javascript
{ paths: '<g transform="scale(0.5)" stroke-width="3"><path d="..."/><circle cx="..." r="..."/></g>', source: "IconPark" }
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
4. **Strip XML comments from the SVG** — Lucide SVGs from unpkg may contain `<!-- @license lucide-static vX.X.X - ISC -->` comments. Remove them before embedding.
5. **Strip `\\n` whitespace from paths** — Some Lucide SVGs contain embedded `\\n` characters from the SVG formatting. These don't break rendering but should be cleaned for consistency.

```python
# Strip XML comment and newlines from Lucide SVG
inner = re.sub(r'<!--[^>]*-->', '', inner)
inner = inner.replace('\\n', '').strip()

# Strip explicit stroke-width from Lucide children
inner = re.sub(r'\\s+stroke-width="2"', '', inner)
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
- For IconPark (48×48 scaled): wrap in `<g transform="scale(0.5)" stroke-width="3">` with child stroke-width stripped (ensures display stroke matches Feather at 1.5)
- For Lucide: strip `stroke-width="2"` from children
- For Huge Icons: convert tuple array to SVG element strings, strip `strokeWidth`, convert `currentColor`→`#000000`
- Aim for 6 icons per group. Min 1, max 6.

### Step 5: Deliver

1. Copy `assets/icons-template.html` to a new file (e.g., `icons.html`)
2. Edit the copy: fill `PAGE_TITLE` and `ICON_GROUPS`
3. Open in browser to verify rendering
4. Present the file to the user

**⚠️ CRITICAL: Do NOT delete the template's rendering functions when replacing ICON_GROUPS.**
The template has this structure:

```
const ICON_GROUPS = [...];     // ← replace this block only
                              // ← keep everything below
// ═══════ 渲染引擎 ——— 无需修改 ═══════
function buildSvgTag(paths) { ... }  // ← MUST preserve
function renderIcons() { ... }       // ← MUST preserve
renderIcons();                       // ← MUST preserve
function copySVG(btn) { ... }        // ← MUST preserve
```

When doing a string replacement (e.g., via Python script), match from `const ICON_GROUPS = [` to `];` (the closing semicolon of ICON_GROUPS), NOT to `function renderIcons()`. The `buildSvgTag` function sits between them. Missing it = blank page.

**Example safe replacement in Python:**
```python
start = template.find('const ICON_GROUPS = [')
# Find the ]; that closes ICON_GROUPS (not one inside)
end = template.find('\n];\n\n// ═══════════\n// 渲染引擎', start) + 2
new_template = template[:start] + new_groups_js + template[end:]
```

## Priority Enforcement Check

Before delivering, verify each group's icon selection against the priority hierarchy:

1. **Exactly 6 icons per group** — The skill mandates each text item maps to 6 icons. This is a hard rule. Do NOT reduce to fewer without explicit user request.
2. **Count per tier**: Tier 1 (IconPark) ≥ 3 per group? Tier 2 (Feather/Huge) ≤ 2? Tier 3 (Lucide/others) ≤ 1?
3. **Reason for downgrade**: If any icon comes from Tier 2 or 3, verify that IconPark genuinely lacked a matching icon (no equivalent concept, or all candidates failed quality rules)
4. **Stroke uniformity**: Check that IconPark icons use `<g transform="scale(0.5)" stroke-width="3">` — not bare `<g transform="scale(0.5)">` which would make them half as thick as Feather icons
5. **No random pick**: Every icon selection must be traceable to the priority hierarchy decision logic

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

## 📋 IconPark Name Catalog for Chinese Business Concepts

Below is a practical mapping of common Chinese concepts to their IconPark PascalCase names, discovered through real usage. Use this for rapid lookup.

| 中文概念 | IconPark 图标名 | 说明 |
|---------|----------------|------|
| **人员/用户** | | |
| 人员/人群 | `People`, `Group`, `User`, `Avatar` | People=双人, Group=4人矩阵 |
| 面对面沟通 | `People`, `Comments` | Comments=双气泡 |
| 添加用户 | `AddUser` | 用户+加号 |
| **沟通/媒体** | | |
| 摄像机 | `Camera`, `CameraOne`, `CameraFive` | One=摄像头+底座 |
| 电话 | `Phone`, `PhoneCall`, `PhoneBooth`, `HeadphoneSound` | |
| 气泡/消息 | `Comment`, `Comments`, `Message`, `MessageOne` | |
| 语音 | `Microphone`, `Voice`, `VoiceOne`, `VoiceInput` | |
| 放大镜/搜索 | `Search`, `FileSearch`, `PreviewOpen` | 注意: IconPark 无 Magnifier 命名 |
| 眼睛/查看 | `Eyes`, `Eye` | 双眼睛=查看/搜索 |
| **文档/存储** | | |
| 文档 | `FileText`, `FileDoc`, `DocAdd`, `CollectionFiles` | |
| 文件夹 | `Folder`, `FolderOne`, `DocumentFolder` | |
| **列表/清单** | | |
| 列表/总结 | `List`, `ListNumbers`, `ListOne`, `ListCheckbox` | |
| 清单/检查 | `Checklist`, `Checkbox`, `Clipboard` | |
| **情感/关系** | | |
| 爱心 | `Heart`, `HeartBallon`, `Heartbeat`, `Like`, `Dislike` | |
| 标签 | `Tag`, `TagOne`, `Label` | |
| **商业** | | |
| 商机/目标 | `Target`, `TargetOne`, `GoldMedal`, `Briefcase`, `Star` | Target=靶心=机会 |
| 钱/支付 | `Dollar`, `Bitcoin`, `PaperMoney`, `GoldMedal` | |
| **流程/连接** | | |
| 业务流程 | `ProcessLine`, `Branch`, `BranchOne`, `Exchange` | |
| 连接 | `Connect`, `Connection`, `ConnectionPoint`, `CircularConnection` | |

When mapping a Chinese concept to IconPark:
1. Use `curl -sL "https://unpkg.com/@icon-park/svg@1.4.2/es/icons/" | grep -i <keyword>` to find candidates
2. Cross-reference with the table above for commonly needed concepts
3. Verify that the PascalCase name matches the concept (some names are non-obvious, e.g. `Comments` = two speech bubbles = 沟通)
