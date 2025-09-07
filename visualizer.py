import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import contextlib
from io import StringIO

def exec_code(code_str, df):
    local_vars = {
        "df": df, "plt": plt, "sns": sns, "px": px, "st": st
    }
    try:
        with contextlib.redirect_stdout(StringIO()):
            exec(code_str, {}, local_vars)

        # Affichage Matplotlib
        fig = plt.gcf()
        if fig.get_axes():  # vérifie s'il y a un graphe à afficher
            st.pyplot(fig)
            plt.clf()

        # Vérifie si un objet Plotly est généré (optionnel)
        if "fig" in local_vars and hasattr(local_vars["fig"], "to_dict"):
            st.plotly_chart(local_vars["fig"])

    except Exception as e:
        st.error(f"Erreur lors de l'exécution du code généré : {e}")