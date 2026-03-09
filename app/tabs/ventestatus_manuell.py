import streamlit as st
import altair as alt
from functions import (
    get_options_column,
    Columns,
    update,
    TimeResolution,
    TimeRelative,
)


def ventestatus_manuell(data):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        ventestatus_options = get_options_column(
            table=data.ventestatus, options_column=Columns.VENTESTATUS_BESKRIVELSE
        )
        select_ventestatus = st.multiselect(
            "Ventestatus:",
            options=ventestatus_options,
            key="ventestatus_selection",
            on_change=update,
            kwargs={"key": "ventestatus_selection"},
        )

    with col2:
        manuelt_options = ["Alle", "Ja", "Nei"]
        select_manuelt = col2.multiselect(
            label="Håndteres manuelt:",
            options=manuelt_options,
            key="manuelt_selection",
            on_change=update,
            kwargs={"key": "manuelt_selection"},
        )

    with col3:
        select_time_resolution = st.selectbox(
            "Oppløsning:",
            options=TimeResolution.options(),
            index=0,
            key="select_time_resolution",
        )

    with col4:
        select_time_relative = st.selectbox(
            "Periode:", options=TimeRelative.options(), index=0
        )

    df_ventestatus = data.ventestatus.data.copy(deep=True)

    if len(select_ventestatus) > 0 and "Alle" not in select_ventestatus:
        df_ventestatus = df_ventestatus[
            df_ventestatus[Columns.VENTESTATUS_BESKRIVELSE.value].isin(
                select_ventestatus
            )
        ]

    if len(select_manuelt) > 0 and "Alle" not in select_manuelt:
        select_manuelt_int = []
        if "Ja" in select_manuelt:
            select_manuelt_int.append(1)
        if "Nei" in select_manuelt:
            select_manuelt_int.append(0)

        df_ventestatus = df_ventestatus[
            df_ventestatus[Columns.MANUELT.value].isin(select_manuelt_int)
        ]

    # ------------------------------------------------------------------------------------------------------------------------------
    st.header("Antall beregning per dag fordelt på ventestatus")
    st.text(
        "Grafen viser antall beregninger for valgte ventestatus, manuell håndering og valgt periode."
    )
    fig_ventestatus = (
        alt.Chart(data=df_ventestatus)
        .mark_bar()
        .encode(
            x=alt.X(Columns.BEREGNET_DATO.value, title="Beregnet dato"),
            y=alt.Y(Columns.ANTALL_BEREGNINGER.value, title="Antall beregninger"),
            color=alt.Color(
                Columns.VENTESTATUS_BESKRIVELSE.value,
                legend=alt.Legend(
                    orient="right",
                    direction="vertical",
                    title="Ventestatus",
                    labelLimit=300,
                ),
            ),
        )
    )

    st.altair_chart(fig_ventestatus, width="stretch")
    # st.table(df_ventestatus)
