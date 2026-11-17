# BC.Game Video Poker and Baccarat: evidence package

ProvablyFair.org, November 2026. The evidence behind our investigation of BC.Game's Video Poker and Baccarat, and the
code to check every number.

## The finding

BC.Game advertises its Video Poker at **98% RTP**, a 2% house edge. The dealing method in BC's own verifier, which the
live game follows, returns **96.40%** under the optimal fair-deck strategy for the paytable BC's server sends: a
**3.60% house edge**, 1.8 times the advertised one. That is about **$16 of additional expected loss per $1,000
wagered**. (Optimal fair-deck strategy: the best of the 32 holds for each dealt hand, worked out exactly for a fairly
shuffled deck. It is the strategy a video poker trainer teaches.)

- **The live game deals exactly what BC's verifier deals.** We played 62 hands on bc.game on 16 Nov 2026. BC's own
  verifier code reproduces all ten cards of every hand, replacements come in order from card 6, every payout follows
  the paytable BC's server sent, and BC committed to each server seed before the first hand on it. Every hand is public
  on BC's own site, with its cards and seeds, and the raw game frames here carry the same cards, stakes and credits.
- **Why.** BC's verifier sorts the 52 cards by keys cut from one hash, each shifted one character from the last, so
  two cards that sit next to each other in BC's fixed card list turn up in the same five dealt cards 1.30 times as
  often as on a fairly shuffled deck. In BC's list no two neighbours share a suit or a rank, so dealt hands come out
  weaker: fewer high pairs, two pairs, trips, flushes and full houses. 1.12 of the 1.62 points are lost
  on the first five cards.
- **The current card list appears in BC's verifier commit dated 8 April 2020**, and BC's game sends its video poker games
  to that verifier. The repository is BC's. Independently, GitHub's own records bound publication of the changed list
  between 10 February and 21 May 2020 (`verifier/github/`). On their paytables it returns about 97.3% for the 99% game, 94.5% for the 96% game
  (paytable as BC's server sends it in November 2026) and 96.40% for the 98% game. Real bets from July 2024 (99% game)
  and November 2026 (98% game) replay on it. The timeline below dates the rest.
- **The original published verifier favoured players.** BC's original verifier listed the cards in suit
  order. On the paytable players' screenshots show in March and April 2020, it returns about 102.6%, and a player's
  round from February 2020 replays on it. The commit dated 8 April 2020 swapped in the current list; on the
  same paytable that returns about 97.3%.
- **BC's own fairness text describes a different method** (HMAC-SHA512 on the suit-ordered deck). It gives the cards
  BC dealt on none of the 62 hands.
- **Baccarat uses the same method.** The bet it hits is Player Pair: 77.14% instead of 80.81% on a fairly
  shuffled shoe, about $37 of additional expected loss per $1,000 wagered on it. The other bets move by less than
  0.6 points, some up, some down. All 150 live rounds matched BC's verifier.

Every number: [`results/summary.md`](results/summary.md).

## Check it yourself

Needs Python 3.8+, Node 18+, a C compiler and OpenSSL (libcrypto; macOS uses its own).

    git clone https://github.com/ProvablyFair-org/bcgame-videopoker
    cd bcgame-videopoker
    make check

A couple of minutes. Each line prints PASS or FAIL:

1. every file against `SHA256SUMS`
2. our code against BC's own verifier code, unedited: 10,000 random seed sets per page, and the simulator on the server
   seed of every stored run, at nonces up to 99,999,999
3. the 62 hands and 150 rounds: the raw game frames decoded again, and every answer in them against BC's records
   (cards, held cards, stakes, credits, balance), seed commitments, payouts, nothing missing
4. the AI-Hint (all 62 hints BC sent were best holds), BC's fairness text and game description, the history records,
   GitHub's records of the verifier repository, and the paytables on BC's game server
5. each paytable's exact return, BC's public records of the 212 bets, and the stored simulations pooled into
   `results/summary.md`

`make oracle` checks the exact hold values every return rests on, independently: for 200 hands (the 62 live ones and
138 random ones), every draw of all 32 holds is counted one by one in Python and must give the exact calculator's
6,400 values. About half an hour of CPU time.

`make online` reads GitHub's records in `verifier/github/` again, from GitHub and GH Archive. It needs internet and Node
18+, and downloads up to about 250 MB.

`make sims` reruns every simulation, 1.9 billion video poker hands and 80 million baccarat rounds, and checks every
BC-deal result comes out identical, line for line, on any machine. The one fair-shuffle control run is checked against
the exact return instead (its random stream depends on the thread count). Under an hour on 8 cores.

Every live hand and round is also on BC's own site. Each row of `results/live-sessions/video-poker-hands.csv` and
`baccarat-rounds.csv` has two links: `bc_bet_slip` opens BC's bet slip (cards, seeds, payout, as BC recorded them), and
`verify_link` opens BC's verifier on the same seeds. On 17 Nov 2026 BC's public records of all 212 bets matched the
records here in every field compared: game, bet time, seeds, selections, cards, stake and payout
(`results/live-sessions/bc-public-records-check.txt`, one line per bet). Paste `checks/compare_with_bc.js` into the
browser console on bc.game to check that yourself.

## What is in here

| folder | what it holds |
|---|---|
| `evidence/claims/` | what BC says: 98% RTP and 2% house edge, the game description, the paytables BC's server sends, BC's fairness text, BC's RNG certificate |
| `evidence/video-poker-2026-11-16/` | the 62 hands: BC's bet records, the game's socket frames, BC's verifier on six of them |
| `evidence/baccarat-2026-11-16/` | the 150 rounds, the same way |
| `evidence/history/` | 2020 paytables, a February 2020 player round, "House Edge 1%" screens, BC's archived game config 2024 to 2025, BC's help article, a July 2024 player bet |
| `verifier/` | BC's verifier pages, their dated versions, BC's code that links them, and GitHub's records of who published them and when |
| `src/` | BC's deal rebuilt in Python, the simulator in C |
| `checks/` | everything `make check` runs |
| `results/` | simulation outputs, every live hand and round with its links to BC's bet slip and verifier, `summary.md` |
| `METHOD.md` | how each number is made |

## Timeline

| date | what happened | evidence |
|---|---|---|
| 14 Nov 2019 | BC publishes its video poker verifier, cards in suit order | `verifier/versions/`, `verifier/github/` |
| 10 Mar and 7 Apr 2020 | players' screenshots show the paytable 800/60/22/9/6/4/3/2/1 in full | `evidence/history/2020-paytable/` |
| by 7 Feb 2020 | a player's round replays on the 2019 verifier, and on no later one | `evidence/history/2020-02-player-round/` |
| 8 Apr 2020 (commit date) | The commit replaces the card list with BC's current order; independently, GitHub's records show the old list still up on 10 Feb 2020 and the new one public by 21 May 2020 | `verifier/versions/`, `verifier/github/` |
| 2021 to 2022 | the game shows "House Edge 1%"; BC's own game code, archived April 2022, says "The house edge is 1%" and lists the paytable 800/60/22/9/6/4/3/2/1 | `evidence/history/1pct-house-edge-2021/`, `verifier/links/` |
| 24 Dec 2021 | the hash changes, the card list stays; this is the file BC links today | `verifier/versions/` |
| 3 Jul 2024 | a player's bet on the 99% game replays on today's verifier | `evidence/history/2024-07-03-player-bet/` |
| Oct 2024 to Feb 2025 | BC's game config: VideoPoker, RTP 0.99 | `evidence/history/rtp-configs-2024-2025/` |
| 11 Feb 2025 | BC's game code sends a VideoPoker96 game to the same verifier page | `verifier/links/` |
| 5 Mar 2025 | BC's game config: VideoPoker96, RTP 0.96 | `evidence/history/rtp-configs-2024-2025/` |
| 2025 | BC's help centre: Originals moved from 99% RTP to 96% | `evidence/history/2025-help-article/` |
| 7 Nov 2026 | BC's game server sends three video poker paytables: 98%, 96%, and the old 99% one, marked deleted | `evidence/claims/game-configs-2026-11-07/` |
| 16 Nov 2026 | the game shows 98% RTP and a 2% house edge; 62 live hands match the verifier | `evidence/claims/`, `evidence/video-poker-2026-11-16/` |

These are dated records, not a continuous log of the live game. They date each version of the published verifier (by
its commits and, independently, by GitHub's own push and fork records), show the paytables and RTP labels BC used, and
three real bets (February 2020, July 2024, November 2026) replay on the version of their time. When each change
reached the live game, and that nothing else ran in between, is inferred from them. The archived 2025 configs carry
the 96% game's RTP label, not its paytable: the 96% figure uses the paytable BC's server sends in November 2026, and
no live hand from that game was captured.

## Privacy

The copies of our bet records and game frames here leave out the account id and nickname; BC's own bet pages show
them. Other players' names, pictures and bet ids are blurred or replaced. One July 2024 client seed is the player's own
text and is kept, because the cards cannot be checked without it.
