import pytest
import pandas as pd
import streamlit as st
from unittest.mock import patch, MagicMock
from history_ui import afficher_historique

@patch("history_ui.extract_python_code")
@patch("history_ui.get_interpretation_from_code")
@patch("streamlit.button")
@patch("streamlit.columns")
def test_afficher_historique_interpretation(mock_columns, mock_button, mock_interpret, mock_extract):
    st.session_state.clear()
    st.session_state["chat_history"] = [
        {"role": "user", "content": "Créer un nuage de points"},
        {"role": "assistant", "content": "```python\nplt.scatter(df['x'], df['y'])\n```"}
    ]

    # ✅ simulate context manager objects
    mock_context = MagicMock()
    mock_context.__enter__.return_value = mock_context
    mock_context.__exit__.return_value = None
    mock_columns.return_value = [mock_context] * 4

    mock_button.side_effect = [False, False, False, True]  # 🧠 seulement cliqué
    mock_extract.return_value = "plt.scatter(df['x'], df['y'])"
    mock_interpret.return_value = "Ceci est un nuage de points."

    df = pd.DataFrame({"x": [1, 2], "y": [3, 4]})
    afficher_historique(df)

    mock_interpret.assert_called_once_with("plt.scatter(df['x'], df['y'])")
