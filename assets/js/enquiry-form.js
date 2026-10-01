/* Enquiry form enhancement. Without JavaScript the form still posts to /api/enquiry
   and the server redirects to /thank-you/. With it: inline validation, background
   sending with fetch(), clear error states, and the visitor's text is never lost. */
import { todayInIndia, validateEnquiry } from './enquiry-rules.js';

const ENDPOINT = '/api/enquiry';
const THANK_YOU = '/thank-you/';
const TIMEOUT_MS = 20000;
const DRAFT_PREFIX = 'enquiry-draft:';
const FIELDS = ['name', 'phone', 'email', 'event', 'date', 'guests', 'message', 'consent'];
const LABELS = { name: 'Name', phone: 'Phone', email: 'Email', event: 'Event', date: 'Event date', guests: 'Guests', message: 'Details' };

const FAILURES = {
  offline: 'You seem to be offline, so your enquiry was not sent.',
  timeout: 'Sending took longer than 20 seconds, so we stopped trying.',
  network: 'We could not reach our server.',
  rate_limited: 'You have sent several enquiries in a short time, so this one was not sent. Please wait a few minutes before trying again.',
  forbidden: 'We could not verify this form submission, so it was not sent.',
  not_configured: 'We could not deliver your enquiry right now.',
  send_failed: 'We could not deliver your enquiry right now.',
  unknown: 'Something went wrong and your enquiry was not sent.',
};

const storage = {
  get(key) { try { return JSON.parse(sessionStorage.getItem(key) || 'null'); } catch { return null; } },
  set(key, value) { try { sessionStorage.setItem(key, JSON.stringify(value)); } catch { /* private mode: nothing to save */ } },
  remove(key) { try { sessionStorage.removeItem(key); } catch { /* ignore */ } },
};

const isOffline = () => navigator.onLine === false;
const escapeHtml = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);

function enhance(form) {
  const { phone, email, whatsapp } = form.dataset;
  const status = form.querySelector('.form-status');
  const submit = form.querySelector('[data-submit]');
  const waButton = form.querySelector('[data-whatsapp]');
  const submitLabel = submit.querySelector('.btn-label');
  const idleLabel = submitLabel.textContent;
  const draftKey = DRAFT_PREFIX + form.id;
  const touched = new Set();
  let busy = false;

  const control = (name) => form.elements.namedItem(name);
  const errorEl = (name) => form.querySelector(`#${form.id.replace(/-form$/, '')}-${name}-error`);
  const present = FIELDS.filter((n) => control(n));

  /** @returns {Record<string, string>} */
  const values = () => {
    /** @type {Record<string, string>} */
    const out = {};
    present.forEach((n) => {
      const el = /** @type {HTMLInputElement} */ (control(n));
      out[n] = el.type === 'checkbox' ? (el.checked ? 'yes' : '') : el.value;
    });
    return out;
  };

  const compose = () => {
    const v = values();
    const lines = ['Hello Shubh Caterers, I would like a catering quote.'];
    Object.keys(LABELS).forEach((k) => { if (v[k] && v[k].trim()) lines.push(`${LABELS[k]}: ${v[k].trim()}`); });
    return lines.join('\n');
  };

  const alternatives = () => {
    const mail = `mailto:${email}?subject=${encodeURIComponent('Catering enquiry')}&body=${encodeURIComponent(compose())}`;
    return ` Your details are still in the form. Please try again, or call <a href="tel:+91${phone}">${phone}</a>, `
      + `<a href="https://wa.me/${whatsapp}" target="_blank" rel="noopener">WhatsApp us</a> or <a href="${escapeHtml(mail)}">email these details</a> to ${email}.`;
  };

  const setStatus = (kind, html, focus = false) => {
    status.className = `form-status is-${kind}`;
    status.innerHTML = html;
    status.hidden = !html;
    if (focus) status.focus();
  };

  const showFieldError = (name, message) => {
    const el = /** @type {HTMLElement} */ (control(name));
    const err = errorEl(name);
    if (!el || !err) return;
    if (message) {
      err.textContent = message;
      err.hidden = false;
      el.setAttribute('aria-invalid', 'true');
      el.setAttribute('aria-describedby', err.id);
    } else {
      err.textContent = '';
      err.hidden = true;
      el.removeAttribute('aria-invalid');
      el.removeAttribute('aria-describedby');
    }
  };

  const validate = () => validateEnquiry(values(), { today: todayInIndia() }).errors;

  const showErrors = (errors) => {
    present.forEach((n) => showFieldError(n, errors[n]));
    const names = present.filter((n) => errors[n]);
    if (!names.length) return false;
    const items = names.map((n) => `<li><a href="#${control(n).id}">${escapeHtml(errors[n])}</a></li>`).join('');
    setStatus('error', `<strong>Please fix ${names.length === 1 ? 'this field' : `these ${names.length} fields`}:</strong><ul>${items}</ul>`);
    /** @type {HTMLElement} */ (control(names[0])).focus();
    return true;
  };

  const setBusy = (on) => {
    busy = on;
    form.setAttribute('aria-busy', String(on));
    submit.disabled = on;
    if (waButton) waButton.disabled = on;
    submitLabel.textContent = on ? 'Sending…' : idleLabel;
  };

  const saveDraft = () => storage.set(draftKey, values());

  // Restore an unsent draft (e.g. after a failed send and a page reload).
  const draft = storage.get(draftKey);
  if (draft) {
    present.forEach((n) => {
      const el = /** @type {HTMLInputElement} */ (control(n));
      if (draft[n] === undefined) return;
      if (el.type === 'checkbox') el.checked = draft[n] === 'yes';
      else if (!el.value) el.value = draft[n];
    });
  }

  const ts = control('ts');
  if (ts) /** @type {HTMLInputElement} */ (ts).value = String(Date.now());
  const date = /** @type {HTMLInputElement | null} */ (control('date'));
  if (date) date.min = todayInIndia();

  status.addEventListener('click', (e) => {
    const link = /** @type {HTMLElement} */ (e.target).closest('a[href^="#"]');
    if (!link) return;
    e.preventDefault();
    const target = /** @type {HTMLElement | null} */ (form.querySelector(link.getAttribute('href')));
    if (target) target.focus();
  });

  form.addEventListener('input', (e) => {
    const name = /** @type {HTMLInputElement} */ (e.target).name;
    saveDraft();
    if (touched.has(name) || control(name)?.getAttribute('aria-invalid')) showFieldError(name, validate()[name]);
  });
  form.addEventListener('change', saveDraft);
  // Showing an error on blur moves the fields below it. If the blur came from a click
  // (e.g. on the consent box), wait for the pointer to lift so that click is not lost.
  let pointerDown = false;
  const pending = new Set();
  const flush = () => { pending.forEach((n) => showFieldError(n, validate()[n])); pending.clear(); };
  form.addEventListener('pointerdown', () => { pointerDown = true; });
  document.addEventListener('pointerup', () => { if (pointerDown) { pointerDown = false; setTimeout(flush, 0); } });
  document.addEventListener('pointercancel', () => { pointerDown = false; flush(); });
  form.addEventListener('focusout', (e) => {
    const el = /** @type {HTMLInputElement} */ (e.target);
    if (!present.includes(el.name) || (!el.value && el.type !== 'checkbox')) return;
    touched.add(el.name);
    if (pointerDown) pending.add(el.name);
    else showFieldError(el.name, validate()[el.name]);
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (busy) return;
    present.forEach((n) => touched.add(n));
    if (showErrors(validate())) return;
    if (isOffline()) { setStatus('error', escapeHtml(FAILURES.offline) + alternatives(), true); return; }

    setStatus('info', 'Sending your enquiry…');
    setBusy(true);
    const payload = { ...values(), form: control('form').value, page: control('page').value, ts: control('ts').value, sent: String(Date.now()), website: control('website').value };
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
    let leaving = false;
    try {
      const res = await fetch(ENDPOINT, {
        method: 'POST', credentials: 'same-origin', signal: controller.signal,
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(payload),
      });
      const data = await res.json().catch(() => ({}));
      if (res.ok && data.ok) {
        leaving = true;
        storage.remove(draftKey);
        setStatus('success', 'Thank you — your enquiry has been sent.');
        window.location.assign(data.redirect || THANK_YOU);
        return;
      }
      if (res.status === 400 && data.errors && showErrors(data.errors)) return;
      setStatus('error', escapeHtml(FAILURES[data.code] || FAILURES.unknown) + alternatives(), true);
    } catch (err) {
      const reason = /** @type {Error} */ (err).name === 'AbortError' ? 'timeout' : (isOffline() ? 'offline' : 'network');
      setStatus('error', escapeHtml(FAILURES[reason]) + alternatives(), true);
    } finally {
      clearTimeout(timer);
      if (!leaving) setBusy(false);
    }
  });

  // WhatsApp sends nothing to our server, so it skips the bot timer and the consent box.
  if (waButton) {
    waButton.addEventListener('click', () => {
      window.open(`https://wa.me/${whatsapp}?text=${encodeURIComponent(compose())}`, '_blank', 'noopener');
      setStatus('info', 'WhatsApp has opened with your details — just tap send there.');
    });
  }

  // Coming back with the Back button restores the page from cache with buttons still disabled.
  window.addEventListener('pageshow', (e) => { if (e.persisted) { setBusy(false); setStatus('info', ''); status.hidden = true; } });
}

export function initEnquiryForms() {
  document.querySelectorAll('form[data-enquiry-form]').forEach((form) => enhance(/** @type {HTMLFormElement} */ (form)));
}

