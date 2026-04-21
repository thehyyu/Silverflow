SELECT
    user_id,
    CAST(date AS DATE)          AS date,
    CAST(age AS INTEGER)        AS age,
    CAST(sleep_hrs AS DOUBLE)   AS sleep_hrs,
    CAST(hrv AS INTEGER)        AS hrv,
    CAST(steps AS INTEGER)      AS steps,
    CAST(stress AS INTEGER)     AS stress
FROM raw_health_records
WHERE sleep_hrs >= 0
  AND sleep_hrs <= 24
  AND hrv >= 0
