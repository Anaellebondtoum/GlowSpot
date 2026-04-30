import streamlit as st
from PIL import Image
import pandas as pd # Ajouté pour les statistiques
from supabase import create_client, Client # Ajouté pour la fiabilité

# 1. Configuration
st.set_page_config(page_title="GlowSpot", page_icon="✨", layout="wide")

# CONNEXION SUPABASE
URL_SUPABASE = "https://qggjaghlpoeenqmnfvoa.supabase.co" 
KEY_SUPABASE = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFnZ2phZ2hscG9lZW5xbW5mdm9hIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc0OTUxNDcsImV4cCI6MjA5MzA3MTE0N30.lQLAp849nsbFWpt919iJiWzWSsl6QeXwpFLK31yF9RM"

try:
    supabase: Client = create_client(URL_SUPABASE, KEY_SUPABASE)
except:
    st.error("Lien Supabase non configuré. L'application tourne en mode local.")

# FONCTIONS DE COLLECTE 
def inscription_supabase(u, p, n, s, q, r):
    data = {"username": u, "password": p, "nom": n, "sexe": s, "quartier": q, "role": r}
    supabase.table("profiles").insert(data).execute()

#  DESIGN & BACKGROUND 
bg_img = "https://img.magnific.com/vecteurs-libre/vecteur-fond-degrade-bleu-simple-pour-entreprises_53876-161578.jpg?semt=ais_hybrid&w=740" 
side_img = "https://www.culture-coiffure.fr/wp-content/uploads/2024/08/relation-client-en-coiffure.webp"

st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{bg_img}");
        background-size: cover;
        background-attachment: fixed;
    }}
    .main-title {{ font-family: 'Playfair Display', serif; font-size: 4rem; color: #D4A373; text-align: center; margin-bottom: 0; }}
    .subtitle {{ text-align: center; color: #6c757d; font-style: italic; font-size: 1.2rem; margin-bottom: 2rem; }}
    .card {{ background: rgba(255, 255, 255, 0.9); padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 10px; }}
    </style>
    """, unsafe_allow_html=True)

# INITIALISATION 
if 'users_db' not in st.session_state: st.session_state['users_db'] = {}
if 'salons_db' not in st.session_state: st.session_state['salons_db'] = []
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'current_user' not in st.session_state: st.session_state['current_user'] = None

# NAVIGATION 
if not st.session_state['logged_in']:
    st.markdown("<h1 class='main-title'>GlowSpot</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Révélez votre éclat, trouvez votre salon</p>", unsafe_allow_html=True)
    
    col_img, col_form = st.columns([1, 1])
    
    with col_img:
        images_defile = [
            "https://www.culture-coiffure.fr/wp-content/uploads/2024/08/relation-client-en-coiffure.webp", 
            "https://www.franchisemarket.ph/application/files/cache/thumbnails/c0dcf739253fee4f66deb544b4db371d.jpg", 
            "https://i.pinimg.com/736x/0c/48/c9/0c48c9e1ffd220a85df1fc155d476f32.jpg"
        ]
        
        if 'img_idx' not in st.session_state:
            st.session_state.img_idx = 0
            
        st.image(images_defile[st.session_state.img_idx], use_container_width=True)
        
        if st.button("Suivant"):
            st.session_state.img_idx = (st.session_state.img_idx + 1) % len(images_defile)
            st.rerun()
        
    with col_form:
        tab_in, tab_up = st.tabs([" Connexion", " Rejoindre GlowSpot"])
        
        with tab_up:
            new_role = st.selectbox("Je suis un...", ["Client(e)", "Salon de Coiffure"])
            new_u = st.text_input("Identifiant (Username)")
            new_p = st.text_input("Mot de passe", type="password")
            new_n = st.text_input("Nom complet / Nom du Salon")
            new_s = st.radio("Sexe", ["Femme", "Homme"], horizontal=True)
            new_q = st.selectbox("Quartier", ["Bastos", "Akwa", "Bonapriso", "Messa", "Oloumi"])
            
            if st.button("Créer mon compte"):
                if new_u in st.session_state['users_db']:
                    st.error("Cet identifiant existe déjà.")
                else:
                    # Envoi vers Supabase (Collecte Réelle)
                    try:
                        inscription_supabase(new_u, new_p, new_n, new_s, new_q, new_role)
                    except:
                        pass
                    
                    # Sauvegarde locale (Session)
                    user_info = {
                        "pwd": new_p, "role": new_role, "nom": new_n, 
                        "sexe": new_s, "quartier": new_q, "photo": None, "catalogue": []
                    }
                    st.session_state['users_db'][new_u] = user_info
                    if new_role == "Salon de Coiffure":
                        st.session_state['salons_db'].append(new_u)
                    st.success("Inscription réussie et collectée ! Connectez-vous.")

        with tab_in:
            u = st.text_input("Utilisateur")
            p = st.text_input("Mot de passe", type="password", key="login_p")
            if st.button("Entrer dans GlowSpot"):
                if u in st.session_state['users_db'] and st.session_state['users_db'][u]['pwd'] == p:
                    st.session_state['logged_in'] = True
                    st.session_state['current_user'] = u
                    st.rerun()
                else:
                    st.error("Identifiants incorrects.")

else:
    user_id = st.session_state['current_user']
    user_data = st.session_state['users_db'][user_id]
    
    with st.sidebar:
        st.markdown(f"## ✨ GlowSpot")
        if user_data['photo']: st.image(user_data['photo'], width=100)
        st.write(f"Bonjour, **{user_data['nom']}**")
        # Ajout de l'onglet Statistiques pour le prof
        nav = st.radio("Menu", ["Dashboard", "📊 Statistiques", "👤 Mon Profil", "📁 Mon Espace", "🚪 Déconnexion"])

    # --- 1. DASHBOARD ---
    if nav == "Dashboard":
        if user_data['role'] == "Salon de Coiffure":
            st.title("Tableau de bord Pro")
            st.metric("Clients intéressés", "0")
            st.info("Votre salon est prêt. Ajoutez des coiffures dans 'Mon Espace' pour être visible.")
        else:
            st.title("Trouvez votre style aujourd'hui")
            st.text_input("🔍 Que voulez-vous aujourd'hui ?", placeholder="Tresses, Dégradé, Manucure...")
            
            st.subheader(f"Salons à {user_data['quartier']} et alentours")
            if not st.session_state['salons_db']:
                st.warning("Aucun salon n'est encore inscrit sur la plateforme.")
            else:
                for s_id in st.session_state['salons_db']:
                    s_data = st.session_state['users_db'][s_id]
                    with st.container():
                        st.markdown(f"""
                        <div class='card'>
                            <h3>{s_data['nom']}</h3>
                            <p>📍 {s_data['quartier']} | Sexe ciblé : {s_data['sexe']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"Voir le catalogue de {s_data['nom']}", key=s_id):
                            st.session_state['viewing_salon'] = s_id
                
                if 'viewing_salon' in st.session_state:
                    view_id = st.session_state['viewing_salon']
                    view_data = st.session_state['users_db'][view_id]
                    st.divider()
                    st.header(f"Catalogue de {view_data['nom']}")
                    if not view_data['catalogue']:
                        st.write("Ce salon n' pas encore posté de photos.")
                    else:
                        cols = st.columns(3)
                        for i, item in enumerate(view_data['catalogue']):
                            with cols[i%3]:
                                st.image(item['img'], caption=f"{item['nom']} - {item['prix']} FCFA")
                                st.button("Réserver ce style", key=f"book_{i}")

    # ANALYSE DES DONNÉES 
    elif nav == "📊 Statistiques":
        st.title("Analyse Descriptive des Données")
        st.write("Visualisation de la répartition des utilisateurs par quartier.")
        
        # On crée un petit tableau pour le graphique à partir des données collectées
        if st.session_state['users_db']:
            df = pd.DataFrame([v for k, v in st.session_state['users_db'].items()])
            st.bar_chart(df['quartier'].value_counts())
        else:
            st.info("Inscrivez quelques utilisateurs pour voir l'analyse.")

    elif nav == "👤 Mon Profil":
        st.title("Modifier mon Profil")
        col1, col2 = st.columns(2)
        with col1:
            user_data['nom'] = st.text_input("Nom", user_data['nom'])
            user_data['pwd'] = st.text_input("Nouveau mot de passe", user_data['pwd'], type="password")
        with col2:
            user_data['sexe'] = st.radio("Sexe", ["Femme", "Homme", "Autre"], index=["Femme", "Homme", "Autre"].index(user_data['sexe']))
            up_photo = st.file_uploader("Photo de profil", type=['jpg','png'])
            if up_photo: user_data['photo'] = up_photo
        
        if st.button("Enregistrer les modifications"):
            st.success("Profil mis à jour !")

    elif nav == "📁 Mon Espace":
        if user_data['role'] == "Salon de Coiffure":
            st.title("Gestion de mon Catalogue")
            with st.expander("➕ Ajouter une coiffure"):
                n = st.text_input("Nom de la coiffure")
                p = st.number_input("Prix", step=500)
                img = st.text_input("URL de l'image")
                if st.button("Publier"):
                    user_data['catalogue'].append({"nom": n, "prix": p, "img": img})
                    st.rerun()
            
            st.subheader("Mes publications")
            for i, item in enumerate(user_data['catalogue']):
                col_a, col_b = st.columns([3, 1])
                col_a.write(f"**{item['nom']}** - {item['prix']} FCFA")
                if col_b.button("🗑️", key=f"del_{i}"):
                    user_data['catalogue'].pop(i)
                    st.rerun()
        else:
            st.title("Mes Réservations")
            st.write("Vous n'avez pas encore de rendez-vous.")

    elif nav == "🚪 Déconnexion":
        st.session_state['logged_in'] = False
        st.rerun()