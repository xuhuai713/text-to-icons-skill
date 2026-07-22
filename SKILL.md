---
name: text-to-icons
description: "Convert user-provided text into matching linear icons. Output is a single self-contained HTML file using a data-driven template (icons-template.html). All icon data lives in the ICON_GROUPS JS array; the template renders cards dynamically. Uniform 24×24 viewBox, 0.5pt stroke for both display and clipboard. Core source: IconPark (Apache 2.0). Additional sources: Feather/MIT, Lucide/ISC, Huge Icons/MIT."
agent_created: true
---

# Text to Icons — 文本转图标

## Overview

This skill transforms structured text (process steps, feature lists, categories, slide titles) into matching linear/outline icons and renders them as a single self-contained HTML file. Each text item maps to **6 matching icons** drawn from a curated set of free, commercially-usable icon libraries. The HTML includes one-click "Copy SVG" buttons.

## 🔑 Critical Quality Rules — MUST FOLLOW

### Rule 0 (SUPREME — overrides all rules below) — 视觉与概念匹配度

**图标与概念的视觉匹配度 > 一切其他规则。** 当 Tier 1 (IconPark) 的视觉匹配度差于 Tier 3 (Lucide) 时，使用 Tier 3。命名者隐喻 ≠ 用户隐喻，`Transport` 在 IconPark 实际是运输机器人（不是交通工具），`NetworkTree` 实际是组织架构图（不是交通网络）。

**任何选中的图标都必须通过以下视觉检查（不依赖名称推断）：**
- **去标签测试**：移除文本标签，图标本身是否仍能让普通人 1 秒内识别为该概念？
- **去名称测试**：不知道图标英文名的情况下，看视觉是否能直接联想到中文概念？
- **隐喻一致性**：图标的隐喻方向必须与概念的主流隐喻一致（如「交通产业」→ vehicle/ship/plane/bus/factory，不是 robot/org-chart）。

### Rules 1–9 (Quality Checks)

Every icon in the output MUST pass ALL these checks:

1. **Instantly recognizable** — The average person understands the icon within 1 second. No squinting required.
2. **No abstract metaphors** — Only universally understood visual symbols: magnifying glass = search (good); abstract curves labeled "handshake" (bad — looks like random squiggles).
3. **Must decode without labels** — Remove the text label; the icon should still be obvious.
4. **Vet SVG paths** — Before including any icon, mentally trace the paths to confirm they actually draw the intended shape. **Do not trust the icon name as a proxy for visual content.**
5. **No repetitions** — Within the same group's 6 icons, avoid visually similar variants. Also avoid reusing the same icon across different groups more than 2 times.
6. **Path density check** — Max 6 path elements (paths/lines/circles/rects/polylines) unless every element is clearly distinguishable at 28×28px.
7. **Shape integrity check** — Reject squashed circles, mismatched corners, disconnected lines, unintentional overlapping (杂糅).
8. **Visual weight balance** — Strokes must be evenly distributed across the 24×24 viewBox. Reject icons where >70% of strokes cram into one corner.
9. **⚠️ Stroke uniformity across sources** — All icons in the same HTML file must render at visually identical stroke thickness. The template wrapper uses `stroke-width="1.5"` for display and `COPY_STROKE_WIDTH="0.5"` for clipboard. Each source must follow its specific conversion to match:
   - **IconPark (scaled)**: `<g transform="scale(0.5)" stroke-width="3">` → effective display stroke = 3 × 0.5 = 1.5 (matches template). See Step 3(A) for details.
   - **Feather/Huge (native 24×24)**: strip explicit stroke-width from children, let template wrapper control (inherit 1.5 for display, 0.5 for clipboard).
   - **Lucide (native 24×24)**: strip explicit stroke-width from children (Lucide=2), let template wrapper control.
   - **Verification**: After building ICON_GROUPS, visually scan the rendered page — if any icon appears visibly thinner or thicker, check its g wrapper and child stroke-width.

## When to Use

- User provides steps, stages, phases (business process flow, product roadmap, project lifecycle)
- User provides feature names, module names, category labels needing matching icons
- User says "帮我把这些内容转成图标" / "给这些步骤配上图标" / "convert this text to icons"
- User wants copyable SVG icons for design tools or frontend projects
- User requests linear/outline icons with consistent stroke style

## ⚙️ Icon Source Priority Hierarchy

**重要前提**：本优先级仅在「视觉匹配度相当」时生效。当 Tier 1 (IconPark) 的视觉匹配明显差于 Tier 3 (Lucide) 时，**直接使用 Tier 3**，不需要为满足 Tier 1 而降级匹配度。详见 Rule 0。

| 层级 | 源 | 许可证 | 图标数 | 使用条件 |
|------|---|--------|--------|---------|
| **Tier 1 ⭐** | **IconPark** (核心) | Apache 2.0 | 2600+ | **默认首选**。先搜索 IconPark 是否有匹配的图标。每个组至少 3 个 IconPark 图标（前提是 IconPark 候选的视觉匹配度达标） |
| **Tier 2** | **Feather Icons** | MIT | 287 | IconPark 无匹配或不符合质量规则时使用。每个组最多 2 个 |
| **Tier 2** | **Huge Icons** (free) | MIT | 5400+ | IconPark 无匹配时使用。与 Feather 同级，优先选视觉差异更大的 |
| **Tier 3** | **Lucide Icons** | ISC | 1400+ | Tier 1+2 视觉匹配不达标时使用。Lucide 是 Feather 衍生，**当 Lucide 的视觉更准，优先 Lucide**（不再受「Tier 3 兜底」限制） |

**判断流程：**
1. 对每个概念，在所有 4 个源中搜索匹配图标（`--plan` 或 `--search` 一键完成）
2. 肉眼扫一遍自动选图结果，替换明显错配（`Eggplant`→`Seedling`、`Trademark`→`Shop`）
3. 补齐到每组 6 个，同组至少 3 个不同源
4. Rule 0 凌驾一切——当 Tier 1 视觉差于 Tier 3，直接用 Tier 3

## Icon Source Reference

Always load `references/icon-sources.md` into context. It contains a curated catalog (精选参考，非全量) organized by semantic category with SVG path data for rapid lookup without external fetching.

| Source | License | Icons | viewBox | Default Stroke | Fetch Method |
|--------|---------|-------|---------|----------------|--------------|
| **IconPark** ⭐ (core) | Apache 2.0 | 2600+ | 48×48 | 4 | `unpkg.com/@icon-park/svg@1.4.2/es/icons/<PascalCase>.js`; scale(0.5), stroke-width=3 on g |
| **Feather Icons** | MIT | 287 | 24×24 | 1.5 | Reference catalog in `icon-sources.md` |
| **Lucide Icons** | ISC | 1400+ | 24×24 | 2 | `unpkg.com/lucide-static@0.469.0/icons/<kebab-name>.svg`; strip stroke-width="2" |
| **Huge Icons** (free) | MIT | 5400+ | 24×24 | 1.5 | `cdn.jsdelivr.net/npm/@hugeicons/core-free-icons@4.2.2/dist/esm/<PascalCase>Icon.js`; read as tuple array, convert to inner SVG paths |

## Workflow

### Step 1: Parse the Input

Extract all discrete items from the user's text. Separators: newlines, numbered/bulleted lists, commas, table rows. Preserve original order. Output a numbered list for user confirmation.

### Step 2: Map Each Item to 6 Matching Icons

Each text item maps to exactly 6 icons. **6 icons = fuzzy buffer** — 4-5 accurate ones compensate for 1-2 borderline. This eliminates the need for a separate verification step.

**Efficient selection process (2 rounds, no intermediate artifacts):**

**Round 1 — Batch plan (bulk search, 1 tool call):**
1. Write `plan.json` with concepts + keywords per group (≥3 groups recommended)
2. Run `build_icons.py --plan plan.json --draft groups_draft.json` — single-process search across all 4 sources, returns 3 auto-picked icons per group
3. Or for ≤2 groups, use `--search "keyword1 keyword2"` per group

**Round 2 — Fix + fill (manual, no extra tool calls):**
4. Scan auto-picks for visual mismatches (Rule 0): reject icons whose visual doesn't match the concept. Common traps:
   - `Eggplant` = 茄子, not 培育 → use `Seedling`
   - `Trademark` = 商标, not 商贸 → use `Shop`
   - `Transport` = 机器人, not 交通工具 → use `Ship`/`Truck`
   - `CloudStorage` = 云存储, not 能源 → use `Atom`/`Wind`
5. Add 3 more icons per group to reach 6, searching across all 4 sources as needed
6. **Mental filter (30 sec)**: remove labels, check that ≥4/6 icons per group are visually obvious
7. Write `groups.json`

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

**CRITICAL: Before finalizing any icon, mentally trace its SVG paths.** Confirm the paths actually draw what is intended. 6 icons per group = fuzzy buffer; 4-5 accurate ones compensate for 1-2 borderline cases. **Trust visual, not name:** `Transport` = 机器人, `NetworkTree` = 组织图 — reject on sight.

### Step 3: Fetch SVG Paths from Icon Sources

**⚡ 本地缓存优先（默认路径）**：本技能随包附带 `assets/icon-cache.json`——由 `scripts/precache.py` 预抓取并转换好的全部图标 inner-SVG。生成时**直接从此缓存读取**，无需联网，速度从「跨洋串行抓取 ~75s」降到「本地读盘 <1s」。

**读取方式（任选其一）：**

1. 用自带工具函数（推荐）：`scripts/icon_cache.py` 提供 `get_icon(source, name)`，
   优先返回缓存，缓存未命中时自动回退 CDN 实时抓取并转换：
   ```python
   import sys, json
   sys.path.insert(0, "<skill>/scripts")
   from icon_cache import get_icon
   paths = get_icon("IconPark", "People")           # 返回 inner-SVG 字符串
   paths = get_icon("Huge Icons", "Search01Icon")
   ```
2. 直接读 JSON：
   ```python
   import json
   cache = json.load(open("<skill>/assets/icon-cache.json", encoding="utf-8"))
   paths = cache["IconPark"]["People"]               # 键名 = 图标名（见下表）
   ```

**缓存键名规则（与各源一致）：**

| 源 | 键名（name）示例 | 说明 |
|----|----------------|------|
| IconPark | `People`, `CameraOne` | PascalCase，去掉 `.js` |
| Huge Icons | `Search01Icon` | PascalCase + `Icon` 后缀 |
| Lucide | `search`, `user-circle` | kebab-case，去掉 `.svg` |
| Feather | `search`, `user` | kebab-case，去掉 `.svg` |

**仅当缓存确实缺失该图标时**，才使用下方各源的 CDN 抓取方式作为兜底（并建议跑一次 `python scripts/precache.py --source <源>` 把新图标写回缓存）。

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
curl -sL "https://unpkg.com/lucide-static@0.469.0/icons/<kebab-name>.svg"
```

- Names are kebab-case (e.g., `search.svg`, `user-circle.svg`, `file-text.svg`)
- Default SVG: viewBox="0 0 24 24", stroke-width="2"
- Search available icon names: `curl -sL "https://unpkg.com/lucide-static@0.469.0/" | grep -o 'icons/[a-z-]*\.svg' | sort -u`

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

#### D) Huge Icons — Free Pack (MIT, 24×24, stroke=1.5)

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

### Step 3.5: Batch Planning (批量编排 — 多组场景推荐)

当一次要生成 **多个组**（≥3 组）时，用 `--plan` 把「逐组独立搜索」压缩成 **单进程一次搜索**，把 AI 工具调用往返从 N 次降到 2 次（搜索 1 次 + 构建 1 次）。缓存只加载一次，典型耗时 <1s。

**plan.json 两种组格式：**

```json
[
  {
    "name": "主任",
    "concepts": [
      {"concept": "authority",  "keywords": ["crown","king","medal"]},
      {"concept": "expertise",  "keywords": ["master","certificate"]},
      {"concept": "seat",       "keywords": ["chair","seat"]}
    ]
  },
  {
    "name": "关于我们",
    "keywords": ["about","info","people","team","building","book"]
  }
]
```

- **concepts 模式（推荐）**：每组按概念列候选关键词，脚本自动「首关键词优先 + IconPark 优先 + 最短名决胜」选取，**跨概念按图标名去重**，天然避免 Crown×3 / Group×3 撞车。配合 `--draft` 直接写出可 `--groups` 的草稿 JSON。
- **keywords 模式**：返回 TOP-N 排名候选，**由 AI 人工定稿**（不自动选取，留给智力判断）。

**使用流程（2 次调用）：**

```bash
# 第 1 次：单进程批量搜索，写草稿（仅 concepts 组写入；keywords 组打印候选供人工定稿）
python build_icons.py --plan plan.json --draft groups_draft.json

# 人工复核草稿 / 补齐 keywords 组的 6 个图标（遵循质量规则与源优先级）

# 第 2 次：构建 HTML（内置 verify_icons + node --check）
python build_icons.py --groups groups_draft.json --output icons.html --title "标题"
```

**选取策略（concepts 模式，确定性、可复现）：**
1. 关键词按列表顺序即「贴合度」优先级，首个最贴切；
2. 每关键词候选按 `(源层级 IconPark>Feather>Huge>Lucide, 匹配分, 名长)` 排序；
3. 优先采用**词边界强匹配**（如 `friends`⊂`FriendsCircle`、`handshake`⊂`CooperativeHandshake`），命中即停；
4. 某关键词仅产生弱子串命中（如 `users`⊂`trousers`）则跳过，留给后续关键词；
5. 全无强匹配才回退首个关键词的弱命中；
6. 跨概念按图标名去重，保证每组 6 个隐喻互不雷同。

> ⚠️ `--plan` 的自动选取是**最佳努力草稿**，受图标库命名覆盖限制（如 IconPark 无 `Users`，只回退 `User`）。生成前仍须按 Step 2 质量规则逐图标复核。

### Step 4: Build the ICON_GROUPS Data Array

**Use the unified CLI tool `scripts/build_icons.py` to generate HTML.** It reads a groups JSON file (concept→icon mappings), injects data into the canonical template, runs JS syntax validation, and writes the output in one command.

**groups.json format:**
```json
[
  {
    "name": "组名",
    "icons": [
      ["IconPark", "Road"],
      ["Huge Icons", "Road01Icon"],
      ["Lucide", "train-track"]
    ]
  }
]
```

**CLI usage:**
```bash
# 全量生成（替换所有 ICON_GROUPS）
python build_icons.py --groups groups.json --output icons.html --title "标题"

# 追加模式（向已有 HTML 追加新组，自动跳过重复组名）
python build_icons.py --append groups.json --html existing.html

# 缓存搜索（按英文关键词查找匹配图标）
python build_icons.py --search "drone airplane robot"

# 批量编排（单进程搜索多组；concepts=概念去重自动选取，keywords=排名候选）
# 配合 --draft 写出 groups.json 草稿，供 --groups 立即构建
python build_icons.py --plan plan.json --draft groups_draft.json
```

**Template reference:** `assets/icons-template.html` — fully self-contained (0 external dependencies, inline CSS, system fonts). All Tailwind utilities have been replaced with inline CSS rules; the page renders offline without CDN calls.

**Rules:**
- Each `paths` value is the **inner HTML** of the SVG — just the element tags, no `<svg>` wrapper
- Each icon MUST pass all 8 quality rules
- For IconPark (48×48 scaled): wrap in `<g transform="scale(0.5)" stroke-width="3">` with child stroke-width stripped
- For Lucide: strip `stroke-width="2"` from children
- For Huge Icons: convert tuple array to SVG element strings, strip `strokeWidth`, convert `currentColor`→`#000000`
- Aim for 6 icons per group. Min 1, max 6.
- **⚠️ CRITICAL: Sanitize paths.** The CLI tool handles this internally — `re.sub(r'\s+', ' ', paths).strip()` + escaping.

### Step 5: Build + Deliver

1. Run `build_icons.py --groups groups.json --output icons.html --title "标题"`
   - Built-in: reads cache, injects ICON_GROUPS JS, validates with `node --check`
2. Present the output HTML to the user
3. Clean up temp files: `plan.json`, `groups_draft.json`, `groups.json` — build artifacts, not deliverables
4. Save a short memory note (what was generated, any auto-pick corrections made)

**Proven pipeline (2 tool calls):**
```
plan.json → build_icons.py --plan --draft → fix + fill (mental, no tools) → groups.json → build_icons.py --groups → deliver
```

## ⚡ Pre-Delivery Mental Filter (对抗性自审)

生成 `groups.json` 前，用 30 秒跑这个思想实验：**如果去掉所有标签只看视觉，每个组的 6 个图标里至少 4 个能一眼看懂概念。** 如果不到 4 个 → 回退重选。典型错配：`Transport`=机器人、`NetworkTree`=组织图、`CloseRemind`=关闭提醒。

## Fallback Behavior

- No obvious icon match → use generic icons (star, heart, bookmark, circle-dot) as the last option
- Fewer than 4 items → still generate 6 icons per item
- More than 20 items → warn and ask to split into batches of 10

## Resources

### references/
- `icon-sources.md` — Curated icon catalog (精选参考，非全量) organized by semantic category with SVG path data. Load this into context before executing the skill.

### assets/
- `icons-template.html` — 数据驱动模板（**0 外部依赖**，内联 CSS + 系统字体，离线可用）。由 `build_icons.py` 自动注入 `ICON_GROUPS` 数据。不要手动修改渲染引擎或复制函数。
- `icon-cache.json` — **本地图标缓存（核心提速件）**。由 `scripts/precache.py` 预抓取全量图标并转换为统一 inner-SVG，键为 `{ "<源名>": { "<图标名>": "<innerSVG>" } }`。生成时优先读此文件，无需联网。

### scripts/
- `build_icons.py` — **统一生成 CLI（核心工具）**。整合全量生成、追加、搜索、预览、JS 校验五合一。用法见 Step 4-5。
- `precache.py` — 构建/刷新本地缓存。并发抓取 IconPark / Huge Icons / Lucide / Feather，转换为统一 inner-SVG，落盘到 `assets/icon-cache.json`。支持增量（`--force` 全量、`--source <源>` 单源、`--lookup "源:名"` 查询）。
- `icon_cache.py` — 生成期读取辅助。提供 `get_icon(source, name)`：优先读 `icon-cache.json`，缺失则回退 CDN 实时抓取并转换。

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
