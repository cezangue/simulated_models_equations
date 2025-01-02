import streamlit as st
import numpy as np
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

@st.cache_data()
def get_data():
    df = pd.DataFrame(
        np.random.randint(0, 100, 50).reshape(-1, 5), columns=list("ABCDE")
    )
    return df

st.title("Modélisation de l'économie centrafricaine")

st.subheader("Visualisation des dynamiques économiques")

data = get_data()

gb = GridOptionsBuilder.from_dataframe(data)
gb.configure_columns(list('ABCDE'), editable=True)
go = gb.build()

st.subheader("Tableau de données")
AgGrid(data, gridOptions=go, height=400, fit_columns_on_grid_load=True)

st.subheader("Données retournées après modification")
if 'data' in st.session_state:
    st.dataframe(st.session_state['data'])
else:
    st.write("Aucune donnée modifiée.")

st.markdown("""
Vous pouvez éditer les valeurs dans le tableau ci-dessus. Les modifications seront affichées ci-dessous.
""")