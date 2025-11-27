
from sqlalchemy import Column, Integer, String
from .database import Base


class Atleta(Base):
    __tablename__ = "atletas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(11), nullable=False, unique=True, index=True)
    centro_treinamento = Column(String(100), nullable=False)
    categoria = Column(String(50), nullable=False)
