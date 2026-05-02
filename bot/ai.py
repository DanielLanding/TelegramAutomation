import logging
from openai import OpenAI, APIConnectionError, APIStatusError, RateLimitError
from config import GROQ_API_KEY, MODEL_NAME, SYSTEM_PROMPT, MAX_TOKENS

logger = logging.getLogger(__name__)

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)


def ask_openai(user_message: str, conversation_history: list = None) -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if conversation_history:
        messages.extend(conversation_history[-6:])

    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=MAX_TOKENS,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    except RateLimitError:
        logger.warning("Rate limit atingido no Groq")
        return "⚠️ Muitas requisições em pouco tempo. Aguarde alguns segundos e tente novamente."

    except APIConnectionError:
        logger.error("Falha de conexão com o Groq")
        return "⚠️ Serviço de IA temporariamente indisponível. Tente novamente em instantes."

    except APIStatusError as e:
        logger.error("Erro da API Groq %s: %s", e.status_code, e.message)
        if e.status_code == 401:
            return "⚠️ Chave de API inválida. Contate o administrador do bot."
        return "⚠️ Erro ao processar sua pergunta. Por favor, tente novamente."


def check_ai_health() -> dict:
    try:
        client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=1,
        )
        return {"online": True, "model": MODEL_NAME, "provider": "Groq"}
    except Exception as e:
        logger.warning("Groq health check falhou: %s", e)
        return {"online": False, "model": MODEL_NAME, "provider": "Groq"}
