# History

Dated records from public sources, each with its file here and its original location. Other players' names, pictures
and bet ids are blurred or replaced. `make check` (checks/check_history.py) replays both rounds and reads the configs.

| date | what it shows | file | source |
|---|---|---|---|
| 10 Mar 2020 | the paytable 800/60/22/9/6/4/3/2/1, in full, in a player's screenshot | `2020-paytable/2020-03-10_forum-post-3602.jpg` | [forum.bc.game post 3602](https://forum.bc.game/topic/536-%F0%9F%98%8D/#findComment-3602) |
| 7 Apr 2020 | the same paytable, in full, in two players' screenshots, the day before the card list changed | `2020-paytable/2020-04-07_forum-post-4644.png`, `-4648.png` | forum.bc.game [post 4644](https://forum.bc.game/topic/695-straight-flush/#findComment-4644), [post 4648](https://forum.bc.game/topic/696-my-xlm-lucky-day/#findComment-4648) |
| by 7 Feb 2020 | a player's round, with seeds, replays on the November 2019 verifier and on no later one | `2020-02-player-round/` | [forum.bc.game post 2339](https://forum.bc.game/topic/415-royal-flush/#findComment-2339), [archive](https://archive.ph/mAgrj) |
| 24 Jul 2021 | the game screen shows "House Edge 1%" | `1pct-house-edge-2021/2021-07-24_forum-post-33779.png` | [forum.bc.game post 33779](https://forum.bc.game/topic/6036-straight-flush-in-video-poker/#findComment-33779), [archive](https://archive.ph/VDjp0) |
| 15 Dec 2021 | BC's own video poker event graphic lists all nine payouts: 800/60/22/9/6/4/3/2/1 | `1pct-house-edge-2021/2021-12-15_bc-event-graphic_paytable.jpeg` | [forum.bc.game topic 7282](https://forum.bc.game/topic/7282-1000-prestige-video-poker-challenge-9/), [archive](https://archive.ph/u5NNA) |
| Dec 2021 | the game screen shows "House Edge 1%" | `1pct-house-edge-2021/2021-12_forum-upload_archive.ph.jpg` | [archive of the forum upload](https://archive.ph/Dq5S8) |
| 23 Apr 2022 | BC's own video poker code: paytable 800/60/22/9/6/4/3/2/1, "The house edge is 1%." | `../../verifier/links/2022-04-23_arquivo_bc.game_index.66fd1f62.js` | [arquivo.pt copy of bc.game's code](https://arquivo.pt/noFrame/replay/20220423025739id_/https://bc.game/assets/index.66fd1f62.js) |
| 2021 to 2022 | BC's blog: video poker RTP around 99%, house edge 1% | `1pct-house-edge-2021/blog.bc.game_best-odds-in-casino-games.html` | [blog.bc.game](https://blog.bc.game/best-odds-in-casino-games/) (published 3 Apr 2021, modified 22 Nov 2022) |
| 3 Jul 2024 | a player's bet (four of a kind, 22x), seeds revealed, replays on today's verifier | `2024-07-03-player-bet/` | [BC's share API](https://bc.game/api/game/support/share-v3/info/detail/1228WDV7FXKRSZ/), posted on [forum.bc.game](https://forum.bc.game/topic/15992-forum-daily-challenges-650/#findComment-121955) |
| 16 Oct 2024, 10 Dec 2024, 11 Feb 2025 | BC's game config: `VideoPoker`, route /g/vp/main, rtp 0.99 | `rtp-configs-2024-2025/` | arquivo.pt copies of https://bc.game/cache/game/support/system/conf/ |
| 5 Mar 2025 | BC's game config: `VideoPoker96`, route /g/vp/96, rtp 0.96 | `rtp-configs-2024-2025/2025-03-05_arquivo_bc-game-config.json` | arquivo.pt, same address |
| 2025 | BC's help centre: Originals changed from 99% RTP (1% house edge) to 96% (4%) | `2025-help-article/` | [help.bc.support](https://help.bc.support/en/articles/10714803-house-edge-rtp-how-it-functions) (updated 26 Nov 2025), [archive](https://archive.ph/IxGB4) |

## The February 2020 round

The screenshot shows the server seed with its last 5 characters cut off, the server seed's hash with its last 4 cut
off, and a client seed in which O and 0, and I, l and 1, look the same in four places. The check fills the 5 missing
characters every possible way (1,048,576 ways): one fits the shown hash. It then tries the 36 readings of the client
seed on BC's November 2019 page: one gives the dealt hand. The three replacement cards, not used to pick the reading,
then match in order. The April 2020 and current pages give a different hand from the same seeds.

## The July 2024 bet

BC's own share record, retrieved 16 Nov 2026. The player's id and nickname are replaced; the client seed is the player's
own text and is kept, because the cards cannot be checked without it. The bet was on `VideoPoker`, the 99% game: four of
a kind paid 22x, and the 96% game only appears in 2025.
