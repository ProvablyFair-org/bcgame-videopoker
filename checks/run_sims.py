#!/usr/bin/env python3
"""Reruns every simulation behind results/ and compares the new output with the stored one.

Video poker: each results/video-poker/*/run-*/command.txt is run again with build/vpsim (100,000,000 deals). The
exact enumeration and the BC-deal arm are seeded by the deal number, so they must come out the same, line for line, on
any machine and any thread count. One run (98-table_current-verifier/run-1) also has a fair-shuffle control arm, whose
random stream is seeded per thread: with a different thread count it is a different fair sample, so it is checked
against the exact return within its error instead of line for line.
Baccarat: src/baccarat_sim.py is run again and its counts compared with results/baccarat/returns.json (both of its arms
are seeded per batch, so the counts do not depend on the number of processes). Expect several CPU hours.
usage: python3 checks/run_sims.py [--threads N] [--only video-poker|baccarat]
"""
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import check, finish, path

args = sys.argv[1:]
threads = args[args.index("--threads") + 1] if "--threads" in args else str(os.cpu_count() or 4)
only = args[args.index("--only") + 1] if "--only" in args else None

CONTROL = "== Simulation arm: UNIFORM_CONTROL"


def compare_vp(name, new, stored):
    """Everything up to the control arm line for line; the control arm (if any) against the exact return."""
    fixed_new, ctl_new = (new.split(CONTROL, 1) + [""])[:2]
    fixed_old, ctl_old = (stored.split(CONTROL, 1) + [""])[:2]
    check("%s: exact return and BC-deal arm identical to the stored output" % name, fixed_new == fixed_old)
    if ctl_old or ctl_new:
        exact = float(re.search(r"^EXACT_OPTIMAL_RTP ([0-9.]+)", new, re.M).group(1))
        rtp, se = (float(x) for x in re.search(r"^FULL_PLAY_RTP[^:]*: ([0-9.]+) SE ([0-9.]+)", ctl_new, re.M).groups())
        check("%s: fair-shuffle control within 4 SE of the exact return" % name, bool(ctl_old) and abs(rtp - exact) < 4 * se,
              "%.4f%% vs exact %.4f%%, SE %.4f" % (100 * rtp, 100 * exact, 100 * se))


if only in (None, "video-poker"):
    base = path("results", "video-poker")
    for cfg in sorted(os.listdir(base)):
        d = os.path.join(base, cfg)
        if not os.path.isdir(d):
            continue
        for run in sorted(os.listdir(d)):
            cmd = open(os.path.join(d, run, "command.txt")).read().split("./build/vpsim")[0]
            env = dict(os.environ, **dict(tok.split("=", 1) for tok in shlex.split(cmd)))
            with tempfile.TemporaryDirectory() as tmp:
                out = subprocess.run([path("build", "vpsim"), "100000000", threads, tmp], env=env, capture_output=True, text=True, check=True).stdout
            compare_vp("%s/%s" % (cfg, run), out, open(os.path.join(d, run, "run.txt")).read())

if only in (None, "baccarat"):
    stored = json.load(open(path("results", "baccarat", "returns.json")))
    with tempfile.TemporaryDirectory() as tmp:
        backup = {f: open(path("results", "baccarat", f)).read() for f in ("returns.json", "returns.txt")}
        try:
            subprocess.run([sys.executable, path("src", "baccarat_sim.py"), "40000000", "40000000", threads], check=True, capture_output=True)
            new = json.load(open(path("results", "baccarat", "returns.json")))
        finally:
            for f, text in backup.items():
                open(path("results", "baccarat", f), "w").write(text)
    for part in ("bc_deal_simulated", "control_uniform_2_decks"):
        same = new[part]["rounds"] == stored[part]["rounds"] and all(
            new[part][k]["count"] == stored[part][k]["count"] for k in ("player", "banker", "tie", "player_pair", "banker_pair", "player_third", "banker_third"))
        check("baccarat %s: same counts as stored" % part, same)
    check("baccarat exact fair shoe: same fractions as stored", new["exact_fair_shoe"] == stored["exact_fair_shoe"])
finish()
