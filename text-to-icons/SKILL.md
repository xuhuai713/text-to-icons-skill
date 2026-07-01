---
name: text-to-icons
description: "Convert user-provided text into matching linear icons. Output is a single self-contained HTML file using a data-driven template (icons-template.html). All icon data lives in the ICON_GROUPS JS array; the template renders cards dynamically. Uniform 24×24 viewBox, 0.5pt stroke for both display and clipboard."
agent_created: true
---

# Text to Icons

## Overview

This skill transforms textual content—process steps, feature lists, categories, or any structured text—into beautiful linear icons and renders them as a single self-contained HTML file. Each text item maps to **6 matching icons** drawn from a curated set of open-source icon libraries. The HTML includes one-click "Copy SVG" buttons for immediate reuse.

## 🔑 Critical Quality Rules (MUST FOLLOW)

Every icon in the output MUST pass ALL these checks:

1. **Instantly recognizable** — The average person must understand what the icon means within 1 second. If you have to squint or think about it, it fails.
2. **No abstract metaphors** — Only use icons that are universally understood visual symbols. A magnifying glass = search (good). A gear = settings (good). A pair of curvy lines as "handshake" (bad — looks like random squiggles).
3. **Must decode without labels** — Remove the text label and the icon should still be obvious.
4. **Vet your SVG paths** — Before including an icon, mentally trace the paths to ensure they actually draw what you think they draw. A "handshake" icon should clearly show two hands meeting, not abstract curves.
5. **No repetitions** — Within the same item's 6 icons, don't include two icons that look nearly the same (e.g., don't include both "search" and "search-alt"). Also avoid reusing the same icon across different concepts more than 2 times; prefer sourcing from different libraries to reduce duplication.
6. **Path density check** — Reject any icon with more than 6 path elements (paths, lines, circles, rects, etc.) UNLESS every single element is clearly distinguishable at 28x28px. Dense icons with 7+ overlapping paths are illegible and MUST be replaced with simpler alternatives. Rule of thumb: if you can't trace each element at a glance, it fails.
7. **Shape integrity check** — Every geometric shape in the icon must be complete and correctly proportioned. Reject icons where:
   - Circles look squashed or off-center
   - Rectangles have mismatched corners
   - Lines don't connect where they visually should
   - Elements appear to overlap unintentionally ("杂糅")
8. **Visual weight balance** — The icon's strokes must be evenly distributed across the 24x24 viewBox. Reject icons where more than 70% of the strokes are crammed into one corner or side, leaving the rest empty — this creates a heavy, unbalanced appearance at small sizes.

## When to Use

- User provides a list of steps, stages, or phases (e.g., a business process flow, a product roadmap, a project lifecycle)
- User provides feature names, module names, or category labels and wants matching icons
- User says "帮我把这些内容转成图标" / "给这些步骤配上图标" / "convert this text to icons"
- User wants icons that can be copied as SVG code for use in design tools or frontend projects
- User explicitly requests linear/outline icons with 1.5px stroke style

## Workflow

### Step 1: Parse the Input

Extract all discrete items from the user's text. Items may be separated by:
- Newlines (each line is one item)
- Numbered or bulleted lists
- Comma-separated within a sentence
- Table rows

Preserve the original order. Output a numbered list for the user to confirm.

**Example input:**
```
线索挖掘, 商机洞察, 客户拜访, 营销推荐, 方案报价
```

**Parsed output:**
```
1. 线索挖掘
2. 商机洞察
3. 客户拜访
4. 营销推荐
5. 方案报价
```

### Step 2: Map Each Item to 6 Matching Icons (Critical Selection Process)

For each item, **painstakingly hand-pick 6 icons** that are immediately recognizable. This is the most important step.

**Icon selection process:**
1. First, identify the core concept of the item (e.g., "线索挖掘" = search/discovery)
2. Look at the reference catalog and mentally verify each candidate icon's paths
3. Reject any icon whose meaning isn't instantly clear
4. Select exactly 6 icons with DISTINCT visual forms (no similar-looking repeats)
5. Distribute across at least **3 different libraries**; prefer using 2-3 from IconPark, 2-3 from Feather, and 1-2 from Iconoir/Lucide/Phosphor per concept to maximize visual diversity

**Quality benchmarks by category (what icons MUST look like):**

| Category | GOOD examples (instantly recognizable) | BAD examples (REJECT) |
|----------|--------------------------------------|----------------------|
| Search / Discovery | magnifying glass, compass, binoculars | abstract circles, squiggly lines |
| Data / Analysis / Insight | bar chart, line chart, pie chart, eye | brain, abstract geometry |
| People / User / Visit | single person, two people, group, phone, door | abstract "handshake" curves |
| Marketing / Promotion | megaphone, trophy, star, gift, thumbs-up | abstract badges |
| Price / Money / Quotation | dollar sign, coins, credit card, tag, wallet, calculator | abstract symbols |
| Contract / Document / Sign | file text, pen, clipboard, folder, book | ambiguous scroll shapes |
| Project / Task / Implement | clipboard check, flag, layers, target, check circle | abstract branching lines |
| Product / Config / Setup | box, gear, wrench, sliders, grid | abstract lattice |
| Activation / Launch | zap, play, power, plus, rocket | ambiguous arrows |
| Billing / Invoice | monitor, printer, bar chart, receipt, file invoice | abstract file shapes |
| Settlement / Cart | shopping cart, check, x mark, trash, ban | complex checkout flows |
| Completion / Done | check circle, check mark, award, archive, smile | ambiguous checkmarks |
| Service / Maintenance | wrench, tool, terminal, code | abstract gear-only |
| Risk / Security / Audit | shield, lock, warning, alert, search audit | abstract polygons |
| Training / Learning | book open, graduation cap, presentation, file badge | abstract head shapes |

For each item, pick 6 icons that cover distinct visual forms:
- **Literal symbols** (2-3): The most direct, obvious representation of the concept
- **Action/outcome** (2): Something related to the action or result
- **Tool/related object** (1-2): A commonly associated tool

**CRITICAL: Before finalizing any icon, mentally trace its SVG paths.** Make sure the paths actually draw what you think they draw. The "handshake" icon from the previous version was wrong — its SVG paths drew abstract curves that didn't look like hands at all. If the paths look like they might not render correctly, replace the icon.

### Step 3: Fetch SVG Paths from Icon Sources

For each icon needed, fetch SVG path data from the appropriate source. Use curl/bash to fetch from CDN/NPM packages.

**Active Icon Sources:**

| Source | License | viewBox | stroke | How to Fetch |
|--------|---------|---------|--------|-------------|
| **Feather Icons** | MIT | 24x24 | 1.5 | Use `references/icon-sources.md` catalog |
| **Lucide Icons** | ISC | 24x24 | 1.5 | Use `references/icon-sources.md` catalog (shared with Feather) |
| **Phosphor Icons** | MIT | 24x24 | 1.5 | Use catalog or fetch from CDN |
| **IconPark** | Apache 2.0 | 48×48 | 4 | Fetch JS module, convert fill→none, strip child stroke-width, wrap in scale(0.5) g |
| **Iconoir** | MIT | 24×24 | 1.5 | Fetch raw SVG, convert currentColor→#000000 |

**IconPark fetch pattern:**
```bash
curl -sL "https://unpkg.com/@icon-park/svg@1.4.2/es/icons/<PascalCaseName>.js"
```
- Icon names are PascalCase (e.g., `ProcessLine`, `DataServer`, `CodeComputer`)
- **Conversion required**: Output uses 48×48 viewBox with both `fill` and `stroke`. For linear output:
  - Keep `viewBox="0 0 48 48"`
  - Set `fill="none"`, `stroke="#000000"` on all elements
  - Set `stroke-width` on child elements: **do NOT set explicit stroke-width on children** (they will inherit from the wrapper `<g>` tag)
  - Convert `fill="colors[1]"` and `fill="colors[2]"` to `fill="none" stroke="#000000"`
  - Search available icons: `grep -i '<keyword>'` on the icons directory listing

**⚠️ CRITICAL: IconPark conversion rules (MUST follow exactly):**

1. **Extract ALL element types, not just `<path>`** — The JS module contains `<rect>`, `<circle>`, `<path>`, and `<polyline>` elements. Grep patterns like `grep -oE 'd="[^"]*"'` will MISS `<rect>` and `<circle>` tags. Use a broader pattern:
   ```bash
   # WRONG: only finds path d-attributes
   grep -oE 'd="[^"]*"'
   # RIGHT: finds all SVG element types
   grep -oE '(d="[^"]*"|<rect[^>]*|<circle[^>]*|<polyline[^>]*)'
   ```
   OR fetch the full JS and manually extract all element tags.

2. **Every element MUST have `fill="none"` explicitly** — IconPark icons use three color slots:
   - `props.colors[0]` → stroke color (already fine, convert to `#000000`)
   - `props.colors[1]` → primary fill (e.g. body rects, large shapes) — set `fill="none" stroke="#000000"`
   - `props.colors[2]` → secondary fill (e.g. eyes, mouth, decorative dots) — set `fill="none" stroke="#000000"`
   
   After reading the full JS source, scan all elements for any occurrence of `fill="' + props.colors[1]` or `fill="' + props.colors[2]`. These MUST be set to `fill="none"` with `stroke="#000000"`.

3. **Fill-dependent complex paths MUST be replaced with stroke equivalents** — Some paths (especially facial features like mouths, smile arcs) are designed to work only as filled shapes. Converting them to `fill="none"` produces garbled thin lines. Detection criteria:
   - Path uses `V` (vertical-to) and `Z` (close) commands that reference unrelated coordinates
   - Multiple disjoint subpaths (separated by `M`/`Z`) that together form a fill-only shape
   - The path looks like it's drawing a filled area rather than a line/outline
   
   **Fix**: Replace the fill path with a simple bezier curve:
   ```html
   <!-- WRONG: fill-dependent mouth path -->
   <path d="M20 32C18.8954 32 18 32.8954 18 34C18 35.1046 18.8954 36 20 36V32ZM28 36...Z"/>
   <!-- RIGHT: stroke-only smile curve -->
   <path d="M17 34C20 37 28 37 31 34"/>
   ```

4. **Pre-verification process** — Before adding any IconPark icon, mentally trace EACH of its elements:
   - Is this element rendered by `fill` or `stroke` in the original? If fill, it needs stroke conversion.
   - After converting, does it still visually look correct? If the path looks like abstract lines when `fill="none"`, replace it.
   - Are there `<rect>` or `<circle>` tags I might have missed with a grep that only looks for `d=`
   
   The safest approach: **read the full JS source** (curl without grep filter) and manually list all SVG elements before writing the HTML.

5. **⚠️ CRITICAL: Strip `stroke-width` from child elements** — IconPark child elements have explicit `stroke-width="4"`. In the final HTML, these are wrapped in `<g transform="scale(0.5)" stroke-width="1">`. **The child's explicit `stroke-width="4"` overrides the `<g>` tag's inherited value**, resulting in effective stroke = 4 × 0.5 = 2 units — 4× thicker than Feather's 0.5. 

   **Fix**: Remove ALL `stroke-width="4"` from child elements inside the `<g>` block. Let them inherit `stroke-width="1"` from the `<g>` tag. After `scale(0.5)`, effective stroke = 1 × 0.5 = **0.5 units**, matching Feather exactly.

   In Python, this regex strips it from all children:
   ```python
   inner = re.sub(r'\s+stroke-width="4"', '', inner)
   ```

   **Verification**: Every IconPark `<g>` block must be checked — count all blocks and confirm zero have `stroke-width="4"` remaining.

**Iconoir fetch pattern:**
```bash
curl -sL "https://cdn.jsdelivr.net/npm/iconoir@7.11.0/icons/regular/<name>.svg"
```
- Icon names are kebab-case (e.g., `bright-star`, `book-stack`, `open-in-window`)
- **Conversion required**: Change `stroke="currentColor"` to `stroke="#000000"`; add `stroke-linecap="round" stroke-linejoin="round"` if missing
- **⚠️ CRITICAL: Iconoir SVG tag format varies across icons**. Some use `<svg ... stroke-width="1.5" viewBox="..." ...>` while others use `<svg ... viewBox="..." stroke-width="1.5" ...>` (attribute order differs). Use a regex `re.sub(r'<svg[^>]*>', ...)` to strip the entire opening tag rather than a fixed `replace()` — otherwise some icons will retain the original `stroke-width="1.5"` and wrong attributes.
- The raw SVG is 24×24 with `stroke-width="1.5"`. After extracting inner paths, wrap in your own `<svg>` tag with `stroke-width="0.5"`.
- After construction, verify every Iconoir SVG's opening tag has: `stroke-width="0.5"`, `stroke-linecap="round"`, `stroke-linejoin="round"`, `width="24pt" height="24pt"`, `id="..."`.
- Search available icons: `grep -i '<keyword>'` on the regular/ directory listing

### Step 4: Build the ICON_GROUPS Data Array

**Do NOT generate a full HTML file from scratch.** Use the canonical template `icons-template.html` located in the skill's `assets/` directory (or in the workspace root from a prior run). The template is a data-driven framework where all icon content lives in a single JavaScript constant.

**Template structure (read-only — do not modify the rendering code):**

The template has these key sections:
- **Top config**: `PAGE_TITLE`, `ICON_COLOR`, `COPY_STROKE_WIDTH` — change values as needed
- **Data array `ICON_GROUPS`**: The only section to edit. Format:
  ```javascript
  const ICON_GROUPS = [
    {
      name: "组名",     // ← Displayed as section heading
      icons: [
        { paths: '<circle cx="12" cy="12" r="10"/>...', source: "Feather" },  // ← SVG inner paths + source badge
        // ... up to 6 icons per group
      ]
    },
    // ... as many groups as needed
  ];
  ```
- **Render engine + copy functions**: Auto-generate cards and handle clipboard. Never edit these.

**Rules for building the array:**
1. Keep the template file path and rendering code unchanged
2. Only modify: `PAGE_TITLE`, `ICON_COLOR` (if user requests a color), and the `ICON_GROUPS` array
3. Each `paths` value is the **inner HTML** of the SVG — just the `<path>`, `<circle>`, `<line>`, `<polyline>`, `<rect>`, `<ellipse>`, `<polygon>` tags — **without** the `<svg>` wrapper
4. Each icon MUST pass the quality checks from Step 2 (recognizable, no repetitions, path density, etc.)
5. For IconPark 48×48 icons (scaled): wrap in `<g transform="scale(0.5)">` before putting in `paths`. Strip `stroke-width="4"` from child elements.
6. Aim for 6 icons per group. Minimum 1, maximum 6. If fewer than 6, the grid still renders correctly.

### Step 5: Deliver

1. Copy `icons-template.html` to a new file (e.g. `icons.html`, `icons-xxx.html`)
2. Edit the copy: fill in `ICON_GROUPS` with the mapped icons, update `PAGE_TITLE`
3. Open in browser to verify rendering
4. Summarize what was generated in text

## References Reference

Always load `references/icon-sources.md` into context when executing this skill. It contains the full icon catalog with SVG path data organized by semantic category, enabling rapid icon selection without external lookups.

## Fallback Behavior

- If an item has no obvious icon match in the reference catalog, use a generic icon (star, heart, bookmark) as the last option
- If the user provides fewer than 4 items, still generate 6 icons per item
- If the user provides more than 20 items, warn and ask to split into batches of 10

## Resources

### references/
- `icon-sources.md` — Full icon catalog organized by semantic category with SVG path data

### assets/
- `icons-template.html` — Canonical data-driven template file (based on `icons-api.html` format). Copy this to start a new icon set, then edit `ICON_GROUPS` and `PAGE_TITLE`. **Do NOT modify the rendering code or copy functions.**

### scripts/
- (No scripts needed — the icon mapping is done via reference lookup in context)
