import streamlit as st
import pandas as pd
import plotly.express as px



# Configuration de la page
#st.set_page_config(page_title="Visualisateur de séries temporelles", layout="wide")

# Lecture du fichier Excel en arrière-plan
@st.cache_data  # Cache les données pour de meilleures performances
def load_data():
    # Remplacez 'chemin/vers/votre/fichier.xlsx' par le chemin réel de votre fichier
    df = pd.read_excel('base_mes_taf.xlsx')
    return df

# Chargement des données

def Plot():
    try:
        df = load_data()
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
        selected_column = st.selectbox(
            "Choisissez la série temporelle à visualiser :",
            options=numeric_columns
        )

        # Statistiques descriptives
        st.write("Statistiques descriptives :")
        stat = df[selected_column].describe().T 
        stats_df = pd.DataFrame(stat).transpose()
        st.write(stats_df)
        
        # Création du graphique avec Plotly
        if selected_column:
            fig = px.line(
                df,
                y=selected_column,
                title=f'Série temporelle - {selected_column}',
                template='plotly_dark' if st.session_state.get('theme', 'light') == 'dark' else 'plotly_white'
            )
            
            # Personnalisation du graphique
            fig.update_layout(
                xaxis_title="Index temporel",
                yaxis_title=selected_column,
                showlegend=True,
                height=600
            )
            
            # Affichage du graphique
            st.plotly_chart(fig, use_container_width=True)
            
    except Exception as e:
        st.error(f"Une erreur s'est produite lors de la lecture du fichier : {str(e)}")


def Presentation():
    st.markdown("""
    ## La Côte d'Ivoire : Une puissance économique ouest-africaine

    La Côte d'Ivoire, située en Afrique de l'Ouest, se positionne comme un pilier économique majeur de la région. Selon la Banque Mondiale (2023), le pays compte environ 26,5 millions d'habitants sur un territoire de 322 463 km².

    ### Une économie dominée par l'agriculture

    D'après l'Organisation Internationale du Cacao (ICCO, 2023), la Côte d'Ivoire maintient sa position de premier producteur mondial de cacao, représentant environ 45% de la production mondiale. Selon le Conseil Café-Cacao (2023), cette filière emploie plus de 5 millions de personnes.

    Le rapport de la FAO (2023) souligne également l'excellence du pays dans d'autres cultures :
    - Premier producteur mondial de noix de cajou
    - Leader africain dans la production d'hévéa
    - Acteur majeur dans la production d'huile de palme

    ### Une croissance économique remarquable

    Les données de la Banque Africaine de Développement (BAD, 2023) révèlent que depuis 2012, la Côte d'Ivoire maintient une croissance économique moyenne d'environ 7% par an, malgré les chocs externes comme la pandémie de COVID-19. Le FMI (2023) attribue cette performance à :
    - Un programme ambitieux d'investissements publics
    - Des réformes structurelles
    - Une amélioration du climat des affaires

    ### Un hub économique régional

    Selon l'Autorité Portuaire d'Abidjan (2023), le Port Autonome d'Abidjan traite plus de 75% des échanges extérieurs du pays et sert de porte d'entrée pour plusieurs pays enclavés. Le Programme des Nations Unies pour le Développement (PNUD, 2023) note les avancées significatives en matière d'infrastructures :
    - Un réseau routier modernisé
    - Des infrastructures énergétiques en expansion
    - Une diversification du tissu industriel

    Dans son rapport sur les perspectives économiques africaines, la BAD (2023) souligne que le pays poursuit sa transformation économique à travers le Plan National de Développement (PND 2021-2025), visant une industrialisation accélérée et une amélioration du capital humain.

    Sources : Banque Mondiale, ICCO, FAO, BAD, FMI, PNUD, Conseil Café-Cacao, Autorité Portuaire d'Abidjan (2023)
    """)


import base64

def show_pdf(file_path):
    # Ouvrir et lire le fichier PDF en mode binaire
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    
    # Création du bouton de téléchargement
    with open(file_path, "rb") as file:
        btn = st.download_button(
            label="📥 Télécharger le PDF",
            data=file,
            file_name="mon_document.pdf",  # Nom du fichier lors du téléchargement
            mime="application/pdf"
        )
    
    # Afficher le PDF dans l'application (optionnel)
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
