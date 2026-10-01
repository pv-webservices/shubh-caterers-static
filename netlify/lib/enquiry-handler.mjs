// POST /api/enquiry — validates an enquiry and emails it through the client's own Zoho mailbox.
// Answers JSON to fetch() callers and redirects (303) or renders HTML for no-JavaScript form posts.
import { LIMITS, todayInIndia, validateEnquiry } from '../../assets/js/enquiry-rules.js';
import { buildEmail, headerSafe, spamSignals } from './email.mjs';
import { renderFallbackPage } from './fallback-page.mjs';

export const THANK_YOU_PATH = '/thank-you/';
export const MIN_FILL_MS = 3000;
export const MAX_BODY_BYTES = 20_000;
const SMTP_TIMEOUT_MS = 8000;                 // stay under Netlify's 10 s function limit
const REQUIRED_ENV = ['SMTP_HOST', 'SMTP_USER', 'SMTP_PASS', 'MAIL_TO'];
const ALLOWED_ORIGINS = ['https://shubhcaterers.in', 'https://www.shubhcaterers.in', 'https://shubh-caterers.netlify.app'];
const ALLOWED_ORIGIN_PATTERNS = [
  /^https:\/\/[a-z0-9-]+--shubh-caterers\.netlify\.app$/,   // deploy previews and branch deploys
  /^http:\/\/(localhost|127\.0\.0\.1)(:\d{1,5})?$/,          // local development
];

export const PUBLIC_MESSAGES = {
  invalid: 'Please correct the highlighted fields and try again.',
  forbidden: 'We could not verify where this form was sent from. Please call or WhatsApp us instead.',
  rate_limited: 'You have sent several enquiries in a short time. Please wait a few minutes, or call or WhatsApp us.',
  not_configured: 'Our enquiry form is temporarily unavailable. Please call, WhatsApp or email us — your details are still on this page.',
  send_failed: 'We could not deliver your enquiry right now. Please call, WhatsApp or email us — your details are still on this page.',
  bad_request: 'Your enquiry could not be read. Please try again.',
  too_large: 'Your message is too long. Please shorten it and try again.',
  method: 'Please use the enquiry form on our website.',
};

export function isAllowedOrigin(origin, extra = []) {
  if (!origin || origin === 'null') return false;
  return ALLOWED_ORIGINS.includes(origin) || extra.includes(origin) || ALLOWED_ORIGIN_PATTERNS.some((re) => re.test(origin));
}

function requestOrigin(req) {
  const origin = req.headers.get('origin');
  if (origin) return origin;
  try { return new URL(req.headers.get('referer') || '').origin; } catch { return ''; }
}

function clientIp(req, context) {
  return context?.ip || req.headers.get('x-nf-client-connection-ip') || (req.headers.get('x-forwarded-for') || '').split(',')[0].trim() || 'unknown';
}

async function readBody(req) {
  const declared = Number(req.headers.get('content-length') || 0);
  if (declared > MAX_BODY_BYTES) return { error: 'too_large' };
  const raw = await req.text();
  if (raw.length > MAX_BODY_BYTES) return { error: 'too_large' };
  const type = (req.headers.get('content-type') || '').toLowerCase();
  try {
    if (type.includes('application/json')) {
      const data = JSON.parse(raw || '{}');
      return data && typeof data === 'object' && !Array.isArray(data) ? { data } : { error: 'bad_request' };
    }
    if (type.includes('application/x-www-form-urlencoded')) return { data: Object.fromEntries(new URLSearchParams(raw)) };
  } catch {
    return { error: 'bad_request' };
  }
  return { error: 'bad_request' };
}

function sourcePageUrl(origin, page) {
  const path = String(page || '');
  if (!path.startsWith('/') || path.startsWith('//') || path.length > LIMITS.page.max || /[\s<>"]/.test(path)) return '';
  return `${origin}${path}`;
}

/**
 * Fill-time check: returns 'ok', 'too-fast' (bot) or 'missing' (JavaScript was off).
 * Both timestamps come from the visitor's own clock (page load -> submit), so a phone whose
 * clock is off cannot break the check; without a submit time the server clock is used.
 */
function fillTime(ts, sent, nowMs) {
  if (ts === undefined || ts === null || ts === '') return 'missing';
  const started = Number(ts);
  const submitted = sent === undefined || sent === '' ? nowMs : Number(sent);
  if (!Number.isFinite(started) || !Number.isFinite(submitted) || submitted - started < MIN_FILL_MS) return 'too-fast';
  return 'ok';
}

const json = (status, body, headers = {}) => new Response(JSON.stringify(body), {
  status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store', ...headers },
});
const redirect = (location) => new Response(null, { status: 303, headers: { location, 'cache-control': 'no-store' } });

/**
 * @param {object} deps
 * @param {Record<string, string | undefined>} deps.env
 * @param {(options: object) => { sendMail(message: object): Promise<unknown> }} deps.createTransport
 * @param {() => Promise<{ hit(ip: string, now?: number): Promise<{ allowed: boolean, retryAfter: number }> }>} deps.getRateLimiter
 * @param {() => Date} [deps.now]
 * @param {Pick<Console, 'error' | 'warn' | 'info'>} [deps.logger]
 */
export function createHandler({ env, createTransport, getRateLimiter, now = () => new Date(), logger = console }) {
  const extraOrigins = (env.ALLOWED_ORIGINS || '').split(',').map((s) => s.trim()).filter(Boolean);

  return async function handler(req, context) {
    const wantsJson = (req.headers.get('accept') || '').includes('application/json')
      || (req.headers.get('content-type') || '').includes('application/json');
    /** @type {Record<string, any>} */
    let fields = {};
    const fail = (status, code, extra = {}, headers = {}) => (wantsJson
      ? json(status, { ok: false, code, message: PUBLIC_MESSAGES[code], ...extra }, headers)
      : new Response(renderFallbackPage({ message: PUBLIC_MESSAGES[code], errors: extra.errors || {}, values: fields }), {
        status, headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store', 'x-robots-tag': 'noindex', ...headers },
      }));
    const success = () => (wantsJson ? json(200, { ok: true, redirect: THANK_YOU_PATH }) : redirect(THANK_YOU_PATH));

    if (req.method !== 'POST') return fail(405, 'method', {}, { allow: 'POST' });

    const origin = requestOrigin(req);
    if (!isAllowedOrigin(origin, extraOrigins)) {
      logger.warn('enquiry: blocked origin', origin || '(none)');
      return fail(403, 'forbidden');
    }

    const body = await readBody(req);
    if (body.error) return fail(body.error === 'too_large' ? 413 : 400, body.error);
    fields = body.data;

    // Bots: answer exactly like a real success so they learn nothing, but send nothing.
    const timeCheck = fillTime(fields.ts, fields.sent, now().getTime());
    if (String(fields.website || '').trim() !== '' || timeCheck === 'too-fast') {
      logger.info('enquiry: discarded as bot', fields.website ? 'honeypot' : 'too fast');
      return success();
    }

    try {
      const limiter = await getRateLimiter();
      const { allowed, retryAfter } = await limiter.hit(clientIp(req, context), now().getTime());
      if (!allowed) return fail(429, 'rate_limited', {}, { 'retry-after': String(retryAfter) });
    } catch (err) {
      logger.error('enquiry: rate limiter unavailable, continuing', err);
    }

    const { values, errors } = validateEnquiry(fields, { today: todayInIndia(now()) });
    if (Object.keys(errors).length) return fail(400, 'invalid', { errors });

    const missing = REQUIRED_ENV.filter((key) => !env[key]);
    if (missing.length) {
      logger.error('enquiry: missing environment variables', missing.join(', '));
      return fail(500, 'not_configured');
    }

    const meta = {
      formType: fields.form === 'quote' ? 'quote' : 'enquiry',
      pageUrl: sourcePageUrl(origin, fields.page),
      submittedAt: now(),
      flags: spamSignals(values),
      notes: timeCheck === 'missing' ? ['JavaScript was off, so the fill-time check was skipped'] : [],
    };
    const message = buildEmail(values, meta, { mailFrom: headerSafe(env.MAIL_FROM || env.SMTP_USER), mailTo: headerSafe(env.MAIL_TO) });

    try {
      const port = Number(env.SMTP_PORT || 465);
      const transport = createTransport({
        host: env.SMTP_HOST, port, secure: port === 465,
        auth: { user: env.SMTP_USER, pass: env.SMTP_PASS },
        connectionTimeout: SMTP_TIMEOUT_MS, greetingTimeout: SMTP_TIMEOUT_MS, socketTimeout: SMTP_TIMEOUT_MS,
      });
      await transport.sendMail(message);
    } catch (err) {
      logger.error('enquiry: SMTP send failed', err && /** @type {Error} */ (err).message);
      return fail(502, 'send_failed');
    }
    return success();
  };
}
