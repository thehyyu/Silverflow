WITH source AS (
    SELECT * FROM raw_health_records
),

-- 補齊每位使用者應有的完整 90 天日期
date_spine AS (
    SELECT DISTINCT user_id FROM source
),

all_dates AS (
    SELECT CAST(range AS DATE) AS date
    FROM range(DATE '2024-01-01', DATE '2024-01-01' + INTERVAL 90 DAY, INTERVAL 1 DAY)
),

full_grid AS (
    SELECT d.user_id, a.date
    FROM date_spine d
    CROSS JOIN all_dates a
),

joined AS (
    SELECT
        g.user_id,
        g.date,
        s.age,
        s."group",
        s.sleep_hrs,
        s.hrv,
        s.steps,
        s.stress
    FROM full_grid g
    LEFT JOIN source s
        ON g.user_id = s.user_id
        AND CAST(s.date AS DATE) = g.date
),

cleaned AS (
    SELECT
        user_id,
        date,
        CAST(age AS INTEGER)                            AS age,
        CAST("group" AS VARCHAR)                        AS user_group,
        CAST(sleep_hrs AS DOUBLE)                       AS sleep_hrs,
        CAST(hrv AS INTEGER)                            AS hrv,
        CAST(steps AS INTEGER)                          AS steps,
        CAST(stress AS INTEGER)                         AS stress,
        CASE WHEN sleep_hrs IS NULL THEN TRUE ELSE FALSE END AS is_imputed
    FROM joined
    -- 過濾異常值（非補值的紀錄才驗）
    WHERE (sleep_hrs IS NULL OR (sleep_hrs >= 0 AND sleep_hrs <= 24))
      AND (hrv IS NULL OR hrv >= 0)
)

SELECT * FROM cleaned
