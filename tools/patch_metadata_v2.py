"""Rebuild-based patch of IL2CPP global-metadata.dat string literals.

Unlike the in-place patcher, this rebuilds the stringLiteralData section so
English replacements of ANY length are allowed. It then shifts every metadata
section that comes after stringLiteralData and updates the header offsets.

Header layout (v31): int32 sanity, int32 version, then N (offset,size) pairs.
stringLiteral table = pair#0 (Il2CppStringLiteral{uint32 length; uint32 dataIndex}).
stringLiteralData  = pair#1 (raw utf8 blob, dataIndex is relative to its start).

Sources: translation_strings + plant/zombie names + travel_buffs (all 5 kinds,
name+desc reconstructed) + tips + curated HUD overrides.

Usage: python patch_metadata_v2.py <in> <out>
"""
import struct
import re
import json
import sys

MOD = r"./PvZ_Fusion_Translator"
EN = MOD + r"/Localization/English"
TRANS = r"./translations"
CJK = re.compile(r'[一-鿿㐀-䶿]')
BUFF_SIZE = 12  # shrink long modifier/buff descriptions to match almanac descriptions

HUD = {
    "难度：{0}": "Diff: {0}", "章节难度：{0}": "Ch.Diff: {0}", "难度阶数：{0}": "Diff Tier: {0}",
    "章节难度：{0}+2": "Ch.Diff: {0}+2", "，推荐难度：": ", Rec. Diff: ",
    "第{0}关": "Lvl {0}", "第{0}波": "Wave {0}", "第{0}轮": "Round {0}", "第{0}行": "Row {0}",
    "第{0}路": "Lane {0}", "第{0}页": "Page {0}", " 第{0}轮": " Round {0}", "{0}轮": "{0} Rounds",
    "波次：{0}/{1}": "Wave: {0}/{1}", "已选择第{0}路": "Lane {0} chosen",
    "冒险模式：第{0}关": "Adventure Lv.{0}", "场上敌人数量：{0}": "Enemies: {0}",
    "剩余阳光：{0}": "Sun Left: {0}", "剩余金币：{0}": "Coins Left: {0}",
    "产生阳光：{0}": "Sun Made: {0}", "消耗阳光：{0}": "Sun Used: {0}",
    "消耗金币：{0}": "Coins Used: {0}", "获得金币：{0}": "Coins Won: {0}",
    "需要{0}点阳光": "Needs {0} Sun", "最多{0}株植物": "Max {0} Plants",
    "种植植物：{0}": "Planted: {0}", "死亡植物：{0}": "Plants Lost: {0}",
    "铲除植物：{0}": "Removed: {0}", "升级需要{0}金币": "Need {0} Coins",
    "出售植物：": "Sold Plant: ", "购买植物：": "Bought: ", "\n获得植物：": "\nGot Plant: ",
    "获得新植物：": "New Plant: ", "开局阳光归零": "Zero Start Sun",
    "游戏失败": "Game Over", "上传失败": "Upload Failed", "关卡不存在": "Level not found",
    "关卡信息错误": "Bad Level Info", "关卡数据为空！": "Empty Level!",
    "花园植物": "Garden", "融合植物": "Fusion", "彩卡植物": "Rainbow", "普通植物": "Common",
    "关闭僵尸显血": "Hide Zombie HP", "关闭植物显血": "Hide Plant HP",
    "禁用转场动画": "Disable Cutscene", "音游开始！": "Music Start!",
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

    def add(cn, en):
        if isinstance(cn, str) and isinstance(en, str) and en and cn != en and CJK.search(cn):
            d.setdefault(cn, en)

    ts = LJ(f"{EN}/Strings/translation_strings.json") or {}
    for k, v in ts.items():
        if isinstance(v, str) and not k.strip().startswith("---") and not v.strip().endswith("-------"):
            add(k, v)
    # plant / zombie names
    lc, le = LJ(f"{MOD}/Dumps/LawnStrings.json"), LJ(f"{EN}/Almanac/LawnStringsTranslate.json")
    if lc and le:
        eb = {p["seedType"]: p for p in le["plants"]}
        for p in lc["plants"]:
            e = eb.get(p["seedType"])
            if e and "name" in e:
                add(p.get("name", ""), e["name"])
    zc, ze = LJ(f"{MOD}/Dumps/ZombieStrings.json"), LJ(f"{EN}/Almanac/ZombieStringsTranslate.json")
    if zc and ze:
        eb = {z["theZombieType"]: z for z in ze["zombies"]}
        for z in zc["zombies"]:
            e = eb.get(z["theZombieType"])
            if e and "name" in e:
                add(z.get("name", ""), e["name"])
    # travel buffs / modifiers (all categories) -- reconstruct name: desc
    cnb, enb = LJ(f"{MOD}/Dumps/travel_buffs.json") or {}, LJ(f"{EN}/Strings/travel_buffs.json") or {}
    for cat in cnb:
        if not isinstance(cnb[cat], dict):
            continue
        for bid, cbuff in cnb[cat].items():
            ebuff = enb.get(cat, {}).get(bid)
            if not isinstance(cbuff, dict) or not isinstance(ebuff, dict):
                continue
            if cbuff.get("name"):
                add(cbuff["name"], ebuff.get("name") or cbuff["name"])
            if cbuff.get("desc"):
                en_full = ((ebuff.get("name") + ": ") if ebuff.get("name") else "") + (ebuff.get("desc") or "")
                add(cbuff["desc"], f"<size={BUFF_SIZE}>{en_full}</size>")
    # tips
    for f in ("tips_fs", "tips_iz"):
        cnt, ent = LJ(f"{MOD}/Dumps/{f}.json") or {}, LJ(f"{EN}/Strings/{f}.json") or {}
        for k, v in cnt.items():
            if k in ent and isinstance(v, str):
                add(v, ent[k])
    # supplement (my own translations) + detail titles/types + 9-plant names
    for k, v in (LJ(f"{TRANS}/supplement.json") or {}).items():
        add(k, v)
    dt = LJ(f"{TRANS}/detail_titles_en.json") or {}
    for k, v in dt.get("titles", {}).items():
        add(k, v)
    for k, v in dt.get("types", {}).items():
        add(k, v)
    d.update(HUD)
    return d


def main(inp, outp):
    gm = bytearray(open(inp, "rb").read())
    sanity, version = struct.unpack_from("<Ii", gm, 0)
    assert sanity == 0xFAB11BAF
    slOff = struct.unpack_from("<I", gm, 8)[0]
    npairs = (slOff - 8) // 8
    pairs = [list(struct.unpack_from("<II", gm, 8 + i * 8)) for i in range(npairs)]
    sldOff, sldSize = pairs[1]

    tr = build_dict()
    tr_b = {k.encode(): v.encode() for k, v in tr.items()}

    # rebuild stringLiteralData
    nlit = pairs[0][1] // 8
    new_blob = bytearray()
    remap = {}          # (orig_dataIndex, length) -> (new_dataIndex, new_length)
    done = 0
    for i in range(nlit):
        length, di = struct.unpack_from("<II", gm, slOff + i * 8)
        key = (di, length)
        if key in remap:
            ndi, nlen = remap[key]
        else:
            cn_b = bytes(gm[sldOff + di: sldOff + di + length])
            en_b = tr_b.get(cn_b)
            out_b = en_b if en_b is not None else cn_b
            ndi = len(new_blob)
            nlen = len(out_b)
            new_blob += out_b
            remap[key] = (ndi, nlen)
            if en_b is not None:
                done += 1
        struct.pack_into("<II", gm, slOff + i * 8, nlen, ndi)

    # pad to 4-byte alignment
    while len(new_blob) % 4:
        new_blob.append(0)
    new_size = len(new_blob)
    delta = new_size - sldSize

    # update header: pair#1 size; shift offsets of every section after sldOff
    pairs[1][1] = new_size
    for p in pairs:
        if p[0] > sldOff:
            p[0] += delta
    for i, p in enumerate(pairs):
        struct.pack_into("<II", gm, 8 + i * 8, p[0], p[1])

    # reassemble: [0 .. end of stringLiteral table = sldOff] + new_blob + [old data after sldData]
    head = bytes(gm[:sldOff])           # header (updated) + stringLiteral table (updated entries)
    tail = bytes(gm[sldOff + sldSize:]) # everything from string(names) section onward, unchanged
    out = head + bytes(new_blob) + tail

    with open(outp, "wb") as f:
        f.write(out)
    print(f"translated {done} literals; sldData {sldSize} -> {new_size} (delta {delta:+}); "
          f"filesize {len(gm)} -> {len(out)}; wrote {outp}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
