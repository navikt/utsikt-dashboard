SELECT
    DATE_TRUNC(dato_oppdrag_lastet, <TIME_RESOLUTION>) AS dato_oppdrag_lastet,
    ytelse,
    kildesystem,
    SUM(antall_oppdrag) AS antall_oppdrag
FROM `<GOOGLE_CLOUD_PROJECT>.venteregister_agg.agg_oppdrag_per_ytelse_kilde_dag`
WHERE dato_oppdrag_lastet BETWEEN @default_start_date AND @default_end_date
GROUP BY 1, 2, 3
ORDER BY 1
