"""Shared helpers for the checks in this folder. Python standard library only; node runs BC's own page code."""
import base64
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

VERIFIER = os.path.join(ROOT, "verifier")
CRYPTO_JS = os.path.join(VERIFIER, "lib", "crypto-js.js")
VP_PAGES = {
    "verifier_2019": os.path.join(VERIFIER, "versions", "2019-11-14_videopoker.html"),
    "verifier_2020": os.path.join(VERIFIER, "versions", "2020-04-08_videopoker.html"),
    "verifier_2021": os.path.join(VERIFIER, "videopoker.html"),
}
BAC_PAGE = os.path.join(VERIFIER, "baccaratsingle.html")

FAILS = []


def path(*p):
    return os.path.join(ROOT, *p)


def load(*p):
    with open(path(*p), encoding="utf8") as f:
        return json.load(f)


def check(label, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + label + (("   " + detail) if detail else ""))
    if not ok:
        FAILS.append(label)
    return ok


def finish():
    if FAILS:
        print("\n%d check(s) failed" % len(FAILS))
        sys.exit(1)
    print("\nall checks passed")


def bc_videopoker_page(page, rows, mode="asis"):
    """Run BC's own video poker page code (verbatim, in node) on (server, client, nonce) rows.
    Returns one (hash, [first ten card codes]) per row."""
    inp = "".join("%s\t%s\t%s\n" % r for r in rows)
    out = subprocess.run(["node", path("checks", "bc_page_videopoker.js"), page, CRYPTO_JS, mode],
                         input=inp, capture_output=True, text=True, check=True).stdout
    res = []
    for line in out.splitlines():
        s, c, n, h, cards = line.split("\t")
        res.append((h, [int(x) for x in cards.split(",")]))
    return res


def bc_baccarat_page(rows):
    """Run BC's own baccarat page code (the two functions cut from the page, unedited) on (server, client, nonce)."""
    inp = "".join("%s\t%s\t%s\n" % r for r in rows)
    out = subprocess.run(["node", path("checks", "bc_page_baccarat.js"), BAC_PAGE, os.path.join(VERIFIER, "lib")],
                         input=inp, capture_output=True, text=True, check=True).stdout
    res = []
    for line in out.splitlines():
        s, c, n, hm, shoe, pv, bv, pt, bt = line.split("\t")
        res.append({"hmac": hm, "shoe": [int(x) for x in shoe.split(",")],
                    "player_values": [int(x) for x in pv.split(",")], "banker_values": [int(x) for x in bv.split(",")],
                    "player_total": int(pt), "banker_total": int(bt)})
    return res


def zigzag_bytes(b64):
    """Packed sint32 values (protobuf) from a base64 field of the decoded game frames."""
    raw = base64.b64decode(b64)
    out, cur, shift = [], 0, 0
    for byte in raw:
        cur |= (byte & 0x7F) << shift
        shift += 7
        if not byte & 0x80:
            out.append((cur >> 1) ^ -(cur & 1))
            cur, shift = 0, 0
    return out
