# Enquiry email setup — Zoho Mail + Netlify

How it works: the form posts to **`/api/enquiry`** (Netlify Function `netlify/functions/enquiry.mjs`). The function validates the enquiry and sends it **through the client's own Zoho mailbox over SMTP** (`smtp.zoho.in:465`, SSL). Nothing third-party appears in the email.

- **From:** `"Visitor Name via Shubh Caterers Website" <info@shubhcaterers.in>`
- **Reply-To:** the visitor's email (clicking Reply answers the visitor)
- **To:** `info@shubhcaterers.in`
- **Subject:** `New enquiry from {Name}: {Event type}` (`[Possible spam]` is added in front when spam words or several links are found)

Because Zoho's own server sends it from the client's domain, it passes SPF/DKIM/DMARC **once the DNS records below exist**.

---

## ⚠️ 1. DNS is not ready yet (checked 1 Oct 2026)

`shubhcaterers.in` (DNS at **GoDaddy**) currently has **no MX record, no SPF record and no Zoho DKIM record**, but it *does* have a DMARC policy `p=quarantine`. Until this is fixed:

- mail sent **to** info@shubhcaterers.in cannot be delivered (no MX), and
- mail sent **from** it would fail DMARC and go to spam/quarantine.

Add these in **GoDaddy → My Products → shubhcaterers.in → DNS → Add New Record**. Take the exact values from **Zoho Mail Admin Console → Domains → shubhcaterers.in → Email configuration** (Zoho shows them for your account; the ones below are Zoho India's standard values):

| Type | Name | Value | Priority |
|---|---|---|---|
| TXT | `@` | `zoho-verification=zb……zmverify.zoho.in` (from Zoho, only if the domain is not verified yet) | — |
| MX | `@` | `mx.zoho.in` | 10 |
| MX | `@` | `mx2.zoho.in` | 20 |
| MX | `@` | `mx3.zoho.in` | 50 |
| TXT | `@` | `v=spf1 include:zohomail.in ~all` | — |
| TXT | `zmail._domainkey` (selector shown by Zoho) | `v=DKIM1; k=rsa; p=MIGf…` (copy from Zoho → *DKIM* → *Add selector*, then click **Verify** in Zoho) | — |

Keep the existing `_dmarc` record. Optionally change its `rua=` address from GoDaddy's default (`dmarc_rua@onsecureserver.net`) to an address the client reads.

Check with: `nslookup -type=MX shubhcaterers.in 8.8.8.8` and `nslookup -type=TXT shubhcaterers.in 8.8.8.8`.

**Zoho plan:** SMTP access needs a Zoho plan that allows SMTP/IMAP (e.g. *Mail Lite* or higher). Confirm in Zoho Admin Console that SMTP is available for `info@shubhcaterers.in` (the Forever-Free plan has historically not included IMAP/POP/SMTP access).

---

## 2. Create a Zoho app password

1. Log in to <https://accounts.zoho.in> as **info@shubhcaterers.in**.
2. **Security → App Passwords → Generate New Password**, name it `Netlify website form`.
3. Copy the password (shown once). This is **SMTP_PASS**. (If two-factor sign-in is off, Zoho may also accept the normal password, but an app password is safer and can be revoked on its own.)

---

## 3. Netlify environment variables

Netlify → site **shubh-caterers** → **Site configuration → Environment variables → Add a variable → Add a single variable**. For each one:

| Key | Value | Scopes | Deploy contexts | Secret? |
|---|---|---|---|---|
| `SMTP_HOST` | `smtp.zoho.in` | **Functions** | All | No |
| `SMTP_PORT` | `465` | **Functions** | All | No |
| `SMTP_USER` | `info@shubhcaterers.in` | **Functions** | All | No |
| `SMTP_PASS` | *(Zoho app password)* | **Functions** | **Production only** | **Yes — tick "Contains secret values"** |
| `MAIL_TO` | `info@shubhcaterers.in` | **Functions** | All | No |
| `MAIL_FROM` | `info@shubhcaterers.in` | **Functions** | All | No |

- For scopes choose **"Specific scopes" → Functions** (Builds/Runtime are not needed).
- For `SMTP_PASS` choose **"Different value for each deploy context"** / **Production** only, leave the others empty. Deploy previews then return a friendly "temporarily unavailable — call/WhatsApp/email us" message instead of sending email.
- After saving, **redeploy**: *Deploys → Trigger deploy → Deploy site* (environment variables only reach functions on the next deploy).

Never put these values in git. `.env.example` lists the keys with empty secrets.

---

## 4. One live test (after DNS + variables + redeploy)

1. Open <https://shubhcaterers.in/contact/>, wait a few seconds, fill the form with **your own** email, tick the consent box, press **Send Enquiry**.
2. You should land on `/thank-you/`.
3. In Zoho Mail (info@shubhcaterers.in) the email should be in the **Inbox** with sender *"Your Name via Shubh Caterers Website"*. Press **Reply** — it must address your email.
4. If it fails: Netlify → *Logs → Functions → enquiry* shows `missing environment variables` (500) or `SMTP send failed` (502, usually a wrong app password or SMTP not enabled in the Zoho plan).

---

## Spam protection (server-side)

- Hidden honeypot field `website` and a minimum 3-second fill time (page-load → submit, measured on the visitor's clock). Both are **silently accepted and discarded**.
- Origin allow-list: `https://shubhcaterers.in`, `https://www.shubhcaterers.in`, `https://shubh-caterers.netlify.app`, Netlify deploy previews, `localhost`. Add more with `ALLOWED_ORIGINS`.
- Rate limit: 5 enquiries per 10 minutes per IP (stored as a salted hash in Netlify Blobs for 10 minutes).
- Server-side validation of every field and consent, length limits, header-injection protection, HTML escaping, and `[Possible spam]` subject flag instead of dropping.

## FormSubmit fallback

Not used. A server-side function on the actual host is available (Netlify Functions), so no third-party form service, branding or activation email is involved.
