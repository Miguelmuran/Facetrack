from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Aluno
import shutil
import os

router = APIRouter(prefix="/alunos", tags=["Alunos"])

FACES_DIR = "faces_cadastradas"
os.makedirs(FACES_DIR, exist_ok=True)

@router.post("/cadastrar")
async def cadastrar_aluno(
    nome: str = Form(...),
    matricula: str = Form(...),
    email: str = Form(...),
    foto: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    existente = db.query(Aluno).filter(Aluno.matricula == matricula).first()
    if existente:
        raise HTTPException(status_code=400, detail="Matricula ja cadastrada")

    foto_path = os.path.join(FACES_DIR, f"{matricula}.jpg")
    with open(foto_path, "wb") as f:
        shutil.copyfileobj(foto.file, f)

    aluno = Aluno(nome=nome, matricula=matricula, email=email, foto_path=foto_path)
    db.add(aluno)
    db.commit()
    db.refresh(aluno)

    return {"mensagem": "Aluno cadastrado com sucesso", "id": aluno.id}

@router.get("/listar")
def listar_alunos(db: Session = Depends(get_db)):
    alunos = db.query(Aluno).all()
    return [{"id": a.id, "nome": a.nome, "matricula": a.matricula} for a in alunos]
