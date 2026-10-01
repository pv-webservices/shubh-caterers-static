import { readFileSync } from 'node:fs';
import { join } from 'node:path';

const SITE = 'https://shubhcaterers.in';

/** Every page in the sitemap plus the two noindex utility pages. */
export function allPages() {
  const sitemap = readFileSync(join(process.cwd(), 'dist', 'sitemap.xml'), 'utf8');
  const paths = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1].replace(SITE, ''));
  return [...paths, '/thank-you/', '/404.html'];
}

/** Collects console errors and failed same-origin requests while a page is open. */
export function watchPage(page) {
  const problems = [];
  page.on('console', (msg) => { if (msg.type() === 'error') problems.push(`console: ${msg.text()}`); });
  page.on('pageerror', (err) => problems.push(`pageerror: ${err.message}`));
  page.on('response', (res) => {
    const url = new URL(res.url());
    if (url.hostname === 'localhost' && res.status() >= 400 && !url.pathname.startsWith('/nope')) problems.push(`HTTP ${res.status()} ${url.pathname}`);
  });
  page.on('requestfailed', (req) => {
    const url = new URL(req.url());
    if (url.hostname === 'localhost' && !/ERR_ABORTED/.test(req.failure()?.errorText || '')) problems.push(`failed: ${url.pathname} ${req.failure()?.errorText}`);
  });
  return problems;
}

/** Scrolls to the bottom in steps so lazy images load, then back to the top. */
export async function scrollThrough(page) {
  await page.evaluate(async () => {
    const step = Math.max(400, Math.floor(window.innerHeight * 0.8));
    for (let y = 0; y < document.documentElement.scrollHeight; y += step) {
      window.scrollTo(0, y);
      await new Promise((r) => setTimeout(r, 60));
    }
    window.scrollTo(0, 0);
  });
}

/** Blocks the Google Maps iframe so tests never depend on a third-party network call. */
export async function blockThirdParty(page) {
  await page.route(/^https?:\/\/(?!localhost)/, (route) => route.fulfill({ status: 204, body: '' }));
}
