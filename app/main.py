import streamlit as st

from dotenv import load_dotenv

from data import Table, Data
from bq_connector import BigQueryConnector

from tabs.om_dataen import om_dataen
from tabs.ventestatus_manuell import ventestatus_manuell
from tabs.beregninger import beregninger

st.set_page_config(layout="wide")

# load_dotenv("app/.env")


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


data = fetch_data()

if "faggruppe_selection" not in st.session_state:
    st.session_state["faggruppe_selection"] = ["Alle"]

if "fagomrade_selection" not in st.session_state:
    st.session_state["fagomrade_selection"] = ["Alle"]

if "ventestatus_selection" not in st.session_state:
    st.session_state["ventestatus_selection"] = ["Alle"]


tab1, tab2, tab4 = st.tabs(["Beregninger", "Ventestatus manuell", "Om dataen"])

with tab1:
    beregninger(data)

with tab2:
    ventestatus_manuell(data.beregninger_manuell_ventestatuser)

with tab4:
    om_dataen()
