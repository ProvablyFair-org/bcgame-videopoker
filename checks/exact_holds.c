// Per-hand hold values from the exact calculator in src/vpsim.c (used by checks/check_hint.py).
// vpsim.c is included unedited; only its main() is renamed. The tables F[k] it builds (sum of payouts of every 5-card
// hand that contains a given subset) and its inclusion-exclusion formula are used exactly as in build_tables().
// stdin: one hand per line, five BC card codes in dealt order. stdout: line "EXACT <rtp>", then per hand 32 values,
// value m = expected return of holding the dealt positions in mask m (bit 0 = position 1), then vpsim's own best value.
// build: cc -O2 -o exact_holds checks/exact_holds.c -lpthread -lcrypto -lm     paytable: env PAYTABLE as for vpsim
#define main vpsim_main
#include "../src/vpsim.c"
#undef main

int main(void) {
  init_binom();
  if (getenv("PAYTABLE")) { char *e = strdup(getenv("PAYTABLE")), *tok = strtok(e, ","); for (int k = 1; k < 10 && tok; k++, tok = strtok(NULL, ",")) PAY[k] = atof(tok); }
  double exact; uint64_t cc[10];
  build_tables(&exact, cc);
  printf("EXACT %.10f\n", exact);
  int code[5];
  while (scanf("%d %d %d %d %d", &code[0], &code[1], &code[2], &code[3], &code[4]) == 5) {
    int id[5], sorted[5], sub[5];
    for (int i = 0; i < 5; i++) id[i] = sorted[i] = code2id(code[i]);
    qsort(sorted, 5, sizeof(int), cmpint);
    for (int m = 0; m < 32; m++) {            // m is over DEALT positions
      double sum = 0;
      int dmask = (~m) & 31;
      for (int t = dmask;; t = (t - 1) & dmask) {
        int u = m | t, k = 0;
        for (int i = 0; i < 5; i++) if (u >> i & 1) sub[k++] = id[i];
        qsort(sub, k, sizeof(int), cmpint);
        sum += (__builtin_popcount(t) & 1 ? -1.0 : 1.0) * F[k][cidx(sub, k)];
        if (t == 0) break;
      }
      printf("%.15g ", sum / (double)BINOM[47][5 - __builtin_popcount(m)]);
    }
    printf("%.9g\n", (double)EVBEST[cidx(sorted, 5)]);
  }
  return 0;
}
