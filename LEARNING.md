# SilverFlow 學習筆記

> 這個專案的核心精神是**做中學**。每個工具第一次出現時，這裡會記錄「它是什麼、為什麼用它、用完後的體會」。

---

## 學習目標

| 工具 / 概念 | 學習狀態 | 對標企業場景 |
|---|---|---|
| `uv` — Python 套件管理 | 未開始 | 任何 Python 專案的標準工具鏈 |
| `pyproject.toml` — 專案設定總表 | 未開始 | 替代 requirements.txt 的現代標準 |
| `DuckDB` — 本地資料倉儲 | 未開始 | 對標 BigQuery / Snowflake |
| `dbt Core` — 資料轉換與建模 | 未開始 | 業界標準 ELT 工具 |
| Medallion 架構（Bronze/Silver/Gold） | 未開始 | Databricks / Delta Lake 架構模式 |
| `dbt tests` — 資料品質測試 | 未開始 | 對標 Monte Carlo、Soda |
| `Faker` — 合成資料生成 | 未開始 | 企業測試資料策略 |
| `Datasette` — 輕量資料瀏覽 | 未開始 | 對標 Tableau / Power BI（輕量版） |

---

## uv

**它是什麼：** Rust 寫的 Python 套件管理工具，速度比 pip 快 10–100 倍。  
**為什麼用它：** 一個指令同時管虛擬環境 + 套件 + lock file，取代 pip + venv 兩個工具。  
**核心指令：**

```bash
uv venv            # 建立 .venv 虛擬環境
uv add <套件>      # 安裝套件（寫入 pyproject.toml + 更新 lock file）
uv sync            # 根據 lock file 還原所有依賴（換電腦時用）
uv run <指令>      # 在 .venv 環境內執行，不需要 activate
```

**學習後的體會：**  
_（跑完 Branch 0 後填寫）_

---

## pyproject.toml

**它是什麼：** Python 專案的設定總表，一個檔案管套件依賴、專案名稱、Python 版本需求。  
**為什麼用它：** 現代 Python 標準（PEP 518/621），取代 `requirements.txt` + `setup.py` 的組合。  
**基本結構：**

```toml
[project]
name = "silverflow"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "duckdb",
    "dbt-duckdb",
    ...
]
```

**學習後的體會：**  
_（填寫）_

---

## DuckDB

**它是什麼：** 嵌入式分析型資料庫，像 SQLite 一樣零設定，但專為 OLAP（分析查詢）設計。  
**為什麼用它：** 本地模擬 BigQuery 的 ELT 模式，完全免費、不需要雲端帳號。  
**關鍵概念：** 支援直接查詢 Parquet / CSV 檔案，與 dbt 深度整合。

**學習後的體會：**  
_（填寫）_

---

## dbt Core

**它是什麼：** 資料轉換工具，用 SQL + Jinja 模板定義資料模型，管理 Bronze → Silver → Gold 的轉換邏輯。  
**為什麼用它：** 把 SQL 變成有版本控制、可測試、有文件的「程式碼」，這是現代 DE 的核心技能。  
**核心概念：**

| 概念 | 說明 |
|---|---|
| model | 一個 `.sql` 檔案 = 一張資料表或 view |
| `ref()` | 引用其他 model，dbt 自動處理執行順序 |
| test | 資料品質驗證（not_null、unique 等） |
| `dbt run` | 執行所有 model |
| `dbt test` | 執行所有 tests |

**學習後的體會：**  
_（填寫）_

---

## Medallion 架構

**它是什麼：** 把資料倉儲分成三層的架構模式，每層有明確的責任。  

```
Bronze  → 原始資料落地，完全不動，保留原貌
Silver  → 清理、標準化、型態轉換
Gold    → 業務邏輯聚合，分析師直接使用的層
```

**為什麼用它：** 資料可追溯（任何問題都能回到 Bronze 查），與 Databricks、Delta Lake 業界實踐一致。

**學習後的體會：**  
_（填寫）_

---

## 面試故事（持續更新）

> 每完成一個 Branch，用一段話更新這裡，練習用面試語言描述自己做了什麼。

**Branch 0 完成後：**  
_（填寫）_

**Branch 1 完成後：**  
_（填寫）_

**完整故事（Branch 4 完成後）：**  
「從政府開放資料與合成健康資料出發，設計 Medallion 三層架構（Bronze / Silver / Gold），用 dbt 做資料建模與品質測試，本地用 DuckDB 模擬大型資料倉儲的 ELT 模式。」
