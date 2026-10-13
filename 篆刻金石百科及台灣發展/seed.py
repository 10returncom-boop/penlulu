# -*- coding: utf-8 -*-
"""
篆刻金石百科｜台灣發展 — seed.py 內容展開器
================================================
讀 data_master.py（章節）＋ articles_data.py（條目）＋ headings_data.py（每篇專屬小標），
產生：
  data/site.json                       全站規劃（build.py 讀它）
  data/articles/<ch>/<sub>/<slug>.md   逐篇大白話正文

每篇 H2/H3 由 headings_data.py 依 slug 客製，不再套版。
改資料只動 data_master.py / articles_data.py / headings_data.py，再跑：
  python seed.py → python build.py
"""
import os
import json
import importlib.util

ROOT = os.path.dirname(os.path.abspath(__file__))


def load(mod_name, filename):
    spec = importlib.util.spec_from_file_location(mod_name, os.path.join(ROOT, filename))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


dm = load('data_master', 'data_master.py')
ad = load('articles_data', 'articles_data.py')
hd = load('headings_data', 'headings_data.py')

CHAPTERS = dm.CHAPTERS
ARTICLES = ad.ARTICLES
SITE = dm.SITE
HEADINGS = hd.HEADINGS
FAQ_H2 = hd.FAQ_H2


def build_site_json():
    chapters_out = []
    for cid, cz, ce, cd, subs in CHAPTERS:
        chapters_out.append({
            "id": cid, "zh": cz, "en": ce, "desc": cd,
            "subs": [{"id": s[0], "zh": s[1], "en": s[2], "desc": s[3]} for s in subs],
        })
    arts = []
    for (ch, sub, slug, zh, en, origin, traits, masters, tags, diff, summary) in ARTICLES:
        arts.append({
            "slug": slug, "chapter": ch, "sub": sub,
            "title": zh, "en": en, "summary": summary,
            "tags": tags, "difficulty": diff,
        })
    return {"site": SITE, "chapters": chapters_out, "articles": arts}


# 各章節的 bullet 敘事：依主題給真正不同的角度，避免套版
CHAPTER_ANGLE = {
    "jinxue": [
        "先搞懂「它在金石學脈絡裡的位置」：是青銅器、碑刻、還是著錄本身。",
        "再看「一張原物照片或高清拓片」：比讀十段文字都有效。",
        "最後問自己「這跟篆刻有什麼關係」：把它接回你自己的刀下。",
    ],
    "history": [
        "時代脈絡：它出現在什麼政治、文化背景下。",
        "代表實物：找一方（或一件）代表作對照看。",
        "後世影響：它怎麼被後人繼承、反叛、再發揚。",
    ],
    "materials": [
        "質地：握在手上是細、是脆、還是溫。",
        "色澤與紋理：在燈光下看它的「門面」。",
        "行情：台灣現在一顆合理價位帶落在哪。",
    ],
    "techniques": [
        "手勢：手腕、指力、身體重心怎麼放。",
        "常見錯誤：新手最容易在哪一步翻車。",
        "練習步驟：從哪個基本動作開始，一次練多久。",
    ],
    "seal-types": [
        "場合：什麼文件、什麼作品、什麼場合會用到。",
        "搭配：字體、尺寸、朱白文如何與之配合。",
        "位置：在書畫落款或文件上蓋在哪個方位。",
    ],
    "tools": [
        "選購：第一次入手的規格與預算。",
        "保養：台灣潮濕氣候下怎麼照顧。",
        "通路：台北、台中、高雄或網路哪裡買得到。",
    ],
    "taiwan-history": [
        "關鍵人物：誰把它帶進台灣、誰讓它留在台灣。",
        "制度土壤：學校、展覽會、社團如何支撐它。",
        "今日現場：現在去看、去學、去買，實際在哪裡。",
    ],
    "taiwan-societies": [
        "組織結構：誰創辦、誰主持、會員怎麼組成。",
        "年度產出：展覽、出版、比賽的固定節奏。",
        "參與方式：一般人怎麼進得去、看得到。",
    ],
    "taiwan-masters": [
        "生平關鍵：他從哪來、在台灣做了哪些事。",
        "印風特色：用三個形容詞說清楚他的面目。",
        "影響足跡：學生、著作、展覽、收藏。",
    ],
    "taiwan-culture": [
        "現場位置：在台灣哪裡親眼可以看到。",
        "入門建議：第一次去看，先認識哪三件。",
        "延伸路徑：看完之後要接著讀什麼、買什麼。",
    ],
}


def md_body(entry):
    (ch, sub, slug, zh, en, origin, traits, masters, tags, diff, summary) = entry
    trait_list = [t.strip() for t in traits.split('|') if t.strip()]
    while len(trait_list) < 3:
        trait_list.append('—')

    sections = HEADINGS.get(slug)
    if not sections:
        # 保險：若 slug 沒寫進 headings_data，退回通用 H2
        sections = [
            ("%s：一句話定位" % zh, []),
            ("它的來龍去脈", []),
            ("在台灣怎麼接觸它", []),
            ("初學者最容易搞混的地方", []),
        ]

    angle = CHAPTER_ANGLE.get(ch, CHAPTER_ANGLE["jinxue"])

    lines = []
    # 開場：一句話摘要（不當 H2，當引言段）
    lines.append('**%s**：%s' % (zh, summary))
    lines.append('')
    lines.append(origin)
    lines.append('')

    for idx, (h2, h3s) in enumerate(sections, 1):
        lines.append('## %s' % h2)
        lines.append('')
        for h3 in h3s:
            lines.append('### %s' % h3)
            lines.append('')
        # 引言：依段序注入不同素材，避免每段都講一樣的話
        if idx == 1:
            lines.append('%s。這段先把「%s」的輪廓講清楚，後面小節再逐層展開。' % (origin, zh))
        elif idx == 2:
            lines.append('具體看，有三個辨識重點值得記住：')
            lines.append('')
            for i, t in enumerate(trait_list[:3], 1):
                lines.append('- %s' % t)
        elif idx == len(sections):
            lines.append('%s' % masters)
            lines.append('')
            lines.append('把這些名字與實物對照著看，會比硬記觀念更有效。')
        else:
            lines.append('%s。這段是「%s」的核心，建議慢一點讀。' % (masters if idx % 2 == 0 else origin, h2))
        lines.append('')
        # 章節角度 bullet：按主題給真正不同的提問
        for b in angle:
            lines.append('- %s' % b)
        lines.append('')
        # 在第 3 個 H2 前插場景圖 marker（build.py 會替換成 <figure>）
        if idx == 2:
            lines.append('<!-- CH_IMG -->')
            lines.append('')

    # FAQ 段
    lines.append('## %s' % FAQ_H2.format(zh=zh))
    lines.append('')
    lines.append('Q：%s適合初學者從哪裡入門？' % zh)
    lines.append('A：先把一句話定位聽懂，再挑一張原物照片或拓片細看，最後才翻工具書。不要一上來就背術語。')
    lines.append('')
    lines.append('Q：%s在台灣要去哪裡看？' % zh)
    lines.append('A：故宮、各縣市立美術館、社團年度展覽與書畫街店家，都是現場。多看實物比多讀文章重要。')
    lines.append('')
    lines.append('Q：%s最容易和什麼搞混？' % zh)
    lines.append('A：從辨識重點第一條開始比對，連用途一起記，才不會張冠李戴。')
    lines.append('')
    lines.append('Q：學%s需要先會寫書法嗎？' % zh)
    lines.append('A：不一定要是書法家，但基本的篆書筆畫觀念要有。邊看邊查，兩三年下來自然就有手感。')
    lines.append('')

    return '\n'.join(lines)


def write_md(entry):
    (ch, sub, slug, zh, en, origin, traits, masters, tags, diff, summary) = entry
    updated = SITE['updated']
    fm = ['---',
          'title: %s' % zh,
          'chapter: %s' % ch,
          'sub: %s' % sub,
          'slug: %s' % slug,
          'summary: %s' % summary,
          'tags: %s' % tags,
          'difficulty: %s' % diff,
          'updated: %s' % updated,
          '---', '']
    body = md_body(entry)
    outdir = os.path.join(ROOT, 'data', 'articles', ch, sub)
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, slug + '.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(fm) + body + '\n')


def main():
    site = build_site_json()
    os.makedirs(os.path.join(ROOT, 'data'), exist_ok=True)
    with open(os.path.join(ROOT, 'data', 'site.json'), 'w', encoding='utf-8') as f:
        json.dump(site, f, ensure_ascii=False, indent=1)
    for e in ARTICLES:
        write_md(e)
    # 檢查每篇都有客製標題
    missing = [e[2] for e in ARTICLES if e[2] not in HEADINGS]
    if missing:
        print('警告：以下 slug 未在 headings_data.py 定義，已退回通用標題：')
        for m in missing:
            print('  -', m)
    print('seed 完成：%d 章、%d 篇 md，site.json 已更新。' % (len(CHAPTERS), len(ARTICLES)))


if __name__ == '__main__':
    main()
