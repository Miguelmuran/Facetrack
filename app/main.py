from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import alunos, reconhecimento, presenca

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FaceTrack API",
    description="Sistema de registro de frequência por reconhecimento facial",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(alunos.router)
app.include_router(reconhecimento.router)
app.include_router(presenca.router)

@app.get("/")
def raiz():
    return {"status": "FaceTrack rodando", "docs": "/docs"}