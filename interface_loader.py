import streamlit as st
from data_analyzer import load_csv, get_column_info, get_summary

def afficher_upload_et_resume():
    uploaded_file = st.file_uploader("Chargez un fichier CSV", type=["csv", "xls", "xlsx", "json"])
    if uploaded_file:
        df = load_csv(uploaded_file)
        st.write("Aperçu des données", df.head())

        column_info = get_column_info(df)
        summary = get_summary(df)

        st.subheader("Types de colonnes")
        st.json(column_info)

        st.subheader("Résumé statistique")
        st.markdown("""<style>.styled-table th, .styled-table td { padding: 4px 8px; border: 1px solid #ccc; } .styled-table { border-collapse: collapse; width: 100%; } .styled-table th { background-color: #444; color: white; }</style>""", unsafe_allow_html=True)
        st.markdown(summary, unsafe_allow_html=True)

        return df, column_info, summary
    return None, None, None
