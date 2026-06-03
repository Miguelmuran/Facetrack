from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    matricula = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True)
    foto_path = Column(String, nullable=False)
    presencas = relationship("Presenca", back_populates="aluno")

class Presenca(Base):
    __tablename__ = "presencas"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    data_hora = Column(DateTime, default=datetime.now)
    confirmado = Column(Boolean, default=True)
    aluno = relationship("Aluno", back_populates="presencas")
