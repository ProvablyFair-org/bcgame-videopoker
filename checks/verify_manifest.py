#!/usr/bin/env python3
"""Every file in the package against SHA256SUMS (build/ excluded). Also lists files that are not in the manifest."""
import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ROOT, check, finish

listed = {}
for line in open(os.path.join(ROOT, "SHA256SUMS"), encoding="utf8"):
    h, name = line.rstrip("\n").split("  ", 1)
    listed[name] = h
bad = [n for n, h in listed.items() if not os.path.exists(os.path.join(ROOT, n))
       or hashlib.sha256(open(os.path.join(ROOT, n), "rb").read()).hexdigest() != h]
extra = []
for d, _, files in os.walk(ROOT):
    rel = os.path.relpath(d, ROOT)
    if rel.split(os.sep)[0] in ("build", ".git") or "__pycache__" in rel:
        continue
    for f in files:
        n = os.path.normpath(os.path.join(rel, f)).replace(os.sep, "/")
        if n != "SHA256SUMS" and n not in listed:
            extra.append(n)
check("every file matches SHA256SUMS", not bad, "%d files%s" % (len(listed), (", changed or missing: " + ", ".join(bad[:5])) if bad else ""))
check("no file outside the manifest", not extra, ", ".join(extra[:5]))
finish()
