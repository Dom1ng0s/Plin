from sqlalchemy.orm import Session
from database import Transacao

def criar_transacao(db: Session, user_id: int, quantia: float, tipo: str,parcela: str = None):
    """Grava uma nova Movimentação financeira no .db"""

    nova_transacao = Transacao(user_id=user_id, quantia=quantia,tipo=tipo,parcela=parcela)

    db.add(nova_transacao)
    db.commit()
    db.refresh(nova_transacao)
    return nova_transacao