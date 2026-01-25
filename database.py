from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, BigInteger
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///plin.db"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)

base = declarative_base()

class Transacao(base):
    __tablename__ = "transacoes"

    user_id = Column(BigInteger, primary_key=True) 
    id_transacao_user = Column(Integer, primary_key=True) 
    quantia = Column(Float, nullable=False)
    tipo = Column(String, nullable=False)
    parcela = Column(String, nullable=True)
    data = Column(DateTime, default=datetime.now)

base.metadata.create_all(engine)
