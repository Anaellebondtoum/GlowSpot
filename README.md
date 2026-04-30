# GlowSpot | Beauty Connect & Data Analytics

**GlowSpot** est une application web de collecte et d'analyse descriptive des données dédiée au secteur de la beauté. Elle permet de connecter les clients aux salons de coiffure tout en offrant des outils de pilotage statistique pour les professionnels.

> **Lien direct vers l'application :** [Accéder à GlowSpot](https://bondtoum-ndzie-anaelle-aurore-24f2605.streamlit.app/)
##  Informations Étudiant
* **Nom :** BONDTOUM NDZIE Anaelle Aurore
* **Matricule :** 24F2605
* **UE :** INF232 - EC2 (Analyse de données)
* **Date :** Avril 2026
## Fonctionnalités Clés
- **Collecte de Données (Fiabilité) :** Système d'inscription et de connexion robuste stockant les profils (nom, sexe, quartier, rôle) dans une base de données cloud **Supabase**.
- **Analyse Descriptive (Efficacité) :** Dashboard statistique intégré utilisant **Pandas** et **Plotly** pour visualiser la répartition des clients par zone géographique et par besoin.
- **Gestion de Catalogue :** Interface permettant aux salons de publier, modifier ou supprimer leurs prestations en temps réel.
- **Expérience Utilisateur (Créativité) :** Design moderne, interface responsive et navigation fluide entre les rôles Client et Professionnel.

---

## Stack Technique
* **Frontend :** [Streamlit](https://streamlit.io/)
* **Backend :** Python 3.12
* **Base de données :** [Supabase](https://supabase.com/) (PostgreSQL)
* **Visualisation :** Plotly Express / Pandas
* **Hébergement :** Streamlit Community Cloud

---

## Installation & Déploiement Local
Pour tester le projet sur votre machine :
1. Cloner le dépôt :
   ```bash
   git clone [https://github.com/](https://github.com/)[AnaelleBondtoum]/GlowSpot.git
2.Installer les dépendances et lancer l'application :
 ```bash
pip install -r requirements.txt
streamlit run app.py
