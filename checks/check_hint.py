#!/usr/bin/env python3
"""BC's AI-Hint on the 62 live hands: is the hold it suggests a best hold for the paytable on a fairly shuffled deck?

For each hand the expected return of all 32 holds is computed exactly (replacements drawn from the 47 cards not
dealt, the server paytable) by checks/exact_holds.c, which reuses the exact calculator of src/vpsim.c. A hint matches
when its hold has the highest expected return (a tie counts). BC sent the hint flags with every bet answer, so the
check covers the 30 hands played with the hint switched on and the 32 with it off.
Needs build/exact_holds (make build). Reads results/live-sessions/video-poker-hands.csv.
"""
import csv
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import check, finish, path

rows = list(csv.DictReader(open(path("results", "live-sessions", "video-poker-hands.csv"))))
inp = "".join(r["dealt_codes"] + "\n" for r in rows)
env = dict(os.environ, PAYTABLE="1,2,3,4,6,8,22,80,800")
out = subprocess.run([path("build", "exact_holds")], input=inp, capture_output=True, text=True, check=True, env=env).stdout.split("\n")
exact = float(out[0].split()[1])
check("exact calculator: return of the 98% paytable with best play on a fair deck = 98.0194%", abs(exact - 0.9801941005) < 1e-9, "%.10f" % exact)
ok = {"on": [0, 0], "off": [0, 0]}
for r, line in zip(rows, out[1:]):
    vals = [float(x) for x in line.split()[:32]]
    mask = sum(1 << i for i, ch in enumerate(r["ai_hint_hold"]) if ch == "H")
    best = max(vals)
    ok[r["ai_hint_switch"]][0] += vals[mask] >= best - 1e-12
    ok[r["ai_hint_switch"]][1] += 1
check("AI-Hint switched on: the hint is a best hold", ok["on"][0] == ok["on"][1], "%d / %d hands" % tuple(ok["on"]))
check("AI-Hint switched off (BC still sent it): the hint is a best hold", ok["off"][0] == ok["off"][1], "%d / %d hands" % tuple(ok["off"]))
desc = " ".join(open(path("evidence", "claims", "2026-11-16_game-page_description.txt"), encoding="utf8").read().split())
check("BC's game page says the AI Hint shows the mathematically optimal hold",
      "highlights the mathematically optimal cards to keep based on perfect video poker strategy" in desc,
      "evidence/claims/2026-11-16_game-page_description.txt")
finish()
