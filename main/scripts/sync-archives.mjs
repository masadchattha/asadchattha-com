// Copies each archived version into main/public so the ONE Netlify project
// ships every version. archives/vN stays the source you edit; main/public/vN
// is a build artifact and is gitignored.
//
// Runs automatically as npm `prebuild`, so both `npm run build` locally and
// Netlify's build get the same tree.
//
// Result: asadchattha.com/v1, /v2, /v3 — and, once the DNS aliases exist,
// v1.asadchattha.com rewrites onto /v1 via the redirects in netlify.toml.

import { cp, rm, readdir, stat } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, relative, sep } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const repo = join(here, '..', '..');
const archivesDir = join(repo, 'archives');
const publicDir = join(repo, 'main', 'public');

// Working files that belong in the repo but must never reach the CDN:
// img/src is the un-keyed mockup source (5.6 MB across v1 and v2), tools are
// the Python card builders, and each archive's own netlify.toml is a leftover
// from when these deployed as separate sites.
const EXCLUDE_TOP = new Set(['tools', 'README.md', 'netlify.toml']);

// Returns true to copy. Note img/src is dropped by path, not by name, so a
// legitimate top-level src/ in some future version would still ship.
const keep = (srcRoot) => (src) => {
  const rel = relative(srcRoot, src);
  if (!rel) return true; // the version directory itself
  const parts = rel.split(sep);
  const name = parts[parts.length - 1];

  if (name === '.DS_Store') return false;
  if (parts[0] === 'img' && parts[1] === 'src') return false;
  if (parts.length === 1 && EXCLUDE_TOP.has(name)) return false;
  return true;
};

const versions = existsSync(archivesDir)
  ? (await readdir(archivesDir)).filter((n) => /^v\d+$/.test(n)).sort()
  : [];

if (!versions.length) {
  console.log('sync-archives: nothing in archives/, skipping');
}

for (const v of versions) {
  const from = join(archivesDir, v);
  if (!(await stat(from)).isDirectory()) continue;
  if (!existsSync(join(from, 'index.html'))) {
    console.log(`sync-archives: ${v} has no index.html, skipping`);
    continue;
  }

  const to = join(publicDir, v);
  await rm(to, { recursive: true, force: true });
  await cp(from, to, { recursive: true, filter: keep(from) });
  console.log(`sync-archives: archives/${v} -> public/${v}`);
}
