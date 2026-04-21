-- 合成資料無地理欄位，以 user_id 數字 mod 22 deterministic 分配縣市給 senior 使用者
WITH counties AS (
    SELECT
        county,
        (ROW_NUMBER() OVER (ORDER BY county) - 1)  AS idx
    FROM (SELECT DISTINCT county FROM {{ ref('stg_ltc_facilities') }})
),

n_counties AS (
    SELECT COUNT(*) AS n FROM counties
),

senior_users AS (
    SELECT DISTINCT user_id, user_group, age
    FROM {{ ref('stg_health_records') }}
    WHERE user_group = 'senior'
),

user_county_assigned AS (
    SELECT
        s.user_id,
        s.user_group,
        s.age,
        c.county
    FROM senior_users s
    CROSS JOIN n_counties nc
    JOIN counties c
        ON (CAST(REPLACE(s.user_id, 'U', '') AS INTEGER) - 1) % nc.n = c.idx
),

user_health_avg AS (
    SELECT
        user_id,
        ROUND(AVG(stress), 2)       AS avg_stress,
        ROUND(AVG(steps), 0)        AS avg_steps,
        ROUND(AVG(hrv), 1)          AS avg_hrv,
        ROUND(AVG(sleep_hrs), 2)    AS avg_sleep_hrs
    FROM {{ ref('stg_health_records') }}
    WHERE user_group = 'senior'
      AND NOT is_imputed
    GROUP BY user_id
),

county_ltc_stats AS (
    SELECT
        county,
        SUM(approved_beds)                          AS total_approved_beds,
        SUM(occupied_beds)                          AS total_occupied_beds,
        SUM(approved_beds - occupied_beds)          AS available_beds,
        ROUND(AVG(occupancy_rate_pct), 1)           AS avg_occupancy_rate_pct
    FROM {{ ref('stg_ltc_facilities') }}
    GROUP BY county
)

SELECT
    uca.user_id,
    uca.age,
    uca.county,
    uha.avg_stress,
    uha.avg_steps,
    uha.avg_hrv,
    uha.avg_sleep_hrs,
    cls.total_approved_beds,
    cls.available_beds,
    cls.avg_occupancy_rate_pct,
    CASE
        WHEN uha.avg_stress >= 6
         AND uha.avg_steps <= 3000
         AND cls.avg_occupancy_rate_pct >= 70
        THEN TRUE
        ELSE FALSE
    END                                             AS is_high_risk
FROM user_county_assigned uca
JOIN user_health_avg uha ON uca.user_id = uha.user_id
JOIN county_ltc_stats cls ON uca.county = cls.county
ORDER BY is_high_risk DESC, uha.avg_stress DESC
