"""
把 DuckDB 所有 table 匯出成 SQLite，供 Datasette 瀏覽用。
"""

import sqlite3
from pathlib import Path
import duckdb

ROOT = Path(__file__).parent.parent
DUCK_DB = ROOT / "silverflow.duckdb"
SQLITE_DB = ROOT / "silverflow_view.sqlite"

duck = duckdb.connect(str(DUCK_DB))
lite = sqlite3.connect(str(SQLITE_DB))

tables = [r[0] for r in duck.execute(
    "SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'"
).fetchall()]

for table in tables:
    df = duck.execute(f"SELECT * FROM {table}").df()
    df.to_sql(table, lite, if_exists="replace", index=False)
    print(f"✓ {table}：{len(df)} 筆")

duck.close()
lite.close()
print(f"\n→ 開啟方式：uv run datasette {SQLITE_DB.name}")
