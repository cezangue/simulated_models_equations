import streamlit as st
import pandas as pd

def set_background(image_url, opacity=0.5, color="#000000"):
    """Définit l'image de fond de l'application."""
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url({image_url});
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
        .stApp h1, .stApp h2 {{
            color: white !important;
        }}
        .animated-title {{
            font-size: 2.5em;
            font-weight: bold;
            animation: text-animation 10s linear infinite;
            text-shadow: 2px 2px 4px #000000;
        }}
        @keyframes text-animation {{
            0% {{ transform: translateX(-100%); opacity: 0; }}
            10% {{ transform: translateX(0%); opacity: 1;}}
            90% {{transform: translateX(0%); opacity: 1;}}
            100% {{ transform: translateX(100%); opacity: 0; }}
        }}
        .fade-in-out {{
            animation: fade 3s ease-in-out infinite alternate;
            color: #ADD8E6;
        }}
        @keyframes fade {{
            0% {{ opacity: 0.2; color: #ADD8E6;}}
            50% {{ opacity: 1; color: #87CEEB; }}
            100% {{ opacity: 0.2; color: #ADD8E6; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def main():
    st.set_page_config(page_title="Visualisation des Données", page_icon="")
    
    # Définir l'image de fond
    background_url = "https://raw.githubusercontent.com/cezangue/simulated_models_equations/main/image_BDD.jpg"
    set_background(background_url, opacity=0.3, color="#000000")

    # Affichage des titres
    st.markdown("""<h1 class="animated-title">Base de données RDC</h1>""", unsafe_allow_html=True)
    st.markdown("""<h1 class="animated-title">Période étude : 1999 - 2023</h1>""", unsafe_allow_html=True)
    st.markdown('<h2 class="fade-in-out">Soit une série de 24 ans.</h2>', unsafe_allow_html=True)
    st.title("Les données présentées sur cette page résultent d'un téléchargement des données de la Banque Mondiale.")

    # Chargement du fichier Excel
    file_path = "https://github.com/cezangue/simulated_models_equations/blob/main/base_mes_taf.xlsx"
    
    try:
        df = pd.read_excel(file_path, engine='openpyxl')

        # Fonction pour formater l'affichage des nombres
        def format_number(value):
            if isinstance(value, (int, float)):
                return f"{value:.2f}"
            return value

        # Application du formatage à l'ensemble du DataFrame
        styled_df = df.style.format(formatter=format_number)

        # Affichage du DataFrame stylisé
        st.header("Présentation de la Base")
        st.dataframe(styled_df)

    except ImportError:
        st.error("Erreur : La bibliothèque 'openpyxl' n'est pas installée. Veuillez l'installer avec 'pip install openpyxl'.")
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier Excel : {e}")

if __name__ == '__main__':
    main()
