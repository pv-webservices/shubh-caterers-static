// Enquiry form behaviour. /api/enquiry is always intercepted: no request reaches the real function and no email is sent.
import { expect, test } from '@playwright/test';
import { blockThirdParty } from './helpers.mjs';

const VALID = { name: 'Asha Patil', phone: '+91 98765 43210', email: 'asha@example.com', message: 'Wedding lunch for 250 guests in Dhanori.' };
const ok = { status: 200, contentType: 'application/json', body: JSON.stringify({ ok: true, redirect: '/thank-you/' }) };
const fail = (status, code, extra = {}) => ({ status, contentType: 'application/json', body: JSON.stringify({ ok: false, code, ...extra }) });

/** Waits until the form's scroll-reveal entrance animation has finished, so clicks land where expected. */
async function settle(page, prefix) {
  await page.locator(`#${prefix}-form`).scrollIntoViewIfNeeded();
  if (!(await page.evaluate(() => document.documentElement.classList.contains('js')).catch(() => false))) return;
  await page.waitForFunction((id) => !document.getElementById(id).closest('[data-reveal]'), `${prefix}-form`);
}

async function fill(page, prefix = 'quote', values = VALID) {
  await settle(page, prefix);
  for (const [name, value] of Object.entries(values)) await page.fill(`#${prefix}-${name}`, value);
  await page.check(`#${prefix}-consent`);
}

test.beforeEach(async ({ page }) => { await blockThirdParty(page); });

test('successful send posts JSON in the background and lands on /thank-you/', async ({ page }) => {
  /** @type {any} */
  let payload;
  await page.route('**/api/enquiry', async (route) => { payload = route.request().postDataJSON(); await route.fulfill(ok); });
  await page.goto('/contact/');
  await fill(page);
  await page.selectOption('#quote-event', 'Weddings');
  await page.click('#quote-form [data-submit]');
  await expect(page).toHaveURL(/\/thank-you\/$/);
  await expect(page.locator('h1')).toContainText('Enquiry Received');
  expect(payload).toMatchObject({ ...VALID, event: 'Weddings', consent: 'yes', form: 'quote', page: '/contact/', website: '' });
  expect(Number(payload.ts)).toBeGreaterThan(Date.now() - 120_000);
});

test('the home page quick-enquiry form works the same way', async ({ page }) => {
  /** @type {any} */
  let payload;
  await page.route('**/api/enquiry', async (route) => { payload = route.request().postDataJSON(); await route.fulfill(ok); });
  await page.goto('/');
  await fill(page, 'enquiry');
  await page.click('#enquiry-form [data-submit]');
  await expect(page).toHaveURL(/\/thank-you\/$/);
  expect(payload).toMatchObject({ form: 'enquiry', page: '/' });
});

test('empty submit shows linked field errors, a summary, focuses the first field and sends nothing', async ({ page }) => {
  let calls = 0;
  await page.route('**/api/enquiry', (route) => { calls += 1; return route.fulfill(ok); });
  await page.goto('/contact/');
  await page.click('#quote-form [data-submit]');
  for (const name of ['name', 'phone', 'email', 'message', 'consent']) {
    const field = page.locator(`#quote-${name}`);
    await expect(field, name).toHaveAttribute('aria-invalid', 'true');
    await expect(field, name).toHaveAttribute('aria-describedby', `quote-${name}-error`);
    await expect(page.locator(`#quote-${name}-error`), name).toBeVisible();
  }
  await expect(page.locator('#quote-form .form-status')).toContainText('Please fix these 5 fields');
  await expect(page.locator('#quote-name')).toBeFocused();
  expect(calls).toBe(0);
});

test('format, length and date rules are checked in the browser', async ({ page }) => {
  await page.goto('/contact/');
  await fill(page, 'quote', { ...VALID, name: 'A', email: 'asha@example', phone: '12345', message: 'short' });
  await page.fill('#quote-date', '2020-01-01');
  await page.click('#quote-form [data-submit]');
  await expect(page.locator('#quote-name-error')).toContainText('at least 2 characters');
  await expect(page.locator('#quote-email-error')).toContainText('valid email');
  await expect(page.locator('#quote-phone-error')).toContainText('10 to 15 digits');
  await expect(page.locator('#quote-message-error')).toContainText('at least 10 characters');
  await expect(page.locator('#quote-date-error')).toContainText('today or a future date');
  // Fixing a field clears its error as you type
  await page.fill('#quote-name', 'Asha');
  await expect(page.locator('#quote-name-error')).toBeHidden();
  await expect(page.locator('#quote-name')).not.toHaveAttribute('aria-invalid', 'true');
});

test('server-side validation errors are shown on the right fields', async ({ page }) => {
  await page.route('**/api/enquiry', (route) => route.fulfill(fail(400, 'invalid', { errors: { email: 'Please enter a valid email address, e.g. name@example.com.' } })));
  await page.goto('/contact/');
  await fill(page);
  await page.click('#quote-form [data-submit]');
  await expect(page.locator('#quote-email-error')).toContainText('valid email');
  await expect(page.locator('#quote-email')).toBeFocused();
});

for (const [status, code, text] of /** @type {[number, string, string][]} */ ([[502, 'send_failed', 'could not deliver'], [500, 'not_configured', 'could not deliver'], [429, 'rate_limited', 'several enquiries'], [403, 'forbidden', 'could not verify']])) {
  test(`HTTP ${status} (${code}) shows the right message with phone/WhatsApp/email and keeps the data`, async ({ page }) => {
    await page.route('**/api/enquiry', (route) => route.fulfill(fail(status, code)));
    await page.goto('/contact/');
    await fill(page);
    await page.click('#quote-form [data-submit]');
    const status_ = page.locator('#quote-form .form-status');
    await expect(status_).toContainText(text);
    await expect(status_.locator('a[href="tel:+919595956709"]')).toBeVisible();
    await expect(status_.locator('a[href^="https://wa.me/919595956709"]')).toBeVisible();
    await expect(status_.locator('a[href^="mailto:info@shubhcaterers.in"]')).toBeVisible();
    await expect(status_).toBeFocused();
    await expect(page.locator('#quote-message')).toHaveValue(VALID.message);
    await expect(page.locator('#quote-form [data-submit]')).toBeEnabled();
    await expect(page).toHaveURL(/\/contact\/$/);
  });
}

test('network failure shows a connection message and keeps the data', async ({ page }) => {
  await page.route('**/api/enquiry', (route) => route.abort('failed'));
  await page.goto('/contact/');
  await fill(page);
  await page.click('#quote-form [data-submit]');
  await expect(page.locator('#quote-form .form-status')).toContainText('could not reach our server');
  await expect(page.locator('#quote-name')).toHaveValue(VALID.name);
});

test('offline visitors are told they are offline and nothing is sent', async ({ page, context }) => {
  let calls = 0;
  await page.route('**/api/enquiry', (route) => { calls += 1; return route.fulfill(ok); });
  await page.goto('/contact/');
  await fill(page);
  await context.setOffline(true);
  await page.click('#quote-form [data-submit]');
  await expect(page.locator('#quote-form .form-status')).toContainText('offline');
  await expect(page.locator('#quote-email')).toHaveValue(VALID.email);
  expect(calls).toBe(0);
  await context.setOffline(false);
});

test('a request with no answer times out after 20 seconds with a timeout message', async ({ page }) => {
  await page.clock.install();
  await page.route('**/api/enquiry', () => { /* never answer */ });
  await page.goto('/contact/');
  await fill(page);
  await page.click('#quote-form [data-submit]');
  const submit = page.locator('#quote-form [data-submit]');
  await expect(submit).toBeDisabled();
  await expect(submit).toContainText('Sending');
  await expect(page.locator('#quote-form [data-whatsapp]')).toBeDisabled();
  await page.clock.runFor(20_500);
  await expect(page.locator('#quote-form .form-status')).toContainText('longer than 20 seconds');
  await expect(submit).toBeEnabled();
  await expect(page.locator('#quote-message')).toHaveValue(VALID.message);
});

test('buttons are re-enabled when the page is restored with the Back button (pageshow)', async ({ page }) => {
  await page.route('**/api/enquiry', () => { /* keep pending */ });
  await page.goto('/contact/');
  await fill(page);
  await page.click('#quote-form [data-submit]');
  await expect(page.locator('#quote-form [data-submit]')).toBeDisabled();
  await page.evaluate(() => window.dispatchEvent(new PageTransitionEvent('pageshow', { persisted: true })));
  await expect(page.locator('#quote-form [data-submit]')).toBeEnabled();
});

test('typed details survive a reload (draft kept for the session)', async ({ page }) => {
  await page.goto('/contact/');
  await page.fill('#quote-name', VALID.name);
  await page.fill('#quote-message', VALID.message);
  await page.reload();
  await expect(page.locator('#quote-name')).toHaveValue(VALID.name);
  await expect(page.locator('#quote-message')).toHaveValue(VALID.message);
});

test('"Send via WhatsApp" opens WhatsApp with the details pre-filled, without the server or timer', async ({ page }) => {
  let calls = 0;
  await page.route('**/api/enquiry', (route) => { calls += 1; return route.fulfill(ok); });
  await page.addInitScript(() => { const w = /** @type {any} */ (window); w.__opened = []; w.open = (url) => { w.__opened.push(String(url)); return null; }; });
  await page.goto('/contact/');
  await page.fill('#quote-name', VALID.name);
  await page.fill('#quote-message', VALID.message);
  await page.click('#quote-form [data-whatsapp]');
  const opened = await page.evaluate(() => /** @type {any} */ (window).__opened);
  expect(opened).toHaveLength(1);
  expect(opened[0]).toMatch(/^https:\/\/wa\.me\/919595956709\?text=/);
  expect(decodeURIComponent(opened[0])).toContain('Name: Asha Patil');
  expect(calls).toBe(0);
});

test.describe('without JavaScript', () => {
  test.use({ javaScriptEnabled: false });
  test('the form does a normal POST and the 303 redirect lands on /thank-you/', async ({ page }) => {
    let body = '';
    await page.route('**/api/enquiry', async (route) => {
      body = route.request().postData() || '';
      await route.fulfill({ status: 303, headers: { location: '/thank-you/' } });
    });
    await page.goto('/contact/');
    await expect(page.locator('#quote-form [data-whatsapp]')).toBeHidden();
    await fill(page);
    await page.click('#quote-form [data-submit]');
    await expect(page).toHaveURL(/\/thank-you\/$/);
    const params = new URLSearchParams(body);
    expect(params.get('name')).toBe(VALID.name);
    expect(params.get('consent')).toBe('yes');
    expect(params.get('form')).toBe('quote');
    expect(params.get('page')).toBe('/contact/');
    expect(params.get('website')).toBe('');
  });
});
