WITH weekly AS (
    SELECT
        user_id,
        user_group,
        age,
        DATE_TRUNC('week', date)        AS week_start,
        ROUND(AVG(sleep_hrs), 2)        AS avg_sleep_hrs,
        ROUND(AVG(hrv), 1)              AS avg_hrv,
        ROUND(AVG(steps), 0)            AS avg_steps,
        ROUND(AVG(stress), 2)           AS avg_stress,
        COUNT(*)                        AS days_recorded
    FROM {{ ref('stg_health_records') }}
    WHERE NOT is_imputed
    GROUP BY user_id, user_group, age, DATE_TRUNC('week', date)
)

SELECT * FROM weekly
ORDER BY user_group, user_id, week_start
