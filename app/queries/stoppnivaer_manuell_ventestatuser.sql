SELECT
    status_avsluttet_dato,
    ventestatus_kode,
    SUM(antall_stoppnivaer) as antall_stoppnivaer
FROM
    `utsikt-dev-3609.venteregister.agg_stoppnivaer_manuell_ventestatus_per_ventestatus_varighet_fagomrade_dag`
WHERE
    status_avsluttet_dato is not NULL
GROUP BY
    status_avsluttet_dato, ventestatus_kode


