import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.stats.diagnostic import breaks_cusumolsresid
from statsmodels.tsa.api import VAR
import networkx as nx

def set_background(image_url, opacity=0.3, color="#000000"):
    """Fonction pour définir l'image de fond."""
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: {color};
            opacity: {opacity};
            z-index: -1;
        }}
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp p, .stApp label, .stApp .streamlit-expanderHeader {{
            color: yellow !important;
            font-size: 16px !important;
            font-family: sans-serif !important;
        }}
        .dataframe {{
            background-color: rgba(255, 255, 255, 0.7) !important;
            color: green !important;
            font-size: 14px !important;
            border-collapse: collapse !important;
            width: 100% !important;
            margin-bottom: 1em !important;
        }}
        .dataframe th, .dataframe td {{
            border: 1px solid #ddd !important;
            padding: 8px !important;
            text-align: left !important;
        }}
        .dataframe th {{
            background-color: #f2f2f2 !important;
            font-weight: bold !important;
        }}
        .stSuccess {{
            color: lightgreen !important;
        }}
        .stWarning {{
            color: orange !important;
        }}
        .stError {{
            color: red !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def test_adf(series):
    try:
        result = adfuller(series)
        return result[1]
    except Exception as e:
        st.error(f"Erreur test ADF : {e}")
        return None

def test_kpss(series):
    try:
        statistic, p_value, lags, critical_values = kpss(series, regression='c')
        return p_value
    except Exception as e:
        st.error(f"Erreur test KPSS : {e}")
        return None

def plot_time_series(df, selected_columns):
    """Trace les séries temporelles des colonnes sélectionnées."""
    plt.figure(figsize=(12, 6))
    for column in selected_columns:
        plt.plot(df['Annee'], df[column], marker='o', label=column)
    plt.title("Évolution des Variables Choisies", fontsize=16, color="green")
    plt.xlabel("Année")
    plt.ylabel("Valeur")
    plt.grid()
    plt.legend()
    st.pyplot(plt)

def main():
    st.set_page_config(page_title="Visualisation des Données", page_icon="")
    background_url = "https://raw.githubusercontent.com/Ndobo1997/Projet-MES/main/image_analyse_donnees.jpg"
    set_background(background_url, opacity=0.3, color="#000000")

    try:
        # Charger la base de données depuis l'URL
        df = pd.read_excel("https://raw.githubusercontent.com/cezangue/simulated_models_equations/main/base_mes_taf.xlsx")
        excluded_columns = ['Annee']
        if not all(col in df.columns for col in excluded_columns):
            missing_cols = [col for col in excluded_columns if col not in df.columns]
            st.error(f"Colonnes manquantes : {missing_cols}")
            return

        columns_to_choose = df.columns[~df.columns.isin(excluded_columns)]

        # Première partie (Tests de séries temporelles)
        st.subheader("Tests de Séries Temporelles")
        column = st.selectbox("Variable à tester :", columns_to_choose)
        start_year = st.selectbox("Année de début :", df['Annee'].unique())
        end_year = st.selectbox("Année de fin :", df['Annee'].unique(), index=len(df['Annee'].unique()) - 1)
        filtered_df = df[(df['Annee'] >= start_year) & (df['Annee'] <= end_year)].copy()

        try:
            log = ["Banque centrale - Taux directeur","Inflation annuelle moyenne"]
            if column not in log:
                filtered_df[column] = np.log(filtered_df[column])
                st.write(f"Log appliqué à : {column}")
        except (TypeError, ValueError) as e:
            st.error(f"Erreur logarithme : {e}")
            st.stop()

        stationarity_test_adf = st.checkbox("Test ADF")
        stationarity_test_kpss = st.checkbox("Test KPSS")

        if stationarity_test_adf:
            p_value_adf = test_adf(filtered_df[column])
            if p_value_adf is not None:
                st.write(f"p-value ADF : {p_value_adf}")
                if p_value_adf < 0.05:
                    st.success("Stationnaire (test ADF).")
                else:
                    st.warning("Non stationnaire (test ADF).")

        if stationarity_test_kpss:
            p_value_kpss = test_kpss(filtered_df[column])
            if p_value_kpss is not None:
                st.write(f"p-value KPSS : {p_value_kpss}")
                if p_value_kpss < 0.05:
                    st.success("Non stationnaire (test KPSS).")
                else:
                    st.warning("Stationnaire (test KPSS).")

        # Deuxième partie (Visualisation des données)
        st.subheader("Visualisation des Données")
        columns_to_choose_viz = df.columns[1:]
        selected_columns_viz = st.multiselect("Sélectionnez les variables à visualiser :", columns_to_choose_viz)

        if selected_columns_viz:
            plot_time_series(df, selected_columns_viz)
        else:
            st.warning("Veuillez sélectionner au moins une variable à visualiser.")

    except FileNotFoundError:
        st.error("Fichier non trouvé.")
    except Exception as e:
        st.error(f"Erreur : {e}")

if __name__ == '__main__':
    main()
