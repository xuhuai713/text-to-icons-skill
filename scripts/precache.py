#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
precache.py — 为 text-to-icons 技能构建本地图标缓存。

从 CDN 并发抓取 IconPark / Huge Icons / Lucide / Feather，
将每个图标转换为统一格式的 inner-SVG（不含 <svg> 外壳），
写入 assets/icon-cache.json。生成时优先读本地缓存，无需联网。

用法:
  python precache.py                 # 增量：跳过已缓存的图标
  python precache.py --force         # 忽略现有缓存，全量重建
  python precache.py --source IconPark   # 仅刷新某个源
  python precache.py --lookup "IconPark:People"  # 查询并打印某图标 inner-SVG

输出:
  assets/icon-cache.json  ->  { "<源名>": { "<图标名>": "<innerSVG>" } }

源名与 ICON_GROUPS[].icons[].source 字段保持一致:
  "IconPark" / "Feather" / "Lucide" / "Huge Icons"
"""
import os
import re
import sys
import json
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_PATH = os.path.join(ROOT, "assets", "icon-cache.json")
WORKERS = 24
TIMEOUT = 30
RETRIES = 3

# ---- 源定义 -------------------------------------------------------------
# list_url: jsdelivr meta API（递归列出文件树）
# list_prefix/list_suffix: 过滤目标文件，并从中截取图标名
# file_url: 实际抓取单个图标的 URL 模板
SOURCES = {
    "IconPark": {
        "list_url": "https://data.jsdelivr.com/v1/packages/npm/@icon-park/svg@1.4.2",
        "list_prefix": "es/icons/",
        "list_suffix": ".js",
        "file_url": "https://cdn.jsdelivr.net/npm/@icon-park/svg@1.4.2/es/icons/{name}.js",
        "convert": "iconpark",
    },
    "Huge Icons": {
        "list_url": "https://data.jsdelivr.com/v1/packages/npm/@hugeicons/core-free-icons@4.2.2",
        "list_prefix": "dist/esm/",
        "list_suffix": ".js",
        "file_url": "https://cdn.jsdelivr.net/npm/@hugeicons/core-free-icons@4.2.2/dist/esm/{name}.js",
        "convert": "huge",
    },
    "Lucide": {
        "list_url": "https://data.jsdelivr.com/v1/packages/npm/lucide-static@0.469.0",
        "list_prefix": "icons/",
        "list_suffix": ".svg",
        "file_url": "https://cdn.jsdelivr.net/npm/lucide-static@0.469.0/icons/{name}.svg",
        "convert": "lucide",
    },
    "Feather": {
        "list_url": "https://data.jsdelivr.com/v1/packages/npm/feather-icons@4.29.0",
        "list_prefix": "dist/icons/",
        "list_suffix": ".svg",
        "file_url": "https://cdn.jsdelivr.net/npm/feather-icons@4.29.0/dist/icons/{name}.svg",
        "convert": "feather",
    },
}


# ---- 网络 ---------------------------------------------------------------
def fetch_text(url):
    last = None
    for i in range(RETRIES):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "text-to-icons-precache/1.0"})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return r.read().decode("utf-8")
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(0.4 * (i + 1))
    return None


def list_icon_names(meta_url, prefix, suffix):
    """递归遍历 jsdelivr meta JSON，返回去掉 prefix/suffix 后的图标名列表。"""
    txt = fetch_text(meta_url)
    if not txt:
        return []
    meta = json.loads(txt)
    files = []

    def walk(node, prefix=""):
        if node.get("type") == "file":
            files.append(prefix + node["name"])
        for child in node.get("files", []):
            walk(child, prefix + node.get("name", "") + "/")

    for top in meta.get("files", []):
        walk(top)

    names = []
    for f in files:
        if f.startswith(prefix) and f.endswith(suffix):
            names.append(f[len(prefix):-len(suffix)])
    return names


# ---- 转换器 -------------------------------------------------------------
def convert_iconpark(js):
    m = re.search(r"return (.+?);\s*\}\);", js, re.DOTALL)
    if not m:
        m = re.search(r"return (.+);", js, re.DOTALL)
    if not m:
        return None
    expr = m.group(1)
    for a, b in [
        ('props.colors[0]', '"#000000"'),
        ('props.colors[1]', '"#000000"'),
        ('props.colors[2]', '"#000000"'),
        ('props.colors[3]', '"#000000"'),
        ('props.strokeWidth', '"4"'),
        ('props.size', '"48"'),
        ('props.strokeLinecap', '"round"'),
        ('props.strokeLinejoin', '"round"'),
    ]:
        expr = expr.replace(a, b)
    try:
        svg = eval(expr)  # noqa: S307 - trusted CDN content
    except Exception:  # noqa: BLE001
        return None
    svg = re.sub(r'<\?xml[^>]+\?>', '', svg)
    inner = re.sub(r'<svg[^>]*>', '', svg)
    inner = re.sub(r'</svg>', '', inner)
    # 颜色槽 → 线性描边
    inner = inner.replace('fill="#000000"', 'fill="none" stroke="#000000"')
    inner = inner.replace('stroke="#000000" stroke="#000000"', 'stroke="#000000"')
    inner = inner.replace('fill="none" stroke="#000000" stroke="#000000"', 'fill="none" stroke="#000000"')
    # 去除子元素 stroke-width（由外层 g 继承）
    inner = re.sub(r'\s+stroke-width="\d+"', '', inner)
    return '<g transform="scale(0.5)" stroke-width="3">' + inner.strip() + '</g>'


def convert_huge(js):
    m = re.search(r'=\s*(\[.*?\]);', js, re.DOTALL)
    if not m:
        return None
    raw = m.group(1)
    # JS 对象键未加引号（如 { d: "..." }），eval 前先补引号
    quoted = re.sub(r'([{,]\s*)([A-Za-z_$][\w$]*)(\s*:)', r'\1"\2"\3', raw)
    try:
        arr = eval(quoted)  # noqa: S307 - trusted CDN content
    except Exception:  # noqa: BLE001
        return None
    parts = []
    for elem in arr:
        if not isinstance(elem, (list, tuple)) or len(elem) != 2:
            continue
        tag, attrs = elem
        attrs = dict(attrs)
        attrs.pop("key", None)
        kebab = {}
        for k, v in attrs.items():
            kk = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', str(k)).lower()
            if kk == "stroke-width":
                continue  # 由模板外壳控制
            if kk == "stroke" and v == "currentColor":
                v = "#000000"
            kebab[kk] = str(v)
        attrs_str = " ".join(f'{k}="{v}"' for k, v in kebab.items())
        parts.append(f'<{tag} {attrs_str}/>')
    return "".join(parts)


def convert_lucide(svg):
    inner = re.sub(r'<!--[^>]*-->', '', svg)  # 去除 license 注释
    inner = re.sub(r'<svg[^>]*>', '', inner)
    inner = re.sub(r'</svg>', '', inner)
    inner = re.sub(r'\s+stroke-width="\d+"', '', inner)
    inner = inner.replace('fill="currentColor"', 'fill="none"')
    inner = inner.replace('stroke="currentColor"', 'stroke="#000000"')
    return inner.strip()


def convert_feather(svg):
    inner = re.sub(r'<svg[^>]*>', '', svg)
    inner = re.sub(r'</svg>', '', inner)
    inner = re.sub(r'\s+stroke-width="\d+"', '', inner)
    inner = inner.replace('fill="currentColor"', 'fill="none"')
    inner = inner.replace('stroke="currentColor"', 'stroke="#000000"')
    return inner.strip()


CONVERTERS = {
    "iconpark": convert_iconpark,
    "huge": convert_huge,
    "lucide": convert_lucide,
    "feather": convert_feather,
}


# ---- 缓存读写 -----------------------------------------------------------
def load_cache():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(cache):
    tmp = CACHE_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, separators=(",", ":"))
    os.replace(tmp, CACHE_PATH)


# ---- 构建 ---------------------------------------------------------------
def build_source(source_name, source_cfg, cache, force):
    names = list_icon_names(source_cfg["list_url"], source_cfg["list_prefix"], source_cfg["list_suffix"])
    if not names:
        print(f"  [!] {source_name}: 未能列出图标（网络/API 异常）")
        return 0, 0
    existing = cache.get(source_name, {})
    todo = [n for n in names if force or n not in existing or not existing[n]]
    print(f"  [*] {source_name}: 共 {len(names)} 个，需抓取 {len(todo)} 个")

    conv = CONVERTERS[source_cfg["convert"]]
    done = 0
    failed = 0
    new_entries = {}

    def worker(name):
        txt = fetch_text(source_cfg["file_url"].format(name=name))
        if txt is None:
            return name, None
        return name, conv(txt)

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futures = [ex.submit(worker, n) for n in todo]
        total = len(futures)
        for i, fut in enumerate(as_completed(futures), 1):
            name, result = fut.result()
            if result:
                new_entries[name] = result
                done += 1
            else:
                failed += 1
            if i % 200 == 0 or i == total:
                print(f"      ...{i}/{total}  ok={done} fail={failed}")

    cache.setdefault(source_name, {})
    cache[source_name].update(new_entries)
    return done, failed


# ---- 查询 ---------------------------------------------------------------
def lookup(source, name):
    cache = load_cache()
    return cache.get(source, {}).get(name)


# ---- 主流程 -------------------------------------------------------------
def main():
    args = sys.argv[1:]
    force = "--force" in args
    lookup_arg = None
    source_filter = None
    for a in args:
        if a.startswith("--lookup"):
            lookup_arg = a.split("=", 1)[1] if "=" in a else args[args.index(a) + 1]
        elif a.startswith("--source"):
            source_filter = a.split("=", 1)[1] if "=" in a else args[args.index(a) + 1]

    if lookup_arg:
        if ":" in lookup_arg:
            src, nm = lookup_arg.split(":", 1)
        else:
            src, nm = "IconPark", lookup_arg
        res = lookup(src, nm)
        if res:
            print(res)
        else:
            print(f"未命中缓存: {src}:{nm}")
        return

    cache = load_cache()
    targets = {source_filter: SOURCES[source_filter]} if source_filter else SOURCES
    print(f"precache 开始 (force={force}, workers={WORKERS})")
    for sname, scfg in targets.items():
        t0 = time.time()
        done, failed = build_source(sname, scfg, cache, force)
        print(f"  [✓] {sname}: 新增 {done}, 失败 {failed}, 耗时 {time.time()-t0:.1f}s")
        save_cache(cache)  # 每个源结束后落盘，防止中断丢失

    total = sum(len(v) for v in cache.values())
    print(f"precache 完成。缓存总计 {total} 个图标 -> {CACHE_PATH}")


if __name__ == "__main__":
    main()
