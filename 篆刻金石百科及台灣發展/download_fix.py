# -*- coding: utf-8 -*-
import os, urllib.request, ssl, io
from PIL import Image
IMG = r"D:\_WWW_325\篆刻金石百科及台灣發展\assets\images"
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
URLS = {
    "materials": "https://aka.doubaocdn.com/s/72Qg3MhwBU",
    "taiwan-history": "https://aka.doubaocdn.com/s/HgdpBT6AcE",
    "taiwan-masters": "https://aka.doubaocdn.com/s/EXJEilYnzH",
}
for slug, url in URLS.items():
    out = os.path.join(IMG, f"{slug}.webp")
    req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
    data = urllib.request.urlopen(req, context=ctx, timeout=30).read()
    Image.open(io.BytesIO(data)).convert("RGB").save(out, "WEBP", quality=90, method=6)
    print(f"  ✓ {slug}.webp")
