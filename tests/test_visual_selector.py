import pytest
import pandas as pd
import streamlit as st
from unittest.mock import patch
from visual_selector import regenerer_si_manquant

@pytest.fixture
def sample_df():
    return pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

@patch("visual_selector.query_llm")
def test_regenerer_si_manquant_adds_code(mock_llm, sample_df):
    st.session_state.clear()
    st.session_state["total_expected"] = 3
    st.session_state["total_valid"] = 2
    st.session_state["last_codes"] = ["print('A')", "print('B')"]

    # Simule une nouvelle visualisation différente
    mock_llm.return_value = "```python\nprint('C')\n```"

    # Simule le clic utilisateur sur le bouton
    with patch("streamlit.button", return_value=True):
        regenerer_si_manquant(sample_df)

    assert st.session_state["total_valid"] == 3
    assert any("print('C')" == code.strip() for code in st.session_state["last_codes"])

