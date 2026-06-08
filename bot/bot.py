import logging
import time
import threading
from datetime import datetime, timezone
from collections import defaultdict, deque

from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)
from flask import Flask, jsonify

from config import (
    TELEGRAM_TOKEN,
    ANTHROPIC_API_KEY,
    ALLOWED_GROUP_IDS,
    COOLDOWN_SECONDS,
    KEYWORDS,
    STATUS_PORT,
    BOT_NAME,
    MODEL_NAME,
)
from ai import ask_claude, check_ai_health

# ──────────────────────────────────────────────
# Logging
# ──────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# Estado global (em memória)
# ──────────────────────────────────────────────
start_time = datetime.now(timezone.utc)
stats = {"messages_received": 0, "responses_sent": 0, "errors": 0}
recent_logs: deque = deque(maxlen=50)  # últimas 50 interações
cooldowns: dict = defaultdict(float)    # user_id → timestamp da última resposta
conversation_history: dict = defaultdict(list)  # user_id → histórico

# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def is_allowed_group(chat_id: int) -> bool:
    """Retorna True se o grupo está na lista de permitidos (ou lista vazia = todos)."""
    if not ALLOWED_GROUP_IDS:
        return True
    return chat_id in ALLOWED_GROUP_IDS


def should_respond(text: str, bot_username: str) -> bool:
    """Decide se o bot deve responder a uma mensagem."""
    text_lower = text.lower()
    mentioned = f"@{bot_username.lower()}" in text_lower
    has_keyword = any(kw in text_lower for kw in KEYWORDS)
    return mentioned or has_keyword


def is_on_cooldown(user_id: int) -> bool:
    elapsed = time.time() - cooldowns[user_id]
    return elapsed < COOLDOWN_SECONDS


def log_interaction(user: str, question: str, answer: str):
    recent_logs.appendleft(
        {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user": user,
            "question": question[:200],
            "answer": answer[:400],
        }
    )

# ──────────────────────────────────────────────
# Handlers do Telegram
# ──────────────────────────────────────────────

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    message = update.message
    text = message.text
    user = message.from_user
    user_id = user.id
    user_display = user.username or user.first_name or str(user_id)
    bot_username = context.bot.username

    stats["messages_received"] += 1
    logger.info("Mensagem de %s | chat=%s (%s) | texto: %s", user_display, message.chat_id, message.chat.type, text[:80])

    is_private = message.chat.type == "private"

    if not is_private and not is_allowed_group(message.chat_id):
        logger.info("Chat %s não está em ALLOWED_GROUP_IDS — ignorando", message.chat_id)
        return

    if not is_private and not should_respond(text, bot_username):
        logger.info("Sem keyword/menção na msg de %s — ignorando", user_display)
        return

    if is_on_cooldown(user_id):
        remaining = int(COOLDOWN_SECONDS - (time.time() - cooldowns[user_id]))
        await message.reply_text(
            f"⏳ Aguarde {remaining}s antes de enviar outra pergunta.",
            reply_to_message_id=message.message_id,
        )
        return

    logger.info("Respondendo para %s: %s", user_display, text[:80])
    await context.bot.send_chat_action(
        chat_id=message.chat_id, action="typing"
    )

    try:
        history = conversation_history[user_id]
        response = ask_claude(text, history)

        # Atualiza histórico
        history.append({"role": "user", "content": text})
        history.append({"role": "assistant", "content": response})
        if len(history) > 12:
            history = history[-12:]
        conversation_history[user_id] = history

        try:
            await message.reply_text(
                response,
                reply_to_message_id=message.message_id,
                parse_mode="Markdown",
            )
        except Exception:
            await message.reply_text(response, reply_to_message_id=message.message_id)

        cooldowns[user_id] = time.time()
        stats["responses_sent"] += 1
        log_interaction(user_display, text, response)

    except Exception as e:
        logger.error("Erro ao processar mensagem: %s", e)
        stats["errors"] += 1
        await message.reply_text(
            "⚠️ Ocorreu um erro ao processar sua pergunta. Tente novamente.",
            reply_to_message_id=message.message_id,
        )


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"👋 Olá! Sou o {BOT_NAME}, seu assistente de suporte do curso.\n\n"
        "Me mencione ou envie uma dúvida com palavras como *como*, *erro*, *ajuda* "
        "e responderei automaticamente.\n\n"
        "Use /status para ver meu estado atual.",
        parse_mode="Markdown",
    )


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uptime = datetime.now(timezone.utc) - start_time
    h, rem = divmod(int(uptime.total_seconds()), 3600)
    m, s = divmod(rem, 60)

    status_text = (
        f"📊 *Status do {BOT_NAME}*\n\n"
        f"🟢 Bot: Online\n"
        f"🤖 Modelo: `{MODEL_NAME}` (Anthropic)\n"
        f"⏱ Uptime: {h}h {m}m {s}s\n"
        f"📨 Mensagens recebidas: {stats['messages_received']}\n"
        f"✅ Respostas enviadas: {stats['responses_sent']}\n"
        f"❌ Erros: {stats['errors']}\n"
    )
    await update.message.reply_text(status_text, parse_mode="Markdown")


async def cmd_getid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    await update.message.reply_text(
        f"🆔 *IDs desta conversa*\n\n"
        f"Chat ID: `{chat.id}`\n"
        f"Tipo: `{chat.type}`\n"
        f"Nome: `{chat.title or chat.first_name}`\n"
        f"Seu user ID: `{user.id}`\n\n"
        f"Cole o Chat ID no `.env`:\n`ALLOWED_GROUP_IDS={chat.id}`",
        parse_mode="Markdown",
    )


async def cmd_clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    conversation_history[user_id] = []
    await update.message.reply_text("🧹 Histórico de conversa limpo!")

# ──────────────────────────────────────────────
# Status HTTP Server (Flask)
# ──────────────────────────────────────────────
flask_app = Flask(__name__)


@flask_app.route("/api/status")
def api_status():
    uptime = (datetime.now(timezone.utc) - start_time).total_seconds()
    return jsonify(
        {
            "bot": BOT_NAME,
            "online": True,
            "uptime_seconds": int(uptime),
            "provider": "Anthropic",
            "model": MODEL_NAME,
            "stats": stats,
        }
    )


@flask_app.route("/api/logs")
def api_logs():
    return jsonify(list(recent_logs))


@flask_app.route("/health")
def health():
    return jsonify({"status": "ok"})


def run_flask():
    flask_app.run(host="0.0.0.0", port=STATUS_PORT, debug=False, use_reloader=False)

# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def main():
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN não configurado no .env")
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY não configurado no .env")

    # Inicia Flask em thread separada
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info("Status API rodando na porta %s", STATUS_PORT)

    # Inicia bot do Telegram
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_start))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(CommandHandler("getid", cmd_getid))
    app.add_handler(CommandHandler("clear", cmd_clear))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    logger.info("Bot iniciado — aguardando mensagens...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
