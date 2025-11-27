# API de Academia para Competição de Crossfit 🏋️‍♂️

Projeto de uma API REST assíncrona desenvolvida com **FastAPI** para gerenciar atletas de uma academia focada em competições de crossfit.

## Principais pontos implementados

- Query parameters em endpoints de atleta:
  - `nome`
  - `cpf`
- Resposta customizada no endpoint **GET /atletas** contendo:
  - `nome`
  - `centro_treinamento`
  - `categoria`
- Tratamento de `sqlalchemy.exc.IntegrityError` ao cadastrar atleta com CPF duplicado:
  - status code: **303**
  - mensagem: `Já existe um atleta cadastrado com o cpf: x`
- Paginação com **fastapi-pagination** usando `limit` e `offset` (modelo `LimitOffsetPage`).

## Como rodar

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- Swagger UI: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc
