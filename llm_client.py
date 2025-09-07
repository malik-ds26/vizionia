# llm_client.py
import requests
import re

API_URL = "http://127.0.0.1:1234/v1/chat/completions"  # Exemple pour LM Studio

HEADERS = {
    "Content-Type": "application/json"
}

SYSTEM_PROMPT = "Tu es un expert en visualisation de donnees. A partir de la structure d'un DataFrame pandas et de la demande de l'utilisateur, tu proposes le type de graphique le plus adapte et tu ecris du code Python pour le generer. Utilise matplotlib, seaborn ou plotly. Fournis uniquement le code Python dans une balise Markdown ```python."

def query_llm(messages, temperature=1):
    payload = {
        "model": "qwen3-4b",
        "messages": messages,
        "temperature": temperature
    }
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"[ERREUR] La requête LLM a échoué : {e}"

def extract_python_code(response_text):
    match = re.search(r"```python(.*?)```", response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return response_text.strip()  # Fallback if no markdown block found

def remove_think_blocks(text):
    """Supprime les blocs <think>...</think> d'une réponse texte."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

def ask_for_visualization_script(column_info, summary, user_request):
    user_prompt = f"Voici les informations sur le DataFrame :\nColonnes : {column_info}\nRésumé : {summary}\n\nL'utilisateur souhaite : {user_request}\n\nPropose un graphique adapté et écris uniquement le code Python dans une balise markdown."
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]
    raw_response = query_llm(messages)
    return extract_python_code(raw_response)

def get_suggestion_prompts(column_info):
    prompt = f"Voici les colonnes de données : {column_info}. Propose exactement 5 suggestions de visualisation, en français, sous forme de phrases simples, sans aucune réflexion, commentaire ou balise. Donne uniquement ces 5 phrases séparées par des retours à la ligne."
    messages = [
        {
            "role": "system",
            "content": "Tu es un expert en visualisation de données. Tu dois proposer exactement 5 suggestions claires, sans explication ni commentaire, juste les phrases utilisateur."
        },
        {"role": "user", "content": prompt}
    ]
    raw = query_llm(messages)
    return remove_think_blocks(raw)

def extract_all_python_code_blocks(text):
    return re.findall(r"```python(.*?)```", text, re.DOTALL)
