# Method

## 1. BC's deal

Every version of BC's published video poker verifier deals the same way. A hash is made from the server seed, the client seed
and the nonce. Card j of a fixed list of 52 cards gets that hash, rotated left by j characters, as its key. The cards
are sorted by key, as plain text, smallest first. The first five are dealt; replaced cards come from card 6 on, in order.

| version | hash | card list |
|---|---|---|
| 14 Nov 2019 | SHA512(server seed + client seed + nonce) | suit order: spade A to K, heart A to K, club A to K, diamond A to K |
| 8 Apr 2020 | SHA512(server seed + client seed + nonce) | BC's own order (src/bcvp.py, `SCRAMBLED`) |
| 24 Dec 2021, current | SHA512(hex(HMAC_SHA256(server seed, client seed:nonce))) | BC's own order |

Baccarat (verifier/baccaratsingle.html) uses the same idea with two decks: HMAC_SHA256 gives a hex string h; SHA256(h)
keys the first 52 cards by rotation, SHA256 of that keys the second 52; all 104 sorted. Player gets cards 1 and 3,
banker 2 and 4, third cards follow the standard drawing rules.

**Why it is not a fair shuffle.** The 52 keys are rotations of one string, so a card's key and its neighbour's key
share almost all their characters. Cards next to each other in the list therefore tend to sort close together, and to
be dealt in the same hand. Across 600 million deals, two list neighbours turned up in the same five dealt cards 1.30
times as often as on a fairly shuffled deck (anywhere in the hand, not necessarily side by side). In BC's list no two neighbours share a suit or a rank, so the dealt hands carry
fewer pairs, flushes and full houses. In the 2019 list neighbours share a suit, which pushed the other way.

**Our code is BC's code.** `checks/parity.py` runs BC's own page code, unedited, in node and compares it with our
rebuild (src/bcvp.py, src/bcbac.py) on 10,000 random seed sets per page, and with the simulator (src/vpsim.c).

## 2. The live sessions

On 16 Nov 2026 we played 62 video poker hands and 150 baccarat rounds on bc.game with our own account and our own
client seeds. For every hand and round: BC's own verifier code, run on the seeds BC revealed, gives exactly the cards
in BC's own record; each server seed hashes to the hash BC sent before the first hand on it; each credit follows the
paytable or odds the server sent; BC's own count of hands per seed pair equals the hands here, so none is missing.
On the 51 video poker hands where the hold could tell the order apart, the replacements came from card 6 on, in order.

The raw socket frames of both sessions are in the package. `checks/frames.py` decodes them from the bytes (socket.io
binary packets with protobuf bodies), and the session checks work from that decode: every bet and deal answer carries
the cards, held cards, stake and credit of BC's record of the hand; BC's balance pushes debit every stake and pay
every credit, and the balance moves by exactly those amounts; each revealed server seed matches the hash BC sent
before the first hand on it (the frames also record when that hash was requested and received, and when our client
seed went out). For video poker the decode also equals the decoded list the capture script saved in the browser.

## 3. Returns

**Exact, fair deck.** src/vpsim.c enumerates all 2,598,960 deals and all 32 holds per paytable and picks the best hold
for each deal (the optimal fair-deck strategy). Check: the textbook 9/6 Jacks or Better table comes out at 99.5439%.

**BC's deal, simulated.** src/vpsim.c deals 100,000,000 hands per run with BC's verifier code (in C, matched to BC's
page by `checks/parity.py`), plays the optimal fair-deck hold for the paytable, and takes the replacements in order from
card 6. Each configuration has 3 to 6 runs on different server seeds; the result is their mean, with a 95% interval of
1.96 standard errors. The BC deal is seeded by deal number, so `make sims` reproduces every BC-deal output line for
line, on any machine and any thread count. One run also has a control arm (the same code with a fair shuffle); it
agrees with the exact value within its error. Its random stream is seeded per thread, so `make sims` checks it against
the exact return rather than line for line.

**Deal only.** The same runs also score each dealt hand at its best hold with fair replacements. The gap between this
and the exact return is what the dealt five cards alone cost.

**Baccarat.** src/baccarat_sim.py: exact outcome probabilities for a fairly shuffled 2-deck shoe, 40,000,000 rounds of
BC's deal, and 40,000,000 rounds of a fair shuffle through the same counting code as a control. Returns use the odds
BC's server sent, including the 0.9908 a tie pays on player and banker bets.

**The AI-Hint.** BC sent a hint with every hand, whether or not it was switched on. checks/check_hint.py computes the
exact value of all 32 holds for each live hand (fair deck, server paytable) and checks the hint is a best hold. All 62
hints BC sent were best holds.

## 4. What the evidence shows, and what it points to

Shown: BC's published verifier code and its dated versions; that the repository holding those versions is BC's, and,
from GitHub's own push and fork records, that the card list changed between 10 Feb and 21 May 2020 (the commit is
dated 8 Apr 2020); that BC's game links that code; that the live game dealt 62 of 62 hands and 150 of 150 rounds
exactly as that code deals them; the paytables and RTP labels BC displayed, coded and served; player rounds from
February 2020 and July 2024 that replay on the 2019 and current versions; the returns of each paytable on BC's deal.

Inferred from the dated records, not shown: when each change reached the live game, and that the deal stayed the same
between the records. The 96% game is linked to the same verifier in BC's code, but no live hand from it was captured,
and its figure uses the paytable BC's server sends in November 2026 (the archived 2025 configs give its RTP label,
not its paytable).

All returns are for the optimal fair-deck strategy for each paytable: the best of the 32 holds for each dealt hand,
worked out exactly for a fairly shuffled deck. It is the play BC's own AI-Hint suggested on every live hand.
