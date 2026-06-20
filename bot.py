from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from orchestrator import run_agent
from tools.classroom import last_assignment
import requests
from config import GROQ_API_KEY

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Agent online. Send me anything.")

async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    reply = run_agent(user_msg)
    await update.message.reply_text(reply)

async def yes_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    assignment = last_assignment.get(chat_id)

    if not assignment:
        await update.message.reply_text("No assignment on record. Wait for a new notification.")
        return

    await update.message.reply_text("✍️ Drafting a response for your assignment...")

    prompt = f"""You are a student completing a school assignment.

Assignment details:
- Course: {assignment['course']}
- Title: {assignment['title']}
- Type: {assignment['type']}
- Due: {assignment['due']}
- Description: {assignment['description']}

Read the description carefully. Complete exactly what is being asked.
If it is a question, answer it. If it is an essay, write it. If it is a form, list the answers clearly.
Write at a secondary school level. Be thorough and structured."""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GROQ_API_KEY}"
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    if response.status_code == 200:
        draft = response.json()["choices"][0]["message"]["content"]
        await update.message.reply_text(f"📝 *Assignment Draft:*\n\n{draft}", parse_mode='Markdown')
    else:
        await update.message.reply_text(f"LLM error: {response.status_code}")

async def skip_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏭ Skipped. I'll notify you of the next one.")

def build_bot():
    from config import TELEGRAM_TOKEN
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("yes", yes_handler))
    app.add_handler(CommandHandler("skip", skip_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return app