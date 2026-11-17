// Reads GitHub's own records in verifier/github/receipt.json again, online: who owns the repository that holds BC's
// video poker verifier, the pushes GH Archive logged when they happened, and forks of the repository with their dates.
// Every line prints PASS or FAIL.
//
//   node checks/check_verifier_history_online.js        (Node 18+)
//
// Or paste this file into the browser console on https://data.gharchive.org/ (GH Archive allows reading its files
// only from its own pages; GitHub's API allows any page). In the browser the receipt is read from the published
// repository unless RECEIPT is set first.
//
// Downloads four GH Archive hour files (about 50 MB each, stopping once the event is found) and makes 18
// unauthenticated GitHub API calls (GitHub allows 60 an hour). Forks and accounts can change after 17 Nov 2026; a FAIL
// on them means GitHub's data changed, and the receipt keeps what it showed that day.
(async () => {
  const isNode = typeof process !== "undefined" && !!(process.versions && process.versions.node);
  const env = isNode ? process.env : {};
  const GHA = env.GHA_BASE || "https://data.gharchive.org";
  const API = env.API_BASE || "https://api.github.com";
  const RAW = env.RAW_BASE || "https://raw.githubusercontent.com";
  const fails = [];
  const check = (label, ok, detail) => {
    console.log((ok ? "PASS  " : "FAIL  ") + label + (detail ? "   " + detail : ""));
    if (!ok) fails.push(label);
  };

  let receipt = globalThis.RECEIPT;
  if (!receipt && isNode) {
    const fs = require("fs"), path = require("path");
    receipt = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "verifier", "github", "receipt.json"), "utf8"));
  }
  if (!receipt) {
    receipt = await (await fetch(RAW + "/ProvablyFair-org/bcgame-videopoker/HEAD/verifier/github/receipt.json")).json();
  }

  const getJSON = async (url) => {
    const r = await fetch(url, { headers: { Accept: "application/vnd.github+json" } });
    if (!r.ok) throw new Error(url + " -> HTTP " + r.status);
    return r.json();
  };
  const sha256 = async (buf) => {
    if (isNode) return require("crypto").createHash("sha256").update(Buffer.from(buf)).digest("hex");
    const d = await crypto.subtle.digest("SHA-256", buf);
    return Array.from(new Uint8Array(d), (b) => b.toString(16).padStart(2, "0")).join("");
  };
  // Finds the GH Archive line with this event id; reads the hour file only as far as that line.
  const findEvent = async (url, id) => {
    const needle = '"id":"' + id + '"';
    const r = await fetch(url);
    if (!r.ok) throw new Error(url + " -> HTTP " + r.status);
    if (isNode) {
      const { Readable } = require("stream");
      const zlib = require("zlib"), readline = require("readline");
      const gunzip = Readable.fromWeb(r.body).pipe(zlib.createGunzip());
      const rl = readline.createInterface({ input: gunzip, crlfDelay: Infinity });
      for await (const line of rl) {
        if (line.includes(needle)) { rl.close(); gunzip.destroy(); return JSON.parse(line); }
      }
      return null;
    }
    const reader = r.body.pipeThrough(new DecompressionStream("gzip")).pipeThrough(new TextDecoderStream()).getReader();
    let buf = "";
    for (;;) {
      const { value, done } = await reader.read();
      if (done) return null;
      buf += value;
      let i;
      while ((i = buf.indexOf("\n")) >= 0) {
        const line = buf.slice(0, i);
        buf = buf.slice(i + 1);
        if (line.includes(needle)) { await reader.cancel(); return JSON.parse(line); }
      }
    }
  };
  const seconds = (a, b) => (Date.parse(a) - Date.parse(b)) / 1000;

  const repo = receipt.repository, owner = receipt.owner, link = receipt.bc_forum_github_link;
  const acct = receipt.pushing_account, succ = receipt.successor;
  try {
    console.log("\nthe repository and who owns it\n");
    const rj = await getJSON(API + "/repositories/" + repo.id);
    check("repository " + repo.id + " is " + repo.name + ", created " + repo.created_at + ", archived",
      rj.full_name === repo.name && rj.created_at === repo.created_at && rj.archived === repo.archived && rj.owner.id === owner.id);
    const oj = await getJSON(API + "/organizations/" + owner.id);
    check("its owner, account " + owner.id + ", is " + owner.login + " (created " + owner.created_at + ")",
      oj.login === owner.login && oj.created_at === owner.created_at);
    const fj = await getJSON(API + "/repos/BCSNProject/bcgame-crash");
    check("BC's forum link " + link.url + " now serves " + link.github_now_serves + ", owned by the same account",
      fj.id === link.repository_id && fj.full_name === link.github_now_serves && fj.owner.id === owner.id);
    const aj = await getJSON(API + "/user/" + acct.id);
    check("the pushing account " + acct.id + " is " + acct.login + ", website " + acct.website,
      aj.login === acct.login && aj.blog === acct.website && aj.created_at === acct.created_at);
    const sj = await getJSON(API + "/repos/" + succ.name);
    check(succ.name + " was created " + succ.created_at, sj.created_at === succ.created_at);

    console.log("\npushes GH Archive logged as they happened\n");
    for (const e of receipt.push_events) {
      const ev = await findEvent(e.gharchive_file.replace("https://data.gharchive.org", GHA), e.event_id);
      const ok = !!ev && ev.type === "PushEvent" && ev.created_at === e.created_at && ev.repo.id === repo.id &&
        ev.repo.name === repo.name_in_2019_2020_events && ev.org && ev.org.id === owner.id && ev.actor.id === acct.id &&
        ev.actor.login === acct.login_in_2019_2020_events && ev.payload.before === e.before && ev.payload.head === e.head;
      check(e.created_at + " push " + e.before.slice(0, 7) + " -> " + e.head.slice(0, 7) + " (" + e.what + ")", ok,
        "event " + e.event_id + ", " + e.gharchive_file.split("/").pop());
      const cj = await getJSON(API + "/repos/" + repo.name + "/commits/" + e.head);
      const d = seconds(e.created_at, cj.commit.committer.date);
      check("  pushed " + d + " s after its commit", cj.commit.committer.date === e.head_commit_date && d >= 0 && d <= 60);
    }

    console.log("\nforks, with the date GitHub gave them and the video poker page they hold\n");
    for (const f of receipt.forks) {
      const base = API + "/repositories/" + f.repository_id;
      const pj = await getJSON(base);
      const bj = await getJSON(base + "/branches/" + f.branch);
      const cj = await getJSON(base + "/contents/videopoker.html?ref=" + f.head);
      const bytes = isNode ? Buffer.from(cj.content, "base64") : Uint8Array.from(atob(cj.content.replace(/\s/g, "")), (c) => c.charCodeAt(0));
      const h = await sha256(bytes);
      check("fork " + f.repository_id + ", made " + f.created_at + ": head " + f.head.slice(0, 7) + ", videopoker.html " + f.videopoker_html_sha256.slice(0, 12),
        pj.fork === true && pj.created_at === f.created_at && pj.parent && pj.parent.id === repo.id &&
        bj.commit.sha === f.head && h === f.videopoker_html_sha256);
    }
  } catch (err) {
    check("reading GitHub and GH Archive", false, String(err));
  }
  console.log(fails.length ? "\n" + fails.length + " check(s) failed" : "\nall checks passed");
  if (isNode && fails.length) process.exitCode = 1;
  return fails.length ? "FAIL: " + fails.join("; ") : "all checks passed";
})();
