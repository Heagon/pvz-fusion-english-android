"""Self-check for the display-pass helpers in patch_bundle_v2. Run: python test_patch_helpers.py"""
import re
import struct
from patch_bundle_v2 import regex_tr, display_pass, translate_values


def framed(s):
    b = s.encode()
    return struct.pack("<i", len(b)) + b + b"\x00" * ((4 - len(b) % 4) % 4)


rx = [(re.compile(r"^(\d+)轮"), "{0} Rounds"),
      (re.compile(r"^查看([^\s：]+)"), "View {0}"),
      (re.compile(r"^确定退出吗？\s+"), "Are you sure?")]
d = {"图鉴": "Almanac"}
assert regex_tr("3轮", rx, d) == "3 Rounds"
assert regex_tr("查看图鉴", rx, d) == "View Almanac"           # group translated via dict
assert regex_tr("查看草坪", rx, d) is None                      # group stays Chinese -> refuse
assert regex_tr("确定退出吗？\n进度不会保存", rx, d) == "Are you sure?"  # ^prefix\s+ pattern
assert regex_tr("3轮之后", rx, d) is None                       # partial match refused
# a template written for a longer multi-line tooltip must not hijack a one-line label
assert regex_tr("伤害+200%", [(re.compile(r"(.+)\+(\d+)%"), "Not found yet!\n{0} + {1}%")], d) is None

# display_pass: splices only complete, zero-padded framed strings; keeps 4-byte alignment
blob = struct.pack("<i", 7) + framed("返回") + framed("abc") + framed("图鉴")
out, n = display_pass(blob, {"返回": "Back", "图鉴": "Almanac"}.get)
assert n == 2
assert out == struct.pack("<i", 7) + framed("Back") + framed("abc") + framed("Almanac")
assert len(out) % 4 == 0
out, n = display_pass(blob, lambda s: None)
assert (out, n) == (blob, 0)

# logic keys are never translated
st = [0]
j = translate_values({"id": "Other:幸运:0", "title": "幸运", "arguments": ["幸运"]}, {"幸运": "Luck"}, st)
assert j == {"id": "Other:幸运:0", "title": "Luck", "arguments": ["幸运"]} and st[0] == 1
print("ok")
