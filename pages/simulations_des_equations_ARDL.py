import streamlit as st

def set_background(opacity=0.5, color="#000000"):
    """Définit la couleur de fond de l'application."""
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {color};
            opacity: {opacity};
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
            90% {{ transform: translateX(0%); opacity: 1;}}
            100% {{ transform: translateX(100%); opacity: 0; }}
        }}
        .fade-in-out {{
            animation: fade 3s ease-in-out infinite alternate;
            color: #ADD8E6;
        }}
        @keyframes fade {{
            0% {{ opacity: 0.2; color: #ADD8E6;}}
            50% {{ opacity: 1; color: #87CEEB; }}
            100% {{ opacity: 0.2; color: #ADD8E8; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def main():
    st.set_page_config(page_title="Visualisation des Données", page_icon="")
    
    # Définir la couleur de fond
    set_background(opacity=1.0, color="#000000")

    st.markdown("""<h1 class="animated-title">BIENVENUE DANS L'ESPACE D'ANALYSE DES DYNAMIQUES MACROECONMIQUES DE L'ECONOMIE DE LA RCA</h1>""", unsafe_allow_html=True)
    st.markdown('<h2 class="fade-in-out">Bonne navigation</h2>', unsafe_allow_html=True)

    # Ajouter l'image du drapeau depuis le répertoire local
    st.image("RCA_image.JPG", caption="Drapeau de la République Centrafricaine", use_container_width=True)  # Changement ici

    st.title("Cette page, fruit du groupe constitué de TAGNE TCHINDA RINEL et de NAH SAMBOULI LIONEL, vous donne une vue sur la base de données utilisée pour faire des analyses, la description des différentes chroniques retenues, la modélisation ARDL et les simulations.")
    st.title("Pour voir le contenu d'une section, il vous suffit de cliquer sur le nom correspondant pour y accéder. Et pour faire des simulations, vous allez vous-même entrer vos propres données selon le guide que vous trouverez sur la page en question.")

if __name__ == '__main__':
    main()
