"""
生成 100 位虛擬使用者 × 90 天健康紀錄，存到 data/bronze/health_records.csv。
三個族群各有不同統計分布，確保 Gold 層分析有意義的差異。
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

OUTPUT = Path(__file__).parent.parent / "data" / "bronze" / "health_records.csv"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

START_DATE = date(2024, 1, 1)
DAYS = 90
FIELDS = ["user_id", "date", "age", "group", "sleep_hrs", "hrv", "steps", "stress"]

# 族群設定：(group_name, 人數, 年齡範圍, HRV範圍, 睡眠範圍, 步數範圍, 壓力範圍)
GROUPS = [
    ("senior",  40, (65, 85), (20, 50), (5.0, 8.0), (1000,  6000), (3, 7)),
    ("midage",  35, (40, 64), (35, 65), (5.5, 7.5), (3000,  10000), (5, 10)),
    ("healthy", 25, (20, 39), (50, 80), (6.5, 9.0), (5000,  15000), (1, 5)),
]

def jitter(value, ratio=0.1):
    """加入小幅隨機擾動，讓資料不要太規律。"""
    return value * (1 + random.uniform(-ratio, ratio))

rows = []
uid = 1

for group_name, count, age_range, hrv_range, sleep_range, steps_range, stress_range in GROUPS:
    for _ in range(count):
        user_id = f"U{uid:03d}"
        age = random.randint(*age_range)
        base_hrv = random.uniform(*hrv_range)
        base_sleep = random.uniform(*sleep_range)
        base_steps = random.randint(*steps_range)
        base_stress = random.uniform(*stress_range)

        for day in range(DAYS):
            record_date = START_DATE + timedelta(days=day)
            rows.append({
                "user_id": user_id,
                "date": record_date.isoformat(),
                "age": age,
                "group": group_name,
                "sleep_hrs": round(max(0, min(24, jitter(base_sleep))), 1),
                "hrv": max(1, int(jitter(base_hrv))),
                "steps": max(0, int(jitter(base_steps))),
                "stress": max(1, min(10, round(jitter(base_stress)))),
            })
        uid += 1

with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(rows)

total_users = uid - 1
print(f"✓ {total_users} 位使用者 × {DAYS} 天 = {len(rows)} 筆資料：{OUTPUT}")
print(f"  senior {40} 人 / midage {35} 人 / healthy {25} 人")
