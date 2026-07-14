#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
icon_cache.py — 生成期读取本地图标缓存，缺失时回退 CDN 实时抓取。

用法 (作为模块):
    import sys
    sys.path.insert(0, "<skill>/scripts")
    from icon_cache import get_icon
    paths = get_icon("IconPark", "People")        # inner-SVG 字符串 或 None

用法 (CLI):
    python icon_cache.py IconPark People
    python icon_cache.py "Huge Icons:Search01Icon"

设计: 优先读 assets/icon-cache.json（本地、快）；缓存未命中才联网兜底，
并建议随后运行 `python precache.py --source <源>` 把新图标写回缓存。
"""
import os
import sys
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_PATH = os.path.join(ROOT, "assets", "icon-cache.json")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import precache as P  # noqa: E402


def load_cache():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def get_icon(source, name, use_cdn_fallback=True):
    """返回某图标的 inner-SVG 字符串；未找到返回 None。"""
    cache = load_cache()
    src = cache.get(source, {})
    if name in src and src[name]:
        return src[name]
    if use_cdn_fallback:
        cfg = P.SOURCES.get(source)
        if cfg:
            txt = P.fetch_text(cfg["file_url"].format(name=name))
            if txt:
                return P.CONVERTERS[cfg["convert"]](txt)
    return None


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        src, nm = sys.argv[1], sys.argv[2]
    elif len(sys.argv) == 2 and ":" in sys.argv[1]:
        src, nm = sys.argv[1].split(":", 1)
    else:
        print("usage: python icon_cache.py <source> <name>")
        print("   or: python icon_cache.py \"<source>:<name>\"")
        sys.exit(1)
    res = get_icon(src, nm)
    print(res if res else "未命中缓存且 CDN 兜底失败: %s:%s" % (src, nm))
