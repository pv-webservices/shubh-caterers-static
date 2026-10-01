// Unit tests for the validation rules shared by the browser and the function.
import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import { clean, todayInIndia, validateEnquiry } from '../../assets/js/enquiry-rules.js';

const base = { name: 'Asha', email: 'asha@example.com', phone: '9876543210', message: 'Lunch for forty people.', consent: 'on' };
const errorsFor = (overrides, today = '2026-10-01') => Object.keys(validateEnquiry({ ...base, ...overrides }, { today }).errors);

describe('validateEnquiry', () => {
  it('accepts a minimal valid enquiry', () => assert.deepEqual(errorsFor({}), []));

  it('checks minimum lengths by hand (autofill does not trigger tooShort)', () => {
    assert.deepEqual(errorsFor({ name: ' A ' }), ['name']);
    assert.deepEqual(errorsFor({ message: 'too short' }), ['message']);
  });

  it('validates email format', () => {
    for (const email of ['asha', 'asha@', 'asha@example', 'a b@example.com', 'asha@example.c']) assert.deepEqual(errorsFor({ email }), ['email'], email);
    assert.deepEqual(errorsFor({ email: 'first.last+tag@sub.example.co.in' }), []);
  });

  it('requires 10 to 15 phone digits', () => {
    assert.deepEqual(errorsFor({ phone: '987654321' }), ['phone']);
    assert.deepEqual(errorsFor({ phone: '+91 98765-43210' }), []);
    assert.deepEqual(errorsFor({ phone: '1234567890123456' }), ['phone']);
    assert.deepEqual(errorsFor({ phone: '98765abc43210' }), ['phone']);
  });

  it('rejects past and impossible dates but allows today', () => {
    assert.deepEqual(errorsFor({ date: '2026-09-30' }), ['date']);
    assert.deepEqual(errorsFor({ date: '2026-02-30' }), ['date']);
    assert.deepEqual(errorsFor({ date: '2026-10-01' }), []);
  });

  it('requires consent', () => assert.deepEqual(errorsFor({ consent: '' }), ['consent']));

  it('limits event type to the known list when given one', () => {
    assert.deepEqual(Object.keys(validateEnquiry({ ...base, event: 'Rave' }, { today: '2026-10-01', eventTypes: ['Weddings'] }).errors), ['event']);
  });
});

describe('helpers', () => {
  it('clean() removes control characters and line breaks from single-line fields', () => {
    assert.equal(clean('Asha\r\nBcc: x@y.z\u0007'), 'Asha Bcc: x@y.z');
    assert.equal(clean('line 1\r\nline 2', { multiline: true }), 'line 1\nline 2');
  });

  it('todayInIndia() uses Asia/Kolkata', () => {
    assert.equal(todayInIndia(new Date('2026-09-30T19:00:00Z')), '2026-10-01');
  });
});
