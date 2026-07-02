import streamlit as st
import pandas as pd
import datetime
import dateutil

from functions import (
    get_options_column,
    update,
    filter_dataframe_categorical_column,
    filter_dataframe_continuous_column,
    Columns,
)
from plot_functions import create_bar_chart
from data import Table


def oppdrag(oppdrag: Table):

    w1, w2, w3, w4 = st.columns(4)
    with w1:
        ytelse_options = get_options_column(
            table=oppdrag, options_column=Columns.YTELSE
        )
        select_ytelse = st.multiselect(
            "Ytelse:",
            options=ytelse_options,
            key="ytelse_selection",
            on_change=update,
            kwargs={"key": "ytelse_selection"},
        )

    with w2:
        st.selectbox(
            "Oppløsning:",
            options=["Daily", "Weekly", "Monthly", "Quarterly", "Yearly"],
            index=1,
            key="select_time_resolution_oppdrag",
        )

    with w3:
        min_value = (
            datetime.datetime.now() - dateutil.relativedelta.relativedelta(years=2)
        ).date()
        max_value = datetime.datetime.now().date()

        select_date_range_oppdrag = st.slider(
            "Fra dato og til dato:",
            min_value=min_value,
            max_value=max_value,
            value=(
                max_value - dateutil.relativedelta.relativedelta(months=2),
                max_value,
            ),
            key="date_range_oppdrag",
        )

    with w4:
        show_proportion = st.toggle(
            "Vis andel",
            value=False,
            key="oppdrag_show_proportion",
        )

    df_oppdrag = oppdrag.dataframe.copy(deep=True)

    # ------- Filter data based on user selections -------
    df_oppdrag = filter_dataframe_categorical_column(
        df=df_oppdrag,
        column=Columns.YTELSE,
        values=select_ytelse,
        date_col=Columns.DATO_OPPDRAG_LASTET,
    )

    # filter dataframe on time
    df_oppdrag = filter_dataframe_continuous_column(
        df=df_oppdrag,
        column=Columns.DATO_OPPDRAG_LASTET,
        lower_value=select_date_range_oppdrag[0],
        upper_value=select_date_range_oppdrag[1],
    )

    df_oppdrag["dato_oppdrag_lastet"] = pd.to_datetime(
        df_oppdrag["dato_oppdrag_lastet"]
    )

    # ------------------------------------------------------------------------------------------------------------------------------
    st.header("Antall oppdrag fordelt på ytelse")
    st.text("Grafen viser antall oppdrag for valgte ytelser og valgt periode.")

    df_oppdrag_ytelse = df_oppdrag.groupby(
        ["dato_oppdrag_lastet", "ytelse"],
        as_index=False,
    ).sum()

    fig_ytelse = create_bar_chart(
        df=df_oppdrag_ytelse,
        x_column=Columns.DATO_OPPDRAG_LASTET.value,
        y_column=Columns.ANTALL_OPPDRAG.value,
        color_column=Columns.YTELSE.value,
        show_proportion=show_proportion,
    )

    st.plotly_chart(fig_ytelse)

    # ------------------------------------------------------------------------------------------------------------------------------
    st.header("Antall oppdrag fordelt på kildesystem")
    st.text("Grafen viser antall oppdrag for valgte ytelser og valgt periode.")

    df_oppdrag_kildesystem = df_oppdrag.groupby(
        ["dato_oppdrag_lastet", "kildesystem"],
        as_index=False,
    ).sum()

    fig_kildesystem = create_bar_chart(
        df=df_oppdrag_kildesystem,
        x_column=Columns.DATO_OPPDRAG_LASTET.value,
        y_column=Columns.ANTALL_OPPDRAG.value,
        color_column=Columns.KILDESYSTEM.value,
        show_proportion=show_proportion,
    )

    st.plotly_chart(fig_kildesystem)
