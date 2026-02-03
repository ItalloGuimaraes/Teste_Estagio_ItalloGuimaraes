from fastapi import APIRouter, HTTPException, Query
from service import data_service

router = APIRouter()

@router.get("/operadoras")
def listar_operadoras(
    page: int = Query(1, ge=1), 
    limit: int = Query(10, ge=1, le=100),
    search: str = None
):
    resultado = data_service.get_operadoras(page, limit, search)
    
    total_registros = resultado['total']
    total_paginas = (total_registros // limit) + (1 if total_registros % limit > 0 else 0)

    return {
        "data": resultado['data'],
        "meta": {
            "page": page,
            "limit": limit,
            "total_records": total_registros,
            "total_pages": total_paginas
        }
    }

@router.get("/operadoras/{registro_ans}")
def detalhes_operadora(registro_ans: str):
    op = data_service.get_operadora_by_registro(registro_ans)
    if not op:
        raise HTTPException(status_code=404, detail="Operadora não encontrada")
    return op

@router.get("/operadoras/{registro_ans}/despesas")
def historico_despesas(registro_ans: str):
    despesas = data_service.get_despesas_by_registro(registro_ans)
    if despesas is None:
        raise HTTPException(status_code=404, detail="Operadora não encontrada")
    return despesas

@router.get("/estatisticas")
def dashboard():
    stats = data_service.get_dashboard_stats()
    if not stats:
        raise HTTPException(status_code=500, detail="Dados não carregados")
    return stats