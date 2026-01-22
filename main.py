import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from database import SessionLocal
from crud import criar_transacao

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Olá! Eu sou o Plin 💸. 'Registrou, Plin. Controlou.'"
    )
async def gastar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        valor = float(context.args[0])
    except(IndexError, ValueError):
        await update.message.reply_text("Ops! Use assim: /gastar 10.50")
        return
    db = SessionLocal()
    try:
        criar_transacao(db, user_id=update.effective_user.id, quantia=valor, tipo="despesa")
        await update.message.reply_text(f"💸 Despesa de R$ {valor:.2f} registrada com sucesso!")
        
    except Exception as e:
        await update.message.reply_text(f"Erro técnico: {e}")
        
    finally:
        db.close()


if __name__ == '__main__':
    token = os.getenv('TELEGRAM_TOKEN')
    
    if not token:
        print("ERRO: Token não encontrado! Verifique o seu arquivo .env")
    else:
        application = ApplicationBuilder().token(token).build()
        
        start_handler = CommandHandler('start', start)
        application.add_handler(start_handler)
        gastar_handler = CommandHandler('gastar', gastar)
        application.add_handler(gastar_handler)
        
        application.run_polling()
