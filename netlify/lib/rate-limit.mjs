// Per-IP rate limit: at most `limit` enquiries per `windowMs`.
// Uses Netlify Blobs on the live site so the count survives cold starts; falls back to memory.
import { createHash } from 'node:crypto';

export const RATE_LIMIT = { limit: 5, windowMs: 10 * 60 * 1000 };

/** IPs are stored only as a salted hash. */
export const hashIp = (ip, salt = 'shubh-caterers') => createHash('sha256').update(`${salt}:${ip}`).digest('hex').slice(0, 32);

export function memoryStore() {
  const map = new Map();
  return {
    async get(key) { return map.get(key) ?? null; },
    async set(key, value) { map.set(key, value); },
  };
}

export async function blobsStore() {
  const { getStore } = await import('@netlify/blobs');
  const store = getStore({ name: 'enquiry-rate-limit', consistency: 'strong' });
  return {
    async get(key) { return store.get(key, { type: 'json' }); },
    async set(key, value) { await store.setJSON(key, value); },
  };
}

/**
 * @param {{ get(key: string): Promise<number[] | null>, set(key: string, value: number[]): Promise<void> }} store
 */
export function createRateLimiter(store, { limit, windowMs } = RATE_LIMIT) {
  return {
    /** Records a hit and returns whether the caller is still within the limit. */
    async hit(ip, now = Date.now()) {
      const key = hashIp(ip || 'unknown');
      const recent = ((await store.get(key)) || []).filter((t) => now - t < windowMs);
      if (recent.length >= limit) return { allowed: false, retryAfter: Math.ceil((recent[0] + windowMs - now) / 1000) };
      await store.set(key, [...recent, now]);
      return { allowed: true, retryAfter: 0 };
    },
  };
}
