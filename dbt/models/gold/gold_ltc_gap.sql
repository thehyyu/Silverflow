WITH county_summary AS (
    SELECT
        county,
        COUNT(*)                                        AS facility_count,
        SUM(approved_beds)                              AS total_approved_beds,
        SUM(occupied_beds)                              AS total_occupied_beds,
        SUM(approved_beds - occupied_beds)              AS available_beds,
        ROUND(AVG(occupancy_rate_pct), 1)               AS avg_occupancy_rate_pct
    FROM {{ ref('stg_ltc_facilities') }}
    GROUP BY county
),

population AS (
    SELECT county, senior_population_65plus
    FROM raw_population
)

SELECT
    cs.county,
    cs.facility_count,
    cs.total_approved_beds,
    cs.total_occupied_beds,
    cs.available_beds,
    cs.avg_occupancy_rate_pct,
    ROUND(
        CAST(cs.available_beds AS DOUBLE) / NULLIF(cs.total_approved_beds, 0) * 100,
        1
    )                                                   AS available_rate_pct,
    p.senior_population_65plus,
    -- 每千位 65+ 長照核准床位數（越低表示缺口越大）
    ROUND(
        CAST(cs.total_approved_beds AS DOUBLE) / NULLIF(p.senior_population_65plus, 0) * 1000,
        2
    )                                                   AS beds_per_1000_seniors
FROM county_summary cs
LEFT JOIN population p ON cs.county = p.county
ORDER BY beds_per_1000_seniors ASC
