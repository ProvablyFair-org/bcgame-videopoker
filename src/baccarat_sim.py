#!/usr/bin/env python3
"""Baccarat: outcome probabilities and per-bet returns, fairly shuffled shoe (exact) vs BC's verifier deal (simulated).

1. EXACT, fairly shuffled shoe of D decks (D = 1, 2, 6, 8): every ordered sequence of six card values, weighted by the
   number of ways to draw it without replacement, played through src/bcbac.play (the verifier's drawing rules).
   Pair probability (first two cards of one hand of the same rank) = (4D-1)/(52D-1).
2. BC DEAL, simulated: src/bcbac's deal exactly as the verifier computes it. Seed material is generated here
   (server seed = sha256("pf-baccarat-sim <batch> <k>"), client seed "pfbaccsim", nonces 0..999 per server seed).
   95% CI from the binomial standard error.
3. CONTROL: the same counting code fed by a uniform draw of 6 cards from the same 104 (random.Random(batch seed).sample).
   Check: each of the five control frequencies must lie within 3 standard errors of the exact 2-deck value.

Returns use the odds BC's server sent for BaccaratSingle98 on 16 Nov 2026 (read from evidence/baccarat-2026-11-16/
game-frames.json and compared with the table below on every run), including what a tie pays a player or banker bet
(0.9908 of the stake). Pair = the first two cards of that hand have the same rank, as on all 150 live rounds.

usage: python3 src/baccarat_sim.py [rounds_bc=40000000] [rounds_control=40000000] [procs=cpu count]
       -> results/baccarat/returns.json, returns.txt
"""
import base64
import hashlib
import itertools
import json
import math
import multiprocessing as mp
import os
import random
import re
import sys
import time
from fractions import Fraction

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(R, "src"))
import bcbac  # noqa: E402

KEYS = ["player", "banker", "tie", "player_pair", "banker_pair"]
EXTRA = ["player_third", "banker_third", "natural"]
# gross multipliers (stake included)
REAL = "server_98"
PAYTABLES = {
    REAL: {"source": "the odds BC's server sent for BaccaratSingle98 on 16 Nov 2026 (answer to init, namespace /g/baccarats/98, "
                     "evidence/baccarat-2026-11-16/game-frames.json): playerBigBankerOdds 1.9817, bankerBigPlayerOdds 1.9322, "
                     "tieOdds 8.918, pairOdds 11.8907, playerTieOdds = bankerTieOdds = 0.9908; each paid on the live rounds",
           "player": 1.9817, "banker": 1.9322, "tie": 8.9180, "player_pair": 11.8907, "banker_pair": 11.8907, "tie_main": 0.9908},
}


def exact(decks):
    cnt = [16 * decks] + [4 * decks] * 9
    n = 52 * decks
    tot = {k: 0 for k in KEYS[:3] + EXTRA}
    denom = 1
    for i in range(6):
        denom *= n - i
    for seq in itertools.product(range(10), repeat=6):
        c = cnt[:]
        w = 1
        for v in seq:
            w *= c[v]
            c[v] -= 1
            if not w:
                break
        if not w:
            continue
        # bcbac.play reads rank via value(card); a code with suit 10 and rank v (v = 0 -> rank 10) has that value
        cards = [160 + (v if v else 10) for v in seq]
        p, b, pt, bt = bcbac.play(cards)
        tot["player" if pt > bt else "banker" if bt > pt else "tie"] += w
        tot["player_third"] += w * (len(p) == 3)
        tot["banker_third"] += w * (len(b) == 3)
        tot["natural"] += w * (len(p) == 2 and len(b) == 2 and (bcbac.value(p[0]) + bcbac.value(p[1])) % 10 >= 8
                               or len(p) == 2 and len(b) == 2 and (bcbac.value(b[0]) + bcbac.value(b[1])) % 10 >= 8)
    fr = {k: Fraction(v, denom) for k, v in tot.items()}
    assert fr["player"] + fr["banker"] + fr["tie"] == 1
    fr["player_pair"] = fr["banker_pair"] = Fraction(4 * decks - 1, 52 * decks - 1)
    return fr


def count(first6, t):
    p, b, pt, bt = bcbac.play(first6)
    if pt > bt:
        t[0] += 1
    elif bt > pt:
        t[1] += 1
    else:
        t[2] += 1
    if p[0] % 16 == p[1] % 16:
        t[3] += 1
    if b[0] % 16 == b[1] % 16:
        t[4] += 1
    if len(p) == 3:
        t[5] += 1
    if len(b) == 3:
        t[6] += 1
    # joint cells for exact per-bet variance are not needed: each bet's return depends on one or two counters
    return t


def work_bc(args):
    batch, rounds = args
    t = [0] * 7
    sha, hm = hashlib.sha256, bcbac.hmac_hex
    ALL = bcbac.ALL
    done = k = 0
    while done < rounds:
        server = sha(("pf-baccarat-sim %d %d" % (batch, k)).encode()).hexdigest()
        k += 1
        for nonce in range(min(1000, rounds - done)):
            h = sha(hm(server, "pfbaccsim", nonce).encode()).hexdigest()
            keyed = []
            for _ in range(2):
                hh = h + h
                keyed += [(hh[j:j + 64], c) for j, c in enumerate(ALL)]
                h = sha(h.encode()).hexdigest()
            keyed.sort(key=lambda kc: kc[0])
            count([c for _, c in keyed[:6]], t)
            done += 1
    return t


def work_control(args):
    batch, rounds = args
    t = [0] * 7
    rng = random.Random("pf-baccarat-control %d" % batch)
    shoe = bcbac.ALL * 2
    for _ in range(rounds):
        count(rng.sample(shoe, 6), t)
    return t


def check_real_table():
    """The table in this script must equal the odds in the server's init answers in the captured game frames."""
    p = os.path.join(R, "evidence", "baccarat-2026-11-16", "game-frames.json")
    seen = set()
    for f in json.load(open(p))["frames"]:
        m = re.search(rb'\{[^{}]*"playerBigBankerOdds"[^{}]*\}', base64.b64decode(f["b64"]))
        if m and f["dir"] == "in":
            seen.add(json.dumps(json.loads(m.group(0)), sort_keys=True))
    t = PAYTABLES[REAL]
    want = {"playerBigBankerOdds": t["player"], "bankerBigPlayerOdds": t["banker"], "tieOdds": t["tie"], "pairOdds": t["player_pair"],
            "playerTieOdds": t["tie_main"], "bankerTieOdds": t["tie_main"]}
    got = [json.loads(x) for x in seen]
    if len(got) != 1 or any(float(got[0][k]) != v for k, v in want.items()):
        sys.exit("FAIL: the server odds in this script %s differ from the captured ones %s" % (want, got))
    return "equal to the odds in the init answers of evidence/baccarat-2026-11-16/game-frames.json"


def run(fn, rounds, procs, batches):
    per = rounds // batches
    with mp.Pool(procs) as pool:
        res = pool.map(fn, [(b, per) for b in range(batches)])
    return res, per


def summarise(res, per):
    n = per * len(res)
    out = {"rounds": n, "batches": len(res), "rounds_per_batch": per}
    for i, k in enumerate(KEYS + EXTRA[:2]):
        x = sum(r[i] for r in res)
        p = x / n
        se = math.sqrt(p * (1 - p) / n)
        bp = [r[i] / per for r in res]
        mean = sum(bp) / len(bp)
        bsd = math.sqrt(sum((v - mean) ** 2 for v in bp) / (len(bp) - 1)) if len(bp) > 1 else None
        out[k] = {"count": x, "p": p, "se": se, "ci95": [p - 1.96 * se, p + 1.96 * se],
                  "se_from_batches": bsd / math.sqrt(len(bp)) if bsd is not None else None}
    return out


def returns(prob, se=None):
    """prob: dict of probabilities (float). -> per paytable, per bet: return, and SE if se given.
    player/banker bets: X = m on a win, the table's tie_main on a tie, 0 otherwise. Var from the trinomial cells."""
    out = {}
    for name, pt in PAYTABLES.items():
        o = {}
        for bet in KEYS:
            m = pt[bet]
            if m is None:
                o[bet] = None
                continue
            if bet in ("player", "banker"):
                tm = pt["tie_main"]
                ex = m * prob[bet] + tm * prob["tie"]
                ex2 = m * m * prob[bet] + tm * tm * prob["tie"]
            else:
                ex = m * prob[bet]
                ex2 = m * m * prob[bet]
            o[bet] = {"multiplier": m, "return": ex}
            if se is not None:
                o[bet]["se"] = math.sqrt(max(ex2 - ex * ex, 0) / se)
                o[bet]["ci95"] = [ex - 1.96 * o[bet]["se"], ex + 1.96 * o[bet]["se"]]
        out[name] = o
    return out


def main():
    argv = sys.argv[1:]
    n_bc = int(argv[0]) if len(argv) > 0 else 40000000
    n_ct = int(argv[1]) if len(argv) > 1 else 40000000
    procs = int(argv[2]) if len(argv) > 2 else os.cpu_count()
    chk = check_real_table()
    batches = 40
    t0 = time.time()
    ex = {d: exact(d) for d in (1, 2, 6, 8)}
    t1 = time.time()
    bc_res, per = run(work_bc, n_bc, procs, batches)
    t2 = time.time()
    ct_res, perc = run(work_control, n_ct, procs, batches)
    t3 = time.time()
    bc, ct = summarise(bc_res, per), summarise(ct_res, perc)
    e2 = {k: float(v) for k, v in ex[2].items()}
    rule = {}
    for k in KEYS:
        se = math.sqrt(e2[k] * (1 - e2[k]) / ct["rounds"])
        z = (ct[k]["p"] - e2[k]) / se
        rule[k] = {"exact": e2[k], "control": ct[k]["p"], "z": z, "within_3_se": abs(z) <= 3}
    doc = {"generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "command": "python3 src/baccarat_sim.py %d %d %d" % (n_bc, n_ct, procs),
           "runtime_seconds": {"exact_4_shoes": round(t1 - t0, 1), "bc_deal": round(t2 - t1, 1), "control": round(t3 - t2, 1)},
           "assumptions": ["payouts: the server's odds; a tie pays a player or banker bet 0.9908 of the stake (paid on the live tie rounds of 16 Nov)",
                           "pair = first two cards of that hand have the same rank (as on all 150 live rounds of 16 Nov)",
                           "the BC deal is the published verifier's deal, which the live game matched on all 150 rounds of 16 Nov"],
           "real_paytable": REAL, "real_paytable_check": chk,
           "paytables": {k: v["source"] for k, v in PAYTABLES.items()},
           "exact_fair_shoe": {str(d): {k: {"fraction": "%d/%d" % (v.numerator, v.denominator), "p": float(v)} for k, v in ex[d].items()} for d in ex},
           "exact_fair_shoe_returns": {str(d): returns({k: float(v) for k, v in ex[d].items()}) for d in ex},
           "bc_deal_simulated": bc, "bc_deal_returns": returns({k: bc[k]["p"] for k in KEYS}, bc["rounds"]),
           "control_uniform_2_decks": ct, "control_returns": returns({k: ct[k]["p"] for k in KEYS}, ct["rounds"]),
           "control_agreement_rule": {"rule": "each control frequency within 3 SE of the exact 2-deck value", "bets": rule,
                                      "result": "PASS" if all(v["within_3_se"] for v in rule.values()) else "MISS"}}
    real_bc, real_ex, real_ct = doc["bc_deal_returns"][REAL], doc["exact_fair_shoe_returns"]["2"][REAL], doc["control_returns"][REAL]
    doc["per_bet_table_real_payouts"] = {
        bet: {"pays": PAYTABLES[REAL][bet], "exact_2_deck_return": real_ex[bet]["return"], "bc_deal_return": real_bc[bet]["return"],
              "bc_deal_ci95": real_bc[bet]["ci95"], "control_return": real_ct[bet]["return"], "control_ci95": real_ct[bet]["ci95"],
              "bc_minus_exact_points": 100 * (real_bc[bet]["return"] - real_ex[bet]["return"]),
              "exact_inside_bc_ci95": real_bc[bet]["ci95"][0] <= real_ex[bet]["return"] <= real_bc[bet]["ci95"][1]} for bet in KEYS}
    out = os.path.join(R, "results", "baccarat")
    os.makedirs(out, exist_ok=True)
    json.dump(doc, open(os.path.join(out, "returns.json"), "w"), indent=1)
    L = [doc["command"], "generated %s; runtimes (s): %s" % (doc["generated_utc"], doc["runtime_seconds"]), ""]
    L.append("ASSUMPTIONS: " + "; ".join(doc["assumptions"]))
    L.append("")
    L.append("Outcome probabilities (%)")
    L.append("%-13s %12s %12s %12s %12s | %-28s | %-28s" % ("", "exact 1 deck", "exact 2", "exact 6", "exact 8",
                                                           "BC deal (95%% CI), n=%d" % bc["rounds"], "control (95%% CI), n=%d" % ct["rounds"]))
    for k in KEYS + EXTRA[:2]:
        L.append("%-13s %12.6f %12.6f %12.6f %12.6f | %9.4f (%8.4f..%8.4f) | %9.4f (%8.4f..%8.4f)"
                 % ((k,) + tuple(100 * float(ex[d][k]) for d in (1, 2, 6, 8))
                    + (100 * bc[k]["p"], 100 * bc[k]["ci95"][0], 100 * bc[k]["ci95"][1], 100 * ct[k]["p"], 100 * ct[k]["ci95"][0], 100 * ct[k]["ci95"][1])))
    L.append("")
    L.append("Control agreement rule (each frequency within 3 SE of the exact 2-deck value): %s" % doc["control_agreement_rule"]["result"])
    for k, v in rule.items():
        L.append("   %-12s z = %+.2f" % (k, v["z"]))
    L.append("")
    L.append("server table check: " + chk)
    for name in PAYTABLES:
        L.append("")
        L.append("Returns (%), the server's odds for BaccaratSingle98")
        L.append("   a tie pays a player or banker bet: %s of the stake" % PAYTABLES[name]["tie_main"])
        L.append("   source: " + PAYTABLES[name]["source"])
        L.append("   %-12s %7s %10s %10s %10s %10s | %-30s | %-30s | %s" % ("bet", "pays", "exact 1", "exact 2", "exact 6", "exact 8", "BC deal (95% CI)", "control (95% CI)", "BC deal minus exact 2 decks, points"))
        for bet in KEYS:
            e = [100 * doc["exact_fair_shoe_returns"][str(d)][name][bet]["return"] for d in (1, 2, 6, 8)]
            b, c = doc["bc_deal_returns"][name][bet], doc["control_returns"][name][bet]
            L.append("   %-12s %7s %10.4f %10.4f %10.4f %10.4f | %8.3f (%8.3f..%8.3f) | %8.3f (%8.3f..%8.3f) | %+.3f"
                     % (bet, PAYTABLES[name][bet], e[0], e[1], e[2], e[3], 100 * b["return"], 100 * b["ci95"][0], 100 * b["ci95"][1],
                        100 * c["return"], 100 * c["ci95"][0], 100 * c["ci95"][1], 100 * b["return"] - e[1]))
    open(os.path.join(out, "returns.txt"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
