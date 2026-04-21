WITH source AS (
    SELECT * FROM raw_ltc_facilities
),

standardized AS (
    SELECT
        facility_id,
        facility_name,
        -- 統一縣市名稱（移除可能的空白、舊式寫法）
        TRIM(county)                            AS county,
        TRIM(district)                          AS district,
        TRIM(facility_type)                     AS facility_type,
        CAST(approved_beds AS INTEGER)          AS approved_beds,
        CAST(occupied_beds AS INTEGER)          AS occupied_beds,
        -- 計算使用率
        ROUND(
            CAST(occupied_beds AS DOUBLE) / NULLIF(approved_beds, 0) * 100,
            1
        )                                       AS occupancy_rate_pct,
        address,
        phone
    FROM source
    WHERE approved_beds > 0
)

SELECT * FROM standardized
