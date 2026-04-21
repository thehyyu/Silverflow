"""
把 data/bronze/ 的 CSV 載入 DuckDB，建立 Bronze raw tables。
"""

from pathlib import Path
import duckdb

DB = Path(__file__).parent.parent / "silverflow.duckdb"
BRONZE = Path(__file__).parent.parent / "data" / "bronze"

con = duckdb.connect(str(DB))

con.execute("""
    CREATE OR REPLACE TABLE raw_health_records AS
    SELECT * FROM read_csv_auto(?)
""", [str(BRONZE / "health_records.csv")])

count = con.execute("SELECT COUNT(*) FROM raw_health_records").fetchone()[0]
print(f"✓ raw_health_records：{count} 筆")
print(con.execute("SELECT * FROM raw_health_records LIMIT 3").df())

con.close()
