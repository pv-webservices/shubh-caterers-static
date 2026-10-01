"""Builds every web image from the masters in source-files/.  Run:  python generator/images.py

- source-files/images/<folder>/<name>.webp -> assets/images/<folder>/<name>-<width>.{avif,webp}
- source-files/brand/logo-transparent.webp -> assets/images/brand/logo-{240,480}.webp
- source-files/brand/logo-original.jpeg     -> favicons in static/ (emblem on a solid background)
- page hero masters                        -> assets/images/og/<name>.jpg (1200x630 social cards)

Outputs are skipped when they are newer than their master, so re-running is cheap.
"""
import base64
import io
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'source-files'
MASTERS = SOURCE / 'images'
OUT = ROOT / 'assets' / 'images'
STATIC = ROOT / 'static'
MANIFEST = OUT / 'manifest.json'   # widths + intrinsic size of every responsive image, read by templates.py

BREAKPOINTS = (480, 800, 1200)
MIN_GAP = 120                      # skip a breakpoint that is within this many px of the master width
WEBP_QUALITY = 78
AVIF_QUALITY = 52
OG_SIZE = (1200, 630)
CREAM = (255, 250, 241)
MAROON = '#7a0c0c'


def is_fresh(target, source):
    return target.exists() and target.stat().st_mtime >= source.stat().st_mtime


def widths_for(master_width):
    return [w for w in BREAKPOINTS if w < master_width - MIN_GAP] + [master_width]


def responsive_images():
    manifest = {}
    for master in sorted(MASTERS.rglob('*.webp')):
        key = master.relative_to(MASTERS).with_suffix('').as_posix()
        with Image.open(master) as im:
            im = im.convert('RGB')
            w, h = im.size
            ws = widths_for(w)
            manifest[key] = {'width': w, 'height': h, 'widths': ws}
            for width in ws:
                size = (width, round(h * width / w))
                for fmt, opts in (('webp', {'quality': WEBP_QUALITY, 'method': 6}), ('avif', {'quality': AVIF_QUALITY})):
                    target = OUT / f'{key}-{width}.{fmt}'
                    if is_fresh(target, master):
                        continue
                    target.parent.mkdir(parents=True, exist_ok=True)
                    resized = im if width == w else im.resize(size, Image.LANCZOS)
                    resized.save(target, fmt.upper(), **opts)
    MANIFEST.write_text(json.dumps(manifest, indent=1, sort_keys=True) + '\n', encoding='utf-8')
    return manifest


def logos():
    master = SOURCE / 'brand' / 'logo-transparent.webp'
    with Image.open(master) as im:
        im = im.convert('RGBA')
        for width in (240, 480):
            target = OUT / 'brand' / f'logo-{width}.webp'
            if not is_fresh(target, master):
                im.resize((width, round(im.height * width / im.width)), Image.LANCZOS).save(target, 'WEBP', quality=88, method=6)


def emblem():
    """The swastik emblem from the original logo, the 'S' letter masked out, on the site's cream colour."""
    with Image.open(SOURCE / 'brand' / 'logo-original.jpeg') as im:
        im = im.convert('RGB')
    ImageDraw.Draw(im).rectangle([568, 315, 700, 565], fill=(255, 255, 255))
    crop = im.crop((30, 120, 680, 770))
    tinted = ImageChops.multiply(crop, Image.new('RGB', crop.size, CREAM))
    pad = round(crop.width * 0.08)
    return ImageOps.expand(tinted, border=pad, fill=CREAM)


def favicons():
    master = SOURCE / 'brand' / 'logo-original.jpeg'
    if is_fresh(STATIC / 'favicon.ico', master):
        return
    STATIC.mkdir(exist_ok=True)
    icon = emblem()
    sized = lambda s: icon.resize((s, s), Image.LANCZOS)
    for name, s in (('favicon-48x48.png', 48), ('favicon-96x96.png', 96), ('apple-touch-icon.png', 180),
                    ('web-app-manifest-192x192.png', 192), ('web-app-manifest-512x512.png', 512)):
        sized(s).save(STATIC / name, 'PNG', optimize=True)
    sized(48).save(STATIC / 'favicon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])
    # No vector logo exists, so the SVG wraps a crisp 128px raster of the emblem.
    buf = io.BytesIO()
    sized(128).save(buf, 'PNG', optimize=True)
    data = base64.b64encode(buf.getvalue()).decode()
    (STATIC / 'favicon.svg').write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 128 128" width="128" height="128">'
        f'<rect width="128" height="128" fill="#fffaf1"/><image width="128" height="128" xlink:href="data:image/png;base64,{data}"/></svg>\n',
        encoding='utf-8')
    manifest = {
        'name': 'Shubh Caterers', 'short_name': 'Shubh Caterers',
        'description': 'Pure vegetarian catering in Pune for weddings, corporate events and celebrations.',
        'start_url': '/', 'scope': '/', 'display': 'standalone',
        'theme_color': MAROON, 'background_color': '#fffaf1',
        'icons': [
            {'src': '/web-app-manifest-192x192.png', 'sizes': '192x192', 'type': 'image/png', 'purpose': 'any'},
            {'src': '/web-app-manifest-512x512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any'},
            {'src': '/web-app-manifest-512x512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'},
        ],
    }
    (STATIC / 'site.webmanifest').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')


def og_images(keys):
    """1200x630 social share cards: the page's hero photo with the logo on a cream badge."""
    with Image.open(SOURCE / 'brand' / 'logo-transparent.webp') as logo:
        logo = logo.convert('RGBA')
        logo = logo.resize((300, round(logo.height * 300 / logo.width)), Image.LANCZOS)
    for key in keys:
        master = MASTERS / f'{key}.webp'
        target = OUT / 'og' / f'{key.split("/")[-1]}.jpg'
        if is_fresh(target, master):
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(master) as im:
            card = ImageOps.fit(im.convert('RGB'), OG_SIZE, Image.LANCZOS, centering=(0.5, 0.5))
        badge = Image.new('RGBA', (logo.width + 40, logo.height + 28), (*CREAM, 238))
        mask = Image.new('L', badge.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, badge.width - 1, badge.height - 1], radius=18, fill=238)
        badge.putalpha(mask)
        badge.alpha_composite(logo, (20, 14))
        card.paste(badge, (40, OG_SIZE[1] - badge.height - 40), badge)
        card.save(target, 'JPEG', quality=82, optimize=True, progressive=True)


if __name__ == '__main__':
    found = responsive_images()
    logos()
    favicons()
    og_images([k for k in found if not k.startswith('video-posters/')])
    print(f'Images ready: {len(found)} responsive masters, logos, favicons, OG cards')
