SELECT
    beregnet_dato,
    faggruppe_navn,
    fagomrade_navn,
    SUM(antall_beregninger) AS antall_beregninger
FROM
    `utsikt-dev-3609.venteregister_agg.agg_beregninger_per_fagomrade_dag`
GROUP BY
    beregnet_dato,
    faggruppe_navn,
    fagomrade_navn
ORDER BY
    beregnet_dato ASC, faggruppe_navn ASC, faggruppe_navn ASC
