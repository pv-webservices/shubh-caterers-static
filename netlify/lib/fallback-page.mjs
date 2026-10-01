// Page shown to visitors without JavaScript when their enquiry could not be sent.
// It repeats everything they typed in a pre-filled form, so nothing is lost.
import { LIMITS } from '../../assets/js/enquiry-rules.js';
import { escapeHtml as e } from './email.mjs';

export const CONTACT = {
  phone: '+91 95959 56709',
  phoneHref: 'tel:+919595956709',
  whatsappHref: 'https://wa.me/919595956709',
  email: 'info@shubhcaterers.in',
};

const LABELS = { name: 'Your name', email: 'Email address', phone: 'Phone number', event: 'Event type', date: 'Event date', guests: 'Approx. guests', message: 'Message / event details' };

function field(name, values, errors) {
  const id = `f-${name}`;
  const error = errors[name] ? `<p class="err" id="${id}-error">${e(errors[name])}</p>` : '';
  const aria = errors[name] ? ` aria-invalid="true" aria-describedby="${id}-error"` : '';
  const value = e(values[name] ?? '');
  const control = name === 'message'
    ? `<textarea id="${id}" name="message" rows="5" maxlength="${LIMITS.message.max}"${aria}>${value}</textarea>`
    : `<input id="${id}" name="${name}" value="${value}" type="${name === 'email' ? 'email' : name === 'date' ? 'date' : 'text'}"${aria}>`;
  return `<div class="f"><label for="${id}">${LABELS[name]}</label>${control}${error}</div>`;
}

/**
 * @param {{ message: string, errors: Record<string, string>, values: Record<string, unknown> }} input
 */
export function renderFallbackPage({ message, errors, values }) {
  const v = values || {};
  const names = ['name', 'email', 'phone', 'event', ...(v.form === 'quote' ? ['date', 'guests'] : []), 'message'];
  const checked = v.consent ? ' checked' : '';
  const consentError = errors.consent ? `<p class="err" id="f-consent-error">${e(errors.consent)}</p>` : '';
  return `<!doctype html><html lang="en-IN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, follow"><title>Enquiry not sent | Shubh Caterers</title>
<style>body{margin:0;font:16px/1.6 system-ui,-apple-system,'Segoe UI',sans-serif;color:#2b1a12;background:#fffaf1}main{max-width:640px;margin:0 auto;padding:32px 16px}
h1{font-family:Georgia,serif;color:#7a0c0c;font-size:1.7rem;margin:0 0 8px}.alert{padding:14px 16px;border-radius:10px;background:#fdecea;border:1px solid #e3a59f;color:#7a1410}
.f{display:grid;gap:4px;margin:14px 0}label{font-weight:600}input,textarea{font:inherit;padding:10px 12px;border:1.5px solid #d8c3a0;border-radius:10px;background:#fff}
[aria-invalid=true]{border-color:#b3161d}.err{margin:0;color:#b3161d;font-size:.9rem}button{font:inherit;font-weight:600;padding:12px 22px;border:0;border-radius:999px;background:#7a0c0c;color:#fff;cursor:pointer}
.alt{margin-top:28px;padding:16px;border-radius:10px;background:#fff;border:1px solid #ead8b8}a{color:#7a0c0c;font-weight:600}</style></head>
<body><main><h1>Your enquiry was not sent yet</h1><p class="alert" role="alert">${e(message)}</p>
<form method="post" action="/api/enquiry">
<input type="hidden" name="form" value="${e(v.form === 'quote' ? 'quote' : 'enquiry')}"><input type="hidden" name="page" value="${e(v.page || '/')}">
${names.map((n) => field(n, v, errors)).join('\n')}
<div class="f"><label><input type="checkbox" name="consent" value="yes"${checked}${errors.consent ? ' aria-invalid="true" aria-describedby="f-consent-error"' : ''}> I agree to the <a href="/privacy/">privacy policy</a> and to Shubh Caterers contacting me about this enquiry.</label>${consentError}</div>
<button type="submit">Send enquiry again</button></form>
<div class="alt"><strong>Prefer to talk?</strong><br>Call <a href="${CONTACT.phoneHref}">${CONTACT.phone}</a> · <a href="${CONTACT.whatsappHref}">WhatsApp us</a> · Email <a href="mailto:${CONTACT.email}">${CONTACT.email}</a></div>
<p><a href="/">← Back to the Shubh Caterers website</a></p></main></body></html>`;
}
