import streamlit as st
from visualizer import exec_code
from llm_client import query_llm, extract_all_python_code_blocks
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def afficher_et_choisir_visualisation(df):
    st.subheader("Choisissez une visualisation")
    for idx, code in enumerate(st.session_state["last_codes"]):
        with st.expander(f"Option {idx+1}"):
            st.code(code, language="python")
            exec_code(code, df)
            if st.button(f"✅ Choisir cette visualisation", key=f"select_{idx}"):
                st.session_state["chat_history"].append({"role": "user", "content": st.session_state["last_input"]})
                st.session_state["chat_history"].append({"role": "assistant", "content": f"```python\n{code}\n```"})
                for k in ["last_codes", "last_response", "last_input"]:
                    st.session_state[k] = [] if isinstance(st.session_state[k], list) else ""
                st.rerun()

def regenerer_si_manquant(df):
    if st.session_state.get("total_valid", 0) < st.session_state.get("total_expected", 3):
        missing = st.session_state["total_expected"] - st.session_state["total_valid"]
        if st.button(f"🔁 Regénérer {missing} visualisation(s) manquante(s)"):
            existing_codes = st.session_state["last_codes"]
            already_used = "\n\n".join([f"```python\n{code}\n```" for code in existing_codes])
            user_msg = (
                f"L'utilisateur a reçu {st.session_state['total_valid']} visualisation(s) valides "
                f"sur les 3 attendues. Voici ce qui a déjà été généré :\n\n{already_used}\n\n"
                f"Propose {missing} nouvelle(s) visualisation(s) différente(s). "
                f"Utilise d'autres types ou bibliothèques si possible."
            )
            messages = [
                {"role": "system", "content": "Tu es un expert en visualisation. Fournis uniquement du code Python dans des balises ```python."},
                {"role": "user", "content": user_msg}
            ]
            response = query_llm(messages)
            new_blocks = extract_all_python_code_blocks(response)

            for code in new_blocks:
                if code.strip() not in [c.strip() for c in existing_codes]:
                    try:
                        local_env = {"df": df.copy(), "plt": plt, "sns": sns, "px": px}
                        exec(code, {}, local_env)
                        st.session_state["last_codes"].append(code)
                        st.session_state["total_valid"] += 1
                    except Exception as e:
                        st.warning(f"❌ Nouveau code invalide ignoré. Erreur : {e}")
                else:
                    st.info("⚠️ Visualisation ignorée : déjà présente.")
            st.rerun()
