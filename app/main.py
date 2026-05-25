from fastapi import FastAPI
from app.modulos.ingestao.rotas import router as ingestao_router
from app.modulos.historico.rotas import router as historico_router
from fastapi.middleware.cors import CORSMiddleware

"Para rodar o código: python -m uvicorn app.main:app --reload"

app = FastAPI(title="DataGrim API")

app.include_router(ingestao_router)
app.include_router(historico_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def raiz():
    return {"status": "API DataGrim online"}
