# API de Academia para Competição de Crossfit 🏋️‍♂️

Este projeto implementa uma **API REST assíncrona** para gerenciar uma academia focada em **competições de crossfit**, utilizando **Python** e **FastAPI**.  
O objetivo é praticar construção de APIs modernas, performáticas e escaláveis, usando recursos como:

- Endpoints assíncronos
- Query parameters
- Respostas customizadas
- Tratamento de exceções de integridade com SQLAlchemy
- Paginação com a biblioteca **fastapi-pagination**

---

## 🧱 Tecnologias Utilizadas

- **Python 3.10+**
- **FastAPI**
- **Uvicorn** (servidor ASGI)
- **SQLAlchemy** (ORM)
- **fastapi-pagination** (paginação)
- (Opcional) **Poetry** para gerenciamento de dependências

---

## 🚀 Funcionalidades Principais

### 1. Gestão de Atletas

A API permite cadastrar, listar, detalhar, atualizar e remover **atletas**, incluindo:

- `nome`
- `cpf`
- `centro_treinamento`
- `categoria`

### 2. Query Parameters nos Endpoints

Foi adicionado suporte a **query parameters** em endpoints de atleta, por exemplo:

- Filtro por **nome**
- Filtro por **cpf**

Exemplo de rota de listagem com filtros:

```http
GET /atletas?nome=Rafael&cpf=12345678900
Exemplo de assinatura em FastAPI:

python
Copiar código
from typing import Optional
from fastapi import APIRouter

router = APIRouter(prefix="/atletas", tags=["Atletas"])

@router.get("/")
async def listar_atletas(
    nome: Optional[str] = None,
    cpf: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
):
    # lógica de filtro por nome e cpf + paginação
    ...
3. Respostas Customizadas
O endpoint de listar todos os atletas retorna uma resposta customizada com os seguintes campos:

nome

centro_treinamento

categoria

Exemplo de resposta:

json
Copiar código
[
  {
    "nome": "Rafael Santos",
    "centro_treinamento": "CT Elite Cross",
    "categoria": "RX"
  },
  {
    "nome": "Ana Silva",
    "centro_treinamento": "CT Iron Box",
    "categoria": "Scaled"
  }
]
Modelo de resposta em FastAPI:

python
Copiar código
from pydantic import BaseModel

class AtletaListaResponse(BaseModel):
    nome: str
    centro_treinamento: str
    categoria: str
E no endpoint:

python
Copiar código
from typing import List

@router.get("/", response_model=List[AtletaListaResponse])
async def listar_atletas(...):
    ...
4. Tratamento de Exceções de Integridade (IntegrityError)
Para garantir mensagens claras quando ocorre violação de integridade (por exemplo, CPF duplicado), foi tratada a exceção:

sqlalchemy.exc.IntegrityError

Sempre que tentar cadastrar um atleta com um CPF já existente, a API devolve:

status_code: 303

mensagem: Já existe um atleta cadastrado com o cpf: x

Exemplo de implementação:

python
Copiar código
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

@router.post("/", status_code=status.HTTP_201_CREATED)
async def criar_atleta(atleta_in: AtletaCreateSchema):
    try:
        # lógica de inserção no banco
        ...
    except IntegrityError:
        # faz rollback da sessão antes de lançar o erro
        db.session.rollback()
        raise HTTPException(
            status_code=303,
            detail=f"Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}",
        )
💡 Obs.: em APIs reais costuma-se usar 409 Conflict, mas neste projeto foi especificamente solicitado o uso de 303.

5. Paginação com fastapi-pagination
Foi adicionada paginação baseada em limit e offset, utilizando a biblioteca fastapi-pagination.

Instalação:

bash
Copiar código
pip install fastapi-pagination
# ou com poetry:
# poetry add fastapi-pagination
Configuração básica:

python
Copiar código
from fastapi import FastAPI
from fastapi_pagination import add_pagination

app = FastAPI()

# incluir rotas aqui

add_pagination(app)
Exemplo de uso com SQLAlchemy:

python
Copiar código
from fastapi_pagination import Page, paginate

@router.get("/paginado", response_model=Page[AtletaListaResponse])
async def listar_atletas_paginado(
    nome: Optional[str] = None,
    cpf: Optional[str] = None,
):
    query = db.query(Atleta)

    if nome:
        query = query.filter(Atleta.nome.ilike(f"%{nome}%"))
    if cpf:
        query = query.filter(Atleta.cpf == cpf)

    return paginate(query)
A biblioteca também permite o uso de limit e offset diretamente, dependendo do Page/LimitOffsetPage configurado.

📦 Instalação e Execução
1. Clonar o repositório
bash
Copiar código
git clone https://github.com/seu-usuario/crossfit-academia-api.git
cd crossfit-academia-api
2. Criar e ativar ambiente virtual (opcional mas recomendado)
bash
Copiar código
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# ou
.venv\\Scripts\\activate   # Windows
3. Instalar dependências
Usando pip:

bash
Copiar código
pip install -r requirements.txt
Ou usando Poetry:

bash
Copiar código
poetry install
4. Rodar a aplicação
Com Uvicorn:

bash
Copiar código
uvicorn app.main:app --reload
A API estará disponível em:

http://127.0.0.1:8000

5. Documentação Interativa
O FastAPI gera automaticamente duas interfaces de documentação:

Swagger UI: http://127.0.0.1:8000/docs

Redoc: http://127.0.0.1:8000/redoc

🧪 Testes
Você pode adicionar testes com pytest para validar regras de negócio, resposta de endpoints, tratamento de exceções e paginação.

Exemplos de cenários para testar:

Criar atleta com CPF novo → deve retornar 201

Criar atleta com CPF duplicado → deve retornar 303 e mensagem correta

Listar atletas com filtros de nome e cpf

Verificar se a paginação está respeitando limit e offset

✅ Resumo do que foi implementado
 API assíncrona com FastAPI

 Endpoints para gestão de atletas

 Query parameters (nome, cpf, limit, offset)

 Resposta customizada no GET all atletas

 Tratamento de sqlalchemy.exc.IntegrityError com status 303

 Paginação com fastapi-pagination

📚 Próximos Passos (Sugestões)
Adicionar autenticação (JWT)

Criar módulos para centros de treinamento e competições

Implementar testes automatizados com CI

Dockerizar a aplicação

Feito com ❤️ usando Python + FastAPI.
