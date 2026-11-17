# Results

Numbers in percent. Every return is for the optimal fair-deck strategy for the paytable: the best of the 32 holds for each dealt hand, worked out exactly for a fairly shuffled deck. Written by `checks/summarize.py`.

## Video poker

Each row is a paytable played on one version of BC's published verifier. When each version ran on bc.game is in the README's timeline.

| paytable and verifier | return on a fairly shuffled deck | return on BC's deal (95% interval) | against the paytable | runs | additional expected loss per $1,000 wagered, vs advertised |
|---|---|---|---|---|---|
| 98% game (VideoPoker98, live): its paytable, current verifier | 98.02 | **96.40** (96.37 to 96.44) | 1.62 points below | 6 x 100M | $16 |
| 96% game (VideoPoker96): paytable as BC's server sends it in Nov 2026, current verifier | 95.98 | **94.46** (94.41 to 94.51) | 1.51 points below | 3 x 100M | $15 |
| 99% game (VideoPoker): its paytable, current verifier (hash of 24 Dec 2021) | 98.94 | **97.29** (97.24 to 97.34) | 1.65 points below | 3 x 100M | $17 |
| 99% game (VideoPoker): its paytable, verifier of 8 Apr 2020 (earlier hash) | 98.94 | **97.30** (97.25 to 97.35) | 1.65 points below | 3 x 100M | $17 |
| 99% paytable, original verifier of 14 Nov 2019 (suit-ordered list) | 98.94 | **102.59** (102.53 to 102.66) | 3.65 points above | 3 x 100M | players had the edge |

98% game, 600,000,000 hands: house edge **3.60%** against the advertised 2% (1.8x). Of the 1.62 points lost against the paytable, 1.12 are lost on the five dealt cards alone (best hold, fair replacements).

### Dealt hands, 98% game, the same 600,000,000 deals: BC's deal against a fairly shuffled deck

The five cards dealt before any hold, not the final hands. Expected = deals x exact share of the 2,598,960 hands.

| dealt hand | on BC's deal | expected on a fair deck | change (95% interval) |
|---|---|---|---|
| nothing/low pair | 477,960,025 | 476,235,109.4 | +0.36% (+0.36 to +0.37) |
| jacks or better | 77,508,142 | 78,012,743.6 | -0.65% (-0.67 to -0.63) |
| two pair | 28,009,577 | 28,523,409.4 | -1.80% (-1.84 to -1.77) |
| three of a kind | 12,221,726 | 12,677,070.8 | -3.59% (-3.65 to -3.54) |
| straight | 2,301,699 | 2,354,788.1 | -2.25% (-2.38 to -2.13) |
| flush | 1,025,377 | 1,179,240.9 | -13.05% (-13.22 to -12.88) |
| full house | 832,141 | 864,345.7 | -3.73% (-3.93 to -3.52) |
| four of a kind | 133,383 | 144,057.6 | -7.41% (-7.91 to -6.91) |
| straight flush | 7,183 | 8,311.0 | -13.57% (-15.55 to -11.55) |
| royal flush | 747 | 923.4 | -19.11% (-24.70 to -13.09) |

Why: two cards that sit next to each other in BC's 52-card list turn up in the same five dealt cards 1.30 times as often as on a fairly shuffled deck (anywhere in the hand, not side by side), and in BC's list no two neighbours share a suit or a rank.

Control (run 1): the same program with a fair shuffle returns 98.023% (SE 0.044), within its error of the exact 98.019%.

## Baccarat

40,000,000 rounds of BC's deal, returns at the server's odds, against the exact return of a fairly shuffled 2-deck shoe.

| bet | pays | fairly shuffled shoe | on BC's deal (95% interval) | change, points |
|---|---|---|---|---|
| player | 1.9817 | 97.84 | 98.13 (98.10 to 98.16) | +0.29 |
| banker | 1.9322 | 98.06 | 97.77 (97.74 to 97.80) | -0.29 |
| tie | 8.918 | 84.20 | 84.03 (83.95 to 84.11) | -0.17 |
| player pair | 11.8907 | 80.81 | 77.14 (77.04 to 77.23) | -3.68 |
| banker pair | 11.8907 | 80.81 | 81.38 (81.29 to 81.47) | +0.57 |

Player pair: about $37 of additional expected loss per $1,000 wagered on it, against a fairly shuffled shoe. Control (a fair shuffle through the same counting code): PASS.
