from pydantic import BaseModel
from typing import Any, Dict, Optional, List


class AnaliseResumoOut(BaseModel):
  id: int
  nomeArquivo: str
  timestamp: str
  percentual: float
  severidade: str


class AnaliseDetalheOut(BaseModel):
  id: int
  nomeArquivo: str
  timestamp: str
  caminhoArquivo: str
  sha256: str
  contentType: Optional[str] = None
  tamanhoBytes: int

  percentual: float
  severidade: str
  recomendacao: str

  resultado: Dict[str, Any]  # JSON completo do backend


class AnaliseCriadaOut(BaseModel):
  id: int
  nomeArquivo: str
  timestamp: str
