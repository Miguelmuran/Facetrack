from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Aluno, Presenca
from app.services.face_recognition_service import reconhecer_face
from app.services.liveness_service import verificar_vivacidade
from datetime import datetime

router = APIRouter(prefix="/reconhecimento", tags=["Reconhecimento"])

@router.post("/registrar-presenca")
async def registrar_presenca(
    foto: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    imagem_bytes = await foto.read()

    e_real = verificar_vivacidade(imagem_bytes)
    if not e_real:
        raise HTTPException(status_code=403, detail="Fraude detectada")

    matricula = reconhecer_face(imagem_bytes)
    if not matricula:
        raise HTTPException(status_code=404, detail="Rosto nao reconhecido")

    aluno = db.query(Aluno).filter(Aluno.matricula == matricula).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno nao encontrado")

    hoje = datetime.now().date()
    presenca_existente = db.query(Presenca).filter(
        Presenca.aluno_id == aluno.id,
        Presenca.data_hora >= datetime(hoje.year, hoje.month, hoje.day)
    ).first()

    if presenca_existente:
        return {"mensagem": f"Presenca de {aluno.nome} ja registrada hoje"}

    presenca = Presenca(aluno_id=aluno.id)
    db.add(presenca)
    db.commit()

    return {
        "mensagem": "Presenca registrada com sucesso",
        "aluno": aluno.nome,
        "matricula": aluno.matricula,
        "data_hora": presenca.data_hora.strftime("%d/%m/%Y %H:%M")
    }
