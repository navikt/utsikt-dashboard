import streamlit as st
import altair as alt
import plotly.express as px
import pandas as pd
import datetime
import dateutil

from functions import (
    get_options_column,
    Columns,
    update,
    TimeResolution,
    TimeRelative,
)


def ventestatus_manuell(beregninger_manuell_ventestatuser):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        ventestatus_options = get_options_column(
            table=beregninger_manuell_ventestatuser,
            options_column=Columns.VENTESTATUS_BESKRIVELSE,
        )
        select_ventestatus = st.multiselect(
            "Ventestatus:",
            options=ventestatus_options,
            key="ventestatus_selection",
            on_change=update,
            kwargs={"key": "ventestatus_selection"},
        )

    with col2:
        faggruppe_options = get_options_column(
            table=beregninger_manuell_ventestatuser, options_column=Columns.FAGGRUPPE
        )
        select_faggruppe = st.multiselect(
            label="Faggruppe:",
            options=faggruppe_options,
            key="faggruppe_selection2",
            on_change=update,
            kwargs={"key": "faggruppe_selection2"},
        )

    with col3:
        select_time_resolution = st.selectbox(
            "Oppløsning:",
            options=TimeResolution.options(),
            index=0,
            key="select_time_resolution",
        )

    with col4:
        min_value = (
            datetime.datetime.now() - dateutil.relativedelta.relativedelta(days=720)
        ).date()
        max_value = datetime.datetime.now().date()

        select_time_relative = st.selectbox(
            "Periode:", options=TimeRelative.options(), index=0
        )

    df_beregninger_manuell_ventestatuser = beregninger_manuell_ventestatuser.data.copy(
        deep=True
    )

    df_beregninger_manuell_ventestatuser = df_beregninger_manuell_ventestatuser[
        (
            (df_beregninger_manuell_ventestatuser["status_avsluttet_dato"] >= min_value)
            & (
                df_beregninger_manuell_ventestatuser["status_avsluttet_dato"]
                <= max_value
            )
        )
        | (df_beregninger_manuell_ventestatuser["status_avsluttet_dato"].isnull())
    ]

    if len(select_ventestatus) > 0 and "Alle" not in select_ventestatus:
        df_beregninger_manuell_ventestatuser = df_beregninger_manuell_ventestatuser[
            df_beregninger_manuell_ventestatuser[
                Columns.VENTESTATUS_BESKRIVELSE.value
            ].isin(select_ventestatus)
        ]

    if len(select_faggruppe) > 0 and "Alle" not in select_faggruppe:
        df_beregninger_manuell_ventestatuser = df_beregninger_manuell_ventestatuser[
            df_beregninger_manuell_ventestatuser[Columns.FAGGRUPPE.value].isin(
                select_faggruppe
            )
        ]

    # -------
    st.header("Antall beregninger manuelt behandlet per status")
    st.text(
        "Grafen viser antall beregninger for valgte ventestatus, manuell håndering og valgt periode."
    )
    st.markdown(f"minimum dato: {min_value}, max dato: {max_value}")
    # st.table(
    #     df_beregninger_manuell_ventestatuser[
    #         df_beregninger_manuell_ventestatuser.gjeldende_flagg == 0
    #     ].head()
    # )

    df_til_bar_chart = (
        df_beregninger_manuell_ventestatuser[
            df_beregninger_manuell_ventestatuser.gjeldende_flagg == 0
        ]
        .groupby(["status_avsluttet_dato", "ventestatus_beskrivelse"])[
            "antall_beregninger"
        ]
        .sum()
        .reset_index()
    )

    st.table(df_til_bar_chart.head())

    fig_bar = px.bar(
        df_til_bar_chart,
        x="status_avsluttet_dato",
        y="antall_beregninger",
        color="ventestatus_beskrivelse",
    )

    st.plotly_chart(fig_bar)

    df_til_pie = df_beregninger_manuell_ventestatuser[
        df_beregninger_manuell_ventestatuser.gjeldende_flagg == 1
    ]

    fig_pie = px.pie(
        df_til_pie,
        values="antall_beregninger",
        names="ventestatus_kode",
        title=f"Antall åpne bergninger: {len(df_til_pie)}",
    )

    st.header("Antall manuelle beregninger per ventestatus")
    st.plotly_chart(fig_pie)
