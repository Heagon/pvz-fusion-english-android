"""Safe in-place patch of Chinese string literals in IL2CPP global-metadata.dat.

Only replaces a literal when the English encodes to <= the original byte length,
overwriting the bytes and updating the per-literal length field. No section is
resized and no header offset changes -> cannot corrupt the metadata layout.

Sources: mod translation_strings + plant/zombie names + curated HUD overrides.

Usage: python patch_metadata.py <in_metadata> <out_metadata>
"""
import struct
import re
import json
import sys

MOD = r"./PvZ_Fusion_Translator"
EN = MOD + r"/Localization/English"
CJK = re.compile(r'[一-鿿㐀-䶿]')

# curated HUD / notification / category overrides (each English must be <= CN byte length)
HUD = {
    "难度：{0}": "Diff: {0}", "章节难度：{0}": "Ch.Diff: {0}", "难度阶数：{0}": "Diff Tier:{0}",
    "章节难度：{0}+2": "Ch.Diff: {0}+2", "，推荐难度：": ", Rec. Diff:",
    "第{0}关": "Lvl {0}", "第{0}波": "Wave {0}", "第{0}轮": "Round {0}", "第{0}行": "Row {0}",
    "第{0}路": "Lane {0}", "第{0}页": "Page {0}", " 第{0}轮": " Round {0}",
    "波次：{0}/{1}": "Wave: {0}/{1}", "已选择第{0}路": "Lane {0} chosen",
    "冒险模式：第{0}关": "Adventure Lv.{0}", "场上敌人数量：{0}": "Enemies: {0}",
    "剩余阳光：{0}": "Sun Left: {0}", "剩余金币：{0}": "Coins Left: {0}",
    "产生阳光：{0}": "Sun Made: {0}", "消耗阳光：{0}": "Sun Used: {0}",
    "消耗金币：{0}": "Coins Used: {0}", "获得金币：{0}": "Coins Won: {0}",
    "需要{0}点阳光": "Needs {0} Sun", "最多{0}株植物": "Max {0} Plants",
    "种植植物：{0}": "Planted: {0}", "死亡植物：{0}": "Plants Lost:{0}",
    "铲除植物：{0}": "Removed: {0}", "升级需要{0}金币": "Need {0} Coins",
    "出售植物：": "Sold Plant:", "购买植物：": "Bought:", "\n获得植物：": "\nGot Plant:",
    "获得新植物：": "New Plant:", "开局阳光归零": "Zero Start Sun",
    "游戏失败": "Game Over", "上传失败": "Upload Fail", "关卡不存在": "No Level",
    "关卡信息错误": "Bad Level Info", "关卡数据为空！": "Empty Level!",
    "花园植物": "Garden", "融合植物": "Fusion", "彩卡植物": "Rainbow", "普通植物": "Common",
    "关闭僵尸显血": "Hide Zombie HP", "关闭植物显血": "Hide Plant HP",
    "禁用转场动画": "No Cutscenes", "音游开始！": "Music Start!",
    "主菜单": "Main Menu", "查看草坪": "View Lawn", "切换手套": "Toggle Glove",
    "使用手套": "Use Glove", "确定": "OK", "取消": "Cancel", "返回": "Back",
    "开始": "Start", "暂停": "Pause", "继续": "Resume", "关闭": "Close", "确认": "Confirm",
}


def LJ(p):
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def build_dict():
    d = {}
    ts = LJ(f"{EN}/Strings/translation_strings.json") or {}
    for k, v in ts.items():
        if isinstance(v, str) and not k.strip().startswith("---") and not v.strip().endswith("-------") and CJK.search(k):
            d.setdefault(k, v)
    # plant / zombie names
    lc, le = LJ(f"{MOD}/Dumps/LawnStrings.json"), LJ(f"{EN}/Almanac/LawnStringsTranslate.json")
    if lc and le:
        eb = {p["seedType"]: p for p in le["plants"]}
        for p in lc["plants"]:
            e = eb.get(p["seedType"])
            if e and "name" in e and CJK.search(p.get("name", "")):
                d.setdefault(p["name"], e["name"])
    zc, ze = LJ(f"{MOD}/Dumps/ZombieStrings.json"), LJ(f"{EN}/Almanac/ZombieStringsTranslate.json")
    if zc and ze:
        eb = {z["theZombieType"]: z for z in ze["zombies"]}
        for z in zc["zombies"]:
            e = eb.get(z["theZombieType"])
            if e and "name" in e and CJK.search(z.get("name", "")):
                d.setdefault(z["name"], e["name"])
    d.update(HUD)  # curated overrides win
    return d


def main(inp, outp):
    orig = open(inp, "rb").read()
    buf = bytearray(orig)
    sanity, version = struct.unpack_from("<Ii", orig, 0)
    assert sanity == 0xFAB11BAF, "not il2cpp metadata"
    slOff, slCnt, sldOff, sldCnt = struct.unpack_from("<IIII", orig, 8)

    tr = build_dict()
    tr_b = {k.encode(): v.encode() for k, v in tr.items()}

    done = skip_len = 0
    seen_di = {}
    n = slCnt // 8
    for i in range(n):
        length, di = struct.unpack_from("<II", orig, slOff + i * 8)
        if length == 0 or length > 4096:
            continue
        cn_b = bytes(orig[sldOff + di: sldOff + di + length])
        en_b = tr_b.get(cn_b)
        if en_b is None:
            continue
        if len(en_b) > length:
            skip_len += 1
            continue
        # overwrite bytes in-place (read decisions from orig; safe for dedup)
        buf[sldOff + di: sldOff + di + len(en_b)] = en_b
        # update per-literal length field (first uint32 of the entry)
        struct.pack_into("<I", buf, slOff + i * 8, len(en_b))
        done += 1

    with open(outp, "wb") as f:
        f.write(buf)
    print(f"metadata literals translated in-place: {done}  (skipped too-long: {skip_len})")
    print(f"size unchanged: {len(buf)==len(orig)}  wrote {outp}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
