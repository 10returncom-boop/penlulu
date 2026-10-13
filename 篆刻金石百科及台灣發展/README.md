# 篆刻金石百科｜台灣發展 — 網站專案 README

權威、專業、大白話、資訊齊全、差異化的「篆刻金石 × 台灣發展」知識網站。
零依賴 Python 靜態生成器，資料與模板完全分離（Content Collections 式內容層），
圖片全數 WebP（165 張）。

## 快速開始

```bash
# 1) 展開內容層（data/site.json + data/articles/**/*.md）
python seed.py

# 2) 產生 WebP 圖庫（章節主視覺 + 每篇主圖 + 辨識卡）
python gen_images.py

# 3) 建置全站（HTML / sitemap.xml / assets/js/config.js / manifest.webmanifest）
python build.py

# 4) 產出交付物（2 份 Excel + 規格書 docx）
python gen_excel.py
python gen_spec_doc.py

# 5) 三項批次檢查（SEO 元素／連結圖片路徑／本機斷鏈）
python check.py
```

## 專案結構

```
build.py            建置腳本（讀 data/site.json + md → 全站 HTML、sitemap、config.js、manifest）
seed.py             內容展開器（articles_data.py → site.json + 逐篇 md）
data_master.py      10 大主題／35 子分類定義（唯一內容來源）
articles_data.py    77 篇條目明細（唯一內容來源）
gen_images.py       PIL 產生全部 WebP（165 張）
gen_excel.py        網站地圖.xlsx＋網站變數與網站導覽.xlsx
gen_spec_doc.py     規格書.docx
check.py            三項批次檢查
data/               site.json + articles/**/*.md（Content Collections 內容層）
assets/css|js|images/   樣式、互動腳本、WebP 圖庫
網站地圖.xlsx        全部頁面清單
網站變數與網站導覽.xlsx  變數＋導覽樹＋標籤索引
規格書.docx         完整專案規格書
CONTENT-SPEC.md     內容撰寫規範（唯一格式標準）
README.md           本檔
```

## 十大主題（Topic Cluster）

| 主題 | 說明 |
| --- | --- |
| 金石學入門 | 金石學是什麼、演變、與篆刻的關係、拓片著錄 |
| 篆刻演變史 | 先秦古璽 → 秦漢印 → 唐宋元 → 明清流派 → 近現代 |
| 印石材料百科 | 四大名石、壽山、青田、昌化、巴林、平價石、選石行情 |
| 篆刻技法 | 刀法、篆法、章法、鈐印 |
| 印章形制與用途 | 名號印、閒章、肖形印、鑑藏印 |
| 工具印泥與印譜 | 刻刀輔具、印泥品牌保養、印譜臨摹 |
| 台灣篆刻發展史 | 清代書院 → 日治書道 → 戰後渡海名家 → 解嚴 → 當代 |
| 台灣印社與社團 | 台灣印社、篆刻學會、縣市印社、教育比賽、兩岸國際交流 |
| 台灣篆刻名家 | 渡海名家、中生代、當代中堅、女性篆刻家 |
| 台灣金石文化現場 | 故宮典藏、拍賣市場、印石店、收藏、文創跨界 |

## 功能清單（全部實裝）

Breadcrumb＋BreadcrumbList Schema、Accordion 卡片、Sidebar＋Treemap＋TOC、
白天預設主題、MegaMenu 巨型導覽、Tag System、全站搜尋（autocomplete）、
Faceted Search、相關文章推薦、知識圖譜＋收藏清單、右下角固定導航、
OG=9 標籤、Favicon、FAQPage JSON-LD（每頁 ≥3 種結構化資料）、
sitemap.xml／robots.txt／404／webmanifest。

## 批次更新（改資料不動模板）

新增文章 → 改 `articles_data.py`（章節不存在則先在 `data_master.py` 加子分類）
→ 依「快速開始」第 1–5 步重跑即可，N 頁一次建置，Excel 與規格書同步更新。
