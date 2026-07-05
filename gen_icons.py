#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère les icônes PWA pour Mes Abos : 192, 512, 512-maskable + feature graphic 1024x500."""
from PIL import Image, ImageDraw, ImageFont
import math

# Palette "fintech friendly" - bleu nuit + vert/teal
BG_TOP = (8, 20, 38)      # bleu nuit profond
BG_BOTTOM = (10, 42, 46)  # vert nuit
ACCENT = (46, 213, 158)   # vert teal vif (money green)
ACCENT_DARK = (20, 120, 110)
WHITE = (240, 250, 248)


def gradient_bg(size, top=BG_TOP, bottom=BG_BOTTOM):
    img = Image.new("RGB", (size, size), top)
    draw = ImageDraw.Draw(img)
    for y in range(size):
        t = y / size
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        draw.line([(0, y), (size, y)], fill=(r, g, b))
    return img


def draw_recurrence_symbol(img, size, center_ratio=0.5, radius_ratio=0.30, stroke_ratio=0.075, gap_deg=55, color=ACCENT):
    """Cercle de récurrence (flèche circulaire) avec un symbole € au centre - motif 'abonnement qui revient'."""
    draw = ImageDraw.Draw(img)
    cx = cy = size * center_ratio
    r = size * radius_ratio
    stroke = max(6, int(size * stroke_ratio))

    bbox = [cx - r, cy - r, cx + r, cy + r]
    start_angle = gap_deg
    end_angle = 360 - 20
    draw.arc(bbox, start=start_angle, end=end_angle, fill=color, width=stroke)

    # flèche au bout de l'arc (pointe la reprise du cycle)
    end_rad = math.radians(end_angle)
    tip_x = cx + r * math.cos(end_rad)
    tip_y = cy + r * math.sin(end_rad)
    tangent = end_rad + math.pi / 2
    arrow_len = stroke * 2.0
    a1x = tip_x - arrow_len * math.cos(tangent - 0.5)
    a1y = tip_y - arrow_len * math.sin(tangent - 0.5)
    a2x = tip_x - arrow_len * math.cos(tangent + 0.5)
    a2y = tip_y - arrow_len * math.sin(tangent + 0.5)
    draw.polygon([(tip_x, tip_y), (a1x, a1y), (a2x, a2y)], fill=color)

    # symbole Euro stylisé au centre
    try:
        font = ImageFont.truetype("segoeuib.ttf", int(size * 0.30))
    except Exception:
        try:
            font = ImageFont.truetype("arialbd.ttf", int(size * 0.30))
        except Exception:
            font = ImageFont.load_default()
    text = "€"
    bbox_txt = draw.textbbox((0, 0), text, font=font)
    tw = bbox_txt[2] - bbox_txt[0]
    th = bbox_txt[3] - bbox_txt[1]
    draw.text((cx - tw / 2 - bbox_txt[0], cy - th / 2 - bbox_txt[1]), text, font=font, fill=WHITE)
    return img


def make_icon(size, maskable=False, out_path=None):
    img = gradient_bg(size)
    if maskable:
        # zone de sécurité maskable = 80% central -> on réduit le rayon du motif
        draw_recurrence_symbol(img, size, radius_ratio=0.24, stroke_ratio=0.06)
    else:
        draw_recurrence_symbol(img, size, radius_ratio=0.30, stroke_ratio=0.075)
    img.save(out_path, "PNG")
    print("Ecrit:", out_path, img.size)


def make_feature_graphic(out_path):
    W, H = 1024, 500
    img = Image.new("RGB", (W, H), BG_TOP)
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        r = int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * t)
        g = int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * t)
        b = int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # motif à gauche
    cx, cy, r = 250, 250, 130
    stroke = 22
    draw.arc([cx - r, cy - r, cx + r, cy + r], start=55, end=340, fill=ACCENT, width=stroke)
    try:
        font_symbol = ImageFont.truetype("segoeuib.ttf", 110)
        font_title = ImageFont.truetype("segoeuib.ttf", 70)
        font_sub = ImageFont.truetype("segoeui.ttf", 26)
    except Exception:
        font_symbol = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    text = "€"
    bbox_txt = draw.textbbox((0, 0), text, font=font_symbol)
    tw = bbox_txt[2] - bbox_txt[0]
    th = bbox_txt[3] - bbox_txt[1]
    draw.text((cx - tw / 2 - bbox_txt[0], cy - th / 2 - bbox_txt[1]), text, font=font_symbol, fill=WHITE)

    draw.text((460, 150), "Mes Abos", font=font_title, fill=WHITE)
    draw.text((462, 245), "Reprends le contrôle de tes", font=font_sub, fill=(200, 230, 225))
    draw.text((462, 280), "abonnements", font=font_sub, fill=(200, 230, 225))
    draw.text((462, 330), "100% gratuit • 100% local • 0 compte", font=font_sub, fill=ACCENT)

    img.save(out_path, "PNG")
    print("Ecrit:", out_path, img.size)


if __name__ == "__main__":
    import os
    out_dir = os.path.join(os.path.dirname(__file__), "icons_out")
    os.makedirs(out_dir, exist_ok=True)
    make_icon(192, maskable=False, out_path=os.path.join(out_dir, "icon-192.png"))
    make_icon(512, maskable=False, out_path=os.path.join(out_dir, "icon-512.png"))
    make_icon(512, maskable=True, out_path=os.path.join(out_dir, "icon-512-maskable.png"))
    make_feature_graphic(os.path.join(out_dir, "feature-graphic-1024x500.png"))
    print("Termine.")
