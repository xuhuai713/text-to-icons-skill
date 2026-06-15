---
name: text-to-icons
description: Convert user-provided text into matching linear icons, presented as an interactive HTML with one-click SVG copying. Uniform 24×24 viewBox, 0.5pt stroke for both display and clipboard. Default color: #000000.
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
| **IconPark** | Apache 2.0 | 48×48 | 4 → 3 | Fetch JS module, convert fill→none, stroke-width 3 |
| **Iconoir** | MIT | 24×24 | 1.5 | Fetch raw SVG, convert currentColor→#000000 |

**IconPark fetch pattern:**
```bash
curl -sL "https://unpkg.com/@icon-park/svg@1.4.2/es/icons/<PascalCaseName>.js"
```
- Icon names are PascalCase (e.g., `ProcessLine`, `DataServer`, `CodeComputer`)
- **Conversion required**: Output uses 48×48 viewBox with both `fill` and `stroke`. For linear output:
  - Keep `viewBox="0 0 48 48"`
  - Set `fill="none"`, `stroke="#000000"`, `stroke-width="3"`
  - Remove `fill="colors[1]"` and `stroke="colors[1]"` properties — set all to `fill="none" stroke="#000000"`
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

**Iconoir fetch pattern:**
```bash
curl -sL "https://cdn.jsdelivr.net/npm/iconoir@7.11.0/icons/regular/<name>.svg"
```
- Icon names are kebab-case (e.g., `bright-star`, `book-stack`, `open-in-window`)
- **Conversion required**: Change `stroke="currentColor"` to `stroke="#000000"`; add `stroke-linecap="round" stroke-linejoin="round"` if missing
- The raw SVG is 24×24 with `stroke-width="1.5"` — minimal conversion needed
- Search available icons: `grep -i '<keyword>'` on the regular/ directory listing

### Step 4: Generate the HTML Output

Generate a single self-contained HTML file with these requirements:

**Structure:**
- Single card/block per item with the item name and **6 icon options**
- Responsive grid layout (1 column on mobile, **6 columns for icons on desktop** — or 3 rows × 2 columns on tablet)
- Clean, professional design with subtle card styling

**Copy-to-clipboard feature:**
- Each icon has a "Copy SVG" button
- On click, copies the raw SVG code (with `<svg>` tag and all attributes) to clipboard
- Show a brief "已复制!" / "Copied!" feedback animation
- Use `navigator.clipboard.writeText()` with a `<textarea>` fallback
- **CRITICAL: No hidden SVGs** — copy function reads SVG paths directly from the visible `<svg>` element using `viewSvg.innerHTML`. Do NOT store duplicate SVG data in hidden elements; this caused border rendering issues and doubled file size.
- **Color handling**: Copy function reads the `stroke` attribute from the visible SVG to use in the output. Never use `stroke="currentColor"` — some apps (WeChat, Feishu) can't resolve this CSS keyword and render nothing.
- **Stroke width**: Display and copy both use `0.5pt` (via `COPY_STROKE_WIDTH` variable). Uniform across all icon sources.

**SVG format rules:**
- **Uniform 24×24 viewBox** for ALL icons (Feather, Lucide, Phosphor, Iconoir). 
- **IconPark 48×48 icons**: Wrap original 48×48 paths in `<g transform="scale(0.5)" stroke-width="1">` to scale into 24×24 viewBox.
- **Uniform stroke-width="0.5"** for ALL display SVGs and copied SVGs.
- `fill="none"`, `stroke="#000000"`, `stroke-linecap="round"`, `stroke-linejoin="round"` on all SVG tags
- Copied SVG **must include** `xmlns="http://www.w3.org/2000/svg"`, `viewBox="0 0 24 24"`, and **`width="24pt" height="24pt"`** to ensure PPT imports at consistent size and stroke weight
- `stroke-linecap="round"` and `stroke-linejoin="round"` on SVG tag
- Width/height for display: `w-10 h-10` (Tailwind) or `width="40" height="40"`
- **Color customization**: Default stroke color is `#000000`. If the user provides a custom hex color (e.g. "#ff6600" or "red"), use it for all icon strokes.
- **Stroke width customization**: Default copy stroke is `0.5`. Update the `COPY_STROKE_WIDTH` variable to change.

**Styling defaults:**
- Light theme (slate/white background)
- Tailwind CSS via CDN for layout (`<script src="https://cdn.tailwindcss.com"></script>`)
- Card hover: slight lift with shadow
- Copy button: border style, transitions smoothly to "Copied" state
- Step numbers displayed with gradient badges
- **Source attribution**: Each icon card must display a small tag/badge showing which icon library it comes from (`Feather`, `Lucide`, `Phosphor`, `IconPark`, `Iconoir`) — this builds user trust and clarifies licensing
- **Icon color**: All displayed and copied SVGs use `#000000` as default stroke color. If the user specifies a custom color, apply it globally (display SVGs + copy output).

### Step 5: Deliver

1. Write the HTML to `icons.html` in the workspace root
2. Use `preview_url` to show it in the browser
3. Summarize what was generated in text

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
- (No assets needed — everything is generated programmatically)

### scripts/
- (No scripts needed — the icon mapping is done via reference lookup in context)
