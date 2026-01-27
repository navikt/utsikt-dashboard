SELECT
    beregnet_dato,
    faggruppe_navn,
    fagomrade_navn,
    SUM(antall_beregninger) AS antall_beregninger
FROM
    `utsikt-dev-3609.venteregister.antall_beregninger_per_fagomrade_per_beregnet_dato`
GROUP BY
    beregnet_dato,
    faggruppe_navn,
    fagomrade_navn
ORDER BY
    beregnet_dato, faggruppe_navn, faggruppe_navn ASC