// Technical SEO audit of the built site in dist/.  Run: npm run build && npm run audit:seo
// Exits with code 1 when any issue is found.
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { dirname, join, relative, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parse } from 'node-html-parser';

const SITE = 'https://shubhcaterers.in';
const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const dist = join(root, 'dist');
const NOINDEX_REQUIRED = ['/404.html', '/thank-you/'];
const ROBOTS_INDEX = 'index, follow, max-image-preview:large';
const ROBOTS_NOINDEX = 'noindex, follow';
const TITLE_MAX = 65;
const DESC = { min: 70, max: 170 };
const REQUIRED_OG = ['og:site_name', 'og:locale', 'og:type', 'og:title', 'og:description', 'og:image', 'og:image:width', 'og:image:height', 'og:image:alt'];
const REQUIRED_TWITTER = ['twitter:card', 'twitter:title', 'twitter:description', 'twitter:image'];
const FAVICONS = ['/favicon.ico', '/favicon.svg', '/favicon-96x96.png', '/favicon-48x48.png', '/apple-touch-icon.png', '/site.webmanifest'];

const issues = [];
const report = (page, message) => issues.push(`${page}: ${message}`);

const walk = (dir) => readdirSync(dir, { withFileTypes: true }).flatMap((d) => (d.isDirectory() ? walk(join(dir, d.name)) : [join(dir, d.name)]));
const toPosix = (p) => p.split(sep).join('/');
function urlPathOf(file) {
  const rel = toPosix(relative(dist, file));
  if (rel === 'index.html') return '/';
  return rel.endsWith('/index.html') ? `/${rel.slice(0, -10)}` : `/${rel}`;
}

/** Resolves a root-relative URL path to a file in dist/, or null. */
function fileFor(path) {
  const clean = decodeURIComponent(path.split(/[?#]/)[0]);
  if (clean.endsWith('/')) return existsSync(join(dist, clean, 'index.html')) ? join(dist, clean, 'index.html') : null;
  return existsSync(join(dist, clean)) ? join(dist, clean) : null;
}

function jpegSize(file) {
  const b = readFileSync(file);
  for (let i = 2; i < b.length;) {
    if (b[i] !== 0xff) return null;
    const marker = b[i + 1];
    if (marker >= 0xc0 && marker <= 0xc3) return { height: b.readUInt16BE(i + 5), width: b.readUInt16BE(i + 7) };
    i += 2 + b.readUInt16BE(i + 2);
  }
  return null;
}

if (!existsSync(dist)) { console.error('dist/ not found — run npm run build first'); process.exit(1); }

const files = walk(dist).filter((f) => f.endsWith('.html'));
const pages = files.map((file) => {
  const html = readFileSync(file, 'utf8');
  return { file, path: urlPathOf(file), html, doc: parse(html, { comment: false }) };
});
const byPath = new Map(pages.map((p) => [p.path, p]));
const titles = new Map();
const descriptions = new Map();
const indexable = new Set();
let linksChecked = 0;
let imagesChecked = 0;

for (const page of pages) {
  const { doc, path, html } = page;
  const meta = (attr, key) => doc.querySelector(`meta[${attr}="${key}"]`)?.getAttribute('content');

  // URL style
  if (path !== '/404.html' && (!path.endsWith('/') || /[A-Z_ ]/.test(path))) report(path, 'URL should be lowercase, hyphenated and end with /');

  // Title + description
  const title = doc.querySelector('title')?.text.trim() || '';
  if (!title) report(path, 'missing <title>');
  else if (title.length > TITLE_MAX) report(path, `title is ${title.length} chars (max ${TITLE_MAX}): "${title}"`);
  const desc = meta('name', 'description') || '';
  if (!desc) report(path, 'missing meta description');
  else if (desc.length < DESC.min || desc.length > DESC.max) report(path, `description is ${desc.length} chars (want ${DESC.min}-${DESC.max})`);
  titles.set(title, [...(titles.get(title) || []), path]);
  descriptions.set(desc, [...(descriptions.get(desc) || []), path]);

  // Robots + canonical
  const robots = meta('name', 'robots');
  const canonicals = doc.querySelectorAll('link[rel="canonical"]');
  const isNoindex = (robots || '').includes('noindex');
  if (NOINDEX_REQUIRED.includes(path)) {
    if (robots !== ROBOTS_NOINDEX) report(path, `robots should be "${ROBOTS_NOINDEX}", is "${robots}"`);
  } else if (robots !== ROBOTS_INDEX) report(path, `robots should be "${ROBOTS_INDEX}", is "${robots}"`);
  if (isNoindex) {
    if (canonicals.length) report(path, 'noindex page must not have a canonical tag');
  } else {
    indexable.add(SITE + path);
    if (canonicals.length !== 1) report(path, `expected 1 canonical, found ${canonicals.length}`);
    else if (canonicals[0].getAttribute('href') !== SITE + path) report(path, `canonical ${canonicals[0].getAttribute('href')} is not self-referencing`);
    if (meta('property', 'og:url') !== SITE + path) report(path, 'og:url should equal the canonical URL');
  }

  // Headings
  const h1s = doc.querySelectorAll('h1');
  if (h1s.length !== 1) report(path, `expected exactly 1 <h1>, found ${h1s.length}`);
  let previous = 0;
  for (const h of doc.querySelectorAll('h1, h2, h3, h4, h5, h6')) {
    const level = Number(h.tagName[1]);
    if (previous && level > previous + 1) report(path, `heading level skipped: h${previous} -> h${level} ("${h.text.trim().slice(0, 40)}")`);
    previous = level;
  }

  // Images
  for (const img of doc.querySelectorAll('img')) {
    imagesChecked += 1;
    const src = img.getAttribute('src') || img.getAttribute('data-src') || '';
    if (img.getAttribute('alt') === undefined) report(path, `<img> without alt: ${src}`);
    else if (img.getAttribute('alt') === '' && !img.closest('.page-hero-media, [aria-hidden="true"]')) report(path, `empty alt on a content image: ${src}`);
    if (!img.getAttribute('width') || !img.getAttribute('height')) report(path, `<img> without width/height: ${src}`);
    if (/-(1200|1264|1376)\.(webp|avif)$/.test(src)) report(path, `img src uses the full-size file: ${src}`);
  }

  // Open Graph + Twitter
  for (const key of REQUIRED_OG) if (!meta('property', key)) report(path, `missing ${key}`);
  for (const key of REQUIRED_TWITTER) if (!meta('name', key)) report(path, `missing ${key}`);
  const ogImage = meta('property', 'og:image') || '';
  if (ogImage) {
    const file = ogImage.startsWith(SITE) ? fileFor(ogImage.slice(SITE.length)) : null;
    const size = file && file.endsWith('.jpg') ? jpegSize(file) : null;
    if (!file) report(path, `og:image not found in build: ${ogImage}`);
    else if (!size || size.width !== 1200 || size.height !== 630) report(path, `og:image is not 1200x630: ${ogImage}`);
  }
  if (meta('property', 'og:image:width') !== '1200' || meta('property', 'og:image:height') !== '630') report(path, 'og:image:width/height should be 1200/630');

  // Favicons
  for (const icon of FAVICONS) {
    if (!doc.querySelector(`link[href="${icon}"]`)) report(path, `missing <link> to ${icon}`);
  }

  // JSON-LD
  const scripts = doc.querySelectorAll('script[type="application/ld+json"]');
  if (scripts.length !== 1) report(path, `expected 1 JSON-LD block, found ${scripts.length}`);
  for (const s of scripts) {
    const raw = s.innerHTML;
    if (raw.includes('<')) report(path, 'JSON-LD contains an unescaped "<"');
    let graph = [];
    try { graph = JSON.parse(raw)['@graph'] || []; } catch { report(path, 'JSON-LD is not valid JSON'); continue; }
    const types = graph.map((n) => n['@type']);
    const org = graph.find((n) => n['@type'] === 'FoodEstablishment');
    if (!org) report(path, 'JSON-LD missing FoodEstablishment (LocalBusiness)');
    else for (const k of ['@id', 'name', 'url', 'logo', 'address', 'telephone']) if (!org[k]) report(path, `LocalBusiness missing ${k}`);
    if (!types.includes('WebSite')) report(path, 'JSON-LD missing WebSite');
    if (!types.includes('Person')) report(path, 'JSON-LD missing Person (founders)');
    if (!isNoindex && path !== '/' && !types.includes('BreadcrumbList')) report(path, 'inner page missing BreadcrumbList');
    if (doc.querySelector('.faq-list details') && !types.includes('FAQPage')) report(path, 'page has FAQs but no FAQPage schema');
    const crumbs = graph.find((n) => n['@type'] === 'BreadcrumbList');
    if (crumbs && crumbs.itemListElement.at(-1).item !== SITE + path) report(path, 'last breadcrumb is not this page');
  }

  // Internal links, fragments and assets
  const refs = [
    ...doc.querySelectorAll('a[href]').map((a) => ['link', a.getAttribute('href')]),
    ...doc.querySelectorAll('link[href]').map((l) => ['asset', l.getAttribute('href')]),
    ...doc.querySelectorAll('script[src], img[src], video[poster], source[data-src], [data-src], [data-poster]').flatMap((el) => [
      ['asset', el.getAttribute('src')], ['asset', el.getAttribute('poster')], ['asset', el.getAttribute('data-src')], ['asset', el.getAttribute('data-poster')]]),
    ...doc.querySelectorAll('[srcset], [data-srcset]').flatMap((el) => `${el.getAttribute('srcset') || ''},${el.getAttribute('data-srcset') || ''}`
      .split(',').map((s) => s.trim().split(/\s+/)[0]).filter(Boolean).map((u) => ['asset', u])),
  ].filter(([, href]) => href);
  for (const [kind, href] of refs) {
    if (href.startsWith('#')) {
      if (href.length > 1 && !doc.getElementById(href.slice(1))) report(path, `broken in-page anchor ${href}`);
      continue;
    }
    if (!href.startsWith('/') || href.startsWith('//')) continue;
    linksChecked += 1;
    const target = fileFor(href);
    if (!target) { report(path, `broken internal ${kind}: ${href}`); continue; }
    if (kind === 'link' && /\.html($|[?#])/.test(href) && href !== '/404.html') report(path, `link uses .html URL: ${href}`);
    const hash = href.split('#')[1];
    if (hash && target.endsWith('.html')) {
      const other = pages.find((p) => p.file === target);
      if (other && !other.doc.getElementById(hash)) report(path, `link ${href} points to a missing #${hash}`);
    }
  }
  if (/href="[^"]*\.example/.test(html)) report(path, 'placeholder .example URL found');
}

for (const [title, paths] of titles) if (paths.length > 1) report(paths.join(', '), `duplicate title "${title}"`);
for (const [desc, paths] of descriptions) if (paths.length > 1) report(paths.join(', '), `duplicate description "${desc.slice(0, 50)}…"`);
for (const path of NOINDEX_REQUIRED) if (!byPath.has(path)) report(path, 'required utility page is missing');

// Sitemap must list exactly the indexable pages
const sitemap = existsSync(join(dist, 'sitemap.xml')) ? readFileSync(join(dist, 'sitemap.xml'), 'utf8') : '';
const locs = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
const lastmods = [...sitemap.matchAll(/<lastmod>\d{4}-\d{2}-\d{2}<\/lastmod>/g)];
if (!sitemap) report('sitemap.xml', 'missing');
if (lastmods.length !== locs.length) report('sitemap.xml', 'every URL needs a lastmod');
for (const loc of locs) if (!indexable.has(loc)) report('sitemap.xml', `lists a non-indexable or missing page: ${loc}`);
for (const url of indexable) if (!locs.includes(url)) report('sitemap.xml', `missing indexable page: ${url}`);
const index = existsSync(join(dist, 'sitemap-index.xml')) ? readFileSync(join(dist, 'sitemap-index.xml'), 'utf8') : '';
if (!index.includes(`<loc>${SITE}/sitemap.xml</loc>`)) report('sitemap-index.xml', 'must reference sitemap.xml');

// robots.txt: allow everything, point to the sitemap index
const robotsTxt = existsSync(join(dist, 'robots.txt')) ? readFileSync(join(dist, 'robots.txt'), 'utf8') : '';
if (!/^User-agent: \*$/m.test(robotsTxt) || !/^Allow: \/$/m.test(robotsTxt)) report('robots.txt', 'should allow all crawlers');
if (/^Disallow:\s*\S/m.test(robotsTxt)) report('robots.txt', 'must not disallow any path (noindex pages and CSS/JS must stay crawlable)');
if (!robotsTxt.includes(`Sitemap: ${SITE}/sitemap-index.xml`)) report('robots.txt', 'missing Sitemap line');

// Redirect targets must exist
const redirects = existsSync(join(dist, '_redirects')) ? readFileSync(join(dist, '_redirects'), 'utf8') : '';
for (const line of redirects.split('\n').filter((l) => l && !l.startsWith('#'))) {
  const [, to] = line.trim().split(/\s+/);
  if (to.startsWith('/') && !fileFor(to)) report('_redirects', `target does not exist: ${line}`);
}
for (const icon of FAVICONS) if (!fileFor(icon)) report('favicons', `${icon} missing from build`);

const summary = `${pages.length} pages (${indexable.size} indexable), ${linksChecked} internal links/assets and ${imagesChecked} images checked, ${locs.length} sitemap URLs`;
if (issues.length) {
  console.error(issues.map((i) => `  ✖ ${i}`).join('\n'));
  console.error(`\nSEO audit FAILED: ${issues.length} issue(s). ${summary}`);
  process.exit(1);
}
console.log(`SEO audit passed with 0 issues. ${summary}`);
