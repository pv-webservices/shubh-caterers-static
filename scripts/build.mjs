// Copies only the files the live site needs into dist/ (Netlify's publish dir).
// Keeps public/ (source videos), the Python generator and caches out of the deploy.
import { cpSync, existsSync, mkdirSync, readdirSync, rmSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const dist = join(root, 'dist');

const rootFiles = readdirSync(root).filter((name) => name.endsWith('.html'));
const staticFiles = ['robots.txt', 'sitemap.xml'];
const staticDirs = ['assets', 'services'];

rmSync(dist, { recursive: true, force: true });
mkdirSync(dist, { recursive: true });

for (const name of [...rootFiles, ...staticFiles]) {
  if (!existsSync(join(root, name))) {
    throw new Error(`Missing required file: ${name}`);
  }
  cpSync(join(root, name), join(dist, name));
}

for (const name of staticDirs) {
  if (!existsSync(join(root, name))) {
    throw new Error(`Missing required folder: ${name}/`);
  }
  cpSync(join(root, name), join(dist, name), { recursive: true });
}

console.log(`Built dist/ with ${rootFiles.length} pages, ${staticDirs.join(', ')} and ${staticFiles.join(', ')}`);
