#!/usr/bin/env python3
"""Recursive mirror of a static ES-module site: parses JS/CSS for relative imports and assets."""
import posixpath
import re
import sys
import urllib.parse
import urllib.request

BASE = "https://petalwake.non.io/v2/"
OUT = "/Users/smzdm/Projects/AI/Re/Petalwake/site"

ASSET_EXT = re.compile(
    r"\.(js|mjs|css|html|json|glb|gltf|bin|png|jpg|jpeg|webp|ktx2|basis|hdr|exr|mp3|ogg|wav|m4a|frag|vert|glsl|svg|ico|woff2?|ttf)($|\?)",
    re.I,
)

queue = ["index.html"]
seen = set()
failed = []

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}

# patterns that yield quoted relative specifiers from JS
JS_PATTERNS = [
    re.compile(r"""\bfrom\s*['"]([^'"]+)['"]"""),
    re.compile(r"""\bimport\s*['"]([^'"]+)['"]"""),
    re.compile(r"""\bimport\s*\(\s*['"]([^'"]+)['"]"""),
    re.compile(r"""new\s+URL\(\s*['"]([^'"]+)['"]"""),
    re.compile(r"""(?<![\w./])['"](\.{0,2}/[^'"]+\.(?:js|mjs|json|glb|gltf|bin|png|jpg|jpeg|webp|ktx2|hdr|exr|mp3|ogg|wav|frag|vert|glsl))['"]""", re.I),
]
CSS_PATTERNS = [
    re.compile(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)"),
    re.compile(r"""@import\s+['"]([^'"]+)['"]"""),
]
HTML_PATTERNS = [
    re.compile(r"""(?:src|href)\s*=\s*["']([^"']+)["']"""),
    re.compile(r"""content\s*=\s*["'](https?://[^"']+)["']"""),
]


def resolve(base_dir, spec):
    if spec.startswith(("http://", "https://", "data:", "//")):
        return None
    spec = spec.split("?")[0].split("#")[0]
    if not ASSET_EXT.search(spec):
        return None
    path = posixpath.normpath(posixpath.join(base_dir, spec))
    return path.lstrip("/")


def fetch(rel):
    url = BASE + rel
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
    except Exception as e:
        failed.append((rel, str(e)))
        return None
    import os
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb") as f:
        f.write(data)
    print(f"{len(data):>9}  {rel}")
    return data


while queue:
    rel = queue.pop(0)
    if rel in seen:
        continue
    seen.add(rel)
    data = fetch(rel)
    if data is None:
        continue
    base_dir = posixpath.dirname(rel)
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        continue
    pats = []
    if rel.endswith((".js", ".mjs")):
        pats = JS_PATTERNS
    elif rel.endswith(".css"):
        pats = CSS_PATTERNS
    elif rel.endswith(".html"):
        pats = HTML_PATTERNS
    for pat in pats:
        for spec in pat.findall(text):
            r = resolve(base_dir, spec)
            if r and r not in seen:
                queue.append(r)

print("\n--- FAILED ---")
for rel, err in failed:
    print(f"{rel}: {err}")
print(f"\nDownloaded {len(seen) - len(failed)} files, {len(failed)} failed")
