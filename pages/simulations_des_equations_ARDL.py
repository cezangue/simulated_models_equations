import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm

# Charger les données à partir d'un fichier Excel
@st.cache_data
def load_data(file_path):
    return pd.read_excel(file_path)

# Charger les données
data = load_data('base_mes_taf.xlsx')

# Spécification des équations
def model_equations(data):
    models = []
    equations = [
        ('Pib', ['FBCF', 'G', 'X', 'M']),
        ('DCF', ['Taux_interet', 'Pib']),
        ('FBCF', ['Taux_interet', 'Pib']),
        ('Chom', ['Pib', 'Taux_interet', 'Infflation']),
        ('TC', ['Pib', 'Pibmond']),
    ]

    for Y_var, X_vars in equations:
        Y = data[Y_var]
        X = data[X_vars].copy()

        # Création des variables retardées
        for var in X_vars:
            X[f'{var}_lag'] = data[var].shift(1)

        combined_data = pd.concat([Y, X], axis=1).dropna()
        Y_clean = combined_data[Y_var]
        X_clean = sm.add_constant(combined_data.drop(columns=Y_var))
        models.append(sm.OLS(Y_clean, X_clean).fit())

    return models

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

# Streamlit Interface
st.title("Modèle à Équations Simultanées")

# Affichage des équations
st.subheader("Équations à Modéliser")
st.markdown("""
1. **PIB**: PIB_t = a_0 + a_1 PIB_{t-1} + b_1 FBCF_{t-1} + c_1 FBCF_t + d_1 G_t + e_1 G_{t-1} + f_1 X_t + g_1 X_{t-1} + h_1 M_t + i_1 M_{t-1}
2. **DCF**: DCF_t = a_2 DCF_{t-1} + b_2 PIB_{t-1} + c_2 Taux_interet_{t-1}
3. **FBCF**: FBCF_t = a_3 FBCF_{t-1} + b_3 Taux_interet_t + c_3 PIB_{t-1} + d_3 Taux_interet_{t-1}
4. **Chom**: Chom_t = a_4 Chom_{t-1} + b_4 PIB_{t-1} + c_4 Pibmond_{t-1}
5. **TC**: TC_t = a_5 PIB_t + b_5 Pibmond_t + c_5 TC_{t-1}
""")

# Estimation des modèles
models = model_equations(data)

# Sélecteur de variable à prévoir
variable_to_forecast = st.selectbox(
    "Choisissez la variable à prévoir:",
    ["Pib", "DCF", "FBCF", "Chom", "TC"]
)

# Prévisions
if st.button("Prévoir"):
    index = ["Pib", "DCF", "FBCF", "Chom", "TC"].index(variable_to_forecast)
    model = models[index]
    
    # Récupération des dernières valeurs
    last_values = data.iloc[-1:].copy()

    # Prévisions
    forecasts = forecast(model, last_values)

    # Affichage des prévisions
    st.subheader(f"Prévisions pour {variable_to_forecast} sur 5 ans")
    for i, forecast_value in enumerate(forecasts, start=1):
        st.write(f"Année {i}: {forecast_value:.2f}")
