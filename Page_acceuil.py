import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title='MES-Application', page_icon=None, layout="centered", 
                   initial_sidebar_state="auto", menu_items=None)

st.title("Capital humain et croissance économique en Côte d'Ivoire")

st.markdown(
    """
    une approche par les équations simultanées

    """
)

st.info("Même l'avenir se demande ce qu'un ISE lui réserve")

st.subheader("Profitez de votre expérience!")


def afficher_profil_sidebar(photo, Noms, Prenom, Email, Tel):
   
    st.sidebar.image(photo, width=200) # Ajustez la largeur selon vos besoins
    st.sidebar.write(f"Nom : {Noms}")
    st.sidebar.write(f"Prénom : {Prenom}")
    st.sidebar.write(f"Email : {Email}")
    st.sidebar.write(f"Téléphone : {Tel}")

afficher_profil_sidebar("ANABA.jpg", "ANABA", "Telesphore","student.rodrigue.anaba@issea-cemac.org", "(237) 6 96 26 90 77")

afficher_profil_sidebar("ANATO.jpg", "ANATO", "Diane", "dianeanato1@gmail.com", "(229) 61 19 24 40")

def display_single_metric_advanced(label, value, delta, unit="", caption="", color_scheme="blue"):
    """Affiche une seule métrique avec un style avancé et personnalisable."""

    color = {
        "blue": {"bg": "#e6f2ff", "text": "#336699", "delta_pos": "#007bff", "delta_neg": "#dc3545"},
        "green": {"bg": "#e6ffe6", "text": "#28a745", "delta_pos": "#28a745", "delta_neg": "#dc3545"},
        "red": {"bg": "#ffe6e6", "text": "#dc3545", "delta_pos": "#28a745", "delta_neg": "#dc3545"},
    }.get(color_scheme, {"bg": "#f0f0f0", "text": "#333", "delta_pos": "#28a745", "delta_neg": "#dc3545"})

    delta_color = color["delta_pos"] if delta >= 0 else color["delta_neg"]

    st.markdown(
        f"""
        <div style="background-color: {color['bg']}; padding: 3px; border-radius: 5px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); text-align: center;">
            <h3 style="color: {color['text']}; margin-bottom: 3px;">{label}</h3>
            <div style="font-size: 2.5em; font-weight: bold; color: {color['text']};">{value} {unit}</div>
            <p style="font-size: 1em; color: {color['text']};">{caption}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )




tables = st.tabs(["Présentation du pays", "Données", "Tableau de Bord","Modélisation","Rapport"])

with tables[0]:
     from utils import Presentation
     Presentation()

with tables[1]:
     df =pd.read_excel('BASE2.xlsx',sheet_name="Data")
     st.write("Aperçu des données :")
     st.dataframe(df)
     st.write("Source: WDI, OMS (2023)")

with tables[2]:
    from utils import Plot
    cl1,cl2,=st.columns(2)
    with cl1:
            display_single_metric_advanced("PIB TOTAL", 78.79, 1, unit="$", color_scheme="green")
    with cl2:
        display_single_metric_advanced("Taux de chômage Moyen", 2.60, 1, unit="%", color_scheme="red")
    Plot()

with tables[4]:
     from utils import show_pdf
     st.title("Visualiseur rapport PDF")
     pdf_path = "Anaba&Anato.pdf"  

     try:
          show_pdf(pdf_path)
     except Exception as e:
        st.error(f"Erreur lors du chargement du PDF : {str(e)}")

    #
     from utils import show_pdf
     st.title("Visualiseur la lettre de recommandation PDF")
     pdf_path = "Lettre.pdf"  

     try:
        from utils import show_pdf1
        show_pdf1(pdf_path)
     except Exception as e:
         st.error(f"Erreur lors du chargement du PDF : {str(e)}")

def generer_donnees_base():
    return pd.read_excel('BASE2.xlsx', sheet_name='Data')
with tables[3]:
    data = pd.read_excel('BASE2.xlsx', sheet_name='Data')
    def simuler_impact(data, variable, choc_pct, coeff_impact, periodes_futures=3):
        """
        Simule l'impact d'un choc sur une variable et ses effets sur les autres variables
        """
        derniere_annee = data['Annee'].max()
        nouvelles_annees = range(derniere_annee + 1, derniere_annee + periodes_futures + 1)
        
        # Copier les dernières valeurs
        dernieres_valeurs = data.iloc[-1].copy()
        
        resultats = []
        valeurs_courantes = dernieres_valeurs.copy()
        
        # Appliquer le choc initial
        valeurs_courantes[variable] *= (1 + choc_pct/100)
        
        for annee in nouvelles_annees:
            # Calculer les impacts sur les autres variables
            if variable != 'PIB':
                valeurs_courantes['PIB'] *= (1 + coeff_impact['PIB']/100)
            if variable != 'ALPHA':
                valeurs_courantes['ALPHA'] *= (1 + coeff_impact['ALPHA']/100)
            if variable != 'DEPSAN':
                valeurs_courantes['DEPSAN'] *= (1 + coeff_impact['DEPSAN']/100)
            
            valeurs_courantes['Annee'] = annee
            resultats.append(valeurs_courantes.copy())
        
        return pd.DataFrame(resultats)

    def main():
        st.title("Simulation de chocs Économiques - Côte d'Ivoire")
        donnees_hist = generer_donnees_base()
        
        # Interface pour le choc
        st.header("Paramètres du choc")
        col1, col2 = st.columns(2)
        
        with col1:
            variable_choc = st.selectbox(
                "Variable affectée par le choc",
                ["PIB", "ALPHA", "DEPSAN"]
            )
            amplitude_choc = st.slider(
                f"Amplitude du choc sur {variable_choc} (%)",
                -50, 50, 0
            )
        
        with col2:
            st.subheader("Coefficients d'impact")
            coeff_impact = {}
            for var in ["PIB", "ALPHA", "DEPSAN"]:
                if var != variable_choc:
                    coeff_impact[var] = st.slider(
                        f"Impact sur {var} (%)",
                        -20, 20, 0
                    )
                else:
                    coeff_impact[var] = 0
        
        # Simulation
        donnees_sim = simuler_impact(donnees_hist, variable_choc, amplitude_choc, coeff_impact)
        
        # Visualisation
        st.header("Résultats de la simulation")

        #cola, colb, colc = st.columns(3)

        
        fig = make_subplots(rows=3, cols=1,
                            subplot_titles=("PIB", "ALPHA", "DEPSAN"),
                            vertical_spacing=0.1)
        
        variables = ['PIB', 'ALPHA', 'DEPSAN']
        colors = {'historique': 'blue', 'simulation': 'red'}
        
        for i, var in enumerate(variables, 1):
            # Données historiques
            fig.add_trace(
                go.Scatter(
                    x=donnees_hist['Annee'],
                    y=donnees_hist[var],
                    name=f"{var} (historique)",
                    line=dict(color=colors['historique']),
                    showlegend=(i == 1)
                ),
                row=i, col=1
            )
            
            # Données simulées
            fig.add_trace(
                go.Scatter(
                    x=donnees_sim['Annee'],
                    y=donnees_sim[var],
                    name=f"{var} (après choc)",
                    line=dict(color=colors['simulation'], dash='dash'),
                    showlegend=(i == 1)
                ),
                row=i, col=1
            )
            
            # Mise en forme
            fig.update_yaxes(title_text=var, row=i, col=1)
        
        fig.update_layout(
            height=800,
            title_text="Impact du choc sur les variables économiques",
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)

    if __name__ == "__main__":
        main()
