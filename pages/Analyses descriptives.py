import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.stats.diagnostic import breaks_cusumolsresid
import base64
import plotly.graph_objects as go
from statsmodels.tsa.api import VAR
import networkx as nx
def set_background(image_url, opacity=0.3, color="#000000"):
    """Fonction pour définir l'image de fond."""
    # CSS pour définir l'image de fond
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
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp p, .stApp label, .stApp .streamlit-expanderHeader {{
            color: yellow !important;
            font-size: 16px !important;
            font-family: sans-serif !important;
        }}
        .dataframe {{
            background-color: rgba(255, 255, 255, 0.7) !important; /* Fond blanc semi-transparent */
            color: green !important; /* Texte vert */
            font-size: 14px !important;
            border-collapse: collapse !important; /* Fusionne les bordures des cellules */
            width: 100% !important; /* Occupe toute la largeur disponible */
            margin-bottom: 1em !important;
        }}
        .dataframe th, .dataframe td {{
            border: 1px solid #ddd !important; /* Bordure grise pour les cellules */
            padding: 8px !important; /* Espacement intérieur des cellules */
            text-align: left !important; /* Alignement du texte à gauche */
        }}
        .dataframe th {{
            background-color: #f2f2f2 !important; /* Fond gris clair pour l'en-tête */
            font-weight: bold !important;
        }}
        .stSuccess {{
            color: lightgreen !important;
        }}
        .stWarning {{
            color: orange !important;
        }}
        .stError {{
            color: red !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    st.set_page_config(page_title="Visualisation des Données", page_icon="")
    background_url = "https://raw.githubusercontent.com/Ndobo1997/Projet-MES/main/image_analyse_donnees.jpg"
    set_background(background_url, opacity=0.3, color="#000000")

def main():
    st.set_page_config(page_title="Visualisation des Données", page_icon="")
    background_url = "https://raw.githubusercontent.com/Ndobo1997/Projet-MES/main/image_analyse_donnees.jpg"
    set_background(background_url, opacity=0.3, color="#000000")

    # CSS pour définir l'image de fond
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpeg;base64,{image_base64});
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
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp p, .stApp label, .stApp .streamlit-expanderHeader {{
            color: yellow !important;
            font-size: 16px !important;
            font-family: sans-serif !important;
        }}
        .dataframe {{
            background-color: rgba(255, 255, 255, 0.7) !important; /* Fond blanc semi-transparent */
            color: green !important; /* Texte vert */
            font-size: 14px !important;
            border-collapse: collapse !important; /* Fusionne les bordures des cellules */
            width: 100% !important; /* Occupe toute la largeur disponible */
            margin-bottom: 1em !important;
        }}
        .dataframe th, .dataframe td {{
            border: 1px solid #ddd !important; /* Bordure grise pour les cellules */
            padding: 8px !important; /* Espacement intérieur des cellules */
            text-align: left !important; /* Alignement du texte à gauche */
        }}
        .dataframe th {{
            background-color: #f2f2f2 !important; /* Fond gris clair pour l'en-tête */
            font-weight: bold !important;
        }}
        .stSuccess {{
            color: lightgreen !important;
        }}
        .stWarning {{
            color: orange !important;
        }}
        .stError {{
            color: red !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def test_adf(series):
    try:
        result = adfuller(series)
        return result[1]
    except Exception as e:
        st.error(f"Erreur test ADF : {e}")
        return None

def test_kpss(series):
    try:
        statistic, p_value, lags, critical_values = kpss(series, regression='c')
        return p_value
    except Exception as e:
        st.error(f"Erreur test KPSS : {e}")
        return None

def test_phillips_perron(series):
    try:
        result = adfuller(series)
        return result[1]
    except Exception as e:
        st.error(f"Erreur test Phillips-Perron : {e}")
        return None

def plot_acf_pacf(series, max_lags):
    try:
        fig, ax = plt.subplots(1, 2, figsize=(12, 5))
        plot_acf(series, ax=ax[0], lags=max_lags)
        plot_pacf(series, ax=ax[1], lags=max_lags)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Erreur autocorrelogrammes : {e}")

def plot_causality_graph(causality_results):
    G = nx.DiGraph()

    for (var1, var2), p_value in causality_results.items():
        if p_value < 0.05:
            G.add_edge(var1, var2)

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=12, font_weight='bold', arrows=True, arrowstyle='-|>', arrowsize=20)
    plt.title("Graphique des Relations de Causalité", fontsize=16, color="green") # Titre en vert
    plt.axis('off')
    plt.tight_layout()
    st.pyplot(plt)

def test_toda_yamamoto(df, var1, var2, max_lags):
    adf_var1 = adfuller(df[var1])[1]
    adf_var2 = adfuller(df[var2])[1]

    model = VAR(df[[var1, var2]])
    results = model.fit(maxlags=max_lags, ic='aic')

    causality_results = results.test_causality(var1, var2, kind='wald')
    return causality_results, adf_var1, adf_var2


def main():
    st.set_page_config(page_title="Visualisation des Données", page_icon="")
    background_url = "https://raw.githubusercontent.com/Ndobo1997/Projet-MES/main/image_analyse_donnees.jpg"
    set_background(background_url, opacity=0.3, color="#000000")

    try:
        # Charger la base de données depuis l'URL
        df = pd.read_excel("https://raw.githubusercontent.com/Ndobo1997/Projet-MES/main/base%20de%20donnees%20RDC.xlsx")
        excluded_columns = ['Annee']
        if not all(col in df.columns for col in excluded_columns):
            missing_cols = [col for col in excluded_columns if col not in df.columns]
            st.error(f"Colonnes manquantes : {missing_cols}")
            return

        columns_to_choose = df.columns[~df.columns.isin(excluded_columns)]

        # Première partie (Tests de séries temporelles)
        st.subheader("Tests de Séries Temporelles") # Sous-titre en vert
        column = st.selectbox("Variable à tester :", columns_to_choose)
        start_year = st.selectbox("Année de début :", df['Annee'].unique())
        end_year = st.selectbox("Année de fin :", df['Annee'].unique(), index=len(df['Annee'].unique()) - 1)
        filtered_df = df[(df['Annee'] >= start_year) & (df['Annee'] <= end_year)].copy()

        try:
            log = ["Banque centrale - Taux directeur","Inflation annuelle moyenne"]
            if column not in log:
                filtered_df[column] = np.log(filtered_df[column])
                st.write(f"Log appliqué à : {column}")
        except (TypeError, ValueError) as e:
            st.error(f"Erreur logarithme : {e}")
            st.stop()

        stationarity_test_adf = st.checkbox("Test ADF")
        stationarity_test_kpss = st.checkbox("Test KPSS")
        stationarity_test_pp = st.checkbox("Test Phillips-Perron")
        autocorr_test = st.checkbox("Autocorrélations")
        max_lags = st.number_input("Nombre de lags :", min_value=1, max_value=len(filtered_df)//2, value=len(filtered_df)//4)

        if stationarity_test_adf:
            p_value_adf = test_adf(filtered_df[column])
            if p_value_adf is not None:
                st.write(f"p-value ADF : {p_value_adf}")
                if p_value_adf < 0.05:
                    st.success("Stationnaire (test ADF).")
                else:
                    st.warning("Non stationnaire (test ADF).")

        if stationarity_test_kpss:
            p_value_kpss = test_kpss(filtered_df[column])
            if p_value_kpss is not None:
                st.write(f"p-value KPSS : {p_value_kpss}")
                if p_value_kpss < 0.05:
                    st.success("Non stationnaire (test KPSS).")
                else:
                    st.warning("Stationnaire (test KPSS).")
            if stationarity_test_pp:
                p_value_pp = test_phillips_perron(filtered_df[column])
            if p_value_pp is not None:
                st.write(f"p-value Phillips-Perron : {p_value_pp}")
                if p_value_pp < 0.05:
                    st.success("Stationnaire (test Phillips-Perron).")
                else:
                    st.warning("Non stationnaire (test Phillips-Perron).")

        if autocorr_test:
            plot_acf_pacf(filtered_df[column], max_lags)


        # Deuxième partie (Visualisation des données)
        st.subheader("Visualisation des Données")
        columns_to_choose_viz = df.columns[1:]
        selected_columns_viz = st.multiselect("Sélectionnez les variables à visualiser :", columns_to_choose_viz)

        if selected_columns_viz:
            for column_viz in selected_columns_viz:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df['Annee'], y=df[column_viz], mode='lines+markers', name=column_viz))

                fig.update_layout(
                    title=f"{column_viz} au fil des ans",
                    xaxis_title="Année",
                    yaxis_title=column_viz,
                    template="plotly_white"
                )
                st.plotly_chart(fig)
        else:
            st.warning("Veuillez sélectionner au moins une variable à visualiser.")

        # Troisième partie (Test de causalité de Toda et Yamamoto)
        st.subheader("Test de Causalité de Toda et Yamamoto")

        columns_to_choose_ty = df.columns[1:]
        selected_vars_ty = st.multiselect("Sélectionnez les variables pour le test de causalité :", columns_to_choose_ty)

        max_lags_ty = st.number_input("Nombre de lags pour le test de causalité :", min_value=1, max_value=10, value=1)

        if len(selected_vars_ty) >= 2: # Assurez-vous d'avoir au moins 2 variables sélectionnées
            filtered_df_ty = df[selected_vars_ty].dropna()

            if st.button("Effectuer le test de causalité de Toda et Yamamoto"):
                results_summary = []
                conclusions = []
                causality_results = {}
                for i in range(len(selected_vars_ty)):
                    for j in range(i + 1, len(selected_vars_ty)):
                        var1 = selected_vars_ty[i]
                        var2 = selected_vars_ty[j]

                        causality_test, adf_var1, adf_var2 = test_toda_yamamoto(filtered_df_ty, var1, var2, max_lags_ty)

                        results_summary.append({
                            'Variable 1': var1,
                            'Variable 2': var2,
                            'p-value': causality_test.pvalue,
                            'ADF p-value Var1': adf_var1,
                            'ADF p-value Var2': adf_var2
                        })

                        if causality_test.pvalue < 0.05:
                            conclusions.append(f"À l'aide du test de Toda et Yamamoto, {var1} cause {var2} (p-value < 0.05).")
                            causality_results[(var1, var2)] = causality_test.pvalue
                        else:
                            conclusions.append(f"À l'aide du test de Toda et Yamamoto, {var1} ne cause pas {var2} (p-value >= 0.05).")

                results_df = pd.DataFrame(results_summary)
                st.write("Résultats du test de causalité de Toda et Yamamoto :")
                st.dataframe(results_df)

                st.write("Conclusions :")
                for conclusion in conclusions:
                    st.write(conclusion)
                
                if causality_results: # Vérifie si le dictionnaire n'est pas vide avant de tracer le graphe
                    st.write("Résumé des relations de causalité :")
                    plot_causality_graph(causality_results)
                else:
                    st.write("Aucune relation de causalité significative détectée.")

        elif selected_vars_ty: # Message si moins de deux variables sont sélectionnées
            st.warning("Veuillez sélectionner au moins deux variables pour le test de causalité de Toda et Yamamoto.")

    except FileNotFoundError:
        st.error("Fichier non trouvé.")
    except Exception as e:
        st.error(f"Erreur : {e}")

if __name__ == '__main__':
    main()
