import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from statsmodels.tsa.stattools import adfuller, kpss

def test_adf(series):
    result = adfuller(series)
    return result[1]

def test_kpss(series):
    statistic, p_value, lags, critical_values = kpss(series, regression='c')
    return p_value

def plot_time_series(df, selected_columns, start_year, end_year):
    fig = go.Figure()

    # Filtrer les données en fonction de la période sélectionnée
    filtered_df = df[(df.iloc[:, 0] >= start_year) & (df.iloc[:, 0] <= end_year)]

    for column in selected_columns:
        fig.add_trace(go.Scatter(
            x=filtered_df.iloc[:, 0],
            y=filtered_df[column],
            mode='lines+markers',
            name=column
        ))

    fig.update_layout(
        title="Évolution des Variables Choisies",
        xaxis_title="Année",
        yaxis_title="Valeur",
        template='plotly_white'
    )

    st.plotly_chart(fig)

def main():
    st.set_page_config(page_title="Visualisation des Données")

    df = pd.read_excel("https://raw.githubusercontent.com/cezangue/simulated_models_equations/main/base_mes_taf.xlsx")

    # Affichage des colonnes pour le débogage
    st.write("Colonnes disponibles :", df.columns.tolist())

    st.subheader("Sélectionnez les Séries Chronologiques à Tester")
    selected_columns = st.multiselect("Choisissez les variables :", df.columns[1:])

    if selected_columns:
        start_year = st.selectbox("Année de début :", df.iloc[:, 0].unique())
        end_year = st.selectbox("Année de fin :", df.iloc[:, 0].unique(), index=len(df.iloc[:, 0].unique()) - 1)

        results = {}
        for column in selected_columns:
            st.write(f"**Tests pour la série : {column}**")
            
            # Tests sur la série originale
            adf_p_value = test_adf(df[column])
            kpss_p_value = test_kpss(df[column])

            st.write(f"p-value ADF : {adf_p_value} - {'Stationnaire' if adf_p_value < 0.05 else 'Non stationnaire'}")
            st.write(f"p-value KPSS : {kpss_p_value} - {'Non stationnaire' if kpss_p_value < 0.05 else 'Stationnaire'}")

            results[column] = {
                'ADF': adf_p_value,
                'KPSS': kpss_p_value,
            }

            # Differenciation et tests si non stationnaire
            if adf_p_value >= 0.05 or kpss_p_value < 0.05:
                st.write(f"**La série {column} est non stationnaire. Différenciation...**")
                differentiated_series = df[column].diff().dropna()  # Différencier la série

                # Tests sur la série différenciée
                adf_diff_p_value = test_adf(differentiated_series)
                kpss_diff_p_value = test_kpss(differentiated_series)

                st.write(f"p-value ADF (différenciée) : {adf_diff_p_value} - {'Stationnaire' if adf_diff_p_value < 0.05 else 'Non stationnaire'}")
                st.write(f"p-value KPSS (différenciée) : {kpss_diff_p_value} - {'Non stationnaire' if kpss_diff_p_value < 0.05 else 'Stationnaire'}")

                results[column]['Differentiated'] = {
                    'ADF': adf_diff_p_value,
                    'KPSS': kpss_diff_p_value,
                }

        # Visualisation des séries sélectionnées
        if st.button("Visualiser les Séries"):
            plot_time_series(df, selected_columns, start_year, end_year)

    else:
        st.warning("Veuillez sélectionner au moins une variable à tester.")

if __name__ == '__main__':
    main()
