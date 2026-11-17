#!/usr/bin/env python3
"""Exact return of each paytable with the optimal fair-deck strategy on a fairly shuffled 52-card deck (full enumeration of all
2,598,960 deals x 32 holds by src/vpsim.c). The 9/6 Jacks or Better table is the textbook check: 99.5439%.
Writes results/video-poker/exact-returns.txt. Needs build/vpsim (make build).
"""
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import check, finish, path

TABLES = [("98% game (VideoPoker98, live now)", "1,2,3,4,6,8,22,80,800", 0.9801941005),
          ("99% game (VideoPoker)", "1,2,3,4,6,9,22,60,800", 0.9894447794),
          ("96% game (VideoPoker96, Nov 2026 table)", "1,2,3,4,5,8,18,80,800", 0.9597575196),
          ("9/6 Jacks or Better, textbook check", "1,2,3,4,6,9,25,50,800", 0.9954390437)]
lines = ["Exact return with the optimal fair-deck strategy on a fairly shuffled deck (src/vpsim.c, full enumeration)", ""]
for label, pay, want in TABLES:
    with tempfile.TemporaryDirectory() as tmp:
        out = subprocess.run([path("build", "vpsim"), "1000", "1", tmp], env=dict(os.environ, PAYTABLE=pay, VP_ARMS="1"),
                             capture_output=True, text=True, check=True).stdout
    got = float(re.search(r"EXACT_OPTIMAL_RTP ([0-9.]+)", out).group(1))
    table = "/".join(reversed(pay.split(",")))
    check("%-44s %s  %.6f%%" % (label, table, 100 * got), abs(got - want) < 1e-9)
    lines.append("%-44s paytable %-22s %.8f%%" % (label, table, 100 * got))
os.makedirs(path("results", "video-poker"), exist_ok=True)
open(path("results", "video-poker", "exact-returns.txt"), "w").write("\n".join(lines) + "\n")
finish()
