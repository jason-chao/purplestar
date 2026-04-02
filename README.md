# purplestar — Purple Star Astrology (紫微斗數) Natal Chart Generator

[![PyPI](https://img.shields.io/pypi/v/purplestar)](https://pypi.org/project/purplestar/)

[繁體中文說明請見 README.zh-Hant.md](https://github.com/jason-chao/purplestar/blob/main/README.zh-Hant.md)

A Python package and command-line tool for generating Purple Star Astrology (紫微斗數 or "Zi Wei Dou Shu") natal charts. All calculation logic is derived from the algorithms used in [iztro](https://github.com/SylarLong/iztro).

## Features

- Generates complete natal charts from a solar date of birth, optional time, gender, and place
- Supports unknown birth time (defaults to 子時 with a note in the output)
- Outputs in two formats:
  - **JSON** — conforming to the Purple Star Interchange Schema v2
  - **Plain text** — structured, copy-paste-friendly format for chat and LLM use
- Uses Traditional Chinese (繁體中文) throughout

---

## Installation

Requires Python 3.10 or later.

```bash
pip install purplestar
```

### Install from Source

```bash
git clone <repository-url>
cd purplestar_chart
python3 -m venv venv
source venv/bin/activate          # macOS / Linux
# venv\Scripts\activate.bat       # Windows
pip install -e .
```

---

## Command-Line Usage

### Generate a natal chart

```
purplestar generate [OPTIONS]
```

**Required options:**

| Option | Description |
|---|---|
| `-g`, `--gender` | `male` or `female` |
| `-d`, `--date` | Date of birth in solar calendar, `YYYY-MM-DD` |

**Optional options:**

| Option | Default | Description |
|---|---|---|
| `-t`, `--time` | unknown | Time of birth in 24-hour format, `HH:MM`. Omit if unknown. |
| `-z`, `--timezone` | `UTC` | IANA timezone of the birth location (e.g. `Asia/Taipei`). Used for metadata only. |
| `-p`, `--place` | — | Place of birth, free text (e.g. `London, England`). |
| `-n`, `--name` | — | Name or identifier for the native. |
| `-f`, `--format` | `text` | Output format: `text` or `json`. |
| `-o`, `--output` | stdout | Output file path. Prints to stdout if omitted. |

#### Examples

Generate a plain-text chart to the terminal:

```bash
purplestar generate \
  --gender male \
  --date 1990-03-15 \
  --time 07:30 \
  --timezone Asia/Taipei \
  --place "Taipei, Taiwan" \
  --name "陳大明"
```

Generate a JSON chart and save it to a file:

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

Generate a chart for a native with an unknown birth time:

```bash
purplestar generate \
  --gender male \
  --date 1972-07-04 \
  --timezone America/New_York \
  --place "New York, United States" \
  --name "John Doe"
```

When the birth time is omitted, the chart is calculated assuming 子時 (00:00–01:00) and a note is added to the output indicating that the time is unknown and the result should be treated with caution.

---

### Display a saved JSON chart

```bash
purplestar show chart.json
```

Displays a summary of the key fields from a previously saved JSON chart file.

---

### Version

```bash
purplestar --version
```

---

## Package API

You can use the package directly in Python code:

```python
from purplestar.core.chart import generate_chart
from purplestar.output.json_schema import to_json_schema
from purplestar.output.plaintext import to_plaintext

# Generate a chart
chart = generate_chart(
    gender='female',
    solar_date='1990-03-15',
    time='07:30',
    timezone='Asia/Taipei',
    place='Taipei, Taiwan',
    name='Sample Native',
)

# Get plain-text output
text = to_plaintext(chart)
print(text)

# Get JSON schema v2 output
json_str = to_json_schema(chart)
print(json_str)
```

### `generate_chart(gender, solar_date, time, timezone, place, name)`

| Parameter | Type | Description |
|---|---|---|
| `gender` | `str` | `'male'` or `'female'` |
| `solar_date` | `str` | `'YYYY-MM-DD'` in the solar (Gregorian) calendar |
| `time` | `str \| None` | `'HH:MM'` in 24-hour format, or `None` if unknown |
| `timezone` | `str \| None` | IANA timezone string, or `None` |
| `place` | `str \| None` | Free-text place name, or `None` |
| `name` | `str \| None` | Identifier for the native, or `None` |

Returns a `dict` that can be passed to `to_json_schema()` or `to_plaintext()`.

### `to_json_schema(chart, indent=2)`

Serialises a chart dict to a JSON string conforming to the Zi Wei Dou Shu Interchange Schema v2. The schema is fully described in the [*Purple Star Astrology Interchange Schema v2*](https://github.com/jason-chao/purplestar/blob/main/guidelines/purplestar_chart_schema.md).

### `to_plaintext(chart)`

Serialises a chart dict to the structured plain-text format described in the [*Plain-Text Format for 紫微斗數 Natal Charts*](https://github.com/jason-chao/purplestar/blob/main/guidelines/purplestar_chart_plaintext_format.md) guide. The output is suitable for sharing via chat programs or pasting into an LLM conversation.

---

## Output Formats

### Plain Text

The plain-text format consists of three sections (see the [*Plain-Text Format for 紫微斗數 Natal Charts*](https://github.com/jason-chao/purplestar/blob/main/guidelines/purplestar_chart_plaintext_format.md) guide for the full specification):

1. **【命盤資料】** — chart metadata: gender, solar and lunar dates, birth hour, palace positions, five-elements bureau, life and body governors
2. **【十二宮】** — twelve palaces listed in the conventional interpretation order (命宮 → 父母宮 → 福德宮 → 田宅宮 → 事業宮 → 交友宮 → 遷移宮 → 疾厄宮 → 財帛宮 → 子女宮 → 夫妻宮 → 兄弟宮), each showing major stars with brightness grades, auxiliary stars, four transformations (四化), malefic stars, and decadal luck age range
3. **【備註】** — notes on the generation method and any caveats

Example snippet:

```
【命宮】亥
主星：天同(廟)
輔星：天魁
四化：天同-化祿
煞星：（無）
大限：3–12
```

### JSON (Schema v2)

The JSON output conforms to the Zi Wei Dou Shu Interchange Schema v2 (see the [*Purple Star Astrology Interchange Schema v2*](https://github.com/jason-chao/purplestar/blob/main/guidelines/purplestar_chart_schema.md) for the full specification):

- **Stable canonical codes** (`zi_wei`, `life`, `miao`, `lu`) rather than display labels
- **Bilingual catalog** with Traditional Chinese and English labels for every code
- **Strict palace structure**: exactly 12 palaces, each with position, stem, branch, body-palace flag, and an array of star placements
- **Star placements** carry brightness code and natal transformation code where applicable
- **Decadal overlays** with age ranges, heavenly stem, and four transformations for each decade

---

## Calculation Notes

The calculation follows the standard 三合派 (Three Harmonies School) methodology as documented in 《紫微斗數全書》:

- **Year boundary**: 立春 (Start of Spring, approximately 4 February) is used as the year boundary for the year's heavenly stem and earthly branch (年干支), as is conventional in 紫微斗數.
- **Lunar calendar**: Conversion from solar to lunar dates is performed by `sxtwl`, which implements the 壽星萬年曆 algorithm.
- **Time periods (時辰)**: The 子時 is split into early 子時 (00:00–01:00) and late 子時 (晚子時, 23:00–00:00). Late 子時 advances the lunar day for the calculation of the Purple Star (紫微星) position.
- **Unknown birth time**: When birth time is unknown, the chart is calculated as if the native were born in early 子時 (00:00–01:00). This affects the soul palace (命宮), body palace (身宮), and several time-dependent stars. The result should be treated as approximate.
- **Leap months (閏月)**: The standard fix-leap rule is applied: a leap month's first 15 days are treated as the preceding month and the remainder as the following month.

---

## Running Tests

```bash
source venv/bin/activate
pytest tests/ -v
```

The tests generate charts for a set of individuals and validate:
- Structural integrity (exactly 12 palaces, 14 major stars)
- Presence of all four natal transformations (化祿, 化權, 化科, 化忌)
- Correct five-elements bureau and palace positions for a known case

Generated chart files (JSON and plain text) are saved to `tests/output/`.

---

## Project Structure

```
purplestar_chart/
├── purplestar/
│   ├── data/
│   │   ├── constants.py      # Lookup tables: stems, branches, palaces, star names
│   │   └── stars_data.py     # Star brightness tables (12 positions × 20 stars)
│   ├── core/
│   │   ├── lunar.py          # Solar-to-lunar conversion, year GZ, time index
│   │   ├── palace.py         # Soul/body palace, five-elements bureau, decadal luck
│   │   ├── stars.py          # All star placement algorithms (major, minor, adjective)
│   │   └── chart.py          # Main generate_chart() orchestrator
│   ├── output/
│   │   ├── json_schema.py    # JSON schema v2 serialiser
│   │   └── plaintext.py      # Plain-text serialiser
│   └── cli.py                # Click-based CLI
├── tests/
│   ├── test_charts.py        # Parametrised chart generation tests
│   └── output/               # Generated chart files (JSON + text)
├── guidelines/
│   ├── purplestar_chart_schema.md           # Purple Star Astrology Interchange Schema v2
│   └── purplestar_chart_plaintext_format.md # Plain-Text Format for 紫微斗數 Natal Charts
├── iztro/                    # Reference TypeScript implementation
├── pyproject.toml
├── LICENSE
└── README.md
```

---

## License

[MIT License](LICENSE) — Copyright (c) 2026 Jason Chao
