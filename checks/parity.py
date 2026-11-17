#!/usr/bin/env python3
"""Parity: our code deals exactly what BC's own page code deals.

  - src/bcvp.py against BC's video poker pages (Nov 2019, Apr 2020 and the current page), N random seed sets each
  - src/bcbac.py against BC's baccarat page, N random seed sets: the full 104-card shoe, both hands, both totals
  - src/vpsim.c (the simulator behind every return in results/) against the same pages, on the server seed of every
    stored run and 17 more, at nonces 0..4, at a random point and at the last nonces a 100M-deal run uses
BC's page code runs unedited in node (checks/bc_page_*.js). usage: python3 checks/parity.py [N, default 10000]
"""
import glob
import os
import random
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import VP_PAGES, bc_baccarat_page, bc_videopoker_page, check, finish, path
import bcbac
import bcvp

N = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
rng = random.Random(20261117)


def seeds(n):
    out = []
    for _ in range(n):
        server = "%064x" % rng.getrandbits(256)
        client = "".join(rng.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(rng.randint(8, 32)))
        out.append((server, client, rng.randint(0, 100000)))
    return out


for variant, label in [("verifier_2019", "Nov 2019 page"), ("verifier_2020", "Apr 2020 page"), ("verifier_2021", "current page")]:
    rows = seeds(N)
    page = bc_videopoker_page(VP_PAGES[variant], rows)
    same = sum(h == bcvp.deal(variant, *r)[0] and ten == bcvp.deal(variant, *r)[1][:10] for r, (h, ten) in zip(rows, page))
    check("video poker, %s: rebuild = BC's code (hash and ten cards)" % label, same == N, "%d / %d seed sets" % (same, N))

rows = seeds(N)
page = bc_baccarat_page(rows)
same = 0
for r, pg in zip(rows, page):
    hm, shoe, p, b, pt, bt = bcbac.deal(*r)
    same += (hm == pg["hmac"] and shoe == pg["shoe"] and [bcbac.value(c) for c in p] == [v % 10 for v in pg["player_values"]]
             and [bcbac.value(c) for c in b] == [v % 10 for v in pg["banker_values"]] and pt == pg["player_total"] and bt == pg["banker_total"])
check("baccarat, current page: rebuild = BC's code (shoe, hands, totals)", same == N, "%d / %d seed sets" % (same, N))

# the simulator, on the server seed of every stored run plus 17 more, at nonces 0..4, five nonces at a random point
# below 100,000,000 and the last five a 100M-deal run uses
vpsim = path("build", "vpsim")
servers = []
for cmd in sorted(glob.glob(path("results", "video-poker", "*", "run-*", "command.txt"))):
    m = re.search(r"VP_SERVER=(\S+)", open(cmd).read())
    servers.append(m.group(1) if m else "pf-audit-server-seed-2026-11-05")   # the simulator's default seed
servers = sorted(set(servers)) + ["parity-%d" % k for k in range(17)]
rng = random.Random("pf-parity-nonces")
for env, variant, label in [({}, "verifier_2021", "current page"), ({"VP_HASH": "plain2019"}, "verifier_2020", "Apr 2020 page"),
                            ({"VP_HASH": "plain2019", "VP_DECK": "suit"}, "verifier_2019", "Nov 2019 page")]:
    lines = []
    for server in servers:
        for n0 in (0, rng.randrange(5, 99999990), 99999995):
            with tempfile.TemporaryDirectory() as tmp:
                out = subprocess.run([vpsim, "0", "1", tmp], env=dict(os.environ, VP_SERVER=server, VP_NONCE0=str(n0), **env),
                                     capture_output=True, text=True, check=True).stdout
            lines += [l.split("\t") for l in out.splitlines() if l.count("\t") == 3]
    page = bc_videopoker_page(VP_PAGES[variant], [(s, c, n) for s, c, n, _ in lines])
    ok = sum([int(x) for x in cards.split(",")] == ten for (s, c, n, cards), (_, ten) in zip(lines, page))
    check("simulator, %s mode: deals = BC's code" % label, ok == len(lines) == len(page) == 15 * len(servers),
          "%d / %d deals, %d server seeds, nonces up to 99,999,999" % (ok, len(lines), len(servers)))
finish()
