#!/usr/bin/env python3
"""The 150 baccarat rounds played on bc.game on 16 Nov 2026 (evidence/baccarat-2026-11-16).

Checks, from BC's own records and the raw game frames:
  0. The raw socket frames are decoded (checks/frames.py). Every round's bet request and answer are in them: the bets we
     sent are the bets BC recorded, and BC's answer carries the recorded cards, totals, stake and credit. BC's balance
     pushes move the balance by exactly each round's credit minus stake.
  1. BC's own verifier page code, run on each round's seeds, gives the cards and totals BC recorded.
  2. Our rebuild (src/bcbac.py) gives the same 104-card shoe and the same hands.
  3. Every credit is the stakes times the odds the server sent (a tie gives player and banker bets 0.9908 back).
  4. Each server seed hashes (SHA256) to the hash BC recorded, and BC sent that hash before the first round on it. The
     detail lists the frames in order: hash requested, our client seed sent, hash received, hash confirmed.
  5. BC's own round count per seed pair equals the number of rounds here, with nonces 0, 1, 2, ... without gaps.
Writes results/live-sessions/baccarat-rounds.csv: one row per round, with the link to BC's own bet slip and to BC's verifier.
"""
import base64
import collections
import csv
import datetime
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import bc_baccarat_page, check, finish, load, path
from decimal import Decimal
import bcbac
import frames as F

recs = [r["data"] for r in load("evidence", "baccarat-2026-11-16", "bet-records.json")]
frames = load("evidence", "baccarat-2026-11-16", "game-frames.json")["frames"]
print("baccarat, 16 Nov 2026: %d rounds\n" % len(recs))
dec = F.decode_requests(frames, "/g/baccarats/")

# odds as the server sent them: a JSON object inside the init answers of the game namespace
odds_seen = []
for f in frames:
    raw = base64.b64decode(f["b64"])
    m = re.search(rb'\{[^{}]*"playerBigBankerOdds"[^{}]*\}', raw)
    if m and f["dir"] == "in":
        odds_seen.append((f["i"], json.loads(m.group(0))))
odds = odds_seen[0][1]
check("server odds: player %s, banker %s, tie %s, pairs %s, main bets on a tie %s" % (
      odds["playerBigBankerOdds"], odds["bankerBigPlayerOdds"], odds["tieOdds"], odds["pairOdds"], odds["playerTieOdds"]),
      all(o == odds for _, o in odds_seen), "same in all %d init answers" % len(odds_seen))
PAY = {0: odds["playerBigBankerOdds"], 1: odds["bankerBigPlayerOdds"], 2: odds["tieOdds"], 3: odds["pairOdds"], 4: odds["pairOdds"]}
TIE_MAIN = {0: odds["playerTieOdds"], 1: odds["bankerTieOdds"]}
NAMES = {0: "player", 1: "banker", 2: "tie", 3: "player pair", 4: "banker pair"}


def card(c):
    return " A 2 3 4 5 6 7 8 9 10 J Q K".split(" ")[c % 16] + "♠♥♣♦"[c // 16 - 10]

rows = [(r["seedHistory"]["serverSeed"], r["seedHistory"]["clientSeed"], r["betLog"]["nonce"]) for r in recs]
page = bc_baccarat_page(rows)
n_page = n_rebuild = n_credit = 0
placed, won = collections.Counter(), collections.Counter()
out = []
for i, (r, pg) in enumerate(zip(recs, page)):
    b, sh, gv = r["betLog"], r["seedHistory"], r["betLog"]["gv"]
    hm, shoe, p, bk, pt, bt = bcbac.deal(sh["serverSeed"], sh["clientSeed"], b["nonce"])
    n_rebuild += (p == gv["players"] and bk == gv["bankers"] and pt == gv["playerPoint"] and bt == gv["bankerPoint"]
                  and shoe == pg["shoe"])
    # the page shows 10, J, Q and K as 10 points; mod 10 that is the 0 of the rebuild
    n_page += ([v % 10 for v in pg["player_values"]] == [bcbac.value(c) for c in gv["players"]]
               and [v % 10 for v in pg["banker_values"]] == [bcbac.value(c) for c in gv["bankers"]]
               and pg["player_total"] == gv["playerPoint"] and pg["banker_total"] == gv["bankerPoint"])
    res = bcbac.outcome(p, bk, pt, bt)
    hit = {0: res["player"], 1: res["banker"], 2: res["tie"], 3: res["player_pair"], 4: res["banker_pair"]}
    credit = 0.0
    for bd in b["bv"]["betData"]:
        t, st = bd["type"], float(bd["betAmount"])
        placed[t] += 1
        if t in (0, 1) and res["tie"]:
            credit += st * TIE_MAIN[t]
        elif hit[t]:
            credit += st * PAY[t]
            won[t] += 1
    n_credit += abs(credit - float(b["winAmount"])) < 1e-6
    out.append({"round": i + 1, "bet_id": b["distributeId"], "bc_bet_slip": "https://bc.game/game-detail/%s" % b["distributeId"],
                "bet_time_utc": datetime.datetime.fromtimestamp(b["betTime"] / 1000, datetime.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
                "client_seed": sh["clientSeed"], "nonce": b["nonce"],
                "bets": " + ".join(NAMES[bd["type"]] for bd in b["bv"]["betData"]), "stake_usdt": b["betAmount"],
                "player": " ".join(card(c) for c in gv["players"]), "player_total": pt,
                "banker": " ".join(card(c) for c in gv["bankers"]), "banker_total": bt,
                "credit_usdt": b["winAmount"],
                "verify_link": "https://game-verify.github.io/public/baccaratsingle.html?s=%s&c=%s&n=%d&he=2&m=0" % (sh["serverSeed"], sh["clientSeed"], b["nonce"])})
check("BC's verifier page code gives the recorded hands and totals", n_page == len(recs), "%d / %d rounds" % (n_page, len(recs)))
check("our rebuild gives the same 104-card shoe and hands", n_rebuild == len(recs), "%d / %d" % (n_rebuild, len(recs)))
check("credit = stakes x server odds", n_credit == len(recs), "%d / %d rounds, %d bets" % (n_credit, len(recs), sum(placed.values())))
print("      bets placed: " + ", ".join("%s %d" % (NAMES[t], placed[t]) for t in sorted(placed)))
print("      bets won:    " + ", ".join("%s %d" % (NAMES[t], won[t]) for t in sorted(placed)))

# every round's request and answer in the raw frames, against BC's record of it
rounds = F.baccarat_rounds(dec)
by_id = {x["id"]: x for x in rounds if x["code"] == 0}
found = [(r["betLog"], by_id.get(r["betLog"]["distributeId"])) for r in recs]
check("every round's bet request and answer are in the frames", len(rounds) == len(recs) and all(x for _, x in found),
      "%d / %d rounds, all answered with code 0" % (sum(1 for _, x in found if x), len(recs)))
check("  the bets we sent = the bets BC recorded (type and amount)",
      all(x["bets_sent"] == [(bd["type"], bd["betAmount"]) for bd in b["bv"]["betData"]] and Decimal(x["stake_sent"]) == Decimal(b["betAmount"])
          for b, x in found), "%d / %d rounds" % (len(found), len(recs)))
check("  BC's answers carry the recorded cards and totals",
      all(x["players"] == b["gv"]["players"] and x["bankers"] == b["gv"]["bankers"] and x["player_point"] == b["gv"]["playerPoint"]
          and x["banker_point"] == b["gv"]["bankerPoint"] for b, x in found), "%d / %d" % (len(found), len(recs)))
check("  stake and credit in BC's answers = the record",
      all(Decimal(x["stake"]) == Decimal(b["betAmount"]) and Decimal(x["credit"]) == Decimal(b["winAmount"]) for b, x in found),
      "%d / %d" % (len(found), len(recs)))
pushes = F.balance_pushes(frames)
chain = all(Decimal(pushes[i]["balance"]) == Decimal(pushes[i - 1]["balance"]) + Decimal(pushes[i]["change"]) for i in range(1, len(pushes)))
per_round = all(sum(Decimal(p["change"]) for p in pushes if p["id"] == b["distributeId"]) == Decimal(b["winAmount"]) - Decimal(b["betAmount"])
                for b, _ in found)
check("BC's balance pushes: the balance moves by exactly each round's credit minus stake",
      chain and per_round and {p["id"] for p in pushes} == {b["distributeId"] for b, _ in found}, "%d pushes, one per round" % len(pushes))

pairs = collections.OrderedDict()
for r in recs:
    pairs.setdefault((r["seedHistory"]["serverSeed"], r["seedHistory"]["clientSeed"]), []).append(r)
for (server, client), rs in pairs.items():
    h = rs[0]["seedHistory"]["serverSeedHash"]
    first = min(x["betLog"]["betTime"] for x in rs)
    sc = next((c for c in F.seed_changes(dec) if c["hash"] == h and c["client_seed"] == client), None)
    check("seed pair %s: SHA256(server seed) = recorded hash" % client, hashlib.sha256(server.encode()).hexdigest() == h)
    ok = bool(sc and sc["hash_answer"]) and sc["hash_answer"]["frame_out"] < sc["change"]["frame_out"] and sc["change"]["t_in"] < first
    check("seed pair %s: BC sent that hash before the first round" % client, ok,
          ("hash requested in frame %d, our client seed sent in frame %d, hash received in frame %d and confirmed in frame %d, %.0f s before the first round"
           % (sc["hash_answer"]["frame_out"], sc["change"]["frame_out"], sc["hash_answer"]["frame_in"], sc["change"]["frame_in"], (first - sc["change"]["t_in"]) / 1000))
          if sc and sc["hash_answer"] else "not found")
    nonces = sorted(x["betLog"]["nonce"] for x in rs)
    bc_count = {x["seedHistory"]["maxNonce"] for x in rs}
    check("seed pair %s: no round missing" % client, nonces == list(range(len(rs))) and bc_count == {len(rs)},
          "BC counts %s rounds on this seed pair, %d here" % ("/".join(map(str, bc_count)), len(rs)))

print("\nstaked %.2f USDT, credited %.5f USDT" % (sum(float(r["betLog"]["betAmount"]) for r in recs), sum(float(r["betLog"]["winAmount"]) for r in recs)))
os.makedirs(path("results", "live-sessions"), exist_ok=True)
with open(path("results", "live-sessions", "baccarat-rounds.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
    w.writeheader()
    w.writerows(out)
print("wrote results/live-sessions/baccarat-rounds.csv")
finish()
