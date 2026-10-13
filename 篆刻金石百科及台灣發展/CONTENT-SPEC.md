# 內容撰寫規範 CONTENT-SPEC — 篆刻金石百科｜台灣發展

本檔是全站內容的**唯一格式標準**。所有篆刻金石與台灣發展知識內容由 `seed.py` 依
`data_master.py`（章節）＋ `articles_data.py`（條目）展開，
要新增／修改文章，只改這兩個資料檔，**不要動 build.py 模板**。

## 1. 架構（改資料不用動模板，Content Collections 式資料分離）

```
data_master.py       10 大主題、35 子分類定義（chapter/sub）
articles_data.py     77 篇條目明細（每筆 11 欄位，見下）
seed.py              → 產生 data/site.json + data/articles/<ch>/<sub>/<slug>.md
build.py             → 讀 site.json + md，產生全站 HTML（Content Collections 生成器）
gen_images.py        → PIL 產生 assets/images/*.webp（章節＋每篇主圖＋辨識卡）
gen_excel.py         → 產出「網站地圖.xlsx」「網站變數與網站導覽.xlsx」
gen_spec_doc.py      → 產出「規格書.docx」
check.py             → 三項批次檢查（SEO／連結圖片路徑／本機斷鏈）
```

單一檔案一頁：`data/articles/<chapter>/<sub>/<slug>.md` → `<chapter>/<sub>/<slug>.html`。
一個大主題＝一個資料夾，一次點擊＝一頁專業分析。

## 2. 每筆文章資料欄位（articles_data.py tuple）

```
(ch, sub, slug, zh, en, origin, traits, masters, tags, difficulty, summary)
```

- `ch/sub`    ：必須存在於 `data_master.py` 的 CHAPTERS / subs
- `origin`    ：年代／產地／流派／台灣在地定位（大白話一句）
- `traits`    ：3 條辨識重點（`|` 隔開），自動產生辨識表格
- `masters`   ：代表人物／經典作品／產地／台灣在地案例（一兩句）
- `tags`      ：4~6 個短標籤（逗號隔開），驅動 Tag System 與相關推薦
- `difficulty`：入門 / 中階 / 進階
- `summary`   ：一句話摘要（用於 meta description 與卡片）

## 3. 每篇自動產生的章節（seed.py / build.py 已內建）

1. 一句話搞懂（定義，大白話）
2. 來龍去脈（原理與脈絡）
3. 一眼辨識（3 條辨識重點表格）
4. 代表人物與經典（含台灣在地案例）
5. 為什麼重要
6. **台灣在地怎麼看**（台灣章節或含「台灣」標籤的條目自動加入：故宮實物、社團課程、店家採買）
7. 容易搞混（相似做法對照）
8. 常見問題 FAQ（Q/A，自動轉 FAQPage JSON-LD）

## 4. 內容定位原則

- 領域：篆刻金石百科 × 台灣發展；台灣在地實務觀點貫穿全站（約八成條目帶台灣視角）。
- 文筆：專業大白話、去 AI 模板化、具差異化特色；嚴禁學術腔、簡體用字與大陸術語。
- 內容：分類完整齊全、權威分析；非虛構案例（人物、展覽、社團、店家）需可查證。
- 語言：繁體中文（正體），人名、機構名以台灣通行用法為準。

## 5. 驗證

```
python build.py --check        # 驗證全部 md 完整性（frontmatter／章節歸屬／正文長度）
python build.py                # 完整建置
python build.py --list         # 列出每章篇數
python check.py                # 批次掃描：SEO 元素／連結圖片路徑／本機斷鏈
```

## 6. 重新產出流程（批次更新，可重複執行）

改完 `data_master.py` / `articles_data.py` 後依序執行：

```
python seed.py        # 更新 site.json 與全部 md
python gen_images.py  # 若新增文章，補 webp
python build.py       # 重建全站 HTML（含 sitemap.xml / config.js / manifest）
python gen_excel.py   # 更新兩份 Excel
python gen_spec_doc.py# 更新規格書
python check.py       # 三項檢核，0 缺失才交付
```
