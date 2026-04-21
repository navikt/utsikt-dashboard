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

    beregninger_faggruppe = data["beregninger_faggruppe"]
    beregninger_fagomrade = data["beregninger_fagomrade"]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        faggruppe_options = get_options_column(
            table=beregninger_faggruppe, options_column=Columns.FAGGRUPPE
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
            table=beregninger_fagomrade,
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

    df_beregninger_faggruppe = beregninger_faggruppe.dataframe.copy(deep=True)
    df_beregninger_fagomrade = beregninger_fagomrade.dataframe.copy(deep=True)


    df_beregninger_faggruppe = filter_dataframe_categorical_column(df=df_beregninger_faggruppe,
                                                       column=Columns.FAGGRUPPE,
                                                       values=select_faggrupe)

    df_beregninger_fagomrade = filter_dataframe_categorical_column(df=df_beregninger_fagomrade,
                                                       column=Columns.FAGGRUPPE,
                                                       values=select_fagomrade)

    # st.table(df_faggruppe)
    # filter dataframe on time
    df_beregninger_faggruppe = filter_dataframe_continuous_column(df=df_beregninger_faggruppe,
                                                      column=Columns.BEREGNET_DATO,
                                                      lower_value=select_date_range[0],
                                                      upper_value=select_date_range[1])


    df_beregninger_fagomrade = filter_dataframe_continuous_column(df=df_beregninger_fagomrade,
                                                      column=Columns.BEREGNET_DATO,
                                                      lower_value=select_date_range[0],
                                                      upper_value=select_date_range[1])


    df_beregninger_faggruppe["beregnet_dato"] = pd.to_datetime(df_beregninger_faggruppe["beregnet_dato"])
    frequency = TimeResolution[select_time_resolution.upper()].value
    df_beregninger_faggruppe = df_beregninger_faggruppe.groupby(
        [
            pd.Grouper(key="beregnet_dato", freq=frequency),
            pd.Grouper(key="faggruppe_navn"),
        ]
    ).sum()
    df_beregninger_faggruppe = df_beregninger_faggruppe.sort_values(
        by=["beregnet_dato"], ascending=True
    ).reset_index()

    # df_faggruppe["D"] =  df_faggruppe["beregnet_dato"].apply(lambda x: x.isocalendar().week)
    df_beregninger_faggruppe["WS"] = df_beregninger_faggruppe["beregnet_dato"].apply(
        lambda x: x.isocalendar().week
    )
    # df_faggruppe["MS"]
    # df_faggruppe["QS"]
    # df_faggruppe["YS"]
    with st.expander("Tabell"):
        st.table(df_beregninger_faggruppe)

    # ------------------------------------------------------------------------------------------------------------------------------
    st.header("Antall beregning per dag fordelt på faggrupper")
    st.text("Grafen viser antall beregninger for valgte faggrupper og valgt periode.")

    fig_faggruppe = create_bar_chart(
        df=df_beregninger_faggruppe,
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
        df=df_beregninger_fagomrade,
        x_column=Columns.BEREGNET_DATO.value,
        y_column=Columns.ANTALL_BEREGNINGER.value,
        color_column=Columns.FAGOMRADE.value,
    )

    st.plotly_chart(fig_fagomrade, width="stretch")
