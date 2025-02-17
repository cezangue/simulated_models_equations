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
    data['DCF'] = data.iloc[:, 1]
    data['Pib'] = data.iloc[:, 3]
    data['G'] = data.iloc[:, 2]
    data['X'] = data.iloc[:, 4]
    data['M'] = data.iloc[:, 5]
    data['TC'] = data.iloc[:, 6]
    data['FBCF'] = data.iloc[:, 7]
    data['Chom'] = data.iloc[:, 8]
    data['Pibmond'] = data.iloc[:, 9]
    data['Infflation'] = data.iloc[:, 10]
    data['MM'] = data.iloc[:, 11]
    data['Taux_interet'] = data.iloc[:, 12]

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

    # Affichage du texte d'introduction
    st.markdown("<h4 style='color: blue; font-weight: bold;'>"
                "Nous vous proposons donc ici une simulation du comportement des dynamiques macroéconomiques de la RCA au cours des 5 prochaines années après 2023 (2024 à 2028)."
                "</h4>", unsafe_allow_html=True)

    # Sélection des variables par l'utilisateur
    st.subheader("Choisissez les variables dont vous voulez voir l'impact sur l'économie")
    selected_vars = st.multiselect("Sélectionnez les variables :", list(equations.keys()))

    if selected_vars:
        # Choisir entre hausse ou baisse de 5 %
        change_direction = st.radio("Voulez-vous une hausse ou une baisse de 5 % ?", ['Hausse', 'Baisse'])

        # Calcul de la nouvelle valeur pour 2024
        for var in selected_vars:
            current_value = data[var].iloc[-1]  # Valeur de 2023
            change_amount = current_value * 0.05  # 5 % de la valeur actuelle
            
            if change_direction == 'Hausse':
                new_value = current_value + change_amount
            else:
                new_value = current_value - change_amount
            
            # Afficher la nouvelle valeur
            st.write(f"Nouvelle valeur de {var} pour 2024 : {new_value}")

            # Mettre à jour la dernière valeur dans le DataFrame pour prédiction
            data[var].iloc[-1] = new_value

        # Graphique des prévisions pour les 5 prochaines années
        st.subheader("Prévisions des Valeurs Futures")
        if st.button("Générer les Prévisions"):
            forecast_years = 5

            for var in selected_vars:
                last_values = data.iloc[-1:].copy()
                var_forecasts = []

                for _ in range(forecast_years):
                    # Ajouter une constante ici
                    last_values_for_prediction = sm.add_constant(last_values[equations[var]], has_constant='add')
                    forecast_value = results[var].predict(last_values_for_prediction)
                    var_forecasts.append(forecast_value.iloc[-1])  # Prendre la dernière prévision

                    # Mise à jour des valeurs pour la prochaine prévision
                    last_values = last_values.shift(1)  # Décalage
                    for exog_var in equations[var]:
                        if exog_var in last_values.columns:
                            last_values[exog_var].iloc[-1] = forecast_value.iloc[-1]

                # Création du graphique pour cette variable
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=np.arange(2024, 2024 + forecast_years), y=var_forecasts,
                                         mode='lines+markers', name=var))
                fig.update_layout(title=f'Prévisions pour {var} (2024-2028)',
                                  xaxis_title='Années',
                                  yaxis_title='Valeurs Prévues',
                                  showlegend=True)

                st.plotly_chart(fig)
