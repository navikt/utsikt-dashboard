SELECT
  beregnet_dato,
  ventestatus_beskrivelse,
  handteres_manuelt_flagg,
  SUM(antall_beregninger) AS antall_beregninger
FROM
    `utsikt-dev-3609.venteregister.antall_beregninger_per_ventestatus_per_beregnet_dato`
WHERE
    beregnet_dato IS NOT NULL
GROUP BY
    beregnet_dato,
    ventestatus_beskrivelse,
    handteres_manuelt_flagg
ORDER BY beregnet_dato, ventestatus_beskrivelse, handteres_manuelt_flagg asc