import json
from pathlib import Path
from datetime import datetime

CAMINHO = Path(__file__).parent / "historico_analises.json"


def carregar():
    if not CAMINHO.exists():
        return []

    with open(CAMINHO, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar(dados: dict):
    historico = carregar()

    dados["data_analise"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dados["id_analise"] = len(historico) + 1

    historico.append(dados)

    with open(CAMINHO, "w", encoding="utf-8") as f:
        json.dump(historico, f, indent=2, ensure_ascii=False)

    return dados
