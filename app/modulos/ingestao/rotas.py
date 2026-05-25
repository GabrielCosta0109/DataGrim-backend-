from fastapi import APIRouter, UploadFile
from app.modulos.ingestao.servico import analisar_arquivo

router = APIRouter(prefix="/analise", tags=["Análise"])


@router.post("/")
def analisar(file: UploadFile):
    return analisar_arquivo(file)
