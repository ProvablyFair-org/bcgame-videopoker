# Baccarat, 16 Nov 2026: 150 rounds

Played on bc.game (BaccaratSingle98) on two seed pairs we set: each round 0.1 USDT on player or banker and 0.1 USDT
each on tie, player pair and banker pair. 600 bets.

| file | what it is |
|---|---|
| `bet-records.json` | BC's own record of each round: seeds, nonce, bets, both hands, totals, credit |
| `game-frames.json` | the socket frames of the game page, raw (base64): the odds the server sent, the seed hashes, every round, the balance pushes |
| `screenshots/` | BC's verifier page opened on six of the rounds |

The account id and nickname are replaced by REDACTED. Every other frame of the game is kept; frame numbers and times
are unchanged.

`make check` (checks/check_baccarat_session.py) decodes the raw frames (checks/frames.py) and checks every round's bet
request and answer against BC's record of it (bets, cards, totals, stake, credit), BC's balance pushes, the seed
commitments, and BC's own verifier code on every round. It then writes `results/live-sessions/baccarat-rounds.csv` with
a verify link per round.

Each round is public on BC's own site at `https://bc.game/game-detail/<bet id>` (the `distributeId` in the records),
with the cards, seeds and payout BC recorded. On 17 Nov 2026 BC's public records of all 62 hands and 150 rounds
matched these records (`results/live-sessions/bc-public-records-check.txt`).
