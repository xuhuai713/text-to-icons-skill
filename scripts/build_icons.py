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
