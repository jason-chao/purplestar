# Plain-Text Format for 紫微斗數 Natal Charts

## A Practical Guide for chat and LLM Use

---

## 1. Why Plain Text?

### The Problem with Grid Layouts

The traditional 紫微斗數 chart is a 4×4 bordered grid (twelve outer cells representing the twelve palaces, with the centre used for metadata). Recreating this in ASCII art or Unicode box-drawing characters is tempting but fails in practice for two reasons:

1. **Chat programs use a proportional font.** Characters like `│`, `─`, and CJK glyphs all have different widths, so columns never align. What looks perfect in a code editor turns into a jumbled mess on a phone screen.
2. **LLMs do not benefit from spatial layout.** Language models parse tokens sequentially. A neatly drawn grid adds noise (hundreds of formatting characters) without improving comprehension. Structured labelled text is far easier for an LLM to parse, reference, and reason about.

### Why a Structured List Format Works

A **palace-by-palace list** — each palace clearly labelled with its stars, Four Transformations (四化), and auxiliary information — solves both problems at once:

- **For human practitioners:** easy to scroll, search (Ctrl-F / Cmd-F), and read on any screen width. No alignment issues.
- **For LLMs:** unambiguous, parseable, and compact. Every data point is explicitly labelled, eliminating the need for the model to infer meaning from position.
- **Copy-paste friendly:** the same block of text works identically in chat programs and LLMs, a plain `.txt` file, or an email.

---

## 2. Format Specification

### 2.1 Overall Structure

A chart is divided into two sections, separated by blank lines:

```
【命盤資料】  ← Section 1: Metadata
【十二宮】    ← Section 2: The twelve palaces
```

### 2.2 Section 1 — 命盤資料 (Chart Metadata)

This header block captures everything about the native and the chart's foundational settings. Use one line per field, with a colon separator.

**Required fields:**

| Field | Description |
|---|---|
| 性別 | Gender (男 / 女) |
| 陽曆 | Gregorian date of birth (YYYY-MM-DD) |
| 陰曆 | Lunar date of birth (year stem-branch, month, day) |
| 時辰 | Birth hour as a 地支 two-hour period (e.g. 子時, 丑時) |
| 命宮地支 | The Earthly Branch position of the 命宮 |
| 身宮所在 | Which palace the 身宮 falls in |
| 五行局 | The element-number bureau (e.g. 水二局, 火六局) |
| 命主 | Life Governor star |
| 身主 | Body Governor star |

**Optional but helpful fields:**

| Field | Description |
|---|---|
| 姓名 or 代號 | Name or pseudonym (for privacy, initials or a code are fine) |
| 陰曆閏月 | Whether the birth month is a leap month (是 / 否) |
| 派別 | School or system used (e.g. 三合派, 飛星派, 欽天四化) |

### 2.3 Section 2 — 十二宮 (The Twelve Palaces)

List the twelve palaces in the conventional order:

> 命宮 → 兄弟宮 → 夫妻宮 → 子女宮 → 財帛宮 → 疾厄宮 → 遷移宮 → 交友宮 → 事業宮 → 田宅宮 → 福德宮 → 父母宮

Each palace is a block with the following structure:

```
【宮名】地支
主星：(list of major stars, comma-separated)
輔星：(list of minor/auxiliary stars, comma-separated)
四化：(any Transformations present, format: 星名-化X)
煞星：(malefic stars, if any)
大限：(decade luck period, e.g. 23–32)
小限：(if relevant, state the age)
```

**Formatting rules for star entries:**

- **Major stars (主星):** List 甲級主星 here — e.g. 紫微, 天機, 太陽, 武曲, 天同, 廉貞, 天府, 太陰, 貪狼, 巨門, 天相, 天梁, 七殺, 破軍. Include their brightness grade in parentheses: (廟), (旺), (得), (利), (平), (不), (陷).
- **Auxiliary stars (輔星):** 左輔, 右弼, 文昌, 文曲, 天魁, 天鉞, 祿存, 天馬, and similar.
- **Four Transformations (四化):** Mark each transformation next to the star that carries it, using the format `星名-化祿`, `星名-化權`, `星名-化科`, `星名-化忌`. If a star already listed as a 主星 carries a transformation, note it here rather than duplicating the star.
- **Malefic stars (煞星):** 擎羊, 陀羅, 火星, 鈴星, 地空, 地劫, and similar.
- **If a category is empty**, write `（無）` so that both humans and LLMs can confirm the field was not accidentally omitted.

---

## 3. Conventions and Tips

### 3.1 Character Encoding

Always use **UTF-8**. This is the default on all modern LLM interfaces, and virtually every text editor. Traditional Chinese characters will display correctly without any special settings.

### 3.2 Keeping It Copy-Paste Friendly

- Avoid tabs; use spaces or simply rely on line breaks.
- Avoid box-drawing characters (─ │ ┌ ┐ etc.) — they add no value and break.
- Use 【】(fullwidth square brackets) as section delimiters. They are visually distinct, easy to search for, and unambiguous.

### 3.3 Privacy

When sharing charts in group chats or with LLMs, consider replacing the native's real name with a pseudonym or code (e.g. "Case A", "甲君"). Omit the exact Gregorian date if only the lunar calendar data is needed for analysis.

### 3.4 Communicating with LLMs

When pasting a chart into an LLM conversation, a brief instruction line before the chart helps set context. For example:

> "Below is a 紫微斗數 natal chart in structured plain-text format. Please analyse the 命宮 and 事業宮 for career prospects."

This primes the model to treat the text block as structured chart data rather than free-form prose.

---

## 4. Worked Example

Below is a complete fictional chart demonstrating the format. All data is invented for illustration.

```
====================================
紫微斗數命盤
====================================

【命盤資料】
代號：范例甲君
性別：男
陽曆：1990-03-15
陰曆：庚午年 二月十九日
陰曆閏月：否
時辰：寅時
命宮地支：辰
身宮所在：遷移宮
五行局：水二局
命主：廉貞
身主：天同
派別：三合派

------------------------------------
【十二宮】
------------------------------------

【命宮】辰
主星：紫微(廟)、天府(廟)
輔星：左輔、天魁
四化：紫微-化權
煞星：（無）
大限：3–12

【兄弟宮】巳
主星：天機(旺)
輔星：文曲
四化：天機-化科
煞星：火星
大限：13–22

【夫妻宮】午
主星：太陽(旺)、太陰(不)
輔星：右弼
四化：太陽-化祿
煞星：陀羅
大限：23–32

【子女宮】未
主星：武曲(得)、貪狼(旺)
輔星：天鉞
四化：（無）
煞星：地劫
大限：33–42

【財帛宮】申
主星：天同(得)、巨門(旺)
輔星：祿存
四化：巨門-化忌
煞星：（無）
大限：43–52

【疾厄宮】酉
主星：廉貞(平)
輔星：（無）
四化：（無）
煞星：擎羊
大限：53–62

【遷移宮】戌 ★身宮
主星：天相(廟)
輔星：文昌、天馬
四化：文昌-化科
煞星：鈴星
大限：63–72

【交友宮】亥
主星：天梁(廟)
輔星：（無）
四化：（無）
煞星：地空
大限：73–82

【事業宮】子
主星：七殺(廟)
輔星：左輔
四化：（無）
煞星：火星
大限：83–92

【田宅宮】丑
主星：破軍(旺)
輔星：（無）
四化：（無）
煞星：（無）
大限：93–102

【福德宮】寅
主星：（無）
輔星：右弼
四化：（無）
煞星：陀羅
大限：103–112

【父母宮】卯
主星：天機(利)、天梁(廟)
輔星：天魁
四化：天機-化祿
煞星：（無）
大限：113–122

====================================
```

---

## 5. Quick Checklist Before Sending

Use this checklist to verify your chart is complete before pasting it into a chat program or an LLM prompt:

1. **Metadata complete?** Gender, both calendar dates, birth hour, 命宮 branch, 身宮 location, 五行局, 命主, 身主 all present.
2. **All twelve palaces listed?** Count them — there should be exactly twelve.
3. **Every palace has all fields?** Even empty ones should show （無）.
4. **四化 accounted for?** Exactly four Transformations (化祿、化權、化科、化忌) should appear across the entire chart — no more, no fewer.
5. **身宮 marked?** The palace containing the 身宮 should have a ★身宮 note next to its 地支.
6. **Brightness grades included?** Every major star should have its brightness in parentheses.
7. **No grid or box-drawing characters?** Confirm the text uses only line breaks, dashes, and brackets for structure.
8. **UTF-8 encoding?** If saving to a file, ensure it is saved as UTF-8.

---

## 6. Adapting the Format

### 6.1 For 飛星派 (Flying Star School)

If you follow a Flying Star school, add a line to each palace for palace-level flying transformations:

```
飛化：宮飛化祿入XX宮, 宮飛化忌入XX宮
```

### 6.2 For 大限 / 流年 Analysis

To include a specific decade or annual chart overlay, add a supplementary section after the natal chart:

```
------------------------------------
【大限盤】大限：33–42（命宮在未）
------------------------------------
【大限命宮】未
大限主星：武曲(得)、貪狼(旺)
大限四化：...
...
```

Follow the same palace-by-palace structure so the reader (human or LLM) can cross-reference with the natal chart.

### 6.3 Minimal Version for Quick Queries

If you only need to discuss one or two palaces (e.g. asking an LLM about career), you may send just the metadata section plus the relevant palaces, noting in your prompt that the chart is partial.

---

*Guide version 1.0 — March 2026*
