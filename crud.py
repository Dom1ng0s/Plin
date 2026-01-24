from sqlalchemy.orm import Session
from database import Transacao
from sqlalchemy import func

def criar_transacao(db: Session, user_id: int, quantia: float, tipo: str,parcela: str = None):
    """
        /* 2. O Comando Principal (db.add + parte do commit) */
        INSERT INTO transacoes (user_id, quantia, tipo, parcela, data) 
        VALUES (12345, 50.0, 'despesa', '1/2', '2026-01-24 19:30:00');
        

        SELECT id, data 
        FROM transacoes 
        WHERE rowid = last_insert_rowid();"""

    nova_transacao = Transacao(user_id=user_id, quantia=quantia,tipo=tipo,parcela=parcela)

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
