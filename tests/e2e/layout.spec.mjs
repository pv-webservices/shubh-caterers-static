// Responsive layout, tap targets, keyboard navigation, focus visibility and reduced motion.
import { expect, test } from '@playwright/test';
import { allPages, blockThirdParty } from './helpers.mjs';

const WIDTHS = [320, 375, 768, 1024, 1440];
const TAP_MIN = 24;   // WCAG 2.2 AA target size (minimum); 44px is reported as a recommendation
const TARGETS = 'a.btn, button:not(.hero-tab):not([tabindex="-1"]), input:not([type="hidden"]):not([tabindex="-1"]), select, textarea, .nav-link, .mobile-bar a, .socials a, .contact-tile, .info-card, .chip, .menu-nav a, .util-list a';

for (const width of WIDTHS) {
  test(`no horizontal scroll and tap targets >= ${TAP_MIN}px at ${width}px`, async ({ page }) => {
    test.setTimeout(300_000);   // visits every page
    await blockThirdParty(page);
    await page.setViewportSize({ width, height: 900 });
    const small = [];
    for (const path of allPages()) {
      await page.goto(path, { waitUntil: 'domcontentloaded' });
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
      expect(overflow, `${path} overflows by ${overflow}px at ${width}px`).toBeLessThanOrEqual(0);
      const tiny = await page.evaluate(({ selector, min }) => Array.from(document.querySelectorAll(selector)).filter((el) => {
        const r = el.getBoundingClientRect();
        const style = getComputedStyle(el);
        if (!r.width || !r.height || style.visibility === 'hidden' || el.closest('[hidden], [aria-hidden="true"], .dropdown, .main-nav:not(.is-open) .nav-mobile-extra')) return false;
        return r.width < min || r.height < min;
      }).map((el) => `${el.tagName.toLowerCase()}.${String(el.className).split(' ')[0]} "${(el.textContent || el.getAttribute('aria-label') || '').trim().slice(0, 30)}" ${Math.round(el.getBoundingClientRect().width)}x${Math.round(el.getBoundingClientRect().height)}`), { selector: TARGETS, min: TAP_MIN });
      small.push(...tiny.map((t) => `${path}: ${t}`));
    }
    expect(small, 'tap targets smaller than 24x24').toEqual([]);
  });
}

test('skip link is the first tab stop, is visible on focus and moves focus to main', async ({ page }) => {
  await page.goto('/about/');
  await page.keyboard.press('Tab');
  const skip = page.locator('.skip-link');
  await expect(skip).toBeFocused();
  const box = await skip.boundingBox();
  expect(box.y).toBeGreaterThanOrEqual(0);
  await page.keyboard.press('Enter');
  await expect(page).toHaveURL(/#main$/);
  await expect(page.locator('#main')).toBeFocused();
});

test('keyboard focus is clearly visible on links, buttons and form fields', async ({ page }) => {
  await page.goto('/contact/');
  for (const selector of ['.site-header .nav-link >> nth=1', '#quote-name', '#quote-consent', '[data-submit] >> nth=0']) {
    const el = page.locator(selector);
    await el.focus();
    await page.keyboard.press('Shift+Tab');
    await page.keyboard.press('Tab');
    const outline = await el.evaluate((node) => { const s = getComputedStyle(node); return { style: s.outlineStyle, width: parseFloat(s.outlineWidth), shadow: s.boxShadow }; });
    expect(outline.style !== 'none' && outline.width >= 2, `${selector} focus outline ${JSON.stringify(outline)}`).toBe(true);
  }
});

test('mobile menu opens and closes with the keyboard', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 800 });
  await page.goto('/');
  const toggle = page.locator('#menuToggle');
  await toggle.focus();
  await page.keyboard.press('Enter');
  await expect(toggle).toHaveAttribute('aria-expanded', 'true');
  await expect(page.locator('#mainNav .nav-link').first()).toBeVisible();
  await page.keyboard.press('Escape');
  await expect(toggle).toHaveAttribute('aria-expanded', 'false');
  await expect(toggle).toBeFocused();
});

test.describe('reduced motion', () => {
  test.use({ reducedMotion: 'reduce' });
  test('animations are off, content is visible and the hero does not auto-advance', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('[data-reveal]')).toHaveCount(0);
    const duration = await page.locator('.hero-slide.is-active img').evaluate((el) => parseFloat(getComputedStyle(el).animationDuration));
    expect(duration).toBeLessThan(0.1);
    await page.waitForTimeout(8000);
    await expect(page.locator('.hero-tab').first()).toHaveAttribute('aria-pressed', 'true');
    await expect(page.locator('[data-count]').first()).not.toHaveText('0');
  });
});
