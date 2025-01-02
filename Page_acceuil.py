import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='MES-Application', page_icon=None, layout="centered", 
                   initial_sidebar_state="auto", menu_items=None)

st.title("Capital humain et croissance économique en Côte d'Ivoire")

st.markdown(
    """
    une approche par les équations simultanées

    """
)

st.info("Cliquez sur le menu latéral de gauche pour naviguer vers les différentes applications.")

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
            <div style="font-size: 1.5em; color: {delta_color};">{'▲' if delta >= 0 else '▼'} {abs(delta)}</div>
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
            display_single_metric_advanced("PIB TOTAL", 78.79, 1, unit="$", caption="Total", color_scheme="green")
    with cl2:
        display_single_metric_advanced("Taux de chômage Moyen", 2.60, 1, unit="%", caption="Maximun", color_scheme="red")
    Plot()

with tables[4]:
     from utils import show_pdf
     st.title("Visualiseur de PDF")
     pdf_path = "Anaba&Anato.pdf"  

     try:
          show_pdf(pdf_path)
     except Exception as e:
        st.error(f"Erreur lors du chargement du PDF : {str(e)}")
