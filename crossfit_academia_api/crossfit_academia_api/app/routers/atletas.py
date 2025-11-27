
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from fastapi_pagination import LimitOffsetPage, Params
from fastapi_pagination.ext.sqlalchemy import paginate

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/atletas", tags=["Atletas"])


@router.post("/", response_model=schemas.AtletaResponse, status_code=status.HTTP_201_CREATED)
async def criar_atleta(atleta_in: schemas.AtletaCreate, db: Session = Depends(get_db)):
    atleta = models.Atleta(
        nome=atleta_in.nome,
        cpf=atleta_in.cpf,
        centro_treinamento=atleta_in.centro_treinamento,
        categoria=atleta_in.categoria,
    )
    db.add(atleta)
    try:
        db.commit()
        db.refresh(atleta)
    except IntegrityError:
        db.rollback()
        # Mensagem e status_code conforme instruções
        raise HTTPException(
            status_code=303,
            detail=f"Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}",
        )
    return atleta


@router.get("/", response_model=LimitOffsetPage[schemas.AtletaListaResponse])
async def listar_atletas(
    nome: Optional[str] = None,
    cpf: Optional[str] = None,
    params: Params = Depends(),
    db: Session = Depends(get_db),
):
    """
    Lista atletas com filtros por nome e cpf, utilizando paginação
    via fastapi-pagination (limit e offset).
    A resposta é customizada, retornando apenas:
    - nome
    - centro_treinamento
    - categoria
    """
    query = db.query(models.Atleta)

    if nome:
        query = query.filter(models.Atleta.nome.ilike(f"%{nome}%"))
    if cpf:
        query = query.filter(models.Atleta.cpf == cpf)

    # A paginação aplica limit/offset automaticamente usando Params
    page = paginate(query, params)

    return page
