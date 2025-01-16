import streamlit as st
import os
from pathlib import Path

# Définir le titre de l'application
st.title("Page d'Accueil")

# Fonction pour créer des onglets
def display_tabs():
    tabs = ["Volet de visualisation des indicateurs", "Autre page 1", "Autre page 2"]  # Ajoutez ici d'autres onglets si nécessaire
    selected_tab = st.selectbox("Choisissez une option :", tabs)

    if selected_tab == "Volet de visualisation des indicateurs":
        display_visualisation()
    elif selected_tab == "Autre page 1":
        st.write("Contenu de l'autre page 1")
    elif selected_tab == "Autre page 2":
        st.write("Contenu de l'autre page 2")

# Fonction pour afficher le contenu de la visualisation
def display_visualisation():
    st.markdown(
        """
        <style>
        body {
            background-color: #FFA500; /* Couleur de fond orange */
            color: white;
            font-family: Arial, sans-serif;
        }
        h1 {
            font-size: 2.5em;
            font-weight: bold;
            animation: text-animation 10s linear infinite;
            text-shadow: 2px 2px 4px #000000;
        }
        @keyframes text-animation {
            0% { transform: translateX(-100%); opacity: 0; }
            10% { transform: translateX(0%); opacity: 1; }
            90% { transform: translateX(0%); opacity: 1; }
            100% { transform: translateX(100%); opacity: 0; }
        }
        h2 {
            animation: fade 3s ease-in-out infinite alternate;
            color: #ADD8E6;
        }
        @keyframes fade {
            0% { opacity: 0.2; color: #ADD8E6; }
            50% { opacity: 1; color: #87CEEB; }
            100% { opacity: 0.2; color: #ADD8E8; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("""<h1>TAGNE TCHINDA VOUS SOUHAITE LA BIENVENUE DANS L'ESPACE D'ANALYSE DES EFFETS DU CHANGEMENT CLIMATIQUE EN AFRIQUE SUB-SAHARIENNE</h1>""", unsafe_allow_html=True)
    st.markdown('<h2>Bonne navigation</h2>', unsafe_allow_html=True)

    # Ajouter l'image du drapeau depuis le répertoire local
    st.image("Changement_climatique.JPG", caption="  ", use_container_width=True)

    st.write("Cette page, fruit du travail de TAGNE TCHINDA RINEL, nous vous proposons une vue sur la base de données utilisée pour faire des analyses, la description des différentes chroniques retenues, et l'analyse de la stationnarité des chroniques.")
    st.write("Pour voir le contenu d'une section, il vous suffit de cliquer sur le nom correspondant pour y accéder.")

# Appel de la fonction pour afficher les onglets
display_tabs()
