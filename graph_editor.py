import streamlit as st
from llm_client import query_llm, extract_python_code
from visualizer import exec_code

def modifier_derniere_visualisation(df):
    if st.session_state.get("chat_history"):
        last_user_msg = st.session_state["chat_history"][-2] if len(st.session_state["chat_history"]) >= 2 else None
        last_assistant_msg = st.session_state["chat_history"][-1] if len(st.session_state["chat_history"]) >= 2 else None

        if last_user_msg and last_assistant_msg and last_assistant_msg["role"] == "assistant":
            previous_code = extract_python_code(last_assistant_msg["content"])

            st.subheader("💬 Modifier cette visualisation")
            modif_input = st.text_input("Décris la modification souhaitée")

            if st.button("Appliquer la modification") and modif_input:
                prompt = f"Voici le code original :\n```python\n{previous_code}\n```\nVoici la modification souhaitée : {modif_input}"

                messages = [
                    {
                        "role": "system",
                        "content": "Tu es un assistant expert en visualisation Python. Tu reçois un code existant, ainsi qu'une demande utilisateur pour le modifier. Applique uniquement cette modification. Ne renvoie que le code corrigé, dans une balise markdown ```python."
                    },
                    {"role": "user", "content": prompt}
                ]

                raw_modif = query_llm(messages)
                new_code = extract_python_code(raw_modif)

                st.subheader("Visualisation modifiée")
                st.code(new_code, language="python")
                exec_code(new_code, df)

                st.session_state["chat_history"].append({"role": "user", "content": modif_input})
                st.session_state["chat_history"].append({"role": "assistant", "content": f"```python\n{new_code}\n```"})
                st.rerun()
