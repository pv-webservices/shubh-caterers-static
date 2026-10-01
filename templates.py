"""Shared layout pieces for every page. All URLs are relative so the site works from any folder."""
from datetime import datetime
from html import escape
from pathlib import Path
import json

from PIL import Image

from icons import icon, ORNAMENT
from site_data import BUSINESS, SERVICES

ROOT = Path(__file__).parent
IMG_DIR = ROOT / 'assets' / 'img'
_WIDTHS = {}

NAV = [
    ('index.html', 'Home'), ('about.html', 'About Us'), ('services.html', 'Our Services'), ('menu.html', 'Menu'),
    ('gallery.html', 'Gallery'), ('testimonials.html', 'Testimonials'), ('contact.html', 'Contact Us'),
]
PHONE_1, PHONE_2 = BUSINESS['phones'][0][1], BUSINESS['phones'][1][1]
WA_URL = f"https://wa.me/{BUSINESS['whatsapp']}"
MAP_URL = BUSINESS['map_url']


def width_of(name):
    if name not in _WIDTHS:
        with Image.open(IMG_DIR / f'{name}.webp') as im:
            _WIDTHS[name] = im.size
    return _WIDTHS[name]


def img(name, alt, R, sizes='100vw', cls='', eager=False, extra=''):
    """Responsive <img> for a WebP in assets/img (uses the -sm variant when it exists)."""
    w, h = width_of(name)
    src = f'{R}assets/img/{name}.webp'
    srcset = ''
    if (IMG_DIR / f'{name}-sm.webp').exists():
        srcset = f' srcset="{R}assets/img/{name}-sm.webp 640w, {src} {w}w" sizes="{sizes}"'
    loading = ' fetchpriority="high"' if eager else ' loading="lazy"'
    cls_attr = f' class="{cls}"' if cls else ''
    return f'<img{cls_attr} src="{src}"{srcset} width="{w}" height="{h}" alt="{escape(alt)}"{loading} decoding="async"{extra}>'


def btn(label, href, kind='primary', ic='arrow', extra=''):
    arrow = f'<span class="btn-ic">{icon(ic, 16, stroke=2)}</span>' if ic else ''
    return f'<a class="btn btn-{kind}" href="{href}"{extra}><span class="btn-label">{label}</span>{arrow}</a>'


def heading(eyebrow, title, accent='', text='', light=False, left=False):
    classes = 'section-heading' + (' light' if light else '') + (' left' if left else '')
    accent_html = f' <em>{accent}</em>' if accent else ''
    copy = f'<p class="section-copy">{text}</p>' if text else ''
    return f'<div class="{classes}" data-reveal>{ORNAMENT}<p class="eyebrow">{eyebrow}</p><h2>{title}{accent_html}</h2>{copy}</div>'


def topbar():
    return f'''<div class="topbar"><div class="container topbar-inner">
<div class="topbar-group"><a href="tel:+91{PHONE_1}">{icon('phone', 14)} {PHONE_1}</a><span class="sep">|</span><a href="tel:+91{PHONE_2}">{PHONE_2}</a><span class="sep hide-sm">|</span><a class="hide-sm" href="mailto:{BUSINESS['email']}">{icon('mail', 14)} {BUSINESS['email']}</a></div>
<a class="topbar-address" href="{MAP_URL}" target="_blank" rel="noopener">{icon('pin', 14)} Bhairvnagar, Dhanori, Pune - 411015</a>
</div></div>'''


def header(active, R):
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if label == active else ''
        if label == 'Our Services':
            drop = ''.join(f'<a href="{R}services/{s[0]}.html">{icon(s[3], 20)}<span>{escape(s[2])}</span></a>' for s in SERVICES)
            links.append(f'''<div class="nav-item has-drop"><a class="nav-link" href="{R}{href}"{cur}>{label}</a><button class="drop-toggle" aria-expanded="false" aria-label="Show services">{icon('arrow', 14, stroke=2)}</button><div class="dropdown"><div class="dropdown-grid">{drop}</div><a class="dropdown-all" href="{R}services.html">View all services {icon('arrow', 14, stroke=2)}</a></div></div>''')
        else:
            links.append(f'<div class="nav-item"><a class="nav-link" href="{R}{href}"{cur}>{label}</a></div>')
    return f'''<header class="site-header" data-header><div class="container nav-wrap">
<a class="brand" href="{R}index.html" aria-label="Shubh Caterers home"><img src="{R}assets/brand/logo-460.webp" width="460" height="181" alt="Shubh Caterers"></a>
<nav class="main-nav" id="mainNav" aria-label="Primary">{''.join(links)}
<div class="nav-mobile-extra"><a class="btn btn-primary" href="{R}contact.html#quote"><span class="btn-label">Get a Free Quote</span></a><div class="nav-mobile-contact"><a href="tel:+91{PHONE_1}">{icon('phone', 18)} {PHONE_1}</a><a href="{WA_URL}" target="_blank" rel="noopener">{icon('whatsapp', 18)} WhatsApp</a></div></div></nav>
{btn('Get a Quote', f'{R}contact.html#quote', 'primary nav-cta')}
<button class="menu-toggle" id="menuToggle" aria-expanded="false" aria-controls="mainNav" aria-label="Open menu"><span></span><span></span><span></span></button>
</div></header><div class="nav-overlay" data-nav-overlay></div>'''


def footer(R):
    svc = ''.join(f'<li><a href="{R}services/{s[0]}.html">{escape(s[2])}</a></li>' for s in SERVICES)
    quick = ''.join(f'<li><a href="{R}{h}">{l}</a></li>' for h, l in NAV) + f'<li><a href="{R}faq.html">FAQ</a></li>'
    return f'''<footer class="footer"><div class="footer-glow" aria-hidden="true"></div>
<div class="container footer-grid">
<div class="footer-brand"><a class="footer-logo" href="{R}index.html"><img src="{R}assets/brand/logo-460.webp" width="460" height="181" alt="Shubh Caterers" loading="lazy"></a>
<p>Delicious food. Beautiful moments. Unforgettable celebrations.</p><p class="muted">Shubh Caterers — 100% pure vegetarian catering for weddings, corporate events and every special occasion in Pune.</p>
<div class="socials"><a href="{WA_URL}" target="_blank" rel="noopener" aria-label="WhatsApp">{icon('whatsapp', 18)}</a><a href="tel:+91{PHONE_1}" aria-label="Call">{icon('phone', 18)}</a><a href="mailto:{BUSINESS['email']}" aria-label="Email">{icon('mail', 18)}</a><a href="{MAP_URL}" target="_blank" rel="noopener" aria-label="Google Maps">{icon('map', 18)}</a></div></div>
<div><h3>Quick Links</h3><ul>{quick}</ul></div>
<div><h3>Our Services</h3><ul class="two-col-list">{svc}</ul></div>
<div><h3>Get in Touch</h3><ul class="footer-contact">
<li>{icon('phone', 18)}<span><a href="tel:+91{PHONE_1}">{PHONE_1}</a> ({BUSINESS['phones'][0][0]})<br><a href="tel:+91{PHONE_2}">{PHONE_2}</a> ({BUSINESS['phones'][1][0]})</span></li>
<li>{icon('mail', 18)}<a href="mailto:{BUSINESS['email']}">{BUSINESS['email']}</a></li>
<li>{icon('pin', 18)}<a href="{MAP_URL}" target="_blank" rel="noopener">{'<br>'.join(BUSINESS['address_lines'])}</a></li></ul></div>
</div>
<div class="footer-bottom"><div class="container"><span>© {datetime.now().year} Shubh Caterers. All Rights Reserved.</span><span>Designed with <span class="heart">♥</span> for memorable celebrations · <a href="{R}privacy.html">Privacy Policy</a></span></div></div></footer>'''


def floating(R):
    return f'''<a class="wa-fab" href="{WA_URL}?text=Hi%20Shubh%20Caterers%2C%20I%27d%20like%20to%20enquire%20about%20catering." target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{icon('whatsapp', 28)}</a>
<button class="to-top" data-to-top aria-label="Back to top">{icon('arrow', 18, stroke=2)}</button>
<nav class="mobile-bar" aria-label="Quick actions"><a href="tel:+91{PHONE_1}">{icon('phone', 20)}<span>Call</span></a><a href="{WA_URL}" target="_blank" rel="noopener">{icon('whatsapp', 20)}<span>WhatsApp</span></a><a class="mb-quote" href="{R}contact.html#quote">{icon('calendar', 20)}<span>Get Quote</span></a></nav>
<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Media viewer" hidden>
<button class="lb-btn lb-close" data-lb-close aria-label="Close">{icon('close', 22, stroke=2)}</button>
<button class="lb-btn lb-prev" data-lb-prev aria-label="Previous">{icon('arrow-left', 22, stroke=2)}</button>
<button class="lb-btn lb-next" data-lb-next aria-label="Next">{icon('arrow', 22, stroke=2)}</button>
<figure class="lb-figure"><div class="lb-media"></div><figcaption class="lb-caption"></figcaption></figure></div>'''


EVENT_TYPES = [s[2] if s[2] != 'Cocktails' else 'Cocktail / Sangeet' for s in SERVICES] + ['Other']


def quote_form(compact=False):
    options = ''.join(f'<option>{escape(e)}</option>' for e in EVENT_TYPES)
    extra = '' if compact else '''<label class="field"><span>Event Date</span><input type="date" name="date"></label>
<label class="field"><span>Approx. Guests</span><input type="number" name="guests" min="10" step="1" inputmode="numeric" placeholder="e.g. 250"></label>'''
    return f'''<form class="quote-form" data-quote-form novalidate>
<div class="form-grid">
<label class="field"><span>Your Name *</span><input name="name" required autocomplete="name" placeholder="Full name"></label>
<label class="field"><span>Phone Number *</span><input name="phone" type="tel" required autocomplete="tel" inputmode="tel" pattern="[0-9+()\\- ]{{10,15}}" placeholder="10-digit mobile"></label>
<label class="field"><span>Email Address</span><input type="email" name="email" autocomplete="email" placeholder="you@example.com"></label>
<label class="field"><span>Event Type *</span><select name="event" required><option value="">Select event</option>{options}</select></label>
{extra}</div>
<label class="field"><span>Message / Event Details</span><textarea name="message" rows="3" placeholder="Venue, preferred menu, live counters…"></textarea></label>
<button class="btn btn-primary btn-block" type="submit"><span class="btn-label">Send Enquiry on WhatsApp</span><span class="btn-ic">{icon('whatsapp', 16)}</span></button>
<p class="form-note">Your details open in WhatsApp, ready to send to Shubh Caterers. Prefer email? <a href="mailto:{BUSINESS['email']}" data-mail-link>Send by email</a>.</p>
<p class="form-status" role="status" aria-live="polite"></p></form>'''


def inquiry(R):
    return f'''<section class="inquiry-band" id="enquire"><div class="inquiry-pattern" aria-hidden="true"></div><div class="container inquiry-grid">
<div class="inquiry-copy" data-reveal="left"><p class="eyebrow gold">Let’s plan together</p><h2>Plan Your Next Event<br><em>with Shubh Caterers</em></h2>
<p>Let’s create a memorable experience with delicious pure-vegetarian food and seamless service.</p>
<div class="contact-tiles"><a class="contact-tile" href="tel:+91{PHONE_1}"><span class="ct-ic">{icon('phone', 22)}</span><span><small>Call us</small>{PHONE_1}<br>{PHONE_2}</span></a>
<a class="contact-tile" href="mailto:{BUSINESS['email']}"><span class="ct-ic">{icon('mail', 22)}</span><span><small>Email us</small>{BUSINESS['email']}</span></a>
<a class="contact-tile wide" href="{MAP_URL}" target="_blank" rel="noopener"><span class="ct-ic">{icon('pin', 22)}</span><span><small>Visit us</small>{BUSINESS['address_short']}</span></a></div></div>
<div class="quote-card" data-reveal="right"><h3>Get a Free Quote</h3><p class="quote-sub">Quick response · No obligation</p>{quote_form(compact=True)}</div>
</div></section>'''


def page_hero(eyebrow, title, accent, text, image, R, crumbs=()):
    trail = ''.join(f'<li><a href="{R}{h}">{escape(l)}</a></li>' for h, l in crumbs)
    return f'''<section class="page-hero"><div class="page-hero-media">{img(image, '', R, eager=True)}</div><div class="page-hero-shade"></div>
<div class="container page-hero-inner"><nav aria-label="Breadcrumb"><ol class="crumbs"><li><a href="{R}index.html">Home</a></li>{trail}<li aria-current="page">{escape(eyebrow)}</li></ol></nav>
<h1 class="split-in">{escape(title)} <em>{escape(accent)}</em></h1><p>{escape(text)}</p>
<div class="hero-actions">{btn('Get a Free Quote', f'{R}contact.html#quote')}{btn('Call ' + PHONE_1, f'tel:+91{PHONE_1}', 'ghost', 'phone')}</div></div>
<svg class="hero-curve" viewBox="0 0 1440 60" preserveAspectRatio="none" aria-hidden="true"><path d="M0 60V30C240 0 480 0 720 22s480 40 720 8v30z"/></svg></section>'''


def schema_business():
    data = {
        '@context': 'https://schema.org', '@type': 'FoodEstablishment', 'name': 'Shubh Caterers',
        'description': 'Pure vegetarian catering for weddings, corporate events and celebrations in Pune.',
        'servesCuisine': ['Vegetarian', 'North Indian', 'Maharashtrian', 'South Indian', 'Indo-Chinese'],
        'telephone': [f'+91-{PHONE_1}', f'+91-{PHONE_2}'], 'email': BUSINESS['email'],
        'address': {'@type': 'PostalAddress', 'streetAddress': 'Sr. No. 51, Plot No. 117, Lane No. 9, Bhairvnagar, Dhanori',
                    'addressLocality': 'Pune', 'postalCode': '411015', 'addressRegion': 'Maharashtra', 'addressCountry': 'IN'},
        'url': BUSINESS['domain'] + '/',
    }
    return json.dumps(data, ensure_ascii=False)


def document(title, description, body, R, active='', extra_schema=''):
    canonical = BUSINESS['domain'] + '/'
    fonts = 'https://fonts.googleapis.com/css2?family=Great+Vibes&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,500&family=Poppins:wght@300;400;500;600&display=swap'
    schemas = f'<script type="application/ld+json">{schema_business()}</script>' + extra_schema
    return f'''<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(title)} | Shubh Caterers Pune</title>
<meta name="description" content="{escape(description)}">
<meta name="theme-color" content="#7a0c0c">
<meta property="og:type" content="website"><meta property="og:title" content="{escape(title)} | Shubh Caterers">
<meta property="og:description" content="{escape(description)}"><meta property="og:image" content="{canonical}assets/img/hero-buffet.webp">
<link rel="icon" type="image/png" sizes="32x32" href="{R}assets/brand/favicon-32.png"><link rel="apple-touch-icon" href="{R}assets/brand/icon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{fonts}">
<link rel="stylesheet" href="{R}assets/css/base.css"><link rel="stylesheet" href="{R}assets/css/sections.css"><link rel="stylesheet" href="{R}assets/css/pages.css">
{schemas}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
{topbar()}{header(active, R)}
<main id="main">{body}</main>
{footer(R)}{floating(R)}
<script src="{R}assets/js/main.js" defer></script>
</body>
</html>'''
