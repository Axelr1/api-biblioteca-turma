"""
API Biblioteca da Turma
Trabalho "Crie sua API" - ARA0160 Sistemas Distribuídos e Computação Paralela

CRUD de livros com FastAPI. Os dados ficam em memória (uma lista),
então tudo volta ao estado inicial quando o servidor é reiniciado.
"""

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field

app = FastAPI(
    title="API Biblioteca da Turma",
    description="Cadastra, lista, atualiza e apaga os livros da biblioteca da turma.",
    version="1.0.0",
)


# ---------- Modelo de dados ----------

class LivroEntrada(BaseModel):
    """Campos que o cliente envia para cadastrar ou atualizar um livro."""
    titulo: str = Field(min_length=1, examples=["Dom Casmurro"])
    autor: str = Field(min_length=1, examples=["Machado de Assis"])
    ano: int = Field(examples=[1899])
    disponivel: bool = True  # opcional: se não vier, o livro está disponível


# ---------- "Banco de dados" em memória ----------

livros = [
    {"id": 1, "titulo": "Dom Casmurro", "autor": "Machado de Assis", "ano": 1899, "disponivel": True},
    {"id": 2, "titulo": "O Cortiço", "autor": "Aluísio Azevedo", "ano": 1890, "disponivel": True},
    {"id": 3, "titulo": "Vidas Secas", "autor": "Graciliano Ramos", "ano": 1938, "disponivel": False},
]
proximo_id = 4


def buscar_livro(livro_id: int) -> dict:
    """Procura o livro pelo id. Se não existir, responde 404."""
    for livro in livros:
        if livro["id"] == livro_id:
            return livro
    raise HTTPException(status_code=404, detail="Livro não encontrado")


# ---------- Validação: campo faltando ou inválido responde 400 ----------
# Por padrão o FastAPI responde 422. O trabalho pede 400, então trocamos aqui.

@app.exception_handler(RequestValidationError)
async def erro_de_validacao(request: Request, exc: RequestValidationError):
    erros = []
    for erro in exc.errors():
        campo = erro["loc"][-1]
        if erro["type"] == "missing":
            erros.append(f"O campo '{campo}' é obrigatório")
        else:
            erros.append(f"O campo '{campo}' é inválido: {erro['msg']}")
    return JSONResponse(status_code=400, content={"detail": erros})


# ---------- Endpoints ----------

@app.get("/livros", status_code=status.HTTP_200_OK)
def listar_livros():
    """Lista todos os livros."""
    return livros


@app.get("/livros/{livro_id}", status_code=status.HTTP_200_OK)
def mostrar_livro(livro_id: int):
    """Mostra um livro pelo id (404 se não existir)."""
    return buscar_livro(livro_id)


@app.post("/livros", status_code=status.HTTP_201_CREATED)
def cadastrar_livro(dados: LivroEntrada):
    """Cadastra um livro novo (400 se faltar campo obrigatório)."""
    global proximo_id
    novo_livro = {"id": proximo_id, **dados.model_dump()}
    livros.append(novo_livro)
    proximo_id += 1
    return novo_livro


@app.put("/livros/{livro_id}", status_code=status.HTTP_200_OK)
def atualizar_livro(livro_id: int, dados: LivroEntrada):
    """Atualiza um livro existente (404 se não existir, 400 se faltar campo)."""
    livro = buscar_livro(livro_id)
    livro.update(dados.model_dump())
    return livro


@app.delete("/livros/{livro_id}", status_code=status.HTTP_204_NO_CONTENT)
def apagar_livro(livro_id: int):
    """Apaga um livro (204 sem conteúdo, ou 404 se não existir)."""
    livro = buscar_livro(livro_id)
    livros.remove(livro)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
