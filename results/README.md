# Results

`summary.md` has every number the article quotes; `checks/summarize.py` writes it from the files below.

| folder | what it holds |
|---|---|
| `video-poker/<paytable>_<verifier>/run-N/` | one simulation of 100,000,000 deals each: `command.txt` (how to rerun it) and `run.txt` (the simulator's full output: return, standard error, dealt-hand counts, neighbour effect) |
| `video-poker/exact-returns.txt` | each paytable's exact return on a fairly shuffled deck |
| `baccarat/returns.txt`, `returns.json` | baccarat outcome probabilities and per-bet returns: fair shoe, BC's deal, control |
| `live-sessions/` | one row per live hand and round, with links to BC's own bet slip and BC's verifier for it; `bc-public-records-check.txt`: BC's public records of all 212 bets against the ones here, one line per bet |

`make sims` reruns every simulation and checks the new output against these files.
