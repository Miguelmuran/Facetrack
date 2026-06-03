from fastapi import FastAPI
from app.database import engine, Base
from app.routes import alunos, reconhecimento, presenca

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FaceTrack API",
    description="Sistema de registro de frequência por reconhecimento facial",
    version="1.0.0"
)

app.include_router(alunos.router)
app.include_router(reconhecimento.router)
app.include_router(presenca.router)

@app.get("/")
def raiz():
    return {"status": "FaceTrack rodando", "docs": "/docs"}