#!/usr/bin/env python3
"""Translate the treasure item name + lore inside each place definition."""
import json

SITE = "/Users/smzdm/Projects/AI/Re/Petalwake/site"

TREASURES = {
    # place id -> (treasure name, lore)
    "blossom_sister": ("未洒之盏",
                       "任凭狂风在姐妹石四周呼啸，这只杯里的茶从未起过一丝涟漪。"),
    "farewell_bridge": ("初雨顶针",
                        "仍盛满这座岛落下的第一场雨。从那时起，它就一直在设法奔向大海。"),
    "shipless_mast": ("疾风哨",
                      "吹响一次，风会记得你的名字。吹响两次，风就会来找你。"),
    "marigold_wreck": ("七潮之结",
                       "有人想留住大海，把七次潮汐系进了这根绳子里。至今没人敢把它解开。"),
    "clock_meadow": ("溜走的时辰",
                     "一只黄铜沙漏，沙子极慢地向上涨。从没有人见过它流完。"),
    "open_hand": ("风暴弹珠",
                  "一颗玻璃弹珠，里面关着拇指大的雷雨。巨人输掉了那局游戏，却留下了奖品。"),
    "wish_pine": ("御风铃",
                  "一只被拇指磨亮的青铜铃，没有铃舌。可在风改变主意的夜晚，松树仍会摇响它。"),
    "kettle_pools": ("余温之卵",
                     "一颗从未凉过的河石。牧羊人把它揣在怀里度过七个冬天，还为该谁保管争个不停。"),
    "starfall": ("天穹碎片",
                 "坠落的星辰留下的一片碎屑。贴在耳边，还能听见它坠落时那一声嗡鸣。"),
    "conch_garden": ("月华珠",
                     "满月照到一粒沙，潮汐用一百年把它裹成了珍珠。"),
    "lantern_roots": ("渡灯",
                      "一盏比渡口更老的灯，那时还没有可以对岸的镇子。它一生只需要点一次。"),
    "whalebone_arbour": ("歌之骨",
                         "一块鲸的耳骨，被潮水磨得温润。无风的傍晚，它会慢慢还回听过的歌。"),
}

for set_name in ("west", "east"):
    path = f"{SITE}/assets/places/{set_name}.json"
    d = json.load(open(path, encoding="utf-8"))
    for p in d["places"]:
        t = p.get("treasure")
        if not t:
            continue
        zh = TREASURES[p["id"]]
        assert t["name"], p["id"]
        t["name"], t["lore"] = zh
    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"ok {set_name}")
print("done")
