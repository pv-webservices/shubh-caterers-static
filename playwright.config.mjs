// End-to-end tests against `netlify dev` (serves dist/ with _redirects, headers and the function).
// The enquiry endpoint is intercepted in every form test, so no email is ever sent.
import { defineConfig, devices } from '@playwright/test';

const PORT = 8888;

export default defineConfig({
  testDir: 'tests/e2e',
  timeout: 60_000,
  fullyParallel: true,
  workers: 2,   // the local netlify dev proxy times out with more
  reporter: [['list']],
  use: { baseURL: `http://localhost:${PORT}`, trace: 'retain-on-failure' },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
  webServer: {
    command: `npx netlify dev --offline --port ${PORT}`,
    url: `http://localhost:${PORT}/`,
    reuseExistingServer: true,
    timeout: 120_000,
  },
});
