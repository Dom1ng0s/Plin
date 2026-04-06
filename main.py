import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from database import SessionLocal
from crud import criar_transacao, ler_saldo, ler_extrato, deletar_transacao
from nlp_parser import analisar_mensagem

def formatar_moeda(valor: float) -> str:
    """Formata um número float em padrão de moeda."""
    texto = f"{valor:_.2f}"
    texto = texto.replace('.', ',')
    return texto.replace('_', '.')

def limpar_valor(entrada: str) -> float:
    """Limpa e converte a entrada de texto numérico para float."""
    limpo = entrada.strip().replace('R$', '').replace(' ', '')
    
    if ',' in limpo and '.' in limpo:
        limpo = limpo.replace('.', '').replace(',', '.')
    elif ',' in limpo:
        limpo = limpo.replace(',', '.')
    elif '.' in limpo:
        partes = limpo.split('.')
        if len(partes[-1]) == 3:
            limpo = limpo.replace('.', '')
            
    return float(limpo)

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicia o bot e envia a mensagem de boas-vindas."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Olá! Eu sou o Plin 💸. 'Registrou, Plin. Controlou.'"
    )

async def gastar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Registra uma despesa explicitamente via comando."""
    try:
        valor_bruto = limpar_valor(context.args[0])
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

async def ganhar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Registra uma receita explicitamente via comando."""
    try:
        valor_bruto = limpar_valor(context.args[0])
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

async def saldo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Consulta o saldo total do utilizador."""
    db = SessionLocal()
    try:
        valor_total = ler_saldo(db, update.effective_user.id)
        await update.message.reply_text(f"💰 Saldo Atual: R$ {formatar_moeda(valor_total)}")
    except Exception as e:
        await update.message.reply_text(f"Erro ao consultar: {e}")
    finally:
        db.close()

async def extrato(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gera o extrato das últimas movimentações."""
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
            texto += f"{icone} `[#{mov.id_transacao_user}]` `{data_formatada}`: *R$ {formatar_moeda(mov.quantia)}*\n"
            
        await update.message.reply_text(texto, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"Erro ao gerar extrato: {e}")
    finally:
        db.close()

async def apagar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Apaga uma transação específica pelo ID."""
    try:
        id_para_apagar = int(context.args[0])
    except (IndexError, ValueError):
        await update.message.reply_text("⚠️ Use assim: /apagar [número_do_id]\nExemplo: /apagar 2")
        return

    db = SessionLocal()
    try:
        sucesso = deletar_transacao(db, update.effective_user.id, id_para_apagar)
        if sucesso:
            await update.message.reply_text(f"✅ Transação #{id_para_apagar} apagada com sucesso!")
        else:
            await update.message.reply_text("❌ Não encontrada. Verifique o número no /extrato.")
    except Exception as e:
        await update.message.reply_text(f"Erro ao apagar: {e}")
    finally:
        db.close()

async def processar_mensagem_livre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Interceta mensagens de texto normais e processa através do motor de NLP."""
    texto_utilizador = update.message.text
    
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    
    dados = analisar_mensagem(texto_utilizador)
    
    if not dados:
        await update.message.reply_text(
            "🤔 Hum, não percebi muito bem. Tente algo como:\n"
            "- 'gastei 45 no mercado'\n"
            "- 'recebi 200 de freela'"
        )
        return

    db = SessionLocal()
    try:
        criar_transacao(
            db, 
            user_id=update.effective_user.id, 
            quantia=dados["valor"], 
            tipo=dados["tipo_transacao"], 
            parcela=dados["categoria"] 
        )
        
        icone = "✅" if dados["tipo_transacao"] == "receita" else "💸"
        await update.message.reply_text(
            f"{icone} Registo efetuado com sucesso!\n"
            f"🏷️ Categoria: {dados['categoria']}\n"
            f"💰 Valor: R$ {formatar_moeda(abs(dados['valor']))}"
        )
    except Exception as e:
        logging.error(f"Erro ao guardar no BD: {e}")
        await update.message.reply_text("❌ Ocorreu um erro técnico ao guardar a transação.")
    finally:
        db.close()

async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Exibe o menu de ajuda com os comandos disponíveis."""
    texto = (
        "🆘 *Central de Ajuda do Plin*\n\n"
        "Aqui estão os comandos que eu conheço:\n\n"
        "💬 *Mensagem Livre*\n"
        "Escreva naturalmente: 'gastei 50 no ifood' ou 'recebi 200 de freela'\n\n"
        "🟢 */ganhar [valor]*\n"
        "Registra uma entrada de dinheiro.\n"
        "Ex: `/ganhar 1500`\n\n"
        "🔴 */gastar [valor]*\n"
        "Registra uma saída de dinheiro.\n"
        "Ex: `/gastar 45.50`\n\n"
        "💰 */saldo*\n"
        "Mostra quanto você tem em caixa hoje.\n\n"
        "📄 */extrato*\n"
        "Lista as últimas 10 movimentações com seus IDs.\n\n"
        "🗑️ */apagar [ID]*\n"
        "Remove uma transação errada usando o número do ID.\n"
        "Ex: `/apagar 5`"
    )
    await update.message.reply_text(texto, parse_mode='Markdown')

if __name__ == '__main__':
    token = os.getenv('TELEGRAM_TOKEN')
    
    if not token:
        print("ERRO: Token não encontrado! Verifique o seu arquivo .env")
    else:
        application = ApplicationBuilder().token(token).build()
        
        handlers = [
            ('start', start),
            ('ajuda', ajuda),
            ('saldo', saldo),
            ('extrato', extrato),
            ('ganhar', ganhar),
            ('gastar', gastar),
            ('apagar', apagar)
        ]

        for comando, funcao in handlers:
            application.add_handler(CommandHandler(comando, funcao))

        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, processar_mensagem_livre))
        
        application.run_polling()