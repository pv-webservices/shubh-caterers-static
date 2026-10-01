// Unit tests for the enquiry Netlify Function. The mail transport is mocked: nothing is ever sent.
import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import nodemailer from 'nodemailer';
import { createHandler, MIN_FILL_MS } from '../../netlify/lib/enquiry-handler.mjs';
import { buildEmail } from '../../netlify/lib/email.mjs';
import { createRateLimiter, memoryStore } from '../../netlify/lib/rate-limit.mjs';

const NOW = new Date('2026-10-01T10:00:00Z');
const ENV = { SMTP_HOST: 'smtp.zoho.in', SMTP_PORT: '465', SMTP_USER: 'info@shubhcaterers.in', SMTP_PASS: 'test-only', MAIL_TO: 'info@shubhcaterers.in', MAIL_FROM: 'info@shubhcaterers.in' };
const VALID = {
  form: 'quote', page: '/contact/', name: 'Asha Patil', email: 'asha@example.com', phone: '+91 98765 43210',
  event: 'Weddings', date: '2026-12-12', guests: '250', message: 'Wedding lunch for 250 guests in Dhanori.', consent: 'yes',
  website: '', ts: String(NOW.getTime() - 10_000),
};
const silent = { error() {}, warn() {}, info() {} };

/** @param {{ env?: Record<string, string>, sendMail?: (msg: any) => Promise<unknown>, limiter?: any }} [options] */
function setup({ env = ENV, sendMail, limiter } = {}) {
  const sent = [];
  const transports = [];
  const handler = createHandler({
    env,
    createTransport: (options) => {
      transports.push(options);
      return { sendMail: sendMail || (async (msg) => { sent.push(msg); return { messageId: 'mock' }; }) };
    },
    getRateLimiter: async () => limiter || createRateLimiter(memoryStore()),
    now: () => NOW,
    logger: silent,
  });
  return { handler, sent, transports };
}

/** @returns {[Request, { ip: string }]} */
function jsonRequest(body, { origin = 'https://shubhcaterers.in', ip = '203.0.113.7', headers = {} } = {}) {
  return [new Request('https://shubhcaterers.in/api/enquiry', {
    method: 'POST',
    headers: { 'content-type': 'application/json', accept: 'application/json', ...(origin ? { origin } : {}), ...headers },
    body: JSON.stringify(body),
  }), { ip }];
}

/** @returns {[Request, { ip: string }]} */
function formRequest(body, { origin = 'https://shubhcaterers.in', ip = '203.0.113.8' } = {}) {
  return [new Request('https://shubhcaterers.in/api/enquiry', {
    method: 'POST',
    headers: { 'content-type': 'application/x-www-form-urlencoded', accept: 'text/html', origin },
    body: new URLSearchParams(body).toString(),
  }), { ip }];
}

describe('successful enquiry', () => {
  it('sends from the client mailbox with the visitor as sender name and Reply-To', async () => {
    const { handler, sent, transports } = setup();
    const res = await handler(...jsonRequest(VALID));
    assert.equal(res.status, 200);
    assert.deepEqual(await res.json(), { ok: true, redirect: '/thank-you/' });
    assert.equal(sent.length, 1);
    const [mail] = sent;
    assert.deepEqual(mail.from, { name: 'Asha Patil via Shubh Caterers Website', address: 'info@shubhcaterers.in' });
    assert.deepEqual(mail.replyTo, { name: 'Asha Patil', address: 'asha@example.com' });
    assert.equal(mail.to, 'info@shubhcaterers.in');
    assert.equal(mail.subject, 'New enquiry from Asha Patil: Weddings');
    assert.match(mail.text, /Sent from page: https:\/\/shubhcaterers\.in\/contact\//);
    assert.match(mail.text, /Submitted: .*IST/);
    assert.match(mail.text, /Form: Quote request/);
    assert.match(mail.html, /<table/);
    assert.doesNotMatch(mail.html + mail.text, /formsubmit/i);
    assert.equal(transports[0].host, 'smtp.zoho.in');
    assert.equal(transports[0].secure, true);
  });

  it('redirects no-JavaScript form posts to /thank-you/ with 303', async () => {
    const { handler, sent } = setup();
    const res = await handler(...formRequest({ ...VALID, ts: '' }));
    assert.equal(res.status, 303);
    assert.equal(res.headers.get('location'), '/thank-you/');
    assert.equal(sent.length, 1);
    assert.match(sent[0].text, /fill-time check was skipped/);
  });

  it('uses "General enquiry" when no event type is chosen', async () => {
    const { handler, sent } = setup();
    await handler(...jsonRequest({ ...VALID, event: '' }));
    assert.equal(sent[0].subject, 'New enquiry from Asha Patil: General enquiry');
  });
});

describe('validation', () => {
  it('returns field errors for every invalid field', async () => {
    const { handler, sent } = setup();
    const res = await handler(...jsonRequest({ ...VALID, name: 'A', email: 'not-an-email', phone: '12345', message: 'short', date: '2026-09-30', guests: '0' }));
    assert.equal(res.status, 400);
    const body = await res.json();
    assert.equal(body.code, 'invalid');
    assert.deepEqual(Object.keys(body.errors).sort(), ['date', 'email', 'guests', 'message', 'name', 'phone']);
    assert.equal(sent.length, 0);
  });

  it('checks maximum lengths', async () => {
    const { handler } = setup();
    const res = await handler(...jsonRequest({ ...VALID, name: 'x'.repeat(81), message: 'y'.repeat(2001), phone: '1'.repeat(16) }));
    const body = await res.json();
    assert.deepEqual(Object.keys(body.errors).sort(), ['message', 'name', 'phone']);
  });

  it('requires consent', async () => {
    const { handler, sent } = setup();
    const res = await handler(...jsonRequest({ ...VALID, consent: '' }));
    assert.equal(res.status, 400);
    assert.ok((await res.json()).errors.consent);
    assert.equal(sent.length, 0);
  });

  it('accepts today as the event date (India time)', async () => {
    const { handler } = setup();
    const res = await handler(...jsonRequest({ ...VALID, date: '2026-10-01' }));
    assert.equal(res.status, 200);
  });

  it('shows no-JS visitors their entries again, escaped, with the errors', async () => {
    const { handler } = setup();
    const res = await handler(...formRequest({ ...VALID, email: 'bad', message: '<b>Hi</b> there, wedding please' }));
    assert.equal(res.status, 400);
    assert.match(res.headers.get('content-type'), /text\/html/);
    const html = await res.text();
    assert.match(html, /value="Asha Patil"/);
    assert.match(html, /&lt;b&gt;Hi&lt;\/b&gt; there/);
    assert.match(html, /aria-invalid="true" aria-describedby="f-email-error"/);
    assert.match(html, /noindex/);
  });
});

describe('spam protection', () => {
  it('silently accepts and discards the honeypot', async () => {
    const { handler, sent } = setup();
    const res = await handler(...jsonRequest({ ...VALID, website: 'http://spam.example' }));
    assert.equal(res.status, 200);
    assert.deepEqual(await res.json(), { ok: true, redirect: '/thank-you/' });
    assert.equal(sent.length, 0);
  });

  it('silently discards forms filled faster than the minimum time', async () => {
    const { handler, sent } = setup();
    const res = await handler(...jsonRequest({ ...VALID, ts: String(NOW.getTime() - (MIN_FILL_MS - 500)) }));
    assert.equal(res.status, 200);
    assert.equal(sent.length, 0);
  });

  it("measures fill time on the visitor's own clock, so clock skew does not matter", async () => {
    const { handler, sent } = setup();
    const skewed = NOW.getTime() + 3_600_000;   // visitor's clock one hour fast
    await handler(...jsonRequest({ ...VALID, ts: String(skewed - 1000), sent: String(skewed) }));
    assert.equal(sent.length, 0, '1 second fill on a skewed clock is still a bot');
    await handler(...jsonRequest({ ...VALID, ts: String(skewed - 20_000), sent: String(skewed) }));
    assert.equal(sent.length, 1, '20 second fill on a skewed clock is a person');
  });

  it('silently discards a garbage timestamp', async () => {
    const { handler, sent } = setup();
    await handler(...jsonRequest({ ...VALID, ts: 'abc' }));
    assert.equal(sent.length, 0);
  });

  it('rejects unknown and missing origins', async () => {
    const { handler, sent } = setup();
    assert.equal((await handler(...jsonRequest(VALID, { origin: 'https://evil.example' }))).status, 403);
    assert.equal((await handler(...jsonRequest(VALID, { origin: null }))).status, 403);
    assert.equal(sent.length, 0);
  });

  it('allows www, deploy previews and localhost', async () => {
    const { handler, sent } = setup();
    for (const origin of ['https://www.shubhcaterers.in', 'https://deploy-preview-4--shubh-caterers.netlify.app', 'http://localhost:8888']) {
      assert.equal((await handler(...jsonRequest(VALID, { origin, ip: origin }))).status, 200, origin);
    }
    assert.equal(sent.length, 3);
  });

  it('strips line breaks from header values (header injection)', async () => {
    const { handler, sent } = setup();
    const res = await handler(...jsonRequest({ ...VALID, name: 'Asha\r\nBcc: victim@example.com', event: 'Weddings\nX-Evil: 1' }));
    assert.equal(res.status, 200);
    const [mail] = sent;
    for (const value of [mail.from.name, mail.replyTo.name, mail.subject]) assert.doesNotMatch(value, /[\r\n]/);
    const headers = (await renderRaw(mail)).split(/\r?\n\r?\n/)[0];
    assert.doesNotMatch(headers, /^Bcc:/mi);
    assert.doesNotMatch(headers, /^X-Evil:/mi);
  });

  it('HTML-escapes every value in the email body', async () => {
    const { handler, sent } = setup();
    await handler(...jsonRequest({ ...VALID, message: '<script>alert(1)</script> lunch for 40' }));
    assert.match(sent[0].html, /&lt;script&gt;alert\(1\)&lt;\/script&gt;/);
    assert.doesNotMatch(sent[0].html, /<script>/);
  });

  it('flags suspicious keywords in the subject instead of dropping the email', async () => {
    const { handler, sent } = setup();
    await handler(...jsonRequest({ ...VALID, message: 'We offer SEO services and crypto for your wedding business.' }));
    assert.equal(sent.length, 1);
    assert.match(sent[0].subject, /^\[Possible spam\] New enquiry from Asha Patil/);
  });

  it('rate-limits to 5 enquiries per 10 minutes per IP', async () => {
    const limiter = createRateLimiter(memoryStore());
    const { handler, sent } = setup({ limiter });
    for (let i = 0; i < 5; i += 1) assert.equal((await handler(...jsonRequest(VALID, { ip: '198.51.100.1' }))).status, 200);
    const blocked = await handler(...jsonRequest(VALID, { ip: '198.51.100.1' }));
    assert.equal(blocked.status, 429);
    assert.ok(Number(blocked.headers.get('retry-after')) > 0);
    assert.equal((await handler(...jsonRequest(VALID, { ip: '198.51.100.2' }))).status, 200, 'other IPs are unaffected');
    assert.equal(sent.length, 6);
  });

  it('frees the rate limit after the window', async () => {
    const limiter = createRateLimiter(memoryStore(), { limit: 1, windowMs: 1000 });
    assert.equal((await limiter.hit('1.1.1.1', 0)).allowed, true);
    assert.equal((await limiter.hit('1.1.1.1', 500)).allowed, false);
    assert.equal((await limiter.hit('1.1.1.1', 1500)).allowed, true);
  });
});

describe('failures', () => {
  it('returns 500 when SMTP configuration is missing', async () => {
    const { handler, sent } = setup({ env: { ...ENV, SMTP_PASS: '' } });
    const res = await handler(...jsonRequest(VALID));
    assert.equal(res.status, 500);
    assert.equal((await res.json()).code, 'not_configured');
    assert.equal(sent.length, 0);
  });

  it('returns 502 when the SMTP server fails', async () => {
    const { handler } = setup({ sendMail: async () => { throw new Error('535 Authentication Failed'); } });
    const res = await handler(...jsonRequest(VALID));
    assert.equal(res.status, 502);
    const body = await res.json();
    assert.equal(body.code, 'send_failed');
    assert.match(body.message, /call, WhatsApp or email/);
  });

  it('rejects other methods, unreadable and oversized bodies', async () => {
    const { handler } = setup();
    assert.equal((await handler(new Request('https://shubhcaterers.in/api/enquiry'), {})).status, 405);
    const [bad] = jsonRequest(VALID);
    const unreadable = new Request(bad.url, { method: 'POST', headers: bad.headers, body: '{not json' });
    assert.equal((await handler(unreadable, {})).status, 400);
    assert.equal((await handler(...jsonRequest({ ...VALID, message: 'x'.repeat(25_000) }))).status, 413);
  });

  it('keeps working when the rate limiter store is down', async () => {
    const handler = createHandler({
      env: ENV, now: () => NOW, logger: silent,
      createTransport: () => ({ sendMail: async () => ({}) }),
      getRateLimiter: async () => { throw new Error('blobs down'); },
    });
    assert.equal((await handler(...jsonRequest(VALID))).status, 200);
  });
});

/** Renders the message with nodemailer's stream transport (no network) and returns the raw RFC 822 text. */
async function renderRaw(mail) {
  const transport = nodemailer.createTransport({ streamTransport: true, buffer: true, newline: 'unix' });
  const info = await transport.sendMail(mail);
  return info.message.toString();
}

describe('rendered email (nodemailer, not sent)', () => {
  it('has the expected From, Reply-To, To and Subject headers and both parts', async () => {
    const mail = buildEmail(
      { name: 'Asha Patil', email: 'asha@example.com', phone: '9876543210', event: 'Birthday Party', date: '', guests: '', message: 'Birthday for 40 kids.', consent: 'yes' },
      { formType: 'enquiry', pageUrl: 'https://shubhcaterers.in/', submittedAt: NOW, flags: [] },
      { mailFrom: 'info@shubhcaterers.in', mailTo: 'info@shubhcaterers.in' },
    );
    const raw = await renderRaw(mail);
    assert.match(raw, /^From: "?Asha Patil via Shubh Caterers Website"? <info@shubhcaterers\.in>$/m);
    assert.match(raw, /^Reply-To: "?Asha Patil"? <asha@example\.com>$/m);
    assert.match(raw, /^To: info@shubhcaterers\.in$/m);
    assert.match(raw, /^Subject: New enquiry from Asha Patil: Birthday Party$/m);
    assert.match(raw, /Content-Type: multipart\/alternative/);
    assert.match(raw, /Content-Type: text\/plain/);
    assert.match(raw, /Content-Type: text\/html/);
    assert.match(mail.text, /Submitted: Thursday, 1 October 2026 at 3:30\s?pm IST/i);
  });
});
