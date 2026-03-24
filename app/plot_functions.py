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


def create_bar_chart(
    df: pd.DataFrame, x_column: str, y_column: str, color_column: Optional[str] = None
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

    bar_chart = px.bar(
        df,
        x=x_column,
        y=y_column,
        hover_data=hover_data,
        color=color_column,
        color_discrete_map=color_discrete_map,
        category_orders=category_orders,
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
