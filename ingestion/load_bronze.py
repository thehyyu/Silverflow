"""
把 data/bronze/ 的 CSV 載入 DuckDB，建立 Bronze raw tables。
可單獨重跑，每次 CREATE OR REPLACE 確保冪等。
"""

from pathlib import Path
import duckdb

DB = Path(__file__).parent.parent / "silverflow.duckdb"
BRONZE = Path(__file__).parent.parent / "data" / "bronze"

con = duckdb.connect(str(DB))

sources = [
    ("raw_health_records", BRONZE / "health_records.csv"),
    ("raw_ltc_facilities", BRONZE / "ltc_facilities.csv"),
]

for table, csv_path in sources:
    con.execute(f"""
        CREATE OR REPLACE TABLE {table} AS
        SELECT * FROM read_csv_auto(?)
    """, [str(csv_path)])
    count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"✓ {table}：{count} 筆")

con.close()
