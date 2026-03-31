import streamlit as st
import altair as alt
import pandas as pd
import datetime
import dateutil

from functions import (
    get_options_column,
    filter_dataframe_categorical_column,
    filter_dataframe_continuous_column,
    Columns,
    update,
    TimeResolution,
    TimeRelative,
)
from plot_functions import create_bar_chart


def beregninger(data):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        faggruppe_options = get_options_column(
            table=data.faggruppe, options_column=Columns.FAGGRUPPE
        )
        select_faggrupe = st.multiselect(
            "Faggruppe:",
            options=faggruppe_options,
            key="faggruppe_selection",
            on_change=update,
            kwargs={"key": "faggruppe_selection"},
        )

    with col2:
        fagomrade_options = get_options_column(
            table=data.fagomrade,
            options_column=Columns.FAGOMRADE,
            filter_column=Columns.FAGGRUPPE,
            filter_values=select_faggrupe,
        )

        select_fagomrade = st.multiselect(
            "Fagomrade:",
            options=fagomrade_options,
            key="fagomrade_selection",
            on_change=update,
            kwargs={"key": "fagomrade_selection"},
        )

    with col3:
        select_time_resolution = st.selectbox(
            "Oppløsning:", options=TimeResolution.options(), index=0
        )

    with col4:
        min_value = (
            datetime.datetime.now() - dateutil.relativedelta.relativedelta(years=2)
        ).date()
        max_value = datetime.datetime.now().date()

        select_date_range = st.slider(
            "Fra dato og til dato:",
            min_value=min_value,
            max_value=max_value,
            value=(min_value, max_value),
        )

    df_faggruppe = data.faggruppe.data.copy(deep=True)
    df_fagomrade = data.fagomrade.data.copy(deep=True)


    df_faggruppe = filter_dataframe_categorical_column(df=df_faggruppe,
                                                       column=Columns.FAGGRUPPE,
                                                       select_values=select_faggrupe)

    df_fagomrade = filter_dataframe_categorical_column(df=df_fagomrade,
                                                       column=Columns.FAGGRUPPE,
                                                       select_values=select_fagomrade)

    # st.table(df_faggruppe)

    # Filter dataframe on column
    if len(select_faggrupe) > 0 and "Alle" not in select_faggrupe:
        df_fagomrade = df_fagomrade[
            df_fagomrade[Columns.FAGGRUPPE.value].isin(select_faggrupe)
        ]

    if len(select_fagomrade) > 0 and "Alle" not in select_fagomrade:
        df_fagomrade = df_fagomrade[
            df_fagomrade[Columns.FAGOMRADE.value].isin(select_fagomrade)
        ]


    # filter dataframe on time
    df_faggruppe = filter_dataframe_continuous_column(df=df_faggruppe,
                                                      column=Columns.BEREGNET_DATO,
                                                      lower_value=select_date_range[0],
                                                      upper_value=select_date_range[1])


    df_fagomrade = filter_dataframe_continuous_column(df=df_fagomrade,
                                                      column=Columns.BEREGNET_DATO,
                                                      lower_value=select_date_range[0],
                                                      upper_value=select_date_range[1])

    df_faggruppe = df_faggruppe[
        (df_faggruppe[Columns.BEREGNET_DATO.value] >= select_date_range[0])
        & (df_faggruppe[Columns.BEREGNET_DATO.value] <= select_date_range[1])
    ]
    df_fagomrade = df_fagomrade[
        (df_fagomrade[Columns.BEREGNET_DATO.value] >= select_date_range[0])
        & (df_fagomrade[Columns.BEREGNET_DATO.value] <= select_date_range[1])
    ]

    df_faggruppe["beregnet_dato"] = pd.to_datetime(df_faggruppe["beregnet_dato"])
    frequency = TimeResolution[select_time_resolution.upper()].value
    df_faggruppe = df_faggruppe.groupby(
        [
            pd.Grouper(key="beregnet_dato", freq=frequency),
            pd.Grouper(key="faggruppe_navn"),
        ]
    ).sum()
    df_faggruppe = df_faggruppe.sort_values(
        by=["beregnet_dato"], ascending=True
    ).reset_index()

    # df_faggruppe["D"] =  df_faggruppe["beregnet_dato"].apply(lambda x: x.isocalendar().week)
    df_faggruppe["WS"] = df_faggruppe["beregnet_dato"].apply(
        lambda x: x.isocalendar().week
    )
    # df_faggruppe["MS"]
    # df_faggruppe["QS"]
    # df_faggruppe["YS"]
    with st.expander("Tabell"):
        st.table(df_faggruppe)

    # ------------------------------------------------------------------------------------------------------------------------------
    st.header("Antall beregning per dag fordelt på faggrupper")
    st.text("Grafen viser antall beregninger for valgte faggrupper og valgt periode.")

    fig_faggruppe = create_bar_chart(
        df=df_faggruppe,
        x_column=Columns.BEREGNET_DATO.value,
        y_column=Columns.ANTALL_BEREGNINGER.value,
        color_column=Columns.FAGGRUPPE.value,
    )

    st.plotly_chart(fig_faggruppe)

    # ------------------------------------------------------------------------------------------------------------------------------
    st.header("Antall beregning per dag fordelt på fagområder")
    st.text(
        "Grafen viser antall beregninger for valgte faggrupper, valgte fagområder og valgt periode."
    )

    fig_fagomrade = create_bar_chart(
        df=df_fagomrade,
        x_column=Columns.BEREGNET_DATO.value,
        y_column=Columns.ANTALL_BEREGNINGER.value,
        color_column=Columns.FAGOMRADE.value,
    )

    st.plotly_chart(fig_fagomrade, width="stretch")
