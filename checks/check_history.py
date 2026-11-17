#!/usr/bin/env python3
"""The history: which verifier BC published when, which page BC's game links, which paytables and RTP labels BC's
servers carried, and two live rounds from other players that date the deal (evidence/history, verifier/).
"""
import csv
import hashlib
import itertools
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import VP_PAGES, bc_videopoker_page, check, finish, load, path
import bcvp


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def read(*p):
    return open(path(*p), encoding="utf8", errors="replace").read()


print("published verifier versions\n")
rows = list(csv.DictReader(open(path("verifier", "versions", "commits.csv"))))
for r in rows:
    if r["copy_in_this_package"]:
        check("%s %s: file here matches the commit" % (r["date_utc"][:10], r["commit"][:7]), sha(path(r["copy_in_this_package"])) == r["videopoker_html_sha256"])
cur = sha(path("verifier", "videopoker.html"))
check("today's page = the 24 Dec 2021 version, byte for byte", cur == sha(path("verifier", "versions", "2021-12-24_videopoker.html")))
check("the same file in the 24 Dec 2021 commit and in both repositories behind BC's links", all(r["videopoker_html_sha256"] == cur for r in rows if r["date_utc"] >= "2021-12-24"),
      "bc-game-project/verify, bcgame-project/verify, game-verify/public")
same = [("seed-%d" % k, "client-%d" % k, k) for k in range(3)]
p19 = bc_videopoker_page(VP_PAGES["verifier_2019"], same)
p20 = bc_videopoker_page(VP_PAGES["verifier_2020"], same)
check("8 Apr 2020: same hash as 2019, different card list", all(a[0] == b[0] and a[1] != b[1] for a, b in zip(p19, p20)))
check("  2019 list = spade A-K, heart A-K, club A-K, diamond A-K; 2020 list = BC's own order",
      all(a[1] == bcvp.deal("verifier_2019", *s)[1][:10] and b[1] == bcvp.deal("verifier_2020", *s)[1][:10] for s, a, b in zip(same, p19, p20)))
L = bcvp.SCRAMBLED
adj = [(L[i], L[i + 1]) for i in range(51)]
check("  in BC's list no two neighbouring cards share a suit or a rank",
      all(a // 16 != b // 16 and a % 16 != b % 16 for a, b in adj), "51 neighbouring pairs")

print("\nwho publishes that history, and when the card list changed: GitHub's own records (verifier/github/)\n")
gh = load("verifier", "github", "receipt.json")
rp, ow, lk, ev = gh["repository"], gh["owner"], gh["bc_forum_github_link"], gh["push_events"]
hist = {r["commit"]: r for r in rows if r["repository"] == "https://github.com/" + rp["name"]}
v19 = hist["385651dc485d00b44aed498899bfff4f5b39db36"]
v20 = hist["cb2be877a5d52bd347558af80edd3c0a5086321a"]
v21 = hist["1e64d725658a0e2d00d57a45d9006499cd348eb9"]


def secs(a, b):
    from datetime import datetime
    f = "%Y-%m-%dT%H:%M:%SZ"
    return (datetime.strptime(a, f) - datetime.strptime(b, f)).total_seconds()


check("the history above is one GitHub repository, %d: %s in GitHub's 2019 and 2020 records, %s now" % (rp["id"], rp["name_in_2019_2020_events"], rp["name"]),
      len(hist) == 4 and all(r["repository"].endswith("/" + rp["name"]) for r in hist.values()))
foot = read("verifier", "github", "bc-forum-footer_archive.ph-mAgrj.txt")
check("BC's forum footer links its GitHub as %s; GitHub serves that from account %d, which owns the verifier" % (lk["url"], ow["id"]),
      "https://forum.bc.game/" in foot and "/" + lk["url"] in foot and lk["owner_id"] == ow["id"], "archive.ph/mAgrj")
d0 = secs(ev[0]["created_at"], v19["date_utc"])
check("14 Nov 2019: GitHub logged the push of the suit-order page %d s after its commit" % d0,
      ev[0]["head"] == v19["commit"] and ev[0]["head_commit_date"] == v19["date_utc"] and 0 <= d0 <= 60)
cas, sak, ibt = sorted(gh["forks"], key=lambda f: f["created_at"])
check("10 Feb 2020: a logged push still carries the suit-order page, as does a fork made 8 Feb 2020",
      v19["date_utc"] < ev[1]["head_commit_date"] < v20["date_utc"] and cas["videopoker_html_sha256"] == v19["videopoker_html_sha256"]
      and cas["created_at"] < v20["date_utc"], "no change to the page between the two commits in commits.csv")
check("21 May 2020: a logged push came after the 8 Apr 2020 card-list commit, so the new list was public by then; a fork made 10 Jun 2020 has it",
      ev[2]["before"] == v20["commit"] and sak["videopoker_html_sha256"] == v20["videopoker_html_sha256"])
check("  22 Dec 2021: a fork has the 21 Dec 2021 page", ibt["videopoker_html_sha256"] == v21["videopoker_html_sha256"] and ibt["head"] == v21["commit"])
delays = [secs(e["created_at"], e["head_commit_date"]) for e in ev]
check("every push GitHub logged came within a minute of its commit", all(0 <= d <= 60 for d in delays),
      ", ".join("%d s" % d for d in delays))

print("\nwhere BC's game sends players to verify\n")
g = read("verifier", "links", "2026-11-05_bc.game_games-DEcz4odY.js")
check("bc.game client code, 5 Nov 2026: VideoPoker98 -> game-verify.github.io/public/videopoker.html",
      'const Y="https://game-verify.github.io/public"' in g and re.search(r'id:"VideoPoker98",validateLink:`\$\{Y\}/videopoker\.html`', g) is not None)
check("bc.game client code, 5 Nov 2026: BaccaratSingle98 -> game-verify.github.io/public/baccaratsingle.html",
      re.search(r'id:"BaccaratSingle98",validateLink:`\$\{Y\}/baccaratsingle\.html`', g) is not None)
ix = read("verifier", "links", "2026-11-05_bc.game_index-CmEYgXxK.js")
check("bc.game client code builds the link ?s=server seed&c=client seed&n=nonce&he=house edge&m=mode",
      "?s=${i.serverSeed}&c=${i.clientSeed}&n=${t.betLog.nonce}&he=${r}&m=${n}" in ix)
a22 = read("verifier", "links", "2022-04-23_arquivo_bc.game_index.66fd1f62.js")
check("bc.game client code archived 23 Apr 2022: video poker -> bcgame-project.github.io/verify/videopoker.html",
      'name:"VideoPoker",namespace:"/g/vp"' in a22 and 'validateLink:"https://bcgame-project.github.io/verify/videopoker.html"' in a22)
check("  the same archived code: paytable 800/60/22/9/6/4/3/2/1 and \"The house edge is 1%.\"",
      'pokerPayouts",[0,1,2,3,4,6,9,22,60,800]' in a22 and "The house edge is 1%." in a22)
a25 = read("verifier", "links", "2025-02-11_arquivo_bc.game_config-225813cf.js")
check("bc.game client code archived 11 Feb 2025: VideoPoker96 -> bcgame-project.github.io/verify/videopoker.html",
      'id:"VideoPoker96",key:"video-poker",name:"VideoPoker",namespace:"/g/vp/96",validateLink:"https://bcgame-project.github.io/verify/videopoker.html"' in a25)

print("\npaytables and RTP labels on BC's game server, 7 Nov 2026 (decoded with BC's own client code)\n")
src = path("evidence", "claims", "game-configs-2026-11-07")
with tempfile.TemporaryDirectory() as tmp:
    shutil.copytree(src, os.path.join(tmp, "c"))
    subprocess.run(["node", "verify_socket_original_schema.cjs"], cwd=os.path.join(tmp, "c"), capture_output=True, check=True)
    fresh = json.load(open(os.path.join(tmp, "c", "socket_original_schema_verification.json")))["results"]
stored = json.load(open(os.path.join(src, "socket_original_schema_verification.json")))["results"]
check("decoding the raw frames again gives the stored result", fresh == stored)
for r in fresh:
    for gc in r["gameConfig"]:
        if gc["gameName"] in ("VideoPoker", "VideoPoker96", "VideoPoker98"):
            print("      %-13s %-11s rtp %s  paytable %s" % (gc["gameName"], gc["namespace"], gc["rtp"], "/".join(map(str, gc["orderedPaytable"]))))

print("\nRTP label of bc.game's video poker in independently archived copies of BC's game config (arquivo.pt)\n")
for fn in sorted(os.listdir(path("evidence", "history", "rtp-configs-2024-2025"))):
    if fn.endswith("config.json"):
        s = read("evidence", "history", "rtp-configs-2024-2025", fn)
        vp = [json.loads(m.group(0)) for m in re.finditer(r'\{[^{}]*"gameName": "VideoPoker[0-9]*"[^{}]*\}', json.dumps(json.loads(s)))]
        print("      %s  %s" % (fn[:10], ", ".join("%s %s rtp %s" % (v["gameName"], v["gameSocketNameSpace"], v["rtp"]) for v in vp)))

print("\nFebruary 2020: a player's round posted on BC's forum\n")
rd = load("evidence", "history", "2020-02-player-round", "round.json")
vis, hvis = rd["server_seed_visible"], rd["server_seed_hash_visible"]
hits = [vis + "".join(t) for t in itertools.product("0123456789abcdef", repeat=rd["server_seed_hidden_characters"])
        if hashlib.sha256((vis + "".join(t)).encode()).hexdigest().startswith(hvis)]
check("of the 1,048,576 ways to fill the 5 hidden characters, one fits the shown hash", len(hits) == 1, hits[0] if hits else "")
server = hits[0]
pages = bc_videopoker_page(VP_PAGES["verifier_2019"], [(server, c, rd["nonce"]) for c in rd["client_seed_readings"]])
fit = [c for c, (_, ten) in zip(rd["client_seed_readings"], pages) if ten[:5] == rd["initial_hand_codes"]]
check("of the 36 readings of the client seed, one gives the dealt hand on the Nov 2019 page", len(fit) == 1, fit[0] if fit else "")
ten = bc_videopoker_page(VP_PAGES["verifier_2019"], [(server, fit[0], rd["nonce"])])[0][1]
final = bcvp.draw_sequential(ten[:5], {c for i, c in enumerate(ten[:5]) if i not in rd["replaced_positions"]}, ten)
check("  the three replacement cards then match too, in order (checked separately)", final == rd["player_hand_codes"], " ".join(bcvp.txt(c) for c in final))
later = [bc_videopoker_page(VP_PAGES[v], [(server, fit[0], rd["nonce"])])[0][1][:5] for v in ("verifier_2020", "verifier_2021")]
check("  the April 2020 and current pages do not give this hand", all(x != rd["initial_hand_codes"] for x in later))

print("\n3 July 2024: a player's bet, as BC's share API returns it\n")
bet = load("evidence", "history", "2024-07-03-player-bet", "bc-share-record.json")["data"]["gameData"]
bl, sh = bet["betLog"], bet["seedHistory"]
check("SHA256(server seed) = the hash BC recorded", hashlib.sha256(sh["serverSeed"].encode()).hexdigest() == sh["serverSeedHash"])
t24 = bc_videopoker_page(VP_PAGES["verifier_2021"], [(sh["serverSeed"], sh["clientSeed"], bl["nonce"])])[0][1]
check("today's page gives the ten cards BC recorded", t24 == bl["gv"]["initialHard"], " ".join(bcvp.txt(c) for c in t24))
f24 = bcvp.draw_sequential(t24[:5], set(bl["gv"]["holdHard"]), t24)
check("  final hand by the in-order rule = BC's record: %s, paid %sx" % (bcvp.CLASS_NAMES[bcvp.classify(f24)], bl["oddsString"]),
      f24 == bl["gv"]["playerHard"] and bcvp.PAYTABLES["99"][bcvp.classify(f24)] == float(bl["oddsString"]))
finish()
