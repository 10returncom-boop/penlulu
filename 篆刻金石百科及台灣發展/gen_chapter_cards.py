# -*- coding: utf-8 -*-
"""10 張滿版無字章節卡片圖——每張不同視覺，統一米/硃砂/金色調"""
import os, math, random
from PIL import Image, ImageDraw

IMG = r"D:\_WWW_325\篆刻金石百科及台灣發展\assets\images"
W, H = 1280, 720
random.seed(42)

# 色票
BG = (247, 245, 240)       # 米色
RED = (155, 44, 44)        # 硃砂
GOLD = (210, 180, 130)     # 淡金
DARK = (60, 40, 30)        # 深棕
LIGHT_RED = (200, 100, 90) # 淺硃砂

def base():
    return Image.new("RGB", (W, H), BG)

# 1. 金石學入門：青銅器紋理滿版
def c_jinxue():
    img = base(); d = ImageDraw.Draw(img)
    # 滿版：多個同心圓+雲雷紋
    cx, cy = W//2, H//2
    for r in range(350, 30, -20):
        d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=RED, width=2)
    # 隨機雲雷紋
    for _ in range(40):
        x = random.randint(50, W-50); y = random.randint(50, H-50)
        d.rectangle([x, y, x+25, y+25], outline=GOLD, width=2)
    return img

# 2. 篆刻演變史：卷軸+時間軸
def c_history():
    img = base(); d = ImageDraw.Draw(img)
    # 橫軸時間線
    d.line([(80, H//2), (W-80, H//2)], fill=RED, width=4)
    # 節點
    for x in [160, 380, 600, 820, 1040, 1200]:
        d.ellipse([x-18, H//2-18, x+18, H//2+18], fill=RED)
        d.ellipse([x-8, H//2-8, x+8, H//2+8], fill=BG)
    # 上下波紋
    for i in range(8):
        y = 80 + i*80
        d.arc([100, y, 400, y+60], 0, 180, fill=GOLD, width=2)
        d.arc([500, y, 800, y+60], 0, 180, fill=GOLD, width=2)
        d.arc([900, y, 1200, y+60], 0, 180, fill=GOLD, width=2)
    return img

# 3. 印石材料：多個石頭
def c_materials():
    img = base(); d = ImageDraw.Draw(img)
    stones = [(200,200,80), (500,300,100), (800,180,70), (1050,320,90),
              (350,500,90), (700,520,75), (1000,550,85)]
    for x,y,r in stones:
        d.ellipse([x-r, y-r, x+r, y+r], fill=(220,200,170), outline=RED, width=3)
        # 石頭紋理
        for _ in range(5):
            a = random.uniform(0, 2*math.pi)
            px = x + math.cos(a)*r*0.5
            py = y + math.sin(a)*r*0.5
            d.ellipse([px-5, py-3, px+5, py+3], fill=GOLD)
    return img

# 4. 篆刻技法：刻刀+刀痕
def c_techniques():
    img = base(); d = ImageDraw.Draw(img)
    # 斜放刻刀
    d.line([(200, 550), (900, 150)], fill=DARK, width=12)
    d.polygon([(900,150),(860,170),(880,120)], fill=RED)
    # 刀痕（平行斜線）
    for i in range(15):
        x = 150 + i*70
        d.line([(x, 100), (x+100, 620)], fill=GOLD, width=2)
    return img

# 5. 印章形制：多個印章堆疊
def c_forms():
    img = base(); d = ImageDraw.Draw(img)
    seals = [(200,200,90), (450,250,70), (700,180,100), (950,280,80),
             (300,450,80), (600,480,90), (900,500,75)]
    for x,y,s in seals:
        d.rectangle([x-s, y-s, x+s, y+s], outline=RED, width=4)
        d.line([(x-s, y), (x+s, y)], fill=RED, width=2)
        d.line([(x, y-s), (x, y+s)], fill=RED, width=2)
    return img

# 6. 工具印泥：印泥盒+印譜
def c_tools():
    img = base(); d = ImageDraw.Draw(img)
    # 大印泥盒
    d.ellipse([400, 200, 880, 600], fill=RED)
    d.ellipse([450, 250, 830, 550], outline=BG, width=4)
    # 小印譜線條
    for i in range(5):
        y = 150 + i*100
        d.line([(100, y), (300, y)], fill=GOLD, width=3)
        d.line([(980, y), (1180, y)], fill=GOLD, width=3)
    return img

# 7. 台灣篆刻發展史：台灣島輪廓
def c_taiwan_hist():
    img = base(); d = ImageDraw.Draw(img)
    # 台灣島形
    island = [(560,120),(680,150),(720,250),(700,380),(650,500),(580,580),
              (520,560),(500,450),(510,300),(530,180)]
    d.polygon(island, outline=RED, width=4)
    # 島內紋理
    for _ in range(15):
        x = random.randint(520, 680); y = random.randint(150, 550)
        d.ellipse([x-6, y-6, x+6, y+6], fill=GOLD)
    return img

# 8. 台灣印社與社團：多人聚會
def c_clubs():
    img = base(); d = ImageDraw.Draw(img)
    # 圍圈的人
    cx, cy = W//2, H//2
    for i in range(8):
        a = i * math.pi/4
        x = cx + math.cos(a)*220
        y = cy + math.sin(a)*180
        d.ellipse([x-30, y-40, x+30, y+40], outline=RED, width=3)
        d.ellipse([x-15, y-55, x+15, y-25], outline=RED, width=3)
    return img

# 9. 台灣篆刻名家：人物側影
def c_masters():
    img = base(); d = ImageDraw.Draw(img)
    # 側臉輪廓
    d.ellipse([500, 150, 780, 430], outline=RED, width=4)  # 頭
    d.arc([450, 400, 830, 700], 180, 360, fill=RED, width=4)  # 肩
    # 書卷
    d.rectangle([300, 500, 980, 560], outline=GOLD, width=3)
    return img

# 10. 台灣金石文化現場：展覽場景
def c_culture():
    img = base(); d = ImageDraw.Draw(img)
    # 展櫃
    d.rectangle([200, 150, 1080, 550], outline=RED, width=4)
    d.line([(200, 350), (1080, 350)], fill=GOLD, width=2)
    # 展櫃內印章
    for x in [300, 450, 600, 750, 900]:
        d.rectangle([x-25, 250, x+25, 320], outline=RED, width=3)
        d.rectangle([x-20, 400, x+20, 470], outline=RED, width=3)
    return img

FUNCS = [
    ("jinxue", c_jinxue),
    ("history", c_history),
    ("materials", c_materials),
    ("techniques", c_techniques),
    ("seal-types", c_forms),
    ("tools", c_tools),
    ("taiwan-history", c_taiwan_hist),
    ("taiwan-societies", c_clubs),
    ("taiwan-masters", c_masters),
    ("taiwan-culture", c_culture),
]

for slug, fn in FUNCS:
    img = fn()
    out = os.path.join(IMG, f"{slug}.webp")
    img.save(out, "WEBP", quality=88, method=6)
    print(f"  ✓ {slug}.webp")
print("完成 10 張滿版無字卡片圖")
