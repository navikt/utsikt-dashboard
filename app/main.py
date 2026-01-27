import streamlit as st

from dotenv import load_dotenv

from data import Table, Data
from bq_connector import BigQueryConnector
st.set_page_config(layout="wide")

load_dotenv("app/.env")

bq_connector = BigQueryConnector()

faggruppe = Table(path_to_query="app/queries/faggruppe.sql")
fagomrade = Table(path_to_query="app/queries/fagomrade.sql")
ventestatus = Table(path_to_query="app/queries/ventestatus.sql")


data = Data(faggruppe=faggruppe, fagomrade=fagomrade, ventestatus=ventestatus)
data.reload_data(bq_connector=bq_connector)

st.text(f"{data.fagomrade.data.shape}")

tab1, tab2 = st.tabs(["Faggruppe", "Ventestatus"])

with tab1:
    col1, col2, col3, col4= st.columns(4)
    with col1:
        faggruppe = st.multiselect("Faggruppe:", ["Alle", "test"], default="Alle")

    with col2:
        fagomrade = st.multiselect("Fagomrade:", ["Alle", "test"], default="Alle")

    with col3:
        oppløsning = st.selectbox("Oppløsning:", ["Alle", "test"], index=0)

    with col4:
        fra_dato = st.slider("Fra dato og til dato:", min_value=0, max_value=100, value=(10,100))



with tab2:
    st.text("Faggruppe")
