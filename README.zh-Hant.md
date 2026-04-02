# purplestar — 紫微斗數命盤排算工具

[![PyPI](https://img.shields.io/pypi/v/purplestar)](https://pypi.org/project/purplestar/)

[English README available at README.md](https://github.com/jason-chao/purplestar/blob/main/README.md)

本套件為 Python 命令列工具，用於排算紫微斗數本命盤。計算邏輯源自 [iztro](https://github.com/SylarLong/iztro) 的演算法。

## 功能特色

- 輸入陽曆生日、出生時間（可省略）、性別及出生地，即可排出完整命盤
- 支援不詳出生時間（預設以子時排盤，並於輸出中注明）
- 支援兩種輸出格式：
  - **JSON** — 符合紫微斗數交換格式 v2（Zi Wei Dou Shu Interchange Schema v2）
  - **純文字** — 結構化純文字，適合在即時通訊軟件或 LLM 對話中分享
- 全程使用繁體中文

---

## 安裝

需要 Python 3.10 或以上版本。

```bash
pip install purplestar
```

### 從原始碼安裝

```bash
git clone <repository-url>
cd purplestar_chart
python3 -m venv venv
source venv/bin/activate          # macOS / Linux
# venv\Scripts\activate.bat       # Windows
pip install -e .
```

---

## 命令列使用說明

### 排出命盤

```
purplestar generate [OPTIONS]
```

**必填選項：**

| 選項 | 說明 |
|---|---|
| `-g`, `--gender` | `male`（男）或 `female`（女） |
| `-d`, `--date` | 陽曆出生日期，格式 `YYYY-MM-DD` |

**選填選項：**

| 選項 | 預設值 | 說明 |
|---|---|---|
| `-t`, `--time` | 不詳 | 24 小時制出生時間，格式 `HH:MM`。不知道時可省略。 |
| `-z`, `--timezone` | `UTC` | 出生地所在 IANA 時區（如 `Asia/Taipei`）。僅用於元資料。 |
| `-p`, `--place` | — | 出生地，自由文字（如 `台北市`）。 |
| `-n`, `--name` | — | 命主姓名或代號。 |
| `-f`, `--format` | `text` | 輸出格式：`text` 或 `json`。 |
| `-o`, `--output` | 標準輸出 | 輸出檔案路徑。省略時輸出至終端機。 |

#### 使用範例

輸出純文字命盤至終端機：

```bash
purplestar generate \
  --gender male \
  --date 1990-03-15 \
  --time 07:30 \
  --timezone Asia/Taipei \
  --place "台北市，台灣" \
  --name "陳大明"
```

輸出 JSON 命盤並儲存至檔案：

```bash
purplestar generate \
  --gender female \
  --date 1985-11-08 \
  --time 14:20 \
  --timezone Europe/London \
  --place "Bristol, England" \
  --name "Jane Smith" \
  --format json \
  --output jane_smith.json
```

出生時間不詳的情況：

```bash
purplestar generate \
  --gender male \
  --date 1972-07-04 \
  --timezone America/New_York \
  --place "New York, United States" \
  --name "John Doe"
```

省略出生時間時，命盤以子時（00:00–01:00）起算，輸出中會加入注意事項，說明結果僅供參考。

---

### 顯示已儲存的 JSON 命盤

```bash
purplestar show chart.json
```

顯示先前儲存的 JSON 命盤檔案中的主要欄位摘要。

---

### 版本資訊

```bash
purplestar --version
```

---

## Python API

亦可直接在 Python 程式碼中使用：

```python
from purplestar.core.chart import generate_chart
from purplestar.output.json_schema import to_json_schema
from purplestar.output.plaintext import to_plaintext

# 排出命盤
chart = generate_chart(
    gender='female',
    solar_date='1990-03-15',
    time='07:30',
    timezone='Asia/Taipei',
    place='台北市，台灣',
    name='範例命主',
)

# 取得純文字輸出
text = to_plaintext(chart)
print(text)

# 取得 JSON 格式輸出
json_str = to_json_schema(chart)
print(json_str)
```

### `generate_chart(gender, solar_date, time, timezone, place, name)`

| 參數 | 型別 | 說明 |
|---|---|---|
| `gender` | `str` | `'male'`（男）或 `'female'`（女） |
| `solar_date` | `str` | 陽曆出生日期，格式 `'YYYY-MM-DD'` |
| `time` | `str \| None` | 24 小時制出生時間 `'HH:MM'`，或 `None`（不詳） |
| `timezone` | `str \| None` | IANA 時區字串，或 `None` |
| `place` | `str \| None` | 出生地文字，或 `None` |
| `name` | `str \| None` | 命主識別代號，或 `None` |

回傳的 `dict` 可傳入 `to_json_schema()` 或 `to_plaintext()`。

### `to_json_schema(chart, indent=2)`

將命盤 dict 序列化為符合紫微斗數交換格式 v2 的 JSON 字串。格式規格詳見 [*Purple Star Astrology Interchange Schema v2*](https://github.com/jason-chao/purplestar/blob/main/guidelines/purplestar_chart_schema.md)。

### `to_plaintext(chart)`

將命盤 dict 序列化為結構化純文字格式。格式規格詳見 [*Plain-Text Format for 紫微斗數 Natal Charts*](https://github.com/jason-chao/purplestar/blob/main/guidelines/purplestar_chart_plaintext_format.md)。輸出適合直接貼入即時通訊軟件或 LLM 對話視窗。

---

## 輸出格式

### 純文字

純文字格式分三大區塊（完整規格見 [*Plain-Text Format for 紫微斗數 Natal Charts*](https://github.com/jason-chao/purplestar/blob/main/guidelines/purplestar_chart_plaintext_format.md)）：

1. **【命盤資料】** — 元資料：性別、陽曆及陰曆生日、時辰、宮位、五行局、命主、身主
2. **【十二宮】** — 依傳統論命順序列出十二宮（命宮 → 父母宮 → 福德宮 → 田宅宮 → 事業宮 → 交友宮 → 遷移宮 → 疾厄宮 → 財帛宮 → 子女宮 → 夫妻宮 → 兄弟宮），每宮列出主星（含廟旺）、輔星、四化、煞星及大限年齡
3. **【備註】** — 排盤方式說明及注意事項

範例片段：

```
【命宮】亥
主星：天同(廟)
輔星：天魁
四化：天同-化祿
煞星：（無）
大限：3–12
```

### JSON（交換格式 v2）

JSON 輸出符合紫微斗數交換格式 v2（完整規格見 [*Purple Star Astrology Interchange Schema v2*](https://github.com/jason-chao/purplestar/blob/main/guidelines/purplestar_chart_schema.md)）：

- **穩定的代碼系統**（`zi_wei`、`life`、`miao`、`lu`）而非顯示名稱
- **雙語目錄**：每個代碼均附繁體中文及英文標籤
- **嚴格宮位結構**：12 個宮位，每宮含位置、天干、地支、身宮標記及星曜陣列
- **星曜資料**：含廟旺代碼及四化代碼（如適用）
- **大限資料**：含年齡區間、天干及各大限四化

---

## 排盤說明

排盤採三合派標準，依據《紫微斗數全書》：

- **年干支起算**：以立春（約每年 2 月 4 日）為年份分界，計算年干支，符合紫微斗數慣例。
- **農曆轉換**：由 `sxtwl`（壽星萬年曆）套件負責陽曆轉農曆。
- **時辰劃分**：子時分為早子時（00:00–01:00）及晚子時（23:00–00:00）。晚子時在計算紫微星落宮時，農曆日期進一日。
- **時間不詳**：時間不詳時，以早子時排盤，命宮、身宮及若干時系星均受影響，結果僅供參考。
- **閏月處理**：閏月前 15 日視同前一月，後半月視同後一月。

---

## 執行測試

```bash
source venv/bin/activate
pytest tests/ -v
```

測試內容包括：
- 結構驗證（12 個宮位、14 顆主星）
- 四化完整性（化祿、化權、化科、化忌各一）
- 時間不詳時輸出中含注意事項

排出的命盤檔案（JSON 及純文字）儲存於 `tests/output/`。

---

## 專案結構

```
purplestar_chart/
├── purplestar/
│   ├── data/
│   │   ├── constants.py      # 查找表：天干、地支、宮位、星曜名稱
│   │   └── stars_data.py     # 星曜廟旺表（12 宮位 × 20 顆星）
│   ├── core/
│   │   ├── lunar.py          # 陽曆轉農曆、年干支、時辰索引
│   │   ├── palace.py         # 命宮、身宮、五行局、大限
│   │   ├── stars.py          # 各類星曜排布演算法（主星、輔星、雜曜）
│   │   └── chart.py          # generate_chart() 主函數
│   ├── output/
│   │   ├── json_schema.py    # JSON 格式序列化
│   │   └── plaintext.py      # 純文字格式序列化
│   └── cli.py                # Click 命令列介面
├── tests/
│   ├── test_charts.py        # 參數化命盤排算測試
│   └── output/               # 排出的命盤檔案（JSON + 純文字）
├── guidelines/
│   ├── purplestar_chart_schema.md           # Purple Star Astrology Interchange Schema v2
│   └── purplestar_chart_plaintext_format.md # Plain-Text Format for 紫微斗數 Natal Charts
├── iztro/                    # 參考用 TypeScript 實作
├── pyproject.toml
├── LICENSE
├── README.md                 # 英文說明
└── README.zh-Hant.md         # 本檔案（繁體中文說明）
```

---

## 授權條款

[MIT License](LICENSE) — Copyright (c) 2026 Jason Chao
