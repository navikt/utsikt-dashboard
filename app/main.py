import streamlit as st

from dotenv import load_dotenv

from data import Table
from bq_connector import BigQueryConnector

from tabs.om_dataen import om_dataen
from tabs.oppdrag import oppdrag
from tabs.ventestatus_manuell import ventestatus_manuell
from tabs.beregninger import beregninger

st.set_page_config(layout="wide")

# load_dotenv("app/.env")


@st.cache_data(ttl=24 * 3600)
def fetch_tables() -> dict[str, Table]:
    bq_connector = BigQueryConnector()

    oppdrag = Table(path_to_query="queries/oppdrag.sql")
    beregninger_faggruppe = Table(path_to_query="queries/beregninger_faggruppe.sql")
    beregninger_fagomrade = Table(path_to_query="queries/beregninger_fagomrade.sql")
    beregninger_manuell_ventestatuser = Table(
        path_to_query="queries/beregninger_manuell_ventestatuser.sql"
    )

    oppdrag.fetch_data(bq_connector=bq_connector)
    beregninger_faggruppe.fetch_data(bq_connector=bq_connector)
    beregninger_fagomrade.fetch_data(bq_connector=bq_connector)
    beregninger_manuell_ventestatuser.fetch_data(bq_connector=bq_connector)

    fetched_tables = {
        "oppdrag": oppdrag,
        "beregninger_faggruppe": beregninger_faggruppe,
        "beregninger_fagomrade": beregninger_fagomrade,
        "beregninger_manuell_ventestatuser": beregninger_manuell_ventestatuser,
    }

    return fetched_tables


tables = fetch_tables()

if "faggruppe_selection" not in st.session_state:
    st.session_state["faggruppe_selection"] = ["Alle"]

if "fagomrade_selection" not in st.session_state:
    st.session_state["fagomrade_selection"] = ["Alle"]

if "ventestatus_selection" not in st.session_state:
    st.session_state["ventestatus_selection"] = ["Alle"]


tab1, tab2, tab3, tab4 = st.tabs(
    ["Oppdrag", "Beregninger", "Ventestatus manuell", "Om dataen"]
)

with tab1:
    oppdrag(tables["oppdrag"])

with tab2:
    beregninger(tables)

with tab3:
    ventestatus_manuell(tables["beregninger_manuell_ventestatuser"])

with tab4:
    om_dataen()
