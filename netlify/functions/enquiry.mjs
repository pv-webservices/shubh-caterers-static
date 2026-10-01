// Netlify Function: POST /api/enquiry
// Secrets come only from Netlify environment variables (see .env.example and README).
import nodemailer from 'nodemailer';
import { createHandler } from '../lib/enquiry-handler.mjs';
import { blobsStore, createRateLimiter, memoryStore } from '../lib/rate-limit.mjs';

let limiter;
async function getRateLimiter() {
  if (!limiter) {
    let store;
    try {
      store = await blobsStore();
    } catch (err) {
      console.warn('enquiry: Netlify Blobs unavailable, using in-memory rate limit', err);
      store = memoryStore();
    }
    limiter = createRateLimiter(store);
  }
  return limiter;
}

export default createHandler({ env: process.env, createTransport: nodemailer.createTransport, getRateLimiter });

export const config = { path: '/api/enquiry' };
