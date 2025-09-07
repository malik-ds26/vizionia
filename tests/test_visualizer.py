import pytest
import pandas as pd
from visualizer import exec_code
import streamlit as st

# Test de sécurité basique : exécute un code matplotlib simple sans plantage
def test_exec_code_runs_safely():
    df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
    simple_plot = "import matplotlib.pyplot as plt\nplt.plot(df['x'], df['y'])\nplt.title('Test')"
    try:
        exec_code(simple_plot, df)
    except Exception as e:
        pytest.fail(f"exec_code a levé une exception : {e}")
