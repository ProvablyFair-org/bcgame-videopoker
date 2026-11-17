// Runs BC's own baccarat verifier code beside our rebuild's inputs.
// The page (baccaratsingle.html) is a React/JSX page, so it cannot run as a whole in node. Two pieces of its inline
// script are cut out BY POSITION, unedited, and executed in a node vm with the page's own lib/crypto-js.js and lib/tools.js:
//   A. from "const allNums" up to "function BaccaratSingle"  (createCards, create, canBankerGetCard, getPoint,
//      getRestlt, createCardFram, encode)
//   B. the body of the page's useMemo callback, from "const serverSeedHash" up to its "return {"
// The React component, its inputs and the rendering are NOT executed. `state` is supplied with the three inputs.
// usage: node js_crosscheck_baccarat.js <baccaratsingle.html> <lib dir> < cases.tsv   (server \t client \t nonce)
// prints: server, client, nonce, hmac, the 104 card codes, player card values, banker card values, player total, banker total
// with --cards as a third argument (added 16 Nov 2026) two more columns follow: the player's and the banker's cards as the
// page would draw them, suit sign + rank text (the `suits` and `point` fields of the page's createCardFram), e.g. "♠A,♦10"
const fs = require('fs'), vm = require('vm'), path = require('path');
const [htmlPath, libDir, flag] = process.argv.slice(2);
const html = fs.readFileSync(htmlPath, 'utf8');
const cut = (a, b) => { const i = html.indexOf(a), j = html.indexOf(b, i); if (i < 0 || j < 0) throw new Error('marker not found: ' + a + ' / ' + b); return html.slice(i, j); };
const partA = cut('const allNums', 'function BaccaratSingle');
const partB = cut('const serverSeedHash', 'return {\n          player,');
const sb = { console }; sb.window = sb; sb.location = { search: '' };
vm.createContext(sb);
vm.runInContext(fs.readFileSync(path.join(libDir, 'crypto-js.js'), 'utf8'), sb);
vm.runInContext(fs.readFileSync(path.join(libDir, 'tools.js'), 'utf8'), sb);
vm.runInContext(partA + '\nfunction __run(state){' + partB +
  '\nreturn {hmacSha256Result, resultList, player, banker, playerPointFinal, bankerPointFinal};}', sb);
for (const l of fs.readFileSync(0, 'utf8').split('\n').filter(Boolean)) {
  const [s, c, n] = l.split('\t');
  const r = sb.__run({ serverSeed: s, clientSeed: c, nonce: n });
  console.log([s, c, n, r.hmacSha256Result, r.resultList.join(','), r.player.map(x => x.pointNum).join(','),
    r.banker.map(x => x.pointNum).join(','), r.playerPointFinal % 10, r.bankerPointFinal % 10]
    .concat(flag === '--cards' ? [r.player.map(x => x.suits + x.point).join(','), r.banker.map(x => x.suits + x.point).join(',')] : []).join('\t'));
}
