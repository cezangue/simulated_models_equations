import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm

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
    # Spécification des équations
    equations = {
        'Pib': ['FBCF', 'G', 'X', 'M', 'DCF', 'Taux_interet', 'Infflation', 'Chom', 'Pibmond', 'TC'],
        'DCF': ['Taux_interet', 'Pib'],
        'FBCF': ['Taux_interet', 'Pib'],
        'Chom': ['Pib', 'Taux_interet', 'Infflation'],
        'TC': ['Pib', 'Pibmond']
    }

    # Estimation avec 3SLS
    model = sm.system.ThreeStageLeastSquares(
        endog=[data[equation] for equation in equations.keys()],
        exog=[sm.add_constant(data[equations[equation]]) for equation in equations.keys()]
    ).fit()

    st.subheader("Résultats des Estimations")
    st.write(model.summary())

    # Fonction de prévision
    def forecast(model, last_values, n_years=5):
        forecasts = []
        for _ in range(n_years):
            last_values = sm.add_constant(last_values)  # Ajout de la constante
            forecast_value = model.predict(last_values)
            forecasts.append(forecast_value.iloc[-1])  # Prendre la dernière prévision
            
            # Mise à jour des valeurs pour la prochaine prévision
            last_values_new = last_values.copy()
            for col in last_values.columns[1:]:  # Ignorer la constante
                last_values_new[col].iloc[-1] = forecast_value.iloc[-1]  # Mise à jour de la dernière valeur
            
            last_values_new = last_values_new.shift(1)  # Décalage pour la prochaine prévision
            last_values_new.iloc[-1, 0] = 1  # Remettre la constante à 1
            last_values = last_values_new  # Mettre à jour last_values

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
        forecasts = forecast(model, last_values)

        # Affichage des prévisions
        st.subheader(f"Prévisions pour {variable_to_forecast} sur 5 ans")
        for i, forecast_value in enumerate(forecasts, start=1):
            st.write(f"Année {i}: {forecast_value:.2f}")
