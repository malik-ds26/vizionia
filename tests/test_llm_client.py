from unittest.mock import patch
from llm_client import (
    query_llm,
    extract_python_code,
    extract_all_python_code_blocks,
    remove_think_blocks,
    get_suggestion_prompts,
    ask_for_visualization_script
)

def test_extract_python_code():
    text = "Some text\n```python\nprint(42)\n``` more text"
    assert extract_python_code(text) == "print(42)"

def test_extract_all_python_code_blocks():
    text = "```python\nprint(1)\n```\n```python\nprint(2)\n```"
    blocks = extract_all_python_code_blocks(text)
    assert blocks == ["\nprint(1)\n", "\nprint(2)\n"]

def test_remove_think_blocks():
    text = "Here is some text. <think>Do not show this</think> Continue here."
    cleaned = remove_think_blocks(text)
    assert "<think>" not in cleaned
    assert "Continue here." in cleaned

@patch("llm_client.requests.post")
def test_query_llm(mock_post):
    mock_post.return_value.json.return_value = {
        "choices": [{"message": {"content": "✅"} }]
    }
    mock_post.return_value.raise_for_status = lambda: None

    result = query_llm([{"role": "user", "content": "hello"}])
    assert result == "✅"

@patch("llm_client.query_llm")
def test_get_suggestion_prompts(mock_query):
    mock_query.return_value = "Suggestion 1\nSuggestion 2\nSuggestion 3\nSuggestion 4\nSuggestion 5"
    result = get_suggestion_prompts({"A": "int64", "B": "float64"})
    assert result.count("Suggestion") == 5

@patch("llm_client.query_llm")
def test_ask_for_visualization_script(mock_query):
    mock_query.return_value = "```python\nprint('viz')\n```"
    result = ask_for_visualization_script("A: int64", "Résumé", "Tracer un histogramme")
    assert "print" in result
