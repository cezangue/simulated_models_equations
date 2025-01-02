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

    model1 = sm.OLS(Y1_clean, X1_clean).fit()

    # Équation 2: DCF
    Y2 = data['DCF']
    X2 = data[['Taux_interet', 'Pib']]
    X2['DCF_lag'] = data['DCF'].shift(1)
    combined_data = pd.concat([Y2, X2], axis=1).dropna()
    Y2_clean = combined_data['DCF']
    X2_clean = sm.add_constant(combined_data.drop(columns='DCF'))

    model2 = sm.OLS(Y2_clean, X2_clean).fit()

    # Équation 3: FBCF
    Y3 = data['FBCF']
    X3 = data[['Taux_interet', 'Pib']]
    X3['FBCF_lag'] = data['FBCF'].shift(1)
    combined_data = pd.concat([Y3, X3], axis=1).dropna()
    Y3_clean = combined_data['FBCF']
    X3_clean = sm.add_constant(combined_data.drop(columns='FBCF'))

    model3 = sm.OLS(Y3_clean, X3_clean).fit()

    # Équation 4: Chom
    Y4 = data['Chom']
    X4 = data[['Pib', 'Taux_interet', 'Infflation']]
    X4['Chom_lag'] = data['Chom'].shift(1)
    combined_data = pd.concat([Y4, X4], axis=1).dropna()
    Y4_clean = combined_data['Chom']
    X4_clean = sm.add_constant(combined_data.drop(columns='Chom'))

    model4 = sm.OLS(Y4_clean, X4_clean).fit()

    # Équation 5: TC
    Y5 = data['TC']
    X5 = data[['Pib', 'Pibmond']]
    X5['TC_lag'] = data['TC'].shift(1)
    combined_data = pd.concat([Y5, X5], axis=1).dropna()
    Y5_clean = combined_data['TC']
    X5_clean = sm.add_constant(combined_data.drop(columns='TC'))

    model5 = sm.OLS(Y5_clean, X5_clean).fit()

    return model1, model2, model3, model4, model5

# Streamlit Interface
st.title("Modèle à Équations Simultanées")

# Affichage des équations
st.subheader("Équations à Modéliser")
st.markdown("""
1. **PIB**: 
   \[
   PIB_t = a_0 + a_1 PIB_{t-1} + b_1 FBCF_{t-1} + c_1 FBCF_t + d_1 G_t + e_1 G_{t-1} + f_1 X_t + g_1 X_{t-1} + h_1 M_t + i_1 M_{t-1}
   \]

2. **DCF**: 
   \[
   DCF_t = a_2 DCF_{t-1} + b_2 PIB_{t-1} + c_2 Taux\_interet_{t-1}
   \]

3. **FBCF**: 
   \[
   FBCF_t = a_3 FBCF_{t-1} + b_3 Taux\_interet_t + c_3 PIB_{t-1} + d_3 Taux\_interet_{t-1}
   \]

4. **Chom**: 
   \[
   Chom_t = a_4 Chom_{t-1} + b_4 PIB_{t-1} + c_4 Pibmond_{t-1}
   \]

5. **TC**: 
   \[
   TC_t = a_5 PIB_t + b_5 Pibmond_t + c_5 TC_{t-1}
   \]
""")

# Estimation des modèles
models = model_equations(data)

# Affichage des résultats
st.subheader("Résultats des Estimations par Double Moindres Carrés")
for i, model in enumerate(models, start=1):
    st.markdown(f"### Modèle {i}")
    st.write(model.summary())
