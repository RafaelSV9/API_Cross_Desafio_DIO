
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from .database import Base, engine
from .routers import atletas

# Cria as tabelas no banco (apenas para exemplo didático)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Academia de Crossfit",
    description="API assíncrona para gestão de atletas de uma academia focada em competições de crossfit.",
    version="0.1.0",
)

app.include_router(atletas.router)

# Adiciona suporte à paginação globalmente
add_pagination(app)
