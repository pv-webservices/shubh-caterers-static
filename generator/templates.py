"""Shared layout pieces for every page. URLs are root-relative with a trailing slash (/about/)."""
from datetime import datetime
from html import escape
from pathlib import Path
import json

from icons import icon, ORNAMENT
from site_data import BUSINESS, SERVICES

ROOT = Path(__file__).resolve().parent.parent
PAGES_DIR = ROOT / 'pages'
IMAGES = json.loads((ROOT / 'assets' / 'images' / 'manifest.json').read_text(encoding='utf-8'))
SITE = BUSINESS['domain']
ORG_ID = f'{SITE}/#organization'
WEBSITE_ID = f'{SITE}/#website'

NAV = [
    ('/', 'Home'), ('/about/', 'About Us'), ('/services/', 'Our Services'), ('/menu/', 'Menu'),
    ('/gallery/', 'Gallery'), ('/testimonials/', 'Testimonials'), ('/contact/', 'Contact Us'),
]
PHONE_1, PHONE_2 = BUSINESS['phones'][0][1], BUSINESS['phones'][1][1]
WA_URL = f"https://wa.me/{BUSINESS['whatsapp']}"
MAP_URL = BUSINESS['map_url']
CRITICAL_FONTS = ['poppins-latin-400-normal.woff2', 'playfair-display-latin-600-normal.woff2']
LOGO = ('/assets/images/brand/logo-240.webp', '/assets/images/brand/logo-480.webp', 240, 94)


def service_url(slug):
    return f'/services/{slug}/'


def image_url(name, width=None):
    meta = IMAGES[name]
    return f"/assets/images/{name}-{width or meta['widths'][-1]}.webp"


def img(name, alt, sizes='100vw', cls='', eager=False, defer=False):
    """Responsive AVIF + WebP <picture> with intrinsic width/height (no layout shift).

    eager: the LCP image (fetchpriority=high). defer: loaded by JS after the page has loaded."""
    meta = IMAGES[name]
    widths = meta['widths']
    base = f'/assets/images/{name}'
    avif = ', '.join(f'{base}-{w}.avif {w}w' for w in widths)
    webp = ', '.join(f'{base}-{w}.webp {w}w' for w in widths)
    fallback = f'{base}-{widths[min(1, len(widths) - 1)]}.webp'
    pre = 'data-' if defer else ''
    loading = ' fetchpriority="high"' if eager else ('' if defer else ' loading="lazy"')
    cls_attr = f' class="{cls}"' if cls else ''
    return (f'<picture{" data-defer" if defer else ""}><source type="image/avif" {pre}srcset="{avif}" sizes="{sizes}">'
            f'<img{cls_attr} {pre}src="{fallback}" {pre}srcset="{webp}" sizes="{sizes}" width="{meta["width"]}" height="{meta["height"]}" '
            f'alt="{escape(alt)}"{loading} decoding="async"></picture>')


def logo_img(sizes, lazy=False):
    small, large, w, h = LOGO
    return (f'<img src="{small}" srcset="{small} 240w, {large} 480w" sizes="{sizes}" width="{w}" height="{h}" alt="Shubh Caterers"'
            f'{" loading=\"lazy\"" if lazy else ""} decoding="async">')


def btn(label, href, kind='primary', ic='arrow', extra=''):
    arrow = f'<span class="btn-ic">{icon(ic, 16, stroke=2)}</span>' if ic else ''
    return f'<a class="btn btn-{kind}" href="{href}"{extra}><span class="btn-label">{label}</span>{arrow}</a>'


def heading(eyebrow, title, accent='', text='', light=False, left=False, level=2):
    classes = 'section-heading' + (' light' if light else '') + (' left' if left else '')
    accent_html = f' <em>{accent}</em>' if accent else ''
    copy = f'<p class="section-copy">{text}</p>' if text else ''
    return f'<div class="{classes}" data-reveal>{ORNAMENT}<p class="eyebrow">{eyebrow}</p><h{level}>{title}{accent_html}</h{level}>{copy}</div>'


def topbar():
    return f'''<div class="topbar"><div class="container topbar-inner">
<div class="topbar-group"><a href="tel:+91{PHONE_1}">{icon('phone', 14)} {PHONE_1}</a><span class="sep" aria-hidden="true">|</span><a href="tel:+91{PHONE_2}">{PHONE_2}</a><span class="sep hide-sm" aria-hidden="true">|</span><a class="hide-sm" href="mailto:{BUSINESS['email']}">{icon('mail', 14)} {BUSINESS['email']}</a></div>
<a class="topbar-address" href="{MAP_URL}" target="_blank" rel="noopener">{icon('pin', 14)} Bhairvnagar, Dhanori, Pune - 411015</a>
</div></div>'''


def header(active):
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if label == active else ''
        if label == 'Our Services':
            drop = ''.join(f'<a href="{service_url(s[0])}">{icon(s[3], 20)}<span>{escape(s[2])}</span></a>' for s in SERVICES)
            links.append(f'''<div class="nav-item has-drop"><a class="nav-link" href="{href}"{cur}>{label}</a><button class="drop-toggle" type="button" aria-expanded="false" aria-label="Show services">{icon('arrow', 14, stroke=2)}</button><div class="dropdown"><div class="dropdown-grid">{drop}</div><a class="dropdown-all" href="/services/">View all services {icon('arrow', 14, stroke=2)}</a></div></div>''')
        else:
            links.append(f'<div class="nav-item"><a class="nav-link" href="{href}"{cur}>{label}</a></div>')
    return f'''<header class="site-header" data-header><div class="container nav-wrap">
<a class="brand" href="/" aria-label="Shubh Caterers home">{logo_img('163px')}</a>
<nav class="main-nav" id="mainNav" aria-label="Primary">{''.join(links)}
<div class="nav-mobile-extra"><a class="btn btn-primary" href="/contact/#quote"><span class="btn-label">Get a Free Quote</span></a><div class="nav-mobile-contact"><a href="tel:+91{PHONE_1}">{icon('phone', 18)} {PHONE_1}</a><a href="{WA_URL}" target="_blank" rel="noopener">{icon('whatsapp', 18)} WhatsApp</a></div></div></nav>
{btn('Get a Quote', '/contact/#quote', 'primary nav-cta')}
<button class="menu-toggle" id="menuToggle" type="button" aria-expanded="false" aria-controls="mainNav" aria-label="Open menu"><span></span><span></span><span></span></button>
</div></header><div class="nav-overlay" data-nav-overlay></div>'''


def footer():
    svc = ''.join(f'<li><a href="{service_url(s[0])}">{escape(s[2])}</a></li>' for s in SERVICES)
    quick = ''.join(f'<li><a href="{h}">{l}</a></li>' for h, l in NAV) + '<li><a href="/faq/">FAQ</a></li>'
    return f'''<footer class="footer"><div class="footer-glow" aria-hidden="true"></div>
<div class="container footer-grid">
<div class="footer-brand"><a class="footer-logo" href="/" aria-label="Shubh Caterers home">{logo_img('200px', lazy=True)}</a>
<p>Delicious food. Beautiful moments. Unforgettable celebrations.</p><p class="muted">Shubh Caterers — 100% pure vegetarian catering for weddings, corporate events and every special occasion in Pune.</p>
<div class="socials"><a href="{WA_URL}" target="_blank" rel="noopener" aria-label="WhatsApp">{icon('whatsapp', 18)}</a><a href="tel:+91{PHONE_1}" aria-label="Call {PHONE_1}">{icon('phone', 18)}</a><a href="mailto:{BUSINESS['email']}" aria-label="Email {BUSINESS['email']}">{icon('mail', 18)}</a><a href="{MAP_URL}" target="_blank" rel="noopener" aria-label="Google Maps">{icon('map', 18)}</a></div></div>
<div><h2 class="footer-title">Quick Links</h2><ul>{quick}</ul></div>
<div><h2 class="footer-title">Our Services</h2><ul class="two-col-list">{svc}</ul></div>
<div><h2 class="footer-title">Get in Touch</h2><ul class="footer-contact">
<li>{icon('phone', 18)}<span><a href="tel:+91{PHONE_1}">{PHONE_1}</a> ({BUSINESS['phones'][0][0]})<br><a href="tel:+91{PHONE_2}">{PHONE_2}</a> ({BUSINESS['phones'][1][0]})</span></li>
<li>{icon('mail', 18)}<a href="mailto:{BUSINESS['email']}">{BUSINESS['email']}</a></li>
<li>{icon('pin', 18)}<a href="{MAP_URL}" target="_blank" rel="noopener">{'<br>'.join(BUSINESS['address_lines'])}</a></li></ul></div>
</div>
<div class="footer-bottom"><div class="container"><span>© {datetime.now().year} Shubh Caterers. All Rights Reserved.</span><span>Designed with <span class="heart" aria-hidden="true">♥</span> for memorable celebrations · <a href="/privacy/">Privacy Policy</a></span></div></div></footer>'''


def floating():
    return f'''<a class="wa-fab" href="{WA_URL}?text=Hi%20Shubh%20Caterers%2C%20I%27d%20like%20to%20enquire%20about%20catering." target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{icon('whatsapp', 28)}</a>
<button class="to-top" type="button" data-to-top aria-label="Back to top">{icon('arrow', 18, stroke=2)}</button>
<nav class="mobile-bar" aria-label="Quick actions"><a href="tel:+91{PHONE_1}">{icon('phone', 20)}<span>Call</span></a><a href="{WA_URL}" target="_blank" rel="noopener">{icon('whatsapp', 20)}<span>WhatsApp</span></a><a class="mb-quote" href="/contact/#quote">{icon('calendar', 20)}<span>Get Quote</span></a></nav>
<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Media viewer" hidden>
<button class="lb-btn lb-close" type="button" data-lb-close aria-label="Close">{icon('close', 22, stroke=2)}</button>
<button class="lb-btn lb-prev" type="button" data-lb-prev aria-label="Previous">{icon('arrow-left', 22, stroke=2)}</button>
<button class="lb-btn lb-next" type="button" data-lb-next aria-label="Next">{icon('arrow', 22, stroke=2)}</button>
<figure class="lb-figure"><div class="lb-media"></div><figcaption class="lb-caption"></figcaption></figure></div>'''


# ---------------------------------------------------------------- enquiry form
EVENT_TYPES = [s[2] if s[2] != 'Cocktails' else 'Cocktail / Sangeet' for s in SERVICES] + ['Other']


def _field(fid, name, label, control, required=False):
    star = ' <span class="req" aria-hidden="true">*</span>' if required else ' <span class="opt">(optional)</span>'
    return (f'<div class="field" data-field="{name}"><label for="{fid}-{name}">{label}{star}</label>{control}'
            f'<p class="field-error" id="{fid}-{name}-error" hidden></p></div>')


def quote_form(page_path, kind='enquiry'):
    """Works without JavaScript (POST + 303 to /thank-you/); main.js adds inline validation and fetch()."""
    fid = 'quote' if kind == 'quote' else 'enquiry'
    options = ''.join(f'<option>{escape(e)}</option>' for e in EVENT_TYPES)
    fields = [
        _field(fid, 'name', 'Your name', f'<input id="{fid}-name" name="name" required minlength="2" maxlength="80" autocomplete="name">', True),
        _field(fid, 'phone', 'Phone number', f'<input id="{fid}-phone" name="phone" type="tel" required maxlength="25" autocomplete="tel" inputmode="tel">', True),
        _field(fid, 'email', 'Email address', f'<input id="{fid}-email" name="email" type="email" required maxlength="254" autocomplete="email" spellcheck="false">', True),
        _field(fid, 'event', 'Event type', f'<select id="{fid}-event" name="event"><option value="">Select event</option>{options}</select>'),
    ]
    if kind == 'quote':
        fields += [
            _field(fid, 'date', 'Event date', f'<input id="{fid}-date" name="date" type="date">'),
            _field(fid, 'guests', 'Approx. guests', f'<input id="{fid}-guests" name="guests" type="number" min="1" max="100000" step="1" inputmode="numeric">'),
        ]
    message = _field(fid, 'message', 'Message / event details', f'<textarea id="{fid}-message" name="message" rows="3" required minlength="10" maxlength="2000" placeholder="Venue, preferred menu, live counters…"></textarea>', True)
    consent = (f'<div class="field field-check" data-field="consent"><input id="{fid}-consent" name="consent" type="checkbox" value="yes" required>'
               f'<label for="{fid}-consent">I agree to the <a href="/privacy/">privacy policy</a> and to Shubh Caterers contacting me about this enquiry. <span class="req" aria-hidden="true">*</span></label>'
               f'<p class="field-error" id="{fid}-consent-error" hidden></p></div>')
    return f'''<form class="quote-form" id="{fid}-form" action="/api/enquiry" method="post" novalidate data-enquiry-form data-phone="{PHONE_1}" data-email="{BUSINESS['email']}" data-whatsapp="{BUSINESS['whatsapp']}">
<input type="hidden" name="form" value="{kind}"><input type="hidden" name="page" value="{page_path}"><input type="hidden" name="ts" value="">
<div class="hp-field" aria-hidden="true"><label for="{fid}-website">Leave this field empty</label><input id="{fid}-website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
<div class="form-status" role="status" aria-live="polite" tabindex="-1" hidden></div>
<div class="form-grid">{''.join(fields)}</div>
{message}{consent}
<div class="form-actions"><button class="btn btn-primary btn-block" type="submit" data-submit><span class="btn-label">Send Enquiry</span><span class="btn-ic">{icon('arrow', 16, stroke=2)}</span></button>
<button class="btn btn-outline btn-block js-only" type="button" data-whatsapp><span class="btn-label">Send via WhatsApp</span><span class="btn-ic">{icon('whatsapp', 16)}</span></button></div>
<p class="form-note">Fields marked * are required. Prefer to talk? Call <a href="tel:+91{PHONE_1}">{PHONE_1}</a> or email <a href="mailto:{BUSINESS['email']}">{BUSINESS['email']}</a>.</p>
</form>'''


def inquiry(page_path):
    return f'''<section class="inquiry-band" id="enquire" aria-labelledby="enquire-title"><div class="inquiry-pattern" aria-hidden="true"></div><div class="container inquiry-grid">
<div class="inquiry-copy" data-reveal="left"><p class="eyebrow gold">Let’s plan together</p><h2 id="enquire-title">Plan Your Next Event<br><em>with Shubh Caterers</em></h2>
<p>Let’s create a memorable experience with delicious pure-vegetarian food and seamless service.</p>
<div class="contact-tiles"><a class="contact-tile" href="tel:+91{PHONE_1}"><span class="ct-ic">{icon('phone', 22)}</span><span><small>Call us</small>{PHONE_1}<br>{PHONE_2}</span></a>
<a class="contact-tile" href="mailto:{BUSINESS['email']}"><span class="ct-ic">{icon('mail', 22)}</span><span><small>Email us</small>{BUSINESS['email']}</span></a>
<a class="contact-tile wide" href="{MAP_URL}" target="_blank" rel="noopener"><span class="ct-ic">{icon('pin', 22)}</span><span><small>Visit us</small>{BUSINESS['address_short']}</span></a></div></div>
<div class="quote-card" data-reveal="right"><h3>Get a Free Quote</h3><p class="quote-sub">Free, no-obligation quote</p>{quote_form(page_path)}</div>
</div></section>'''


def page_hero(title, accent, text, image, crumbs):
    """crumbs: [(url, label), ...] ending with the current page."""
    trail = ''.join(f'<li><a href="{h}">{escape(l)}</a></li>' for h, l in crumbs[:-1])
    return f'''<section class="page-hero"><div class="page-hero-media">{img(image, '', eager=True)}</div><div class="page-hero-shade"></div>
<div class="container page-hero-inner"><nav aria-label="Breadcrumb"><ol class="crumbs">{trail}<li aria-current="page">{escape(crumbs[-1][1])}</li></ol></nav>
<h1 class="split-in">{escape(title)}{f" <em>{escape(accent)}</em>" if accent else ""}</h1><p>{escape(text)}</p>
<div class="hero-actions">{btn('Get a Free Quote', '/contact/#quote')}{btn('Call ' + PHONE_1, f'tel:+91{PHONE_1}', 'ghost', 'phone')}</div></div>
<svg class="hero-curve" viewBox="0 0 1440 60" preserveAspectRatio="none" aria-hidden="true"><path d="M0 60V30C240 0 480 0 720 22s480 40 720 8v30z"/></svg></section>'''


# ---------------------------------------------------------------- structured data
FOUNDERS = [('pawan-agarwal', 'Pawan Agarwal', PHONE_1), ('ajay-agarwal', 'Ajay Agarwal', PHONE_2)]


def schema_graph(page):
    url = SITE + page['path']
    lat, lng = (float(x) for x in BUSINESS['map_coords'].split(','))
    org = {
        '@type': 'FoodEstablishment', '@id': ORG_ID, 'name': BUSINESS['name'], 'url': SITE + '/',
        'description': 'Pure vegetarian catering for weddings, corporate events and celebrations in Pune.',
        'logo': {'@type': 'ImageObject', 'url': SITE + LOGO[1], 'width': 480, 'height': 189},
        'image': SITE + '/assets/images/og/wedding-buffet-night.jpg',
        'telephone': f'+91-{PHONE_1}', 'email': BUSINESS['email'],
        'address': {'@type': 'PostalAddress', 'streetAddress': 'Sr. No. 51, Plot No. 117, Lane No. 9, Bhairvnagar, Dhanori',
                    'addressLocality': 'Pune', 'postalCode': '411015', 'addressRegion': 'Maharashtra', 'addressCountry': 'IN'},
        'geo': {'@type': 'GeoCoordinates', 'latitude': lat, 'longitude': lng},
        'hasMap': MAP_URL, 'areaServed': {'@type': 'City', 'name': 'Pune'},
        'servesCuisine': ['Vegetarian', 'North Indian', 'Maharashtrian', 'South Indian', 'Indo-Chinese'],
        'founder': [{'@id': f'{SITE}/about/#{slug}'} for slug, _, _ in FOUNDERS],
    }
    people = [{'@type': 'Person', '@id': f'{SITE}/about/#{slug}', 'name': name, 'telephone': f'+91-{phone}', 'worksFor': {'@id': ORG_ID}}
              for slug, name, phone in FOUNDERS]
    website = {'@type': 'WebSite', '@id': WEBSITE_ID, 'url': SITE + '/', 'name': BUSINESS['name'], 'inLanguage': 'en-IN', 'publisher': {'@id': ORG_ID}}
    graph = [org, *people, website]
    if not page['indexable']:
        return graph
    webpage = {'@type': page.get('page_type', 'WebPage'), '@id': url + '#webpage', 'url': url, 'name': page['title'],
               'description': page['description'], 'isPartOf': {'@id': WEBSITE_ID}, 'about': {'@id': ORG_ID}, 'inLanguage': 'en-IN',
               'primaryImageOfPage': {'@type': 'ImageObject', 'url': SITE + page['og_image']}}
    graph.append(webpage)
    if len(page['crumbs']) > 1:
        webpage['breadcrumb'] = {'@id': url + '#breadcrumb'}
        graph.append({'@type': 'BreadcrumbList', '@id': url + '#breadcrumb', 'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'name': label, 'item': SITE + href} for i, (href, label) in enumerate(page['crumbs'])]})
    graph.extend(page.get('schema', []))
    return graph


def json_ld(graph):
    data = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, separators=(',', ':'))
    return '<script type="application/ld+json">' + data.replace('<', '\\u003c') + '</script>'


def faq_schema(url, faqs):
    return {'@type': 'FAQPage', '@id': url + '#faq', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faqs]}


# ---------------------------------------------------------------- document
def head(page):
    title, desc = escape(page['title']), escape(page['description'])
    url = SITE + page['path']
    og_image = SITE + page['og_image']
    og_alt = escape(page.get('og_alt', 'Shubh Caterers — pure vegetarian catering in Pune'))
    if page['indexable']:
        seo = f'<meta name="robots" content="index, follow, max-image-preview:large">\n<link rel="canonical" href="{url}">\n<meta property="og:url" content="{url}">'
    else:
        seo = '<meta name="robots" content="noindex, follow">'
    fonts = ''.join(f'<link rel="preload" href="/assets/fonts/{f}" as="font" type="font/woff2" crossorigin>' for f in CRITICAL_FONTS)
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
{seo}
<meta name="theme-color" content="#7a0c0c">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png" type="image/png" sizes="96x96">
<link rel="icon" href="/favicon-48x48.png" type="image/png" sizes="48x48">
<link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">
<link rel="manifest" href="/site.webmanifest">
{fonts}
<link rel="stylesheet" href="/assets/css/site.css">
<meta property="og:site_name" content="Shubh Caterers">
<meta property="og:locale" content="en_IN">
<meta property="og:type" content="{page.get('og_type', 'website')}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{og_alt}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_image}">
<meta name="twitter:image:alt" content="{og_alt}">
{json_ld(schema_graph(page))}'''


def document(page):
    """page: dict(path, title, description, body, active, crumbs, og_image, indexable, schema, page_type)."""
    return f'''<!doctype html>
<html lang="en-IN">
<head>
{head(page)}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
{topbar()}{header(page.get('active', ''))}
<main id="main" tabindex="-1">{page['body']}</main>
{footer()}{floating()}
<script src="/assets/js/main.js" defer></script>
</body>
</html>
'''
