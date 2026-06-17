import streamlit as st
import os

from data import Table
from bq_connector import BigQueryConnector

from tabs.om_dataen import om_dataen
from tabs.oppdrag import oppdrag
from tabs.ventestatus_manuell import ventestatus_manuell
from tabs.beregninger import beregninger
from tabs.p4 import p4

st.set_page_config(layout="wide")


google_project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "utsikt-dev-3609")


@st.cache_data(ttl=24 * 3600)
def fetch_tables(current_google_project_id: str) -> dict[str, Table]:
    bq_connector = BigQueryConnector()

    oppdrag = Table(
        path_to_query="queries/oppdrag.sql", google_project_id=current_google_project_id
    )

    beregninger_faggruppe = Table(
        path_to_query="queries/beregninger_faggruppe.sql",
        google_project_id=current_google_project_id,
    )
    beregninger_fagomrade = Table(
        path_to_query="queries/beregninger_fagomrade.sql",
        google_project_id=current_google_project_id,
    )

    beregninger_manuell_ventestatuser = Table(
        path_to_query="queries/beregninger_manuell_ventestatuser.sql",
        google_project_id=current_google_project_id,
    )

    beregninger_p4 = Table(
        path_to_query="queries/beregninger_p4.sql",
        google_project_id=current_google_project_id,
    )

    oppdrag.fetch_data(bq_connector=bq_connector)
    beregninger_faggruppe.fetch_data(bq_connector=bq_connector)
    beregninger_fagomrade.fetch_data(bq_connector=bq_connector)
    beregninger_manuell_ventestatuser.fetch_data(bq_connector=bq_connector)
    beregninger_p4.fetch_data(bq_connector=bq_connector)

    fetched_tables = {
        "oppdrag": oppdrag,
        "beregninger_faggruppe": beregninger_faggruppe,
        "beregninger_fagomrade": beregninger_fagomrade,
        "beregninger_manuell_ventestatuser": beregninger_manuell_ventestatuser,
        "beregninger_p4": beregninger_p4,
    }

    return fetched_tables


tables = fetch_tables(current_google_project_id=google_project_id)

if "faggruppe_selection" not in st.session_state:
    st.session_state["faggruppe_selection"] = ["Alle"]

if "fagomrade_selection" not in st.session_state:
    st.session_state["fagomrade_selection"] = ["Alle"]

if "ventestatus_selection" not in st.session_state:
    st.session_state["ventestatus_selection"] = ["Alle"]


tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Oppdrag", "Beregninger", "Ventestatus manuell", "P4", "Om dataen"]
)

with tab1:
    oppdrag(tables["oppdrag"])

with tab2:
    beregninger(tables)

with tab3:
    ventestatus_manuell(tables["beregninger_manuell_ventestatuser"])

with tab4:
    p4(tables["beregninger_p4"])

with tab5:
    om_dataen()
