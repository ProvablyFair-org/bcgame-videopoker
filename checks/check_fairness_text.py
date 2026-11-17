#!/usr/bin/env python3
"""BC's in-game fairness text for video poker (evidence/claims/2026-11-05_bc-fairness-text_videopoker-B-dyWROu.js) says:
    hash = HMAC_SHA512(clientSeed:nonce, serverSeed); the deck is spade A-K, heart A-K, club A-K, diamond A-K;
    card j gets the hash rotated left j characters as its weight; cards sorted by weight, small to large.
This runs that method on the seeds of the 62 live hands: with BC's own 2019 page code (the one with that deck) and the
text's hash, and with our rebuild. Neither gives the cards BC dealt on any hand. The live game deals with the verifier.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import VP_PAGES, bc_videopoker_page, check, finish, load
import bcvp

text = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "evidence", "claims",
                         "2026-11-05_bc-fairness-text_videopoker-B-dyWROu.js"), encoding="utf8").read()
text = " ".join(text.split())
check("BC's fairness text names HMAC_SHA512 and the suit-ordered deck",
      "HMAC_SHA512(clientSeed:nonce, serverSeed)" in text and "spade A-K, heart A-K, club A-K and diamond A-K" in text)
desc = " ".join(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "evidence", "claims",
                                  "2026-11-16_game-page_description.txt"), encoding="utf8").read().split())
check("BC's game page says the game uses a single, fresh 52-card deck per round",
      "played with a single, fresh 52-card deck per round" in desc, "evidence/claims/2026-11-16_game-page_description.txt")
recs = [r["data"] for r in load("evidence", "video-poker-2026-11-16", "bet-records.json")]
rows = [(r["seedHistory"]["serverSeed"], r["seedHistory"]["clientSeed"], r["betLog"]["nonce"]) for r in recs]
page = bc_videopoker_page(VP_PAGES["verifier_2019"], rows, mode="hmac512")
same_code = sum(bcvp.deal("fairness_text", *row)[1][:10] == ten for row, (_, ten) in zip(rows, page))
check("our rebuild of the text's method = BC's page code with the text's hash", same_code == len(rows), "%d / %d" % (same_code, len(rows)))
match10 = sum(ten == r["betLog"]["gv"]["initialHard"] for r, (_, ten) in zip(recs, page))
match5 = sum(ten[:5] == r["betLog"]["gv"]["initialHard"][:5] for r, (_, ten) in zip(recs, page))
check("the text's method gives the cards BC dealt on no hand", match10 == 0 and match5 == 0,
      "ten cards equal on %d of %d hands, dealt five on %d" % (match10, len(recs), match5))
finish()
