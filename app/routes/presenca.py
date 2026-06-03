from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Presenca, Aluno
from datetime import datetime, date

router = APIRouter(prefix="/presenca", tags=["Presenca"])

@router.get("/relatorio/{data}")
def relatorio_por_data(data: str, db: Session = Depends(get_db)):
    try:
        data_obj = date.fromisoformat(data)
    except ValueError:
        return {"erro": "Formato de data invalido. Use YYYY-MM-DD"}

    presencas = db.query(Presenca).filter(
        Presenca.data_hora >= datetime(data_obj.year, data_obj.month, data_obj.day),
        Presenca.data_hora < datetime(data_obj.year, data_obj.month, data_obj.day + 1)
    ).all()

    resultado = []
    for p in presencas:
        aluno = db.query(Aluno).filter(Aluno.id == p.aluno_id).first()
        resultado.append({
            "nome": aluno.nome,
            "matricula": aluno.matricula,
            "horario": p.data_hora.strftime("%H:%M:%S")
        })

    return {"data": data, "total_presentes": len(resultado), "alunos": resultado}
