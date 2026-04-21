"""
生成合成長照機構資料，結構對應衛福部長照機構清單欄位。
因政府開放資料 API 有存取限制，改用合成資料模擬相同結構。
"""

import csv
import random
from pathlib import Path

random.seed(123)

OUTPUT = Path(__file__).parent.parent / "data" / "bronze" / "ltc_facilities.csv"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

FIELDS = ["facility_id", "facility_name", "county", "district", "facility_type",
          "approved_beds", "occupied_beds", "address", "phone"]

# 台灣 22 縣市，附帶 65+ 人口比例（影響長照需求）
COUNTIES = [
    ("臺北市",   270),  # 核定床數權重（人口規模）
    ("新北市",   380),
    ("桃園市",   210),
    ("臺中市",   260),
    ("臺南市",   180),
    ("高雄市",   280),
    ("基隆市",    60),
    ("新竹市",    55),
    ("新竹縣",    80),
    ("苗栗縣",    70),
    ("彰化縣",   130),
    ("南投縣",    60),
    ("雲林縣",    80),
    ("嘉義市",    45),
    ("嘉義縣",    70),
    ("屏東縣",    90),
    ("宜蘭縣",    55),
    ("花蓮縣",    50),
    ("臺東縣",    40),
    ("澎湖縣",    20),
    ("金門縣",    15),
    ("連江縣",     5),
]

FACILITY_TYPES = ["居家式", "社區式", "機構式"]

DISTRICTS = {
    "臺北市": ["中正區", "大安區", "信義區", "松山區", "內湖區", "士林區", "北投區", "萬華區"],
    "新北市": ["板橋區", "三重區", "中和區", "永和區", "新莊區", "新店區", "土城區", "淡水區"],
    "臺中市": ["西屯區", "北屯區", "南屯區", "豐原區", "大里區", "太平區", "清水區", "梧棲區"],
    "高雄市": ["三民區", "鳳山區", "左營區", "楠梓區", "前鎮區", "苓雅區", "小港區", "鼓山區"],
}
DEFAULT_DISTRICTS = ["第一區", "第二區", "第三區", "市區", "鄉區"]

def get_district(county):
    return random.choice(DISTRICTS.get(county, DEFAULT_DISTRICTS))

rows = []
fid = 1
for county, weight in COUNTIES:
    count = max(5, weight // 10)
    for _ in range(count):
        ftype = random.choice(FACILITY_TYPES)
        approved = random.randint(20, 150) if ftype == "機構式" else random.randint(5, 40)
        occupied = int(approved * random.uniform(0.6, 0.98))
        rows.append({
            "facility_id": f"LTC{fid:04d}",
            "facility_name": f"{county}{get_district(county)}{ftype}長照機構{fid:03d}",
            "county": county,
            "district": get_district(county),
            "facility_type": ftype,
            "approved_beds": approved,
            "occupied_beds": occupied,
            "address": f"{county}{get_district(county)}範例路{random.randint(1,999)}號",
            "phone": f"0{random.randint(2,8)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}",
        })
        fid += 1

with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(rows)

print(f"✓ 長照機構資料：{len(rows)} 筆，涵蓋 {len(COUNTIES)} 縣市：{OUTPUT}")
