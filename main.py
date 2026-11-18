#!/usr/bin/env python3
"""THE WORLD TODAY - front page for Tuesday 17 November 2026.

Draws a 1024x1024 newspaper front page summing up the day's world news.
Pure Python 3.13 standard library only: no network, no clock, no randomness.
Two runs produce byte-identical output.
"""
import os
import struct
import zlib

W, H = 1024, 1024
PAPER = (247, 243, 234)   # warm newsprint
INK = (17, 17, 17)        # near-black
RED = (158, 27, 23)       # headline red
BLUE = (24, 52, 96)       # navy accent
GREY = (96, 92, 84)       # rule grey

# ---------------------------------------------------------------- font: 5x7
# Each glyph: 7 rows, 5 bits each (bit 4 = leftmost pixel).
FONT = {
    'A': (0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    'B': (0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E),
    'C': (0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E),
    'D': (0x1E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1E),
    'E': (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F),
    'F': (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10),
    'G': (0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0F),
    'H': (0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    'I': (0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E),
    'J': (0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0C),
    'K': (0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11),
    'L': (0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F),
    'M': (0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11),
    'N': (0x11, 0x19, 0x15, 0x13, 0x11, 0x11, 0x11),
    'O': (0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    'P': (0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10),
    'Q': (0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D),
    'R': (0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11),
    'S': (0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E),
    'T': (0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04),
    'U': (0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    'V': (0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04),
    'W': (0x11, 0x11, 0x11, 0x15, 0x15, 0x1B, 0x11),
    'X': (0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11),
    'Y': (0x11, 0x11, 0x0A, 0x04, 0x04, 0x04, 0x04),
    'Z': (0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F),
    '0': (0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E),
    '1': (0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E),
    '2': (0x0E, 0x11, 0x01, 0x06, 0x08, 0x10, 0x1F),
    '3': (0x1F, 0x02, 0x04, 0x02, 0x01, 0x11, 0x0E),
    '4': (0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02),
    '5': (0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E),
    '6': (0x06, 0x08, 0x10, 0x1E, 0x11, 0x11, 0x0E),
    '7': (0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08),
    '8': (0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E),
    '9': (0x0E, 0x11, 0x11, 0x0F, 0x01, 0x02, 0x0C),
    ' ': (0, 0, 0, 0, 0, 0, 0),
    '.': (0, 0, 0, 0, 0, 0x0C, 0x0C),
    ',': (0, 0, 0, 0, 0x0C, 0x04, 0x08),
    '-': (0, 0, 0, 0x0E, 0, 0, 0),
    ':': (0, 0x0C, 0x0C, 0, 0x0C, 0x0C, 0),
    ';': (0, 0x0C, 0x0C, 0, 0x0C, 0x04, 0x08),
    '!': (0x04, 0x04, 0x04, 0x04, 0x04, 0x00, 0x04),
    '?': (0x0E, 0x11, 0x01, 0x02, 0x04, 0x00, 0x04),
    '(': (0x02, 0x04, 0x08, 0x08, 0x08, 0x04, 0x02),
    ')': (0x08, 0x04, 0x02, 0x02, 0x02, 0x04, 0x08),
    '/': (0x01, 0x01, 0x02, 0x04, 0x08, 0x10, 0x10),
    '%': (0x19, 0x19, 0x02, 0x04, 0x08, 0x13, 0x13),
    '$': (0x04, 0x0F, 0x14, 0x0E, 0x05, 0x1E, 0x04),
    '&': (0x0C, 0x12, 0x14, 0x08, 0x15, 0x12, 0x0D),
    '+': (0, 0x04, 0x04, 0x0E, 0x04, 0x04, 0),
    '=': (0, 0, 0x1F, 0, 0x1F, 0, 0),
    "'": (0x04, 0x04, 0x08, 0, 0, 0, 0),
    '"': (0x0A, 0x0A, 0x0A, 0, 0, 0, 0),
    '*': (0, 0x04, 0x15, 0x0E, 0x15, 0x04, 0),
    '[': (0x0E, 0x08, 0x08, 0x08, 0x08, 0x08, 0x0E),
    ']': (0x0E, 0x02, 0x02, 0x02, 0x02, 0x02, 0x0E),
    '_': (0, 0, 0, 0, 0, 0, 0x1F),
    '<': (0x02, 0x04, 0x08, 0x10, 0x08, 0x04, 0x02),
    '>': (0x08, 0x04, 0x02, 0x01, 0x02, 0x04, 0x08),
}
UNKNOWN = (0x1F, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1F)  # box for missing glyphs


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg) * (w * h)

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = c

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, c)

    def hline(self, x, y, w, c, t=1):
        self.rect(x, y, w, t, c)

    def vline(self, x, y, h, c, t=1):
        self.rect(x, y, t, h, c)

    def line(self, x0, y0, x1, y1, c, t=1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.rect(x0 - t // 2, y0 - t // 2, t, t, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, c, fill=False):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d = (xx - cx) ** 2 + (yy - cy) ** 2
                if fill:
                    if d <= r * r:
                        self.set(xx, yy, c)
                else:
                    if (r - 1) ** 2 <= d <= r * r:
                        self.set(xx, yy, c)

    def triangle(self, x0, y0, x1, y1, x2, y2, c):
        # filled triangle via scanline
        pts = sorted([(x0, y0), (x1, y1), (x2, y2)], key=lambda p: p[1])
        (ax, ay), (bx, by), (cx, cy) = pts
        def interp(xa, ya, xb, yb, y):
            return xa if yb == ya else xa + (xb - xa) * (y - ya) / (yb - ya)
        for y in range(ay, cy + 1):
            if y < by:
                xa = interp(ax, ay, bx, by, y)
                xb = interp(ax, ay, cx, cy, y)
            else:
                xa = interp(bx, by, cx, cy, y)
                xb = interp(ax, ay, cx, cy, y)
            for x in range(int(min(xa, xb)), int(max(xa, xb)) + 1):
                self.set(x, y, c)

    # -- text -------------------------------------------------------------
    def text(self, x, y, s, scale, c):
        """Draw text at top-left (x, y); returns width drawn."""
        s = s.upper()  # font is uppercase-only; normalise here
        cx = x
        for ch in s:
            g = FONT.get(ch, UNKNOWN)
            for row in range(7):
                bits = g[row]
                for col in range(5):
                    if bits & (1 << (4 - col)):
                        self.rect(cx + col * scale, y + row * scale,
                                  scale, scale, c)
            cx += 6 * scale
        return cx - x - scale  # width without trailing gap

    def text_w(self, s, scale):
        return len(s) * 6 * scale - scale

    def text_center(self, y, s, scale, c):
        self.text((W - self.text_w(s, scale)) // 2, y, s, scale, c)

    def wrap(self, s, scale, max_w):
        """Greedy word wrap; returns list of lines fitting max_w."""
        words, lines, cur = s.split(' '), [], ''
        for wd in words:
            trial = wd if not cur else cur + ' ' + wd
            if self.text_w(trial, scale) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        return lines


# ---------------------------------------------------------------- PNG
def write_png(cv, path):
    raw = bytearray()
    for y in range(cv.h):
        raw.append(0)  # filter: none
        raw += cv.px[y * cv.w * 3:(y + 1) * cv.w * 3]

    def chunk(kind, data):
        c = struct.pack('>I', len(data)) + kind + data
        return c + struct.pack('>I', zlib.crc32(kind + data) & 0xFFFFFFFF)

    ihdr = struct.pack('>IIBBBBB', cv.w, cv.h, 8, 2, 0, 0, 0)
    png = (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr)
           + chunk(b'IDAT', zlib.compress(bytes(raw), 9))
           + chunk(b'IEND', b''))
    with open(path, 'wb') as f:
        f.write(png)
    return len(png)

# ---------------------------------------------------------------- pictograms
def pic_bridge(cv, x, y, w, h, c):
    """A bridge over water, middle span collapsed."""
    deck = y + h // 3
    # piers
    cv.rect(x + 8, deck, 10, h - deck // 2, c)
    cv.rect(x + w - 18, deck, 10, h - deck // 2, c)
    cv.rect(x + w // 2 - 5, deck + 26, 10, h - deck // 2 - 26, c)
    # deck, left and right, middle section dropped into the water
    cv.rect(x, deck, w // 2 - 22, 7, c)
    cv.rect(x + w // 2 + 22, deck, w // 2 - 22, 7, c)
    cv.line(x + w // 2 - 22, deck + 7, x + w // 2 - 4, deck + 30, c, 5)
    cv.line(x + w // 2 + 22, deck + 7, x + w // 2 + 4, deck + 30, c, 5)
    # cables
    cv.line(x + 8, deck, x + w // 2 - 22, deck - 26, c, 2)
    cv.line(x + w - 18, deck, x + w // 2 + 22, deck - 26, c, 2)
    # water
    wy = y + h - 22
    for i in range(4):
        cv.line(x + 4 + i * 6, wy + i * 5, x + w - 4 - i * 6, wy + i * 5,
                BLUE, 3)
    # smoke from the gap: one grey puff above the break
    cv.circle(x + w // 2, deck - 2, 9, GREY, fill=True)


def pic_tanker(cv, x, y, w, h, c):
    """A tanker at sea with a mine blast."""
    wy = y + h - 30
    cv.rect(x + 10, wy - 34, w - 20, 30, c)          # hull
    cv.triangle(x + 10, wy - 4, x + 34, wy - 4, x + 10, wy + 16, c)
    cv.rect(x + w // 2 - 8, wy - 58, 16, 24, c)     # funnel
    cv.rect(x + 18, wy - 52, 8, 18, c)              # mast
    cv.line(x + 4, wy + 4, x + w - 4, wy + 4, BLUE, 3)
    cv.line(x + 10, wy + 12, x + w - 10, wy + 12, BLUE, 3)
    # mine blast star above the bow
    bx, by = x + w - 26, wy - 66
    for dx, dy in ((0, -14), (10, -10), (14, 0), (10, 10), (0, 14),
                   (-10, 10), (-14, 0), (-10, -10)):
        cv.line(bx, by, bx + dx, by + dy, RED, 4)
    cv.circle(bx, by, 5, RED, fill=True)


def pic_carrier(cv, x, y, w, h, c):
    """An aircraft carrier with a jet above."""
    wy = y + h - 26
    cv.rect(x + 6, wy - 22, w - 12, 20, c)          # flight deck
    cv.rect(x + 14, wy - 2, w - 28, 14, c)          # hull
    cv.rect(x + w - 44, wy - 44, 22, 22, c)         # island
    cv.rect(x + w - 40, wy - 52, 6, 8, c)
    cv.line(x + 4, wy + 8, x + w - 4, wy + 8, BLUE, 3)
    # jet
    jx, jy = x + w // 3, y + 16
    cv.triangle(jx, jy, jx + 34, jy + 7, jx, jy + 14, c)
    cv.line(jx + 2, jy + 7, jx - 12, jy + 7, c, 3)
    cv.line(jx - 12, jy + 7, jx - 22, jy + 7, RED, 2)


def pic_summit(cv, x, y, w, h, c):
    """Three flags behind a table: three-way meeting."""
    base = y + h - 26
    cols = [RED, BLUE, INK]
    for i, col in enumerate(cols):
        fx = x + 16 + i * (w - 32) // 3
        cv.vline(fx, y + 8, base - y - 34, c, 3)
        cv.rect(fx + 3, y + 8, 34, 22, col)
        cv.rect(fx + 3, y + 8, 34, 7, PAPER)
    cv.rect(x + 8, base - 14, w - 16, 12, c)        # table
    cv.rect(x + 20, base - 2, 8, 22, c)
    cv.rect(x + w - 28, base - 2, 8, 22, c)


def pic_audit(cv, x, y, w, h, c):
    """A magnifier over a dollar sign, crossed out."""
    cx, cy, r = x + w // 2 - 6, y + h // 2 - 6, 34
    cv.circle(cx, cy, r, c)
    cv.circle(cx, cy, r - 6, c)
    cv.text(cx - 12, cy - 21, '$', 6, c)
    cv.line(cx + 24, cy + 24, cx + 44, cy + 44, c, 5)
    cv.line(x + 6, y + 6, x + w - 6, y + h - 6, RED, 5)
    cv.line(x + w - 6, y + 6, x + 6, y + h - 6, RED, 5)


def pic_sanction(cv, x, y, w, h, c):
    """Scales of justice, one pan tipped."""
    base = y + h - 20
    cv.vline(x + w // 2, y + 10, base - y - 10, c, 4)
    cv.hline(x + w // 2 - 40, y + 16, 80, c, 4)
    cv.line(x + w // 2 - 40, y + 20, x + w // 2 - 56, y + 52, c, 3)
    cv.line(x + w // 2 - 40, y + 20, x + w // 2 - 24, y + 52, c, 3)
    cv.rect(x + w // 2 - 62, y + 50, 44, 8, c)
    cv.line(x + w // 2 + 40, y + 20, x + w // 2 + 24, y + 44, c, 3)
    cv.line(x + w // 2 + 40, y + 20, x + w // 2 + 56, y + 44, c, 3)
    cv.rect(x + w // 2 + 18, y + 42, 44, 8, c)
    cv.rect(x + w // 2 - 44, base - 4, 88, 6, c)


def pic_jet(cv, x, y, w, h, c):
    """A fighter jet climbing, with motion lines."""
    jx, jy = x + 12, y + h // 2 - 8
    cv.triangle(jx, jy + 8, jx + 66, jy + 16, jx, jy + 24, c)
    cv.triangle(jx + 20, jy + 16, jx + 44, jy - 6, jx + 52, jy + 16, c)
    cv.triangle(jx + 20, jy + 16, jx + 44, jy + 38, jx + 52, jy + 16, c)
    cv.line(jx + 66, jy + 16, jx + 78, jy + 16, c, 4)
    for i, yy in enumerate((y + 20, y + 40, y + 60, y + 80)):
        cv.hline(x + w - 46 - i * 4, yy, 34, BLUE, 3)


def pic_globe(cv, x, y, w, h, c):
    """Simple globe: circle, meridians, land blobs."""
    cx, cy, r = x + w // 2, y + h // 2, min(w, h) // 2 - 6
    cv.circle(cx, cy, r, c)
    cv.circle(cx, cy, r, BLUE)
    cv.vline(cx, cy - r, 2 * r, BLUE, 2)
    cv.hline(cx - r, cy, 2 * r, BLUE, 2)
    cv.circle(cx - r // 3, cy - r // 4, r // 4, c, fill=True)
    cv.circle(cx + r // 3, cy + r // 4, r // 5, c, fill=True)
    cv.circle(cx + r // 5, cy - r // 2, r // 6, c, fill=True)

# ---------------------------------------------------------------- layout
def story(cv, x, y, w, kicker, head1, head2, deck, pic):
    cv.text(x, y, kicker, 2, RED)
    cv.text(x, y + 22, head1, 3, INK)
    cv.text(x, y + 46, head2, 3, INK)
    lines = cv.wrap(deck, 2, w - 118)
    yy = y + 74
    for ln in lines[:4]:
        cv.text(x, yy, ln, 2, INK)
        yy += 18
    pic(cv, x + w - 106, y + 18, 104, 104, INK)


def draw():
    cv = Canvas(W, H, PAPER)
    # frame
    cv.rect(8, 8, W - 16, 4, INK)
    cv.rect(8, H - 12, W - 16, 4, INK)
    cv.rect(8, 8, 4, H - 16, INK)
    cv.rect(W - 12, 8, 4, H - 16, INK)

    # masthead
    cv.text_center(30, 'THE WORLD TODAY', 8, INK)
    cv.hline(24, 108, W - 48, INK, 3)
    cv.text_center(122, 'TUESDAY, 17 NOVEMBER 2026', 3, RED)
    cv.hline(24, 152, W - 48, INK, 2)

    # ---- lead story: Ukraine / Kerch Bridge
    cv.text(28, 168, 'LEAD STORY - UKRAINE', 2, RED)
    cv.text(28, 192, 'KERCH BRIDGE HIT', 5, INK)
    cv.text(28, 232, 'SECOND DAY RUNNING', 5, INK)
    lead = ("Road span collapses as Russia hits Kyiv's bridges over the "
            "Dnipro - heating, water and power cut across the capital.")
    yy = 282
    for ln in cv.wrap(lead, 2, 640):
        cv.text(28, yy, ln, 2, INK)
        yy += 20
    pic_bridge(cv, 700, 172, 292, 190, INK)
    cv.hline(24, 392, W - 48, INK, 3)

    # ---- story grid: 2 columns x 3 rows
    col_w = 464
    rows = [
        (428, [
            ('IRAN - GULF', 'MINES HIT TANKERS', 'NEAR HORMUZ',
             'Drones hit a US radar base in Bahrain - intercepted. '
             'US intel warns of a dirty-bomb plot on Trump officials.', pic_tanker),
            ('US NAVY', 'THIRD US CARRIER', 'SAILS FOR GULF',
             'USS Theodore Roosevelt joins two carriers in the Middle East '
             'as tensions rise.', pic_carrier),
        ]),
        (584, [
            ('SUMMIT - SHENZHEN', 'XI, TRUMP, PUTIN', 'TO MEET THURSDAY',
             'First three-way talks confirmed for 19 Nov in Shenzhen, on '
             'the APEC sidelines.', pic_summit),
            ('WASHINGTON', 'PENTAGON FAILS', '9TH AUDIT IN A ROW',
             '$4.8 trillion in assets unverified - ninth straight year '
             'without a clean audit.', pic_audit),
        ]),
        (740, [
            ('WEST BANK', 'UK SANCTIONS 8', 'SETTLEMENT FIRMS',
             'Settlers kill a 72-year-old woman in Jericho. Netanyahu camp '
             'accused of election-day meddling.', pic_sanction),
            ('JAPAN', 'JETS SCRAMBLED', 'OVER AIRSPACE ROW',
             'Japan sends fighters after suspected Russian planes enter its '
             'skies.', pic_jet),
        ]),
    ]
    for y, pair in rows:
        story(cv, 28, y, col_w, *pair[0])
        story(cv, 532, y, col_w, *pair[1])
        cv.vline(508, y, 148, GREY, 2)
        if y != 740:
            cv.hline(24, y + 152, W - 48, GREY, 2)

    # ---- also today strip
    cv.hline(24, 896, W - 48, INK, 3)
    cv.text(28, 910, 'ALSO TODAY', 2, RED)
    briefs = [
        'XI AND CARNEY AGREE TARIFF CUTS',
        'TRUMP VISITS THE PHILIPPINES',
        'JPMORGAN GLITCH HITS BANKING, ZELLE',
        'US MEASLES CASES HIGHEST SINCE 1991',
    ]
    bx = 28
    for b in briefs:
        lines = cv.wrap(b, 2, 228)
        yy = 934
        for ln in lines:
            cv.text(bx, yy, ln, 2, INK)
            yy += 18
        bx += 242

    # footer
    cv.hline(24, 978, W - 48, GREY, 2)
    cv.text_center(990, "THE WORLD TODAY - ONE DAY'S NEWS ON ONE PAGE", 2,
                   GREY)
    return cv


def main():
    out_dir = os.environ.get('MAKEFUN_OUTPUT_DIR', '/output')
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, 'entry.png')
    n = write_png(draw(), path)
    print(f'wrote {path} ({n} bytes)')


if __name__ == '__main__':
    main()
