# -*- coding: utf-8 -*-
"""下載 AI 生成的卡片圖並轉 webp"""
import os, urllib.request, ssl
from PIL import Image
import io

IMG = r"D:\_WWW_325\篆刻金石百科及台灣發展\assets\images"
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

URLS = {
    "jinxue": "https://aka.doubaocdn.com/s/VHOe8JgUyP",
    "history": "https://aka.doubaocdn.com/s/tJx6lQVMmK",
    "materials": "https://aka.doubaocdn.com/s/MmFMVcR0E4",  # 黑圖，稍後重生成
    "techniques": "https://aka.doubaocdn.com/s/CmIfrvOTA4",
    "seal-types": "https://aka.doubaocdn.com/s/kN9e4zFo8u",
    "tools": "https://aka.doubaocdn.com/s/QdmhVrTKc8",
    "taiwan-history": "https://aka.doubaocdn.com/s/GOtc9WixA8",  # 有字，稍後重生成
    "taiwan-societies": "https://aka.doubaocdn.com/s/CrkTM8LyQB",
    "taiwan-masters": "https://aka.doubaocdn.com/s/kPVYQSmtBf",  # 有人臉，稍後重生成
    "taiwan-culture": "https://aka.doubaocdn.com/s/9fvkef3Kd6",
}

for slug, url in URLS.items():
    out = os.path.join(IMG, f"{slug}.webp")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, context=ctx, timeout=30).read()
        img = Image.open(io.BytesIO(data)).convert("RGB")
        img.save(out, "WEBP", quality=90, method=6)
        print(f"  ✓ {slug}.webp  ({img.size[0]}x{img.size[1]})")
    except Exception as e:
        print(f"  ✗ {slug}.webp  {e}")
