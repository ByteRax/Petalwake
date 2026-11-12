#!/usr/bin/env python3
"""Download the game's ./assets tree: fixed manifest first, then recurse into JSON references."""
import json
import os
import posixpath
import re
import sys
import urllib.request

BASE = "https://petalwake.non.io/v2/"
OUT = "/Users/smzdm/Projects/AI/Re/Petalwake/site"
UA = {"User-Agent": "Mozilla/5.0"}

queue = [
    "assets/terrain/meta.json",
    "assets/terrain/height.u16",
    "assets/terrain/splat.png",
    "assets/terrain/light.png",
    "assets/terrain/tint.png",
    "assets/terrain/props.json",
    "assets/textures/materials.json",
    "assets/town/index.json",
    "assets/town/masks.json",
    "assets/town/tex/materials.json",
    "assets/shore/shore.json",
    "assets/shore/shore.bin",
    "assets/models/rider.glb",
    "assets/models/rider.json",
    "assets/places/west.json",
    "assets/places/east.json",
    "assets/materials.json",  # may not exist
]
seen, failed, ok = set(), [], []

EXT = re.compile(r"\.(glb|gltf|bin|u16|png|jpg|jpeg|webp|ktx2|json|mp3|ogg|wav)$", re.I)
STR = re.compile(r'"([^"\\]{1,200})"')


def fetch(rel):
    if rel in seen:
        return None
    seen.add(rel)
    req = urllib.request.Request(BASE + rel, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        seen.discard(rel)
        if e.code != 404:
            failed.append((rel, f"HTTP {e.code}"))
        else:
            print(f"   404  {rel}")
        return None
    except Exception as e:
        failed.append((rel, str(e)))
        return None
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb") as f:
        f.write(data)
    ok.append(rel)
    print(f"{len(data):>9}  {rel}")
    return data


def add(rel):
    if rel and rel not in seen:
        queue.append(rel)


def resolve(json_rel, s):
    """Resolve a string found in a JSON file into an asset path (if it looks like one)."""
    if not EXT.search(s):
        return None
    if s.startswith(("http", "data:")):
        return None
    d = posixpath.dirname(json_rel)
    path = posixpath.normpath(posixpath.join(d, s)) if not s.startswith("/") else s
    return path.lstrip("/")


while queue:
    rel = queue.pop(0)
    data = fetch(rel)
    if data is None:
        continue
    # derived files
    if rel == "assets/town/index.json":
        try:
            idx = json.loads(data)
            for t in idx.get("towns", []):
                add(f"assets/town/{t['id']}.json")
                add(f"assets/town/{t['id']}.bin")
        except Exception as e:
            failed.append((rel + " [parse index]", str(e)))
    elif rel == "assets/town/masks.json":
        try:
            masks = json.loads(data)
            for m in masks.values():
                if isinstance(m, dict) and m.get("file"):
                    add(f"assets/town/{m['file']}")
        except Exception as e:
            failed.append((rel + " [parse masks]", str(e)))
    elif rel.endswith("materials.json"):
        try:
            meta = json.loads(data)
            d = posixpath.dirname(rel)
            for name in meta.get("order", []):
                add(f"{d}/{name}_c.webp")
                add(f"{d}/{name}_n.webp")
        except Exception as e:
            failed.append((rel + " [parse materials]", str(e)))
    elif rel.endswith(".json"):
        # generic: scan all strings for path-like values
        try:
            obj = json.loads(data)
            for s in STR.findall(data.decode("utf-8", "replace")):
                r = resolve(rel, s)
                if r:
                    add(r)
        except Exception as e:
            failed.append((rel + " [scan]", str(e)))
    # town json has a .bin sibling built in code
    m = re.match(r"assets/town/([^/]+)\.json$", rel)
    if m:
        add(f"assets/town/{m.group(1)}.bin")

print("\n--- FAILED ---")
for rel, err in failed:
    print(f"{rel}: {err}")
print(f"\nOK {len(ok)} files")
