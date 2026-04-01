import streamlit as st
import pandas as pd

from enum import Enum
from typing import Any
from data import Table


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
    ANTALL_BEREGNINGER = "antall_beregninger"




def filter_dataframe_categorical_column(df: pd.DataFrame, column: Columns, values: list[str]) -> pd.DataFrame:
    if len(values) > 0 and "Alle" not in values:
        df = (
            df[df[column.value].isin(values)]
            .sort_values(by=Columns.BEREGNET_DATO.value, ascending=True)
            .reset_index(drop=True))

    return df


def filter_dataframe_continuous_column(df: pd.DataFrame, column: Columns, lower_value: Any, upper_value: Any ) -> pd.DataFrame:
    df = df[(df[column.value] >= lower_value) & (df[column.value] <= upper_value)]
    return df



def get_options_column(
    table: Table,
    options_column: Columns,
    filter_column: Columns = None,
    filter_values: list[str] = None,
) -> list[str]:
    if filter_values and filter_column:
        df = filter_dataframe_categorical_column(df=table.dataframe, column=filter_column, values=filter_values)
    else:
        df = table.dataframe

    options = df[options_column.value].unique().tolist()
    options = [o for o in options if o is not None]

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
