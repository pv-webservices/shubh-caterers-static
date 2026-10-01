/* Enquiry form rules shared by the browser (assets/js/enquiry-form.js) and the
   Netlify Function (netlify/functions/enquiry.mjs), so both validate identically. */

export const LIMITS = {
  name: { min: 2, max: 80 },
  email: { max: 254 },
  phone: { minDigits: 10, maxDigits: 15, max: 25 },
  message: { min: 10, max: 2000 },
  event: { max: 60 },
  guests: { min: 1, max: 100000 },
  page: { max: 300 },
};

export const MESSAGES = {
  name: `Please enter your name (at least ${LIMITS.name.min} characters).`,
  nameLong: `Please keep your name under ${LIMITS.name.max} characters.`,
  email: 'Please enter a valid email address, e.g. name@example.com.',
  phone: `Please enter a valid phone number with ${LIMITS.phone.minDigits} to ${LIMITS.phone.maxDigits} digits.`,
  message: `Please tell us a little about your event (at least ${LIMITS.message.min} characters).`,
  messageLong: `Please keep your message under ${LIMITS.message.max} characters.`,
  event: 'Please choose an event type from the list.',
  date: 'Please choose today or a future date.',
  guests: `Please enter a guest count between ${LIMITS.guests.min} and ${LIMITS.guests.max.toLocaleString('en-IN')}.`,
  consent: 'Please tick the box to agree to our privacy policy so we can reply to you.',
};

export const FORM_TYPES = { quote: 'Quote request', enquiry: 'Quick enquiry' };

const EMAIL_RE = /^[^\s@<>()[\]\\,;:"]+@[^\s@<>()[\]\\,;:"]+\.[a-z]{2,}$/i;
const PHONE_CHARS_RE = /^[0-9+()\-.\s]+$/;
const DATE_RE = /^(\d{4})-(\d{2})-(\d{2})$/;
const CONTROL_RE = /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/g;
const LINE_BREAK_RE = /[\r\n\u2028\u2029]+/g;
const TRUTHY = new Set(['on', 'yes', 'true', '1']);

/** Trims, removes control characters and (for single-line fields) collapses line breaks. */
export function clean(value, { multiline = false } = {}) {
  const text = value == null ? '' : String(value);
  const noControls = text.replace(CONTROL_RE, '');
  return (multiline ? noControls.replace(/\r\n?/g, '\n') : noControls.replace(LINE_BREAK_RE, ' ')).trim();
}

export const digitsOf = (phone) => String(phone || '').replace(/\D/g, '');

/** Today's date as YYYY-MM-DD in India (the business's time zone). */
export function todayInIndia(now = new Date()) {
  return new Intl.DateTimeFormat('en-CA', { timeZone: 'Asia/Kolkata', year: 'numeric', month: '2-digit', day: '2-digit' }).format(now);
}

function isRealDate(value) {
  const m = DATE_RE.exec(value);
  if (!m) return false;
  const d = new Date(Date.UTC(Number(m[1]), Number(m[2]) - 1, Number(m[3])));
  return d.getUTCFullYear() === Number(m[1]) && d.getUTCMonth() === Number(m[2]) - 1 && d.getUTCDate() === Number(m[3]);
}

/**
 * Validates one enquiry. Lengths are checked by hand because the browser's
 * `validity.tooShort` does not fire for autofilled or script-set values.
 * @param {Record<string, unknown>} input raw field values
 * @param {{ today?: string, eventTypes?: string[] }} [options]
 * @returns {{ values: Record<string, string>, errors: Record<string, string> }}
 */
export function validateEnquiry(input, { today = todayInIndia(), eventTypes } = {}) {
  /** @type {Record<string, string>} */
  const values = {
    name: clean(input.name),
    email: clean(input.email),
    phone: clean(input.phone),
    event: clean(input.event),
    date: clean(input.date),
    guests: clean(input.guests),
    message: clean(input.message, { multiline: true }),
    consent: TRUTHY.has(clean(input.consent).toLowerCase()) || input.consent === true ? 'yes' : '',
  };
  /** @type {Record<string, string>} */
  const errors = {};

  if (values.name.length < LIMITS.name.min) errors.name = MESSAGES.name;
  else if (values.name.length > LIMITS.name.max) errors.name = MESSAGES.nameLong;

  if (values.email.length > LIMITS.email.max || !EMAIL_RE.test(values.email)) errors.email = MESSAGES.email;

  const digits = digitsOf(values.phone);
  if (values.phone.length > LIMITS.phone.max || !PHONE_CHARS_RE.test(values.phone)
      || digits.length < LIMITS.phone.minDigits || digits.length > LIMITS.phone.maxDigits) errors.phone = MESSAGES.phone;

  if (values.message.length < LIMITS.message.min) errors.message = MESSAGES.message;
  else if (values.message.length > LIMITS.message.max) errors.message = MESSAGES.messageLong;

  if (values.event && (values.event.length > LIMITS.event.max || (eventTypes && !eventTypes.includes(values.event)))) errors.event = MESSAGES.event;

  if (values.date && (!isRealDate(values.date) || values.date < today)) errors.date = MESSAGES.date;

  if (values.guests) {
    const n = Number(values.guests);
    if (!Number.isInteger(n) || n < LIMITS.guests.min || n > LIMITS.guests.max) errors.guests = MESSAGES.guests;
  }

  if (values.consent !== 'yes') errors.consent = MESSAGES.consent;

  return { values, errors };
}
