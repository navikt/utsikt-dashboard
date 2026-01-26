import streamlit as st

st.set_page_config(layout="wide")




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
