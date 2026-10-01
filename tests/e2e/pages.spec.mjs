// Every page: HTTP status, console errors, broken images/assets and axe WCAG 2.1 AA.
import { AxeBuilder } from '@axe-core/playwright';
import { expect, test } from '@playwright/test';
import { allPages, blockThirdParty, scrollThrough, watchPage } from './helpers.mjs';

// Scroll-reveal entrance animations are skipped (same final colours and layout) so axe measures
// the settled page, not an element half-way through fading in. Motion is covered in layout/form specs.
test.use({ reducedMotion: 'reduce' });

for (const path of allPages()) {
  test(`page ${path}: loads cleanly, images load, 0 axe violations`, async ({ page }) => {
    await blockThirdParty(page);
    const problems = watchPage(page);
    const res = await page.goto(path, { waitUntil: 'load' });
    expect(res.status(), 'HTTP status').toBe(200);
    await scrollThrough(page);
    // the Maps iframe can keep the network busy, so idle is waited for but not required
    await page.waitForLoadState('networkidle', { timeout: 10_000 }).catch(() => {});

    expect(await page.locator('[data-reveal]').count(), 'unrevealed content').toBe(0);

    const broken = await page.evaluate(() => Array.from(document.images)
      .filter((img) => !img.closest('picture[data-defer]') && img.complete && img.naturalWidth === 0)
      .map((img) => img.currentSrc || img.src));
    expect(broken, 'broken images').toEqual([]);

    const axe = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).exclude('iframe').analyze();
    const violations = axe.violations.map((v) => `${v.id} (${v.impact}): ${v.nodes.length}x ${v.nodes.slice(0, 3).map((n) => n.target.join(' ')).join(' | ')}`);
    expect(violations, 'axe WCAG 2.1 AA violations').toEqual([]);
    expect(problems, 'console errors / failed requests').toEqual([]);
  });
}

test('unknown URL returns the branded 404 with a real 404 status', async ({ page }) => {
  const res = await page.goto('/nope-this-does-not-exist/');
  expect(res.status()).toBe(404);
  await expect(page.locator('h1')).toContainText('Not Found');
  await expect(page.locator('meta[name="robots"]')).toHaveAttribute('content', 'noindex, follow');
  await expect(page.locator('link[rel="canonical"]')).toHaveCount(0);
  for (const href of ['/', '/services/', '/menu/', '/contact/', 'tel:+919595956709']) await expect(page.locator(`main a[href="${href}"]`).first()).toBeVisible();
});

test('old .html URLs and /index.html redirect permanently to the clean URL', async ({ request }) => {
  for (const [from, to] of [['/about.html', '/about/'], ['/index.html', '/'], ['/services/wedding-catering.html', '/services/wedding-catering/'], ['/privacy.html', '/privacy/']]) {
    const res = await request.get(from, { maxRedirects: 0 });
    expect(res.status(), from).toBe(301);
    expect(new URL(res.headers().location, 'http://localhost').pathname, from).toBe(to);
  }
});

test('security headers are sent', async ({ request }) => {
  const res = await request.get('/');
  const h = res.headers();
  expect(h['x-content-type-options']).toBe('nosniff');
  expect(h['x-frame-options']).toBe('SAMEORIGIN');
  expect(h['referrer-policy']).toBe('strict-origin-when-cross-origin');
  expect(h['content-security-policy']).toContain("default-src 'self'");
});
