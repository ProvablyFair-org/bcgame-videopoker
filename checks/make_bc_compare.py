#!/usr/bin/env python3
"""Writes checks/compare_with_bc.js: a snippet to paste into the browser console on https://bc.game. It fetches BC's
public record of each of the 212 live bets (the record behind https://bc.game/game-detail/<bet id>, no login) and
compares it, field group by field group, with the records in this package:
  game       which game (gameUnique, gameName)
  bet        bet id, currency, bet time
  seeds      server seed, server seed hash, client seed, nonce
  selection  video poker: the hint switch and the held cards; baccarat: each bet's type and amount
  cards      video poker: the ten cards and the final hand; baccarat: both hands and both totals
  money      stake and payout
Each group is compared by a SHA-256 fingerprint, so the snippet carries no seeds or cards itself. It prints one line
per bet (the groups that differ, if any) and a total.
With --check (run by make check): the fingerprints in compare_with_bc.js are the ones these records give, for all 212
bets, and results/live-sessions/bc-public-records-check.txt lists the same 212 bets, every group the same.
"""
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import check, finish, load, path

GROUPS = ("game", "bet", "seeds", "selection", "cards", "money")


def s(v):
    return "" if v is None else str(v)


def groups(d):
    b, sd, gv, bv = d["betLog"], d["seedHistory"], d["betLog"]["gv"], d["betLog"]["bv"] or {}
    if d["gameUnique"] == "video-poker":
        sel = [s(bv.get("suggest")), ",".join(map(s, gv.get("holdHard") or []))]
        cards = [",".join(map(s, gv.get("initialHard") or [])), ",".join(map(s, gv.get("playerHard") or []))]
    else:
        sel = [";".join("%s:%s" % (s(x["type"]), s(x["betAmount"])) for x in bv.get("betData") or [])]
        cards = [",".join(map(s, gv["players"])), ",".join(map(s, gv["bankers"])), s(gv["playerPoint"]), s(gv["bankerPoint"])]
    return {"game": [s(d["gameUnique"]), s(d.get("gameName"))],
            "bet": [s(b["distributeId"]), s(b["currencyName"]), s(b["betTime"])],
            "seeds": [s(sd["serverSeed"]), s(sd["serverSeedHash"]), s(sd["clientSeed"]), s(b["nonce"])],
            "selection": sel, "cards": cards, "money": [s(b["betAmount"]), s(b["winAmount"])]}


def fingerprints(d):
    return [hashlib.sha256("|".join(v).encode()).hexdigest()[:16] for v in (groups(d)[g] for g in GROUPS)]


recs = [r["data"] for r in load("evidence", "video-poker-2026-11-16", "bet-records.json") + load("evidence", "baccarat-2026-11-16", "bet-records.json")]
exp = {d["betLog"]["distributeId"]: fingerprints(d) for d in recs}
JS = """// Compare BC's public bet records with this package. Paste into the browser console on https://bc.game and wait about a minute.
// Written by checks/make_bc_compare.py from the bet records in evidence/. No login needed; nothing is sent anywhere else.
// Each bet: SHA-256 fingerprints of six field groups (game, bet, seeds, selection, cards, money); see make_bc_compare.py.
(async () => {
  const GROUPS = %s;
  const expected = %s;
  const s = (v) => (v === null || v === undefined) ? '' : String(v);
  const groups = (d) => { const b = d.betLog, sd = d.seedHistory, gv = b.gv, bv = b.bv || {};
    const vp = d.gameUnique === 'video-poker';
    const sel = vp ? [s(bv.suggest), (gv.holdHard || []).map(s).join(',')]
                   : [(bv.betData || []).map(x => s(x.type) + ':' + s(x.betAmount)).join(';')];
    const cards = vp ? [(gv.initialHard || []).map(s).join(','), (gv.playerHard || []).map(s).join(',')]
                     : [gv.players.map(s).join(','), gv.bankers.map(s).join(','), s(gv.playerPoint), s(gv.bankerPoint)];
    return {game: [s(d.gameUnique), s(d.gameName)], bet: [s(b.distributeId), s(b.currencyName), s(b.betTime)],
            seeds: [s(sd.serverSeed), s(sd.serverSeedHash), s(sd.clientSeed), s(b.nonce)], selection: sel, cards: cards,
            money: [s(b.betAmount), s(b.winAmount)]}; };
  const sha = async (t) => Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(t))))
    .map(x => x.toString(16).padStart(2, '0')).join('').slice(0, 16);
  const lines = []; let same = 0;
  for (const [id, want] of Object.entries(expected)) {
    let line;
    try {
      const j = await (await fetch('/api/game/bet/v2/bet/' + id, {credentials: 'omit'})).json();
      if (!j || !j.data) line = id + '  no record';
      else {
        const g = groups(j.data), differ = [];
        for (let i = 0; i < GROUPS.length; i++) if (await sha(g[GROUPS[i]].join('|')) !== want[i]) differ.push(GROUPS[i]);
        if (!differ.length) same++;
        line = id + '  ' + j.data.gameUnique + '  ' + (differ.length ? 'differs: ' + differ.join(', ') : 'same: ' + GROUPS.join(', '));
      }
    } catch (e) { line = id + '  error ' + e; }
    lines.push(line);
    await new Promise(res => setTimeout(res, 150));
  }
  const total = 'BC public records matching this package: ' + same + ' of ' + Object.keys(expected).length;
  console.log(lines.join('\\n') + '\\n' + total);
  return total;
})();
"""


def write():
    js = JS % (json.dumps(list(GROUPS)), json.dumps(exp, indent=1))
    open(path("checks", "compare_with_bc.js"), "w").write(js)
    print("wrote checks/compare_with_bc.js for %d bets" % len(exp))


if "--check" in sys.argv:
    js = open(path("checks", "compare_with_bc.js")).read()
    m = re.search(r"const expected = (\{[\s\S]*?\n\});", js)
    embedded = json.loads(m.group(1)) if m else {}
    check("compare_with_bc.js expects exactly what these bet records give", embedded == exp, "%d bets, 6 field groups each" % len(embedded))
    receipt = open(path("results", "live-sessions", "bc-public-records-check.txt")).read()
    rows = dict(re.findall(r"^(\d{19})  \S+  (.+)$", receipt, re.M))
    check("BC's public records, 17 Nov 2026: every bet here, every field group the same", set(rows) == set(exp) and
          all(v == "same: " + ", ".join(GROUPS) for v in rows.values()), "%d / %d bets in the receipt" % (sum(v.startswith("same") for v in rows.values()), len(exp)))
    finish()
else:
    write()
