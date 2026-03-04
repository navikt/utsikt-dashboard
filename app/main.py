import datetime
from datetime import timedelta

import dateutil

import streamlit as st
import pandas as pd
import altair as alt

from dotenv import load_dotenv
from enum import Enum


from data import Table, Data
from bq_connector import BigQueryConnector


st.set_page_config(layout="wide")

load_dotenv("app/.env")


@st.cache_data(ttl=24 * 3600)
def fetch_data() -> Data:
    bq_connector = BigQueryConnector()
    faggruppe = Table(path_to_query="queries/faggruppe.sql")
    fagomrade = Table(path_to_query="queries/fagomrade.sql")
    ventestatus = Table(path_to_query="queries/ventestatus.sql")
    beregninger_manuell_ventestatuser = Table(
        path_to_query="queries/beregninger_manuell_ventestatuser.sql"
    )

    fetched_data = Data(
        faggruppe=faggruppe,
        fagomrade=fagomrade,
        ventestatus=ventestatus,
        beregninger_manuell_ventestatuser=beregninger_manuell_ventestatuser,
    )
    fetched_data.reload_data(bq_connector=bq_connector)

    return fetched_data


class TimeResolution(Enum):
    DAILY = "D"
    WEEKLY = "W"
    MONTHLY = "MS"
    QUARTERLY = "QS"
    YEARLY = "YS"

    @classmethod
    def options(cls):
        return [option.name.capitalize() for option in cls]


class TimeRelative(Enum):
    LAST_DAY = "LAST_DAY"
    LAST_WEEK = "LAST_WEEK"
    LAST_MONTH = "LAST_MONTH"
    LAST_TERTIARY = "LAST_TERTIARY"
    LAST_YEAR = "LAST_YEAR"

    @classmethod
    def options(cls):
        return [option.value.capitalize() for option in cls]


class Columns(Enum):
    FAGGRUPPE = "faggruppe_navn"
    FAGOMRADE = "fagomrade_navn"
    VENTESTATUS = "ventestatus_navn"
    BEREGNET_DATO = "beregnet_dato"
    VENTESTATUS_BESKRIVELSE = "ventestatus_beskrivelse"
    MANUELT = "handteres_manuelt_flagg"
    ANTALL_BEREGNINGER = "antall_beregninger"


data = fetch_data()


def filter_on_column(table: Table, column: Columns, values: list[str]) -> pd.DataFrame:
    df = (
        table.data[table.data[column.value].isin(values)]
        .sort_values(by=Columns.BEREGNET_DATO.value, ascending=True)
        .reset_index(drop=True)
    )
    return df


def get_options_column(
    table: Table,
    options_column: Columns,
    filter_column: Columns = None,
    filter_values: list[str] = None,
) -> list[str]:
    if filter_values and filter_column:
        df = filter_on_column(table=table, column=filter_column, values=filter_values)
    else:
        df = table.data

    options = df[options_column.value].unique().tolist()
    options.sort()
    options.insert(0, "Alle")

    return options


def update(key):
    selection = st.session_state[key]
    if len(selection) > 0:
        if "Alle" == selection[-1]:
            st.session_state[key] = ["Alle"]

        if "Alle" in selection and selection[-1] != "Alle":
            st.session_state[key] = [
                value for value in st.session_state[key] if value != "Alle"
            ]


if "faggruppe_selection" not in st.session_state:
    st.session_state["faggruppe_selection"] = ["Alle"]

if "fagomrade_selection" not in st.session_state:
    st.session_state["fagomrade_selection"] = ["Alle"]

if "ventestatus_selection" not in st.session_state:
    st.session_state["ventestatus_selection"] = ["Alle"]

if "manuelt_selection" not in st.session_state:
    st.session_state["manuelt_selection"] = ["Alle"]

tab1, tab2, tab3, tab4 = st.tabs(["Faggruppe", "Ventestatus", "Stoppnivå", "Om dataen"])

with tab1:
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

    if len(select_faggrupe) > 0 and "Alle" not in select_faggrupe:
        df_faggruppe = df_faggruppe[
            df_faggruppe[Columns.FAGGRUPPE.value].isin(select_faggrupe)
        ]

    # st.table(df_faggruppe)

    if len(select_faggrupe) > 0 and "Alle" not in select_faggrupe:
        df_fagomrade = df_fagomrade[
            df_fagomrade[Columns.FAGGRUPPE.value].isin(select_faggrupe)
        ]

    if len(select_fagomrade) > 0 and "Alle" not in select_fagomrade:
        df_fagomrade = df_fagomrade[
            df_fagomrade[Columns.FAGOMRADE.value].isin(select_fagomrade)
        ]

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

    fig_faggruppe = (
        alt.Chart(data=df_faggruppe)
        .mark_bar()
        .encode(
            x=alt.X(Columns.BEREGNET_DATO.value, title="Beregnet dato"),
            y=alt.Y(Columns.ANTALL_BEREGNINGER.value, title="Antall beregninger"),
            color=alt.Color(
                Columns.FAGGRUPPE.value,
                legend=alt.Legend(
                    orient="right",
                    direction="vertical",
                    title="Ventestatus",
                    labelLimit=300,
                ),
            ),
        )
    )

    st.altair_chart(fig_faggruppe, width="stretch")

    # ------------------------------------------------------------------------------------------------------------------------------
    st.header("Antall beregning per dag fordelt på fagområder")
    st.text(
        "Grafen viser antall beregninger for valgte faggrupper, valgte fagområder og valgt periode."
    )

    fig_fagomrade = (
        alt.Chart(data=df_fagomrade)
        .mark_bar()
        .encode(
            x=alt.X(Columns.BEREGNET_DATO.value, title="Beregnet dato"),
            y=alt.Y(Columns.ANTALL_BEREGNINGER.value, title="Antall beregninger"),
            color=alt.Color(
                Columns.FAGOMRADE.value,
                legend=alt.Legend(
                    orient="right",
                    direction="vertical",
                    title="Ventestatus",
                    labelLimit=300,
                ),
            ),
        )
    )

    st.altair_chart(fig_fagomrade, width="stretch")


with tab2:
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


with tab3:

    st.header("Antall stoppnivåer som er manuelt behandlet og er avsluttet")
    df_stoppnivaer_manuell = data.beregninger_manuell_ventestatuser.data.copy(deep=True)

    df_stoppnivaer_manuell["uke"] = df_stoppnivaer_manuell[
        "status_avsluttet_dato"
    ].apply(lambda x: x - timedelta(days=x.weekday()))
    df_stoppnivaer_manuell = df_stoppnivaer_manuell[
        ["ventestatus_kode", "uke", "antall_beregninger"]
    ]
    df_stoppnivaer_manuell = (
        df_stoppnivaer_manuell.groupby(by=["ventestatus_kode", "uke"])
        .sum()
        .reset_index()
    )
    df_stoppnivaer_manuell = df_stoppnivaer_manuell.sort_values(
        by="uke", ascending=True
    ).reset_index(drop=True)

    fig_ventestatus_manuell = (
        alt.Chart(data=df_stoppnivaer_manuell)
        .mark_bar()
        .encode(
            x=alt.X("uke", title="Uke"),
            y=alt.Y("antall_beregninger", title="Antall stoppnivaer"),
            color=alt.Color(
                "ventestatus_kode",
                legend=alt.Legend(
                    orient="right",
                    direction="vertical",
                    title="Ventestatus",
                    labelLimit=300,
                ),
            ),
        )
    )

    st.altair_chart(fig_ventestatus_manuell, width="stretch")

with tab4:
    st.header("Om dataen")
    st.markdown(
        """Datagrunnlaget for visualiseringene er hentet fra Oppdragssystemet  og omhandler beregninger.

En beregning starter som et utbetalingsoppdrag fra fagssystem.  Etterhvert som Oppdragssystemet jobber med beregningen, vil beregningen brytes ned i mindre deler og være innom ulike steg. 


#### Stoppnivå
 Stoppnivå er et begrep i Oppdragssystemet som brukes for nedbryting av beregninger. En beregning kan brytes ned i f.eks. perioder med tilhørende forfallsdato gjelde forskjellige mottakere eller kan gjelde ulike saker f.eks sykepenger til én bruker men gjelder flere forhold.

#### Ventestatus
 Ventestatus er  status for stoppnivået,  altså hvor i beregningsløpet et stoppnivå er.  F.eks. et stoppnivå kan ha ventestatusen OVFO (for 'Overført til UR').

#### Faggruppe
 En faggruppe består av flere fagområder hvor man ønsker en samlet felles skatt-og trekkberegning. F.eks. pensjonsrelaterte ytelser. 

#### Fagområde
Fagområde angir selve ytelsen f.eks. arbeidsavklaringspenger. 
"""
    )
