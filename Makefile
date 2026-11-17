# BC.Game Video Poker and Baccarat: evidence package.
# make check (a few minutes)  |  make oracle (about 30 CPU minutes)  |  make sims (several CPU hours)
# make online (reads the GitHub records in verifier/github/ again from GitHub and GH Archive; needs internet)
PY ?= python3
export PYTHONDONTWRITEBYTECODE = 1
CC ?= cc
THREADS ?= $(shell nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)
ifeq ($(shell uname -s),Darwin)
LIBS = -lpthread
else
LIBS = -lpthread -lcrypto -lm
endif

.PHONY: check build oracle sims online clean

check: build
	$(PY) checks/verify_manifest.py
	$(PY) checks/parity.py
	$(PY) checks/check_video_poker_session.py
	$(PY) checks/check_hint.py
	$(PY) checks/check_fairness_text.py
	$(PY) checks/check_baccarat_session.py
	$(PY) checks/check_history.py
	$(PY) checks/check_exact_returns.py
	$(PY) checks/make_bc_compare.py --check
	$(PY) checks/summarize.py

build: build/vpsim build/exact_holds

build/vpsim: src/vpsim.c
	mkdir -p build
	$(CC) -O3 -o $@ src/vpsim.c $(LIBS)

build/exact_holds: checks/exact_holds.c src/vpsim.c
	mkdir -p build
	$(CC) -O2 -o $@ checks/exact_holds.c $(LIBS)

oracle: build
	$(PY) checks/check_holds_oracle.py $(THREADS)

sims: build
	$(PY) checks/run_sims.py --threads $(THREADS)
	$(PY) checks/summarize.py

online:
	node checks/check_verifier_history_online.js

clean:
	rm -rf build
