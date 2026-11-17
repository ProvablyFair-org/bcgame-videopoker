#!/usr/bin/env python3
"""Independent check of the exact hold values behind every return here: every draw counted one by one.

For 200 hands (the 62 live hands and 138 pseudo-random hands, fixed seed), the expected return of each of the 32 holds
is computed by brute force in Python: the discards are replaced from the 47 cards not dealt, every combination counted
once, scored with src/bcvp.py's classifier and the 98% paytable. checks/exact_holds.c (the exact calculator of
src/vpsim.c, which picks the best hold in every simulation) must give the same 6,400 values within 1e-9, and the same
best value per hand. Negative check: with three of a kind paying one more on the Python side only, the values must
disagree. Slow: about 8 CPU seconds a hand, half an hour in all. Run by `make oracle`.
usage: python3 checks/check_holds_oracle.py [procs]
"""
import csv
import itertools
import multiprocessing as mp
import os
import random
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import check, finish, path
import bcvp

PAY = [0, 1, 2, 3, 4, 6, 8, 22, 80, 800]   # by bcvp.CLASS_NAMES: nothing ... royal flush


def evs(args):
    dealt, pay = args
    rest = [c for c in bcvp.SUIT_ORDER if c not in dealt]
    out = []
    for mask in range(32):
        held = [dealt[i] for i in range(5) if mask & (1 << i)]
        tot = n = 0
        for draw in itertools.combinations(rest, 5 - len(held)):
            tot += pay[bcvp.classify(held + list(draw))]
            n += 1
        out.append(tot / n)
    return out


if __name__ == "__main__":
    procs = int(sys.argv[1]) if len(sys.argv) > 1 else (os.cpu_count() or 2)
    live = [[int(x) for x in r["dealt_codes"].split()] for r in csv.DictReader(open(path("results", "live-sessions", "video-poker-hands.csv")))]
    rng = random.Random(20261116)
    hands = live + [rng.sample(bcvp.SUIT_ORDER, 5) for _ in range(200 - len(live))]
    env = dict(os.environ, PAYTABLE=",".join(map(str, PAY[1:])))
    out = subprocess.run([path("build", "exact_holds")], input="".join(" ".join(map(str, h)) + "\n" for h in hands),
                         capture_output=True, text=True, check=True, env=env).stdout.split("\n")
    c_rows = [[float(x) for x in ln.split()] for ln in out[1:] if ln.strip()]
    with mp.Pool(procs) as pool:
        py = pool.map(evs, [(h, PAY) for h in hands])
        bad_pay = list(PAY)
        bad_pay[3] += 1
        py_bad = pool.map(evs, [(h, bad_pay) for h in hands[:12]])
    worst = max(abs(p[m] - c[m]) for p, c in zip(py, c_rows) for m in range(32))
    worst_best = max(abs(max(p) - c[32]) for p, c in zip(py, c_rows))
    check("brute force = exact calculator, every hold value", len(c_rows) == len(hands) == 200 and worst < 1e-9,
          "%d hands (%d live, %d pseudo-random), %d hold values, largest difference %.1g" % (len(hands), len(live), len(hands) - len(live), 32 * len(hands), worst))
    check("brute force = exact calculator, best value per hand", worst_best < 1e-6, "largest difference %.1g" % worst_best)
    neg = sum(1 for p, c in zip(py_bad, c_rows) if any(abs(p[m] - c[m]) > 1e-9 for m in range(32)))
    check("negative check: three of a kind paying one more (Python side only) is caught", neg > 0, "%d of 12 hands disagree" % neg)
    finish()
