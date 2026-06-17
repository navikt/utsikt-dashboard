SELECT
    fagomrade_navn,
    fagomrade_kode,
    faggruppe_navn,
    beregnet_dato,
    ytelse,
    antall_beregninger
FROM `<GOOGLE_CLOUD_PROJECT>.venteregister_agg.agg_beregninger_p4_per_fagomrade_ytelse_dag`
