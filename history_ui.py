import streamlit as st
import io
import matplotlib.pyplot as plt
from llm_client import extract_python_code
from visualizer import exec_code
from interpretation import get_interpretation_from_code

def afficher_historique(df):
    st.subheader("Historique interactif")
    for i in range(0, len(st.session_state["chat_history"]), 2):
        if i + 1 >= len(st.session_state["chat_history"]):
            continue

        user_msg = st.session_state["chat_history"][i]
        assistant_msg = st.session_state["chat_history"][i + 1]

        col1, col2, col3, col4 = st.columns([0.65, 0.10, 0.10, 0.15])
        with col1:
            if st.button(user_msg["content"], key=f"replay_{i}"):
                code = extract_python_code(assistant_msg["content"])
                st.subheader("Code relancé")
                st.code(code, language="python")
                exec_code(code, df)
        with col2:
            if st.button("🗑️", key=f"delete_{i}"):
                del st.session_state["chat_history"][i:i+2]
                st.rerun()
        with col3:
            if st.button("⬇️", key=f"download_{i}"):
                code = extract_python_code(assistant_msg["content"])
                buf = io.BytesIO()
                plt.figure()
                try:
                    exec(code, {"df": df, "plt": plt})
                    plt.savefig(buf, format="png", bbox_inches="tight")
                    plt.close()
                    buf.seek(0)

                    st.download_button(
                        label="📥 Télécharger le graphique (PNG)",
                        data=buf,
                        file_name="graphique.png",
                        mime="image/png",
                        key=f"download_button_{i}"
                    )
                    st.download_button(
                        label="📄 Télécharger le code (PY)",
                        data=code.encode("utf-8"),
                        file_name="graphique.py",
                        mime="text/x-python",
                        key=f"code_button_{i}"
                    )
                except Exception as e:
                    st.error(f"Erreur lors de l'exécution du code : {e}")
        with col4:
            if st.button("🧠", key=f"interpret_{i}"):
                code = extract_python_code(assistant_msg["content"])
                interpretation = get_interpretation_from_code(code)
                st.download_button(
                    label="📄 Télécharger l'interprétation (.txt)",
                    data=interpretation,
                    file_name="interpretation.txt",
                    mime="text/plain",
                    key=f"download_interpretation_{i}"
                )
