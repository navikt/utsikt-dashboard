import streamlit as st
import datetime
import dateutil

from functions import (
    get_options_column,
    Columns,
    update,
    TimeResolution,
    TimeRelative,
)

from plot_functions import create_bar_chart, create_pie_chart


def ventestatus_manuell(beregninger_manuell_ventestatuser):
    # Row 1: 4 widgets
    w1, w2, w3, w4 = st.columns(4)

    with w1:
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

    with w2:
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

    with w3:
        st.selectbox(
            "Oppløsning:",
            options=TimeResolution.options(),
            index=0,
            key="select_time_resolution",
        )

    with w4:
        min_value = (
            datetime.datetime.now() - dateutil.relativedelta.relativedelta(days=720)
        ).date()
        max_value = datetime.datetime.now().date()

        st.selectbox("Periode:", options=TimeRelative.options(), index=0)

    df_beregninger_manuell_ventestatuser = beregninger_manuell_ventestatuser.data.copy(
        deep=True
    )

    # ------- Filter data based on user selections -------
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

    # ------- Create bar chart and pie chart -------
    st.header("Antall beregninger manuelt behandlet per status")
    st.text(
        "Grafen viser antall beregninger for valgte ventestatus, manuell håndering og valgt periode."
    )
    st.markdown(f"minimum dato: {min_value}, max dato: {max_value}")

    df_til_bar_chart = (
        df_beregninger_manuell_ventestatuser[
            df_beregninger_manuell_ventestatuser.gjeldende_flagg == 0
        ]
        .groupby(
            ["status_avsluttet_dato", "ventestatus_kode", "ventestatus_beskrivelse"]
        )["antall_beregninger"]
        .sum()
        .reset_index()
    )

    fig_bar = create_bar_chart(
        df=df_til_bar_chart,
        x_column="status_avsluttet_dato",
        y_column="antall_beregninger",
        color_column="ventestatus_kode",
    )

    st.plotly_chart(fig_bar)
    # Row 3: 2 charts
    pie1, pie2 = st.columns(2)
    df_til_pie = df_beregninger_manuell_ventestatuser[
        df_beregninger_manuell_ventestatuser.gjeldende_flagg == 1
    ]

    fig_pie = create_pie_chart(
        df=df_til_pie,
        names_column="ventestatus_kode",
        values_column="antall_beregninger",
        title=f"Antall åpne beregninger {len(df_til_pie)}",
    )

    fig_pie2 = create_pie_chart(
        df=df_til_pie,
        names_column="faggruppe_navn",
        values_column="antall_beregninger",
        title=f"Antall åpne beregninger {len(df_til_pie)}",
    )

    with pie1:
        st.header("Antall manuelle beregninger per ventestatus")
        st.plotly_chart(fig_pie)

    with pie2:
        st.header("Antall manuelle beregninger per faggruppe")
        st.plotly_chart(fig_pie2)
