import streamlit as st
import numpy as np
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
st.title("Mon Application Streamlit de modele à equations simultanées")
st.subheader("Bienvenue l'application de simulation")
st.write("Voici un exemple de texte pour expliquer ce que fait l'application: cette application vous presente l'évolution des grandes grandeurs macroéconomiques de la RCA; propose quelques simulations et un rapport d'analyse.")
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
import matplotlib.pyplot as plt
import numpy as np

# Données pour le graphique
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Créer le graphique
plt.plot(x, y)
plt.title("Graphique Sinusoidal")
plt.xlabel("x")
plt.ylabel("sin(x)")

# Afficher le graphique dans Streamlit
st.pyplot(plt)
