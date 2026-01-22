from database import SessionLocal, engine, base
from crud import criar_transacao

# 1. Cria uma nova sessão com o banco
db = SessionLocal()

# 2. Tenta criar uma transação de teste
print("Tentando salvar transação...")
gasto = criar_transacao(db, user_id=12345, quantia=50.0, tipo="despesa", parcela="1/2")

# 3. Mostra o que foi salvo (inclusive o ID e a Data gerados automaticamente)
print(f"Sucesso! ID: {gasto.id} | Data: {gasto.data} | Valor: {gasto.quantia} | Parcela: {gasto.parcela}")

# 4. Fecha a conexão
db.close()