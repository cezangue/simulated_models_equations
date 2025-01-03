import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
import plotly.graph_objects as go

# Charger les données à partir d'un fichier Excel
@st.cache_data
def load_data(file_path):
    try:
        return pd.read_excel(file_path)
    except FileNotFoundError:
        st.error("Le fichier n'a pas été trouvé. Vérifiez le nom et le chemin.")
        return None
    except Exception as e:
        st.error(f"Une erreur est survenue lors du chargement du fichier : {e}")
        return None

# Charger les données
data = load_data('base_mes_taf.xlsx')

if data is not None:
    # Vérifier les noms des colonnes
    st.write("Noms des colonnes dans le DataFrame :", data.columns)

    # Supprimer les espaces dans les noms des colonnes
    data.columns = data.columns.str.strip()

    # Utiliser la quatrième colonne comme Pib, la troisième comme G et la cinquième comme X
    data['Pib'] = data.iloc[:, 3]  # Quatrième colonne
    data['G'] = data.iloc[:, 2]    # Troisième colonne
    data['X'] = data.iloc[:, 4]    # Cinquième colonne

    # Création des variables avec retards
    try:
        data['Pib_lag'] = data['Pib'].shift(1)
        data['FBCF_lag'] = data['FBCF'].shift(1)
        data['G_lag'] = data['G'].shift(1)
        data['X_lag'] = data['X'].shift(1)
        data['M_lag'] = data['M'].shift(1)
        data['DCF_lag'] = data['DCF'].shift(1)
        data['Taux_interet_lag'] = data['Taux_interet'].shift(1)
        data['Infflation_lag'] = data['Infflation'].shift(1)
        data['Chom_lag'] = data['Chom'].shift(1)
        data['TC_lag'] = data['TC'].shift(1)
        data['Pibmond_lag'] = data['Pibmond'].shift(1)
    except KeyError as e:
        st.error(f"Erreur : la colonne {e} n'existe pas dans le DataFrame.")

    # Supprimer les lignes avec des valeurs manquantes
    data.dropna(inplace=True)

    # Spécification des équations
    equations = {
        'Pib': ['Pib_lag', 'FBCF_lag', 'FBCF', 'G', 'G_lag', 'X', 'X_lag', 'M', 'M_lag'],
        'DCF': ['DCF_lag', 'Pib_lag', 'Taux_interet_lag'],
        'FBCF': ['FBCF_lag', 'Taux_interet', 'Pib_lag', 'Taux_interet_lag'],
        'MM': ['MM_lag', 'Pib', 'Pib_lag', 'Taux_interet', 'Taux_interet_lag', 'Infflation_lag'],
        'TC': ['Pib', 'Pib_lag', 'Pibmond', 'TC_lag'],
        'Chom': ['Chom_lag', 'Pib_lag', 'Pibmond_lag']
    }

    # Estimation des modèles OLS pour chaque équation
    results = {}
    for endog_var, exog_vars in equations.items():
        exog_data = sm.add_constant(data[exog_vars])  # Ajouter une constante
        model = sm.OLS(data[endog_var], exog_data).fit()  # Estimation
        results[endog_var] = model

    st.subheader("Résultats des Estimations")
    for var, result in results.items():
        st.write(f"Résultats pour {var}:")
        st.write(result.summary())

    # Fonction de prévision
    def forecast(model, last_values, n_years=5):
        forecasts = []
        for _ in range(n_years):
            last_values = sm.add_constant(last_values)  # Ajouter une constante
            forecast_value = model.predict(last_values)
            forecasts.append(forecast_value.iloc[-1])  # Prendre la dernière prévision
            
            # Mise à jour des valeurs pour la prochaine prévision
            last_values = last_values.shift(1)  # Décalage
            last_values.iloc[-1, 0] = 1  # Remettre la constante à 1

        return forecasts

    # Sélecteur de variable à prévoir
    variable_to_forecast = st.selectbox(
        "Choisissez la variable à prévoir:",
        list(equations.keys())
    )

    # Prévisions
    if st.button("Prévoir"):
        # Récupération des dernières valeurs
        last_values = data.iloc[-1:].copy()

        # Prévisions
        forecasts = forecast(results[variable_to_forecast], last_values)

        # Préparation des données pour le graphique
        forecast_years = np.arange(1, len(forecasts) + 1)
        forecast_values = forecasts

        # Création du graphique avec Plotly
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index[-len(forecasts):], y=data[variable_to_forecast].iloc[-len(forecasts):],
                                 mode='lines+markers', name='Valeurs Observées'))
        fig.add_trace(go.Scatter(x=forecast_years + data.index[-1], y=forecast_values,
                                 mode='lines+markers', name='Prévisions', line=dict(dash='dash')))

        fig.update_layout(title=f'Prévisions pour {variable_to_forecast}',
                          xaxis_title='Années',
                          yaxis_title=variable_to_forecast,
                          showlegend=True)

        st.plotly_chart(fig)
