
from pydantic import BaseModel, constr


class AtletaBase(BaseModel):
    nome: str
    cpf: constr(min_length=11, max_length=11)
    centro_treinamento: str
    categoria: str


class AtletaCreate(AtletaBase):
    pass


class AtletaResponse(BaseModel):
    id: int
    nome: str
    cpf: str
    centro_treinamento: str
    categoria: str

    class Config:
        orm_mode = True


class AtletaListaResponse(BaseModel):
    nome: str
    centro_treinamento: str
    categoria: str

    class Config:
        orm_mode = True
