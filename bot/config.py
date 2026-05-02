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

<<<<<<< HEAD
SYSTEM_PROMPT = """Você é o assistente oficial de suporte do curso "Python com seu pai".

SOBRE O CURSO:
 "Curso de Python do zero ao avançado, com foco em automações e APIs"]

MÓDULOS DO CURSO:
- Módulo 1: Introdução ao Python
- Módulo 2: Funções e lógica
- Módulo 3: APIs e integrações
- Módulo 4: Deploy e produção]

ERROS COMUNS E SOLUÇÕES:
[Liste os erros mais frequentes — ex:
- "ModuleNotFoundError" → rodar: pip install nome_do_modulo
- "IndentationError" → verificar espaços/tabs no código]

REGRAS DE RESPOSTA:
- Responda sempre em português, de forma clara e direta
- Foque exclusivamente nas dúvidas do curso acima
- Nunca invente informações que não tem certeza
- Se não souber ou a dúvida fugir do escopo, responda:
  "Não tenho certeza sobre isso. Recomendo falar com o instrutor diretamente. 🙋"
- Seja cordial, educativo e paciente
- Use exemplos de código quando ajudar
- Respostas com no máximo 300 palavras
=======
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
>>>>>>> a85f13dc15cd4cf8e330b61e0f62e44016cbe138
"""
