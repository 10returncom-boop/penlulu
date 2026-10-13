# -*- coding: utf-8 -*-
"""
篆刻金石百科｜台灣發展 — gen_images.py
================================================
用 PIL 產生全部 WebP：
  assets/images/home-hero.webp          首頁主視覺 1280x720
  assets/images/<chapter>.webp          10 張章節主視覺
  assets/images/<slug>.webp             每篇文章主圖
  assets/images/<slug>-trait.webp       每篇辨識卡
風格：米色宣紙底、硃紅印鈕、分章暖色系，無需外部素材。
"""
import os
import hashlib
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
IMGDIR = os.path.join(ROOT, 'assets', 'images')
os.makedirs(IMGDIR, exist_ok=True)

CH_COLOR = {
    'jinxue': (30, 45, 10),
    'history': (15, 25, 10),
    'materials': (350, 25, 8),
    'techniques': (165, 30, 10),
    'seal-types': (230, 25, 12),
    'tools': (40, 20, 10),
    'taiwan-history': (210, 30, 11),
    'taiwan-societies': (140, 30, 12),
    'taiwan-masters': (280, 28, 11),
    'taiwan-culture': (90, 32, 10),
    'home-hero': (0, 45, 14),
}

FONT_CANDIDATES = [
    r'C:\Windows\Fonts\msjhbd.ttc',
    r'C:\Windows\Fonts\msjh.ttc',
    r'C:\Windows\Fonts\simhei.ttf',
    r'C:\Windows\Fonts\simsun.ttc',
]


def load_font(size):
    for fp in FONT_CANDIDATES:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                continue
    return ImageFont.load_default()


def hsl_to_rgb(h, s, l):
    h = h % 360
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2
    if h < 60:
        r, g, b = c, x, 0
    elif h < 120:
        r, g, b = x, c, 0
    elif h < 180:
        r, g, b = 0, c, x
    elif h < 240:
        r, g, b = 0, x, c
    elif h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    return (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))


def gradient(w, h, c1, c2):
    base = Image.new('RGB', (w, h), c1)
    top = Image.new('RGB', (w, h), c2)
    mask = Image.new('L', (w, h))
    md = mask.load()
    for y in range(h):
        for x in range(w):
            t = (x / w * 0.5 + y / h * 0.5)
            md[x, y] = int(t * 255)
    base.paste(top, (0, 0), mask)
    return base


def paper_texture(img):
    w, h = img.size
    noise = Image.effect_noise((w, h), 12).convert('L').filter(ImageFilter.GaussianBlur(0.4))
    tint = Image.new('RGB', (w, h), (246, 236, 216))
    return Image.blend(img, Image.composite(tint, Image.new('RGB', (w, h), (255, 255, 255)), noise), 0.22)


def seal_stamp(draw, cx, cy, size, color=(155, 44, 44)):
    x0, y0 = cx - size // 2, cy - size // 2
    x1, y1 = cx + size // 2, cy + size // 2
    draw.rounded_rectangle([x0, y0, x1, y1], radius=int(size * 0.12), fill=color)
    pad = int(size * 0.16)
    draw.rounded_rectangle([x0 + pad, y0 + pad, x1 - pad, y1 - pad],
                           radius=int(size * 0.06), outline=(245, 233, 208), width=max(2, size // 40))
    c = size // 4
    draw.rectangle([cx - c, cy - c, cx + c, cy + c], outline=(245, 233, 208), width=max(2, size // 36))


def make_canvas(key, title, w=1280, h=720, trait=False):
    hue, sat, lum = CH_COLOR.get(key, (20, 30, 12))
    hh = int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)
    hue_shift = (hh % 30) - 15
    c1 = hsl_to_rgb(hue + hue_shift, sat * 0.5, 0.88)
    c2 = hsl_to_rgb(hue + hue_shift + 12, sat, 0.74)
    img = gradient(w, h, c1, c2)
    img = paper_texture(img)
    draw = ImageDraw.Draw(img, 'RGBA')
    seal_size = int(min(w, h) * (0.40 if not trait else 0.32))
    seal_stamp(draw, w // 2, h // 2 - 24, seal_size, color=(155, 44, 44))
    font_big = load_font(int(h * 0.10))
    font_sub = load_font(int(h * 0.045))
    draw.text((w // 2 + 3, h - 118 + 3), title, font=font_big, fill=(0, 0, 0, 60), anchor='mm')
    draw.text((w // 2, h - 118), title, font=font_big, fill=(60, 35, 25, 235), anchor='mm')
    draw.text((w // 2, h - 55), '篆刻金石百科｜台灣發展', font=font_sub, fill=(120, 90, 70, 200), anchor='mm')
    if trait:
        r = 16
        for i in range(3):
            cx = w // 2 + (i - 1) * (r * 4)
            cy = h // 2 + seal_size // 2 + 56
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(155, 44, 44, 220))
    return img


def save(img, name):
    img.save(os.path.join(IMGDIR, name), 'WEBP', quality=82, method=6)


def main():
    made = 0
    save(make_canvas('home-hero', '篆刻金石百科｜台灣發展'), 'home-hero.webp'); made += 1
    ch_titles = {
        'jinxue': '金石學入門', 'history': '篆刻演變史', 'materials': '印石材料',
        'techniques': '篆刻技法', 'seal-types': '印章形制', 'tools': '工具與印泥',
        'taiwan-history': '台灣篆刻發展史', 'taiwan-societies': '台灣印社與社團',
        'taiwan-masters': '台灣篆刻名家', 'taiwan-culture': '台灣金石文化現場',
    }
    for c, t in ch_titles.items():
        save(make_canvas(c, t), c + '.webp'); made += 1
    import importlib.util
    spec = importlib.util.spec_from_file_location('ad', os.path.join(ROOT, 'articles_data.py'))
    ad = importlib.util.module_from_spec(spec); spec.loader.exec_module(ad)
    for (ch, sub, slug, zh, en, *rest) in ad.ARTICLES:
        save(make_canvas(slug, zh), slug + '.webp'); made += 1
        save(make_canvas(slug + 't', zh + ' 辨識卡', trait=True), slug + '-trait.webp'); made += 1
    print('gen_images 完成，共 %d 張 WebP。' % made)


if __name__ == '__main__':
    main()
