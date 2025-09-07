import streamlit as st
from llm_client import query_llm, extract_all_python_code_blocks

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def generer_visualisations(df, column_info, summary, user_input):
    messages = [
        {"role": "system", "content": "Tu es un assistant expert en visualisation de données. Tu aides à créer ou modifier des graphiques en Python avec matplotlib/seaborn/plotly. Fournis uniquement le code Python entre balises markdown."},
        {"role": "user", "content": f"Voici les colonnes : {column_info}. Résumé : {summary}.\n\nL'utilisateur souhaite : {user_input}\n\nPropose exactement trois visualisations graphiques **différentes en type** (ex : histogramme, nuage de points, camembert, boxplot, courbe, heatmap, etc.), toutes pertinentes pour cette demande.\n\nPour chaque visualisation :\n- Donne uniquement le code Python\n- Place chaque code dans une balise markdown ```python\n-Utilise si possible des bibliothèques variées (matplotlib, seaborn, plotly)\n- Ne commente rien, ne discute pas, donne simplement trois blocs de code consécutifs."}
    ]
    raw_response = query_llm(messages)
    code_blocks = extract_all_python_code_blocks(raw_response)

    st.session_state["total_expected"] = 3
    st.session_state["total_valid"] = 0

    valid_codes = []
    for i, code in enumerate(code_blocks):
        try:
            local_env = {"df": df.copy(), "plt": plt, "sns": sns, "px": px}
            exec(code, {}, local_env)
            valid_codes.append(code)
        except Exception as e:
            st.warning(f"⚠️ Option {i+1} ignorée : code invalide. Détail : {e}")

    st.session_state["total_valid"] = len(valid_codes)

    if not valid_codes:
        st.error("❌ Aucune visualisation exécutable. Essayez une autre instruction.")
    else:
        st.session_state["last_response"] = raw_response
        st.session_state["last_codes"] = valid_codes
        st.session_state["last_input"] = user_input
        st.rerun()
