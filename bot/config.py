import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN  = os.getenv("TELEGRAM_TOKEN", "")
GROQ_API_KEY    = os.getenv("GROQ_API_KEY", "")
MODEL_NAME      = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

# IDs dos grupos autorizados (separados por vírgula). Vazio = responde em todos.
_allowed = os.getenv("ALLOWED_GROUP_IDS", "")
ALLOWED_GROUP_IDS: list[int] = [int(x.strip()) for x in _allowed.split(",") if x.strip()]
COOLDOWN_SECONDS = int(os.getenv("COOLDOWN_SECONDS", "30"))
STATUS_PORT     = int(os.getenv("STATUS_PORT", "8080"))
BOT_NAME        = os.getenv("BOT_NAME", "SupportBot")
MAX_TOKENS      = int(os.getenv("MAX_TOKENS", "400"))

KEYWORDS = [
    k.strip()
    for k in os.getenv(
        "KEYWORDS",
        "como,erro,ajuda,problema,não funciona,dúvida,quando,por que,porque,qual,consigo,posso",
    ).split(",")
]

def _load_knowledge():
    """Carrega a base de conhecimento do arquivo knowledge.txt."""
    knowledge_path = os.path.join(os.path.dirname(__file__), "knowledge.txt")
    try:
        with open(knowledge_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

_KNOWLEDGE_BASE = _load_knowledge()

SYSTEM_PROMPT = f"""Você é um assistente do curso Corretores Vencedores do Altemir Rocha. Você responde dúvidas dos alunos no Telegram com base no conhecimento do curso.

Regras:
- Responda em português, de forma clara, direta e motivadora
- Use a base de conhecimento abaixo para fundamentar suas respostas
- Quando a resposta estiver na base de conhecimento, responda com confiança
- Quando a dúvida for muito específica ou não estiver na base, responda:
  "Não tenho certeza sobre isso. Recomendo assistir a aula relacionada no curso ou perguntar diretamente ao Altemir na próxima mentoria. 🙋"
- Nunca invente informações sobre o curso
- Sempre incentive o aluno a aplicar o curso na prática
- Seja cordial, educativo e paciente
- Respostas devem ter no máximo 300 palavras

BASE DE CONHECIMENTO DO CURSO:
{_KNOWLEDGE_BASE}
"""
