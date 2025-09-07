import pandas as pd
from data_analyzer import get_column_info, get_summary

def test_get_column_info():
    df = pd.DataFrame({
        "A": [1, 2, 3],
        "B": ["x", "y", "z"]
    })
    info = get_column_info(df)
    assert info == {"A": "int64", "B": "object"}

def test_get_summary_html():
    df = pd.DataFrame({"A": [1, 2, 3]})
    summary = get_summary(df)
    assert "<table" in summary
    assert "A" in summary
