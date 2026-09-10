"""Run with KiCad's Python: verify_pcb.py path/to/Circa40.kicad_pcb."""
import pathlib
import re
import sys

import pcbnew

board = pcbnew.LoadBoard(sys.argv[1])
footprints = {f.GetReference(): f for f in board.GetFootprints()}


def pads(ref):
    return {p.GetNumber(): p.GetNetname() for p in footprints[ref].Pads() if p.GetNumber()}


diodes = {pads(ref)["2"]: pads(ref)["1"] for ref in footprints if re.fullmatch(r"D\d+", ref)}
order = (list(range(1, 7)) + list(range(22, 28)) + list(range(7, 13))
         + list(range(28, 33)) + list(range(13, 18)) + list(range(33, 39))
         + list(range(18, 22)) + [39, 40, 45, 41, 42])
actual = []
for number in order:
    switch = pads(f"SW{number}")
    row = int(re.fullmatch(r"Row(\d)_[LR]", diodes[switch["2"]])[1])
    col, side = re.fullmatch(r"Col(\d)_([LR])", switch["1"]).groups()
    actual.append((row, int(col) + (6 if side == "R" else 0)))

root = pathlib.Path(__file__).resolve().parents[1]
shield = root / "config/boards/shields/circa40"
configured = [tuple(map(int, pair)) for pair in re.findall(r"RC\((\d+),(\d+)\)", (shield / "circa40.dtsi").read_text())]
assert actual == configured, (actual, configured)
assert len(set(configured)) == 43
for bindings in re.findall(r"bindings\s*=\s*<([^>]+)>", (root / "config/circa40.keymap").read_text()):
    assert bindings.count("&") == 43
expected_pads = {
    "Left-XiaoPlus1": {"1": "Col0_L", "2": "Col1_L", "3": "Col2_L", "4": "Col3_L", "15": "Col4_L", "16": "Col5_L", "17": "Row0_L", "23": "Row1_L", "22": "Row2_L", "21": "Row3_L"},
    "U1": {"1": "Col0_R", "2": "Col1_R", "3": "Col2_R", "4": "Col3_R", "5": "Col4_R", "6": "Col5_R", "7": "Row0_R", "8": "Row1_R", "9": "Row2_R", "10": "Row3_R", "11": "MOTION_R", "21": "SCLK_R", "22": "CS_R", "23": "SDIO_R"},
}
for ref, expected in expected_pads.items():
    found = pads(ref)
    assert all(found[pin] == net for pin, net in expected.items()), ref
print("PASS: 43 matrix positions, diode direction, MCU pad nets, and all keymap layer sizes")
