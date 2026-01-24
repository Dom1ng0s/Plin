import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from database import SessionLocal
from crud import criar_transacao, ler_saldo, ler_extrato



def formatar_moeda(valor):
    """
    Formata um número float (ex: 1234.50) em '1.234,50'.
    """

    texto = f"{valor:_.2f}"
    
    texto = texto.replace('.', ',')
    
    return texto.replace('_', '.')


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
        valor_bruto = float(context.args[0])
        valor_final = -abs(valor_bruto)
    except (IndexError, ValueError):
        await update.message.reply_text("Ops! Use assim: /gastar 10.50")
        return

    db = SessionLocal()
    
    try:
        criar_transacao(db, user_id=update.effective_user.id, quantia=valor_final, tipo="despesa")
        await update.message.reply_text(f"💸 Despesa de R$ {formatar_moeda(abs(valor_final))} registrada com sucesso!")
    except Exception as e:
        await update.message.reply_text(f"Erro técnico: {e}")
    finally:
        db.close()



async def saldo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    try:
        valor_total = ler_saldo(db,update.effective_user.id)

        await update.message.reply_text(f"💰 Saldo Atual: R$ {formatar_moeda(valor_total)}")
    except Exception as e:
        await update.message.reply_text(f"Erro ao consultar: {e}")
    finally:
        db.close()

async def ganhar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        valor_bruto = float(context.args[0])
        valor_final = abs(valor_bruto)
    except (IndexError, ValueError):
        await update.message.reply_text("Ops! Use assim: /ganhar 1000.00")
        return

    db = SessionLocal()
    
    try:
        criar_transacao(db, user_id=update.effective_user.id, quantia=valor_final, tipo="receita")
        await update.message.reply_text(f"✨ Receita de R$ {formatar_moeda(valor_final)} registrada!")
    except Exception as e:
        await update.message.reply_text(f"Erro técnico: {e}")
    finally:
        db.close()


        
async def extrato(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    
    try:
        movimentacoes = ler_extrato(db, update.effective_user.id)
        
        if not movimentacoes:
            await update.message.reply_text("📭 Nenhuma movimentação encontrada.")
            return

        texto = "📄 *Últimas Movimentações:*\n\n"
        
        for mov in movimentacoes:
            data_formatada = mov.data.strftime("%d/%m %H:%M")
            
            icone = "🟢" if mov.quantia > 0 else "🔴"
            
            texto += f"{icone} `[#{mov.id}]` `{data_formatada}`: *R$ {formatar_moeda(mov.quantia)}*\n"
            
        await update.message.reply_text(texto, parse_mode='Markdown')
        
    except Exception as e:
        await update.message.reply_text(f"Erro ao gerar extrato: {e}")
        
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
        saldo_handler = CommandHandler('saldo', saldo)
        application.add_handler(saldo_handler)
        ganhar_handler = CommandHandler('ganhar', ganhar)
        application.add_handler(ganhar_handler)
        extrato_handler = CommandHandler('extrato', extrato)
        application.add_handler(extrato_handler)
        application.run_polling()

