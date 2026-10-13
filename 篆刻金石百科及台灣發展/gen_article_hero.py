# -*- coding: utf-8 -*-
"""為每篇百科文章生成對應標題的 hero webp（若尚無檔案）"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
from articles_data import ARTICLES

IMG_DIR = r"D:\_WWW_325\篆刻金石百科及台灣發展\assets\images"
W, H = 1280, 720

# 字體
FONT_PATH = r"C:\Windows\Fonts\msjh.ttc"  # 微軟正黑體

def make_hero(slug, title, out_path):
    bg = Image.new("RGB", (W, H), (247, 245, 240))  # 米色 #f7f5f0
    draw = ImageDraw.Draw(bg)
    # 左側淡金圓暈
    draw.ellipse([60, H//2-140, 340, H//2+140], fill=(232, 210, 170))
    # 右側淡硃砂方塊
    draw.rounded_rectangle([W-380, 120, W-80, H-120], radius=24, fill=(155, 44, 44))
    # 右側方塊內畫一個簡單朱文印（方框+十字）
    cx, cy = W-230, H//2
    draw.rectangle([cx-70, cy-90, cx+70, cy+90], outline=(247,245,240), width=4)
    draw.line([cx-70, cy, cx+70, cy], fill=(247,245,240), width=3)
    draw.line([cx, cy-90, cx, cy+90], fill=(247,245,240), width=3)

    # 標題文字（左側，避開圓暈）
    font_big = ImageFont.truetype(FONT_PATH, 44)
    font_small = ImageFont.truetype(FONT_PATH, 18)
    # 標題置中偏左
    title_color = (42, 32, 24)
    # 自動換行
    lines = []
    cur = ""
    for ch in title:
        test = cur + ch
        bbox = draw.textbbox((0,0), test, font=font_big)
        if bbox[2] - bbox[0] > 700:
            lines.append(cur)
            cur = ch
        else:
            cur = test
    if cur:
        lines.append(cur)
    # 垂直置中
    total_h = len(lines) * 60
    y = (H - total_h) // 2
    for line in lines:
        bbox = draw.textbbox((0,0), line, font=font_big)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw)//2 - 100, y), line, fill=title_color, font=font_big)
        y += 60
    # 小標：SEAL CARVING & EPIGRAPHY
    draw.text((80, 60), "SEAL CARVING & EPIGRAPHY · TAIWAN", fill=(155, 44, 44), font=font_small)

    bg.save(out_path, "WEBP", quality=85, method=6)

generated = 0
skipped = 0
for art in ARTICLES:
    slug = art[2]
    title = art[3]
    out = os.path.join(IMG_DIR, f"{slug}.webp")
    # 強制重新生成（統一風格）
    make_hero(slug, title, out)
    print(f"  ✓ {slug}.webp  ({title})")
    generated += 1

print(f"\n完成：重新產生 {generated} 張")
