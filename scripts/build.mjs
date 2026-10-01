// Builds the deployable site into dist/ (Netlify's publish directory).
//  - pages/  -> dist/            generated HTML (run `npm run generate` after editing generator/)
//  - static/ -> dist/            favicons + web manifest at the site root
//  - assets/ -> dist/assets/     fonts, images, video (masters in source-files/ are never deployed)
//  - CSS + JS are bundled, minified and fingerprinted into dist/assets/build/ (cached for a year)
//  - sitemap.xml, sitemap-index.xml, robots.txt and _redirects are generated from the built pages
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { cpSync, existsSync, mkdirSync, readdirSync, readFileSync, rmSync, statSync, writeFileSync } from 'node:fs';
import { dirname, join, relative, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { build } from 'esbuild';

export const SITE = 'https://shubhcaterers.in';
const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const dist = join(root, 'dist');
const LEGACY_HTML_PAGES = ['about', 'services', 'menu', 'gallery', 'testimonials', 'contact', 'faq', 'privacy'];

const walk = (dir) => readdirSync(dir, { withFileTypes: true })
  .flatMap((d) => (d.isDirectory() ? walk(join(dir, d.name)) : [join(dir, d.name)]));
const toPosix = (p) => p.split(sep).join('/');
const hashOf = (text) => createHash('sha256').update(text).digest('hex').slice(0, 10);

/** Public URL path of a built HTML file: dist/about/index.html -> /about/ */
export function urlPathOf(file, base = dist) {
  const rel = toPosix(relative(base, file));
  if (rel === 'index.html') return '/';
  if (rel.endsWith('/index.html')) return `/${rel.slice(0, -'index.html'.length)}`;
  return `/${rel}`;
}

function lastModified(sourceFile) {
  try {
    const out = execFileSync('git', ['log', '-1', '--format=%cs', '--', sourceFile], { cwd: root, encoding: 'utf8' }).trim();
    if (out) return out;
  } catch { /* not a git checkout */ }
  return new Date().toISOString().slice(0, 10);
}

async function bundle(entry, name, ext, options) {
  const result = await build({ entryPoints: [join(root, entry)], bundle: true, minify: true, write: false, logLevel: 'warning', ...options });
  const code = result.outputFiles[0].text;
  const file = `${name}.${hashOf(code)}.${ext}`;
  writeFileSync(join(dist, 'assets', 'build', file), code);
  return `/assets/build/${file}`;
}

async function main() {
  for (const dir of ['pages', 'static', 'assets/images', 'assets/fonts', 'assets/video']) {
    if (!existsSync(join(root, dir))) throw new Error(`Missing required folder: ${dir}/ (run npm run generate)`);
  }
  rmSync(dist, { recursive: true, force: true });
  mkdirSync(join(dist, 'assets', 'build'), { recursive: true });

  cpSync(join(root, 'pages'), dist, { recursive: true });
  cpSync(join(root, 'static'), dist, { recursive: true });
  for (const dir of ['fonts', 'images', 'video']) {
    cpSync(join(root, 'assets', dir), join(dist, 'assets', dir), { recursive: true, filter: (src) => !src.endsWith('manifest.json') });
  }

  const css = await bundle('assets/css/site.css', 'site', 'css', { external: ['/assets/fonts/*'] });
  const js = await bundle('assets/js/main.js', 'main', 'js', { format: 'iife', target: 'es2019' });

  const pages = walk(dist).filter((f) => f.endsWith('.html'));
  const indexable = [];
  for (const file of pages) {
    const html = readFileSync(file, 'utf8');
    if (!html.includes('/assets/css/site.css') || !html.includes('/assets/js/main.js')) throw new Error(`${file} is missing the stylesheet or script tag`);
    writeFileSync(file, html.replace('/assets/css/site.css', css).replace('/assets/js/main.js', js));
    if (!/<meta name="robots" content="[^"]*noindex/.test(html)) {
      const source = join(root, 'pages', relative(dist, file));
      indexable.push({ loc: SITE + urlPathOf(file), lastmod: lastModified(source) });
    }
  }
  indexable.sort((a, b) => (a.loc.length - b.loc.length) || a.loc.localeCompare(b.loc));

  const newest = indexable.map((p) => p.lastmod).sort().at(-1);
  writeFileSync(join(dist, 'sitemap.xml'), '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + indexable.map((p) => `  <url><loc>${p.loc}</loc><lastmod>${p.lastmod}</lastmod></url>\n`).join('') + '</urlset>\n');
  writeFileSync(join(dist, 'sitemap-index.xml'), '<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + `  <sitemap><loc>${SITE}/sitemap.xml</loc><lastmod>${newest}</lastmod></sitemap>\n</sitemapindex>\n`);
  writeFileSync(join(dist, 'robots.txt'), `User-agent: *\nAllow: /\n\nSitemap: ${SITE}/sitemap-index.xml\n`);

  // Old *.html URLs (before 2026-10) and index.html duplicates -> the clean trailing-slash URL.
  const services = readdirSync(join(root, 'pages', 'services'), { withFileTypes: true }).filter((d) => d.isDirectory()).map((d) => d.name);
  const redirects = [
    '# Generated by scripts/build.mjs — edit there, not here.',
    `https://www.shubhcaterers.in/*  ${SITE}/:splat  301!`,
    '/index.html  /  301!',
    ...LEGACY_HTML_PAGES.flatMap((p) => [`/${p}.html  /${p}/  301!`, `/${p}/index.html  /${p}/  301!`]),
    ...services.flatMap((s) => [`/services/${s}.html  /services/${s}/  301!`, `/services/${s}/index.html  /services/${s}/  301!`]),
    '/thank-you/index.html  /thank-you/  301!',
  ];
  writeFileSync(join(dist, '_redirects'), redirects.join('\n') + '\n');

  const bytes = walk(dist).reduce((sum, f) => sum + statSync(f).size, 0);
  console.log(`Built dist/: ${pages.length} pages (${indexable.length} in sitemap), ${css}, ${js}, ${redirects.length - 1} redirects, ${(bytes / 1048576).toFixed(1)} MB`);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main().catch((err) => { console.error(err); process.exit(1); });
}
