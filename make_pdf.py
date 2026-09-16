#!/usr/bin/env python3
"""Build the Asian Paints complete shade book PDF (A4 landscape, 30 swatches/page)."""
import json
import html as htmllib
import re
from datetime import date
from pathlib import Path

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

ROOT = Path(__file__).resolve().parent
SRC = ROOT / 'data' / 'shades.jsonl'
OUT = Path('/home/apv/.openclaw/workspace/asian_paints_complete_shade_book.pdf')

PAGE_W, PAGE_H = landscape(A4)          # 841.89 x 595.28
MARGIN = 28
COLS, ROWS = 6, 5
GAP = 10
HEADER_ZONE = 34
FOOTER_ZONE = 14
GRID_TOP = PAGE_H - MARGIN - HEADER_ZONE          # top of first card row
CARD_W = (PAGE_W - 2 * MARGIN - (COLS - 1) * GAP) / COLS
CARD_H = (GRID_TOP - MARGIN - FOOTER_ZONE - (ROWS - 1) * GAP) / ROWS
BLOCK_H = CARD_H * 0.60                            # color block height
TEXT_X_PAD = 5

INK = Color(0.10, 0.10, 0.12)
GREY = Color(0.45, 0.45, 0.48)
LIGHT_RULE = Color(0.82, 0.82, 0.84)
CARD_BORDER = Color(0.72, 0.72, 0.75)
FAMILY_COLORS = {  # representative header accent per family (hex pulled from palette)
    'blue': '#1F5FBF', 'brown': '#6B4226', 'green': '#2E7D32', 'grey': '#6D6E71',
    'off-white': '#C9C5BA', 'orange': '#E8721C', 'pink': '#D6527E', 'purple': '#6A3BA5',
    'red': '#C0272D', 'white': '#BFBFBF', 'yellow': '#E3B505',
}


def fam_display(slug):
    words = slug.split('-')
    return '-'.join(w.capitalize() for w in words)


def hex_rgb(h):
    h = h.lstrip('#')
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def load_shades():
    recs, seen = [], set()
    for line in SRC.read_text(encoding='utf-8').splitlines():
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not (r.get('complete') and r.get('hex')):
            continue
        if r['url'] in seen:
            continue
        seen.add(r['url'])
        name = htmllib.unescape(str(r['name'])).strip()
        name = re.sub(r'\s+', ' ', name)
        if not name:
            name = str(r['code'])
        recs.append({'family': r['family'], 'name': name,
                     'code': str(r['code']).strip(), 'hex': r['hex'].upper()})
    recs.sort(key=lambda r: (r['family'], r['name'].lower()))
    return recs


class Book:
    def __init__(self, path, families_meta):
        self.c = canvas.Canvas(str(path), pagesize=(PAGE_W, PAGE_H))
        self.c.setTitle('Asian Paints — Complete Shade Book')
        self.c.setAuthor('William (OpenClaw) — data: asianpaints.com')
        self.page_num = 1
        self.families_meta = families_meta

    def footer(self, family=None):
        c = self.c
        c.setFont('Helvetica', 6.5)
        c.setFillColor(GREY)
        c.drawString(MARGIN, MARGIN / 2 + 2, 'asianpaints.com colour catalogue · scraped 2026-09-16')
        c.drawRightString(PAGE_W - MARGIN, MARGIN / 2 + 2, f'Page {self.page_num}')
        if family:
            c.drawCentredString(PAGE_W / 2, MARGIN / 2 + 2, fam_display(family))

    def family_header(self, family, count, continued=False):
        c = self.c
        y = PAGE_H - MARGIN - 8
        accent = hex_rgb(FAMILY_COLORS.get(family, '#888888'))
        c.setFillColorRGB(*[v / 255 for v in accent])
        c.rect(MARGIN, y - 14, 5, 20, stroke=0, fill=1)
        c.setFillColor(INK)
        c.setFont('Helvetica-Bold', 17)
        title = fam_display(family).upper() + ('  (cont.)' if continued else '')
        c.drawString(MARGIN + 12, y - 8, title)
        c.setFont('Helvetica', 9)
        c.setFillColor(GREY)
        if not continued:
            c.drawRightString(PAGE_W - MARGIN, y - 8, f'{count} shades')
        c.setStrokeColor(LIGHT_RULE)
        c.setLineWidth(0.7)
        c.line(MARGIN, y - 20, PAGE_W - MARGIN, y - 20)

    def swatch(self, x, y, s):
        c = self.c
        # color block
        r, g, b = hex_rgb(s['hex'])
        c.setFillColorRGB(r / 255, g / 255, b / 255)
        c.setStrokeColor(CARD_BORDER)
        c.setLineWidth(0.6)
        c.rect(x, y + CARD_H - BLOCK_H, CARD_W, BLOCK_H, stroke=1, fill=1)
        # text
        tx = x + TEXT_X_PAD
        ty = y + CARD_H - BLOCK_H - 12
        c.setFillColor(INK)
        c.setFont('Helvetica-Bold', 9.5)
        c.drawString(tx, ty, s['code'])
        c.setFillColor(Color(0.20, 0.20, 0.24))
        size = 8.2
        while size > 5.4 and stringWidth(s['name'], 'Helvetica', size) > CARD_W - 2 * TEXT_X_PAD:
            size -= 0.3
        c.setFont('Helvetica', size)
        c.drawString(tx, ty - 12, s['name'])
        c.setFillColor(GREY)
        c.setFont('Helvetica', 7)
        c.drawString(tx, ty - 22.5, s['hex'])

    def cover(self, total, families):
        c = self.c
        c.setFillColor(Color(1, 1, 1))
        c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        # family color strip
        strip_h = 16
        seg = PAGE_W / len(families)
        for i, fam in enumerate(families):
            r, g, b = hex_rgb(FAMILY_COLORS.get(fam, '#888888'))
            c.setFillColorRGB(r / 255, g / 255, b / 255)
            c.rect(i * seg, PAGE_H - strip_h, seg + 0.5, strip_h, stroke=0, fill=1)
        y = PAGE_H / 2 + 60
        c.setFillColor(INK)
        c.setFont('Helvetica-Bold', 42)
        c.drawCentredString(PAGE_W / 2, y, 'ASIAN PAINTS')
        c.setFont('Helvetica', 17)
        c.setFillColor(GREY)
        c.drawCentredString(PAGE_W / 2, y - 30, 'Complete Wall Colour Shade Book')
        c.setStrokeColor(LIGHT_RULE)
        c.setLineWidth(0.8)
        c.line(PAGE_W / 2 - 120, y - 48, PAGE_W / 2 + 120, y - 48)
        c.setFont('Helvetica', 11)
        c.setFillColor(INK)
        c.drawCentredString(PAGE_W / 2, y - 76,
                            f'{total} shades  ·  {len(families)} colour families  ·  {date.today():%d %b %Y}')
        c.setFont('Helvetica', 8.5)
        c.setFillColor(GREY)
        c.drawCentredString(PAGE_W / 2, y - 94,
                            'Source: asianpaints.com/colour-catalogue  ·  RGB values as published per shade')
        self.footer()
        c.showPage()
        self.page_num += 1

    def run(self, by_family):
        total = sum(len(v) for v in by_family.values())
        self.cover(total, list(by_family.keys()))
        for fam, shades in by_family.items():
            page_open = False
            idx = 0
            for s in shades:
                if not page_open:
                    self.family_header(fam, len(shades), continued=(idx > 0))
                    page_open = True
                col = idx % COLS
                row = idx // COLS
                x = MARGIN + col * (CARD_W + GAP)
                y_top = GRID_TOP - row * (CARD_H + GAP)
                self.swatch(x, y_top - CARD_H, s)
                idx += 1
                if idx % (COLS * ROWS) == 0 and idx < len(shades):
                    self.footer(fam)
                    self.c.showPage()
                    self.page_num += 1
                    page_open = False
            if page_open:
                self.footer(fam)
                self.c.showPage()
                self.page_num += 1
        self.c.save()
        return self.page_num - 1  # pages incl. cover


def main():
    recs = load_shades()
    by_family = {}
    for r in recs:
        by_family.setdefault(r['family'], []).append(r)
    book = Book(OUT, by_family)
    pages = book.run(by_family)
    print(f'shades={len(recs)} families={len(by_family)} pages={pages} out={OUT}')
    print('per-family:', {fam_display(k): len(v) for k, v in by_family.items()})


if __name__ == '__main__':
    main()
