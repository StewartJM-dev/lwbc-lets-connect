#!/usr/bin/env python3
"""
Generates labeled placeholder graphics for every image slot on the site,
at the exact filename and pixel size the Question Mark site uses. Replace
each file in images/ with Gordon's real artwork at the same size and the
site needs no other changes.

Run once: python3 scripts/make_placeholders.py
(Safe to delete this script after the real graphics are in.)
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(__file__), "..", "images")
BG = (12, 12, 11)
GOLD = (212, 165, 58)
BLUE = (61, 139, 255)
CHROME = (215, 218, 224)
INK = (245, 244, 239)
FAINT = (120, 117, 106)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def centered(draw, xy, text, f, fill):
    x, y = xy
    l, t, r, b = draw.textbbox((0, 0), text, font=f)
    draw.text((x - (r - l) / 2 - l, y - (b - t) / 2 - t), text, font=f, fill=fill)


def tile(name, size, label, fmt):
    w = h = size
    im = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(im)
    m = int(w * 0.04)
    d.ellipse([m, m, w - m, h - m], outline=GOLD, width=max(2, w // 120))
    d.ellipse([m * 3, m * 3, w - m * 3, h - m * 3], outline=BLUE, width=max(1, w // 300))
    centered(d, (w / 2, h * 0.40), label, font(BOLD, int(w * 0.11)), INK)
    centered(d, (w / 2, h * 0.58), f"{name}", font(MONO, int(w * 0.055)), CHROME)
    centered(d, (w / 2, h * 0.66), f"{w}x{h}", font(MONO, int(w * 0.045)), FAINT)
    im.save(os.path.join(OUT, name), **fmt)


def wide(name, w, h, title, sub, boxes=()):
    im = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], outline=GOLD, width=3)
    if boxes:
        # footer: keep labels out of the guide boxes
        centered(d, (w / 2, h * 0.10), sub, font(MONO, int(h * 0.04)), CHROME)
    else:
        centered(d, (w / 2, h * 0.34), title, font(BOLD, int(h * 0.095)), INK)
        centered(d, (w / 2, h * 0.52), sub, font(MONO, int(h * 0.045)), CHROME)
        centered(d, (w / 2, h * 0.62), f"{name}  {w}x{h}", font(MONO, int(h * 0.04)), FAINT)
    # Optional guide boxes (used for the footer so the clickable hotspot
    # regions in css/style.css line up with the real design).
    for (top, left, bw, bh, text) in boxes:
        x0, y0 = w * left, h * top
        x1, y1 = x0 + w * bw, y0 + h * bh
        d.rectangle([x0, y0, x1, y1], outline=BLUE, width=2)
        centered(d, ((x0 + x1) / 2, (y0 + y1) / 2), text, font(MONO, int(h * 0.035)), BLUE)
    im.save(os.path.join(OUT, name), quality=88)


JPG = {"quality": 88}
PNG = {}

# --- Circular tiles (homepage nav) ---
tile("tile-about.jpg", 420, "ABOUT", JPG)
tile("tile-latest.jpg", 420, "LATEST", JPG)
tile("tile-episodes.jpg", 420, "EPISODES", JPG)
tile("tile-question.jpg", 420, "ASK", JPG)
tile("tile-subscribe.jpg", 1254, "SUBSCRIBE", JPG)
tile("tile-download-app.png", 1254, "APP", PNG)

# --- Logos ---
tile("lets-connect-logo.jpg", 1254, "LOGO", JPG)
tile("lwbc-media-ministry-logo.jpg", 1254, "LWBC MEDIA", JPG)

# --- App icons / favicon (square, from the logo) ---
tile("icon-512.png", 512, "ICON", PNG)
tile("icon-192.png", 192, "ICON", PNG)
tile("apple-touch-icon.png", 180, "ICON", PNG)
tile("favicon-64.png", 64, "LC", PNG)

# --- Banner (top of every page) ---
wide("banner.jpg", 1942, 809,
     "LWBC LET'S CONNECT PODCAST",
     "with Pastor Raymond Purdy  |  Faith . Truth . Real Talk . Real Life")

# --- Footer: hotspot regions match .fh-* rules in css/style.css ---
wide("footer.jpg", 2048, 768,
     "", "footer.jpg 2048x768 - blue boxes = clickable regions (css/style.css .fh-*)",
     boxes=[
         (0.22, 0.010, 0.155, 0.46, "LWBC logo"),
         (0.37, 0.185, 0.14, 0.17, "LWBC Media Ministry"),
         (0.55, 0.185, 0.14, 0.15, "Built by CCD"),
         (0.28, 0.345, 0.062, 0.34, "Home"),
         (0.28, 0.410, 0.062, 0.34, "About"),
         (0.28, 0.475, 0.062, 0.34, "Episodes"),
         (0.28, 0.540, 0.075, 0.34, "Ask"),
         (0.28, 0.617, 0.065, 0.34, "Subscribe"),
         (0.30, 0.700, 0.15, 0.32, "40 Hess Ln, Sweet Valley PA"),
     ])

# --- Optional host photo on the About page (hidden if missing) ---
tile("raymond-purdy.jpg", 600, "HOST PHOTO", JPG)

print("Placeholders written to", os.path.abspath(OUT))
