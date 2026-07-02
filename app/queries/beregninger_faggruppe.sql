SELECT
    DATE_TRUNC(beregnet_dato, <TIME_RESOLUTION>) AS beregnet_dato,
    faggruppe_navn,
    SUM(antall_beregninger) AS antall_beregninger
FROM
    `<GOOGLE_CLOUD_PROJECT>.venteregister_agg.agg_beregninger_per_faggruppe_dag`
WHERE
    beregnet_dato BETWEEN @default_start_date_beregninger AND @default_end_date_beregninger
GROUP BY
    1,
    2
ORDER BY
    1 ASC, 2 ASC
