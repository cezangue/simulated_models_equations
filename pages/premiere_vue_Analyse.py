import streamlit as st
import pandas as pd
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

def plot_time_series(df, selected_columns, start_year, end_year):
    plt.figure(figsize=(12, 6))
    
    # Filtrer les données en fonction de la période sélectionnée
    filtered_df = df[(df['Annee'] >= start_year) & (df['Annee'] <= end_year)]
    
    for column in selected_columns:
        plt.plot(filtered_df['Annee'], filtered_df[column], marker='o', label=column)
        
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

    st.subheader("Sélectionnez les Séries Chronologiques à Tester")
    selected_columns = st.multiselect("Choisissez les variables :", df.columns[1:])

    if selected_columns:
        start_year = st.selectbox("Année de début :", df['Annee'].unique())
        end_year = st.selectbox("Année de fin :", df['Annee'].unique(), index=len(df['Annee'].unique()) - 1)

        results = {}
        for column in selected_columns:
            st.write(f"**Tests pour la série : {column}**")
            adf_p_value = test_adf(df[column])
            kpss_p_value = test_kpss(df[column])

            st.write(f"p-value ADF : {adf_p_value} - {'Stationnaire' if adf_p_value < 0.05 else 'Non stationnaire'}")
            st.write(f"p-value KPSS : {kpss_p_value} - {'Non stationnaire' if kpss_p_value < 0.05 else 'Stationnaire'}")

            results[column] = {
                'ADF': adf_p_value,
                'KPSS': kpss_p_value,
            }

        # Visualisation des séries sélectionnées
        if st.button("Visualiser les Séries"):
            plot_time_series(df, selected_columns, start_year, end_year)

    else:
        st.warning("Veuillez sélectionner au moins une variable à tester.")

if __name__ == '__main__':
    main()
