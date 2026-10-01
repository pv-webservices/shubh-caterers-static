# Google Search Console — launch guide for shubhcaterers.in

Canonical site: **https://shubhcaterers.in/** (no `www`, HTTPS, trailing slash on every page).
Hosting: Netlify (auto-deploys from GitHub `main`). DNS: **GoDaddy** (nameservers `ns41/ns42.domaincontrol.com`).

---

## 1. Pre-launch checklist (on the live domain, after the deploy)

Run these from any terminal (or open the URLs in a browser). Every line should match.

| Check | Command | Expected |
|---|---|---|
| HTTPS redirect | `curl -sI http://shubhcaterers.in/` | `301` → `https://shubhcaterers.in/` |
| www redirect | `curl -sI https://www.shubhcaterers.in/about/` | `301` → `https://shubhcaterers.in/about/` |
| Old URLs | `curl -sI https://shubhcaterers.in/about.html` | `301` → `/about/` |
| `/index.html` | `curl -sI https://shubhcaterers.in/index.html` | `301` → `/` |
| robots.txt | `curl -s https://shubhcaterers.in/robots.txt` | `Allow: /` and `Sitemap: https://shubhcaterers.in/sitemap-index.xml` |
| Sitemap | `curl -sI https://shubhcaterers.in/sitemap-index.xml` | `200`, `application/xml` |
| 404 status | `curl -sI https://shubhcaterers.in/this-does-not-exist/` | `404` (branded page) |
| Favicon | `curl -sI https://shubhcaterers.in/favicon.ico` | `200` |
| No noindex on live | `curl -sI https://shubhcaterers.in/ \| grep -i robots` | nothing (only drafts/previews get `noindex`) |
| Form | Send one test enquiry from `/contact/` | lands on `/thank-you/`, email arrives in the **Inbox** of info@shubhcaterers.in |

> The form email depends on Zoho DNS records (MX, SPF, DKIM) — see [EMAIL-SETUP.md](EMAIL-SETUP.md). Do the form test only after those are live.

---

## 2. Add a Domain property (DNS TXT verification at GoDaddy)

A **Domain** property covers `https://`, `http://`, `www` and every subdomain in one place.

1. Open <https://search.google.com/search-console> → **Add property** → choose **Domain** → type `shubhcaterers.in` → **Continue**.
2. Google shows a TXT record like `google-site-verification=AbC123…`. Click **Copy**.
3. In GoDaddy: sign in → **My Products** → next to *shubhcaterers.in* click **DNS** (or *Manage DNS*).
4. **Add New Record** →
   - Type: **TXT**
   - Name / Host: **@**
   - Value: paste the `google-site-verification=…` text
   - TTL: **1 hour** (default is fine)
   → **Save**. Do **not** delete the existing `_dmarc` TXT record or any Zoho records.
5. Back in Search Console click **Verify**. If it fails, wait 10–30 minutes (GoDaddy TTL is 600 s) and click Verify again. Keep the TXT record forever — removing it un-verifies the property.

---

## 3. Submit the sitemap

1. Search Console → **Sitemaps** (left menu).
2. In *Add a new sitemap* type **`sitemap-index.xml`** → **Submit**.

- `sitemap-index.xml` points to `sitemap.xml`, which lists **every indexable page** (it is regenerated on every deploy, with `lastmod` dates from git). You do not need to submit anything else.
- Status **"Couldn't fetch"** or **"Pending"** for up to 24 hours is normal for a new property. Re-check the next day before worrying.
- Opening the sitemap in a browser shows *"This XML file does not appear to have any style information associated with it"* — that is normal for XML and not an error.

---

## 4. Indexable URLs — exactly 20

**Main pages (9)**

1. https://shubhcaterers.in/
2. https://shubhcaterers.in/about/
3. https://shubhcaterers.in/services/
4. https://shubhcaterers.in/menu/
5. https://shubhcaterers.in/gallery/
6. https://shubhcaterers.in/testimonials/
7. https://shubhcaterers.in/contact/
8. https://shubhcaterers.in/faq/
9. https://shubhcaterers.in/privacy/

**Service pages (11)**

10. https://shubhcaterers.in/services/wedding-catering/
11. https://shubhcaterers.in/services/cocktail-events/
12. https://shubhcaterers.in/services/corporate-catering/
13. https://shubhcaterers.in/services/theme-party/
14. https://shubhcaterers.in/services/private-party/
15. https://shubhcaterers.in/services/niche-events/
16. https://shubhcaterers.in/services/institutional-catering/
17. https://shubhcaterers.in/services/birthday-party/
18. https://shubhcaterers.in/services/house-warming/
19. https://shubhcaterers.in/services/parcels/
20. https://shubhcaterers.in/services/baby-shower/

### Manual "Request indexing" (URL Inspection → paste URL → *Request indexing*)

Google limits manual requests (roughly 10 a day), so use two batches:

- **Day 1 (10):** `/`, `/services/`, `/menu/`, `/contact/`, `/about/`, `/services/wedding-catering/`, `/services/corporate-catering/`, `/services/birthday-party/`, `/services/house-warming/`, `/faq/`
- **Day 2 (10):** `/gallery/`, `/testimonials/`, `/services/cocktail-events/`, `/services/private-party/`, `/services/baby-shower/`, `/services/theme-party/`, `/services/parcels/`, `/services/institutional-catering/`, `/services/niche-events/`, `/privacy/`

Requesting the **homepage first** also speeds up Google picking up the new favicon.

---

## 5. Do NOT submit these

| URL | Why |
|---|---|
| `/thank-you/` | Utility page after a form send — `noindex, follow`, not in the sitemap |
| `/404.html` (and any missing URL) | Error page — `noindex`, returns HTTP 404 |
| `/api/enquiry` | Form endpoint, not a page |
| `/about.html`, `/services.html`, `/services/*.html`, `/index.html` | Old URLs that now **301-redirect** to the clean URLs. Google will follow the redirects by itself; "Page with redirect" in reports is expected and fine |
| `https://www.shubhcaterers.in/…`, `http://…` | Redirect to the canonical `https://shubhcaterers.in/…` |

robots.txt deliberately does **not** block these pages: Google must be able to crawl them to see the `noindex`.

---

## 6. Weeks 1–4 follow-up

**Week 1**
- *Sitemaps*: status **Success**, "Discovered pages" = 20.
- *Pages* (Indexing → Pages): pages move from "Discovered – currently not indexed" to **Indexed** over days. "Excluded by 'noindex' tag" should show only `/thank-you/` (and maybe the 404 page). "Page with redirect" for the old `.html` URLs is expected.
- Create a **Google Business Profile** (<https://business.google.com>) if the client doesn't have one: name *Shubh Caterers*, category *Caterer*, address Sr. No. 51, Plot No. 117, Lane No. 9, Bhairvnagar, Dhanori, Pune 411015, phone +91 95959 56709, website `https://shubhcaterers.in/`. Keep name/address/phone identical to the website. Verification is usually by postcard, phone or video.

**Week 2**
- *Enhancements*: check **Breadcrumbs** (all inner pages), **FAQ** (FAQ page + service pages) and the **organization/local business** data in *URL Inspection → View crawled page → More info / Rich results*. Fix anything marked *Invalid*. (Google now shows FAQ rich results only for a few authoritative sites, so FAQ snippets may not appear — the markup is still valid.)
- Test a page at <https://search.google.com/test/rich-results>.

**Week 3**
- *Core Web Vitals* report (needs real-user traffic; may say "Not enough data").
- PageSpeed: <https://pagespeed.web.dev/> for `/` and `/services/wedding-catering/` on **Mobile**. Compare with the numbers in the audit report.
- **Bing Webmaster Tools** (<https://www.bing.com/webmasters>): *Import from Google Search Console* (fastest), or add the site and verify with the same GoDaddy TXT method; submit `https://shubhcaterers.in/sitemap-index.xml`.

**Week 4**
- *Performance* report: which queries show impressions (e.g. "pure veg caterers Pune", "wedding catering Dhanori"). Use them to improve titles/descriptions of matching pages.
- *Pages*: any URL still "Crawled – currently not indexed" → improve its unique content and request indexing again.
- Search `site:shubhcaterers.in` in Google and check titles, descriptions and the favicon. The favicon can take **days to weeks** to update in results.
