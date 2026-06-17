import streamlit as st
import pandas as pd
import datetime
import dateutil

from functions import (
    get_options_column,
    TimeResolution,
    update,
    filter_dataframe_categorical_column,
    filter_dataframe_continuous_column,
    Columns,
)
from plot_functions import create_bar_chart
from data import Table


def p4(p4: Table):

    w1, w2, w3, w4 = st.columns(4)
    with w1:
        ytelse_options = get_options_column(table=p4, options_column=Columns.YTELSE)
        select_ytelse = st.multiselect(
            "Ytelse:",
            options=ytelse_options,
            key="ytelse_selection_p4",
            on_change=update,
            kwargs={"key": "ytelse_selection_p4"},
        )

    with w2:
        select_time_resolution_p4 = st.selectbox(
            "Oppløsning:",
            options=TimeResolution.options(),
            index=1,  # default to weekly
            key="select_time_resolution_p4",
        )

    with w3:
        min_value = (
            datetime.datetime.now() - dateutil.relativedelta.relativedelta(years=2)
        ).date()
        max_value = datetime.datetime.now().date()

        select_date_range_p4 = st.slider(
            "Fra dato og til dato:",
            min_value=min_value,
            max_value=max_value,
            value=(
                max_value - dateutil.relativedelta.relativedelta(months=2),
                max_value,
            ),
            key="date_range_p4",
        )

    with w4:
        show_proportion = st.toggle(
            "Vis andel",
            value=False,
            key="p4_show_proportion",
        )

    df_p4 = p4.dataframe.copy(deep=True)

    # ------- Filter data based on user selections -------
    df_p4 = filter_dataframe_categorical_column(
        df=df_p4,
        column=Columns.YTELSE,
        values=select_ytelse,
        date_col=Columns.BEREGNET_DATO,
    )

    # filter dataframe on time
    df_p4 = filter_dataframe_continuous_column(
        df=df_p4,
        column=Columns.BEREGNET_DATO,
        lower_value=select_date_range_p4[0],
        upper_value=select_date_range_p4[1],
    )

    df_p4["beregnet_dato"] = pd.to_datetime(df_p4["beregnet_dato"])

    frequency = TimeResolution[select_time_resolution_p4.upper()].value

    # ------------------------------------------------------------------------------------------------------------------------------
    st.header("Antall beregninger fordelt på ytelse")
    st.text("Grafen viser antall beregninger for valgte ytelser og valgt periode.")

    df_p4_ytelse = df_p4.groupby(
        [
            pd.Grouper(key="beregnet_dato", freq=frequency),
            pd.Grouper(key="ytelse"),
        ],
        as_index=False,
    ).sum()

    fig_ytelse = create_bar_chart(
        df=df_p4_ytelse,
        x_column=Columns.BEREGNET_DATO.value,
        y_column=Columns.ANTALL_BEREGNINGER.value,
        color_column=Columns.YTELSE.value,
        show_proportion=show_proportion,
    )

    st.plotly_chart(fig_ytelse)

    # ------------------------------------------------------------------------------------------------------------------------------
    st.header("Antall beregninger fordelt på fagområde")
    st.text("Grafen viser antall beregninger for valgte ytelser og valgt periode.")

    df_p4_fagomrade = df_p4.groupby(
        [
            pd.Grouper(key="beregnet_dato", freq=frequency),
            pd.Grouper(key="fagomrade_kode"),
        ],
        as_index=False,
    ).sum()

    fig_fagomrade = create_bar_chart(
        df=df_p4_fagomrade,
        x_column=Columns.BEREGNET_DATO.value,
        y_column=Columns.ANTALL_BEREGNINGER.value,
        color_column=Columns.FAGOMRADE_KODE.value,
        show_proportion=show_proportion,
    )

    st.plotly_chart(fig_fagomrade)
