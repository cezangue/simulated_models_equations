import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm

# Génération de données fictives
np.random.seed(0)
n = 100
data = pd.DataFrame({
    'Pib': np.random.rand(n),
    'FBCF': np.random.rand(n),
    'G': np.random.rand(n),
    'X': np.random.rand(n),
    'M': np.random.rand(n),
    'DCF': np.random.rand(n),
    'Taux_interet': np.random.rand(n),
    'Infflation': np.random.rand(n),
    'Chom': np.random.rand(n),
    'Pibmond': np.random.rand(n),
    'TC': np.random.rand(n)  # Ajout de la colonne TC
})

# Spécification des équations
def model_equations(data):
    models = []
    
    # Équation 1: PIB
    Y1 = data['Pib']
    X1 = data[['FBCF', 'G', 'X', 'M']]
    X1['Pib_lag'] = data['Pib'].shift(1)
    X1['FBCF_lag'] = data['FBCF'].shift(1)
    X1['G_lag'] = data['G'].shift(1)
    X1['X_lag'] = data['X'].shift(1)
    X1['M_lag'] = data['M'].shift(1)
    combined_data = pd.concat([Y1, X1], axis=1).dropna()
    Y1_clean = combined_data['Pib']
    X1_clean = sm.add_constant(combined_data.drop(columns='Pib'))
    models.append(sm.OLS(Y1_clean, X1_clean).fit())

    # Équation 2: DCF
    Y2 = data['DCF']
    X2 = data[['Taux_interet', 'Pib']]
    X2['DCF_lag'] = data['DCF'].shift(1)
    combined_data = pd.concat([Y2, X2], axis=1).dropna()
    Y2_clean = combined_data['DCF']
    X2_clean = sm.add_constant(combined_data.drop(columns='DCF'))
    models.append(sm.OLS(Y2_clean, X2_clean).fit())

    # Équation 3: FBCF
    Y3 = data['FBCF']
    X3 = data[['Taux_interet', 'Pib']]
    X3['FBCF_lag'] = data['FBCF'].shift(1)
    combined_data = pd.concat([Y3, X3], axis=1).dropna()
    Y3_clean = combined_data['FBCF']
    X3_clean = sm.add_constant(combined_data.drop(columns='FBCF'))
    models.append(sm.OLS(Y3_clean, X3_clean).fit())

    # Équation 4: Chom
    Y4 = data['Chom']
    X4 = data[['Pib', 'Taux_interet', 'Infflation']]
    X4['Chom_lag'] = data['Chom'].shift(1)
    combined_data = pd.concat([Y4, X4], axis=1).dropna()
    Y4_clean = combined_data['Chom']
    X4_clean = sm.add_constant(combined_data.drop(columns='Chom'))
    models.append(sm.OLS(Y4_clean, X4_clean).fit())

    # Équation 5: TC
    Y5 = data['TC']
    X5 = data[['Pib', 'Pibmond']]
    X5['TC_lag'] = data['TC'].shift(1)
    combined_data = pd.concat([Y5, X5], axis=1).dropna()
    Y5_clean = combined_data['TC']
    X5_clean = sm.add_constant(combined_data.drop(columns='TC'))
    models.append(sm.OLS(Y5_clean, X5_clean).fit())

    return models

# Fonction de prévision
def forecast(model, last_values, n_years=5):
    forecasts = []
    
    # Prévisions pour n_years
    for _ in range(n_years):
        forecast_value = model.predict(last_values)
        forecasts.append(forecast_value.iloc[-1])  # Prendre la dernière prévision
        
        # Mise à jour des valeurs pour la prochaine prévision
        last_values = last_values.copy()
        last_values.iloc[-1, 1:] = forecast_value.iloc[-1]  # Mettre à jour les valeurs prévues
