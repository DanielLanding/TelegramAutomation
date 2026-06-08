import logging
import anthropic
from config import ANTHROPIC_API_KEY, MODEL_NAME, SYSTEM_PROMPT, MAX_TOKENS

logger = logging.getLogger(__name__)

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def ask_claude(user_message: str, conversation_history: list = None) -> str:
    messages = []
    if conversation_history:
        messages.extend(conversation_history[-6:])
    messages.append({"role": "user", "content": user_message})

    try:
        response = client.messages.create(
            model=MODEL_NAME,
            system=SYSTEM_PROMPT,
            messages=messages,
            max_tokens=MAX_TOKENS,
        )
        return response.content[0].text.strip()

    except anthropic.RateLimitError:
        logger.warning("Rate limit atingido na API Claude")
        return "⚠️ Muitas requisições em pouco tempo. Aguarde alguns segundos e tente novamente."

    except anthropic.APIConnectionError:
        logger.error("Falha de conexão com a API Claude")
        return "⚠️ Serviço de IA temporariamente indisponível. Tente novamente em instantes."

    except anthropic.APIStatusError as e:
        logger.error("Erro da API Claude %s: %s", e.status_code, e.message)
        if e.status_code == 401:
            return "Chave de API inválida. Contate o administrador do bot."
        return "Erro ao processar sua pergunta. Por favor, tente novamente."


def check_ai_health() -> dict:
    try:
        client.messages.create(
            model=MODEL_NAME,
            system="You are a health check.",
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=1,
        )
        return {"online": True, "model": MODEL_NAME, "provider": "Anthropic"}
    except Exception as e:
        logger.warning("Claude health check falhou: %s", e)
        return {"online": False, "model": MODEL_NAME, "provider": "Anthropic"}
