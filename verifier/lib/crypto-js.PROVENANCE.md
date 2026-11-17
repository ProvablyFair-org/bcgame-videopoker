# CryptoJS provenance and notices

`crypto-js.js` is the unchanged library captured with BC.Game's published verifier pages; see
[`../README.md`](../README.md) for those captures. Its contents are byte-identical to
[`crypto-js.js` in the official `brix/crypto-js` tag `3.1.9-1`](https://github.com/brix/crypto-js/blob/3.1.9-1/crypto-js.js).
This identifies the bundled source against that release tag; it does not claim that BC supplied a version label.

The comparison was checked on 17 November 2026 using the
[official GitHub contents API](https://api.github.com/repos/brix/crypto-js/contents/crypto-js.js?ref=3.1.9-1).
The API's Git blob SHA-1 and byte size exactly match those calculated from the local file:

| Identifier | Value |
|---|---|
| Size | 191936 bytes |
| Git blob SHA-1 | `17f2b1163a74d56fd16b4e2de193d975a0f464d2` |
| Local SHA-256 | `c6826494432163d74fd27e78ad011a13d55e4670441cd49fc9f1e52a4afd28d9` |

Git blob SHA-1 hashes `blob <byte-size>\0` followed by the file bytes, rather than the file bytes alone.
The tag's [`package.json`](https://github.com/brix/crypto-js/blob/3.1.9-1/package.json)
reports version `3.1.9` and license `MIT`; `3.1.9-1` is the upstream tag used for this comparison.

[`crypto-js.LICENSE.txt`](crypto-js.LICENSE.txt) reproduces the MIT notice from the
[same tag's upstream LICENSE](https://raw.githubusercontent.com/brix/crypto-js/3.1.9-1/LICENSE),
including the Jeff Mott and Evan Vosberg copyright notices. It also reproduces the Cédric Mesnil
RIPEMD-160 component notice already embedded in `crypto-js.js` (beginning at line 1627).
That embedded notice remains in place. Adding these companion files does not alter or relicense the captured JavaScript.
