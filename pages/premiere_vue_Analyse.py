import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller, kpss

def set_background(image_url, opacity=0.3, color="#000000"):
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
        </style>
        """,
        unsafe_allow_html=True
    )

def test_adf(series):
    result = adfuller(series)
    return result[1]

def test_kpss(series):
    statistic, p_value, lags, critical_values = kpss(series, regression='c')
    return p_value

def plot_time_series(df, selected_columns):
    plt.figure(figsize=(12, 6))
    for column in selected_columns:
        plt.plot(df['Annee'], df[column], marker='o', label=column)
    plt.title("Évolution des Variables Choisies", fontsize=16)
    plt.xlabel("Année")
    plt.ylabel("Valeur")
    plt.grid()
    plt.legend()
    st.pyplot(plt)

def main():
    st.set_page_config(page_title="Visualisation des Données")
    background_url = "https://raw.githubusercontent.com/Ndobo1997/Projet-MES/main/image_analyse_donnees.jpg"
    set_background(background_url, opacity=0.3)

    df = pd.read_excel("https://raw.githubusercontent.com/cezangue/simulated_models_equations/main/base_mes_taf.xlsx")

    st.subheader("Tests de Séries Temporelles")
    column = st.selectbox("Variable à tester :", df.columns[1:])
    start_year = st.selectbox("Année de début :", df['Annee'].unique())
    end_year = st.selectbox("Année de fin :", df['Annee'].unique(), index=len(df['Annee'].unique()) - 1)
    filtered_df = df[(df['Annee'] >= start_year) & (df['Annee'] <= end_year)]

    if st.checkbox("Test ADF"):
        p_value_adf = test_adf(filtered_df[column])
        st.write(f"p-value ADF : {p_value_adf}")
        st.success("Stationnaire" if p_value_adf < 0.05 else "Non stationnaire")

    if st.checkbox("Test KPSS"):
        p_value_kpss = test_kpss(filtered_df[column])
        st.write(f"p-value KPSS : {p_value_kpss}")
        st.success("Non stationnaire" if p_value_kpss < 0.05 else "Stationnaire")

    st.subheader("Visualisation des Données")
    selected_columns_viz = st.multiselect("Sélectionnez les variables à visualiser :", df.columns[1:])
    if selected_columns_viz:
        plot_time_series(df, selected_columns_viz)
    else:
        st.warning("Veuillez sélectionner au moins une variable à visualiser.")

if __name__ == '__main__':
    main()
