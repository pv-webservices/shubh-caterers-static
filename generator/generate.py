"""Builds every HTML page of the Shubh Caterers website into pages/.  Run:  python generator/generate.py

Run `python generator/images.py` first when images in source-files/ changed.
The sitemap, robots.txt and _redirects are written by `npm run build` (scripts/build.mjs)."""
from html import escape

from icons import icon, SPRIG
from site_data import (BUSINESS, SERVICES, MENU, CUISINES, VIDEOS, GALLERY, TESTIMONIALS, PROCESS, FAQS, YEARS_OF_SERVICE,
                       CORPORATE_CLIENTS, SOCIETY_CLIENTS)
from templates import (PAGES_DIR, SITE, PHONE_1, PHONE_2, WA_URL, MAP_URL, IMAGES, ORG_ID, img, image_url, btn, heading,
                       inquiry, page_hero, quote_form, document, service_url, faq_schema)

DISH_COUNT = len({d for c in MENU for d in c[4]})
DISHES = f'{DISH_COUNT // 50 * 50}+'
STATS = [(YEARS_OF_SERVICE, '+', 'Years of Service'), (DISH_COUNT // 50 * 50, '+', 'Vegetarian Dishes'),
         (30, '+', 'Live Counter Options'), (100, '%', 'Pure Vegetarian')]
FEATURES = [('sparkle', 'Hygienic Preparation'), ('cloche', 'Customised Menus'), ('team', 'Experienced Team'), ('diamond', 'Quality Ingredients')]
MARQUEE = ['Paneer Tikka', 'Pani Puri', 'Dal Makhani', 'Mango Mastani', 'Masala Dosa', 'Kaju Katli', 'Veg Biryani',
           'Misal Pav', 'Kesar Rabdi', 'Chilli Paneer', 'Puran Puri', 'Pav Bhaji', 'Jalebi', 'Malai Kofta']
HOME = ('/', 'Home')
SERVICE_SEO_TITLES = {
    'wedding-catering': 'Wedding Catering', 'cocktail-events': 'Cocktail & Mocktail Evening Catering',
    'corporate-catering': 'Corporate Catering', 'theme-party': 'Theme Party Catering', 'private-party': 'Private Party Catering',
    'niche-events': 'Niche Event Catering', 'institutional-catering': 'Institutional Catering',
    'birthday-party': 'Birthday Party Catering', 'house-warming': 'House Warming & Pooja Catering',
    'parcels': 'Food Parcel Orders', 'baby-shower': 'Baby Shower Catering',
}
written = []


def og(name):
    return f"/assets/images/og/{name.split('/')[-1]}.jpg"


def write(page):
    path = page['path']
    target = PAGES_DIR / ('404.html' if path == '/404.html' else f"{path.strip('/')}/index.html".lstrip('/'))
    target.parent.mkdir(parents=True, exist_ok=True)
    page.setdefault('indexable', True)
    page.setdefault('crumbs', [HOME])
    target.write_text(document(page), encoding='utf-8')
    written.append(path)


def service_card(s):
    return (f'<a class="service-card tilt" href="{service_url(s[0])}" data-reveal="zoom">'
            f'<span class="service-icon">{icon(s[3], 34, stroke=1.4)}</span><strong>{escape(s[2])}</strong>'
            f'<span class="card-more">Explore {icon("arrow", 14, stroke=2)}</span></a>')


def video_card(v, cls=''):
    slug, title, desc = v
    poster = image_url(f'video-posters/{slug}')
    return (f'<button class="video-card {cls}" type="button" data-lightbox="videos" data-type="video" data-src="/assets/video/{slug}.mp4" '
            f'data-poster="{poster}" data-title="{escape(title)}" aria-label="{escape(title)} {escape(desc)} (play video)" data-reveal>'
            f'<video muted loop playsinline preload="none" poster="{image_url(f"video-posters/{slug}", 480)}" aria-hidden="true" data-lazy-video>'
            f'<source data-src="/assets/video/{slug}-loop.mp4" type="video/mp4"></video>'
            f'<span class="video-play">{icon("play", 22)}</span><span class="video-meta"><strong>{escape(title)}</strong><small>{escape(desc)}</small></span></button>')


def gallery_tile(item, group='gallery'):
    name, title, cat = item
    return (f'<button class="gallery-card" type="button" data-lightbox="{group}" data-type="image" data-src="{image_url(name)}" '
            f'data-title="{escape(title)}" data-category="{escape(cat)}" aria-label="{escape(cat)} {escape(title)} (view larger)">{img(name, title, "(max-width: 640px) 80vw, 360px")}'
            f'<span class="gallery-cap"><small>{escape(cat)}</small><strong>{escape(title)}</strong></span></button>')


def testimonial_card(t):
    quote, name, kind = t
    initials = ''.join(p[0] for p in name.replace('&', '').split()[:2])
    return (f'<figure class="testimonial-card" data-reveal>{icon("quote", 34, "quote-ic")}<div class="stars" role="img" aria-label="5 out of 5 stars">★★★★★</div>'
            f'<blockquote>{escape(quote)}</blockquote><figcaption><span class="avatar" aria-hidden="true">{initials}</span>'
            f'<span><strong>{escape(name)}</strong><small>{escape(kind)}</small></span></figcaption></figure>')


def clients_section():
    corporate = ''.join(f'<li>{icon("briefcase", 20)}{escape(c)}</li>' for c in CORPORATE_CLIENTS)
    societies = ''.join(f'<li>{icon("home", 18)}{escape(c)}</li>' for c in SOCIETY_CLIENTS)
    return f'''<section class="section clients"><div class="container">{heading('Our Clients', f'{YEARS_OF_SERVICE}+ Years of', 'Trusted Service', 'For over three decades, leading organisations and some of Pune’s most respected residential societies have trusted Shubh Caterers with their celebrations.')}
<div class="clients-grid"><div class="client-card client-years" data-reveal="left"><p class="years-mark"><strong><span data-count="{YEARS_OF_SERVICE}">{YEARS_OF_SERVICE}</span>+</strong><span>Years of Catering Excellence</span></p>
<h3>Corporate Clients</h3><ul class="client-list">{corporate}</ul></div>
<div class="client-card" data-reveal="right"><h3>Residential Societies</h3><p>Society festivals, community gatherings and family celebrations at:</p><ul class="client-chips">{societies}<li class="client-more">&amp; many more across Pune</li></ul></div></div></div></section>'''


# ---------------------------------------------------------------- HOME
def home():
    slides = [('venues/wedding-buffet-night', 'Golden buffet counters at a wedding night'), ('venues/reception-dining-hall', 'Elegant reception dining hall'),
              ('food/pure-veg-feast', 'A lavish pure vegetarian feast')]
    slide_html = ''.join(f'<div class="hero-slide{" is-active" if i == 0 else ""}">{img(n, a, eager=(i == 0), defer=(i > 0))}</div>' for i, (n, a) in enumerate(slides))
    tabs = ''.join(f'<button class="hero-tab{" is-active" if i == 0 else ""}" type="button" data-hero-tab="{i}" aria-pressed="{"true" if i == 0 else "false"}"><span class="ht-num">0{i + 1}</span><span class="ht-label">{l}</span><span class="ht-bar"><i></i></span></button>'
                   for i, l in enumerate(['Wedding Feasts', 'Grand Receptions', 'Pure Veg Spreads']))
    hero = f'''<section class="hero" data-hero>
<div class="hero-slides">{slide_html}</div><div class="hero-shade"></div>
<div class="container hero-inner"><div class="hero-copy">
<p class="hero-badge"><span class="veg-dot"></span>100% Pure Vegetarian Catering · Pune</p>
<p class="eyebrow gold hero-eyebrow">Flavours for Every Celebration</p>
<h1 class="hero-title"><span class="line"><span>Making Every</span></span><span class="line"><span>Occasion <em>Special</em></span></span></h1>
<p class="hero-promise">We are a part of your celebration</p>
<p class="hero-text">At Shubh Caterers, we bring people together with exceptional vegetarian food, memorable experiences and heartfelt hospitality.</p>
<div class="hero-actions">{btn('Explore Our Services', '/services/')}
<button class="watch-btn" type="button" data-lightbox="hero-video" data-type="video" data-src="/assets/video/event-1.mp4" data-poster="{image_url('video-posters/event-1')}" data-title="Shubh Caterers — live counters at a reception"><span class="watch-ring">{icon('play', 18)}</span><span>Watch Video</span></button></div>
<ul class="hero-trust"><li>{icon('leaf', 16)}Fresh Ingredients</li><li>{icon('flame', 16)}Authentic Taste</li><li>{icon('star', 16)}Impeccable Service</li></ul>
</div><div class="hero-tabs" role="group" aria-label="Choose a slide">{tabs}</div></div>
<a class="scroll-cue" href="#services" aria-label="Scroll to services"><span></span></a>
<svg class="hero-curve" viewBox="0 0 1440 70" preserveAspectRatio="none" aria-hidden="true"><path d="M0 70V36C240 0 480 0 720 26s480 44 720 6v38z"/></svg></section>'''

    marquee_items = ''.join(f'<span>{escape(m)}</span><i>✦</i>' for m in MARQUEE)
    marquee = f'<div class="marquee" aria-hidden="true"><div class="marquee-track">{marquee_items}{marquee_items}</div></div>'

    services = f'''<section class="section services-home" id="services"><div class="sprig sprig-left" data-parallax="-0.15">{SPRIG}</div><div class="sprig sprig-right" data-parallax="0.12">{SPRIG}</div>
<div class="container">{heading('Our Services', 'Catering for', 'Every Occasion', 'From grand weddings to intimate gatherings, we serve delightful pure-vegetarian food experiences for all your special moments.')}
<div class="services-grid">{''.join(service_card(s) for s in SERVICES)}</div></div></section>'''

    features = ''.join(f'<li class="feature-mini" data-reveal="zoom"><span>{icon(i, 26, stroke=1.4)}</span>{t}</li>' for i, t in FEATURES)
    about = f'''<section class="section about-home"><div class="container about-wrap">
<div class="about-collage" data-reveal="left"><div class="ac ac-1" data-parallax="0.06">{img('team/chef-garnishing-curry', 'Chef garnishing a paneer curry', '(max-width: 900px) 70vw, 380px')}</div>
<div class="ac ac-2" data-parallax="-0.08">{img('venues/brass-handi-counter', 'Brass handi buffet counter with floral décor', '(max-width: 900px) 50vw, 280px')}</div>
<div class="ac ac-3" data-parallax="0.1">{img('food/pure-veg-feast', 'Pure vegetarian feast spread', '(max-width: 900px) 70vw, 420px')}</div>
<div class="quote-ribbon" data-parallax="-0.05"><span>Good Food<br>Brings People<br>Together</span></div></div>
<div class="about-copy" data-reveal="right">{heading('About Shubh Caterers', 'A Passion for <em>Food,</em><br>A Commitment to', 'Excellence', left=True)}
<p>With over {YEARS_OF_SERVICE} years of experience, Shubh Caterers is a Pune-based pure vegetarian catering service known for delicious food, elegant presentation and seamless execution. From our home in Dhanori, we create memorable culinary experiences for weddings, corporate events, private parties and family celebrations.</p>
<ul class="feature-row">{features}</ul>{btn('Know More About Us', '/about/')}</div></div></section>'''

    stats = ''.join(f'<div class="stat" data-reveal><strong><span data-count="{n}">{n}</span>{suf}</strong><span>{l}</span></div>' for n, suf, l in STATS)
    stats_band = f'<section class="stats-band" aria-label="Shubh Caterers in numbers"><div class="container stats-grid">{stats}</div></section>'

    cards = ''.join(f'''<a class="cuisine-card" href="/menu/#{a}"><div class="cuisine-img">{img(n, t, '(max-width: 700px) 72vw, 320px')}</div>
<div class="cuisine-body"><small>0{i + 1}</small><strong>{escape(t)}</strong><span>{escape(sub)}</span><em class="card-more">View dishes {icon('arrow', 14, stroke=2)}</em></div></a>'''
                    for i, (t, sub, n, a) in enumerate(CUISINES))
    menu = f'''<section class="menu-home" data-hscroll><div class="hs-sticky"><div class="menu-bg" aria-hidden="true"></div>
<div class="container">{heading('Our Speciality', 'A Menu for', 'Every Taste', f'From traditional Indian flavours to global favourites — {DISH_COUNT}+ pure-vegetarian dishes crafted to delight every palate.', light=True)}</div>
<div class="hs-viewport" tabindex="0" aria-label="Menu highlights, scroll sideways"><div class="hs-track">{cards}<a class="cuisine-card cuisine-cta" href="/menu/"><span>{icon('menu-book', 40, stroke=1.3)}</span><strong>Explore the full menu</strong><em>{DISH_COUNT}+ dishes across {len(MENU)} categories</em></a></div></div>
<div class="container hs-foot"><div class="hs-progress" aria-hidden="true"><i></i></div>{btn('Explore Our Menu', '/menu/', 'gold')}</div></div></section>'''

    videos = f'''<section class="section showcase"><div class="container showcase-grid">
<div class="showcase-intro"><div class="sticky-col">{heading('Real Events, Real Food', 'See Us', 'in Action', 'Actual footage from events we have catered — illuminated live counters, brass handis and a uniformed team serving with care.', left=True)}
<ul class="tick-list">{''.join(f'<li>{icon("check", 18, stroke=2)}{t}</li>' for t in ['Signature carved & back-lit counters', 'Hygienic, gloved and masked service', 'Every dish neatly labelled for guests', 'Indoor banquets and outdoor gardens'])}</ul>
{btn('See the Gallery', '/gallery/')}</div></div>
<div class="video-grid">{''.join(video_card(v, 'tall' if i in (0, 3) else '') for i, v in enumerate(VIDEOS))}</div></div></section>'''

    steps = ''.join(f'''<article class="stack-card" style="--i:{i}"><span class="stack-num" aria-hidden="true">0{i + 1}</span><div><h3>{escape(t)}</h3><p>{escape(d)}</p></div>{icon(ic, 46, 'stack-ic', 1.2)}</article>'''
                    for i, ((t, d), ic) in enumerate(zip(PROCESS, ['phone', 'menu-book', 'calendar', 'chef'])))
    process = f'''<section class="section process"><div class="container process-grid">
<div class="sticky-col">{heading('How It Works', 'Effortless from', 'Enquiry to Encore', 'Four simple steps — and we take care of everything in between.', left=True)}{btn('Start Planning', '/contact/#quote')}</div>
<div class="stack">{steps}</div></div></section>'''

    zoom = f'''<section class="zoom-band" data-zoom><div class="zoom-frame">{img('venues/reception-dining-hall', 'Reception dining hall set for guests')}<div class="zoom-shade"></div>
<div class="zoom-copy"><p class="script">Good food brings people together</p><h2>Your guests remember how you made them feel — we make sure they also remember the food.</h2>{btn('Plan Your Celebration', '/contact/#quote', 'gold')}</div></div></section>'''

    gal_items = [g for g in GALLERY if not g[0].startswith('video-posters')][:10]
    gallery = f'''<section class="section gallery-home"><div class="sprig sprig-right" data-parallax="0.1">{SPRIG}</div><div class="container">{heading('Our Gallery', 'Moments', 'We Catered', 'A glimpse of our food, setups and celebrations.')}</div>
<div class="carousel" data-carousel><button class="car-btn prev" type="button" data-car-prev aria-label="Previous photos">{icon('arrow-left', 20, stroke=2)}</button>
<div class="car-viewport"><div class="car-track">{''.join(gallery_tile(g, 'home-gallery') for g in gal_items)}</div></div>
<button class="car-btn next" type="button" data-car-next aria-label="Next photos">{icon('arrow', 20, stroke=2)}</button></div>
<div class="center-cta">{btn('View Full Gallery', '/gallery/')}</div></section>'''

    testimonials = f'''<section class="section testimonials-home"><div class="sprig sprig-left" data-parallax="-0.1">{SPRIG}</div><div class="container">{heading('Testimonials', 'What', 'Our Clients Say')}
<div class="testimonial-grid">{''.join(testimonial_card(t) for t in TESTIMONIALS)}</div><div class="center-cta">{btn('Read More Reviews', '/testimonials/', 'outline')}</div></div></section>'''

    body = hero + marquee + services + about + stats_band + menu + videos + process + zoom + gallery + testimonials + clients_section() + inquiry('/')
    write({'path': '/', 'title': 'Shubh Caterers | Pure Vegetarian Catering Services in Pune',
           'description': f'100% pure vegetarian catering in Pune for weddings, corporate events, birthdays, house warming and baby showers — {DISHES} dishes and live counters.',
           'body': body, 'active': 'Home', 'og_image': og('venues/wedding-buffet-night'), 'og_alt': 'Golden buffet counters at a wedding night'})


# ---------------------------------------------------------------- ABOUT
def about():
    values = [('leaf', 'Pure Vegetarian, Always', 'Every dish on every menu is vegetarian — prepared with fresh ingredients and care.'),
              ('sparkle', 'Hygiene First', 'Clean kitchens, gloved and masked service staff, and covered, labelled food at the counter.'),
              ('cloche', 'Menus Made for You', f'Choose from {DISH_COUNT}+ dishes, or ask for your family favourites. We tailor every menu.'),
              ('team', 'A Team That Cares', 'Uniformed, courteous staff who keep counters stocked and guests smiling.'),
              ('flame', 'Live Counter Theatre', '30+ live stalls — from pani puri and dosa to barf gola and paan.'),
              ('star', 'Presentation that Wows', 'Carved back-lit counters, brass handis and floral styling that elevate your venue.')]
    cards = ''.join(f'<article class="value-card tilt" data-reveal="zoom"><span class="value-ic">{icon(i, 30, stroke=1.4)}</span><h3>{t}</h3><p>{d}</p></article>' for i, t, d in values)
    crumbs = [HOME, ('/about/', 'About Us')]
    body = page_hero('A Passion for Food,', 'A Commitment to Excellence', 'Pure vegetarian catering from Dhanori, Pune — crafted with love, served with pride.', 'venues/brass-handi-counter', crumbs) + f'''
<section class="section"><div class="container two-col">
<div class="stacked-media" data-reveal="left"><div class="sm-main" data-parallax="0.05">{img('team/chef-garnishing-curry', 'Chef preparing paneer tikka masala', '(max-width: 900px) 90vw, 460px')}</div><div class="sm-float" data-parallax="-0.08">{img('food/live-chaat-counter', 'Live chaat counter', '(max-width: 900px) 45vw, 240px')}</div><div class="exp-badge"><strong>{YEARS_OF_SERVICE}+</strong><span>Years</span></div></div>
<div class="prose" data-reveal="right">{heading('Our Story', 'Where Every Occasion', 'Becomes Shubh', left=True)}
<p><strong>Shubh</strong> means auspicious — and for over {YEARS_OF_SERVICE} years, that is exactly how we have wanted every celebration we cater to feel. Led by <strong>Pawan Agarwal</strong> and <strong>Ajay Agarwal</strong>, Shubh Caterers serves weddings, corporate functions, family occasions and private events across Pune with a strictly pure-vegetarian kitchen.</p>
<p>We begin by understanding your event — the format, your guests, the venue and your expectations — and then shape a menu and service plan around it. From Maharashtrian breakfasts to Punjabi feasts, Indo-Chinese starters to halwai-style mithai, our menu covers {DISH_COUNT}+ dishes — see the <a href="/menu/">full menu</a> or our <a href="/services/">catering services</a>.</p>
<ul class="tick-list">{''.join(f'<li>{icon("check", 18, stroke=2)}{t}</li>' for t in ['We accept party & marriage orders of every size', 'Buffet, live-counter and traditional pangat service', 'Clear, no-obligation quotes'])}</ul>
<div class="hero-actions">{btn('Get a Free Quote', '/contact/#quote')}{btn('View Our Menu', '/menu/', 'outline', 'menu-book')}</div></div></div></section>
<section class="section alt"><div class="container">{heading('Why Choose Us', 'What Makes Us', 'Shubh', 'Six promises we keep at every event.')}<div class="value-grid">{cards}</div></div></section>
{clients_section()}
<section class="section showcase compact"><div class="container">{heading('Behind the Scenes', 'Our Team', 'at Work')}<div class="video-row">{''.join(video_card(v) for v in VIDEOS[:3])}</div></div></section>''' + inquiry('/about/')
    write({'path': '/about/', 'title': 'About Us | Shubh Caterers, Pure Veg Caterers in Pune', 'page_type': 'AboutPage',
           'description': f'Shubh Caterers: {YEARS_OF_SERVICE}+ years of pure vegetarian catering in Dhanori, Pune, led by Pawan Agarwal and Ajay Agarwal — trusted by corporates and housing societies.',
           'body': body, 'active': 'About Us', 'crumbs': crumbs, 'og_image': og('venues/brass-handi-counter'), 'og_alt': 'Brass handi buffet counter with floral décor'})


# ---------------------------------------------------------------- SERVICES
def services():
    cards = ''.join(f'''<a class="service-big tilt" href="{service_url(s[0])}" data-reveal><div class="sb-img">{img(s[4], s[1], '(max-width: 700px) 92vw, 400px')}<span class="sb-icon">{icon(s[3], 26, stroke=1.5)}</span></div>
<div class="sb-body"><h3>{escape(s[1])}</h3><p>{escape(s[5])}</p><span class="card-more">Explore service {icon('arrow', 14, stroke=2)}</span></div></a>''' for s in SERVICES)
    crumbs = [HOME, ('/services/', 'Our Services')]
    body = page_hero('Catering for', 'Every Occasion', 'From grand weddings to intimate pooja lunches — flexible pure-vegetarian catering for every celebration.', 'venues/wedding-buffet-night', crumbs) + f'''
<section class="section"><div class="container">{heading('What We Cater', f'{len(SERVICES)} Ways to', 'Celebrate')}<div class="service-list-grid">{cards}</div>
<p class="center-cta">Not sure which fits? Browse the <a href="/menu/">full menu</a>, read our <a href="/faq/">catering FAQs</a> or <a href="/contact/">contact us</a>.</p></div></section>''' + inquiry('/services/')
    write({'path': '/services/', 'title': 'Catering Services for Every Occasion | Shubh Caterers Pune',
           'description': 'Pure vegetarian catering in Pune for weddings, cocktail evenings, corporate events, birthdays, house warming, baby showers, institutions and parcel orders.',
           'body': body, 'active': 'Our Services', 'crumbs': crumbs, 'og_image': og('venues/wedding-buffet-night'),
           'schema': [{'@type': 'ItemList', '@id': SITE + '/services/#list', 'itemListElement': [
               {'@type': 'ListItem', 'position': i + 1, 'url': SITE + service_url(s[0]), 'name': s[1]} for i, s in enumerate(SERVICES)]}]})


def service_page(s):
    slug, title, short, ic, image, summary, intro, suitable, highlights, picks = s
    index = SERVICES.index(s)
    others = [SERVICES[(index + k) % len(SERVICES)] for k in range(1, 5)]
    faq = [('Can the menu be customised?', f'Yes. Pick from our {DISH_COUNT}+ dish menu or ask for family favourites — we shape it around your guests and budget.'),
           ('Is the food pure vegetarian?', 'Yes, 100%. Shubh Caterers is a strictly pure-vegetarian caterer.'),
           ('Can live counters be included?', 'Yes — choose from 30+ live stalls such as pani puri, dosa, pav bhaji, Chinese and more, subject to venue logistics.')]
    related = ''.join(f'<a class="related-card tilt" href="{service_url(o[0])}">{img(o[4], o[1], "260px")}<span>{icon(o[3], 20)} {escape(o[2])}</span></a>' for o in others)
    video = VIDEOS[index % len(VIDEOS)]
    path = service_url(slug)
    crumbs = [HOME, ('/services/', 'Our Services'), (path, short)]
    body = page_hero(title, '', summary, image, crumbs) + f'''
<section class="section"><div class="container service-detail-grid">
<article class="prose" data-reveal>{heading('Pure Vegetarian Catering', 'Designed Around', 'Your Event', left=True)}<p class="lead">{escape(intro)}</p>
<div class="detail-media">{img(image, title, '(max-width: 900px) 92vw, 720px')}</div>
<h3>Menu Favourites for {escape(short)}</h3><ul class="dish-chips">{''.join(f'<li>{escape(p)}</li>' for p in picks)}</ul>
<p>These are popular picks — your final menu can include any of our {DISH_COUNT}+ dishes across breakfast, starters, mains, breads, mithai, beverages and live counters. {btn('See the full menu', '/menu/', 'text')}</p>
<h3>Presentation & Service</h3><p>Buffet layouts, live counters, food stations and serving patterns are planned according to your venue space, guest movement and event timings — so food stays fresh and queues stay short.</p>
<h3>Common Questions</h3><div class="faq-list">{''.join(f'<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>' for q, a in faq)}</div>
<p>More answers on our <a href="/faq/">catering FAQ page</a>.</p></article>
<aside class="service-side" aria-label="{escape(short)} at a glance"><div class="side-card" data-reveal="right"><span class="side-icon">{icon(ic, 34, stroke=1.3)}</span><h3>Perfect for</h3><ul>{''.join(f'<li>{icon("check", 16, stroke=2)}{escape(x)}</li>' for x in suitable)}</ul>
<h3>Highlights</h3><ul>{''.join(f'<li>{icon("check", 16, stroke=2)}{escape(x)}</li>' for x in highlights)}</ul>{btn('Request a Quote', '/contact/#quote')}
<a class="side-call" href="tel:+91{PHONE_1}">{icon('phone', 18)} Call {PHONE_1}</a></div>
<div class="side-video" data-reveal="right">{video_card(video)}</div></aside></div></section>
<section class="section alt"><div class="container">{heading('Explore More', 'Other', 'Services')}<div class="related-grid">{related}</div>
<div class="center-cta">{btn('View All Services', '/services/', 'outline')}</div></div></section>''' + inquiry(path)
    seo_title = SERVICE_SEO_TITLES[slug]
    url = SITE + path
    write({'path': path, 'title': f'{seo_title} in Pune | Shubh Caterers', 'description': f'{title} by Shubh Caterers, Pune — {summary}',
           'body': body, 'active': 'Our Services', 'crumbs': crumbs, 'og_image': og(image), 'og_alt': title,
           'schema': [{'@type': 'Service', '@id': url + '#service', 'name': seo_title, 'serviceType': title, 'description': summary,
                       'url': url, 'provider': {'@id': ORG_ID}, 'areaServed': {'@type': 'City', 'name': 'Pune'}},
                      faq_schema(url, faq)]})


# ---------------------------------------------------------------- MENU
def menu():
    nav = ''.join(f'<a href="#{a}">{escape(t)}</a>' for a, t, *_ in MENU)
    sections = ''.join(f'''<section class="menu-cat" id="{a}" data-reveal><div class="menu-cat-media">{img(im, t, '(max-width: 900px) 92vw, 360px')}<span class="menu-count">{len(items)} dishes</span></div>
<div class="menu-cat-body"><h2>{escape(t)}</h2><p>{escape(d)}</p><ul class="dish-list">{''.join(f'<li><span class="veg-dot"></span>{escape(x)}</li>' for x in items)}</ul></div></section>'''
                       for a, t, im, d, items in MENU)
    crumbs = [HOME, ('/menu/', 'Menu')]
    body = page_hero('A Menu for', 'Every Taste', f'{DISH_COUNT}+ pure-vegetarian dishes across {len(MENU)} categories. Mix, match and build your perfect celebration menu.', 'food/pure-veg-feast', crumbs) + f'''
<nav class="menu-nav" data-menu-nav aria-label="Menu categories"><div class="container"><div class="menu-nav-track">{nav}</div></div></nav>
<section class="section menu-page"><div class="container"><p class="menu-intro" data-reveal>{icon('veg', 20)} Every dish below is 100% vegetarian. Menus are customised per event — share your picks and guest count and we will send a tailored quote.</p>{sections}
<div class="menu-cta" data-reveal><h2>Ready to build your menu?</h2><p>Send us your favourite dishes on WhatsApp or through the enquiry form — or see how we cater <a href="/services/wedding-catering/">weddings</a>, <a href="/services/corporate-catering/">corporate events</a> and <a href="/services/">other occasions</a>.</p><div class="hero-actions center">{btn('Get a Free Quote', '/contact/#quote')}{btn('WhatsApp Your Menu', WA_URL, 'outline', 'whatsapp', ' target="_blank" rel="noopener"')}</div></div></div></section>''' + inquiry('/menu/')
    write({'path': '/menu/', 'title': f'Pure Veg Catering Menu – {DISHES} Dishes | Shubh Caterers',
           'description': f'Explore the Shubh Caterers pure vegetarian menu — {DISHES} dishes: breakfast, starters, paneer specials, dal, rice, rotis, mithai, rabdi, juices and live counters.',
           'body': body, 'active': 'Menu', 'crumbs': crumbs, 'og_image': og('food/pure-veg-feast'), 'og_alt': 'A lavish pure vegetarian feast'})


# ---------------------------------------------------------------- GALLERY
def gallery():
    cats = ['All', 'Food', 'Setups', 'Real Events', 'Videos']
    filters = ''.join(f'<button class="chip{" is-active" if c == "All" else ""}" type="button" data-filter="{c}" aria-pressed="{"true" if c == "All" else "false"}">{c}</button>' for c in cats)
    tiles = ''.join(f'<div class="masonry-item" data-category="{escape(g[2])}" data-reveal="zoom">{gallery_tile(g)}</div>' for g in GALLERY)
    vids = ''.join(f'<div class="masonry-item" data-category="Videos" data-reveal="zoom">{video_card(v)}</div>' for v in VIDEOS)
    crumbs = [HOME, ('/gallery/', 'Gallery')]
    body = page_hero('Moments', 'We Catered', 'Food, setups and real footage from celebrations we have been part of.', 'venues/reception-dining-hall', crumbs) + f'''
<section class="section" aria-labelledby="gallery-title"><div class="container"><h2 class="visually-hidden" id="gallery-title">Photos and videos</h2><div class="filter-row" role="toolbar" aria-label="Filter gallery">{filters}</div><div class="masonry" data-gallery>{tiles}{vids}</div></div></section>''' + inquiry('/gallery/')
    write({'path': '/gallery/', 'title': 'Gallery – Food, Setups & Real Events | Shubh Caterers Pune',
           'description': 'Photos and videos of Shubh Caterers pure vegetarian food, buffet setups, live counters and real events in Pune.',
           'body': body, 'active': 'Gallery', 'crumbs': crumbs, 'og_image': og('venues/reception-dining-hall'), 'og_alt': 'Reception dining hall set for guests'})


# ---------------------------------------------------------------- TESTIMONIALS
def testimonials():
    crumbs = [HOME, ('/testimonials/', 'Testimonials')]
    body = page_hero('What Our', 'Clients Say', 'Celebrations remembered, experiences shared.', 'events/birthday-dessert-table', crumbs) + f'''
<section class="section"><div class="container">{heading('Kind Words', 'Reviews from', 'Our Clients')}<div class="testimonial-grid">{''.join(testimonial_card(t) for t in TESTIMONIALS)}</div>
<div class="review-cta" data-reveal><div>{icon('quote', 40)}<h3>Celebrated with us?</h3><p>We’d love to hear about your experience. Share your feedback on WhatsApp — it helps other families plan with confidence.</p></div>{btn('Share Your Feedback', WA_URL + '?text=Hi%20Shubh%20Caterers%2C%20here%20is%20my%20feedback%3A%20', 'primary', 'whatsapp', ' target="_blank" rel="noopener"')}</div></div></section>
<section class="section alt showcase compact"><div class="container">{heading('Proof on the Plate', 'Watch Our', 'Events')}<div class="video-row">{''.join(video_card(v) for v in VIDEOS[3:6])}</div></div></section>''' + inquiry('/testimonials/')
    write({'path': '/testimonials/', 'title': 'Client Testimonials & Reviews | Shubh Caterers Pune',
           'description': 'Client testimonials and reviews for Shubh Caterers, pure vegetarian caterers in Pune for weddings, corporate events and birthdays.',
           'body': body, 'active': 'Testimonials', 'crumbs': crumbs, 'og_image': og('events/birthday-dessert-table'), 'og_alt': 'Birthday dessert table'})


# ---------------------------------------------------------------- CONTACT
def contact():
    (n1, p1), (n2, p2) = BUSINESS['phones']
    tiles = [('phone', 'Call ' + n1, p1, f'tel:+91{p1}'), ('phone', 'Call ' + n2, p2, f'tel:+91{p2}'),
             ('whatsapp', 'WhatsApp', 'Chat with us instantly', WA_URL), ('mail', 'Email', BUSINESS['email'], f"mailto:{BUSINESS['email']}")]
    info = ''.join(f'<a class="info-card tilt" href="{h}"{" target=_blank rel=noopener" if h.startswith("http") else ""} data-reveal="zoom"><span class="info-ic">{icon(i, 24)}</span><small>{escape(t)}</small><strong>{escape(v)}</strong></a>' for i, t, v, h in tiles)
    map_src = f"https://maps.google.com/maps?q={BUSINESS['map_coords']}&z=17&output=embed"
    crumbs = [HOME, ('/contact/', 'Contact Us')]
    body = page_hero('Let’s Plan Your', 'Celebration', 'Tell us about your event and we will get back with a tailored menu and quote.', 'venues/brass-handi-counter', crumbs) + f'''
<section class="section"><div class="container"><h2 class="visually-hidden">Ways to reach us</h2><div class="info-grid">{info}</div>
<div class="contact-grid" id="quote"><div class="quote-card big" data-reveal="left"><h2>Get a Free Quote</h2><p class="quote-sub">Share a few details — it takes less than a minute.</p>{quote_form('/contact/', kind='quote')}</div>
<div class="contact-side" data-reveal="right"><div class="map-card"><iframe title="Shubh Caterers location on Google Maps" src="{escape(map_src)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>
<div class="address-card"><span class="info-ic">{icon('pin', 24)}</span><div><h3>Visit Us</h3><p>{'<br>'.join(BUSINESS['address_lines'])}</p>{btn('Get Directions', MAP_URL, 'text', 'arrow', ' target="_blank" rel="noopener"')}</div></div></div></div></div></section>'''
    write({'path': '/contact/', 'title': 'Contact Us – Get a Catering Quote | Shubh Caterers Pune', 'page_type': 'ContactPage',
           'description': 'Contact Shubh Caterers, Bhairvnagar, Dhanori, Pune — call 9595956709 / 9822323230 or send an enquiry for pure vegetarian catering.',
           'body': body, 'active': 'Contact Us', 'crumbs': crumbs, 'og_image': og('venues/brass-handi-counter')})


# ---------------------------------------------------------------- FAQ, PRIVACY, UTILITY PAGES
def faq():
    items = ''.join(f'<details data-reveal><summary>{escape(q)}</summary><p>{escape(a)}</p></details>' for q, a in FAQS)
    crumbs = [HOME, ('/faq/', 'FAQ')]
    body = page_hero('Questions', 'Before You Plan', 'Everything you need to know about menus, live counters, bookings and quotes.', 'food/mithai-platter', crumbs) + f'''
<section class="section"><div class="container">{heading('FAQ', 'Frequently Asked', 'Questions')}<div class="faq-wrap"><div class="faq-list big">{items}</div>
<aside class="side-card" data-reveal="right" aria-label="Contact Shubh Caterers"><span class="side-icon">{icon('phone', 32, stroke=1.3)}</span><h3>Still have questions?</h3><p>Talk to us directly — we are happy to help you plan. You can also browse our <a href="/services/">services</a> and <a href="/menu/">menu</a>.</p>{btn('Call ' + PHONE_1, f'tel:+91{PHONE_1}', 'primary', 'phone')}<a class="side-call" href="{WA_URL}" target="_blank" rel="noopener">{icon('whatsapp', 18)} WhatsApp us</a></aside></div></div></section>''' + inquiry('/faq/')
    write({'path': '/faq/', 'title': 'Catering FAQs – Menus, Pricing & Booking | Shubh Caterers',
           'description': 'Frequently asked questions about Shubh Caterers pure vegetarian catering in Pune — menus, live counters, pricing and bookings.',
           'body': body, 'crumbs': crumbs, 'og_image': og('food/mithai-platter'), 'schema': [faq_schema(SITE + '/faq/', FAQS)]})


def privacy():
    crumbs = [HOME, ('/privacy/', 'Privacy Policy')]
    email = BUSINESS['email']
    body = page_hero('Privacy', 'Policy', 'How we handle the information you share with us.', 'food/pure-veg-feast', crumbs) + f'''
<section class="section"><div class="container prose narrow">
<p><em>Last updated: 1 October 2026</em></p>
<h2>What we collect</h2><p>When you send the enquiry form, we receive your name, phone number, email address, event type, optional event date and guest count, your message, your agreement to this policy, the page you sent it from and the time it was sent. We do not use cookies for tracking or advertising, and this website has no analytics.</p>
<h2>How the form is sent</h2><p>Your enquiry is sent securely (HTTPS) to a small program hosted by our web host, <strong>Netlify</strong>, which checks it and emails it straight to our own mailbox, {email}, using our email provider <strong>Zoho Mail</strong>. The website itself does not keep a copy or store your details in a database. The email stays in our mailbox so we can reply and plan your event.</p>
<h2>Spam protection</h2><p>To stop automated spam, the form contains a hidden field and a short timer, and we limit how many enquiries can be sent from one internet connection in ten minutes. For that limit we store a scrambled (hashed) version of your IP address — not the address itself — for about ten minutes on Netlify. Our host may also keep standard server logs for security.</p>
<h2>WhatsApp, phone and email</h2><p>If you choose “Send via WhatsApp”, call us or email us directly, your message goes through WhatsApp (Meta), your phone provider or your email provider under their own privacy policies.</p>
<h2>How we use your details</h2><p>We use your details only to answer your enquiry, prepare quotes and plan your event. We do not sell, rent or share them for marketing. We keep enquiry emails only as long as needed to serve you and meet legal or accounting requirements, and then delete them.</p>
<h2>Other services on this site</h2><p>The contact page shows an embedded Google Map, which Google may use under its own privacy policy when it loads. Fonts and all other files are served from our own website.</p>
<h2>Your choices</h2><p>You can ask us to see, correct or delete the details you sent by emailing <a href="mailto:{email}">{email}</a> or calling <a href="tel:+91{PHONE_1}">{PHONE_1}</a>.</p></div></section>'''
    write({'path': '/privacy/', 'title': 'Privacy Policy | Shubh Caterers',
           'description': 'How Shubh Caterers handles the details you send through this website’s enquiry form, WhatsApp, phone and email, and who processes them.',
           'body': body, 'crumbs': crumbs, 'og_image': og('food/pure-veg-feast')})


def helpful_links():
    main = [('/', 'Home'), ('/services/', 'Catering services'), ('/menu/', 'Our menu'), ('/gallery/', 'Gallery'), ('/faq/', 'FAQ'), ('/contact/', 'Contact us')]
    svc = ''.join(f'<li><a href="{service_url(s[0])}">{escape(s[1])}</a></li>' for s in SERVICES)
    return f'''<div class="util-links"><div><h2>Popular pages</h2><ul class="util-list">{''.join(f'<li><a href="{h}">{l}</a></li>' for h, l in main)}</ul></div>
<div><h2>Our services</h2><ul class="util-list">{svc}</ul></div>
<div><h2>Talk to us</h2><ul class="util-list"><li><a href="tel:+91{PHONE_1}">Call {PHONE_1}</a></li><li><a href="tel:+91{PHONE_2}">Call {PHONE_2}</a></li><li><a href="{WA_URL}" target="_blank" rel="noopener">WhatsApp us</a></li><li><a href="mailto:{BUSINESS['email']}">{BUSINESS['email']}</a></li></ul></div></div>'''


def not_found():
    crumbs = [HOME, ('/404.html', 'Page not found')]
    body = page_hero('Page', 'Not Found', 'Sorry — this page has moved or no longer exists. These links will take you where you need to go.', 'food/pure-veg-feast', crumbs) + f'''
<section class="section"><div class="container prose">{helpful_links()}</div></section>'''
    write({'path': '/404.html', 'title': 'Page Not Found | Shubh Caterers', 'indexable': False,
           'description': 'The page you were looking for could not be found. Browse Shubh Caterers services, menu and gallery, or contact us in Pune.',
           'body': body, 'crumbs': crumbs, 'og_image': og('food/pure-veg-feast')})


def thank_you():
    crumbs = [HOME, ('/thank-you/', 'Thank you')]
    body = page_hero('Thank You —', 'Enquiry Received', 'Your enquiry has reached Shubh Caterers. We will get back to you by phone or email.', 'venues/wedding-buffet-night', crumbs) + f'''
<section class="section"><div class="container prose"><p class="lead">While you wait, explore our menu and services. For anything urgent, please call or WhatsApp us.</p>{helpful_links()}</div></section>'''
    write({'path': '/thank-you/', 'title': 'Thank You – Enquiry Received | Shubh Caterers', 'indexable': False,
           'description': 'Thank you for contacting Shubh Caterers. Your catering enquiry has been received and we will get back to you by phone or email.',
           'body': body, 'crumbs': crumbs, 'og_image': og('venues/wedding-buffet-night')})


if __name__ == '__main__':
    home(); about(); services(); menu(); gallery(); testimonials(); contact(); faq(); privacy(); not_found(); thank_you()
    for s in SERVICES:
        service_page(s)
    print('Generated', len(written), 'pages into pages/')
