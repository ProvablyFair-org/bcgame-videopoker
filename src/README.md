# Code

| file | what it does |
|---|---|
| `bcvp.py` | BC's video poker deal, every version (Nov 2019, Apr 2020, current, and the method in BC's fairness text), the in-order replacement rule and a Jacks or Better hand classifier |
| `bcbac.py` | BC's baccarat deal and drawing rules |
| `vpsim.c` | exact return of a paytable on a fairly shuffled deck (all 2,598,960 deals x 32 holds), and simulation of the optimal fair-deck strategy on BC's deal, in C for speed. Options by environment: `PAYTABLE`, `VP_DECK=suit`, `VP_HASH=plain2019`, `VP_SERVER`, `VP_ARMS` (header of the file) |
| `baccarat_sim.py` | baccarat: exact outcome probabilities for a fair shoe, BC's deal simulated, a fair-shuffle control, returns at the server's odds |

`checks/parity.py` shows each of these deals exactly what BC's own page code deals.
