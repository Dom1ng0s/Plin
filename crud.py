from sqlalchemy.orm import Session
from database import Transacao
from sqlalchemy import func

def criar_transacao(db: Session, user_id: int, quantia: float, tipo: str, parcela: str = None):
    # 1. Descobrir qual o último ID deste utilizador específico
    ultimo_id = db.query(func.max(Transacao.id_transacao_user))\
                  .filter(Transacao.user_id == user_id).scalar()
    
    proximo_id = (ultimo_id or 0) + 1

    # 2. Criar a transação com o ID manual
    nova_transacao = Transacao(
        user_id=user_id, 
        id_transacao_user=proximo_id, 
        quantia=quantia,
        tipo=tipo,
        parcela=parcela
    )

    db.add(nova_transacao)
    db.commit()
    db.refresh(nova_transacao)
    return nova_transacao


def ler_saldo(db: Session, user_id: int):
    """SELECT COALESCE(SUM(quantia), 0) 
        FROM transacoes 
        WHERE user_id  = id;"""
    resultado = db.query(func.sum(Transacao.quantia))\
        .filter(Transacao.user_id == user_id)\
        .scalar()   
    return resultado if resultado else 0.0 


def ler_extrato(db: Session, user_id: int,):
    """
    SELECT id, user_id, quantia, tipo, parcela, data
    FROM transacoes
    WHERE user_id = 12345
    ORDER BY data DESC
    LIMIT limite;
    """
    limite = 10
    transacoes = db.query(Transacao)\
        .filter(Transacao.user_id == user_id)\
        .order_by(Transacao.data.desc())\
        .limit(limite)\
        .all()
    
    return transacoes


def deletar_transacao(db: Session, user_id: int, id_personalizado: int):
    """
    Remove uma transação baseada no ID local do utilizador, 
    não no ID global do banco de dados.
    """
    transacao = db.query(Transacao).filter(
        Transacao.id_transacao_user == id_personalizado,
        Transacao.user_id == user_id
    ).first()

    if transacao:
        db.delete(transacao)
        db.commit()
        return True
    return False
