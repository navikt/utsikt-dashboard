SELECT
    beregnet_dato,
    faggruppe_navn,
    SUM(antall_beregninger) AS antall_beregninger
FROM
    `utsikt-dev-3609.venteregister.antall_beregninger_per_faggruppe_per_beregnet_dato`
GROUP BY
    beregnet_dato,
    faggruppe_navn
ORDER BY
    beregnet_dato, faggruppe_navn ASC