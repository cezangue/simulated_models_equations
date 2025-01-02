import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.iolib.summary2 import summary_df

# Génération de données fictives pour l'exemple
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
    'Pibmond': np.random.rand(n)
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
    X1 = sm.add_constant(X1.dropna())
    model1 = sm.OLS(Y1.dropna(), X1).fit()

    # Équation 2: DCF
    Y2 = data['DCF']
    X2 = data[['Taux_interet', 'Pib']]
    X2['DCF_lag'] = data['DCF'].shift(1)
    X2['Pib_lag'] = data['Pib'].shift(1)
    X2 = sm.add_constant(X2.dropna())
    model2 = sm.OLS(Y2.dropna(), X2).fit()

    # Équation 3: FBCF
    Y3 = data['FBCF']
    X3 = data[['Taux_interet', 'Pib']]
    X3['FBCF_lag'] = data['FBCF'].shift(1)
    X3 = sm.add_constant(X3.dropna())
    model3 = sm.OLS(Y3.dropna(), X3).fit()

    # Équation 4: MM
    Y4 = data['MM']
    X4 = data[['Pib', 'Taux_interet', 'Infflation']]
    X4['MM_lag'] = data['MM'].shift(1)
    X4 = sm.add_constant(X4.dropna())
    model4 = sm.OLS(Y4.dropna(), X4).fit()

    # Équation 5: TC
    Y5 = data['TC']
    X5 = data[['Pib', 'Pibmond']]
    X5['TC_lag'] = data['TC'].shift(1)
    X5 = sm.add_constant(X5.dropna())
    model5 = sm.OLS(Y5.dropna(), X5).fit()

    # Équation 6: Chom
    Y6 = data['Chom']
    X6 = data[['Pibmond']]
    X6['Chom_lag'] = data['Chom'].shift(1)
    X6['Pib_lag'] = data['Pib'].shift(1)
    X6 = sm.add_constant(X6.dropna())
    model6 = sm.OLS(Y6.dropna(), X6).fit()

    return model1, model2, model3, model4, model5, model6

# Streamlit Interface
st.title("Modèle à Équations Simultanées")

# Affichage des équations
st.subheader("Équations à Modéliser")
st.markdown("""
1. **PIB**: \( PIB_t = a_0 + a_1 PIB_{t-1} + b_1 FBCF_{t-1} + c_1 FBCF_t + d_1 G_t + e_1 G_{t-1} + f_1 X_t + g_1 X_{t-1} + h_1 M_t + i_1 M_{t-1} \)

2. **DCF**: \( DCF_t = a_2 DCF_{t-1} + b_2 PIB_{t-1} + c_2 Taux\_interet_{t-1} \)

3. **FBCF**: \( FBCF_t = a_3 FBCF_{t-1} + b_3 Taux\_interet_t + c_3 PIB_{t-1} + d_3 Taux\_interet_{t-1} + e_3 Taux\_interet_t \)

4. **MM**: \( MM_t = a_0^4 + a_4 MM_{t-1} + b_4 PIB_t + c_4 PIB_{t-1} + d_4 Taux\_interet_t + e_4 Taux\_interet_{t-1} + f_4 Infflation_{t-1} \)

5. **TC**: \( TC_t = a_0^5 + a_5 PIB_t + b_5 PIB_{t-1} + c_5 Pibmond_t + d_5 TC_{t-1} \)

6. **Chom**: \( Chom_t = a_6 Chom_{t-1} + b_6 PIB_{t-1} + c_6 Pibmond_{t-1} \)
""")

# Estimation des modèles
models = model_equations(data)

# Affichage des résultats
st.subheader("Résultats des Estimations par Double Moindres Carrés")
for i, model in enumerate(models, start=1):
    st.markdown(f"### Modèle {i}")
    st.write(summary_df(model))
