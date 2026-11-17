# Video poker, 16 Nov 2026: 62 hands

Played on bc.game (VideoPoker98) at 0.1 USDT a hand on two seed pairs we set: 32 hands with the AI-Hint off,
covering every hold pattern, then 30 hands following the AI-Hint.

| file | what it is |
|---|---|
| `bet-records.json` | BC's own record of each hand: seeds, nonce, the ten cards, the hold, the final hand, stake and credit |
| `game-frames.json` | the socket frames of the game page, raw (base64), and the decoded list the capture script saved in the browser: the paytable the server sent, the seed hashes, every bet and deal, the balance pushes |
| `screenshots/` | BC's verifier page opened on six of the hands (first, tenth and last of each seed pair) |

The account id and nickname are replaced by REDACTED. Every other frame of the game is kept; frame numbers and times
are unchanged.

`make check` (checks/check_video_poker_session.py) decodes the raw frames again (checks/frames.py) and checks the result
equals the saved decoded list. From that decode and these records it checks every bet and deal answer against BC's
record of the hand (cards, held cards, stake, credit), BC's balance pushes, the seed commitments, and BC's own verifier
code on every hand. It then writes `results/live-sessions/video-poker-hands.csv` with a link that opens BC's verifier on
each hand.

Each hand is public on BC's own site at `https://bc.game/game-detail/<bet id>` (the `distributeId` in the records),
with the cards, seeds and payout BC recorded. On 17 Nov 2026 BC's public records of all 62 hands and 150 rounds
matched these records (`results/live-sessions/bc-public-records-check.txt`).
