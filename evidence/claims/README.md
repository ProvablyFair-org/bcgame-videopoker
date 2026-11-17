# What BC says

| file | what BC says | source |
|---|---|---|
| `2026-11-05_game-page_98-rtp_2-house-edge.jpg` | Video Poker: RTP 98%, house edge 2.00% | https://bc.game/game/video-poker, screenshot 5 Nov 2026 |
| `2026-11-16_archive.ph-68l0J_98-rtp.jpg` | the same, in an independent archive | https://archive.ph/68l0J, 16 Nov 2026 |
| `2026-11-05_bc-api_game-detail_video-poker.json` | `rtpDes: 98` for VideoPoker98 | https://bc.game/api/game/home/detail/?gameUrl=video-poker&areaCode= |
| `2026-11-15_bc-api_game-detail_baccarat.json` | `rtpDes: 98` for BaccaratSingle98 | https://bc.game/api/game/home/detail/?gameUrl=baccarat&areaCode= |
| `2026-11_paytable-signed-in.png` | the paytable a signed-in player sees: 800/80/22/8/6/4/3/2/1 | bc.game, screenshot, signed in |
| `2026-11-05_paytable-signed-out.jpg` | signed out, the page shows a default table with a 60x straight flush | bc.game, screenshot, signed out |
| `2026-11-05_bc.game_index--9V6N-Vk.js` | that default table in BC's client code: `fallbackPayouts` = 800/60/22/8/6/4/3/2/1 | https://bc.game/modules/games/assets/index--9V6N-Vk.js |
| `game-configs-2026-11-07/` | the three video poker paytables and RTP labels on BC's game server (below) | socketv4.bc.game, 7 Nov 2026 |
| `2026-11-05_bc-fairness-text_videopoker-B-dyWROu.js` | BC's in-game "provably fair" text for video poker | https://bc.game/modules/games/assets/videopoker-B-dyWROu.js |
| `2026-11-16_game-page_description.txt` | the game page's description: "played with a single, fresh 52-card deck per round", and the AI Hint "highlights the mathematically optimal cards to keep" | https://bc.game/game/video-poker, page text 16 Nov 2026; the same text is in https://archive.ph/68l0J |
| `rng-certificate/` | BC's latest public RNG certificate (iTech Labs, 12 Oct 2020) and BC's trust page | itechlabs.com, bcgame.com/trust, 7 Nov 2026 |

## The paytable that pays

Signed out, the game page shows a default table from BC's client code (straight flush 60x). Signed in, BC's server
sends the game's own table, and that is the one that pays: straight flush 80x. In the session of 16 Nov 2026 the server
sent 800/80/22/8/6/4/3/2/1 (game frames 283 and 648) and every credit followed it. All results for the 98% game use it.

## game-configs-2026-11-07/

Raw answers of BC's game server to the first request a game page makes (`init`), for each video poker route, and
the decoder: BC's own client code (`source_dependencies/`), run by `verify_socket_original_schema.cjs`. No account,
no bets. Decoded:

| game | route | RTP label | paytable, royal flush to jacks or better |
|---|---|---|---|
| VideoPoker98 | /g/vp/98 | 0.98 | 800/80/22/8/6/4/3/2/1 |
| VideoPoker96 | /g/vp/96 | 0.96 | 800/80/18/8/5/4/3/2/1 |
| VideoPoker | /g/vp/main | 0.99 | 800/60/22/9/6/4/3/2/1 (marked deleted, still served) |

## The game description

The Description tab of the game page, as page text (headings, paragraphs and lists, in the order the page shows them),
saved on 16 Nov 2026 while signed out. The file holds that tab only, from its first heading to "Final Verdict"; the rest
of the page (the bet panel, the win lists with other players' names, the game list) is left out. The archive.today
copy of the same page, https://archive.ph/68l0J (16 Nov 2026 18:11 UTC), carries the same text. Two lines matter here:

- "[GAMENAME] is a digital adaptation of the timeless standard five-card draw poker, played with a single, fresh 52-card
  deck per round." The deal is not a fresh shuffle of the deck: it sorts the cards by related keys (METHOD.md).
- The AI Hint "highlights the mathematically optimal cards to keep based on perfect video poker strategy." That is the
  optimal fair-deck strategy every return in this package uses; all 62 hints BC sent were best holds
  (checks/check_hint.py).

## The fairness text

BC's text says the hash is HMAC_SHA512(clientSeed:nonce, serverSeed) and the deck is spade A to K, heart A to K, club A
to K, diamond A to K. That is not what the game deals: on the 62 live hands the text's method gives the cards BC dealt
on none (checks/check_fairness_text.py). The suit-ordered deck it describes is the one BC's published verifier used
before April 2020.

## The certificate

The October 2020 certificate covers BC's random number generator and card shuffling for named games. Video poker is
not named, and no paytable, RTP or code fingerprint is printed. BC's trust page calls it the latest public certificate.
