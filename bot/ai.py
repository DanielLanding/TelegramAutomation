import logging
from openai import OpenAI, APIConnectionError, APIStatusError, RateLimitError
from config import OPENAI_API_KEY, MODEL_NAME, SYSTEM_PROMPT, MAX_TOKENS

logger = logging.getLogger(__name__)

client = OpenAI(api_key=OPENAI_API_KEY)


def ask_openai(user_message: str, conversation_history: list = None) -> str:
    """
    Envia mensagem para a OpenAI e retorna a resposta.
    Mantém histórico de conversa para contexto contínuo.
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if conversation_history:
        messages.extend(conversation_history[-6:])  # últimas 3 trocas

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
        logger.warning("Rate limit atingido na OpenAI")
        return "⚠️ Muitas requisições em pouco tempo. Aguarde alguns segundos e tente novamente."

    except APIConnectionError:
        logger.error("Falha de conexão com a OpenAI")
        return "⚠️ Serviço de IA temporariamente indisponível. Tente novamente em instantes."

    except APIStatusError as e:
        logger.error("Erro da API OpenAI %s: %s", e.status_code, e.message)
        if e.status_code == 401:
            return "⚠️ Chave de API inválida. Contate o administrador do bot."
        return "⚠️ Erro ao processar sua pergunta. Por favor, tente novamente."


def check_ai_health() -> dict:
    """Verifica se a chave da OpenAI está funcional."""
    try:
        # Chamada mínima para validar a chave (gasta < 10 tokens)
        client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=1,
        )
        return {"online": True, "model": MODEL_NAME, "provider": "OpenAI"}
    except Exception as e:
        logger.warning("OpenAI health check falhou: %s", e)
        return {"online": False, "model": MODEL_NAME, "provider": "OpenAI"}
