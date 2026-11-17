"""Decoder for the raw socket frames in evidence/*/game-frames.json.

BC's game socket (socket.io over a websocket) sends binary frames:
  byte 0      4 (engine.io message)
  byte 1      socket.io packet type (2 event, 3 ack), +128 when an ack id follows as uint32 big-endian
  then        1 byte length + namespace, 1 byte length + event name, the rest is a protobuf body
  ack body    ResultObj {1 code sint32, 2 msg string, 3 data bytes}; code 0 = ok
This is the same reading as the capture script that recorded the frames (it decoded them in the browser as they arrived);
decode_requests() rebuilds that script's "decoded" list from the raw bytes alone. The capture ran in JavaScript, where
a varint is a double, so integers above 2**53 are kept here the way JavaScript held them (js_number).
"""
import base64

GV_NOTE = "GameValue {1 active, 2 result, 3 initialHard[], 4 playerHard[], 5 holdHard[]} (packed sint32)"


def js_number(raw_bytes):
    """A varint read the way the capture script read it: r += (x & 127) * 2**s, in doubles."""
    r, s = 0.0, 0
    for x in raw_bytes:
        r += (x & 127) * 2.0 ** s
        s += 7
    return int(r) if r.is_integer() else r


def varint(b, i):
    start = i
    while True:
        if i >= len(b):
            raise ValueError("eof")
        x = b[i]
        i += 1
        if x < 128:
            break
    return js_number(b[start:i]), i


def zz(n):
    return -(n + 1) // 2 if n % 2 else n // 2


def pb(b):
    """Generic protobuf parse: field number -> list of values (ints for varints, bytes otherwise)."""
    o, i = {}, 0
    while i < len(b):
        t, i = varint(b, i)
        f, w = int(t) // 8, int(t) & 7
        if f == 0:
            raise ValueError("field 0")
        if w == 0:
            v, i = varint(b, i)
        elif w == 2:
            n, i = varint(b, i)
            n = int(n)
            if i + n > len(b):
                raise ValueError("len")
            v, i = bytes(b[i:i + n]), i + n
        elif w == 5:
            v, i = bytes(b[i:i + 4]), i + 4
        elif w == 1:
            v, i = bytes(b[i:i + 8]), i + 8
        else:
            raise ValueError("wire %d" % w)
        o.setdefault(str(f), []).append(v)
    return o


def b64(b):
    return base64.b64encode(b).decode()


def _printable(v):
    try:
        s = v.decode("utf-8")
    except UnicodeDecodeError:
        return None
    return s if all(0x20 <= ord(ch) <= 0x7E for ch in s) else None


def dump(b, depth=0):
    """Readable view of a protobuf body: nested messages, printable strings, varints; other bytes as base64."""
    try:
        o = pb(b)
    except ValueError:
        return {"_bytes_b64": b64(b)}
    r = {}
    for k, vals in o.items():
        out = []
        for v in vals:
            if not isinstance(v, bytes):
                out.append(v)
                continue
            if depth < 5 and len(v):
                try:
                    pb(v)
                    d = dump(v, depth + 1)
                    if "_bytes_b64" not in d:
                        out.append(d)
                        continue
                except ValueError:
                    pass
            s = _printable(v)
            out.append(s if s is not None else {"_bytes_b64": b64(v)})
        r[k] = out
    return r


def packed(b):
    r, i = [], 0
    while i < len(b):
        v, i = varint(b, i)
        r.append(zz(int(v)))
    return r


def is_card(c):
    return 1 <= c % 16 <= 13 and 10 <= (c >> 4) <= 13


def find_game_value(b, depth=0):
    """First nested message that parses as GameValue with card arrays (video poker)."""
    if depth > 5:
        return None
    try:
        o = pb(b)
    except ValueError:
        return None
    if isinstance((o.get("3") or [None])[0], bytes) and isinstance((o.get("4") or [None])[0], bytes):
        try:
            ih, ph = packed(o["3"][0]), packed(o["4"][0])
            if len(ih) >= 5 and all(map(is_card, ih)) and all(map(is_card, ph)):
                return {"active": zz(int(o["1"][0])) if "1" in o else 0, "result": zz(int(o["2"][0])) if "2" in o else 0,
                        "initialHard": ih, "playerHard": ph,
                        "holdHard": packed(o["5"][0]) if isinstance((o.get("5") or [None])[0], bytes) else []}
        except ValueError:
            pass
    for vals in o.values():
        for v in vals:
            if isinstance(v, bytes) and len(v) > 4:
                g = find_game_value(v, depth + 1)
                if g:
                    return g
    return None


def parse(raw):
    """One socket.io binary frame -> {type, ack, nsp, ev, body}, or None."""
    if len(raw) < 4 or raw[0] != 4:
        return None
    i, typ, ack = 1, raw[1], None
    i = 2
    if typ >= 128:
        typ -= 128
        ack = int.from_bytes(raw[i:i + 4], "big")
        i += 4
    nl = raw[i]
    nsp = raw[i + 1:i + 1 + nl].decode()
    i += 1 + nl
    el = raw[i]
    ev = raw[i + 1:i + 1 + el].decode()
    i += 1 + el
    return {"type": typ, "ack": ack, "nsp": nsp, "ev": ev, "body": raw[i:]}


def packets(frames):
    out = []
    for f in frames:
        if "b64" not in f:
            continue
        p = parse(base64.b64decode(f["b64"]))
        if p:
            p.update(dir=f["dir"], t=f["t"], frame=f["i"])
            out.append(p)
    return out


def result(ack_packet):
    if ack_packet is None:
        return {"code": None, "msg": "", "data": b""}
    o = pb(ack_packet["body"])
    return {"code": zz(int(o["1"][0])) if "1" in o else 0, "msg": o["2"][0].decode() if "2" in o else "",
            "data": o["3"][0] if "3" in o else b""}


def decode_requests(frames, nsp_prefix):
    """Every request on the game namespace with its ack (same namespace and ack id), decoded from the raw bytes."""
    ps = packets(frames)
    out = []
    for p in ps:
        if p["dir"] != "out" or p["type"] != 2 or not p["nsp"].startswith(nsp_prefix) or p["ack"] is None:
            continue
        a = next((q for q in ps if q["dir"] == "in" and q["type"] == 3 and q["nsp"] == p["nsp"]
                  and q["ack"] == p["ack"] and q["t"] >= p["t"]), None)
        r = result(a)
        out.append({"ev": p["ev"], "nsp": p["nsp"], "ack_id": p["ack"], "t_out": p["t"], "t_in": a["t"] if a else None,
                    "frame_out": p["frame"], "frame_in": a["frame"] if a else None, "request": dump(p["body"]),
                    "code": r["code"], "msg": r["msg"], "data": dump(r["data"]) if r["data"] else None,
                    "gameValue": find_game_value(r["data"]) if r["data"] else None, "_raw_data": r["data"],
                    "_raw_request": p["body"]})
        if a is None:
            del out[-1]["msg"]   # as the capture script saved a request without an answer
    return out


def pushes(frames, nsp, ev):
    """Server events (no ack) on a namespace, with their decoded bodies."""
    return [dict(p, data=dump(p["body"])) for p in packets(frames)
            if p["dir"] == "in" and p["type"] == 2 and p["nsp"] == nsp and p["ev"] == ev]


BIG = 2 ** 53


def norm_js(x):
    """For comparing with the capture script's saved decode: integers above 2**53 as JavaScript held them."""
    if isinstance(x, bool):
        return x
    if isinstance(x, int) and abs(x) > BIG:
        return float(x)
    if isinstance(x, dict):
        return {k: norm_js(v) for k, v in x.items() if not k.startswith("_raw")}
    if isinstance(x, list):
        return [norm_js(v) for v in x]
    return x


def text(v):
    return v.decode() if isinstance(v, bytes) else str(v)


def balance_pushes(frames):
    """BC's /user balance-change-v2 pushes: {1 sequence, 2 bet id, 3 currency, 4 balance after, 7 change}."""
    out = []
    for p in packets(frames):
        if p["dir"] == "in" and p["type"] == 2 and p["nsp"] == "/user" and p["ev"] == "balance-change-v2":
            o = pb(p["body"])
            out.append({"frame": p["frame"], "t": p["t"], "id": text(o["2"][0]), "currency": text(o["3"][0]),
                        "balance": text(o["4"][0]), "change": text(o["7"][0])})
    return out


def seed_changes(dec):
    """Each seed change, with the seed-next-hash answer that first carried its server seed hash."""
    out = []
    for d in dec:
        if d["ev"] != "seed-change" or not d.get("data"):
            continue
        h = d["data"]["2"][0]
        src = next((x for x in dec if x["ev"] == "seed-next-hash" and x.get("data") and x["data"]["2"][0]["2"][0] == h), None)
        out.append({"client_seed": d["request"]["2"][0], "hash": h, "change": d, "hash_answer": src})
    return out


def vp_hands(dec):
    """Video poker: each bet answer with the deal request(s) and the deal answer that follow it."""
    hands = []
    for d in dec:
        if d["ev"] == "bet" and d["code"] == 0:
            o = pb(d["_raw_data"])
            gv = pb(o["5"][0])
            hands.append({"bet_id": text(o["1"][0]), "dealt": packed(gv["4"][0]), "stake": text(o["8"][0]),
                          "deal_requests": 0, "bet_frame": d["frame_in"]})
        elif d["ev"] == "deal" and hands:
            h = hands[-1]
            h["deal_requests"] += 1
            q = pb(d["_raw_request"])
            held = q.get("1", [])
            h["held_sent"] = packed(held[0]) if held and isinstance(held[0], bytes) else [zz(int(v)) for v in held]
            if d["code"] == 0:
                o = pb(d["_raw_data"])
                gv = pb(o["5"][0])
                h.update(deal_id=text(o["1"][0]), ten=packed(gv["3"][0]), final=packed(gv["4"][0]),
                         stake_at_deal=text(o["8"][0]), win=text(o["9"][0]))
    return hands


def baccarat_rounds(dec):
    """Baccarat: each bet request and its answer {1 bet id, 5 {1 player cards, 2 banker cards, 3/4 points}, 8 stake, 9 credit}."""
    out = []
    for d in dec:
        if d["ev"] != "bet":
            continue
        q = pb(d["_raw_request"])
        bets = [pb(x) for x in pb(q["3"][0]).get("1", [])]
        r = {"stake_sent": text(q["2"][0]), "bets_sent": [(zz(int(b["1"][0])) if "1" in b else 0, text(b["2"][0])) for b in bets],
             "code": d["code"], "frame": d["frame_in"]}
        if d["code"] == 0:
            o = pb(d["_raw_data"])
            gv = pb(o["5"][0])
            r.update(id=text(o["1"][0]), players=packed(gv["1"][0]), bankers=packed(gv["2"][0]),
                     player_point=zz(int(gv["3"][0])) if "3" in gv else 0, banker_point=zz(int(gv["4"][0])) if "4" in gv else 0,
                     stake=text(o["8"][0]), credit=text(o["9"][0]))
        out.append(r)
    return out
