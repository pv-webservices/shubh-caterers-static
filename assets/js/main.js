/* Shubh Caterers — site interactions (vanilla JS, no dependencies) */
(() => {
  'use strict';

  const doc = document.documentElement;
  doc.classList.add('js');
  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));
  const clamp = (v, min, max) => Math.min(max, Math.max(min, v));
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isDesktop = () => window.matchMedia('(min-width: 900px)').matches;
  const WHATSAPP_NUMBER = '919595956709';
  const EMAIL = 'shubhcaterers009@gmail.com';
  const HERO_INTERVAL = 7000;
  const CAROUSEL_INTERVAL = 3600;
  const headerH = () => ($('[data-header]') || { offsetHeight: 0 }).offsetHeight;

  /* ---------- Scroll-driven updates share one rAF loop ---------- */
  const scrollTasks = [];
  let ticking = false;
  const runScrollTasks = () => { scrollTasks.forEach((fn) => fn()); ticking = false; };
  const requestTick = () => { if (!ticking) { ticking = true; requestAnimationFrame(runScrollTasks); } };
  window.addEventListener('scroll', requestTick, { passive: true });
  window.addEventListener('resize', requestTick);

  /* ---------- Header state & back-to-top ---------- */
  function initHeader() {
    const header = $('[data-header]');
    const toTop = $('[data-to-top]');
    scrollTasks.push(() => {
      const y = window.scrollY;
      if (header) header.classList.toggle('is-scrolled', y > 40);
      if (toTop) toTop.classList.toggle('is-visible', y > 700);
    });
    if (toTop) toTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' }));
  }

  /* ---------- Mobile navigation drawer ---------- */
  function initNav() {
    const toggle = $('#menuToggle');
    const nav = $('#mainNav');
    const overlay = $('[data-nav-overlay]');
    if (!toggle || !nav) return;
    const setOpen = (open) => {
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      nav.classList.toggle('is-open', open);
      if (overlay) overlay.classList.toggle('is-open', open);
      document.body.style.overflow = open ? 'hidden' : '';
    };
    toggle.addEventListener('click', () => setOpen(toggle.getAttribute('aria-expanded') !== 'true'));
    if (overlay) overlay.addEventListener('click', () => setOpen(false));
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && nav.classList.contains('is-open')) { setOpen(false); toggle.focus(); } });
    $$('a', nav).forEach((a) => a.addEventListener('click', () => setOpen(false)));
    $$('.drop-toggle', nav).forEach((btn) => btn.addEventListener('click', () => {
      const item = btn.closest('.has-drop');
      const open = !item.classList.contains('is-open');
      item.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', String(open));
    }));
    window.addEventListener('resize', () => { if (window.innerWidth > 980) setOpen(false); });
  }

  /* ---------- Reveal on scroll ---------- */
  function initReveal() {
    const items = $$('[data-reveal]');
    if (!('IntersectionObserver' in window) || reduceMotion) { items.forEach((el) => el.removeAttribute('data-reveal')); return; }
    items.forEach((el) => {
      const siblings = $$(':scope > [data-reveal]', el.parentElement);
      const idx = siblings.indexOf(el);
      if (idx > 0) el.style.setProperty('--d', `${Math.min(idx, 6) * 0.08}s`);
    });
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        el.classList.add('is-visible');
        io.unobserve(el);
        // hand transforms back to hover/tilt styles once the entrance finishes
        el.addEventListener('transitionend', function done(ev) {
          if (ev.target !== el || ev.propertyName !== 'opacity') return;
          el.removeAttribute('data-reveal'); el.classList.remove('is-visible'); el.style.removeProperty('--d');
          el.removeEventListener('transitionend', done);
        });
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    items.forEach((el) => io.observe(el));
  }

  /* ---------- Hero slideshow ---------- */
  function initHero() {
    const hero = $('[data-hero]');
    if (!hero) return;
    const slides = $$('.hero-slide', hero);
    const tabs = $$('[data-hero-tab]', hero);
    let current = 0;
    let timer = null;
    const show = (i) => {
      current = (i + slides.length) % slides.length;
      slides.forEach((s, n) => s.classList.toggle('is-active', n === current));
      tabs.forEach((t, n) => {
        t.classList.remove('is-active');
        t.setAttribute('aria-selected', String(n === current));
        if (n === current) { void t.offsetWidth; t.classList.add('is-active'); }
      });
    };
    const start = () => { stop(); if (!reduceMotion) timer = setInterval(() => show(current + 1), HERO_INTERVAL); };
    const stop = () => { if (timer) clearInterval(timer); timer = null; };
    tabs.forEach((t) => t.addEventListener('click', () => { show(Number(t.dataset.heroTab)); start(); }));
    document.addEventListener('visibilitychange', () => (document.hidden ? stop() : start()));
    let touchX = null;
    hero.addEventListener('touchstart', (e) => { touchX = e.touches[0].clientX; }, { passive: true });
    hero.addEventListener('touchend', (e) => {
      if (touchX === null) return;
      const dx = e.changedTouches[0].clientX - touchX;
      if (Math.abs(dx) > 50) { show(current + (dx < 0 ? 1 : -1)); start(); }
      touchX = null;
    }, { passive: true });
    show(0);
    start();
  }

  /* ---------- Animated counters ---------- */
  function initCounters() {
    const nums = $$('[data-count]');
    if (!nums.length) return;
    const run = (el) => {
      const target = Number(el.dataset.count);
      if (reduceMotion) { el.textContent = target; return; }
      const t0 = performance.now();
      const step = (t) => {
        const p = clamp((t - t0) / 1800, 0, 1);
        el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
        if (p < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    };
    const io = new IntersectionObserver((entries) => entries.forEach((e) => { if (e.isIntersecting) { run(e.target); io.unobserve(e.target); } }), { threshold: 0.6 });
    nums.forEach((n) => io.observe(n));
  }

  /* ---------- Parallax (uses the CSS `translate` property so transforms stay free) ---------- */
  function initParallax() {
    const els = $$('[data-parallax]');
    if (!els.length || reduceMotion) return;
    scrollTasks.push(() => {
      const vh = window.innerHeight;
      els.forEach((el) => {
        const r = el.getBoundingClientRect();
        if (r.bottom < -200 || r.top > vh + 200) return;
        const offset = (r.top + r.height / 2 - vh / 2) * Number(el.dataset.parallax);
        el.style.translate = `0 ${offset.toFixed(1)}px`;
      });
    });
  }

  /* ---------- Pinned horizontal scroll (menu) ---------- */
  function initHorizontal() {
    $$('[data-hscroll]').forEach((section) => {
      const sticky = $('.hs-sticky', section);
      const viewport = $('.hs-viewport', section);
      const track = $('.hs-track', section);
      const bar = $('.hs-progress', section);
      let distance = 0;
      const setup = () => {
        const pin = isDesktop() && !reduceMotion;
        section.classList.toggle('is-pinned', pin);
        track.style.transform = '';
        section.style.height = '';
        if (!pin) return;
        distance = Math.max(0, track.scrollWidth - viewport.clientWidth);
        section.style.height = `${sticky.offsetHeight + distance}px`;
      };
      const update = () => {
        if (!section.classList.contains('is-pinned')) return;
        const p = distance ? clamp((headerH() - section.getBoundingClientRect().top) / distance, 0, 1) : 0;
        track.style.transform = `translate3d(${(-p * distance).toFixed(1)}px,0,0)`;
        if (bar) bar.style.setProperty('--p', p.toFixed(3));
      };
      viewport.addEventListener('scroll', () => {
        const max = viewport.scrollWidth - viewport.clientWidth;
        if (bar && max > 0) bar.style.setProperty('--p', (viewport.scrollLeft / max).toFixed(3));
      }, { passive: true });
      setup();
      window.addEventListener('load', () => { setup(); update(); });
      let rt;
      window.addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(() => { setup(); update(); }, 150); });
      scrollTasks.push(update);
    });
  }

  /* ---------- Zoom band: image expands & settles as it scrolls in ---------- */
  function initZoom() {
    const bands = $$('[data-zoom]');
    if (!bands.length) return;
    if (reduceMotion) { bands.forEach((b) => b.style.setProperty('--p', 1)); return; }
    scrollTasks.push(() => {
      const vh = window.innerHeight;
      bands.forEach((b) => {
        const r = b.getBoundingClientRect();
        b.style.setProperty('--p', clamp((vh - r.top) / (vh * 0.85), 0, 1).toFixed(3));
      });
    });
  }

  /* ---------- Lazy, muted preview loops ---------- */
  function initLazyVideos() {
    const vids = $$('video[data-lazy-video]');
    const saveData = navigator.connection && navigator.connection.saveData;
    if (!vids.length || reduceMotion || saveData || !('IntersectionObserver' in window)) return;
    const io = new IntersectionObserver((entries) => {
      entries.forEach(({ target: v, isIntersecting }) => {
        if (isIntersecting) {
          const source = $('source[data-src]', v);
          if (source) { source.src = source.dataset.src; source.removeAttribute('data-src'); v.load(); }
          const played = v.play();
          if (played && played.catch) played.catch(() => {});
        } else if (!v.paused) {
          v.pause();
        }
      });
    }, { rootMargin: '120px 0px', threshold: 0.2 });
    vids.forEach((v) => io.observe(v));
  }

  /* ---------- Lightbox for images & full videos ---------- */
  function initLightbox() {
    const box = $('#lightbox');
    if (!box) return;
    const media = $('.lb-media', box);
    const caption = $('.lb-caption', box);
    let group = [];
    let index = 0;
    let opener = null;
    const render = () => {
      const el = group[index];
      media.innerHTML = '';
      const title = el.dataset.title || '';
      if (el.dataset.type === 'video') {
        const v = document.createElement('video');
        Object.assign(v, { src: el.dataset.src, controls: true, autoplay: true, playsInline: true });
        if (el.dataset.poster) v.poster = el.dataset.poster;
        v.setAttribute('aria-label', title);
        media.appendChild(v);
      } else {
        const img = document.createElement('img');
        img.src = el.dataset.src;
        img.alt = title;
        media.appendChild(img);
      }
      caption.textContent = group.length > 1 ? `${title} · ${index + 1} / ${group.length}` : title;
      box.classList.toggle('single', group.length < 2);
    };
    const open = (el) => {
      const name = el.dataset.lightbox;
      group = $$(`[data-lightbox="${name}"]`).filter((n) => !n.closest('.is-hidden'));
      index = Math.max(0, group.indexOf(el));
      opener = el;
      render();
      box.hidden = false;
      document.body.style.overflow = 'hidden';
      $('[data-lb-close]', box).focus();
    };
    const close = () => {
      box.hidden = true;
      media.innerHTML = '';
      document.body.style.overflow = '';
      if (opener) opener.focus();
    };
    const go = (d) => { if (group.length > 1) { index = (index + d + group.length) % group.length; render(); } };
    document.addEventListener('click', (e) => {
      const trigger = e.target.closest('[data-lightbox]');
      if (trigger) { e.preventDefault(); open(trigger); }
    });
    $('[data-lb-close]', box).addEventListener('click', close);
    $('[data-lb-prev]', box).addEventListener('click', () => go(-1));
    $('[data-lb-next]', box).addEventListener('click', () => go(1));
    box.addEventListener('click', (e) => { if (e.target === box) close(); });
    document.addEventListener('keydown', (e) => {
      if (box.hidden) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowRight') go(1);
      if (e.key === 'ArrowLeft') go(-1);
    });
    let sx = null;
    box.addEventListener('touchstart', (e) => { sx = e.touches[0].clientX; }, { passive: true });
    box.addEventListener('touchend', (e) => { if (sx !== null && Math.abs(e.changedTouches[0].clientX - sx) > 50) go(e.changedTouches[0].clientX < sx ? 1 : -1); sx = null; }, { passive: true });
  }

  /* ---------- Auto-sliding carousel ---------- */
  function initCarousels() {
    $$('[data-carousel]').forEach((car) => {
      const vp = $('.car-viewport', car);
      const step = () => { const card = $('.car-track > *', car); return card ? card.offsetWidth + 18 : 300; };
      const move = (dir) => {
        const atEnd = vp.scrollLeft + vp.clientWidth >= vp.scrollWidth - 8;
        const atStart = vp.scrollLeft <= 8;
        if (dir > 0 && atEnd) vp.scrollTo({ left: 0 });
        else if (dir < 0 && atStart) vp.scrollTo({ left: vp.scrollWidth });
        else vp.scrollBy({ left: dir * step() });
      };
      $('[data-car-prev]', car).addEventListener('click', () => move(-1));
      $('[data-car-next]', car).addEventListener('click', () => move(1));
      if (reduceMotion) return;
      let visible = false;
      let paused = false;
      new IntersectionObserver(([e]) => { visible = e.isIntersecting; }, { threshold: 0.3 }).observe(car);
      ['mouseenter', 'touchstart', 'focusin'].forEach((ev) => car.addEventListener(ev, () => { paused = true; }, { passive: true }));
      ['mouseleave', 'focusout'].forEach((ev) => car.addEventListener(ev, () => { paused = false; }));
      car.addEventListener('touchend', () => setTimeout(() => { paused = false; }, 4000), { passive: true });
      setInterval(() => { if (visible && !paused && !document.hidden) move(1); }, CAROUSEL_INTERVAL);
    });
  }

  /* ---------- Gallery filters ---------- */
  function initFilters() {
    const grid = $('[data-gallery]');
    if (!grid) return;
    const chips = $$('[data-filter]');
    chips.forEach((chip) => chip.addEventListener('click', () => {
      const cat = chip.dataset.filter;
      chips.forEach((c) => { c.classList.toggle('is-active', c === chip); c.setAttribute('aria-pressed', String(c === chip)); });
      $$('.masonry-item', grid).forEach((item) => {
        const show = cat === 'All' || item.dataset.category === cat;
        item.classList.toggle('is-hidden', !show);
        if (show) { item.removeAttribute('data-reveal'); item.animate?.([{ opacity: 0, transform: 'scale(.94)' }, { opacity: 1, transform: 'none' }], { duration: 450, easing: 'ease-out' }); }
      });
    }));
  }

  /* ---------- Menu category scroll-spy ---------- */
  function initMenuSpy() {
    const nav = $('[data-menu-nav]');
    if (!nav) return;
    const track = $('.menu-nav-track', nav);
    const links = $$('a', nav);
    const setActive = (id) => links.forEach((a) => {
      const on = a.getAttribute('href') === `#${id}`;
      a.classList.toggle('is-active', on);
      if (on) track.scrollTo({ left: a.offsetLeft - track.clientWidth / 2 + a.offsetWidth / 2, behavior: 'smooth' });
    });
    const io = new IntersectionObserver((entries) => entries.forEach((e) => { if (e.isIntersecting) setActive(e.target.id); }), { rootMargin: '-35% 0px -60% 0px' });
    $$('.menu-cat').forEach((s) => io.observe(s));
  }

  /* ---------- Hover-like feedback on touch + subtle 3D tilt on mouse ---------- */
  function initTouchAndTilt() {
    const selector = '.btn, .tilt, .service-card, .cuisine-card, .gallery-card, .video-card, .testimonial-card, .feature-mini, .contact-tile, .stack-card, .info-card';
    document.addEventListener('touchstart', (e) => {
      const el = e.target.closest(selector);
      if (!el) return;
      el.classList.add('is-touched');
      const clear = () => { setTimeout(() => el.classList.remove('is-touched'), 450); el.removeEventListener('touchend', clear); el.removeEventListener('touchcancel', clear); };
      el.addEventListener('touchend', clear, { passive: true });
      el.addEventListener('touchcancel', clear, { passive: true });
    }, { passive: true });
    if (reduceMotion) return;
    $$('.tilt').forEach((el) => {
      el.addEventListener('pointermove', (e) => {
        if (e.pointerType !== 'mouse') return;
        const r = el.getBoundingClientRect();
        el.style.setProperty('--ry', `${(((e.clientX - r.left) / r.width) - 0.5) * 8}deg`);
        el.style.setProperty('--rx', `${(0.5 - ((e.clientY - r.top) / r.height)) * 8}deg`);
      });
      el.addEventListener('pointerleave', () => { el.style.removeProperty('--rx'); el.style.removeProperty('--ry'); });
    });
  }

  /* ---------- Enquiry form -> WhatsApp (or email) ---------- */
  function initForms() {
    $$('[data-quote-form]').forEach((form) => {
      const status = $('.form-status', form);
      const mailLink = $('[data-mail-link]', form);
      const labels = { name: 'Name', phone: 'Phone', email: 'Email', event: 'Event', date: 'Event date', guests: 'Guests', message: 'Details' };
      const compose = () => {
        const data = new FormData(form);
        const lines = ['Hello Shubh Caterers, I would like a catering quote.'];
        Object.keys(labels).forEach((k) => { const v = (data.get(k) || '').toString().trim(); if (v) lines.push(`${labels[k]}: ${v}`); });
        return lines.join('\n');
      };
      const syncMail = () => { if (mailLink) mailLink.href = `mailto:${EMAIL}?subject=${encodeURIComponent('Catering enquiry')}&body=${encodeURIComponent(compose())}`; };
      form.addEventListener('input', (e) => { const f = e.target.closest('.field'); if (f) f.classList.remove('has-error'); syncMail(); });
      syncMail();
      form.addEventListener('submit', (e) => {
        e.preventDefault();
        const invalid = $$('input, select, textarea', form).filter((f) => !f.checkValidity());
        $$('.field', form).forEach((f) => f.classList.remove('has-error'));
        if (invalid.length) {
          invalid.forEach((f) => f.closest('.field')?.classList.add('has-error'));
          status.textContent = 'Please enter your name, a valid phone number and the event type.';
          status.classList.add('is-error');
          invalid[0].focus();
          return;
        }
        status.classList.remove('is-error');
        window.open(`https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(compose())}`, '_blank', 'noopener');
        status.textContent = 'WhatsApp has opened with your enquiry — just tap send. Thank you!';
      });
    });
  }

  initHeader(); initNav(); initReveal(); initHero(); initCounters(); initParallax(); initHorizontal(); initZoom();
  initLazyVideos(); initLightbox(); initCarousels(); initFilters(); initMenuSpy(); initTouchAndTilt(); initForms();
  requestTick();
})();
