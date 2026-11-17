"""BC.Game Video Poker deal, rebuilt from BC's published verifier pages (verifier/ in this package).

Every version works the same way: make a hex hash from the seeds; card j of a fixed 52-card list gets that hash
rotated left by j characters as its key; sort the cards by key (plain ascending string sort). The first five cards
are dealt; replaced cards are taken in order from card 6 on, left to right.

  version (published verifier)    hash                                                card list
  2019-11-14                      SHA512(server + client + nonce)                      SUIT_ORDER
  2020-04-08                      SHA512(server + client + nonce)                      BC_LIST (SCRAMBLED below)
  2021-12-24, still current       SHA512(hex(HMAC_SHA256(key=server, client:nonce)))   BC_LIST
  BC's in-game fairness text      HMAC_SHA512(key=server, client:nonce)                SUIT_ORDER

Card codes are BC's: suit * 16 + rank, suit 10..13 = spades, hearts, clubs, diamonds; rank 1..13 = A..K.
"""
import hashlib
import hmac

SCRAMBLED = [161, 180, 199, 218, 162, 205, 181, 200, 219, 163, 182, 220, 201, 177, 196, 215, 170, 178,
             221, 197, 216, 171, 179, 198, 172, 217, 193, 212, 167, 186, 194, 173, 213, 168, 187, 195,
             214, 188, 169, 209, 164, 183, 202, 210, 189, 165, 184, 203, 211, 166, 204, 185]
SUIT_ORDER = [s * 16 + r for s in range(10, 14) for r in range(1, 14)]

RANKS = " ,A,2,3,4,5,6,7,8,9,10,J,Q,K".split(",")
SUIT_SYM = ["♠", "♥", "♣", "♦"]
SUIT_LETTER = ["s", "h", "c", "d"]

# Paytables, index = hand class below (gross multipliers, stake included), from BC's game server (evidence/claims)
PAYTABLES = {
    "98": [0, 1, 2, 3, 4, 6, 8, 22, 80, 800],   # VideoPoker98, live now
    "99": [0, 1, 2, 3, 4, 6, 9, 22, 60, 800],   # VideoPoker (99%), 2020 to early 2025
    "96": [0, 1, 2, 3, 4, 5, 8, 18, 80, 800],   # VideoPoker96, from early 2025
}
PAYTABLE = PAYTABLES["98"]
CLASS_NAMES = ["nothing", "jacks or better", "two pair", "three of a kind", "straight", "flush",
               "full house", "four of a kind", "straight flush", "royal flush"]


def _hmac(key, msg, algo):
    return hmac.new(key.encode(), msg.encode(), algo).hexdigest()


def h_verifier(server, client, nonce):
    return hashlib.sha512(_hmac(server, f"{client}:{nonce}", hashlib.sha256).encode()).hexdigest()


def h_hmac512(server, client, nonce):
    return _hmac(server, f"{client}:{nonce}", hashlib.sha512)



def h_concat_sha512(server, client, nonce):
    return hashlib.sha512(f"{server}{client}{nonce}".encode()).hexdigest()


VARIANTS = {
    # name: (hash function, card list)
    "verifier_2021": (h_verifier, SCRAMBLED),        # current
    "verifier_2020": (h_concat_sha512, SCRAMBLED),
    "verifier_2019": (h_concat_sha512, SUIT_ORDER),
    "fairness_text": (h_hmac512, SUIT_ORDER),
}


def shuffle(h, deck):
    """Full 52-card order: card j of deck gets h rotated left by j chars as its key; ascending string sort."""
    hh = h + h
    keyed = [(hh[j:j + len(h)], j) for j in range(len(deck))]
    keyed.sort(key=lambda kv: kv[0])   # equal keys impossible for distinct rotations of a 128-char hash in practice
    return [deck[j] for _, j in keyed]


def deal(variant, server, client, nonce):
    hf, deck = VARIANTS[variant]
    h = hf(server, client, int(nonce))
    return h, shuffle(h, deck)


# ---------------------------------------------------------------- draws
def draw_sequential(initial5, held, order):
    """Discarded positions, left to right, take shuffled cards 6, 7, ... (as the live game does, and vpsim.c)."""
    nxt = 5
    out = []
    for c in initial5:
        if c in held:
            out.append(c)
        else:
            out.append(order[nxt])
            nxt += 1
    return out



# ---------------------------------------------------------------- cards
def txt(code):
    return RANKS[code % 16] + SUIT_SYM[(code & 240) // 16 - 10]


def parse_card(tok):
    """Accept a BC code (161), or text like 'As', 'A♠', '10h', 'Th', 'qd'."""
    tok = str(tok).strip()
    if tok.isdigit():
        c = int(tok)
        if c not in SUIT_ORDER:
            raise ValueError(f"not a BC card code: {tok}")
        return c
    sym = {"♠": "s", "♥": "h", "♣": "c", "♦": "d", "♤": "s", "♡": "h", "♧": "c", "♢": "d"}
    s = tok[-1]
    s = sym.get(s, s.lower())
    r = tok[:-1].upper()
    r = {"T": "10", "1": "A"}.get(r, r)
    if s not in SUIT_LETTER or r not in RANKS[1:]:
        raise ValueError(f"cannot parse card: {tok!r}")
    return (10 + SUIT_LETTER.index(s)) * 16 + RANKS.index(r)


def parse_cards(field):
    if field is None:
        return []
    if isinstance(field, (list, tuple)):
        return [parse_card(x) for x in field]
    field = str(field).replace(",", " ").split()
    return [parse_card(x) for x in field]


# ---------------------------------------------------------------- classifier (Jacks or Better)
def classify(hand):
    ranks = sorted(((c % 16) if c % 16 != 1 else 14) for c in hand)
    suits = {c >> 4 for c in hand}
    counts = sorted((ranks.count(r) for r in set(ranks)), reverse=True)
    flush = len(suits) == 1
    uniq = sorted(set(ranks))
    straight = len(uniq) == 5 and (uniq[4] - uniq[0] == 4 or uniq == [2, 3, 4, 5, 14])
    if flush and straight:
        return 9 if uniq[0] == 10 else 8
    if counts[0] == 4:
        return 7
    if counts == [3, 2]:
        return 6
    if flush:
        return 5
    if straight:
        return 4
    if counts[0] == 3:
        return 3
    if counts == [2, 2, 1]:
        return 2
    if counts[0] == 2:
        pr = [r for r in set(ranks) if ranks.count(r) == 2][0]
        return 1 if pr >= 11 else 0
    return 0
