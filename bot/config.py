import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN  = os.getenv("TELEGRAM_TOKEN", "")
OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY", "")
MODEL_NAME      = os.getenv("MODEL_NAME", "gpt-4o-mini")   # mais barato e capaz
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

SYSTEM_PROMPT = """Você é um assistente de suporte técnico de um curso online.

Regras:
- Responda em português, de forma clara e direta
- Foque exclusivamente em dúvidas relacionadas ao curso
- Nunca invente informações que não tem certeza
- Se a dúvida fugir do escopo ou for muito específica, responda:
  "Não tenho certeza sobre isso. Recomendo entrar em contato com um instrutor. 🙋"
- Seja cordial, educativo e paciente
- Use exemplos práticos quando possível
- Respostas devem ter no máximo 300 palavras
"""
