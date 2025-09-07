import streamlit as st
from interface_loader import afficher_upload_et_resume
from suggestions import afficher_et_gérer_suggestions
from chat_handler import generer_visualisations
from visual_selector import afficher_et_choisir_visualisation, regenerer_si_manquant
from history_ui import afficher_historique
from graph_editor import modifier_derniere_visualisation

st.set_page_config(layout="wide", page_title="VizionIA - Assistant de Visualisation", page_icon="image/observation.ico")

# --- Initialisation des états ---
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "suggestions" not in st.session_state:
    st.session_state["suggestions"] = ""
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""
if "last_response" not in st.session_state:
    st.session_state["last_response"] = ""
if "last_codes" not in st.session_state:
    st.session_state["last_codes"] = []
if "last_input" not in st.session_state:
    st.session_state["last_input"] = ""

# --- UI ---
st.markdown("""
<style>
    body { background-color: #0e1117; color: #ffffff; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1, h2, h3 { color: #6dd5ed; }
    .stButton>button {
        background-color: #1f77b4; color: white; border-radius: 8px;
        padding: 0.4em 1em;
    }
    .stButton>button:hover { background-color: #145b91; }
</style>
<div style='display: flex; justify-content: space-between; align-items: center; background-color: #1a1a1a; padding: 1rem 2rem; border-radius: 10px;'>
    <h1 style='margin: 0; font-size: 2.5rem;'>VizionIA</h1>
</div>
<hr style='margin-top: 1rem; margin-bottom: 2rem;'>
""", unsafe_allow_html=True)

# --- Réinitialisation ---
if st.button("🔄 Réinitialiser la conversation"):
    for key in ["chat_history", "suggestions", "user_input", "last_response", "last_codes", "last_input"]:
        st.session_state[key] = [] if "history" in key else ""
    st.rerun()

# --- Chargement CSV ---
df, column_info, summary = afficher_upload_et_resume()

if df is not None:
    # --- Suggestions ---
    afficher_et_gérer_suggestions(column_info)

    # --- Dialogue LLM ---
    st.subheader("Dialogue avec le LLM")
    user_input = st.text_input("Entrez une instruction", key="user_input")
    if user_input and st.button("Envoyer"):
        generer_visualisations(df, column_info, summary, user_input)

    # --- Visualisations proposées ---
    if st.session_state.get("last_codes"):
        afficher_et_choisir_visualisation(df)
        regenerer_si_manquant(df)

    # --- Historique + Édition ---
    afficher_historique(df)
    modifier_derniere_visualisation(df)
