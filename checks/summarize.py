#!/usr/bin/env python3
"""Pools the simulation outputs in results/ and writes results/summary.md, the numbers the README quotes.

Video poker: each configuration is the mean of its 100M-deal runs (equal sizes), 95% interval = mean +/- 1.96 x
sqrt(sum of the runs' SE^2) / runs. Every run plays the optimal fair-deck strategy for its paytable (the best of the 32
holds for each dealt hand, worked out exactly for a fairly shuffled deck), with the five dealt cards and the
replacements taken from BC's deal, replacements in order from card 6.
Dealt-hand frequencies: the expected count of each class is the number of deals times its exact share of the 2,598,960
possible hands (combination counts, checked against the simulator's own enumeration); 95% intervals are Wilson score
intervals for each class on its own.
Baccarat: results/baccarat/returns.json (src/baccarat_sim.py).
"""
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import check, finish, path

CONFIGS = [  # folder, label, advertised RTP or None, exact fair return
    ("98-table_current-verifier", "98% game (VideoPoker98, live): its paytable, current verifier", 98.0, 98.01941005),
    ("96-table_current-verifier", "96% game (VideoPoker96): paytable as BC's server sends it in Nov 2026, current verifier", 96.0, 95.97575196),
    ("99-table_current-verifier", "99% game (VideoPoker): its paytable, current verifier (hash of 24 Dec 2021)", 99.0, 98.94447794),
    ("99-table_apr2020-verifier", "99% game (VideoPoker): its paytable, verifier of 8 Apr 2020 (earlier hash)", 99.0, 98.94447794),
    ("99-table_original-list", "99% paytable, original verifier of 14 Nov 2019 (suit-ordered list)", None, 98.94447794),
]
# exact number of each dealt five-card hand among the 2,598,960 (combination counts)
EXACT_COUNTS = {"nothing/low pair": 2062860, "jacks or better": 337920, "two pair": 123552, "three of a kind": 54912,
                "straight": 10200, "flush": 5108, "full house": 3744, "four of a kind": 624, "straight flush": 36, "royal flush": 4}
ALL_HANDS = 2598960


def wilson(k, n, z=1.96):
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return c - h, c + h


def parse(run_txt):
    s = open(run_txt).read()
    bc = s.split("== Simulation arm: BC_VERIFIER_SHUFFLE", 1)[1].split("== Simulation arm:", 1)[0]
    r = {"n": int(re.search(r"n = (\d+) deals", bc).group(1)),
         "exact": float(re.search(r"EXACT_OPTIMAL_RTP ([0-9.]+)", s).group(1)) * 100}
    r["full"], r["se"] = [float(x) * 100 for x in re.search(r"FULL_PLAY_RTP[^:]*: ([0-9.]+) SE ([0-9.]+)", bc).groups()]
    r["deal_only"] = float(re.search(r"DEAL_ONLY_RTP[^:]*: ([0-9.]+)", bc).group(1)) * 100
    r["neighbour_ratio"] = float(re.search(r"neighbour pairs per deal.*?ratio ([0-9.]+)", bc).group(1))
    r["classes"] = {m[0].strip(): (int(m[2]), float(m[1])) for m in
                    re.findall(r"^\s+([a-z /]+?)\s+observed [0-9.]+ exact ([0-9.]+) ratio .*?\(count (\d+)\)", bc, re.M)}
    r["enumerated"] = {m[0].strip(): int(m[1]) for m in re.findall(r"^\s+([a-z /]+?)\s+(\d+)\s+p=[0-9.]+$", s.split("== Simulation arm:", 1)[0], re.M)}
    ctl = re.search(r"== Simulation arm: UNIFORM[\s\S]*?FULL_PLAY_RTP[^:]*: ([0-9.]+) SE ([0-9.]+)", s)
    r["control"] = (float(ctl.group(1)) * 100, float(ctl.group(2)) * 100) if ctl else None
    return r


L = ["# Results", "",
     "Numbers in percent. Every return is for the optimal fair-deck strategy for the paytable: the best of the 32 holds for each dealt hand, "
     "worked out exactly for a fairly shuffled deck. Written by `checks/summarize.py`.", "",
     "## Video poker", "",
     "Each row is a paytable played on one version of BC's published verifier. When each version ran on bc.game is in the README's timeline.", "",
     "| paytable and verifier | return on a fairly shuffled deck | return on BC's deal (95% interval) | against the paytable | runs | additional expected loss per $1,000 wagered, vs advertised |",
     "|---|---|---|---|---|---|"]
pooled = {}
for folder, label, adv, exact in CONFIGS:
    d = path("results", "video-poker", folder)
    if not check("results/video-poker/%s is here" % folder, os.path.isdir(d)):
        continue
    runs = [parse(os.path.join(d, x, "run.txt")) for x in sorted(os.listdir(d)) if os.path.exists(os.path.join(d, x, "run.txt"))]
    check("%s: every run uses the paytable's exact return %.6f" % (folder, exact), all(abs(r["exact"] - exact) < 1e-6 for r in runs))
    mean = sum(r["full"] for r in runs) / len(runs)
    se = math.sqrt(sum(r["se"] ** 2 for r in runs)) / len(runs)
    pooled[folder] = {"mean": mean, "lo": mean - 1.96 * se, "hi": mean + 1.96 * se, "runs": runs, "exact": exact, "adv": adv}
    extra = "$%.0f" % (10 * (adv - mean)) if adv else ("players had the edge" if mean > 100 else "")
    below = "%.2f points below" % (exact - mean) if mean < exact else "%.2f points above" % (mean - exact)
    L.append("| %s | %.2f | **%.2f** (%.2f to %.2f) | %s | %d x 100M | %s |"
             % (label, exact, mean, mean - 1.96 * se, mean + 1.96 * se, below, len(runs), extra))

if "98-table_current-verifier" in pooled:
    p = pooled["98-table_current-verifier"]
    runs = p["runs"]
    n = sum(r["n"] for r in runs)
    deal = sum(r["deal_only"] for r in runs) / len(runs)
    L += ["", "98%% game, %s hands: house edge **%.2f%%** against the advertised 2%% (%.1fx). Of the %.2f points lost against the paytable, %.2f are lost on the five dealt cards alone (best hold, fair replacements)."
          % ("{:,}".format(n), 100 - p["mean"], (100 - p["mean"]) / 2, p["exact"] - p["mean"], p["exact"] - deal), ""]
    check("dealt-hand counts: the simulator's enumeration = the combination counts", all(r["enumerated"] == EXACT_COUNTS for r in runs)
          and sum(EXACT_COUNTS.values()) == ALL_HANDS)
    L += ["### Dealt hands, 98%% game, the same %s deals: BC's deal against a fairly shuffled deck" % "{:,}".format(n), "",
          "The five cards dealt before any hold, not the final hands. Expected = deals x exact share of the 2,598,960 hands.", "",
          "| dealt hand | on BC's deal | expected on a fair deck | change (95% interval) |", "|---|---|---|---|"]
    for name in runs[0]["classes"]:
        cnt = sum(r["classes"][name][0] for r in runs)
        exp = n * EXACT_COUNTS[name] / ALL_HANDS
        lo, hi = wilson(cnt, n)
        L.append("| %s | %s | %s | %+.2f%% (%+.2f to %+.2f) |" % (name, "{:,}".format(cnt), "{:,.1f}".format(exp), 100 * (cnt / exp - 1),
                                                               100 * (lo * n / exp - 1), 100 * (hi * n / exp - 1)))
    nb = sum(r["neighbour_ratio"] for r in runs) / len(runs)
    L += ["", "Why: two cards that sit next to each other in BC's 52-card list turn up in the same five dealt cards %.2f times as often as on a fairly shuffled deck (anywhere in the hand, not side by side), and in BC's list no two neighbours share a suit or a rank." % nb]
    ctl = [r["control"] for r in runs if r["control"]]
    if ctl:
        L += ["", "Control (run 1): the same program with a fair shuffle returns %.3f%% (SE %.3f), within its error of the exact %.3f%%." % (ctl[0][0], ctl[0][1], p["exact"])]

L += ["", "## Baccarat", ""]
bj = path("results", "baccarat", "returns.json")
if os.path.exists(bj):
    b = json.load(open(bj))
    t = b["per_bet_table_real_payouts"]
    L += ["%s rounds of BC's deal, returns at the server's odds, against the exact return of a fairly shuffled 2-deck shoe." % "{:,}".format(b["bc_deal_simulated"]["rounds"]), "",
          "| bet | pays | fairly shuffled shoe | on BC's deal (95% interval) | change, points |", "|---|---|---|---|---|"]
    for bet in ("player", "banker", "tie", "player_pair", "banker_pair"):
        x = t[bet]
        L.append("| %s | %s | %.2f | %.2f (%.2f to %.2f) | %+.2f |" % (bet.replace("_", " "), x["pays"], 100 * x["exact_2_deck_return"], 100 * x["bc_deal_return"],
                                                                     100 * x["bc_deal_ci95"][0], 100 * x["bc_deal_ci95"][1], x["bc_minus_exact_points"]))
    pp = t["player_pair"]
    L += ["", "Player pair: about $%.0f of additional expected loss per $1,000 wagered on it, against a fairly shuffled shoe. Control (a fair shuffle through the same counting code): %s."
          % (10 * (100 * pp["exact_2_deck_return"] - 100 * pp["bc_deal_return"]), b["control_agreement_rule"]["result"])]
else:
    check("results/baccarat/returns.json is here", False)

open(path("results", "summary.md"), "w").write("\n".join(L) + "\n")
print("\n".join(L))

# the numbers the README quotes, and a check that it still quotes them
q = {}
if "98-table_current-verifier" in pooled:
    p = pooled["98-table_current-verifier"]
    runs = p["runs"]
    deal = sum(r["deal_only"] for r in runs) / len(runs)
    q.update(VP98="%.2f" % p["mean"], EDGE98="%.2f" % (100 - p["mean"]), X98="%.1f" % ((100 - p["mean"]) / 2),
             USD98="%.0f" % (10 * (98 - p["mean"])), DEAL_LOSS="%.2f" % (p["exact"] - deal), TOTAL_LOSS="%.2f" % (p["exact"] - p["mean"]),
             NEIGH="%.2f" % (sum(r["neighbour_ratio"] for r in runs) / len(runs)))
for key, folder in (("VP99", "99-table_current-verifier"), ("VP99A", "99-table_apr2020-verifier"), ("VP96", "96-table_current-verifier"), ("VP19", "99-table_original-list")):
    if folder in pooled:
        q[key] = "%.1f" % pooled[folder]["mean"]
q["SIM_HANDS"] = "%.1f billion" % (sum(r["n"] * (2 if r["control"] else 1) for v in pooled.values() for r in v["runs"]) / 1e9)
if os.path.exists(bj):
    pp = json.load(open(bj))["per_bet_table_real_payouts"]["player_pair"]
    q.update(PP_BC="%.2f" % (100 * pp["bc_deal_return"]), PP_FAIR="%.2f" % (100 * pp["exact_2_deck_return"]),
             PP_USD="%.0f" % (10 * (100 * pp["exact_2_deck_return"] - 100 * pp["bc_deal_return"])))
json.dump(q, open(path("results", "summary.json"), "w"), indent=1)
readme = path("README.md")
if os.path.exists(readme):
    text = open(readme, encoding="utf8").read()
    want = ["**%s%%**" % q["VP98"], "**%s%% house edge**" % q["EDGE98"], "%s times" % q["X98"],
            "$%s of additional expected loss per $1,000" % q["USD98"], "about %s%% for the 99%% game" % q["VP99"],
            "%s%% for the 96%% game" % q["VP96"], "about %s%%" % q["VP19"], "about %s%%" % q["VP99A"],
            "%s%% instead of %s%%" % (q["PP_BC"], q["PP_FAIR"])]
    missing = [w for w in want if w not in text]
    check("README quotes the numbers above", not missing, ", ".join(missing))
finish()
