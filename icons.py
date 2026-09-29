"""Inline SVG line icons (24x24, stroke = currentColor)."""

PATHS = {
    'rings': '<circle cx="9" cy="14.5" r="5.5"/><circle cx="15" cy="14.5" r="5.5"/><path d="M7.5 5.5 9 3h6l1.5 2.5L12 9z"/>',
    'glass': '<path d="M4 4h16l-8 9z"/><path d="M12 13v7M8 20h8M7.5 7.5h9"/><circle cx="17.5" cy="3" r="1.4"/>',
    'briefcase': '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18M11 12h2v2h-2z"/>',
    'confetti': '<path d="m4 20 5-13 8 8z"/><path d="M14 4c1 1 1 2.5 0 3.5M19 9c-1-1-2.5-1-3.5 0M17 3l.5 1.5M20.5 5.5l1 .5M21 12l1 .5"/><path d="m7 13 4 4"/>',
    'cheers': '<path d="M5 3h5l-.6 6a2.4 2.4 0 0 1-4.8 0z"/><path d="M14 3h5l.6 6a2.4 2.4 0 0 1-4.8 0z" transform="rotate(12 16.5 6)"/><path d="M7.5 11.5V20M5 20h5M16.8 11.8 15.5 20M13 20h5"/>',
    'star': '<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>',
    'institution': '<path d="M3 9 12 4l9 5M4 9h16M5 9v9M9.5 9v9M14.5 9v9M19 9v9M3 21h18M4 18h16"/>',
    'cake': '<path d="M4 21V13a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8M3 21h18M4 16c2 1.5 4 1.5 5.3 0 1.4 1.5 4 1.5 5.4 0 1.3 1.5 3.3 1.5 5.3 0M12 11V7M12 3.5c.9.9.9 2 0 2.6-.9-.6-.9-1.7 0-2.6"/>',
    'home': '<path d="M3 11.5 12 4l9 7.5M5 10v10h14V10"/><path d="M10 20v-5h4v5"/>',
    'parcel': '<path d="M3 7.5 12 3l9 4.5v9L12 21l-9-4.5z"/><path d="M3 7.5 12 12l9-4.5M12 12v9M7.5 5.2l9 4.6"/>',
    'cradle': '<path d="M4 10h11a5 5 0 0 1-5 6H9a5 5 0 0 1-5-6z"/><path d="M15 10a6 6 0 0 0-6-6v6M20 4l-3 6"/><circle cx="7" cy="19" r="1.6"/><circle cx="14" cy="19" r="1.6"/>',
    'sparkle': '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/><circle cx="12" cy="12" r="2"/>',
    'cloche': '<path d="M3 17h18M4.5 17a7.5 7.5 0 0 1 15 0M12 9.5V8M10.5 7.5h3M2 20h20"/>',
    'team': '<circle cx="9" cy="8" r="3"/><path d="M3 20a6 6 0 0 1 12 0"/><circle cx="17" cy="9" r="2.4"/><path d="M15.5 14.2A5 5 0 0 1 21 19"/>',
    'diamond': '<path d="M6 3h12l3 6-9 12L3 9z"/><path d="M3 9h18M9 3l-1.5 6L12 21l4.5-12L15 3"/>',
    'leaf': '<path d="M5 19C5 10 11 5 20 4c-1 9-6 15-15 15z"/><path d="M5 19 13 11"/>',
    'phone': '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
    'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    'pin': '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
    'arrow-left': '<path d="M19 12H5M11 6l-6 6 6 6"/>',
    'play': '<path d="M8 5v14l11-7z" fill="currentColor"/>',
    'close': '<path d="M6 6l12 12M18 6 6 18"/>',
    'check': '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    'chef': '<path d="M7 14.5V20h10v-5.5M7 14.5A4 4 0 0 1 6.5 7a5.5 5.5 0 0 1 11 0 4 4 0 0 1-.5 7.5zM7 17.5h10"/>',
    'calendar': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    'users': '<circle cx="12" cy="8" r="3.5"/><path d="M5 20a7 7 0 0 1 14 0"/>',
    'flame': '<path d="M12 3c1 3.5 5 5.5 5 10a5 5 0 0 1-10 0c0-2.2 1-3.6 2.4-4.8.3 1.5 1 2.3 2 2.8C11 8.5 11 5.5 12 3z"/>',
    'menu-book': '<path d="M4 4.5A1.5 1.5 0 0 1 5.5 3H20v15H5.5A1.5 1.5 0 0 0 4 19.5zM4 19.5A1.5 1.5 0 0 0 5.5 21H20v-3"/><path d="M9 8h7M9 11.5h5"/>',
    'quote': '<path d="M4 18v-5c0-4 2-6.5 6-8l.8 1.5C8.3 7.8 7.5 9.2 7.5 11H10v7zM13 18v-5c0-4 2-6.5 6-8l.8 1.5c-2.5 1.3-3.3 2.7-3.3 4.5H19v7z" fill="currentColor" stroke="none"/>',
    'whatsapp': '<path d="M12 2.2A9.7 9.7 0 0 0 3.6 16.8L2.2 21.8l5.1-1.3A9.7 9.7 0 1 0 12 2.2zm0 17.7a8 8 0 0 1-4.1-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8 8 0 1 1 12 19.9zm4.4-6c-.2-.1-1.4-.7-1.7-.8-.2-.1-.4-.1-.5.1l-.8 1c-.1.2-.3.2-.5.1a6.5 6.5 0 0 1-3.2-2.8c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.5-.4h-.5a.9.9 0 0 0-.6.3 2.7 2.7 0 0 0-.9 2c0 1.2.9 2.4 1 2.5.1.2 1.7 2.7 4.2 3.8 1.6.7 2.2.7 3 .6.5-.1 1.4-.6 1.6-1.1.2-.6.2-1 .1-1.1l-.4-.3z" fill="currentColor" stroke="none"/>',
    'map': '<path d="M9 4 3 6.5v13.5L9 17.5l6 2.5 6-2.5V4L15 6.5z"/><path d="M9 4v13.5M15 6.5V20"/>',
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    'veg': '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="12" cy="12" r="4.5" fill="currentColor" stroke="none"/>',
}


def icon(name, size=24, cls='', stroke=1.6):
    cls_attr = f' class="{cls}"' if cls else ''
    return (f'<svg{cls_attr} aria-hidden="true" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="{stroke}" stroke-linecap="round" stroke-linejoin="round">{PATHS[name]}</svg>')


# Decorative ornament above section eyebrows (lotus / diya motif)
ORNAMENT = ('<svg class="ornament" aria-hidden="true" width="44" height="22" viewBox="0 0 44 22" fill="none" stroke="currentColor" '
            'stroke-width="1.3" stroke-linecap="round"><path d="M22 3c3 3.5 3 8 0 12-3-4-3-8.5 0-12z"/>'
            '<path d="M22 15c-2.5-4-7-5.5-11-4.5 1.5 3.5 6 5.5 11 4.5zM22 15c2.5-4 7-5.5 11-4.5-1.5 3.5-6 5.5-11 4.5z"/>'
            '<path d="M2 18h14M28 18h14"/><circle cx="22" cy="19" r="1.3" fill="currentColor"/></svg>')

# Gold leaf sprig used as floating decoration (parallax)
SPRIG = ('<svg aria-hidden="true" viewBox="0 0 120 160" fill="none"><path d="M60 158C58 110 62 60 86 10" stroke="#b8862f" stroke-width="2"/>'
         '<g fill="#d3a24a" fill-opacity=".9"><path d="M64 120c-18-4-30-16-32-32 16 2 28 14 32 32z"/><path d="M66 96c16-6 26-20 26-36-14 5-24 18-26 36z"/>'
         '<path d="M70 70c-16-4-26-16-28-30 14 2 25 13 28 30z"/><path d="M76 46c12-6 19-17 18-30-11 5-18 16-18 30z"/></g>'
         '<g fill="#a31a1a"><circle cx="40" cy="132" r="7"/><circle cx="96" cy="84" r="5"/></g></svg>')
