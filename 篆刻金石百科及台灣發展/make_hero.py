"""做 hero 圖：米色底 + 右側純朱文印（裁切掉手寫字）"""
from PIL import Image, ImageDraw

DST = r"D:\_WWW_325\篆刻金石百科及台灣發展\assets\images\home-hero.webp"
W, H = 1280, 720
bg = Image.new("RGB", (W, H), (247, 245, 240))

# 開 yunlin-41（扶光）
seal = Image.open(r"D:\_WWW_325\篆刻金石百科及台灣發展\assets\images\yunlin-41.webp").convert("RGB")
sw, sh = seal.size
# 右側鈐拓：大約 x: 55%-95%, y: 5%-55%（只留紅色印，去掉下方手寫字）
seal_crop = seal.crop((int(sw*0.58), int(sh*0.05), int(sw*0.95), int(sh*0.55)))
# 縮放到高度 500
ratio = 500 / seal_crop.height
seal_new = seal_crop.resize((int(seal_crop.width*ratio), 500), Image.LANCZOS)

# 貼右側
sx = W - seal_new.width - 100
sy = (H - seal_new.height) // 2
bg.paste(seal_new, (sx, sy))

# 左側淡金圓暈
draw = ImageDraw.Draw(bg)
draw.ellipse([80, H//2-120, 320, H//2+120], fill=(232, 210, 170))

bg.save(DST, "WEBP", quality=88, method=6)
print(f"✓ home-hero.webp ({W}x{H})")
