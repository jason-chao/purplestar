# Purple Star Astrology Interchange Schema v2

## Purpose of this document

This document proposes an improved JSON-based interchange design for a Purple Star Astrology (also known as "Zi Wei Dou Shu") chart.

It is intended for two audiences at once:

- **Developers**, who need a stable structure they can validate, store, exchange, index, and transform.
- **Non-technical practitioners**, who need the format to reflect real chart logic in a way that remains readable, faithful, and explainable.

The design keeps a **catalog-driven interchange model** so that machine codes remain stable across software, but it also strengthens the core format with stricter validation rules, clearer separation between natal data and derived overlays, and more practitioner-friendly chart structure.

---

## Design goals

### 1. Stable machine identifiers
The core data uses canonical codes such as `zi_wei`, `life`, `lu`, and `miao` rather than depending on display labels.

### 2. Clear separation between chart facts and display vocabulary
The format distinguishes:

- **chart facts** such as palace placement, stem, branch, brightness, and transformation
- **catalog vocabulary** such as Chinese and English labels

This makes the format more portable and less tied to any single application.

### 3. Stronger reproducibility
The birth input is stored explicitly as the **source of truth** for chart generation. A consumer can inspect the exact date basis, leap-month status, hour branch, timezone, and gender used for calculation.

### 4. Stricter structural validation
The schema uses `additionalProperties: false` in core objects, exact palace counts, bounded position ranges, and controlled enums for the most important shared concepts.

### 5. Better fit with actual Zi Wei chart logic
The schema treats the following as first-class concepts:

- the fixed 12-palace structure
- heavenly stems and earthly branches
- natal placements
- life and body palace positions
- brightness
- natal transformations
- decadal overlays
- annual overlays
- school and engine metadata

### 6. Good bilingual support without making translations canonical
The catalog stores localized labels such as `zh-Hant`, optional `zh-Hans`, and `en`, while the chart itself remains code-based.

### 7. Room for school-specific diversity
The schema standardizes the shared shape of the data without forcing every school to use exactly the same vocabulary or doctrinal rule set.

---

## Summary of the design

This version combines two important ideas:

1. A **catalog-driven interchange architecture**, where codes are primary and localized labels live in a catalog.
2. A **strict natal-core structure**, where the birth input, natal chart, and time overlays are clearly separated and tightly validated.

The result is a schema that is:

- simpler to reason about than a fully merged multi-layer payload
- more reusable across software systems
- easier to explain to practitioners
- safer to validate in production

---

# I. Formal JSON Schema

The following is the proposed JSON Schema.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.org/schemas/ziwei-chart.interchange.v2.schema.json",
  "title": "Purple Star Astrology Interchange Schema",
  "description": "A bilingual, catalog-driven JSON format for Purple Star Astrology natal charts with optional decadal and annual overlays.",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "chart_type",
    "default_locale",
    "meta",
    "subject",
    "birth_data",
    "system",
    "catalog",
    "chart"
  ],
  "properties": {
    "schema_version": {
      "type": "string"
    },
    "chart_type": {
      "type": "string",
      "enum": [
        "ziwei.natal"
      ]
    },
    "default_locale": {
      "type": "string"
    },
    "meta": {
      "$ref": "#/$defs/meta"
    },
    "subject": {
      "$ref": "#/$defs/subject"
    },
    "birth_data": {
      "$ref": "#/$defs/birthData"
    },
    "system": {
      "$ref": "#/$defs/system"
    },
    "catalog": {
      "$ref": "#/$defs/catalog"
    },
    "chart": {
      "$ref": "#/$defs/chart"
    },
    "overlays": {
      "$ref": "#/$defs/overlays"
    },
    "extensions": {
      "type": "object",
      "description": "Optional vendor, project, or school-specific additions."
    }
  },
  "$defs": {
    "canonicalCode": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9_]*$",
      "description": "Stable lowercase snake_case machine identifier."
    },
    "localeStringMap": {
      "type": "object",
      "required": [
        "zh-Hant",
        "en"
      ],
      "properties": {
        "zh-Hant": {
          "type": "string"
        },
        "zh-Hans": {
          "type": "string"
        },
        "en": {
          "type": "string"
        }
      },
      "additionalProperties": {
        "type": "string"
      }
    },
    "codedEntry": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "code",
        "labels"
      ],
      "properties": {
        "code": {
          "$ref": "#/$defs/canonicalCode"
        },
        "labels": {
          "$ref": "#/$defs/localeStringMap"
        },
        "aliases": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "tags": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "notes": {
          "type": "string"
        },
        "extensions": {
          "type": "object"
        }
      }
    },
    "meta": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "generated_by",
        "generated_at"
      ],
      "properties": {
        "generated_by": {
          "type": "string"
        },
        "generated_at": {
          "type": "string",
          "format": "date-time"
        },
        "notes": {
          "type": "string"
        }
      }
    },
    "subject": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "id"
      ],
      "properties": {
        "id": {
          "type": "string"
        },
        "name": {
          "type": "string"
        }
      }
    },
    "stem": {
      "type": "string",
      "enum": [
        "jia",
        "yi",
        "bing",
        "ding",
        "wu",
        "ji",
        "geng",
        "xin",
        "ren",
        "gui"
      ]
    },
    "branch": {
      "type": "string",
      "enum": [
        "yin",
        "mao",
        "chen",
        "si",
        "wu",
        "wei",
        "shen",
        "you",
        "xu",
        "hai",
        "zi",
        "chou"
      ]
    },
    "gender": {
      "type": "string",
      "enum": [
        "male",
        "female"
      ]
    },
    "birthData": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "calendar",
        "year",
        "month",
        "day",
        "is_leap_month",
        "hour_branch",
        "gender",
        "timezone"
      ],
      "properties": {
        "calendar": {
          "type": "string",
          "enum": [
            "lunar",
            "solar"
          ]
        },
        "year": {
          "type": "integer",
          "minimum": 1
        },
        "month": {
          "type": "integer",
          "minimum": 1,
          "maximum": 12
        },
        "day": {
          "type": "integer",
          "minimum": 1,
          "maximum": 31
        },
        "is_leap_month": {
          "type": "boolean"
        },
        "hour_branch": {
          "$ref": "#/$defs/branch"
        },
        "gender": {
          "$ref": "#/$defs/gender"
        },
        "timezone": {
          "type": "string"
        },
        "solar_datetime": {
          "type": "string",
          "format": "date-time"
        },
        "input_clock_time": {
          "type": "string",
          "format": "time"
        },
        "place": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "name": {
              "type": "string"
            },
            "country_code": {
              "type": "string"
            },
            "latitude": {
              "type": "number"
            },
            "longitude": {
              "type": "number"
            }
          }
        }
      }
    },
    "system": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "family",
        "school"
      ],
      "properties": {
        "family": {
          "type": "string",
          "enum": [
            "ziwei_doushu"
          ]
        },
        "school": {
          "type": "string"
        },
        "engine": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "name": {
              "type": "string"
            },
            "version": {
              "type": "string"
            }
          }
        },
        "rule_set": {
          "type": "object",
          "description": "Optional explicit rule metadata used in calculation.",
          "additionalProperties": true
        }
      }
    },
    "catalog": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "stems",
        "branches",
        "palaces",
        "stars",
        "brightness",
        "transformations"
      ],
      "properties": {
        "stems": {
          "type": "object",
          "additionalProperties": {
            "$ref": "#/$defs/codedEntry"
          }
        },
        "branches": {
          "type": "object",
          "additionalProperties": {
            "$ref": "#/$defs/codedEntry"
          }
        },
        "palaces": {
          "type": "object",
          "additionalProperties": {
            "$ref": "#/$defs/codedEntry"
          }
        },
        "stars": {
          "type": "object",
          "additionalProperties": {
            "$ref": "#/$defs/codedEntry"
          }
        },
        "brightness": {
          "type": "object",
          "additionalProperties": {
            "$ref": "#/$defs/codedEntry"
          }
        },
        "transformations": {
          "type": "object",
          "additionalProperties": {
            "$ref": "#/$defs/codedEntry"
          }
        },
        "markers": {
          "type": "object",
          "additionalProperties": {
            "$ref": "#/$defs/codedEntry"
          }
        }
      }
    },
    "yinYang": {
      "type": "string",
      "enum": [
        "yin",
        "yang"
      ]
    },
    "fiveElementBureau": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "element",
        "number"
      ],
      "properties": {
        "element": {
          "type": "string",
          "enum": [
            "water",
            "wood",
            "metal",
            "earth",
            "fire"
          ]
        },
        "number": {
          "type": "integer",
          "enum": [
            2,
            3,
            4,
            5,
            6
          ]
        }
      }
    },
    "starCategory": {
      "type": "string",
      "enum": [
        "major",
        "minor",
        "auxiliary",
        "misc"
      ]
    },
    "brightnessCode": {
      "type": "string",
      "enum": [
        "miao",
        "wang",
        "de",
        "li",
        "ping",
        "bu",
        "xian"
      ]
    },
    "transformationCode": {
      "type": "string",
      "enum": [
        "lu",
        "quan",
        "ke",
        "ji"
      ]
    },
    "transformationEntry": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "star",
        "transformation"
      ],
      "properties": {
        "star": {
          "$ref": "#/$defs/canonicalCode"
        },
        "transformation": {
          "$ref": "#/$defs/transformationCode"
        }
      }
    },
    "starPlacement": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "star",
        "category"
      ],
      "properties": {
        "star": {
          "$ref": "#/$defs/canonicalCode"
        },
        "category": {
          "$ref": "#/$defs/starCategory"
        },
        "brightness": {
          "$ref": "#/$defs/brightnessCode"
        },
        "natal_transformation": {
          "$ref": "#/$defs/transformationCode"
        },
        "transformation_source": {
          "type": "string",
          "enum": [
            "self",
            "applied"
          ]
        },
        "note": {
          "type": "string"
        },
        "extensions": {
          "type": "object"
        }
      }
    },
    "palace": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "position",
        "palace",
        "stem",
        "branch",
        "is_body_palace",
        "stars"
      ],
      "properties": {
        "position": {
          "type": "integer",
          "minimum": 1,
          "maximum": 12
        },
        "palace": {
          "$ref": "#/$defs/canonicalCode"
        },
        "stem": {
          "$ref": "#/$defs/stem"
        },
        "branch": {
          "$ref": "#/$defs/branch"
        },
        "is_body_palace": {
          "type": "boolean"
        },
        "stars": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/starPlacement"
          }
        },
        "markers": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "changsheng12": {
              "$ref": "#/$defs/canonicalCode"
            },
            "boshi12": {
              "$ref": "#/$defs/canonicalCode"
            },
            "jiangqian12": {
              "$ref": "#/$defs/canonicalCode"
            },
            "suiqian12": {
              "$ref": "#/$defs/canonicalCode"
            }
          }
        }
      }
    },
    "chartProfile": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "yin_yang",
        "five_element_bureau",
        "ming_palace_position",
        "body_palace_position"
      ],
      "properties": {
        "yin_yang": {
          "$ref": "#/$defs/yinYang"
        },
        "five_element_bureau": {
          "$ref": "#/$defs/fiveElementBureau"
        },
        "life_master": {
          "$ref": "#/$defs/canonicalCode"
        },
        "body_master": {
          "$ref": "#/$defs/canonicalCode"
        },
        "ming_palace_position": {
          "type": "integer",
          "minimum": 1,
          "maximum": 12
        },
        "body_palace_position": {
          "type": "integer",
          "minimum": 1,
          "maximum": 12
        }
      }
    },
    "chart": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "profile",
        "palaces"
      ],
      "properties": {
        "profile": {
          "$ref": "#/$defs/chartProfile"
        },
        "palaces": {
          "type": "array",
          "minItems": 12,
          "maxItems": 12,
          "items": {
            "$ref": "#/$defs/palace"
          },
          "description": "Exactly 12 palaces ordered by position 1-12, where position 1 is Yin/寅 and then proceeds counter-clockwise through the fixed Zi Wei sequence."
        }
      }
    },
    "decadeLimit": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "age_range",
        "palace_position",
        "stem",
        "transformations"
      ],
      "properties": {
        "age_range": {
          "type": "array",
          "minItems": 2,
          "maxItems": 2,
          "items": {
            "type": "integer",
            "minimum": 0
          }
        },
        "palace_position": {
          "type": "integer",
          "minimum": 1,
          "maximum": 12
        },
        "stem": {
          "$ref": "#/$defs/stem"
        },
        "transformations": {
          "type": "array",
          "minItems": 4,
          "maxItems": 4,
          "items": {
            "$ref": "#/$defs/transformationEntry"
          }
        }
      }
    },
    "annualChart": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "year",
        "stem",
        "branch",
        "ming_position",
        "transformations"
      ],
      "properties": {
        "year": {
          "type": "integer"
        },
        "stem": {
          "$ref": "#/$defs/stem"
        },
        "branch": {
          "$ref": "#/$defs/branch"
        },
        "ming_position": {
          "type": "integer",
          "minimum": 1,
          "maximum": 12
        },
        "transformations": {
          "type": "array",
          "minItems": 4,
          "maxItems": 4,
          "items": {
            "$ref": "#/$defs/transformationEntry"
          }
        }
      }
    },
    "overlays": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "decade_limits": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/decadeLimit"
          }
        },
        "annual_charts": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/annualChart"
          }
        }
      }
    }
  }
}
```

---

# II. Full JSON example

The following example is **illustrative**. Its purpose is to demonstrate the structure completely and coherently. It should not be treated as an authoritative reading or as proof of any specific school calculation.

```json
{
  "schema_version": "2.0.0",
  "chart_type": "ziwei.natal",
  "default_locale": "en",
  "meta": {
    "generated_by": "example-engine 2.0.0",
    "generated_at": "2026-03-30T12:00:00Z",
    "notes": "Illustrative chart showing all core schema features. Placements are structurally complete but not intended as an authoritative reading."
  },
  "subject": {
    "id": "chart-001",
    "name": "Example Native"
  },
  "birth_data": {
    "calendar": "lunar",
    "year": 1985,
    "month": 3,
    "day": 15,
    "is_leap_month": false,
    "hour_branch": "yin",
    "gender": "male",
    "timezone": "Asia/Taipei",
    "solar_datetime": "1985-05-04T04:00:00+08:00",
    "input_clock_time": "04:00:00",
    "place": {
      "name": "Taipei",
      "country_code": "TW",
      "latitude": 25.033,
      "longitude": 121.5654
    }
  },
  "system": {
    "family": "ziwei_doushu",
    "school": "sihua",
    "engine": {
      "name": "example-engine",
      "version": "2.0.0"
    },
    "rule_set": {
      "brightness_model": "core-seven-level",
      "transformation_model": "year-stem-and-overlay-stem",
      "palace_order": "yin_to_chou_counterclockwise"
    }
  },
  "catalog": {
    "stems": {
      "jia": {
        "code": "jia",
        "labels": {
          "zh-Hant": "甲",
          "zh-Hans": "甲",
          "en": "Jia"
        }
      },
      "yi": {
        "code": "yi",
        "labels": {
          "zh-Hant": "乙",
          "zh-Hans": "乙",
          "en": "Yi"
        }
      },
      "bing": {
        "code": "bing",
        "labels": {
          "zh-Hant": "丙",
          "zh-Hans": "丙",
          "en": "Bing"
        }
      },
      "ding": {
        "code": "ding",
        "labels": {
          "zh-Hant": "丁",
          "zh-Hans": "丁",
          "en": "Ding"
        }
      },
      "wu": {
        "code": "wu",
        "labels": {
          "zh-Hant": "戊",
          "zh-Hans": "戊",
          "en": "Wu"
        }
      },
      "ji": {
        "code": "ji",
        "labels": {
          "zh-Hant": "己",
          "zh-Hans": "己",
          "en": "Ji"
        }
      },
      "geng": {
        "code": "geng",
        "labels": {
          "zh-Hant": "庚",
          "zh-Hans": "庚",
          "en": "Geng"
        }
      },
      "xin": {
        "code": "xin",
        "labels": {
          "zh-Hant": "辛",
          "zh-Hans": "辛",
          "en": "Xin"
        }
      },
      "ren": {
        "code": "ren",
        "labels": {
          "zh-Hant": "壬",
          "zh-Hans": "壬",
          "en": "Ren"
        }
      },
      "gui": {
        "code": "gui",
        "labels": {
          "zh-Hant": "癸",
          "zh-Hans": "癸",
          "en": "Gui"
        }
      }
    },
    "branches": {
      "yin": {
        "code": "yin",
        "labels": {
          "zh-Hant": "寅",
          "zh-Hans": "寅",
          "en": "Yin"
        }
      },
      "mao": {
        "code": "mao",
        "labels": {
          "zh-Hant": "卯",
          "zh-Hans": "卯",
          "en": "Mao"
        }
      },
      "chen": {
        "code": "chen",
        "labels": {
          "zh-Hant": "辰",
          "zh-Hans": "辰",
          "en": "Chen"
        }
      },
      "si": {
        "code": "si",
        "labels": {
          "zh-Hant": "巳",
          "zh-Hans": "巳",
          "en": "Si"
        }
      },
      "wu": {
        "code": "wu",
        "labels": {
          "zh-Hant": "午",
          "zh-Hans": "午",
          "en": "Wu"
        }
      },
      "wei": {
        "code": "wei",
        "labels": {
          "zh-Hant": "未",
          "zh-Hans": "未",
          "en": "Wei"
        }
      },
      "shen": {
        "code": "shen",
        "labels": {
          "zh-Hant": "申",
          "zh-Hans": "申",
          "en": "Shen"
        }
      },
      "you": {
        "code": "you",
        "labels": {
          "zh-Hant": "酉",
          "zh-Hans": "酉",
          "en": "You"
        }
      },
      "xu": {
        "code": "xu",
        "labels": {
          "zh-Hant": "戌",
          "zh-Hans": "戌",
          "en": "Xu"
        }
      },
      "hai": {
        "code": "hai",
        "labels": {
          "zh-Hant": "亥",
          "zh-Hans": "亥",
          "en": "Hai"
        }
      },
      "zi": {
        "code": "zi",
        "labels": {
          "zh-Hant": "子",
          "zh-Hans": "子",
          "en": "Zi"
        }
      },
      "chou": {
        "code": "chou",
        "labels": {
          "zh-Hant": "丑",
          "zh-Hans": "丑",
          "en": "Chou"
        }
      }
    },
    "palaces": {
      "siblings": {
        "code": "siblings",
        "labels": {
          "zh-Hant": "兄弟宮",
          "zh-Hans": "兄弟宫",
          "en": "Siblings"
        }
      },
      "spouse": {
        "code": "spouse",
        "labels": {
          "zh-Hant": "夫妻宮",
          "zh-Hans": "夫妻宫",
          "en": "Spouse"
        }
      },
      "life": {
        "code": "life",
        "labels": {
          "zh-Hant": "命宮",
          "zh-Hans": "命宫",
          "en": "Life"
        }
      },
      "parents": {
        "code": "parents",
        "labels": {
          "zh-Hant": "父母宮",
          "zh-Hans": "父母宫",
          "en": "Parents"
        }
      },
      "fortune": {
        "code": "fortune",
        "labels": {
          "zh-Hant": "福德宮",
          "zh-Hans": "福德宫",
          "en": "Fortune"
        }
      },
      "property": {
        "code": "property",
        "labels": {
          "zh-Hant": "田宅宮",
          "zh-Hans": "田宅宫",
          "en": "Property"
        }
      },
      "career": {
        "code": "career",
        "labels": {
          "zh-Hant": "官祿宮",
          "zh-Hans": "官禄宫",
          "en": "Career"
        }
      },
      "friends": {
        "code": "friends",
        "labels": {
          "zh-Hant": "交友宮",
          "zh-Hans": "交友宫",
          "en": "Friends"
        }
      },
      "travel": {
        "code": "travel",
        "labels": {
          "zh-Hant": "遷移宮",
          "zh-Hans": "迁移宫",
          "en": "Travel"
        }
      },
      "health": {
        "code": "health",
        "labels": {
          "zh-Hant": "疾厄宮",
          "zh-Hans": "疾厄宫",
          "en": "Health"
        }
      },
      "wealth": {
        "code": "wealth",
        "labels": {
          "zh-Hant": "財帛宮",
          "zh-Hans": "财帛宫",
          "en": "Wealth"
        }
      },
      "children": {
        "code": "children",
        "labels": {
          "zh-Hant": "子女宮",
          "zh-Hans": "子女宫",
          "en": "Children"
        }
      }
    },
    "stars": {
      "tai_yang": {
        "code": "tai_yang",
        "labels": {
          "zh-Hant": "太陽",
          "zh-Hans": "太阳",
          "en": "Tai Yang"
        },
        "tags": [
          "major"
        ]
      },
      "wen_chang": {
        "code": "wen_chang",
        "labels": {
          "zh-Hant": "文昌",
          "zh-Hans": "文昌",
          "en": "Wen Chang"
        },
        "tags": [
          "auxiliary"
        ]
      },
      "wu_qu": {
        "code": "wu_qu",
        "labels": {
          "zh-Hant": "武曲",
          "zh-Hans": "武曲",
          "en": "Wu Qu"
        },
        "tags": [
          "major"
        ]
      },
      "tian_xiang": {
        "code": "tian_xiang",
        "labels": {
          "zh-Hant": "天相",
          "zh-Hans": "天相",
          "en": "Tian Xiang"
        },
        "tags": [
          "major"
        ]
      },
      "zi_wei": {
        "code": "zi_wei",
        "labels": {
          "zh-Hant": "紫微",
          "zh-Hans": "紫微",
          "en": "Zi Wei"
        },
        "tags": [
          "major"
        ]
      },
      "tian_fu": {
        "code": "tian_fu",
        "labels": {
          "zh-Hant": "天府",
          "zh-Hans": "天府",
          "en": "Tian Fu"
        },
        "tags": [
          "major"
        ]
      },
      "zuo_fu": {
        "code": "zuo_fu",
        "labels": {
          "zh-Hant": "左輔",
          "zh-Hans": "左辅",
          "en": "Zuo Fu"
        },
        "tags": [
          "auxiliary"
        ]
      },
      "you_bi": {
        "code": "you_bi",
        "labels": {
          "zh-Hant": "右弼",
          "zh-Hans": "右弼",
          "en": "You Bi"
        },
        "tags": [
          "auxiliary"
        ]
      },
      "tai_yin": {
        "code": "tai_yin",
        "labels": {
          "zh-Hant": "太陰",
          "zh-Hans": "太阴",
          "en": "Tai Yin"
        },
        "tags": [
          "major"
        ]
      },
      "tan_lang": {
        "code": "tan_lang",
        "labels": {
          "zh-Hant": "貪狼",
          "zh-Hans": "贪狼",
          "en": "Tan Lang"
        },
        "tags": [
          "major"
        ]
      },
      "tian_ma": {
        "code": "tian_ma",
        "labels": {
          "zh-Hant": "天馬",
          "zh-Hans": "天马",
          "en": "Tian Ma"
        },
        "tags": [
          "misc"
        ]
      },
      "ju_men": {
        "code": "ju_men",
        "labels": {
          "zh-Hant": "巨門",
          "zh-Hans": "巨门",
          "en": "Ju Men"
        },
        "tags": [
          "major"
        ]
      },
      "huo_xing": {
        "code": "huo_xing",
        "labels": {
          "zh-Hant": "火星",
          "zh-Hans": "火星",
          "en": "Huo Xing"
        },
        "tags": [
          "minor"
        ]
      },
      "tian_ji": {
        "code": "tian_ji",
        "labels": {
          "zh-Hant": "天機",
          "zh-Hans": "天机",
          "en": "Tian Ji"
        },
        "tags": [
          "major"
        ]
      },
      "tian_liang": {
        "code": "tian_liang",
        "labels": {
          "zh-Hant": "天梁",
          "zh-Hans": "天梁",
          "en": "Tian Liang"
        },
        "tags": [
          "major"
        ]
      },
      "qi_sha": {
        "code": "qi_sha",
        "labels": {
          "zh-Hant": "七殺",
          "zh-Hans": "七杀",
          "en": "Qi Sha"
        },
        "tags": [
          "major"
        ]
      },
      "lian_zhen": {
        "code": "lian_zhen",
        "labels": {
          "zh-Hant": "廉貞",
          "zh-Hans": "廉贞",
          "en": "Lian Zhen"
        },
        "tags": [
          "major"
        ]
      },
      "wen_qu": {
        "code": "wen_qu",
        "labels": {
          "zh-Hant": "文曲",
          "zh-Hans": "文曲",
          "en": "Wen Qu"
        },
        "tags": [
          "auxiliary"
        ]
      },
      "po_jun": {
        "code": "po_jun",
        "labels": {
          "zh-Hant": "破軍",
          "zh-Hans": "破军",
          "en": "Po Jun"
        },
        "tags": [
          "major"
        ]
      },
      "ling_xing": {
        "code": "ling_xing",
        "labels": {
          "zh-Hant": "鈴星",
          "zh-Hans": "铃星",
          "en": "Ling Xing"
        },
        "tags": [
          "minor"
        ]
      },
      "tian_tong": {
        "code": "tian_tong",
        "labels": {
          "zh-Hant": "天同",
          "zh-Hans": "天同",
          "en": "Tian Tong"
        },
        "tags": [
          "major"
        ]
      },
      "qing_yang": {
        "code": "qing_yang",
        "labels": {
          "zh-Hant": "擎羊",
          "zh-Hans": "擎羊",
          "en": "Qing Yang"
        },
        "tags": [
          "minor"
        ]
      },
      "tuo_luo": {
        "code": "tuo_luo",
        "labels": {
          "zh-Hant": "陀羅",
          "zh-Hans": "陀罗",
          "en": "Tuo Luo"
        },
        "tags": [
          "minor"
        ]
      },
      "di_kong": {
        "code": "di_kong",
        "labels": {
          "zh-Hant": "地空",
          "zh-Hans": "地空",
          "en": "Di Kong"
        },
        "tags": [
          "misc"
        ]
      },
      "di_jie": {
        "code": "di_jie",
        "labels": {
          "zh-Hant": "地劫",
          "zh-Hans": "地劫",
          "en": "Di Jie"
        },
        "tags": [
          "misc"
        ]
      },
      "tian_kui": {
        "code": "tian_kui",
        "labels": {
          "zh-Hant": "天魁",
          "zh-Hans": "天魁",
          "en": "Tian Kui"
        },
        "tags": [
          "auxiliary"
        ]
      },
      "tian_yue": {
        "code": "tian_yue",
        "labels": {
          "zh-Hant": "天鉞",
          "zh-Hans": "天钺",
          "en": "Tian Yue"
        },
        "tags": [
          "auxiliary"
        ]
      }
    },
    "brightness": {
      "miao": {
        "code": "miao",
        "labels": {
          "zh-Hant": "廟",
          "zh-Hans": "庙",
          "en": "Exalted"
        }
      },
      "wang": {
        "code": "wang",
        "labels": {
          "zh-Hant": "旺",
          "zh-Hans": "旺",
          "en": "Prosperous"
        }
      },
      "de": {
        "code": "de",
        "labels": {
          "zh-Hant": "得",
          "zh-Hans": "得",
          "en": "Favorable"
        }
      },
      "li": {
        "code": "li",
        "labels": {
          "zh-Hant": "利",
          "zh-Hans": "利",
          "en": "Advantageous"
        }
      },
      "ping": {
        "code": "ping",
        "labels": {
          "zh-Hant": "平",
          "zh-Hans": "平",
          "en": "Neutral"
        }
      },
      "bu": {
        "code": "bu",
        "labels": {
          "zh-Hant": "不",
          "zh-Hans": "不",
          "en": "Weak"
        }
      },
      "xian": {
        "code": "xian",
        "labels": {
          "zh-Hant": "陷",
          "zh-Hans": "陷",
          "en": "Fallen"
        }
      }
    },
    "transformations": {
      "lu": {
        "code": "lu",
        "labels": {
          "zh-Hant": "祿",
          "zh-Hans": "禄",
          "en": "Lu"
        }
      },
      "quan": {
        "code": "quan",
        "labels": {
          "zh-Hant": "權",
          "zh-Hans": "权",
          "en": "Quan"
        }
      },
      "ke": {
        "code": "ke",
        "labels": {
          "zh-Hant": "科",
          "zh-Hans": "科",
          "en": "Ke"
        }
      },
      "ji": {
        "code": "ji",
        "labels": {
          "zh-Hant": "忌",
          "zh-Hans": "忌",
          "en": "Ji"
        }
      }
    },
    "markers": {
      "lin_guan": {
        "code": "lin_guan",
        "labels": {
          "zh-Hant": "臨官",
          "zh-Hans": "临官",
          "en": "Lin Guan"
        }
      },
      "qing_long": {
        "code": "qing_long",
        "labels": {
          "zh-Hant": "青龍",
          "zh-Hans": "青龙",
          "en": "Qing Long"
        }
      },
      "jiang_xing": {
        "code": "jiang_xing",
        "labels": {
          "zh-Hant": "將星",
          "zh-Hans": "将星",
          "en": "Jiang Xing"
        }
      },
      "sui_jian": {
        "code": "sui_jian",
        "labels": {
          "zh-Hant": "歲建",
          "zh-Hans": "岁建",
          "en": "Sui Jian"
        }
      }
    }
  },
  "chart": {
    "profile": {
      "yin_yang": "yang",
      "five_element_bureau": {
        "element": "water",
        "number": 2
      },
      "life_master": "qing_yang",
      "body_master": "tian_xiang",
      "ming_palace_position": 3,
      "body_palace_position": 9
    },
    "palaces": [
      {
        "position": 1,
        "palace": "siblings",
        "stem": "wu",
        "branch": "yin",
        "is_body_palace": false,
        "stars": [
          {
            "star": "tai_yang",
            "category": "major",
            "brightness": "wang"
          },
          {
            "star": "wen_chang",
            "category": "auxiliary",
            "brightness": "miao"
          }
        ],
        "markers": {
          "changsheng12": "lin_guan",
          "boshi12": "qing_long",
          "jiangqian12": "jiang_xing",
          "suiqian12": "sui_jian"
        }
      },
      {
        "position": 2,
        "palace": "spouse",
        "stem": "ji",
        "branch": "mao",
        "is_body_palace": false,
        "stars": [
          {
            "star": "wu_qu",
            "category": "major",
            "brightness": "de",
            "natal_transformation": "ke",
            "transformation_source": "self"
          },
          {
            "star": "tian_xiang",
            "category": "major",
            "brightness": "miao"
          }
        ]
      },
      {
        "position": 3,
        "palace": "life",
        "stem": "geng",
        "branch": "chen",
        "is_body_palace": false,
        "stars": [
          {
            "star": "zi_wei",
            "category": "major",
            "brightness": "wang",
            "natal_transformation": "lu",
            "transformation_source": "applied"
          },
          {
            "star": "tian_fu",
            "category": "major",
            "brightness": "miao"
          },
          {
            "star": "zuo_fu",
            "category": "auxiliary",
            "brightness": "miao"
          },
          {
            "star": "you_bi",
            "category": "auxiliary",
            "brightness": "miao"
          },
          {
            "star": "tian_kui",
            "category": "auxiliary"
          }
        ]
      },
      {
        "position": 4,
        "palace": "parents",
        "stem": "xin",
        "branch": "si",
        "is_body_palace": false,
        "stars": [
          {
            "star": "tai_yin",
            "category": "major",
            "brightness": "xian",
            "natal_transformation": "ji",
            "transformation_source": "self"
          }
        ]
      },
      {
        "position": 5,
        "palace": "fortune",
        "stem": "ren",
        "branch": "wu",
        "is_body_palace": false,
        "stars": [
          {
            "star": "tan_lang",
            "category": "major",
            "brightness": "wang"
          },
          {
            "star": "tian_ma",
            "category": "misc"
          }
        ]
      },
      {
        "position": 6,
        "palace": "property",
        "stem": "gui",
        "branch": "wei",
        "is_body_palace": false,
        "stars": [
          {
            "star": "ju_men",
            "category": "major",
            "brightness": "wang"
          },
          {
            "star": "huo_xing",
            "category": "minor"
          }
        ]
      },
      {
        "position": 7,
        "palace": "career",
        "stem": "jia",
        "branch": "shen",
        "is_body_palace": false,
        "stars": [
          {
            "star": "tian_ji",
            "category": "major",
            "brightness": "de"
          },
          {
            "star": "tian_liang",
            "category": "major",
            "brightness": "miao"
          }
        ]
      },
      {
        "position": 8,
        "palace": "friends",
        "stem": "yi",
        "branch": "you",
        "is_body_palace": false,
        "stars": [
          {
            "star": "qi_sha",
            "category": "major",
            "brightness": "wang",
            "natal_transformation": "quan",
            "transformation_source": "applied"
          }
        ]
      },
      {
        "position": 9,
        "palace": "travel",
        "stem": "bing",
        "branch": "xu",
        "is_body_palace": true,
        "stars": [
          {
            "star": "lian_zhen",
            "category": "major",
            "brightness": "ping"
          },
          {
            "star": "wen_qu",
            "category": "auxiliary",
            "brightness": "de"
          },
          {
            "star": "tian_yue",
            "category": "auxiliary"
          }
        ]
      },
      {
        "position": 10,
        "palace": "health",
        "stem": "ding",
        "branch": "hai",
        "is_body_palace": false,
        "stars": [
          {
            "star": "po_jun",
            "category": "major",
            "brightness": "de"
          },
          {
            "star": "ling_xing",
            "category": "minor"
          }
        ]
      },
      {
        "position": 11,
        "palace": "wealth",
        "stem": "wu",
        "branch": "zi",
        "is_body_palace": false,
        "stars": [
          {
            "star": "tian_tong",
            "category": "major",
            "brightness": "wang"
          },
          {
            "star": "qing_yang",
            "category": "minor"
          }
        ]
      },
      {
        "position": 12,
        "palace": "children",
        "stem": "ji",
        "branch": "chou",
        "is_body_palace": false,
        "stars": [
          {
            "star": "tuo_luo",
            "category": "minor"
          },
          {
            "star": "di_kong",
            "category": "misc"
          },
          {
            "star": "di_jie",
            "category": "misc"
          }
        ]
      }
    ]
  },
  "overlays": {
    "decade_limits": [
      {
        "age_range": [
          2,
          11
        ],
        "palace_position": 3,
        "stem": "geng",
        "transformations": [
          {
            "star": "tai_yang",
            "transformation": "lu"
          },
          {
            "star": "wu_qu",
            "transformation": "quan"
          },
          {
            "star": "tai_yin",
            "transformation": "ke"
          },
          {
            "star": "tian_tong",
            "transformation": "ji"
          }
        ]
      },
      {
        "age_range": [
          12,
          21
        ],
        "palace_position": 2,
        "stem": "ji",
        "transformations": [
          {
            "star": "wu_qu",
            "transformation": "lu"
          },
          {
            "star": "tan_lang",
            "transformation": "quan"
          },
          {
            "star": "tian_liang",
            "transformation": "ke"
          },
          {
            "star": "wen_qu",
            "transformation": "ji"
          }
        ]
      }
    ],
    "annual_charts": [
      {
        "year": 2026,
        "stem": "bing",
        "branch": "wu",
        "ming_position": 5,
        "transformations": [
          {
            "star": "tian_ji",
            "transformation": "lu"
          },
          {
            "star": "tian_liang",
            "transformation": "quan"
          },
          {
            "star": "wen_chang",
            "transformation": "ke"
          },
          {
            "star": "lian_zhen",
            "transformation": "ji"
          }
        ]
      }
    ]
  },
  "extensions": {
    "ui": {
      "preferred_label_script": "zh-Hant"
    }
  }
}
```

---

# III. Detailed explanation of the design

## 1. Top-level layout

The top-level object contains these main sections:

- `schema_version`
- `chart_type`
- `default_locale`
- `meta`
- `subject`
- `birth_data`
- `system`
- `catalog`
- `chart`
- optional `overlays`
- optional `extensions`

This division is deliberate.

### Why this layout works well
It clearly distinguishes:

- **who the chart belongs to** → `subject`
- **what input produced the chart** → `birth_data`
- **which calculation tradition and engine were used** → `system`
- **how codes are displayed** → `catalog`
- **what the natal chart contains** → `chart`
- **what time-based derived layers exist** → `overlays`

That makes the design easier to inspect, debug, document, and evolve.

---

## 2. `meta`: provenance and file-level context

The `meta` object records:

- the generating software
- the generation timestamp
- optional notes

This is useful for both technical and practical reasons.

### Why it matters
A chart file may be transmitted, cached, stored in a database, or regenerated years later. Provenance helps answer questions such as:

- Which engine produced this chart?
- When was it produced?
- Is this a demonstration file, a live production file, or a corrected export?

This field is intentionally lightweight. Provenance should exist, but it should not overwhelm the chart itself.

---

## 3. `subject` and `birth_data`: identity separated from calculation input

One of the most useful structural decisions in this design is the split between:

- `subject` → identity or record information
- `birth_data` → calculation input

### Why this split is important
A subject may be anonymized, renamed, or identified by an internal database key without changing the chart calculation. By contrast, `birth_data` is the actual input used to generate the chart.

That means software can:

- protect privacy by masking the subject name
- keep stable chart identity through `subject.id`
- still preserve the exact calculation basis in `birth_data`

### Birth data as source of truth
The `birth_data` section is the source of truth for computation. It records:

- whether the original input is `solar` or `lunar`
- year, month, and day
- leap-month status
- hour branch
- gender
- timezone
- optional solar datetime
- optional place and coordinates

This addresses several real-world failure points.

#### Calendar ambiguity
Zi Wei systems often need explicit calendar interpretation. Storing `calendar` prevents silent confusion between solar and lunar input.

#### Leap-month ambiguity
Leap month handling is one of the most common chart disputes. Requiring `is_leap_month` makes the producer declare its position explicitly.

#### Time ambiguity
Storing `hour_branch` keeps the chart faithful to Zi Wei logic, while `timezone`, optional `solar_datetime`, and optional `input_clock_time` preserve auditability.

---

## 4. `system`: doctrine, engine, and rules

The `system` object identifies how the chart was produced.

It contains:

- `family`
- `school`
- optional `engine`
- optional `rule_set`

### Why this matters
Two charts may share the same structure and still differ in meaning if they come from different schools or engines.

A good interchange format should not pretend that all Zi Wei lineages calculate every detail identically. Instead, it should make differences explicit.

### `school`
This field names the school, lineage, or computational tradition. It remains an open string because the real Zi Wei ecosystem is broader than any single enum.

### `engine`
This records the actual software or service. It is especially useful when comparing outputs between engines.

### `rule_set`
This provides a place for precise rule metadata, such as:

- brightness model
- transformation model
- palace sequencing convention
- optional registry names

This preserves flexibility without overloading the core schema.

---

## 5. `catalog`: display vocabulary separated from chart facts

The catalog is one of the central strengths of the design.

It stores code definitions for:

- stems
- branches
- palaces
- stars
- brightness levels
- transformations
- optional markers

Each catalog entry has:

- a stable `code`
- localized `labels`
- optional aliases
- optional tags
- optional notes
- optional extensions

### Why this is useful
A chart file can say:

```json
{ "star": "zi_wei", "brightness": "miao" }
```

and the display layer can resolve that through the catalog to show:

- `紫微 / 廟`
- or `Zi Wei / Exalted`

without changing the underlying chart facts.

### Why not store labels directly on every placement?
Because repeated inline labels create:

- larger payloads
- more duplication
- more translation lock-in
- more maintenance burden

The catalog approach keeps the chart compact and interoperable.

### Why this version still feels readable
Although the chart uses codes as primary values, the catalog is in the same file. That means a human can still inspect the file without needing an external dictionary.

---

## 6. `chart.profile`: summary fields for fast access

The `chart.profile` section collects the most important natal summary fields:

- `yin_yang`
- `five_element_bureau`
- `life_master`
- `body_master`
- `ming_palace_position`
- `body_palace_position`

### Why profile fields are useful
These values are often needed quickly by user interfaces, validation tools, and explanation systems. Grouping them in one place avoids forcing every consumer to recalculate or infer them from the palace array.

### Five element bureau
The design stores both:

- the element
- the bureau number

This is compact, machine-readable, and faithful to Zi Wei practice.

### Life and body positions
Global `ming_palace_position` and `body_palace_position` make the chart easy to navigate programmatically.

---

## 7. `chart.palaces`: exact 12-palace natal structure

The palace array is the heart of the natal chart.

This design requires:

- exactly 12 palaces
- ordered positions from `1` to `12`
- a fixed Zi Wei sequence starting at `Yin/寅`
- a palace code
- a stem
- a branch
- an `is_body_palace` flag
- a star list

### Why 1-based positions are used
This design uses palace positions `1` through `12` instead of `0` through `11`.

That is deliberate.

It aligns more naturally with how practitioners think about the chart and how chart diagrams are usually described, while still remaining simple for software.

### Why both global and local body references exist
The schema stores:

- `chart.profile.body_palace_position`
- `palace.is_body_palace`

This is intentionally slightly redundant.

The redundancy is helpful because:

- one field supports direct indexed lookup
- the other supports easy inspection while iterating through palaces

That improves usability without adding much complexity.

### Palace order
The array is explicitly ordered by position. A consumer does not need to sort the palaces before rendering or processing them.

---

## 8. `starPlacement`: natal placements kept simple and explicit

Each star placement records:

- the star code
- its category
- optional brightness
- optional natal transformation
- optional transformation source
- optional note
- optional extensions

### Why category is stored on the placement
Even if a star is tagged in the catalog, explicit placement-level `category` improves local readability and protects consumers from relying too heavily on a particular registry.

### Brightness
Brightness is optional because not every producer will apply brightness uniformly to all star types. The shared enum covers the common seven-level vocabulary.

### Natal transformation
The design keeps natal transformation on the natal placement itself. This is appropriate because natal transformation is a property of the natal chart.

### `transformation_source`
This small field is especially useful. It distinguishes whether a natal transformation is:

- generated by the star itself in the current context
- or applied from elsewhere

That is valuable for more advanced analysis and for avoiding ambiguity in flying-star style logic.

---

## 9. `overlays`: derived time layers separated from the natal core

Time-based layers are stored in `overlays`, not merged into every palace and star object.

The core overlay types are:

- `decade_limits`
- `annual_charts`

### Why this separation is better
The natal chart should remain stable and readable on its own. Time overlays are derived layers that can change or be expanded independently.

By separating them:

- the natal core stays simpler
- validation stays cleaner
- software can load only what it needs
- practitioners can understand the difference between permanent structure and temporary activation

### Decade limits
Each decade limit contains:

- `age_range`
- `palace_position`
- `stem`
- exactly four transformations

This gives a concise and faithful representation of a ten-year activation layer.

### Annual charts
Each annual chart contains:

- `year`
- `stem`
- `branch`
- `ming_position`
- exactly four transformations

This keeps annual overlays easy to exchange and easy to compare.

### Why overlays do not duplicate the full palace grid
A full re-expansion of every overlay into every palace would make the payload much larger and tie the standard too closely to a specific rendering model.

The chosen design stores overlay facts in a normalized form instead.

---

## 10. `extensions`: flexibility without polluting the core

Real production systems often need fields that not every consumer understands.

Examples include:

- UI hints
- cached interpretive snippets
- vendor-specific IDs
- extra markers
- school-specific computed fields

These should live in `extensions`.

### Why this matters
If every project adds custom fields directly into the core objects, interoperability degrades quickly. A dedicated extension area keeps the shared model cleaner.

A simple rule is:

> if another system can still understand the chart without the field, that field probably belongs in `extensions`

---

## 11. Why this design is simpler than a fully layered palace payload

Some designs attempt to embed natal, decade, annual, and other layers directly inside each palace and star entry.

That can be convenient for a specific front-end, but it usually creates:

- larger payloads
- more duplication
- more server-side preprocessing
- tighter coupling between the API and the rendering model

This design instead keeps:

- one clear natal structure
- separate overlay summaries
- one in-file catalog for vocabulary

That makes it a stronger interchange format.

---

## 12. Why this design is friendlier to non-technical readers than a pure code-only schema

A purely normalized schema can be hard for non-technical readers because codes alone are not visually meaningful.

This design softens that problem by including:

- an in-file catalog
- strict, chart-shaped objects
- 1-based palace positions
- explicit life and body palace references
- clearly separated overlay sections

So while the chart remains machine-first, it is still explainable in human terms.

---

# IV. Practical implementation guidance

## Recommended validation approach

Use two layers of validation.

### Layer 1: structural validation
Validate the payload against the JSON Schema.

### Layer 2: vocabulary validation
Validate that every referenced code exists in the matching catalog section.

For example:

- every palace code in `chart.palaces[*].palace` should exist in `catalog.palaces`
- every star code in `chart.palaces[*].stars[*].star` should exist in `catalog.stars`
- every brightness code should exist in `catalog.brightness`
- every transformation code should exist in `catalog.transformations`

This two-layer approach keeps the schema practical without exploding the core with hard-coded domain lists.

---

## Recommended canonical code style

Use lowercase snake_case ASCII codes such as:

- `zi_wei`
- `tian_fu`
- `life`
- `wen_chang`
- `changsheng12`

This avoids problems with:

- whitespace
- punctuation
- encoding
- translation drift
- inconsistent romanization styles

---

## Recommended registry strategy

For real-world interoperability, publish companion registries such as:

- `palace-codes.json`
- `star-codes.core.json`
- `brightness-codes.json`
- `transformation-codes.json`
- `school-codes.json`

Projects can then share the same structural schema while aligning more closely on semantics.

---

## Recommended extension policy

When adding custom data:

- keep the core chart facts unchanged
- prefer `extensions`
- document extension names clearly
- avoid mixing UI-only fields into the canonical chart

---

# V. Critical reflection

## Strengths

### 1. Strong interoperability
The chart facts are stable and machine-friendly, while the vocabulary remains localizable.

### 2. Stronger reproducibility
The birth input is explicit and auditable.

### 3. Better validation discipline
Core objects are tightly shaped, which reduces ambiguity and accidental drift.

### 4. Better natal-versus-overlay clarity
Permanent natal data and temporary cycle layers are not mixed together.

### 5. Good balance between software needs and practitioner logic
The design stays normalized enough for engineering but chart-shaped enough for human explanation.

## Limitations

### 1. Catalog indirection still exists
A human must still consult the catalog to fully read codes.

### 2. School differences are not eliminated
The schema captures structure, not total doctrinal agreement.

### 3. Some semantic validation still belongs outside JSON Schema
For example, ensuring that palace order, transformation mappings, and school-specific calculations are doctrinally valid requires engine logic or companion registries.

### 4. A single-file example is readable, but a production ecosystem is better with shared registries
The in-file catalog is useful for portability, but larger deployments may prefer registry references and slimmer payloads.

---

# VI. Recommended usage scenarios

This schema is a good fit for:

- API exchange between chart engines and front ends
- long-term storage of chart data
- document export pipelines
- bilingual chart viewers
- interpretation services
- AI-assisted explanation systems
- data migration between Zi Wei tools

---

# VII. Glossary

## Canonical code
A stable machine identifier such as `zi_wei` or `life`.

## Catalog
A map of codes to labels, aliases, and tags.

## Natal chart
The permanent chart derived from the birth input.

## Overlay
A time-based derived layer such as a decadal limit or annual chart.

## Source of truth
The exact input record used to compute the chart.

## Interchange format
A format designed to move reliably between different systems rather than being tied to one app's internal model.

---

## Final note

This schema is designed as a **shared structural language** for Zi Wei chart data.

It does not try to replace lineage knowledge, interpretation skill, or school-specific doctrine. Instead, it provides a clear, strict, and extensible container in which Zi Wei chart facts can be represented, exchanged, displayed, audited, and built upon.
