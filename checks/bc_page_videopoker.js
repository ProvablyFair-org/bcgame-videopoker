// Independent cross-check of bcvp.py against the published verifier pages' code, run VERBATIM in a node vm
// (inline <script> of each historical videopoker.html + lib/crypto-js.js as downloaded).
//
//   mode "asis"     : the page's own result_hash
//   mode "hmac512"  : the page's own deck + rotate/sort code, with result_hash replaced by
//                     CryptoJS.HmacSHA512(client_seed + ":" + nonce, server_seed)  (the fairness-text hash)
//
// usage: node js_crosscheck.js <videopoker.html> <crypto-js.js> <asis|hmac512> < cases.tsv
// prints: server \t client \t nonce \t hash \t first-10 codes
const fs = require('fs');
const vm = require('vm');
const [htmlPath, cjsPath, mode] = process.argv.slice(2);
const html = fs.readFileSync(htmlPath, 'utf8');
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
if (scripts.length !== 1) throw new Error('expected exactly one inline script, got ' + scripts.length);
const sandbox = { console };
sandbox.window = sandbox;
sandbox.parseInt = parseInt;
vm.createContext(sandbox);
vm.runInContext(fs.readFileSync(cjsPath, 'utf8'), sandbox);
// 2019/2020 pages call a global queryString(); 2021 calls tools.queryString()
vm.runInContext('var tools={queryString:function(){return {}}}; function queryString(){return {}};' +
  'var ga=function(){}; var __opts=null; function Vue(o){__opts=o;}', sandbox);
vm.runInContext(scripts[0], sandbox);
const opts = sandbox.__opts;

function cardsFor(server, client, nonce) {
  const self = {};
  const data = typeof opts.data === 'function' ? opts.data() : opts.data;
  Object.assign(self, JSON.parse(JSON.stringify(data)));
  self.client_seed = client; self.server_seed = server; self.nonce = nonce;
  for (const [k, f] of Object.entries(opts.methods)) self[k] = f.bind(self);
  opts.created.call(self);
  const computed = Object.assign({}, opts.computed);
  if (mode === 'hmac512') {
    computed.result_hash = function () {
      return sandbox.CryptoJS.HmacSHA512(this.client_seed + ':' + this.nonce, this.server_seed);
    };
  } else if (mode !== 'asis') throw new Error('mode must be asis or hmac512');
  for (const [k, f] of Object.entries(computed))
    Object.defineProperty(self, k, { get: () => f.call(self) });
  return { hash: String(self.result_hash), cards: self.card_list.map(c => c.card) };
}

const lines = fs.readFileSync(0, 'utf8').split('\n').filter(Boolean);
for (const l of lines) {
  const [s, c, n] = l.split('\t');
  const r = cardsFor(s, c, parseInt(n));
  console.log([s, c, n, r.hash, r.cards.join(',')].join('\t'));
}
