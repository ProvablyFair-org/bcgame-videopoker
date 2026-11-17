# BC's verifier pages

The pages BC's game sends players to when they press Verify, saved byte for byte.

| file | what it is | source, fetched |
|---|---|---|
| `videopoker.html` | the video poker verifier BC links today | https://game-verify.github.io/public/videopoker.html, 5 Nov 2026 |
| `baccaratsingle.html` | the baccarat verifier BC links today | https://game-verify.github.io/public/baccaratsingle.html, 15 Nov 2026 |
| `lib/crypto-js.js`, `lib/tools.js` | the libraries the checks need from those pages | same site, same dates |

Archived copies of the video poker page: [Wayback Machine](https://web.archive.org/web/20261116180733/https://game-verify.github.io/public/videopoker.html).

## versions/

Every change to the video poker page in its public GitHub history (`commits.csv`: commit, date, message, file hash).

| file | commit | what changed |
|---|---|---|
| `2019-11-14_videopoker.html` | 385651d | first version: hash = SHA512(server seed + client seed + nonce); the 52 cards listed in suit order (spade A to K, heart A to K, club A to K, diamond A to K) |
| `2020-04-08_videopoker.html` | cb2be87 | the card list is replaced by BC's own order; the hash is unchanged |
| `2021-12-21_videopoker.html` | 1e64d72 | page edits; hash and card list unchanged |
| `2021-12-24_videopoker.html` | e78221b | hash = SHA512(hex(HMAC_SHA256(server seed, client seed:nonce))); card list unchanged. Byte-identical to today's `videopoker.html` |

Archived copies of the commit pages: [2019-11-14](https://web.archive.org/web/20261116181045/https://github.com/bc-game-project/verify/blob/385651dc485d00b44aed498899bfff4f5b39db36/videopoker.html), [2020-04-08](https://web.archive.org/web/20261116181128/https://github.com/bc-game-project/verify/blob/cb2be877a5d52bd347558af80edd3c0a5086321a/videopoker.html), [2021-12-24](https://web.archive.org/web/20261116181511/https://github.com/bc-game-project/verify/commit/e78221be44219c4c6b9b78fa195d758f57492987).

## links/

Where BC's game code sends players to verify.

| file | shows |
|---|---|
| `2026-11-05_bc.game_games-DEcz4odY.js` | bc.game's game list today: `VideoPoker98` and `BaccaratSingle98` verify at `https://game-verify.github.io/public/...` |
| `2026-11-05_bc.game_index-CmEYgXxK.js` | bc.game's bet-slip code that builds the link: `?s=<server seed>&c=<client seed>&n=<nonce>&he=<house edge>&m=<mode>` |
| `2022-04-23_arquivo_bc.game_index.66fd1f62.js` | bc.game's video poker code as archived by arquivo.pt on 23 Apr 2022: verify at `https://bcgame-project.github.io/verify/videopoker.html` |
| `2025-02-11_arquivo_bc.game_config-225813cf.js` | bc.game's game config as archived by arquivo.pt on 11 Feb 2025: `VideoPoker96` verifies at the same page |
| `identical.txt` | the video poker file is byte-identical at game-verify.github.io (BC's link today), at bcgame-project.github.io (BC's link in 2022 and 2025) and in the 24 Dec 2021 commit of github.com/bc-game-project/verify |

`make check` (checks/check_history.py) tests each line above.

## github/

Who owns the repository that holds the history above, and when its card list changed, from GitHub's own records. A
commit's date is written by whoever makes the commit. The push times and fork dates below are set by GitHub's servers
when the push or fork happens: GH Archive (https://www.gharchive.org) has kept GitHub's public events, hour by hour,
since 2011.

| file | what it holds |
|---|---|
| `receipt.json` | the records as read on 17 Nov 2026: the repository and its owner, BC's forum link to that owner, the account that pushed the changes, four pushes from GH Archive, three forks |
| `bc-forum-footer_archive.ph-mAgrj.txt` | the links in the footer of BC's forum, from the archive.today copy https://archive.ph/mAgrj (16 Nov 2026) |

**Whose repository it is.** The history is GitHub repository 218674280: `BCSNProject/verify` in GitHub's 2019 and 2020
records, `bc-game-project/verify` now (the account was renamed in 2020). BC's forum footer links its GitHub as
github.com/BCSNProject/bcgame-crash, which GitHub now serves from the same account. Every push GitHub logged came from
one account, whose website is https://bc.game. The repository was archived on 13 May 2022, the day
`bcgame-project/verify`, behind BC's links of 2022 and 2025, was created.

**When the card list changed.** GitHub logged the push of the suit-order page on 14 Nov 2019, 8 seconds after its
commit. It logged another push on 10 Feb 2020 with the video poker page unchanged, and a fork made on 8 Feb 2020 holds
that page. A push logged on 21 May 2020 came after the 8 Apr 2020 commit that swapped in the current list, so the new
list was public by then; a fork made on 10 Jun 2020 holds it. The push of the 8 Apr 2020 commit itself is not in GH
Archive (we read every hour of that day from the commit's time on). Every push it did log came within a minute of its
commit.

`make check` (checks/check_history.py) tests these records against the commits and files in `versions/`.
`make online` (checks/check_verifier_history_online.js, Node 18+, or pasted into the browser console on
https://data.gharchive.org/) reads them again from GitHub and GH Archive. On 17 Nov 2026 all 16 of its checks passed.
