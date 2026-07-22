#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_icons.py — text-to-icons 统一生成 / 追加 / 搜索 / 预览 CLI。

用法:
  # 全量生成（替换 ICON_GROUPS）
  python build_icons.py --groups groups.json --output icons.html

  # 追加模式（在现有 HTML 尾部插入新组）
  python build_icons.py --append groups.json --html existing.html

  # 搜索缓存（快速查找匹配图标）
  python build_icons.py --search "交通 基础设施"

  # 批量编排（单进程搜索多组；concepts=概念去重自动选取，keywords=排名候选）
  # 配合 --draft 直接写出 groups.json 草稿，供 --groups 立即构建
  python build_icons.py --plan plan.json --draft groups_draft.json

  # 启动本地预览服务器
  python build_icons.py --serve icons.html

groups.json 格式:
  [
    { "name": "交通基础设施",
      "icons": [["IconPark","Road"], ["Huge Icons","Road01Icon"], ...] },
    ...
  ]
"""

import os
import re
import sys
import json
import time
import http.server
import socketserver
from pathlib import Path
from typing import Optional

ROOT = Path(os.path.dirname(os.path.abspath(__file__))).parent
CACHE_PATH = ROOT / "assets" / "icon-cache.json"
TEMPLATE_PATH = ROOT / "assets" / "icons-template.html"

# ── 缓存 ──────────────────────────────────────────────────────
_cache: Optional[dict] = None

def cache():
    global _cache
    if _cache is None:
        _cache = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    return _cache


def sanitize_js(paths: str) -> str:
    """将 SVG inner HTML 转义为 JS 单引号字面量。"""
    s = re.sub(r'\s+', ' ', paths).strip()
    return s.replace('\\', '\\\\').replace("'", "\\'")


# ── 验证 ──────────────────────────────────────────────────────
def verify_icons(groups: list) -> bool:
    """检查所有图标在缓存中是否存在，缺失时打印并返回 False。"""
    ok = True
    c = cache()
    for g in groups:
        for src, name in g.get("icons", []):
            if src not in c or name not in c[src]:
                print(f"  ❌ MISSING: {src}:{name}", file=sys.stderr)
                ok = False
    return ok


# ── 生成 ICON_GROUPS JS ───────────────────────────────────────
def build_groups_js(groups: list) -> str:
    """从 groups 数据生成 const ICON_GROUPS = [...]; JS 代码块。"""
    c = cache()
    lines = ["const ICON_GROUPS = ["]
    for g in groups:
        lines.append("  {")
        lines.append(f'    name: "{g["name"]}",')
        lines.append("    icons: [")
        for src, name in g["icons"]:
            paths = sanitize_js(c[src][name])
            lines.append(f"      {{ paths: '{paths}', source: '{src}' }},")
        lines.append("    ]")
        lines.append("  },")
    lines.append("];")
    return "\n".join(lines)


# ── 模板操作 ──────────────────────────────────────────────────
def apply_template(groups: list, title: str) -> str:
    """生成完整 HTML 字符串。"""
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    groups_js = build_groups_js(groups)

    start = template.find("const ICON_GROUPS = [")
    end = template.find("];\n\n// ", start) + 2
    if start < 0 or end < 2:
        raise RuntimeError("模板中未找到 ICON_GROUPS 标记")

    html = template[:start] + groups_js + template[end:]
    html = html.replace("const PAGE_TITLE = '图标集';", f"const PAGE_TITLE = '{title}';")
    return html


def append_to_html(html_path: str, groups: list) -> tuple:
    """向已有 HTML 文件追加新组，返回 (新的 HTML 内容, 实际追加组数)。自动跳过已存在的同名组。"""
    html = Path(html_path).read_text(encoding="utf-8")

    # ── 去重检测：提取已有组名 ──
    existing_names = set()
    for m in re.finditer(r'name:\s*"([^"]+)"', html):
        existing_names.add(m.group(1))

    duplicates = [g["name"] for g in groups if g["name"] in existing_names]
    if duplicates:
        print(f"  ⚠️  跳过 {len(duplicates)} 个重复组: {', '.join(duplicates)}")
    groups_to_add = [g for g in groups if g["name"] not in existing_names]
    if not groups_to_add:
        print("  ⚠️  所有组名均已存在，无需追加")
        return html, 0

    groups_js = build_groups_js(groups_to_add)
    # 找 `const ICON_GROUPS` 块末尾的 `];\n\n// ` 标记
    pos = html.find("];\n\n// ", html.find("const ICON_GROUPS"))
    if pos < 0:
        raise RuntimeError("HTML 中未找到 ICON_GROUPS 插入点")
    # 在 `];` 前插入新组
    return html[:pos] + "\n" + groups_js.replace("const ICON_GROUPS = [\n", "  ").replace("\n];", "\n") + html[pos:], len(groups_to_add)


# ── 校验 ──────────────────────────────────────────────────────
def validate_js(html: str) -> bool:
    """提取 HTML 中 <script> 块并用 node --check 校验。"""
    import subprocess, tempfile
    m = re.search(r"<script>(.*?)</script>", html, re.DOTALL)
    if not m:
        print("❌ HTML 中未找到 <script>", file=sys.stderr)
        return False
    js = m.group(1)
    tf = tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False, encoding="utf-8")
    tf.write(js)
    tf.close()
    try:
        r = subprocess.run(["node", "--check", tf.name], capture_output=True, text=True)
        if r.returncode != 0:
            print(f"❌ JS 语法错误:\n{r.stderr}", file=sys.stderr)
            return False
        return True
    finally:
        os.unlink(tf.name)


# ── 搜索 ──────────────────────────────────────────────────────
def search_cache(query: str) -> dict:
    """按关键词模糊搜索缓存，返回 { source: { name: innerSVG } }。"""
    c = cache()
    keywords = [k.strip().lower() for k in query.split() if k.strip()]
    results = {}
    for src, icons in c.items():
        matches = {}
        for name, svg in icons.items():
            score = sum(1 for kw in keywords if kw in name.lower())
            if score > 0:
                matches[name] = (score, svg)
        if matches:
            results[src] = {n: svg for n, (s, svg) in sorted(matches.items(), key=lambda x: -x[1][0])[:30]}
    return results


def format_search_results(results: dict) -> str:
    """格式化搜索结果供终端输出。"""
    lines = []
    for src, matches in results.items():
        lines.append(f"\n{'='*60}")
        lines.append(f"  {src} ({len(matches)} matches)")
        lines.append(f"{'='*60}")
        for name in list(matches.keys())[:20]:
            lines.append(f"  {name}")
    return "\n".join(lines)


# ── 批量编排 ──────────────────────────────────────────────────
def search_icons_ranked(keywords: list) -> list:
    """跨全部源对关键词排名，返回 [(score, src, name), ...]（降序）。

    子串命中计 1 分；任一侧有词边界（前缀或后缀复合，如 friends⊂FriendsCircle、
    handshake⊂CooperativeHandshake）额外 +0.5 分，使精确 token 排序更靠前，
    从而把 trousers⊃users 之类的内部子串噪声压到候选列表下方，而非直接丢弃（避免漏匹配）。
    仅依赖全局 cache() 单例，整个 --plan 过程只加载一次 7MB+ JSON。
    """
    c = cache()
    kws = [k.strip().lower() for k in keywords if k.strip()]
    rows = []
    for src, icons in c.items():
        for name, svg in icons.items():
            if not svg or not svg.strip():
                continue
            n = name.lower()
            score = 0.0
            for kw in kws:
                if kw in n:
                    score += 1.0
                    lead = re.search(r"(?<![a-z])" + re.escape(kw), n)
                    trail = re.search(re.escape(kw) + r"(?![a-z])", n)
                    if lead or trail:
                        score += 0.5
            if score > 0:
                rows.append((score, src, name))
    rows.sort(reverse=True)
    return rows


def plan_icons(plan: list, top: int = 14, draft_path: str = None):
    """批量编排核心：单进程搜索多组，按组格式返回候选。

    plan 元素两种格式：
      A) concepts 模式（推荐）：
         {"name": "主任",
          "concepts": [{"concept": "authority", "keywords": ["crown","king"]}, ...]}
         → 每个概念按「首关键词优先 + IconPark 优先」选取首个存在的图标，
           跨概念按 name 去重，天然避免 Crown×3 撞车，且不会选到语义反例。
         → 若提供 draft_path，写出可直接 --groups 的 groups.json 草稿（需人工复审）。
      B) keywords 模式：
         {"name": "关于我们", "keywords": ["about","info","people"]}
         → 返回 TOP-N 排名候选，由 AI 人工定稿（不自动选取，避免语义撞车）。

    返回 (report_str, draft_groups_or_None)。
    """
    SOURCE_RANK = {"IconPark": 0, "Feather": 1, "Huge Icons": 2, "Lucide": 3}
    lines = []
    draft_groups = []

    def pick_for_concept(concept, keywords, used):
        """按概念关键词顺序选取 1 个图标：
        · 关键词按列表顺序即「贴合度」优先级（首个最贴切）；
        · 每关键词候选按 (源层级, 匹配分, 名长) 排序：IconPark 优先、词边界优先、同档取短名（基础图标优于复合变体）；
        · 优先采用词边界强匹配，命中即停；若某关键词仅产生弱子串命中则跳过，留给后续关键词；
          仅当所有关键词都无强匹配时，才回退首个关键词的弱命中（如 users⊂trousers 的极端情形）。
        跨概念按 name 去重。"""
        weak_fallback = None
        for kw in keywords:
            hits = []
            for score, src, name in search_icons_ranked([kw]):
                if name in used:
                    continue
                hits.append((SOURCE_RANK.get(src, 9), score, src, name, kw))
            if not hits:
                continue
            hits.sort(key=lambda e: (e[0], -e[1], len(e[3])))
            strong = [h for h in hits if h[1] >= 1.5]
            if strong:
                return (concept, strong[0][2], strong[0][3], strong[0][4])
            if weak_fallback is None:
                weak_fallback = hits[0]
        if weak_fallback:
            return (concept, weak_fallback[2], weak_fallback[3], weak_fallback[4])
        return None

    for grp in plan:
        gname = grp.get("name", "")
        if "concepts" in grp:
            chosen = []
            used = set()
            for c in grp["concepts"]:
                hit = pick_for_concept(c.get("concept", ""), c.get("keywords", []), used)
                if hit:
                    chosen.append(hit)
                    used.add(hit[2])
            comp = {}
            for _, src, _, _ in chosen:
                comp[src] = comp.get(src, 0) + 1
            ip = comp.get("IconPark", 0)
            flag = "" if len(chosen) == 6 else "  ⚠️不足6"
            lines.append(f"\n===== {gname} (概念去重选定 {len(chosen)} | IconPark={ip}){flag} =====")
            for concept, src, name, kw in chosen:
                lines.append(f"  {concept:<12} ({kw}) = {src}:{name}")
            if chosen:
                draft_groups.append({"name": gname, "icons": [[s, n] for _, s, n, _ in chosen]})
        else:
            rows = search_icons_ranked(grp.get("keywords", []))
            rows.sort(key=lambda r: (SOURCE_RANK.get(r[1], 9), -r[0]))
            rows = rows[:top]
            lines.append(f"\n===== {gname} (候选 TOP {len(rows)}) =====")
            for score, src, name in rows:
                lines.append(f"  {score:>4}  {src}:{name}")
    report = "\n".join(lines)
    if draft_path and draft_groups:
        Path(draft_path).write_text(
            json.dumps(draft_groups, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    return report, (draft_groups if draft_path else None)


# ── 预览服务器 ────────────────────────────────────────────────
class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # 静默日志


def serve_preview(html_path: str, port: int = 8765):
    """启动本地 HTTP 服务器预览 HTML。"""
    target = Path(html_path).resolve()
    os.chdir(target.parent)
    print(f"\n🔍 预览: http://localhost:{port}/{target.name}")
    print("   按 Ctrl+C 停止\n")
    with socketserver.TCPServer(("", port), QuietHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n已停止")


# ── CLI ────────────────────────────────────────────────────────
def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args or not args:
        print(__doc__)
        return

    # 搜索模式
    if "--search" in args:
        idx = args.index("--search")
        query = args[idx + 1] if idx + 1 < len(args) else ""
        if not query:
            print("请提供搜索关键词", file=sys.stderr)
            sys.exit(1)
        results = search_cache(query)
        if not results:
            print("未找到匹配图标")
        else:
            print(format_search_results(results))
        return

    # 批量编排模式
    if "--plan" in args:
        idx = args.index("--plan")
        plan_path = args[idx + 1] if idx + 1 < len(args) else ""
        if not plan_path or not os.path.exists(plan_path):
            print(f"JSON 文件不存在: {plan_path}", file=sys.stderr)
            sys.exit(1)
        plan = json.loads(Path(plan_path).read_text(encoding="utf-8"))
        top_idx = args.index("--top") if "--top" in args else -1
        top = int(args[top_idx + 1]) if top_idx >= 0 and top_idx + 1 < len(args) else 14
        draft_idx = args.index("--draft") if "--draft" in args else -1
        draft_path = args[draft_idx + 1] if draft_idx >= 0 and draft_idx + 1 < len(args) else None
        report, _ = plan_icons(plan, top=top, draft_path=draft_path)
        print(report)
        if draft_path:
            print(f"\n✅ 已写草稿组 → {draft_path}（仅 concepts 组；keywords 组需人工定稿）")
        return

    # 预览模式
    if "--serve" in args:
        idx = args.index("--serve")
        path = args[idx + 1] if idx + 1 < len(args) else ""
        if not path or not os.path.exists(path):
            print(f"文件不存在: {path}", file=sys.stderr)
            sys.exit(1)
        serve_preview(path)
        return

    # 追加模式
    if "--append" in args:
        idx = args.index("--append")
        json_path = args[idx + 1] if idx + 1 < len(args) else ""
        html_idx = args.index("--html") if "--html" in args else -1
        html_path = args[html_idx + 1] if html_idx >= 0 and html_idx + 1 < len(args) else ""

        if not json_path or not os.path.exists(json_path):
            print(f"JSON 文件不存在: {json_path}", file=sys.stderr)
            sys.exit(1)
        if not html_path or not os.path.exists(html_path):
            print(f"HTML 文件不存在: {html_path}", file=sys.stderr)
            sys.exit(1)

        groups = json.loads(Path(json_path).read_text(encoding="utf-8"))
        if not verify_icons(groups):
            sys.exit(1)

        html, added = append_to_html(html_path, groups)
        Path(html_path).write_text(html, encoding="utf-8")
        print(f"✅ 已追加 {added} 组到 {html_path}")
        if validate_js(html):
            print("✅ JS 语法通过")
        else:
            sys.exit(1)
        return

    # 全量生成模式
    if "--groups" in args:
        idx = args.index("--groups")
        json_path = args[idx + 1] if idx + 1 < len(args) else ""
        out_idx = args.index("--output") if "--output" in args else -1
        out_path = args[out_idx + 1] if out_idx >= 0 and out_idx + 1 < len(args) else "icons.html"
        title_idx = args.index("--title") if "--title" in args else -1
        title = args[title_idx + 1] if title_idx >= 0 and title_idx + 1 < len(args) else "图标集"

        if not json_path or not os.path.exists(json_path):
            print(f"JSON 文件不存在: {json_path}", file=sys.stderr)
            sys.exit(1)

        groups = json.loads(Path(json_path).read_text(encoding="utf-8"))
        if not verify_icons(groups):
            sys.exit(1)

        html = apply_template(groups, title)
        Path(out_path).write_text(html, encoding="utf-8")
        print(f"✅ 已生成 {len(groups)} 组 → {out_path}")
        if validate_js(html):
            print("✅ JS 语法通过")
        else:
            sys.exit(1)
        return

    print("未知参数，使用 --help 查看用法", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
