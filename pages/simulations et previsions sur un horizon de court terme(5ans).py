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

    # Assignation des colonnes aux variables
    data['DCF'] = data.iloc[:, 1]      # Deuxième colonne
    data['Pib'] = data.iloc[:, 3]      # Quatrième colonne
    data['G'] = data.iloc[:, 2]        # Troisième colonne
    data['X'] = data.iloc[:, 4]        # Cinquième colonne
    data['M'] = data.iloc[:, 5]        # Sixième colonne
    data['TC'] = data.iloc[:, 6]       # Septième colonne
    data['FBCF'] = data.iloc[:, 7]     # Huitième colonne
    data['Chom'] = data.iloc[:, 8]     # Neuvième colonne
    data['Pibmond'] = data.iloc[:, 9]   # Dixième colonne
    data['Infflation'] = data.iloc[:, 10]  # Onzième colonne
    data['MM'] = data.iloc[:, 11]      # Douzième colonne
    data['Taux_interet'] = data.iloc[:, 12]  # Treizième colonne

    # Création des variables avec retards
    try:
        data['Pib_lag'] = data['Pib'].shift(1)
        data['FBCF_lag'] = data['FBCF'].shift(1)
        data['G_lag'] = data['G'].shift(1)
        data['X_lag'] = data['X'].shift(1)
        data['M_lag'] = data['M'].shift(1)
        data['TC_lag'] = data['TC'].shift(1)
        data['DCF_lag'] = data['DCF'].shift(1)
        data['Taux_interet_lag'] = data['Taux_interet'].shift(1)
        data['Infflation_lag'] = data['Infflation'].shift(1)
        data['Chom_lag'] = data['Chom'].shift(1)
        data['MM_lag'] = data['MM'].shift(1)
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

    # Affichage du texte avant les résultats
    st.markdown("<h4 style='color: blue; font-weight: bold;'>"
                "Après estimation par la méthode des Triples moindres carrés, nous obtenons des modèles ayant un fort pouvoir explicatif et des variables significativement influentes sur les grandes variables macroéconomiques de la RCA."
                "</h4>", unsafe_allow_html=True)

    # Graphique des prévisions pour les 5 prochaines années
    st.subheader("Prévisions des Valeurs Futures")
    if st.button("Générer les Prévisions"):
        # Prévisions pour chaque variable dépendante
        forecast_years = 5
        forecasts = {}
        
        for var in equations.keys():
            last_values = data.iloc[-1:].copy()
            var_forecasts = []
            
            for _ in range(forecast_years):
                last_values = sm.add_constant(last_values)  # Ajouter une constante
                forecast_value = results[var].predict(last_values)
                var_forecasts.append(forecast_value.iloc[-1])  # Prendre la dernière prévision
                
                # Mise à jour des valeurs pour la prochaine prévision
                last_values = last_values.shift(1)  # Décalage
                last_values.iloc[-1, 0] = 1  # Remettre la constante à 1

            forecasts[var] = var_forecasts

        # Création du graphique avec Plotly
        fig = go.Figure()
        for var, forecast_values in forecasts.items():
            fig.add_trace(go.Scatter(x=np.arange(1, forecast_years + 1), y=forecast_values,
                                     mode='lines+markers', name=var))

        fig.update_layout(title='Prévisions des Valeurs Futures pour les Variables Dépendantes',
                          xaxis_title='Années',
                          yaxis_title='Valeurs Prévues',
                          showlegend=True)

        st.plotly_chart(fig)
