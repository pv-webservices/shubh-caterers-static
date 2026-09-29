"""Builds every HTML page of the Shubh Caterers website.  Run:  python generate.py"""
from html import escape
import json

from icons import icon, SPRIG
from site_data import BUSINESS, SERVICES, MENU, CUISINES, VIDEOS, GALLERY, TESTIMONIALS, PROCESS, FAQS
from templates import (ROOT, PHONE_1, PHONE_2, WA_URL, MAP_URL, img, btn, heading, inquiry, page_hero, quote_form,
                       document)

DISH_COUNT = len({d for c in MENU for d in c[4]})
STALL_COUNT = len(MENU[-1][4])
STATS = [(len(SERVICES), '', 'Occasions We Cater'), (DISH_COUNT // 50 * 50, '+', 'Vegetarian Dishes'),
         (STALL_COUNT, '', 'Live Counter Options'), (100, '%', 'Pure Vegetarian')]
FEATURES = [('sparkle', 'Hygienic Preparation'), ('cloche', 'Customised Menus'), ('team', 'Experienced Team'), ('diamond', 'Quality Ingredients')]
MARQUEE = ['Paneer Tikka', 'Pani Puri', 'Dal Makhani', 'Mango Mastani', 'Masala Dosa', 'Kaju Katli', 'Veg Biryani',
           'Misal Pav', 'Kesar Rabdi', 'Chilli Paneer', 'Puran Puri', 'Pav Bhaji', 'Jalebi', 'Malai Kofta']


def write(path, html):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding='utf-8')


def service_card(s, R):
    return (f'<a class="service-card tilt" href="{R}services/{s[0]}.html" data-reveal="zoom">'
            f'<span class="service-icon">{icon(s[3], 34, stroke=1.4)}</span><strong>{escape(s[2])}</strong>'
            f'<span class="card-more">Explore {icon("arrow", 14, stroke=2)}</span></a>')


def video_card(v, R, cls=''):
    slug, title, desc = v
    return (f'<button class="video-card {cls}" data-lightbox="videos" data-type="video" data-src="{R}assets/video/{slug}.mp4" '
            f'data-poster="{R}assets/img/{slug}-poster.webp" data-title="{escape(title)}" data-reveal>'
            f'<video muted loop playsinline preload="none" poster="{R}assets/img/{slug}-poster.webp" data-lazy-video>'
            f'<source data-src="{R}assets/video/{slug}-loop.mp4" type="video/mp4"></video>'
            f'<span class="video-play">{icon("play", 22)}</span><span class="video-meta"><strong>{escape(title)}</strong><small>{escape(desc)}</small></span></button>')


def gallery_tile(item, R, group='gallery'):
    name, title, cat = item
    sizes = '(max-width: 640px) 80vw, 360px'
    return (f'<button class="gallery-card" data-lightbox="{group}" data-type="image" data-src="{R}assets/img/{name}.webp" '
            f'data-title="{escape(title)}" data-category="{escape(cat)}">{img(name, title, R, sizes)}'
            f'<span class="gallery-cap"><small>{escape(cat)}</small><strong>{escape(title)}</strong></span></button>')


def testimonial_card(t):
    quote, name, kind = t
    initials = ''.join(p[0] for p in name.replace('&', '').split()[:2])
    return (f'<figure class="testimonial-card" data-reveal>{icon("quote", 34, "quote-ic")}<div class="stars" aria-label="5 out of 5 stars">★★★★★</div>'
            f'<blockquote>{escape(quote)}</blockquote><figcaption><span class="avatar">{initials}</span>'
            f'<span><strong>{escape(name)}</strong><small>{escape(kind)}</small></span></figcaption></figure>')


# ---------------------------------------------------------------- HOME
def home():
    R = ''
    slides = [('hero-buffet', 'Golden buffet counters at a wedding night'), ('hero-reception', 'Elegant reception dining hall'),
              ('hero-feast', 'A lavish pure vegetarian feast')]
    slide_html = ''.join(f'<div class="hero-slide{" is-active" if i == 0 else ""}">{img(n, a, R, eager=(i == 0))}</div>' for i, (n, a) in enumerate(slides))
    tabs = ''.join(f'<button class="hero-tab{" is-active" if i == 0 else ""}" data-hero-tab="{i}"><span class="ht-num">0{i + 1}</span><span class="ht-label">{l}</span><span class="ht-bar"><i></i></span></button>'
                   for i, l in enumerate(['Wedding Feasts', 'Grand Receptions', 'Pure Veg Spreads']))
    hero = f'''<section class="hero" data-hero>
<div class="hero-slides">{slide_html}</div><div class="hero-shade"></div>
<div class="container hero-inner"><div class="hero-copy">
<p class="hero-badge"><span class="veg-dot"></span>100% Pure Vegetarian Catering · Pune</p>
<p class="eyebrow gold hero-eyebrow">Flavours for Every Celebration</p>
<h1 class="hero-title"><span class="line"><span>Making Every</span></span><span class="line"><span>Occasion <em>Special</em></span></span></h1>
<p class="hero-text">At Shubh Caterers, we bring people together with exceptional vegetarian food, memorable experiences and heartfelt hospitality.</p>
<div class="hero-actions">{btn('Explore Our Services', 'services.html')}
<button class="watch-btn" data-lightbox="hero-video" data-type="video" data-src="assets/video/event-1.mp4" data-poster="assets/img/event-1-poster.webp" data-title="Shubh Caterers — live counters at a reception"><span class="watch-ring">{icon('play', 18)}</span><span>Watch Video</span></button></div>
<ul class="hero-trust"><li>{icon('leaf', 16)}Fresh Ingredients</li><li>{icon('flame', 16)}Authentic Taste</li><li>{icon('star', 16)}Impeccable Service</li></ul>
</div><div class="hero-tabs" role="tablist" aria-label="Hero slides">{tabs}</div></div>
<a class="scroll-cue" href="#services" aria-label="Scroll to services"><span></span></a>
<svg class="hero-curve" viewBox="0 0 1440 70" preserveAspectRatio="none" aria-hidden="true"><path d="M0 70V36C240 0 480 0 720 26s480 44 720 6v38z"/></svg></section>'''

    marquee_items = ''.join(f'<span>{escape(m)}</span><i>✦</i>' for m in MARQUEE)
    marquee = f'<div class="marquee" aria-hidden="true"><div class="marquee-track">{marquee_items}{marquee_items}</div></div>'

    services = f'''<section class="section services-home" id="services"><div class="sprig sprig-left" data-parallax="-0.15">{SPRIG}</div><div class="sprig sprig-right" data-parallax="0.12">{SPRIG}</div>
<div class="container">{heading('Our Services', 'Catering for', 'Every Occasion', 'From grand weddings to intimate gatherings, we serve delightful pure-vegetarian food experiences for all your special moments.')}
<div class="services-grid">{''.join(service_card(s, R) for s in SERVICES)}</div></div></section>'''

    features = ''.join(f'<li class="feature-mini" data-reveal="zoom"><span>{icon(i, 26, stroke=1.4)}</span>{t}</li>' for i, t in FEATURES)
    about = f'''<section class="section about-home"><div class="container about-wrap">
<div class="about-collage" data-reveal="left"><div class="ac ac-1" data-parallax="0.06">{img('about-chef', 'Chef garnishing a paneer curry', R, '(max-width: 900px) 70vw, 380px')}</div>
<div class="ac ac-2" data-parallax="-0.08">{img('about-counter', 'Brass handi buffet counter with floral décor', R, '(max-width: 900px) 50vw, 280px')}</div>
<div class="ac ac-3" data-parallax="0.1">{img('hero-feast', 'Pure vegetarian feast spread', R, '(max-width: 900px) 70vw, 420px')}</div>
<div class="quote-ribbon" data-parallax="-0.05"><span>Good Food<br>Brings People<br>Together</span></div></div>
<div class="about-copy" data-reveal="right">{heading('About Shubh Caterers', 'A Passion for <em>Food,</em><br>A Commitment to', 'Excellence', left=True)}
<p>Shubh Caterers is a Pune-based pure vegetarian catering service known for delicious food, elegant presentation and seamless execution. From our home at Tirupati Garden, Tingre Nagar, we create memorable culinary experiences for weddings, corporate events, private parties and family celebrations.</p>
<ul class="feature-row">{features}</ul>{btn('Know More About Us', 'about.html')}</div></div></section>'''

    stats = ''.join(f'<div class="stat" data-reveal><strong><span data-count="{n}">0</span>{suf}</strong><span>{l}</span></div>' for n, suf, l in STATS)
    stats_band = f'<section class="stats-band"><div class="container stats-grid">{stats}</div></section>'

    cards = ''.join(f'''<a class="cuisine-card" href="menu.html#{a}"><div class="cuisine-img">{img(n, t, R, '(max-width: 700px) 72vw, 320px')}</div>
<div class="cuisine-body"><small>0{i + 1}</small><strong>{escape(t)}</strong><span>{escape(sub)}</span><em class="card-more">View dishes {icon('arrow', 14, stroke=2)}</em></div></a>'''
                    for i, (t, sub, n, a) in enumerate(CUISINES))
    menu = f'''<section class="menu-home" data-hscroll><div class="hs-sticky"><div class="menu-bg" aria-hidden="true"></div>
<div class="container">{heading('Our Speciality', 'A Menu for', 'Every Taste', f'From traditional Indian flavours to global favourites — {DISH_COUNT}+ pure-vegetarian dishes crafted to delight every palate.', light=True)}</div>
<div class="hs-viewport"><div class="hs-track">{cards}<a class="cuisine-card cuisine-cta" href="menu.html"><span>{icon('menu-book', 40, stroke=1.3)}</span><strong>Explore the full menu</strong><em>{DISH_COUNT}+ dishes across {len(MENU)} categories</em></a></div></div>
<div class="container hs-foot"><div class="hs-progress"><i></i></div>{btn('Explore Our Menu', 'menu.html', 'gold')}</div></div></section>'''

    videos = f'''<section class="section showcase"><div class="container showcase-grid">
<div class="showcase-intro"><div class="sticky-col">{heading('Real Events, Real Food', 'See Us', 'in Action', 'Actual footage from events we have catered — illuminated live counters, brass handis and a uniformed team serving with care.', left=True)}
<ul class="tick-list">{''.join(f'<li>{icon("check", 18, stroke=2)}{t}</li>' for t in ['Signature carved & back-lit counters', 'Hygienic, gloved and masked service', 'Every dish neatly labelled for guests', 'Indoor banquets and outdoor gardens'])}</ul>
{btn('See the Gallery', 'gallery.html')}</div></div>
<div class="video-grid">{''.join(video_card(v, R, 'tall' if i in (0, 3) else '') for i, v in enumerate(VIDEOS))}</div></div></section>'''

    steps = ''.join(f'''<article class="stack-card" style="--i:{i}"><span class="stack-num">0{i + 1}</span><div><h3>{escape(t)}</h3><p>{escape(d)}</p></div>{icon(ic, 46, 'stack-ic', 1.2)}</article>'''
                    for i, ((t, d), ic) in enumerate(zip(PROCESS, ['phone', 'menu-book', 'calendar', 'chef'])))
    process = f'''<section class="section process"><div class="container process-grid">
<div class="sticky-col">{heading('How It Works', 'Effortless from', 'Enquiry to Encore', 'Four simple steps — and we take care of everything in between.', left=True)}{btn('Start Planning', 'contact.html#quote')}</div>
<div class="stack">{steps}</div></div></section>'''

    zoom = f'''<section class="zoom-band" data-zoom><div class="zoom-frame">{img('hero-reception', 'Reception dining hall set for guests', R)}<div class="zoom-shade"></div>
<div class="zoom-copy"><p class="script">Good food brings people together</p><h2>Your guests remember how you made them feel — we make sure they also remember the food.</h2>{btn('Plan Your Celebration', 'contact.html#quote', 'gold')}</div></div></section>'''

    gal_items = [g for g in GALLERY if not g[0].startswith('event')][:10]
    gallery = f'''<section class="section gallery-home"><div class="sprig sprig-right" data-parallax="0.1">{SPRIG}</div><div class="container">{heading('Our Gallery', 'Moments', 'We Catered', 'A glimpse of our food, setups and celebrations.')}</div>
<div class="carousel" data-carousel><button class="car-btn prev" data-car-prev aria-label="Previous">{icon('arrow-left', 20, stroke=2)}</button>
<div class="car-viewport"><div class="car-track">{''.join(gallery_tile(g, R, 'home-gallery') for g in gal_items)}</div></div>
<button class="car-btn next" data-car-next aria-label="Next">{icon('arrow', 20, stroke=2)}</button></div>
<div class="center-cta">{btn('View Full Gallery', 'gallery.html')}</div></section>'''

    testimonials = f'''<section class="section testimonials-home"><div class="sprig sprig-left" data-parallax="-0.1">{SPRIG}</div><div class="container">{heading('Testimonials', 'What', 'Our Clients Say')}
<div class="testimonial-grid">{''.join(testimonial_card(t) for t in TESTIMONIALS)}</div><div class="center-cta">{btn('Read More Reviews', 'testimonials.html', 'outline')}</div></div></section>'''

    body = hero + marquee + services + about + stats_band + menu + videos + process + zoom + gallery + testimonials + inquiry(R)
    write('index.html', document('Pure Veg Catering Services in Pune', 'Shubh Caterers — 100% pure vegetarian catering in Pune for weddings, corporate events, birthdays, house warming, baby showers and every celebration. 350+ dishes and live counters.', body, R, 'Home'))


# ---------------------------------------------------------------- ABOUT
def about():
    R = ''
    values = [('leaf', 'Pure Vegetarian, Always', 'Every dish on every menu is vegetarian — prepared with fresh ingredients and care.'),
              ('sparkle', 'Hygiene First', 'Clean kitchens, gloved and masked service staff, and covered, labelled food at the counter.'),
              ('cloche', 'Menus Made for You', f'Choose from {DISH_COUNT}+ dishes, or ask for your family favourites. We tailor every menu.'),
              ('team', 'A Team That Cares', 'Uniformed, courteous staff who keep counters stocked and guests smiling.'),
              ('flame', 'Live Counter Theatre', f'{STALL_COUNT} live stalls — from pani puri and dosa to barf gola and paan.'),
              ('star', 'Presentation that Wows', 'Carved back-lit counters, brass handis and floral styling that elevate your venue.')]
    cards = ''.join(f'<article class="value-card tilt" data-reveal="zoom"><span class="value-ic">{icon(i, 30, stroke=1.4)}</span><h3>{t}</h3><p>{d}</p></article>' for i, t, d in values)
    body = page_hero('About Us', 'A Passion for Food,', 'A Commitment to Excellence', 'Pure vegetarian catering from Tingre Nagar, Pune — crafted with love, served with pride.', 'about-counter', R) + f'''
<section class="section"><div class="container two-col">
<div class="stacked-media" data-reveal="left"><div class="sm-main" data-parallax="0.05">{img('about-chef', 'Chef preparing paneer tikka masala', R, '(max-width: 900px) 90vw, 460px')}</div><div class="sm-float" data-parallax="-0.08">{img('menu-chaat', 'Live chaat counter', R, '(max-width: 900px) 45vw, 240px')}</div><div class="exp-badge"><strong>100%</strong><span>Pure Veg</span></div></div>
<div class="prose" data-reveal="right">{heading('Our Story', 'Where Every Occasion', 'Becomes Shubh', left=True)}
<p><strong>Shubh</strong> means auspicious — and that is exactly how we want every celebration we cater to feel. Led by <strong>Pawan Agarwal</strong> and <strong>Ajay Agarwal</strong>, Shubh Caterers serves weddings, corporate functions, family occasions and private events across Pune with a strictly pure-vegetarian kitchen.</p>
<p>We begin by understanding your event — the format, your guests, the venue and your expectations — and then shape a menu and service plan around it. From Maharashtrian breakfasts to Punjabi feasts, Indo-Chinese starters to halwai-style mithai, our menu covers {DISH_COUNT}+ dishes.</p>
<ul class="tick-list">{''.join(f'<li>{icon("check", 18, stroke=2)}{t}</li>' for t in ['We accept party & marriage orders of every size', 'Buffet, live-counter and traditional pangat service', 'Clear, no-obligation quotes'])}</ul>
<div class="hero-actions">{btn('Get a Free Quote', 'contact.html#quote')}{btn('View Our Menu', 'menu.html', 'outline', 'menu-book')}</div></div></div></section>
<section class="section alt"><div class="container">{heading('Why Choose Us', 'What Makes Us', 'Shubh', 'Six promises we keep at every event.')}<div class="value-grid">{cards}</div></div></section>
<section class="section showcase compact"><div class="container">{heading('Behind the Scenes', 'Our Team', 'at Work')}<div class="video-row">{''.join(video_card(v, R) for v in VIDEOS[:3])}</div></div></section>''' + inquiry(R)
    write('about.html', document('About Us', 'Shubh Caterers is a pure vegetarian catering company in Tingre Nagar, Pune, led by Pawan Agarwal and Ajay Agarwal — weddings, corporate events and celebrations.', body, R, 'About Us'))


# ---------------------------------------------------------------- SERVICES
def services():
    R = ''
    cards = ''.join(f'''<a class="service-big tilt" href="services/{s[0]}.html" data-reveal><div class="sb-img">{img(s[4], s[1], R, '(max-width: 700px) 92vw, 400px')}<span class="sb-icon">{icon(s[3], 26, stroke=1.5)}</span></div>
<div class="sb-body"><h3>{escape(s[1])}</h3><p>{escape(s[5])}</p><span class="card-more">Explore service {icon('arrow', 14, stroke=2)}</span></div></a>''' for s in SERVICES)
    body = page_hero('Our Services', 'Catering for', 'Every Occasion', 'From grand weddings to intimate pooja lunches — flexible pure-vegetarian catering for every celebration.', 'hero-buffet', R) + f'''
<section class="section"><div class="container">{heading('What We Cater', f'{len(SERVICES)} Ways to', 'Celebrate')}<div class="service-list-grid">{cards}</div></div></section>''' + inquiry(R)
    write('services.html', document('Catering Services', 'Pure vegetarian catering services in Pune: weddings, cocktail evenings, corporate events, theme parties, birthdays, house warming, baby showers, institutional catering and parcels.', body, R, 'Our Services'))


def service_page(s):
    R = '../'
    slug, title, short, ic, image, summary, intro, suitable, highlights, picks = s
    others = [o for o in SERVICES if o[0] != slug][:4]
    faq = [('Can the menu be customised?', f'Yes. Pick from our {DISH_COUNT}+ dish menu or ask for family favourites — we shape it around your guests and budget.'),
           ('Is the food pure vegetarian?', 'Yes, 100%. Shubh Caterers is a strictly pure-vegetarian caterer.'),
           ('Can live counters be included?', f'Yes — choose from {STALL_COUNT} live stalls such as pani puri, dosa, pav bhaji, Chinese and more, subject to venue logistics.')]
    related = ''.join(f'<a class="related-card tilt" href="{o[0]}.html">{img(o[4], o[1], R, "260px")}<span>{icon(o[3], 20)} {escape(o[2])}</span></a>' for o in others)
    video = VIDEOS[SERVICES.index(s) % len(VIDEOS)]
    body = page_hero(short, title, '', summary, image, R, [('services.html', 'Services')]) + f'''
<section class="section"><div class="container service-detail-grid">
<article class="prose" data-reveal>{heading('Pure Vegetarian Catering', 'Designed Around', 'Your Event', left=True)}<p class="lead">{escape(intro)}</p>
<div class="detail-media">{img(image, title, R, '(max-width: 900px) 92vw, 720px')}</div>
<h3>Menu Favourites for {escape(short)}</h3><ul class="dish-chips">{''.join(f'<li>{escape(p)}</li>' for p in picks)}</ul>
<p>These are popular picks — your final menu can include any of our {DISH_COUNT}+ dishes across breakfast, starters, mains, breads, mithai, beverages and live counters. {btn('See the full menu', R + 'menu.html', 'text')}</p>
<h3>Presentation & Service</h3><p>Buffet layouts, live counters, food stations and serving patterns are planned according to your venue space, guest movement and event timings — so food stays fresh and queues stay short.</p>
<h3>Common Questions</h3><div class="faq-list">{''.join(f'<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>' for q, a in faq)}</div></article>
<aside class="service-side"><div class="side-card" data-reveal="right"><span class="side-icon">{icon(ic, 34, stroke=1.3)}</span><h3>Perfect for</h3><ul>{''.join(f'<li>{icon("check", 16, stroke=2)}{escape(x)}</li>' for x in suitable)}</ul>
<h3>Highlights</h3><ul>{''.join(f'<li>{icon("check", 16, stroke=2)}{escape(x)}</li>' for x in highlights)}</ul>{btn('Request a Quote', R + 'contact.html#quote')}
<a class="side-call" href="tel:+91{PHONE_1}">{icon('phone', 18)} Call {PHONE_1}</a></div>
<div class="side-video" data-reveal="right">{video_card(video, R)}</div></aside></div></section>
<section class="section alt"><div class="container">{heading('Explore More', 'Other', 'Services')}<div class="related-grid">{related}</div></div></section>''' + inquiry(R)
    write(f'services/{slug}.html', document(title, f'{title} by Shubh Caterers, Pune — {summary}', body, R, 'Our Services'))


# ---------------------------------------------------------------- MENU
def menu():
    R = ''
    nav = ''.join(f'<a href="#{a}">{escape(t)}</a>' for a, t, *_ in MENU)
    sections = ''.join(f'''<section class="menu-cat" id="{a}" data-reveal><div class="menu-cat-media">{img(im, t, R, '(max-width: 900px) 92vw, 360px')}<span class="menu-count">{len(items)} dishes</span></div>
<div class="menu-cat-body"><h2>{escape(t)}</h2><p>{escape(d)}</p><ul class="dish-list">{''.join(f'<li><span class="veg-dot"></span>{escape(x)}</li>' for x in items)}</ul></div></section>'''
                       for a, t, im, d, items in MENU)
    body = page_hero('Menu', 'A Menu for', 'Every Taste', f'{DISH_COUNT}+ pure-vegetarian dishes across {len(MENU)} categories. Mix, match and build your perfect celebration menu.', 'hero-feast', R) + f'''
<div class="menu-nav" data-menu-nav><div class="container"><div class="menu-nav-track">{nav}</div></div></div>
<section class="section menu-page"><div class="container"><p class="menu-intro" data-reveal>{icon('veg', 20)} Every dish below is 100% vegetarian. Menus are customised per event — share your picks and guest count and we will send a tailored quote.</p>{sections}
<div class="menu-cta" data-reveal><h2>Ready to build your menu?</h2><p>Send us your favourite dishes on WhatsApp or through the enquiry form.</p><div class="hero-actions center">{btn('Get a Free Quote', 'contact.html#quote')}{btn('WhatsApp Your Menu', WA_URL, 'outline', 'whatsapp', ' target="_blank" rel="noopener"')}</div></div></div></section>''' + inquiry(R)
    write('menu.html', document('Pure Veg Catering Menu', f'Explore the Shubh Caterers pure vegetarian menu — {DISH_COUNT}+ dishes: breakfast, starters, paneer specials, dal, rice, rotis, mithai, rabdi, juices and live counters.', body, R, 'Menu'))


# ---------------------------------------------------------------- GALLERY
def gallery():
    R = ''
    cats = ['All', 'Food', 'Setups', 'Real Events', 'Videos']
    filters = ''.join(f'<button class="chip{" is-active" if c == "All" else ""}" data-filter="{c}">{c}</button>' for c in cats)
    tiles = ''.join(f'<div class="masonry-item" data-category="{escape(g[2])}" data-reveal="zoom">{gallery_tile(g, R, "gallery")}</div>' for g in GALLERY)
    vids = ''.join(f'<div class="masonry-item" data-category="Videos" data-reveal="zoom">{video_card(v, R)}</div>' for v in VIDEOS)
    body = page_hero('Gallery', 'Moments', 'We Catered', 'Food, setups and real footage from celebrations we have been part of.', 'hero-reception', R) + f'''
<section class="section"><div class="container"><div class="filter-row" role="toolbar" aria-label="Filter gallery">{filters}</div><div class="masonry" data-gallery>{tiles}{vids}</div></div></section>''' + inquiry(R)
    write('gallery.html', document('Gallery', 'Photos and videos of Shubh Caterers pure vegetarian food, buffet setups, live counters and real events in Pune.', body, R, 'Gallery'))


# ---------------------------------------------------------------- TESTIMONIALS
def testimonials():
    R = ''
    body = page_hero('Testimonials', 'What Our', 'Clients Say', 'Celebrations remembered, experiences shared.', 'svc-birthday', R) + f'''
<section class="section"><div class="container"><div class="testimonial-grid">{''.join(testimonial_card(t) for t in TESTIMONIALS)}</div>
<div class="review-cta" data-reveal><div>{icon('quote', 40)}<h3>Celebrated with us?</h3><p>We’d love to hear about your experience. Share your feedback on WhatsApp — it helps other families plan with confidence.</p></div>{btn('Share Your Feedback', WA_URL + '?text=Hi%20Shubh%20Caterers%2C%20here%20is%20my%20feedback%3A%20', 'primary', 'whatsapp', ' target="_blank" rel="noopener"')}</div></div></section>
<section class="section alt showcase compact"><div class="container">{heading('Proof on the Plate', 'Watch Our', 'Events')}<div class="video-row">{''.join(video_card(v, R) for v in VIDEOS[3:6])}</div></div></section>''' + inquiry(R)
    write('testimonials.html', document('Testimonials', 'Client testimonials and reviews for Shubh Caterers, pure vegetarian caterers in Pune.', body, R, 'Testimonials'))


# ---------------------------------------------------------------- CONTACT
def contact():
    R = ''
    (n1, p1), (n2, p2) = BUSINESS['phones']
    tiles = [('phone', 'Call ' + n1, p1, f'tel:+91{p1}'), ('phone', 'Call ' + n2, p2, f'tel:+91{p2}'),
             ('whatsapp', 'WhatsApp', 'Chat with us instantly', WA_URL), ('mail', 'Email', BUSINESS['email'], f"mailto:{BUSINESS['email']}")]
    info = ''.join(f'<a class="info-card tilt" href="{h}"{" target=_blank rel=noopener" if h.startswith("http") else ""} data-reveal="zoom"><span class="info-ic">{icon(i, 24)}</span><small>{escape(t)}</small><strong>{escape(v)}</strong></a>' for i, t, v, h in tiles)
    map_src = 'https://www.google.com/maps?q=' + BUSINESS['map_query'].replace(' ', '+').replace(',', '%2C') + '&output=embed'
    body = page_hero('Contact Us', 'Let’s Plan Your', 'Celebration', 'Tell us about your event and we will get back with a tailored menu and quote.', 'about-counter', R) + f'''
<section class="section"><div class="container"><div class="info-grid">{info}</div>
<div class="contact-grid" id="quote"><div class="quote-card big" data-reveal="left"><h2>Get a Free Quote</h2><p class="quote-sub">Share a few details — it takes less than a minute.</p>{quote_form()}</div>
<div class="contact-side" data-reveal="right"><div class="map-card"><iframe title="Shubh Caterers location on Google Maps" src="{map_src}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>
<div class="address-card"><span class="info-ic">{icon('pin', 24)}</span><div><h3>Visit Us</h3><p>{'<br>'.join(BUSINESS['address_lines'])}</p>{btn('Get Directions', MAP_URL, 'text', 'arrow', ' target="_blank" rel="noopener"')}</div></div></div></div></div></section>'''
    write('contact.html', document('Contact Us', 'Contact Shubh Caterers, Tirupati Garden, Tingre Nagar, Pune — call 9595956709 / 9822323230 or send an enquiry for pure vegetarian catering.', body, R, 'Contact Us'))


# ---------------------------------------------------------------- FAQ & PRIVACY
def faq():
    R = ''
    schema = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQS]}
    items = ''.join(f'<details data-reveal><summary>{escape(q)}</summary><p>{escape(a)}</p></details>' for q, a in FAQS)
    body = page_hero('FAQ', 'Questions', 'Before You Plan', 'Everything you need to know about menus, live counters, bookings and quotes.', 'menu-sweets', R) + f'''
<section class="section"><div class="container faq-wrap"><div class="faq-list big">{items}</div>
<aside class="side-card" data-reveal="right"><span class="side-icon">{icon('phone', 32, stroke=1.3)}</span><h3>Still have questions?</h3><p>Talk to us directly — we are happy to help you plan.</p>{btn('Call ' + PHONE_1, f'tel:+91{PHONE_1}', 'primary', 'phone')}<a class="side-call" href="{WA_URL}" target="_blank" rel="noopener">{icon('whatsapp', 18)} WhatsApp us</a></aside></div></section>''' + inquiry(R)
    write('faq.html', document('FAQ', 'Frequently asked questions about Shubh Caterers pure vegetarian catering in Pune — menus, live counters, pricing and bookings.', body, R, '',
                               f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>'))


def privacy():
    R = ''
    body = page_hero('Privacy Policy', 'Privacy', 'Policy', 'How we handle the information you share with us.', 'hero-feast', R) + f'''
<section class="section"><div class="container prose narrow">
<h2>Information you share</h2><p>This website does not store your personal information. When you use the enquiry form, your name, phone number, email address and event details are placed into a WhatsApp message (or an email, if you choose) that you send to Shubh Caterers yourself. Nothing is saved on this website.</p>
<h2>How we use it</h2><p>We use the details you send only to respond to your enquiry, plan your event and share quotes. We do not sell or rent your information to anyone.</p>
<h2>Third-party services</h2><p>The contact page shows an embedded Google Map, and the site loads fonts from Google Fonts. WhatsApp and your email provider handle messages under their own privacy policies.</p>
<h2>Contact</h2><p>For any privacy question, email <a href="mailto:{BUSINESS['email']}">{BUSINESS['email']}</a> or call <a href="tel:+91{PHONE_1}">{PHONE_1}</a>.</p></div></section>'''
    write('privacy.html', document('Privacy Policy', 'Privacy policy for the Shubh Caterers website.', body, R))


def seo_files():
    d = BUSINESS['domain']
    paths = ['', 'about.html', 'services.html', 'menu.html', 'gallery.html', 'testimonials.html', 'contact.html', 'faq.html', 'privacy.html'] + [f'services/{s[0]}.html' for s in SERVICES]
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{d}/{p}</loc></url>\n' for p in paths) + '</urlset>\n')
    write('robots.txt', f'User-agent: *\nAllow: /\nDisallow: /public/\nSitemap: {d}/sitemap.xml\n')
    return len(paths)


if __name__ == '__main__':
    home(); about(); services(); menu(); gallery(); testimonials(); contact(); faq(); privacy()
    for s in SERVICES:
        service_page(s)
    print('Generated', seo_files(), 'pages')
