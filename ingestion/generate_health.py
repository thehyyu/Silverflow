"""
生成 5 筆假健康紀錄，存到 data/bronze/health_records.csv。
Branch 0.5 曳光彈用，只驗證 pipeline 可通。
"""

import csv
import random
from datetime import date
from pathlib import Path

from faker import Faker

fake = Faker("zh_TW")
random.seed(42)

OUTPUT = Path(__file__).parent.parent / "data" / "bronze" / "health_records.csv"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

FIELDS = ["user_id", "date", "age", "sleep_hrs", "hrv", "steps", "stress"]

rows = []
for i in range(1, 6):
    rows.append({
        "user_id": f"U{i:03d}",
        "date": date(2024, 1, i).isoformat(),
        "age": random.randint(25, 80),
        "sleep_hrs": round(random.uniform(4.0, 9.0), 1),
        "hrv": random.randint(20, 80),
        "steps": random.randint(1000, 15000),
        "stress": random.randint(1, 10),
    })

with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(rows)

print(f"✓ 產出 {len(rows)} 筆資料：{OUTPUT}")
