# -*- coding: utf-8 -*-
"""
篆刻金石百科｜台灣發展 — check.py 自動檢查腳本（批次掃描）
================================================
三項檢核：
  1. SEO 元素掃描：每頁 title / meta description / OG / JSON-LD 是否齊全
  2. 連結與圖片路徑：所有 <a href> 與 <img src> 是否被抽出
  3. 斷鏈偵測：比對本機檔案是否存在，列出 404 內部斷鏈與遺失圖片

用法：
  python check.py            完整掃描，回報缺失
  python check.py --summary  只印統計摘要
"""
import os
import re
import sys
import json
import urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
try:
    site = json.load(open(os.path.join(ROOT, 'data', 'site.json'), encoding='utf-8'))
    SITE_NAME = site['site']['name']
except Exception:
    SITE_NAME = '篆刻金石百科｜台灣發展'

HTML_RE = re.compile(r'\.html?$')
LINK_RE = re.compile(r'href="([^"]+)"')
IMG_RE = re.compile(r'<img[^>]+src="([^"]+)"')
TITLE_RE = re.compile(r'<title>(.*?)</title>', re.S)
META_DESC_RE = re.compile(r'<meta name="description" content="([^"]*)"')
OG_TITLE_RE = re.compile(r'<meta property="og:title"')
OG_IMG_RE = re.compile(r'<meta property="og:image"')
JSONLD_RE = re.compile(r'<script type="application/ld\+json">')


def collect_html():
    files = []
    for dp, _d, fns in os.walk(ROOT):
        for fn in fns:
            if HTML_RE.search(fn):
                files.append(os.path.join(dp, fn))
    return files


def rel_to_abs(base_html, url):
    """把 HTML 頁面裡的相對 href/src 轉成本機絕對路徑。"""
    if not url:
        return None
    # 跳過外部、錨點、mailto、data:、javascript
    if re.match(r'^(https?:|mailto:|data:|javascript:|#)', url):
        return 'EXTERNAL'
    url = url.split('#')[0].split('?')[0]
    if not url:
        return 'ANCHOR'
    url = urllib.parse.unquote(url)
    base_dir = os.path.dirname(base_html)
    target = os.path.normpath(os.path.join(base_dir, url))
    return target


def exists(path):
    if path in ('EXTERNAL', 'ANCHOR', None) or path is None:
        return True
    return os.path.exists(path)


def main():
    summary_only = '--summary' in sys.argv
    files = collect_html()
    seo_problems = []
    broken_links = []
    missing_imgs = []
    n_jsonld_pages = 0

    for fp in files:
        with open(fp, encoding='utf-8') as f:
            html = f.read()
        rel = os.path.relpath(fp, ROOT)
        # 1. SEO 元素
        if not TITLE_RE.search(html):
            seo_problems.append('%s：缺 <title>' % rel)
        if not META_DESC_RE.search(html):
            seo_problems.append('%s：缺 meta description' % rel)
        if not OG_TITLE_RE.search(html):
            seo_problems.append('%s：缺 og:title' % rel)
        if not OG_IMG_RE.search(html):
            seo_problems.append('%s：缺 og:image' % rel)
        if JSONLD_RE.search(html):
            n_jsonld_pages += 1
        else:
            seo_problems.append('%s：缺 JSON-LD' % rel)
        # 2 & 3. 連結與圖片路徑
        for m in LINK_RE.finditer(html):
            tgt = rel_to_abs(fp, m.group(1))
            if tgt == 'EXTERNAL' or tgt == 'ANCHOR':
                continue
            if not exists(tgt):
                broken_links.append('%s → %s' % (rel, m.group(1)))
        for m in IMG_RE.finditer(html):
            tgt = rel_to_abs(fp, m.group(1))
            if tgt and not exists(tgt):
                missing_imgs.append('%s → %s' % (rel, m.group(1)))

    print('=' * 56)
    print('%s — 批次檢查報告' % SITE_NAME)
    print('=' * 56)
    print('掃描 HTML 頁數：%d' % len(files))
    print('含 JSON-LD 頁數：%d' % n_jsonld_pages)
    print('SEO 缺失：%d 項' % len(seo_problems))
    print('斷鏈（404）：%d 條' % len(broken_links))
    print('遺失圖片：%d 條' % len(missing_imgs))

    if not summary_only:
        if seo_problems:
            print('\n--- 1. SEO 元素缺失（前 30 條）---')
            for p in seo_problems[:30]:
                print('  ✗ ' + p)
        if broken_links:
            print('\n--- 2. 內部斷鏈（前 30 條）---')
            for b in broken_links[:30]:
                print('  ✗ ' + b)
        if missing_imgs:
            print('\n--- 3. 遺失圖片（前 30 條）---')
            for m in missing_imgs[:30]:
                print('  ✗ ' + m)

    if seo_problems or broken_links or missing_imgs:
        print('\n結果：發現問題，請看上方清單。')
        sys.exit(1)
    else:
        print('\n結果：全部通過，無 SEO 缺失、無斷鏈、無遺失圖片。')


if __name__ == '__main__':
    main()
