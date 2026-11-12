#!/usr/bin/env python3
"""Translate in-game names in assets JSONs: towns, pads (name+spot), treasure places (name+hint)."""
import json

SITE = "/Users/smzdm/Projects/AI/Re/Petalwake/site"

TOWN_NAMES = {
    "Larkhaven": "云雀港",
    "Cairnwick": "石冢村",
    "The Meadows": "草甸原",
}

PAD_NAMES = {
    "The Star-gazer's Tower": "观星塔",
    "The Hill Gate": "丘门",
    "The Couriers' Guild": "信使公会",
    "Larkhaven Town Hall": "云雀港市政厅",
    "The Chapel Bell Tower": "礼拜堂钟楼",
    "Harbourmaster's Tower": "港务长塔",
    "The Huer's Lookout": "渔汛瞭望塔",
    "Larkhaven Customs House": "云雀港海关",
    "The Terrace Tea House": "临台茶馆",
    "The Shot Tower": "制弹塔",
    "The Carrier's Deck": "货运平台",
    "The Crow's Nest": "鸦巢瞭望台",
    "The Notary's Stair": "公证人阶梯",
    "The Dyers' Drying Tower": "染坊晾晒塔",
    "The Warden's Tower-house": "守卫塔楼",
    "The Dovecote": "鸽舍",
    "The Lookout": "瞭望台",
    "The Old Keep Hostel": "旧堡旅舍",
    "The Notary's Tower-house": "公证人塔楼",
    "The Cistern Tower": "蓄水塔",
    "The Pilot's Tower-house": "引航员塔楼",
    "The Scholars' Library": "学者图书馆",
    "The Lamp House": "灯房",
    "The Harbour Light": "港湾灯塔",
    "Cairnwick Signal Tower": "石冢村信号塔",
    "Whale-watchers' Lookout": "观鲸瞭望台",
    "Cairnwick Wind Pump": "石冢村风泵塔",
    "The Last Lantern": "最后一盏灯",
    "The Weather House": "气象屋",
    "Twin Cowls Oast": "双帽烘塔",
    "Pippin Cote": "苹果园农舍",
    "Whitecap Mill": "白帽磨坊",
    "Harrow Beacon": "哈罗信标",
    "The Candle Stump": "烛台树桩",
    "Heron's Perch": "苍鹭栖架",
}

PAD_SPOTS = {
    "Dome gallery": "穹顶环廊",
    "Gate wall-walk": "城门墙道",
    "Couriers' Guild gallery": "信使公会环廊",
    "Town hall belfry gallery": "市政厅钟楼环廊",
    "Chapel bell tower belfry": "礼拜堂钟室",
    "Harbourmaster's gallery": "港务长环廊",
    "The Huer's Lookout": "渔汛瞭望台",
    "Customs House walk": "海关走道",
    "Tea house roof terrace": "茶馆屋顶露台",
    "Hoist stage": "吊台",
    "Carrier's deck": "货运甲板",
    "Crow's nest": "鸦巢",
    "Notary's leads": "公证人塔顶",
    "Wind deck": "迎风平台",
    "Warden's terrace": "守卫露台",
    "Lantern walk": "提灯走道",
    "The lookout": "瞭望位",
    "Hostel veranda": "旅舍游廊",
    "Turret gallery": "角塔环廊",
    "Cistern roof": "水柜顶",
    "Library balcony": "图书馆阳台",
    "The lamp walk": "灯行走道",
    "The Harbour Light": "港湾灯位",
    "Signal gallery": "信号环廊",
    "Lookout stage": "瞭望平台",
    "Pump stage": "泵台",
    "Roof gallery": "屋顶环廊",
    "Roof walk": "屋顶走道",
    "Loading platform": "装卸平台",
    "Alighting ledge": "落脚檐台",
    "Mill stage": "磨坊平台",
    "Beacon top": "信标顶",
    "Wall-head": "墙头",
}

PLACES = {
    "west": [
        ("The Blossom Sister", "繁花姐妹石",
         "姐妹石中的一座，立在页岩海岸以北，四季都开着粉花。"),
        ("Farewell Bridge", "告别桥",
         "在河流坠下断崖前的最后一步，有什么紫色的东西悬在水面上。"),
        ("The Shipless Mast", "无船之桅",
         "灯笼岬的脊线上，一根桅杆仍扬着旗，桅下却无船。"),
        ("The Wreck of the Marigold", "金盏花号残骸",
         "很久以前，一艘蓝色小船搁浅在长沙岸，从此开花不断。"),
        ("The Clock Meadow", "时钟草甸",
         "西山坳里的蒲公英长得比骑手还高，而且仍然按时报时。"),
        ("The Open Hand", "张开的手掌",
         "西侧悬崖上，一只石凿的手仍向大海伸出。"),
    ],
    "east": [
        ("The Thousand-Wish Pine", "千愿松",
         "在山的西肩高处，有什么东西在飘动——那不是叶子。"),
        ("The Kettle Pools", "茶壶泉池",
         "东麓一道绿色的褶皱里，山坡藏着一挂温热的蓝色水梯。"),
        ("Starfall", "坠星",
         "很久以前，有什么东西坠在东北草甸上，落下时还从崖壁上咬掉了一口。"),
        ("The Conch Garden", "海螺园",
         "最小的岛上守着最大的海螺，还有人在它周围种起了花木。"),
        ("Lantern Roots", "灯笼树根",
         "一棵树蹚进潟湖后再没回来。仍有人为它点灯。"),
        ("The Whalebone Arbour", "鲸骨藤架",
         "在东南的绵长沙滩上，一位巨大的旅人安息着，它曾歌唱过的地方开满了海石竹。"),
    ],
}


def load(rel):
    with open(f"{SITE}/{rel}", encoding="utf-8") as f:
        return json.load(f)


def save(rel, obj):
    with open(f"{SITE}/{rel}", "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"ok {rel}")


# 城镇 index + 各城镇 json
idx = load("assets/town/index.json")
for t in idx["towns"]:
    t["name"] = TOWN_NAMES[t["name"]]
save("assets/town/index.json", idx)

for tid, tname in [("larkhaven", "Larkhaven"), ("cairnwick", "Cairnwick"), ("fields", "The Meadows")]:
    t = load(f"assets/town/{tid}.json")
    assert t["name"] == tname
    t["name"] = TOWN_NAMES[tname]
    for p in t["pads"]:
        p["name"] = PAD_NAMES[p["name"]]
        if p.get("spot"):
            p["spot"] = PAD_SPOTS[p["spot"]]
    save(f"assets/town/{tid}.json", t)

# 宝藏地点
for set_name, items in PLACES.items():
    d = load(f"assets/places/{set_name}.json")
    for p, (en, zh, hint) in zip(d["places"], items):
        assert p["name"] == en, f"{p['name']} != {en}"
        p["name"] = zh
        p["hint"] = hint
    save(f"assets/places/{set_name}.json", d)

print("all done")
