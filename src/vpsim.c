// Variant knobs (environment):
//   VP_DECK=scrambled|suit   VP_HASH=verifier|hmac512|plain2019   VP_DRAW=sequential|positional   VP_ARMS=1|2
//   VP_SERVER=<server seed>  (default pf-audit-server-seed-2026-11-05; client seed is fixed at pf-audit-client)
//   defaults = the current verifier (scrambled list, SHA512(hex(HMAC_SHA256))), sequential draws, two arms.
//   suit      = spade A-K, heart A-K, club A-K, diamond A-K (2019 page, and BC's fairness text).
//   hmac512   = HMAC_SHA512(key=server, msg=client:nonce) hex (BC's fairness text).
//   plain2019 = SHA512(server+client+nonce) hex (verifier pages of 2019-11-14 and 2020-04-08).
// Portability: CommonCrypto on macOS, OpenSSL elsewhere (cc ... -lcrypto). Same digests either way.
//
// BC.game video poker: exact optimal-strategy RTP for a uniform deck, plus simulation of the
// BC verifier shuffle (real HMAC-SHA256 -> SHA512 -> rotate/sort pipeline) and a uniform control.
//
// build: cc -O3 -o vpsim vpsim.c -lpthread          (Linux: add -lcrypto)
// run:   ./vpsim <n_deals_per_arm> <threads> <outdir>
//
// Paytable (multiplier "for 1", index = hand class):
//   0 nothing, 1 Jacks or Better, 2 Two Pair, 3 Trips, 4 Straight, 5 Flush, 6 Full House,
//   7 Quads, 8 Straight Flush, 9 Royal Flush
//   PAY = {0,1,2,3,4,6,8,22,60,800}  -- BC's fallback paytable in the client, `fallbackPayouts:Dt` in data/bc-site/index--9V6N-Vk.js
//
// Draw convention used for the biased arm (ASSUMPTION, not taken from BC code): dealt hand =
// shuffled cards 1..5; discarded positions are refilled left-to-right from shuffled cards 6..10
// (VP_DRAW=positional: discarded slot i takes card 6+i).
#ifdef __APPLE__
#include <CommonCrypto/CommonDigest.h>
#include <CommonCrypto/CommonHMAC.h>
#else
#include <openssl/evp.h>
#include <openssl/hmac.h>
#include <openssl/sha.h>
#define kCCHmacAlgSHA256 0
#define kCCHmacAlgSHA512 1
#define CC_SHA512(d, n, out) SHA512((const unsigned char *)(d), (size_t)(n), (out))
static void CCHmac(int alg, const void *key, size_t kl, const void *msg, size_t ml, unsigned char *out) {
  unsigned int ol = 0;
  HMAC(alg ? EVP_sha512() : EVP_sha256(), key, (int)kl, (const unsigned char *)msg, ml, out, &ol);
}
#endif
#include <math.h>
#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int ALL_CARDS[52] = {161, 180, 199, 218, 162, 205, 181, 200, 219, 163, 182, 220, 201, 177, 196, 215, 170, 178,
                                  221, 197, 216, 171, 179, 198, 172, 217, 193, 212, 167, 186, 194, 173, 213, 168, 187, 195,
                                  214, 188, 169, 209, 164, 183, 202, 210, 189, 165, 184, 203, 211, 166, 204, 185};
static double PAY[10] = {0, 1, 2, 3, 4, 6, 8, 22, 60, 800};   // override: env PAYTABLE="JoB,2P,3K,S,F,FH,4K,SF,RF"
static const char *CLASS_NAME[10] = {"nothing/low pair", "jacks or better", "two pair", "three of a kind", "straight",
                                     "flush", "full house", "four of a kind", "straight flush", "royal flush"};
static const char *SERVER = "pf-audit-server-seed-2026-11-05";
static const char *CLIENT = "pf-audit-client";

// internal id = suit*13 + (point-1); point 1=A .. 13=K
static int code2id(int code) { return ((code & 240) / 16 - 10) * 13 + (code % 16 - 1); }
static int POS2ID[52];
static int HASH512 = 0, POSITIONAL = 0, HASHPLAIN = 0;

static uint64_t BINOM[53][6];
static void init_binom(void) {
  for (int n = 0; n <= 52; n++) {
    BINOM[n][0] = 1;
    for (int k = 1; k <= 5; k++) BINOM[n][k] = n == 0 ? 0 : BINOM[n - 1][k - 1] + BINOM[n - 1][k];
  }
}
// colex index of sorted ascending ids c[0..k-1]
static inline uint32_t cidx(const int *c, int k) {
  uint32_t r = 0;
  for (int i = 0; i < k; i++) r += (uint32_t)BINOM[c[i]][i + 1];
  return r;
}

static int classify(const int *id) {
  int cnt[14] = {0}, suit0 = id[0] / 13, flush = 1, pts[5];
  for (int i = 0; i < 5; i++) {
    int p = id[i] % 13 + 1;
    pts[i] = p;
    cnt[p]++;
    if (id[i] / 13 != suit0) flush = 0;
  }
  int pairs = 0, trips = 0, quads = 0, distinct = 0, highpair = 0;
  for (int p = 1; p <= 13; p++) {
    if (cnt[p]) distinct++;
    if (cnt[p] == 2) { pairs++; if (p == 1 || p >= 11) highpair = 1; }
    if (cnt[p] == 3) trips++;
    if (cnt[p] == 4) quads++;
  }
  int straight = 0, royal = 0;
  if (distinct == 5) {
    int mn = 14, mx = 0;
    for (int i = 0; i < 5; i++) { if (pts[i] < mn) mn = pts[i]; if (pts[i] > mx) mx = pts[i]; }
    if (mx - mn == 4) straight = 1;
    if (cnt[1] && cnt[10] && cnt[11] && cnt[12] && cnt[13]) straight = 1, royal = 1;
  }
  if (straight && flush) return royal ? 9 : 8;
  if (quads) return 7;
  if (trips && pairs) return 6;
  if (flush) return 5;
  if (straight) return 4;
  if (trips) return 3;
  if (pairs == 2) return 2;
  if (pairs == 1 && highpair) return 1;
  return 0;
}

#define NH 2598960
static double *F[6];            // F[k][colex(subset)] = sum of payouts of all 5-card hands containing subset
static float *EVBEST;           // per hand (colex index), optimal-hold expected return (uniform deck)
static uint8_t *BESTMASK;       // per hand, bit i = hold i-th smallest id
static uint8_t *HCLASS;         // per hand, class

static void build_tables(double *exact_rtp, uint64_t class_count[10]) {
  for (int k = 0; k <= 5; k++) F[k] = calloc(BINOM[52][k], sizeof(double));
  EVBEST = malloc(NH * sizeof(float));
  BESTMASK = malloc(NH);
  HCLASS = malloc(NH);
  int c[5], sub[5];
  memset(class_count, 0, 10 * sizeof(uint64_t));
  for (c[0] = 0; c[0] < 52; c[0]++) for (c[1] = c[0] + 1; c[1] < 52; c[1]++) for (c[2] = c[1] + 1; c[2] < 52; c[2]++)
  for (c[3] = c[2] + 1; c[3] < 52; c[3]++) for (c[4] = c[3] + 1; c[4] < 52; c[4]++) {
    int cl = classify(c);
    uint32_t hi = cidx(c, 5);
    HCLASS[hi] = cl;
    class_count[cl]++;
    double pay = PAY[cl];
    for (int m = 0; m < 32; m++) {
      int k = 0;
      for (int i = 0; i < 5; i++) if (m >> i & 1) sub[k++] = c[i];
      F[k][cidx(sub, k)] += pay;
    }
  }
  double total = 0;
  for (c[0] = 0; c[0] < 52; c[0]++) for (c[1] = c[0] + 1; c[1] < 52; c[1]++) for (c[2] = c[1] + 1; c[2] < 52; c[2]++)
  for (c[3] = c[2] + 1; c[3] < 52; c[3]++) for (c[4] = c[3] + 1; c[4] < 52; c[4]++) {
    double best = -1; int bm = 0;
    for (int m = 0; m < 32; m++) {
      double sum = 0;
      int dmask = (~m) & 31;
      for (int t = dmask;; t = (t - 1) & dmask) {          // all T subset of discards
        int u = m | t, k = 0;
        for (int i = 0; i < 5; i++) if (u >> i & 1) sub[k++] = c[i];
        sum += (__builtin_popcount(t) & 1 ? -1.0 : 1.0) * F[k][cidx(sub, k)];
        if (t == 0) break;
      }
      double ev = sum / (double)BINOM[47][5 - __builtin_popcount(m)];
      if (ev > best + 1e-12) { best = ev; bm = m; }
    }
    uint32_t hi = cidx(c, 5);
    EVBEST[hi] = (float)best;
    BESTMASK[hi] = (uint8_t)bm;
    total += best;
  }
  *exact_rtp = total / NH;
}

// ---------------------------------------------------------------- simulation
typedef struct {
  int arm;                 // 0 = BC verifier shuffle, 1 = uniform Fisher-Yates control
  uint64_t start, n;
  uint64_t pair[52][52];   // co-occurrence in first 5, by ALL_CARDS list position
  uint64_t cls[10];
  double nb_sum, nb_sq;    // neighbour pairs (|i-j|==1) per deal
  double ev_sum, ev_sq;    // deal-only: optimal EV of dealt hand, uniform draws
  double pl_sum, pl_sq;    // full play: draws from shuffled cards 6..10
  uint64_t final_cls[10];
} Acc;

static uint64_t splitmix(uint64_t *s) {
  uint64_t z = (*s += 0x9E3779B97F4A7C15ULL);
  z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
  z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
  return z ^ (z >> 31);
}

static void sort_rotations(const char *hh, int *ord) {
  // insertion sort of 52 rotation start positions by memcmp of 128 chars
  for (int i = 0; i < 52; i++) ord[i] = i;
  for (int i = 1; i < 52; i++) {
    int v = ord[i], j = i - 1;
    while (j >= 0 && memcmp(hh + ord[j], hh + v, 128) > 0) { ord[j + 1] = ord[j]; j--; }
    ord[j + 1] = v;
  }
}

static void bc_order(uint64_t nonce, int *ord) {
  char msg[128], hex256[65], hh[257];
  int ml = snprintf(msg, sizeof msg, "%s:%llu", CLIENT, (unsigned long long)nonce);
  unsigned char mac[32], d512[64];
  static const char *hx = "0123456789abcdef";
  if (HASHPLAIN) {
    char pm[256]; int pl = snprintf(pm, sizeof pm, "%s%s%llu", SERVER, CLIENT, (unsigned long long)nonce);
    CC_SHA512(pm, pl, d512);
  } else if (HASH512) {
    CCHmac(kCCHmacAlgSHA512, SERVER, strlen(SERVER), msg, ml, d512);
  } else {
    CCHmac(kCCHmacAlgSHA256, SERVER, strlen(SERVER), msg, ml, mac);
    for (int i = 0; i < 32; i++) { hex256[2 * i] = hx[mac[i] >> 4]; hex256[2 * i + 1] = hx[mac[i] & 15]; }
    CC_SHA512(hex256, 64, d512);
  }
  for (int i = 0; i < 64; i++) { hh[2 * i] = hx[d512[i] >> 4]; hh[2 * i + 1] = hx[d512[i] & 15]; }
  memcpy(hh + 128, hh, 128);
  hh[256] = 0;
  sort_rotations(hh, ord);
}

static int cmpint(const void *a, const void *b) { return *(const int *)a - *(const int *)b; }

static void *worker(void *arg) {
  Acc *a = arg;
  uint64_t rs = 0x5EED2026110500ULL + a->start;   // control arm PRNG seed
  int ord[52];
  for (uint64_t t = 0; t < a->n; t++) {
    if (a->arm == 0) bc_order(a->start + t, ord);
    else {
      for (int i = 0; i < 52; i++) ord[i] = i;
      for (int i = 51; i > 0; i--) {
        uint64_t r = splitmix(&rs) % (uint64_t)(i + 1);   // modulo bias ~1e-17, negligible
        int tmp = ord[i]; ord[i] = ord[r]; ord[r] = tmp;
      }
    }
    // co-occurrence + neighbour count in first five
    int nb = 0;
    for (int i = 0; i < 5; i++) for (int j = i + 1; j < 5; j++) {
      int p = ord[i], q = ord[j];
      if (p > q) { int x = p; p = q; q = x; }
      a->pair[p][q]++;
      if (q - p == 1) nb++;
    }
    a->nb_sum += nb; a->nb_sq += (double)nb * nb;
    int hand[5], sorted[5];
    for (int i = 0; i < 5; i++) hand[i] = sorted[i] = POS2ID[ord[i]];
    qsort(sorted, 5, sizeof(int), cmpint);
    uint32_t hi = cidx(sorted, 5);
    a->cls[HCLASS[hi]]++;
    double ev = EVBEST[hi];
    a->ev_sum += ev; a->ev_sq += ev * ev;
    // full play: hold mask is over sorted ids; map back to dealt positions, refill left to right
    int m = BESTMASK[hi], fin[5], nxt = 5;
    for (int i = 0; i < 5; i++) {
      int keep = 0;
      for (int s = 0; s < 5; s++) if ((m >> s & 1) && sorted[s] == hand[i]) keep = 1;
      fin[i] = keep ? hand[i] : POS2ID[ord[POSITIONAL ? 5 + i : nxt++]];
      (void)nxt;
    }
    qsort(fin, 5, sizeof(int), cmpint);
    int fc = classify(fin);
    a->final_cls[fc]++;
    double pay = PAY[fc];
    a->pl_sum += pay; a->pl_sq += pay * pay;
  }
  return NULL;
}

static void run_arm(int arm, uint64_t n, int nthreads, Acc *tot) {
  Acc *acc = calloc(nthreads, sizeof(Acc));
  pthread_t *th = malloc(nthreads * sizeof(pthread_t));
  uint64_t per = n / nthreads;
  for (int i = 0; i < nthreads; i++) {
    acc[i].arm = arm; acc[i].start = i * per; acc[i].n = (i == nthreads - 1) ? n - i * per : per;
    pthread_create(&th[i], NULL, worker, &acc[i]);
  }
  memset(tot, 0, sizeof(Acc));
  for (int i = 0; i < nthreads; i++) {
    pthread_join(th[i], NULL);
    for (int p = 0; p < 52; p++) for (int q = 0; q < 52; q++) tot->pair[p][q] += acc[i].pair[p][q];
    for (int k = 0; k < 10; k++) { tot->cls[k] += acc[i].cls[k]; tot->final_cls[k] += acc[i].final_cls[k]; }
    tot->nb_sum += acc[i].nb_sum; tot->nb_sq += acc[i].nb_sq;
    tot->ev_sum += acc[i].ev_sum; tot->ev_sq += acc[i].ev_sq;
    tot->pl_sum += acc[i].pl_sum; tot->pl_sq += acc[i].pl_sq;
  }
  tot->n = n; tot->arm = arm;
  free(acc); free(th);
}

static void mean_se(double s, double sq, uint64_t n, double *m, double *se) {
  *m = s / n;
  double var = (sq / n - (*m) * (*m)) * n / (n - 1.0);
  *se = sqrt(var / n);
}

int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage: %s n threads outdir\n", argv[0]); return 1; }
  uint64_t n = strtoull(argv[1], 0, 10);
  int nth = atoi(argv[2]);
  const char *outdir = argv[3];
  init_binom();
  if (getenv("PAYTABLE")) { char *e = strdup(getenv("PAYTABLE")), *tok = strtok(e, ","); for (int k = 1; k < 10 && tok; k++, tok = strtok(NULL, ",")) PAY[k] = atof(tok); }
  if (getenv("VP_DECK") && !strcmp(getenv("VP_DECK"), "suit")) { int k = 0; for (int s = 10; s <= 13; s++) for (int r = 1; r <= 13; r++) ALL_CARDS[k++] = s * 16 + r; }
  if (getenv("VP_HASH") && !strcmp(getenv("VP_HASH"), "hmac512")) HASH512 = 1;
  if (getenv("VP_HASH") && !strcmp(getenv("VP_HASH"), "plain2019")) HASHPLAIN = 1;
  if (getenv("VP_DRAW") && !strcmp(getenv("VP_DRAW"), "positional")) POSITIONAL = 1;
  if (getenv("VP_SERVER") && *getenv("VP_SERVER")) SERVER = getenv("VP_SERVER");
  int narms = getenv("VP_ARMS") ? atoi(getenv("VP_ARMS")) : 2;
  printf("VARIANT deck=%s hash=%s draw=%s arms=%d\n", getenv("VP_DECK") && !strcmp(getenv("VP_DECK"), "suit") ? "suit" : "scrambled",
         HASHPLAIN ? "plain2019" : HASH512 ? "hmac512" : "verifier", POSITIONAL ? "positional" : "sequential", narms);
  int seen[52] = {0};
  for (int i = 0; i < 52; i++) { POS2ID[i] = code2id(ALL_CARDS[i]); seen[POS2ID[i]]++; }
  for (int i = 0; i < 52; i++) if (seen[i] != 1) { fprintf(stderr, "ALL_CARDS is not a 52-card deck\n"); return 1; }
  printf("ALL_CARDS check: 52 distinct cards, each suit/rank exactly once\n");
  if (n == 0) {   // cross-check mode: first 10 card codes for nonces VP_NONCE0..VP_NONCE0+4 (default 0..4), for checks/parity.py
    int ord[52];
    uint64_t n0 = getenv("VP_NONCE0") ? strtoull(getenv("VP_NONCE0"), NULL, 10) : 0;
    for (uint64_t nc = n0; nc < n0 + 5; nc++) {
      bc_order(nc, ord);
      printf("%s\t%s\t%llu\t", SERVER, CLIENT, (unsigned long long)nc);
      for (int i = 0; i < 10; i++) printf("%s%d", i ? "," : "", ALL_CARDS[ord[i]]);
      printf("\n");
    }
    return 0;
  }

  double exact; uint64_t cc[10];
  build_tables(&exact, cc);
  printf("\n== Exact, uniform deck, optimal hold (full enumeration of %d deals x 32 holds)\n", NH);
  printf("paytable {JoB,2P,3K,S,F,FH,4K,SF,RF} = {%g,%g,%g,%g,%g,%g,%g,%g,%g}\n", PAY[1], PAY[2], PAY[3], PAY[4], PAY[5], PAY[6], PAY[7], PAY[8], PAY[9]);
  printf("EXACT_OPTIMAL_RTP %.10f\n", exact);
  double ev_deal_var = 0;
  { double s = 0, sq = 0; for (int i = 0; i < NH; i++) { s += EVBEST[i]; sq += (double)EVBEST[i] * EVBEST[i]; }
    ev_deal_var = sq / NH - (s / NH) * (s / NH);
    printf("EXACT_OPTIMAL_RTP_float_table %.10f   sd(optimal EV of dealt hand) %.6f\n", s / NH, sqrt(ev_deal_var)); }
  printf("initial-hand class counts (of %d):\n", NH);
  for (int k = 0; k < 10; k++) printf("  %-18s %8llu  p=%.10f\n", CLASS_NAME[k], (unsigned long long)cc[k], (double)cc[k] / NH);

  char path[1024];
  for (int arm = 0; arm < narms; arm++) {
    Acc *A = calloc(1, sizeof(Acc));
    run_arm(arm, n, nth, A);
    const char *nm = arm == 0 ? "BC_VERIFIER_SHUFFLE" : "UNIFORM_CONTROL";
    char armdesc[256];
    if (arm == 0) snprintf(armdesc, sizeof armdesc, " (server='%s', client='%s', nonce 0..n-1)", SERVER, CLIENT);
    else snprintf(armdesc, sizeof armdesc, " (splitmix64 Fisher-Yates, seed 0x5EED2026110500 + thread start)");
    printf("\n== Simulation arm: %s, n = %llu deals%s\n", nm, (unsigned long long)n, armdesc);
    double pexp = 20.0 / 2652.0;   // P(two given cards both in first 5)
    double m, se;
    mean_se(A->nb_sum, A->nb_sq, n, &m, &se);
    double nbexp = 51 * pexp;
    printf("neighbour pairs per deal (list positions |i-j|=1): mean %.6f SE %.6f expected %.6f ratio %.4f  z=%.1f\n",
           m, se, nbexp, m / nbexp, (m - nbexp) / se);
    // by distance d
    printf("co-occurrence ratio observed/uniform by list distance d (pairs aggregated over all i<j with j-i=d):\n");
    for (int d = 1; d <= 51; d++) {
      uint64_t cnt = 0; int np = 0;
      for (int p = 0; p + d < 52; p++) { cnt += A->pair[p][p + d]; np++; }
      double e = (double)n * np * pexp;
      double sd = sqrt((double)n * np * pexp * (1 - pexp));   // binomial approx per pair, summed (ignores covariance)
      if (d <= 8 || d % 10 == 0 || d >= 49)
        printf("  d=%2d pairs=%2d observed %12llu expected %14.1f ratio %.4f  z~%.1f\n", d, np,
               (unsigned long long)cnt, e, cnt / e, (cnt - e) / sd);
    }
    // max/min single pair
    double mx = 0, mn = 1e9; int mxp = 0, mxq = 0, mnp = 0, mnq = 0;
    for (int p = 0; p < 52; p++) for (int q = p + 1; q < 52; q++) {
      double r = A->pair[p][q] / (n * pexp);
      if (r > mx) { mx = r; mxp = p; mxq = q; }
      if (r < mn) { mn = r; mnp = p; mnq = q; }
    }
    printf("single-pair ratio range: max %.4f (pos %d,%d) min %.4f (pos %d,%d); per-pair binomial SE of ratio %.4f\n",
           mx, mxp, mxq, mn, mnp, mnq, sqrt((1 - pexp) / (n * pexp)));
    printf("initial-hand class frequency vs exact:\n");
    for (int k = 0; k < 10; k++) {
      double p0 = (double)cc[k] / NH, ph = (double)A->cls[k] / n, s = sqrt(p0 * (1 - p0) / n);
      printf("  %-18s observed %.8f exact %.8f ratio %.4f  z=%+.1f  (count %llu)\n", CLASS_NAME[k], ph, p0, ph / p0,
             (ph - p0) / s, (unsigned long long)A->cls[k]);
    }
    mean_se(A->ev_sum, A->ev_sq, n, &m, &se);
    printf("DEAL_ONLY_RTP (optimal uniform-deck hold EV of the dealt hand, uniform draws): %.6f SE %.6f  delta vs exact %+.4f pt (%.1f SE)\n",
           m, se, 100 * (m - exact), (m - exact) / se);
    mean_se(A->pl_sum, A->pl_sq, n, &m, &se);
    printf("FULL_PLAY_RTP (uniform-optimal hold, draws = shuffled cards 6..10 left to right): %.6f SE %.6f  delta vs exact %+.4f pt (%.1f SE)\n",
           m, se, 100 * (m - exact), (m - exact) / se);
    printf("final-hand class frequency:\n");
    for (int k = 0; k < 10; k++) printf("  %-18s %.8f\n", CLASS_NAME[k], (double)A->final_cls[k] / n);
    snprintf(path, sizeof path, "%s/pair_matrix_%s.csv", outdir, nm);
    FILE *f = fopen(path, "w");
    for (int p = 0; p < 52; p++) { for (int q = 0; q < 52; q++) fprintf(f, "%s%llu", q ? "," : "", (unsigned long long)(p < q ? A->pair[p][q] : A->pair[q][p])); fprintf(f, "\n"); }
    fclose(f);
    fflush(stdout);
    free(A);
  }
  return 0;
}
