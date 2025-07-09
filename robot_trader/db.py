from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timedelta
import os

DATABASE_URL = os.getenv("DB_URL", "postgresql://postgres:postgres@localhost:5432/robotrader")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Candle(Base):
    __tablename__ = "candles"
    id = Column(Integer, primary_key=True, index=True)
    ativo = Column(String)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

def criar_tabelas():
    Base.metadata.create_all(bind=engine)

def salvar_candle(dados: dict):
    session = SessionLocal()
    candle = Candle(
        ativo=dados.get("ativo"),
        open=dados.get("open"),
        high=dados.get("high"),
        low=dados.get("low"),
        close=dados.get("close"),
        volume=dados.get("volume"),
        timestamp=dados.get("timestamp", datetime.utcnow())
    )
    session.add(candle)
    session.commit()
    session.close()

def obter_candles_periodo(dias: int = 30):
    session = SessionLocal()
    limite = datetime.utcnow() - timedelta(days=dias)
    candles = session.query(Candle).filter(Candle.timestamp >= limite).all()
    session.close()
    return candles