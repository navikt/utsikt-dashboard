import streamlit as st
import pandas as pd
from enum import Enum
from data import Table


class TimeResolution(Enum):
    DAILY = "D"
    WEEKLY = "W"
    MONTHLY = "M"
    QUARTERLY = "Q"
    YEARLY = "Y"

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
    options = [o for o in options if o is not None]

    options.sort()
    options.insert(0, "Alle")

    return options


def aggregate_by_time_resolution(
    df: pd.DataFrame,
    date_column: str,
    time_resolution: str,
    group_columns: list[str],
    agg_column: str,
    agg_func: str = "sum",
) -> pd.DataFrame:
    df_copy = df.copy()
    df_copy[date_column] = pd.to_datetime(df_copy[date_column])

    time_resolution_value = TimeResolution[time_resolution.upper()].value

    df_copy["period"] = df_copy[date_column].dt.to_period(time_resolution_value)

    group_cols = ["period"] + group_columns
    result = df_copy.groupby(group_cols)[agg_column].agg(agg_func).reset_index()
    result["period"] = result["period"].astype(str)

    return result


def update(key):
    selection = st.session_state[key]
    if len(selection) > 0:
        if "Alle" == selection[-1]:
            st.session_state[key] = ["Alle"]

        if "Alle" in selection and selection[-1] != "Alle":
            st.session_state[key] = [
                value for value in st.session_state[key] if value != "Alle"
            ]
