"""把 D:/_WWW_325/昀林篆刻金石/*.jpg 批量轉 webp 到網站 assets/images/yunlin-XX.webp"""
import os
from PIL import Image

SRC = r"D:\_WWW_325\昀林篆刻金石"
DST = r"D:\_WWW_325\篆刻金石百科及台灣發展\assets\images"

files = sorted([f for f in os.listdir(SRC) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
os.makedirs(DST, exist_ok=True)

for i, fn in enumerate(files, 1):
    num = "%02d" % i
    out = os.path.join(DST, f"yunlin-{num}.webp")
    img = Image.open(os.path.join(SRC, fn)).convert("RGB")
    # 限制最長邊 1280，維持比例
    img.thumbnail((1280, 1280), Image.LANCZOS)
    img.save(out, "WEBP", quality=82, method=6)
    print(f"  ✓ yunlin-{num}.webp  ({img.size[0]}x{img.size[1]})  <- {fn}")

print(f"\n共轉 {len(files)} 張")
