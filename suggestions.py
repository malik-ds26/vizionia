import streamlit as st
from llm_client import get_suggestion_prompts

def afficher_et_gérer_suggestions(column_info):
    st.subheader("Suggestions de visualisations")
    
    if st.button("🎯 Obtenir des suggestions automatiques"):
        suggestions = get_suggestion_prompts(column_info)
        st.session_state["suggestions"] = suggestions

    for suggestion in st.session_state.get("suggestions", "").split("\n"):
        suggestion = suggestion.strip()
        if suggestion and st.button(suggestion):
            st.session_state["user_input"] = suggestion
            st.rerun()
