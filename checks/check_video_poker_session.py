#!/usr/bin/env python3
"""The 62 video poker hands played on bc.game on 16 Nov 2026 (evidence/video-poker-2026-11-16).

Checks, from BC's own records and the raw game frames:
  0. The raw socket frames decode (checks/frames.py) to the decoded list saved with them; everything below uses the
     fresh decode. Every hand's bet and deal answers are in the frames and carry the recorded cards, held cards, stake
     and credit; BC's balance pushes debit each stake and pay each credit, and the balance moves by exactly those.
  1. BC's own verifier page code, run on each hand's seeds, gives the ten cards BC recorded for that hand.
  2. Our rebuild (src/bcvp.py) gives the same ten cards.
  3. The final hand is the dealt hand with the replaced cards taken in order from card 6.
  4. Every credit is the stake times the multiplier of the paytable the server sent.
  5. Each server seed hashes (SHA256) to the hash BC recorded, and BC sent that hash before the first hand on it. The
     detail lists the frames in order: hash requested, our client seed sent, hash received, hash confirmed.
  6. BC's own hand count per seed pair equals the number of hands here, with nonces 0, 1, 2, ... without gaps.
Writes results/live-sessions/video-poker-hands.csv: one row per hand, with the link to BC's own bet slip for it
(cards, seeds and payout as BC shows them) and a link that opens BC's verifier on its seeds.
"""
import collections
import csv
import datetime
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import FAILS, VP_PAGES, bc_videopoker_page, check, finish, load, path, zigzag_bytes
from decimal import Decimal
import bcvp
import frames as F

recs = [r["data"] for r in load("evidence", "video-poker-2026-11-16", "bet-records.json")]
frames = load("evidence", "video-poker-2026-11-16", "game-frames.json")
print("video poker, 16 Nov 2026: %d hands\n" % len(recs))

# the raw frames, decoded again here; the decoded list saved with them must come out the same
dec = F.decode_requests(frames["frames"], "/g/vp/")
same = sum(F.norm_js(a) == F.norm_js(b) for a, b in zip(dec, frames["decoded"]))
check("raw frames decode to the decoded list saved with them", len(dec) == len(frames["decoded"]) == same,
      "%d / %d requests and answers" % (same, len(frames["decoded"])))

# paytable as the server sent it (answer to init), index = hand class 0..9
inits = [d for d in dec if d["ev"] == "init" and d.get("data")]
tables = []
for d in inits:
    gc = d["data"]["2"][0]
    tables.append((gc["1"][0], json.loads(gc["5"][0]), d["frame_in"]))
paytable = [tables[0][1][str(k)] for k in range(10)]
check("server paytable: %s, %s" % (tables[0][0], "/".join(str(x) for x in reversed(paytable[1:]))),
      all(t[0] == "VideoPoker98" and [t[1][str(k)] for k in range(10)] == paytable for t in tables),
      "init answers in frames %s" % ", ".join(str(t[2]) for t in tables))

rows = [(r["seedHistory"]["serverSeed"], r["seedHistory"]["clientSeed"], r["betLog"]["nonce"]) for r in recs]
page = bc_videopoker_page(VP_PAGES["verifier_2021"], rows)

# hint flags and the hint switch, from the bet answers and requests in the frames; a bet answer is matched to its
# hand by the five dealt cards it carries (field 5.4), which BC sends before any hold
bets = {tuple(zigzag_bytes(d["data"]["5"][0]["4"][0]["_bytes_b64"])): d for d in dec if d["ev"] == "bet" and d.get("data")}

n_page = n_rebuild = n_final = n_credit = n_order = n_order_ok = 0
out = []
for i, (r, (h, ten)) in enumerate(zip(recs, page)):
    b, sh, gv = r["betLog"], r["seedHistory"], r["betLog"]["gv"]
    n_page += ten == gv["initialHard"]
    _, order = bcvp.deal("verifier_2021", sh["serverSeed"], sh["clientSeed"], b["nonce"])
    n_rebuild += order[:10] == gv["initialHard"]
    dealt, held = gv["initialHard"][:5], set(gv.get("holdHard") or [])
    final = bcvp.draw_sequential(dealt, held, gv["initialHard"])
    n_final += final == gv["playerHard"]
    under = [c if c in held else gv["initialHard"][5 + k] for k, c in enumerate(dealt)]   # card under each position
    if under != final:                                                                     # this hand tells them apart
        n_order += 1
        n_order_ok += final == gv["playerHard"]
    cls = bcvp.classify(gv["playerHard"])
    n_credit += abs(float(b["betAmount"]) * paytable[cls] - float(b["winAmount"])) < 1e-9
    bet = bets.get(tuple(dealt))
    hint = suggest = ""
    if bet:
        flags = zigzag_bytes(bet["data"]["5"][0]["5"][0]["_bytes_b64"])
        hint = "".join("H" if f == 0 else "-" for f in flags)            # BC client rule: flag 0 = hold
        bv = bet["request"]["3"][0]                                   # betValue; an empty message means suggest = 0
        raw = bv["1"][0] if isinstance(bv, dict) else 0
        suggest = "on" if ((raw >> 1) ^ -(raw & 1)) == 1 else "off"
    out.append({"hand": i + 1, "bet_id": b["distributeId"], "bc_bet_slip": "https://bc.game/game-detail/%s" % b["distributeId"], "bet_time_utc": datetime.datetime.fromtimestamp(b["betTime"] / 1000, datetime.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"), "client_seed": sh["clientSeed"],
                "nonce": b["nonce"], "dealt": " ".join(bcvp.txt(c) for c in dealt), "dealt_codes": " ".join(map(str, dealt)),
                "ai_hint_switch": suggest, "ai_hint_hold": hint,
                "player_hold": "".join("H" if c in held else "-" for c in dealt),
                "final": " ".join(bcvp.txt(c) for c in gv["playerHard"]), "hand_name": bcvp.CLASS_NAMES[cls],
                "stake_usdt": b["betAmount"], "multiplier": paytable[cls], "credit_usdt": b["winAmount"],
                "bc_page_ten_cards_equal_record": ten == gv["initialHard"],
                "verify_link": "https://game-verify.github.io/public/videopoker.html?s=%s&c=%s&n=%d&he=2&m=0" % (sh["serverSeed"], sh["clientSeed"], b["nonce"])})

check("BC's verifier page code gives the ten recorded cards", n_page == len(recs), "%d / %d hands" % (n_page, len(recs)))
check("our rebuild gives the same ten cards", n_rebuild == len(recs), "%d / %d" % (n_rebuild, len(recs)))
check("final hand = replaced cards taken in order from card 6", n_final == len(recs), "%d / %d" % (n_final, len(recs)))
check("  hands where that differs from 'the card under each position': in order from card 6 every time", n_order_ok == n_order,
      "%d / %d hands" % (n_order_ok, n_order))
check("credit = stake x paytable multiplier", n_credit == len(recs), "%d / %d" % (n_credit, len(recs)))

# every hand's answers in the raw frames, against BC's record of it
hands = F.vp_hands(dec)
by_id = {h["deal_id"]: h for h in hands if "deal_id" in h}
pairs_found = [(r["betLog"], by_id.get(r["betLog"]["distributeId"])) for r in recs]
n_req = sum(h["deal_requests"] for h in hands)
check("every hand's bet and deal answers are in the frames", len(hands) == len(recs) and all(h for _, h in pairs_found),
      "%d / %d hands; %d deal requests, %d answered (one was sent twice)" % (sum(1 for _, h in pairs_found if h), len(recs), n_req, len(by_id)))
check("  BC's answers carry the recorded cards: dealt five at the bet, all ten and the final hand at the deal",
      all(h["dealt"] == b["gv"]["initialHard"][:5] and h["ten"] == b["gv"]["initialHard"] and h["final"] == b["gv"]["playerHard"]
          for b, h in pairs_found), "%d / %d" % (len(pairs_found), len(recs)))
check("  the held cards we sent = the held cards BC recorded",
      all(sorted(h["held_sent"]) == sorted(b["gv"].get("holdHard") or []) for b, h in pairs_found), "%d / %d" % (len(pairs_found), len(recs)))
check("  stake and credit in BC's answers = the record",
      all(Decimal(h["stake"]) == Decimal(b["betAmount"]) == Decimal(h["stake_at_deal"]) and Decimal(h["win"]) == Decimal(b["winAmount"])
          for b, h in pairs_found), "%d / %d" % (len(pairs_found), len(recs)))
pushes = F.balance_pushes(frames["frames"])
chain = all(Decimal(pushes[i]["balance"]) == Decimal(pushes[i - 1]["balance"]) + Decimal(pushes[i]["change"]) for i in range(1, len(pushes)))
ids = {i for h in hands for i in (h["bet_id"], h.get("deal_id"))}
per_hand = all(sum(Decimal(p["change"]) for p in pushes if p["id"] in (h["bet_id"], h["deal_id"])) == Decimal(h["win"]) - Decimal(h["stake"])
               for h in hands)
check("BC's balance pushes: every stake debited, every credit paid, the balance moving by exactly those amounts",
      chain and per_hand and {p["id"] for p in pushes} <= ids,
      "%d pushes: %d stakes, %d credits" % (len(pushes), sum(Decimal(p["change"]) < 0 for p in pushes), sum(Decimal(p["change"]) > 0 for p in pushes)))

# seed commitments: the hash BC sent before the first hand, and the order of the frames around the seed change
changes = F.seed_changes(dec)
pairs = collections.OrderedDict()
for r in recs:
    pairs.setdefault((r["seedHistory"]["serverSeed"], r["seedHistory"]["clientSeed"]), []).append(r)
for (server, client), rs in pairs.items():
    h = rs[0]["seedHistory"]["serverSeedHash"]
    first = min(x["betLog"]["betTime"] for x in rs)
    sc = next((c for c in changes if c["hash"] == h and c["client_seed"] == client), None)
    check("seed pair %s: SHA256(server seed) = recorded hash" % client, hashlib.sha256(server.encode()).hexdigest() == h)
    ok = bool(sc and sc["hash_answer"]) and sc["hash_answer"]["frame_out"] < sc["change"]["frame_out"] and sc["change"]["t_in"] < first
    check("seed pair %s: BC sent that hash before the first hand" % client, ok,
          ("hash requested in frame %d, our client seed sent in frame %d, hash received in frame %d and confirmed in frame %d, %.0f s before the first hand"
           % (sc["hash_answer"]["frame_out"], sc["change"]["frame_out"], sc["hash_answer"]["frame_in"], sc["change"]["frame_in"], (first - sc["change"]["t_in"]) / 1000))
          if sc and sc["hash_answer"] else "not found")
    nonces = sorted(x["betLog"]["nonce"] for x in rs)
    bc_count = {x["seedHistory"]["maxNonce"] for x in rs}
    check("seed pair %s: no hand missing" % client, nonces == list(range(len(rs))) and bc_count == {len(rs)},
          "BC counts %s hands on this seed pair, %d here, nonces 0 to %d" % ("/".join(map(str, bc_count)), len(rs), nonces[-1]))

staked = sum(float(r["betLog"]["betAmount"]) for r in recs)
credited = sum(float(r["betLog"]["winAmount"]) for r in recs)
print("\nstaked %.2f USDT, credited %.2f USDT" % (staked, credited))
os.makedirs(path("results", "live-sessions"), exist_ok=True)
with open(path("results", "live-sessions", "video-poker-hands.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
    w.writeheader()
    w.writerows(out)
print("wrote results/live-sessions/video-poker-hands.csv")
finish()
