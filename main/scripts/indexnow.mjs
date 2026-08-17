#!/usr/bin/env node
// Ping IndexNow so Bing, Yandex, Seznam and Naver recrawl on demand.
//
// Google does not participate — it only reads the sitemap. But Bing powers
// ChatGPT's web search and Copilot, which is the real reason to bother.
//
// Beats the Bing Webmaster dashboard: no login, no account, no OAuth. The key
// file proves ownership, so this keeps working forever from a script.
//
// Usage:
//   node scripts/indexnow.mjs                    # submit everything in the sitemap
//   node scripts/indexnow.mjs https://…/archive/ # submit specific URLs
//
// Success is 200 or 202. A 403 means the key file is missing or unreachable —
// which is why this verifies the key resolves BEFORE posting.

import dns from 'node:dns';

// api.indexnow.org advertises AAAA records this network cannot reach, and Node
// prefers IPv6 by default, so the POST died with EHOSTUNREACH before it left
// the machine. Resolve v4 first.
dns.setDefaultResultOrder('ipv4first');

const KEY = '6e44782f9c75395b6ae2b9e7c044b202';
const HOST = 'asadchattha.com';
const KEY_LOCATION = `https://${HOST}/${KEY}.txt`;
const ENDPOINT = 'https://api.indexnow.org/indexnow';

// Every URL in one batch must share the host above, or the whole batch is
// rejected. The vN subdomains are different hosts, so they go in their own runs.
const DEFAULT_URLS = [
  `https://${HOST}/`,
  `https://${HOST}/archive/`,
];

async function verifyKey() {
  const res = await fetch(KEY_LOCATION);
  if (!res.ok) throw new Error(`key file ${KEY_LOCATION} returned ${res.status}`);
  const body = (await res.text()).trim();
  if (body !== KEY) throw new Error(`key file content mismatch: got "${body.slice(0, 40)}"`);
  console.log(`key file OK  ${KEY_LOCATION}`);
}

async function submit(host, urlList) {
  const res = await fetch(ENDPOINT, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
    body: JSON.stringify({ host, key: KEY, keyLocation: KEY_LOCATION, urlList }),
  });
  const ok = res.status === 200 || res.status === 202;
  console.log(`${ok ? 'accepted' : 'REJECTED'}  ${res.status}  ${host}  (${urlList.length} url${urlList.length > 1 ? 's' : ''})`);
  urlList.forEach((u) => console.log(`   ${u}`));
  if (!ok) console.log(`   body: ${(await res.text()).slice(0, 200)}`);
  return ok;
}

const args = process.argv.slice(2);
const urls = args.length ? args : DEFAULT_URLS;

await verifyKey();

// Group by host so a subdomain never poisons the apex batch.
const byHost = new Map();
for (const u of urls) {
  const h = new URL(u).host;
  byHost.set(h, [...(byHost.get(h) || []), u]);
}

let allOk = true;
for (const [host, list] of byHost) {
  if (!(await submit(host, list))) allOk = false;
}
process.exit(allOk ? 0 : 1);
