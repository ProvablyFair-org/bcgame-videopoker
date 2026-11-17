"""BC.Game baccarat ("Baccarat Single"): independent rebuild of the published verifier's deal and rules.

Written from the page text of https://game-verify.github.io/public/baccaratsingle.html as fetched logged out on
2026-11-15 (verifier/baccaratsingle.html, sha256 3246e21a...7a4f, repo game-verify/public commit 494ad62). What the
page computes:

  hmac   = hex(HMAC_SHA256(key = server_seed, msg = client_seed + ":" + nonce))
  h1     = hex(SHA256(utf8(hmac)))                      64 hex characters
  h2     = hex(SHA256(utf8(h1)))
  keys   : card j (0..51) of the fixed 52-code list gets h1 rotated left by j characters;
           the same 52 codes again get h2 rotated left by j characters           -> 104 (key, card) pairs
  shoe   = the 104 cards in ascending order of key (plain string comparison)
  deal   : player = shoe[0], shoe[2]; banker = shoe[1], shoe[3]; third cards from shoe[4], shoe[5]
  rules  : card value = rank capped at 10, hand value = sum mod 10; player draws on 0-5 unless the banker has
           8 or 9; banker draws by the usual table (see banker_draws)

The page does NOT compare sha256(server_seed) with anything (it computes the value and does not show or use it),
and it shows no bet outcome or payout: only the cards and the two totals.

Card codes are BC's: code = suit*16 + rank, suit 10..13, rank 1..13 (A..K). The 52-code list is the same list the
video poker verifier uses (bcvp.SCRAMBLED).
"""
import hashlib
import hmac as _hmac

ALL = [161, 180, 199, 218, 162, 205, 181, 200, 219, 163, 182, 220, 201, 177, 196, 215, 170, 178,
       221, 197, 216, 171, 179, 198, 172, 217, 193, 212, 167, 186, 194, 173, 213, 168, 187, 195,
       214, 188, 169, 209, 164, 183, 202, 210, 189, 165, 184, 203, 211, 166, 204, 185]
DECKS = 2


def hmac_hex(server, client, nonce):
    return _hmac.new(server.encode(), ("%s:%s" % (client, nonce)).encode(), hashlib.sha256).hexdigest()


def shoe_from_hmac(hm, decks=DECKS):
    """The 104-card order for one hmac hex string."""
    h = hashlib.sha256(hm.encode()).hexdigest()
    keyed = []
    for _ in range(decks):
        hh = h + h
        keyed += [(hh[j:j + 64], c) for j, c in enumerate(ALL)]
        h = hashlib.sha256(h.encode()).hexdigest()
    keyed.sort(key=lambda kc: kc[0])
    return [c for _, c in keyed]


def value(card):
    r = card % 16
    return 0 if r >= 10 else r


def banker_draws(banker, player, third):
    """third = value of the player's third card, or -1 if the player did not draw."""
    if player >= 8:
        return False
    if banker <= 2:
        return True
    if banker == 3:
        return third != 8
    if banker == 4:
        return third not in (0, 1, 8, 9)
    if banker == 5:
        return third not in (0, 1, 2, 3, 8, 9)
    if banker == 6:
        return third in (6, 7)
    return False


def play(first6):
    """first6 = the first six cards of the shoe -> (player cards, banker cards, player total, banker total)."""
    p, b = [first6[0], first6[2]], [first6[1], first6[3]]
    pp, bp = (value(p[0]) + value(p[1])) % 10, (value(b[0]) + value(b[1])) % 10
    p_draw = pp < 6
    third = -1
    if p_draw and bp < 8:
        p.append(first6[4])
        third = value(first6[4])
    if banker_draws(bp, pp, third):
        b.append(first6[5] if p_draw else first6[4])
    return p, b, sum(map(value, p)) % 10, sum(map(value, b)) % 10


def deal(server, client, nonce):
    hm = hmac_hex(server, client, nonce)
    shoe = shoe_from_hmac(hm)
    return (hm, shoe) + play(shoe[:6])


def outcome(p, b, pt, bt):
    """Bet outcomes that follow from the cards alone. Pair = first two cards of the same RANK. BC's own pair
    definition is not in the verifier; this one fits the credit of all 150 live rounds of 16 Nov 2026
    (checks/check_baccarat_session.py)."""
    return {"player": pt > bt, "banker": bt > pt, "tie": pt == bt,
            "player_pair": p[0] % 16 == p[1] % 16, "banker_pair": b[0] % 16 == b[1] % 16}
