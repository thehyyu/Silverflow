"""
從內政部統計處下載 113年（2024）各縣市單一年齡別人口，
計算 65 歲以上總人口，存到 data/bronze/population.csv。

資料來源：
  內政部統計處 人口數單一年齡組─按性別、區域別分
  https://data.gov.tw/dataset/14226
"""

import csv
import urllib.request
from pathlib import Path

OUTPUT = Path(__file__).parent.parent / "data" / "bronze" / "population.csv"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

URL = (
    "https://statis.moi.gov.tw/micst/webMain.aspx"
    "?sys=220&kind=21&type=1&funid=c0110203&cycle=41"
    "&outmode=12&utf=1&compmode=0&outkind=3"
    "&fldspc=0,103,&codspc0=0,2,3,2,6,1,9,1,12,1,15,16,"
    "&codlst1=111&ym=11312&ymt=11312"
)

SENIOR_AGE_COLS = [f"{age}歲" for age in range(65, 100)] + ["100歲以上"]


def fetch_raw() -> list[list[str]]:
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read().decode("utf-8-sig", errors="replace")
    return list(csv.reader(raw.splitlines()))


def parse(rows: list[list[str]]) -> list[dict]:
    headers = rows[0]

    # 找出 65+ 欄位的 index（年份總計列沒有「_統計」後綴，直接用欄名）
    col_idx = {h: i for i, h in enumerate(headers)}

    records = []
    for row in rows[1:]:
        key = row[0].strip() if row else ""
        # 只取「113年/ {縣市}/ 性別總計」，排除「113年 12月/」月資料和總計
        if not (key.startswith("113年/") and key.endswith("/ 性別總計")):
            continue
        county = key.split("/")[1].strip()
        if county == "區域別總計":
            continue

        total_pop = int(row[col_idx["總計"]].replace(",", "") or 0)
        senior_pop = sum(
            int(row[col_idx[col]].replace(",", "") or 0)
            for col in SENIOR_AGE_COLS
            if col in col_idx
        )
        records.append(
            {
                "county": county,
                "year": 2024,
                "total_population": total_pop,
                "senior_population_65plus": senior_pop,
            }
        )
    return records


def main() -> None:
    print("downloading population data from 內政部統計處…")
    rows = fetch_raw()
    records = parse(rows)
    print(f"  parsed {len(records)} counties")

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["county", "year", "total_population", "senior_population_65plus"],
        )
        writer.writeheader()
        writer.writerows(records)

    print(f"  saved → {OUTPUT}")
    for r in records:
        print(f"    {r['county']}: 65+ = {r['senior_population_65plus']:,}")


if __name__ == "__main__":
    main()
