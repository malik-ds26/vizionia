import re


from llm_client import query_llm, remove_think_blocks

def get_interpretation(df_summary, user_request):
    messages = [
        {"role": "system", "content": "Tu es un expert en analyse de données. Tu reçois un résumé statistique d'un DataFrame et une demande utilisateur. Tu résumes les informations importantes et tu proposes une interprétation courte et compréhensible en français, sans code."},
        {"role": "user", "content": f"Voici le résumé du DataFrame :\n{df_summary}\n\nDemande de l'utilisateur : {user_request}\n\nFais une interprétation claire en français."}
    ]
    raw_response = query_llm(messages)
    return remove_think_blocks(raw_response)
def get_interpretation_from_code(code_str):
    prompt = (
        "Voici un code Python utilisé pour générer une visualisation à partir d'un DataFrame nommé `df` :\n\n"
        "```python\n"
        f"{code_str}\n"
        "```\n\n"
        "Interprète cette visualisation. Résume ce qu’elle montre en français, de façon claire et concise. "
        "Dis ce qu'on peut en conclure sur les données."
    )

    messages = [
        {
            "role": "system",
            "content": "Tu es un expert en analyse de données. Tu reçois du code Python générant un graphique et tu expliques ce que montre ce graphique, sans jamais renvoyer de code."
        },
        {"role": "user", "content": prompt}
    ]

    raw_response = query_llm(messages)
    return remove_think_blocks(raw_response)