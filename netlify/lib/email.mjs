// Builds the enquiry email (HTML table + plain-text twin) and its headers.
import { FORM_TYPES } from '../../assets/js/enquiry-rules.js';

export const SITE_NAME = 'Shubh Caterers Website';
const BRAND = { maroon: '#7a0c0c', gold: '#c9973a', cream: '#fffaf1', ink: '#2b1a12', line: '#ead8b8' };
const SUSPICIOUS = [
  'viagra', 'cialis', 'casino', 'betting', 'crypto', 'bitcoin', 'forex', 'loan offer', 'seo service', 'backlink',
  'web design service', 'guest post', 'rank your website', 'first page of google', 'porn', 'escort', 'telegram',
];
const URL_RE = /https?:\/\/|www\./gi;

const HTML_ESCAPES = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
export const escapeHtml = (value) => String(value ?? '').replace(/[&<>"']/g, (c) => HTML_ESCAPES[c]);

/** Header values must never contain line breaks (header injection). */
export const headerSafe = (value) => String(value ?? '').replace(/[\r\n\u2028\u2029]+/g, ' ').replace(/[<>"]/g, '').trim();

/** Reasons this enquiry looks like spam; an empty list means it looks fine. */
export function spamSignals(values) {
  const text = `${values.name} ${values.email} ${values.message}`.toLowerCase();
  const reasons = SUSPICIOUS.filter((word) => text.includes(word)).map((word) => `keyword "${word}"`);
  const links = (values.message.match(URL_RE) || []).length;
  if (links >= 2) reasons.push(`${links} links`);
  return reasons;
}

export function formatIndiaTime(date) {
  return new Intl.DateTimeFormat('en-IN', {
    timeZone: 'Asia/Kolkata', dateStyle: 'full', timeStyle: 'short',
  }).format(date) + ' IST';
}

function rows(values, meta) {
  return [
    ['Form', FORM_TYPES[meta.formType] || FORM_TYPES.enquiry],
    ['Name', values.name],
    ['Email', values.email],
    ['Phone', values.phone],
    ['Event type', values.event || 'Not specified'],
    ...(meta.formType === 'quote' ? [['Event date', values.date || 'Not specified'], ['Guests', values.guests || 'Not specified']] : []),
    ['Message', values.message],
    ['Privacy consent', 'Yes'],
    ['Sent from page', meta.pageUrl || 'Unknown'],
    ['Submitted', formatIndiaTime(meta.submittedAt)],
    ...(meta.flags.length ? [['Spam check', `Flagged: ${meta.flags.join(', ')}`]] : []),
    ...((meta.notes || []).length ? [['Note', meta.notes.join('; ')]] : []),
  ];
}

/**
 * @param {Record<string, string>} values validated form values
 * @param {{ formType: string, pageUrl: string, submittedAt: Date, flags: string[], notes?: string[] }} meta
 * @param {{ mailFrom: string, mailTo: string }} config
 */
export function buildEmail(values, meta, config) {
  const topic = values.event || 'General enquiry';
  const subjectPrefix = meta.flags.length ? '[Possible spam] ' : '';
  const subject = headerSafe(`${subjectPrefix}New enquiry from ${values.name}: ${topic}`);
  const table = rows(values, meta);

  const text = [
    `New enquiry from the ${SITE_NAME}`,
    '',
    ...table.map(([label, value]) => `${label}: ${value}`),
    '',
    `Reply to this email to answer ${values.name} directly.`,
  ].join('\n');

  const cell = 'padding:10px 14px;border-bottom:1px solid ' + BRAND.line + ';vertical-align:top;font:14px/1.5 Arial,Helvetica,sans-serif;';
  const htmlRows = table.map(([label, value]) => `<tr><th align="left" style="${cell}width:150px;color:${BRAND.maroon};">${escapeHtml(label)}</th>`
    + `<td style="${cell}color:${BRAND.ink};">${escapeHtml(value).replace(/\n/g, '<br>')}</td></tr>`).join('');
  const html = `<!doctype html><html><body style="margin:0;padding:24px;background:${BRAND.cream};">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:640px;margin:0 auto;background:#ffffff;border:1px solid ${BRAND.line};border-radius:12px;overflow:hidden;">
<tr><td style="padding:18px 20px;background:${BRAND.maroon};color:#ffffff;font:bold 18px/1.3 Georgia,serif;">Shubh Caterers &mdash; New website enquiry</td></tr>
<tr><td style="padding:0;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0">${htmlRows}</table></td></tr>
<tr><td style="padding:14px 20px;font:13px/1.5 Arial,Helvetica,sans-serif;color:#6b5a4e;border-top:3px solid ${BRAND.gold};">Click <strong>Reply</strong> to answer ${escapeHtml(values.name)} at ${escapeHtml(values.email)}.</td></tr>
</table></body></html>`;

  return {
    from: { name: headerSafe(`${values.name} via ${SITE_NAME}`), address: config.mailFrom },
    to: config.mailTo,
    replyTo: { name: headerSafe(values.name), address: headerSafe(values.email) },
    subject,
    text,
    html,
  };
}
