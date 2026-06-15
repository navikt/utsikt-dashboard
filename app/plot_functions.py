import pandas as pd
import plotly.express as px
from typing import Optional

color_map_faggruppe = {
    "Pensjoner": "#a6cee3",
    "Barnetrygd": "#1f78b4",
    "Arbeidsytelser": "#b2df8a",
    "Inntektsytelser": "#33a02c",
    "Refusjon Arbeidsgiver": "#fb9a99",
    "Grunn og hjelpestønad": "#e31a1c",
    "Korttidsytelser": "#fdbf6f",
    "Kreditoroppgjør": "#ff7f00",
    "Tilbakekreving": "#cab2d6",
    "Interne trekk til TI": "#6a3d9a",
}

color_map_ventestatus = {
    "AVVM": "#8dd3c7",
    "AVVE": "#ffffb3",
    "AVRK": "#bebada",
    "RETU": "#fb8072",
    "AVAV": "#80b1d3",
    "ADDR": "#fdb462",
    "AVAG": "#b3de69",
    "ANRE": "#fccde5",
    "EONK": "#d9d9d9",
    "OVUR": "#bc80bd",
}


def _get_chart_dataframe(
    df: pd.DataFrame, x_column: str, y_column: str, show_proportion: bool
) -> pd.DataFrame:
    df_chart = df.copy(deep=True)

    if not show_proportion:
        return df_chart

    totals = df_chart.groupby(x_column)[y_column].transform("sum")
    df_chart["andel"] = df_chart[y_column].div(totals.where(totals != 0, 1))

    return df_chart


def create_bar_chart(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    color_column: Optional[str] = None,
    show_proportion: bool = False,
):
    if color_column == "faggruppe_navn":
        color_discrete_map = color_map_faggruppe
        category_orders = {"faggruppe_navn": list(color_map_faggruppe.keys())}
        hover_data = None

    elif color_column == "ventestatus_kode":
        color_discrete_map = color_map_ventestatus
        category_orders = {"ventestatus_kode": list(color_map_ventestatus.keys())}
        hover_data = ["ventestatus_beskrivelse"]

    else:
        color_discrete_map = None
        category_orders = None
        hover_data = None

    df_chart = _get_chart_dataframe(
        df=df,
        x_column=x_column,
        y_column=y_column,
        show_proportion=show_proportion,
    )

    chart_y_column = "andel" if show_proportion else y_column

    bar_chart = px.bar(
        df_chart,
        x=x_column,
        y=chart_y_column,
        hover_data=hover_data,
        color=color_column,
        color_discrete_map=color_discrete_map,
        category_orders=category_orders,
    )

    bar_chart.update_yaxes(
        title_text="Andel" if show_proportion else y_column,
        tickformat=".0%" if show_proportion else None,
    )

    return bar_chart


def create_pie_chart(
    df: pd.DataFrame, names_column: str, values_column: str, title: str
):
    if names_column == "faggruppe_navn":
        color_discrete_map = color_map_faggruppe
        category_orders = {"faggruppe_navn": list(color_map_faggruppe.keys())}
        hover_data = None

    elif names_column == "ventestatus_kode":
        color_discrete_map = color_map_ventestatus
        category_orders = {"ventestatus_kode": list(color_map_ventestatus.keys())}
        hover_data = ["ventestatus_beskrivelse"]

    else:
        color_discrete_map = None
        category_orders = None
        hover_data = None

    pie_chart = px.pie(
        df,
        names=names_column,
        color=names_column,
        values=values_column,
        hover_data=hover_data,
        color_discrete_map=color_discrete_map,
        category_orders=category_orders,
        title=title,
    )
    return pie_chart
