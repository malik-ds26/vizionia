import pytest
from unittest.mock import patch
import pandas as pd
import streamlit as st
from graph_editor import modifier_derniere_visualisation

@pytest.fixture
def setup_session():
    st.session_state.clear()
    st.session_state["chat_history"] = [
        {"role": "user", "content": "Fais un graphique"},
        {"role": "assistant", "content": "```python\nplt.plot(df['x'], df['y'])\n```"}
    ]
    st.session_state["modif_input"] = "Ajoute un titre"

@patch("graph_editor.query_llm")
@patch("streamlit.text_input")
@patch("streamlit.button")
def test_modifier_derniere_visualisation(mock_button, mock_input, mock_llm, setup_session):
    mock_input.return_value = "Ajoute un titre"
    mock_button.side_effect = [True]  # Simule le clic sur "Appliquer la modification"
    mock_llm.return_value = "```python\nplt.plot(df['x'], df['y'])\nplt.title('Titre ajouté')\n```"

    df = pd.DataFrame({"x": [1, 2], "y": [3, 4]})
    modifier_derniere_visualisation(df)

    assert st.session_state["chat_history"][-2]["content"] == "Ajoute un titre"
    assert "Titre ajouté" in st.session_state["chat_history"][-1]["content"]
