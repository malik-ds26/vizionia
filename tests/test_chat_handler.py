import pytest
from unittest.mock import patch
import pandas as pd
import streamlit as st

from chat_handler import generer_visualisations

# 🔧 Fixture : DataFrame d'exemple
@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "Age": [20, 30, 40],
        "Score": [80.5, 90.0, 85.0]
    })

# 🧪 Test : génération de 3 visualisations avec LLM mocké
@patch("chat_handler.query_llm")
def test_generer_visualisations_valid(mock_query, sample_df):
    # Réinitialisation de la session state
    st.session_state.clear()

    # Simule une réponse LLM avec 3 blocs python valides
    mock_query.return_value = (
        "```python\nimport matplotlib.pyplot as plt\ndf['Age'].plot(kind='hist')\nplt.show()\n```\n"
        "```python\nimport seaborn as sns\nsns.boxplot(x=df['Score'])\n```\n"
        "```python\nimport plotly.express as px\nfig = px.scatter(df, x='Age', y='Score')\nfig.show()\n```"
    )

    # Appelle la fonction à tester
    generer_visualisations(sample_df, {"Age": "int64", "Score": "float64"}, "Résumé", "Tracer des courbes")

    # Vérifie que les visualisations ont bien été ajoutées
    assert "last_codes" in st.session_state
    assert len(st.session_state["last_codes"]) == 3
    assert st.session_state["total_valid"] == 3
