# ==============================================================================
# PORTAIL WEB OFFICIEL - CLINIQUE LES BAOBABS
# ==============================================================================
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import datetime
import os
import plotly.express as px

# Configuration de la page
st.set_page_config(
    page_title="Clinique Les Baobabs - Portail Médical",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Feuille de style CSS (Thème Institutionnel Santé - Vert & Marron discret, sans emojis)
st.markdown("""
    <style>
    .main {
        background-color: #F8F9FA;
    }
    h1, h2, h3, h4 {
        color: #1B4D3E !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    .stButton>button {
        background-color: #1B4D3E;
        color: white;
        border-radius: 4px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #2E7D32;
        color: white;
    }
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 6px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border-left: 4px solid #8D5524;
        border-top: 1px solid #E0E0E0;
        border-right: 1px solid #E0E0E0;
        border-bottom: 1px solid #E0E0E0;
    }
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E0E0E0;
    }
    </style>
""", unsafe_allow_html=True)

# Connexion à la base de données MySQL
@st.cache_resource
def get_engine():
    mot_de_passe = "fAtima@2002"
    password_securise = quote_plus(mot_de_passe)
    return create_engine(f"mysql+pymysql://root:{password_securise}@localhost:3306/medirdv?charset=utf8mb4")

engine = get_engine()
date_pivot = datetime.date(2026, 9, 28)

# En-tête institutionnel avec logo
col_logo, col_titre = st.columns([1, 6])
with col_logo:
    logo_path = None
    for possible_path in ["logo_clinique_les_baobabs.png", "App/logo_clinique_les_baobabs.png"]:
        if os.path.exists(possible_path):
            logo_path = possible_path
            break
    if logo_path:
        st.image(logo_path, width=90)
    else:
        st.markdown("**Clinique Les Baobabs**")

with col_titre:
    st.title("Clinique Les Baobabs")
    st.markdown("**Portail de Gestion Médicale et d'Analyse** - Dakar, Sénégal")

st.markdown("---")

# Navigation principale structurée par catégories professionnelles
st.sidebar.markdown("### Navigation du Portail")
st.sidebar.markdown("---")

categorie = st.sidebar.radio(
    "Espaces Métiers",
    ["Accueil & Pilotage", "Espace Patient", "Espace Medecin", "Administration", "Analyses & Statistiques"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Paramètres")
session_role = st.sidebar.selectbox("Profil Actif", ["Agent d'accueil", "Medecin", "Responsable des operations", "Administrateur"])

# ==============================================================================
# CATEGORIE 1 : ACCUEIL & PILOTAGE
# ==============================================================================
if categorie == "Accueil & Pilotage":
    st.header("Tableau de Bord General")
    st.markdown("Suivi en temps réel des indicateurs d'activité de la clinique.")
    
    try:
        query_kpi = f"""
            SELECT 
                COUNT(*) AS total_rdv,
                SUM(CASE WHEN statut = 'Honore' THEN 1 ELSE 0 END) AS nb_honores,
                SUM(CASE WHEN statut = 'Absent' THEN 1 ELSE 0 END) AS nb_absents,
                SUM(CASE WHEN statut = 'Annule' THEN 1 ELSE 0 END) AS nb_annules
            FROM rendez_vous
            WHERE DATE(date_rdv) <= '{date_pivot}'
        """
        df_kpi = pd.read_sql(query_kpi, con=engine)
        
        if not df_kpi.empty:
            tot = df_kpi['total_rdv'].iloc[0] or 0
            hon = df_kpi['nb_honores'].iloc[0] or 0
            abs_rdv = df_kpi['nb_absents'].iloc[0] or 0
            ann = df_kpi['nb_annules'].iloc[0] or 0
            
            evalues = hon + abs_rdv
            taux_abs = (abs_rdv / evalues * 100) if evalues > 0 else 0
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Consultations Totales", f"{int(tot):,}")
            c2.metric("Rendez-vous Honores", f"{int(hon):,}")
            c3.metric("Absences Enregistrees", f"{int(abs_rdv):,}")
            c4.metric("Taux d'Absence Global", f"{taux_abs:.1f}%")
            
        st.markdown("---")
        
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.subheader("Distribution des Statuts")
            df_statut = pd.read_sql("SELECT statut, COUNT(*) as count FROM rendez_vous GROUP BY statut", con=engine)
            if not df_statut.empty:
                fig_pie = px.pie(
                    df_statut, 
                    names='statut', 
                    values='count', 
                    hole=0.4, 
                    color_discrete_sequence=['#1B4D3E', '#2E7D32', '#8D5524', '#A5D6A7']
                )
                st.plotly_chart(fig_pie, use_container_width=True)
                
        with col_g2:
            st.subheader("Volume par Specialite")
            query_top_spec = """
                SELECT s.nom_specialite AS Specialite, COUNT(r.id_rdv) AS Total
                FROM rendez_vous r
                JOIN medecin m ON r.id_medecin = m.id_medecin
                JOIN specialite s ON m.id_specialite = s.id_specialite
                GROUP BY s.nom_specialite
                ORDER BY Total DESC
            """
            df_top = pd.read_sql(query_top_spec, con=engine)
            if not df_top.empty:
                fig_bar = px.bar(
                    df_top, 
                    x='Specialite', 
                    y='Total', 
                    color_discrete_sequence=['#1B4D3E']
                )
                st.plotly_chart(fig_bar, use_container_width=True)

    except Exception as e:
        st.error(f"Erreur de chargement du tableau de bord : {e}")

# ==============================================================================
# CATEGORIE 2 : ESPACE PATIENT (DOSSIERS ET PRISES DE RDV)
# ==============================================================================
elif categorie == "Espace Patient":
    st.header("Espace Patient - Gestion et Prise de Rendez-vous")
    
    tab_p1, tab_p2 = st.tabs(["Nouveau Rendez-vous", "Repertoire et Fiches Patients"])
    
    with tab_p1:
        st.subheader("Enregistrement d'une Consultation")
        try:
            df_patients = pd.read_sql("SELECT id_patient, CONCAT(nom, ' ', prenom, ' (', id_patient, ')') AS identite FROM patient", con=engine)
            df_medecins = pd.read_sql("SELECT id_medecin, CONCAT(nom, ' (', id_medecin, ')') AS identite_med FROM medecin", con=engine)
            
            with st.form("form_rdv_patient"):
                c1, c2 = st.columns(2)
                with c1:
                    patient_selection = st.selectbox("Patient concerne", options=df_patients['identite'].tolist())
                    date_rdv = st.date_input("Date du rendez-vous", datetime.date.today())
                    heure_rdv = st.time_input("Heure", datetime.time(9, 0))
                with c2:
                    medecin_selection = st.selectbox("Medecin referent", options=df_medecins['identite_med'].tolist())
                    statut_rdv = st.selectbox("Statut initial", ["Planifie", "Confirme"])
                    confirmation_sms = st.checkbox("Confirmation SMS activee", value=False)
                    
                motif = st.text_input("Motif de consultation")
                valider_rdv = st.form_submit_button("Confirmer la reservation")
                
                if valider_rdv:
                    id_pat_reel = patient_selection.split("(")[-1].replace(")", "").strip()
                    id_med_reel = medecin_selection.split("(")[-1].replace(")", "").strip()
                    
                    import random
                    code_rdv_gen = f"RDV{random.randint(90000, 99999)}"
                    dt_rdv_str = datetime.datetime.combine(date_rdv, heure_rdv).strftime('%Y-%m-%d %H:%M:%S')
                    dt_prise_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    insert_query = f"""
                        INSERT INTO rendez_vous (id_rdv_code, id_patient, id_medecin, date_prise, date_rdv, statut, confirmation_sms)
                        VALUES ('{code_rdv_gen}', '{id_pat_reel}', '{id_med_reel}', '{dt_prise_str}', '{dt_rdv_str}', '{statut_rdv}', {1 if confirmation_sms else 0})
                    """
                    with engine.begin() as conn:
                        conn.exec_driver_sql(insert_query)
                    st.success(f"Rendez-vous cree avec succes. Reference : {code_rdv_gen}")
        except Exception as e:
            st.error(f"Erreur formulaire : {e}")
            
    with tab_p2:
        st.subheader("Repertoire Centralise des Patients")
        try:
            recherche = st.text_input("Recherche par nom, prenom ou telephone :")
            sql_pat = "SELECT id_patient AS 'ID Patient', nom AS 'Nom', prenom AS 'Prenom', date_naissance AS 'Date de Naissance', sexe AS 'Sexe', telephone AS 'Telephone' FROM patient"
            if recherche:
                sql_pat += f" WHERE nom LIKE '%{recherche}%' OR prenom LIKE '%{recherche}%' OR telephone LIKE '%{recherche}%'"
            sql_pat += " LIMIT 100"
            df_patients_list = pd.read_sql(sql_pat, con=engine)
            st.dataframe(df_patients_list, use_container_width=True)
        except Exception as e:
            st.error(f"Erreur lecture répertoire : {e}")

# ==============================================================================
# CATEGORIE 3 : ESPACE MEDECIN (PLANNINGS ET STATUTS)
# ==============================================================================
elif categorie == "Espace Medecin":
    st.header("Espace Medecin - Plannings et Consultations")
    
    try:
        df_meds = pd.read_sql("SELECT id_medecin, CONCAT(nom, ' (', id_medecin, ')') AS info_med FROM medecin", con=engine)
        medecin_choisi = st.selectbox("Selectionner le medecin connecte", options=df_meds['info_med'].tolist())
        id_med_actif = medecin_choisi.split("(")[-1].replace(")", "").strip()
        
        st.markdown("### Agenda des Rendez-vous")
        query_planning = f"""
            SELECT 
                r.id_rdv_code AS 'Code',
                r.date_rdv AS 'Date et Heure',
                p.nom AS 'Nom Patient',
                p.prenom AS 'Prenom Patient',
                p.telephone AS 'Contact',
                r.statut AS 'Statut'
            FROM rendez_vous r
            JOIN patient p ON r.id_patient = p.id_patient
            WHERE r.id_medecin = '{id_med_actif}'
            ORDER BY r.date_rdv DESC
            LIMIT 50
        """
        df_plan = pd.read_sql(query_planning, con=engine)
        if df_plan.empty:
            st.info("Aucun rendez-vous attribue pour le moment.")
        else:
            st.dataframe(df_plan, use_container_width=True)
            
    except Exception as e:
        st.error(f"Erreur d'accès au planning medecin : {e}")

# ==============================================================================
# CATEGORIE 4 : ADMINISTRATION (PARAMETRES ET SOURCE)
# ==============================================================================
elif categorie == "Administration":
    st.header("Administration - Parametres et Donnees Source")
    
    tab_a1, tab_a2 = st.tabs(["Gestion des Medecins & Specialites", "Fichier Source CSV"])
    
    with tab_a1:
        st.subheader("Equipe Medicale et Specialites")
        try:
            df_m_list = pd.read_sql("""
                SELECT m.id_medecin AS 'ID', m.nom AS 'Nom', s.nom_specialite AS 'Specialite'
                FROM medecin m
                JOIN specialite s ON m.id_specialite = s.id_specialite
            """, con=engine)
            st.dataframe(df_m_list, use_container_width=True)
        except Exception as e:
            st.error(f"Erreur : {e}")
            
    with tab_a2:
        st.subheader("Visualisation du Fichier Nettoye")
        clean_file_path = "data/clean/rendez_vous_medirdv_propre.csv"
        if os.path.exists(clean_file_path):
            try:
                df_clean = pd.read_csv(clean_file_path)
                st.dataframe(df_clean.head(100), use_container_width=True)
            except Exception as e:
                st.error(f"Erreur lecture CSV : {e}")
        else:
            st.warning("Le fichier `rendez_vous_medirdv_propre.csv` est introuvable dans le dossier `data/clean/`.")

# ==============================================================================
# CATEGORIE 5 : ANALYSES & STATISTIQUES
# ==============================================================================
elif categorie == "Analyses & Statistiques":
    st.header("Analyses de Gestion et Indicateurs Avances")
    
    try:
        query_abs_spec = """
            SELECT 
                s.nom_specialite AS Specialite,
                ROUND(SUM(CASE WHEN r.statut = 'Absent' THEN 1 ELSE 0 END) * 100.0 / 
                NULLIF(SUM(CASE WHEN r.statut IN ('Honore', 'Absent') THEN 1 ELSE 0 END), 0), 2) AS Taux_Absence
            FROM rendez_vous r
            JOIN medecin m ON r.id_medecin = m.id_medecin
            JOIN specialite s ON m.id_specialite = s.id_specialite
            GROUP BY s.nom_specialite
        """
        df_abs = pd.read_sql(query_abs_spec, con=engine)
        if not df_abs.empty:
            fig_abs = px.bar(
                df_abs, 
                x='Specialite', 
                y='Taux_Absence', 
                title="Taux d'Absence par Specialite (%)",
                color_discrete_sequence=['#8D5524']
            )
            st.plotly_chart(fig_abs, use_container_width=True)
            
    except Exception as e:
        st.error(f"Erreur lors de la generation des graphiques analytiques : {e}")