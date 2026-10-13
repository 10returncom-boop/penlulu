# -*- coding: utf-8 -*-
"""
篆刻金石百科｜台灣發展 — 主資料檔（唯一內容來源）
================================================
每一筆都是一顆印石、一派刀法、一位名家、一段台灣篆刻史或一種形制，
可分析、可搜尋、可比對。改這裡就好，不用動 build.py 模板；
seed.py 會把它展開成 site.json 與逐篇 md。

文章欄位（articles_data.py tuple）：
(ch, sub, slug, zh, en, origin, traits, masters, tags, difficulty, summary)
- ch/sub    : 對照下方 CHAPTERS / subs
- origin    : 年代／產地／流派／台灣在地定位（大白話一句）
- traits    : 3 條辨識重點（以 | 隔開），自動產生辨識表格
- masters   : 代表人物／經典作品／產地／台灣在地案例（一兩句）
- tags      : 4~6 個短標籤（逗號隔開），驅動 Tag System 與相關推薦
- difficulty: 入門 / 中階 / 進階
- summary   : 一句話摘要（用於 meta description 與卡片）

站名：篆刻金石百科｜台灣發展
定位：權威、專業、大白話、資訊齊全、差異化；台灣在地觀點貫穿全站。
"""

SITE = {
    "name": "篆刻金石百科｜台灣發展",
    "name_en": "Seal Carving & Epigraphy Encyclopedia · Taiwan",
    "desc": "從金石學、篆刻史、印石材料到台灣印社與名家，用大白話帶你一次看懂篆刻金石，並以台灣在地觀點看這門千年手藝怎麼活到今天。",
    "rootUrl": "https://seal-epigraphy.example.com/",
    "version": "v1.0.0",
    "updated": "2026-10-10",
}

# ch_id -> (zh, en, desc, subs[(sub_id, zh, en, desc)])
CHAPTERS = [
    ("jinxue", "金石學入門", "Epigraphy Basics",
     "金石學是什麼？從青銅器、石刻到拓片著錄，先搞懂這門學問再談篆刻。", [
        ("intro", "認識金石學", "What Is Epigraphy", "金石二字的由來：青銅器與石刻，怎麼從收藏變成一門學問。"),
        ("history", "金石學的演變", "History of Epigraphy", "宋代呂大臨、清代乾嘉學派，金石學怎麼一步步成熟。"),
        ("relation", "金石與篆刻的關係", "Epigraphy & Seal Carving", "印章本身就是金石的縮影：文字、材質、刀法全都相通。"),
        ("rubbing", "拓片與著錄", "Rubbings & Catalogues", "打拓、題跋、印譜：古人怎麼把金石資料保留下來。"),
     ]),
    ("history", "篆刻演變史", "History of Seal Carving",
     "從先秦古璽到明清流派，一條線看懂印章兩千年怎麼演變。", [
        ("pre-qin", "先秦古璽", "Pre-Qin Seals", "戰國璽印到底在印什麼？東周諸侯的官璽與私璽。"),
        ("han-qin", "秦漢印", "Qin & Han Seals", "漢印為什麼被奉為典範？繆篆與官印制度。"),
        ("tang-ming", "唐宋金元", "Tang–Song–Jin–Yuan", "尺寸變大、九疊文流行，元代花押與文人印萌芽。"),
        ("ming-qing", "明清流派", "Ming–Qing Schools", "文彭、何震到西泠八家，篆刻從實用變成文人藝術。"),
        ("modern", "近現代與當代", "Modern & Contemporary", "吳昌碩、齊白石之後，篆刻怎麼走進當代與台灣。"),
     ]),
    ("materials", "印石材料百科", "Seal Stone Materials",
     "四大名石、凍石、奇石——每顆石頭的脾氣與價位，台灣買得到哪些。", [
        ("four-famous", "四大名石總覽", "Four Famous Stones", "壽山、青田、昌化、巴林，先搞懂四大門派再談選石。"),
        ("shoushan", "壽山石系", "Shoushan Stones", "田黃、荔枝凍、芙蓉、都成坑，福州壽山的百寶箱。"),
        ("qingtian", "青田石系", "Qingtian Stones", "封門青、藍星、龍蛋、燈光凍，溫潤易刻的練刀首選。"),
        ("changhua", "昌化石系", "Changhua Stones", "雞血石為什麼紅得像血？昌化硃砂與凍地。"),
        ("balin", "巴林石系", "Balin Stones", "內蒙古巴林凍與雞血，後起之秀的色彩戰士。"),
        ("other", "其他石種", "Other Stones", "廣元石、遼寧凍、雲南石、浙江紅，台灣文房常見的平價選擇。"),
        ("market", "選石與行情", "Buying & Market", "在台灣怎麼挑第一顆印石、怎麼看行情與真假。"),
     ]),
    ("techniques", "篆刻技法", "Carving Techniques",
     "怎麼下刀、寫什麼字、怎麼佈局、最後怎麼鈐出來，一招一招拆給你看。", [
        ("knife", "刀法基本功", "Knife Techniques", "沖刀、切刀、單刀、雙刀、殘邊——手怎麼動。"),
        ("script", "篆法字體", "Seal Script Systems", "小篆、大篆、繆篆、摹印篆、璽印文字選哪一種。"),
        ("layout", "章法布局", "Composition", "疏密、屈伸、挪讓，一方印的分間佈局。"),
        ("stamping", "鈐印與印泥", "Stamping & Ink Paste", "印泥怎麼選、怎麼鈐才清晰不糊、怎麼蓋在作品上。"),
     ]),
    ("seal-types", "印章形制與用途", "Seal Types & Uses",
     "名號印、閒章、肖形印、鑑藏印——什麼場合用哪一方。", [
        ("name", "名號印", "Name & Style Seals", "姓名印、字印、號印，落款的第一方印。"),
        ("leisure", "閒章閒文", "Leisure Seals", "引首章、壓角章、格言閒章，畫面的呼吸與個性。"),
        ("picture", "肖形印圖案印", "Pictorial Seals", "人物、動物、佛像、生肖圖案印。"),
        ("collector", "鑑藏藏書印", "Collector & Library Seals", "鑑賞印、收藏印、藏書印，一頁畫上的印譜層層疊。"),
     ]),
    ("tools", "工具印泥與印譜", "Tools, Ink Paste & Albums",
     "刻刀、印床、印泥、印譜——把全套家當備齊，台灣哪裡買得到。", [
        ("carving", "刻刀與輔具", "Carving Tools & Aids", "篆刻刀怎麼選、印床、砂紙、放大鏡與刷帚。"),
        ("inkpaste", "印泥品牌與保養", "Ink Paste Brands & Care", "漳州、杭州、上海各大印泥與日常養護。"),
        ("yinpu", "印譜與臨摹", "Seal Albums & Copying", "歷代印譜怎麼看、怎麼藏，臨摹取法的寶庫。"),
     ]),
    ("taiwan-history", "台灣篆刻發展史", "Seal Carving in Taiwan",
     "從清代書院、日治書道到戰後渡海名家，台灣怎麼長出自己的篆刻風景。", [
        ("qing", "清代與日治前期", "Qing & Early Japanese Era", "書院教育、士紳用印與總督府體制下的書道初萌。"),
        ("japanese", "日治時期的書篆教育", "Japanese-Era Education", "展覽會、書法社團與曹秋圃澹廬書會，篆刻的土壤怎麼成形。"),
        ("postwar", "戰後渡海名家與復興", "Postwar Masters & Revival", "王壯為、王北岳等名家來台，篆刻從此扎根學院與民間。"),
        ("liberalization", "解嚴後的多元發展", "Post-Liberalization Diversity", "本土意識抬頭，篆刻從文人雅玩走向當代創作。"),
        ("contemporary", "當代台灣篆刻現場", "Contemporary Scene", "新一代篆刻家、展覽、跨界合作，台灣篆刻現在長什麼樣。"),
     ]),
    ("taiwan-societies", "台灣印社與社團", "Seal Societies in Taiwan",
     "台灣印社、篆刻學會、縣市印社——把全台灣的篆刻組織一次摸清。", [
        ("taiwan-seal-society", "台灣印社", "Taiwan Seal Society", "台灣最具代表性的篆刻團體，怎麼運作、怎麼入社。"),
        ("associations", "學會與協會", "Associations & Institutes", "中華民國篆刻學會、台灣篆刻家協會等組織的角色。"),
        ("local-groups", "縣市印社與書會", "Local Societies", "各縣市印社、書會與澹廬書會，地方上的篆刻據點。"),
        ("education", "教育推廣與比賽", "Education & Competitions", "學校社團、社區大學、美展篆刻類，新手從哪裡開始。"),
        ("exchange", "兩岸與國際交流", "Cross-Strait & International", "與西泠印社、日本篆刻界的交流，台灣篆刻怎麼走出去。"),
     ]),
    ("taiwan-masters", "台灣篆刻名家", "Taiwanese Masters",
     "從渡海名家到當代中堅，認識把篆刻帶進台灣的每一雙手。", [
        ("cross-strait", "渡海名家", "Cross-Strait Masters", "王壯為、王北岳、曾紹杰、吳平——戰後台灣篆刻的奠基者。"),
        ("mid-generation", "中生代大家", "Mid-Generation Masters", "薛平南、黃嘗銘等承先啟後的一代。"),
        ("contemporary", "當代中堅", "Contemporary Practitioners", "陳宏勉、林淑女、柯詩安等活躍於當代的篆刻家。"),
        ("women", "女性篆刻家", "Women Seal Carvers", "林淑女等女性篆刻家如何在這個領域走出自己的路。"),
     ]),
    ("taiwan-culture", "台灣金石文化現場", "Epigraphy Culture in Taiwan",
     "故宮典藏、印石市場、文房印社——台灣現在哪裡看得到金石篆刻。", [
        ("palace", "故宮與文物典藏", "National Palace Museum", "毛公鼎、散氏盤與璽印典藏，鎮館之寶的台灣故事。"),
        ("market", "印石市場與拍賣", "Stone Market & Auctions", "台灣印石市場、拍賣會與行情怎麼走。"),
        ("shops", "印石店與文房", "Stone Shops & Stationery", "台北、台中、高雄哪裡買印石與印泥，店家怎麼挑。"),
        ("collection", "收藏與鑑賞", "Collecting & Appreciation", "收藏印章的門道：名家款、材質、鈕雕與印譜。"),
        ("creative", "文創與跨界應用", "Creative & Cross-Disciplinary", "從婚禮用印到 NFT 印章，篆刻怎麼走進現代生活。"),
     ]),
]

CHAPTER_MAP = {c[0]: {"zh": c[1], "en": c[2], "desc": c[3],
                      "subs": [{"id": s[0], "zh": s[1], "en": s[2], "desc": s[3]} for s in c[4]]}
               for c in CHAPTERS}
SUB_MAP = {}
for cid, cz, ce, cd, subs in CHAPTERS:
    for sid, sz, se, sd in subs:
        SUB_MAP[(cid, sid)] = {"zh": sz, "en": se, "desc": sd}
