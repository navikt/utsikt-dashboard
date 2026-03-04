SELECT
    status_avsluttet_dato,
    ventestatus_kode,
    SUM(antall_beregninger) AS antall_beregninger
FROM
    `utsikt-dev-3609.venteregister.agg_beregninger_manuell_ventestatus_per_ventestatus_varighet_fagomrade_dag`
WHERE
    status_avsluttet_dato IS NOT NULL
GROUP BY
    status_avsluttet_dato, ventestatus_kode
