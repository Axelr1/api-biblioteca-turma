# API Biblioteca da Turma

Trabalho em grupo **"Crie sua API"** da disciplina **ARA0160 · Sistemas Distribuídos e Computação Paralela**
(Estácio UNIMETA · Bacharelado em Sistemas de Informação).

A API cadastra, lista, atualiza e apaga os livros da biblioteca da turma (CRUD: Create, Read, Update, Delete).
As respostas são em JSON e os dados ficam em memória, numa lista em Python.

## Integrantes

- João Gabriel Wisnievski
- Pedro Henrique Santos Nogueira

## Ferramentas utilizadas

- **Python 3.10+**
- **FastAPI**: framework para criar a API
- **Uvicorn**: servidor que roda a API
- **Página /docs do FastAPI (Swagger)**: para testar os endpoints
- **Git e GitHub**: versionamento e entrega
- **Claude (IA da Anthropic)**: usado como apoio (ver seção "Uso de IA")

## Como rodar

1. Instale o Python 3.10 ou mais novo.
2. Baixe o projeto:
   ```bash
   git clone https://github.com/Axelr1/api-biblioteca-turma.git
   cd api-biblioteca-turma
   ```
3. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux / macOS
   source venv/bin/activate
   ```
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
5. Rode a API:
   ```bash
   uvicorn main:app --reload
   ```
6. A API fica em `http://127.0.0.1:8000`.

## Como testar

O jeito mais fácil é abrir **http://127.0.0.1:8000/docs** no navegador.
Clique em um endpoint, depois em **Try it out** e em **Execute**.

Também dá para testar com Postman, Insomnia ou Thunder Client (VS Code), usando os endpoints abaixo.

Os testes que fizemos:

| Teste | Resultado esperado |
|---|---|
| `GET /livros` | 200 com a lista de livros |
| `GET /livros/1` | 200 com o livro |
| `GET /livros/99` (não existe) | 404 |
| `POST /livros` com todos os campos | 201 com o livro criado |
| `POST /livros` sem o campo `titulo` | 400 |
| `PUT /livros/1` com todos os campos | 200 com o livro atualizado |
| `PUT /livros/99` (não existe) | 404 |
| `DELETE /livros/1` | 204 (sem conteúdo) |
| `DELETE /livros/99` (não existe) | 404 |

## Endpoints

| Método | Endpoint | O que faz | Resposta |
|---|---|---|---|
| GET | `/livros` | Lista todos os livros | 200 + lista |
| GET | `/livros/{id}` | Mostra um livro | 200 ou 404 |
| POST | `/livros` | Cadastra um livro novo | 201 ou 400 |
| PUT | `/livros/{id}` | Atualiza um livro | 200, 400 ou 404 |
| DELETE | `/livros/{id}` | Apaga um livro | 204 ou 404 |

### Campos de um livro

| Campo | Tipo | Obrigatório |
|---|---|---|
| `titulo` | texto | sim |
| `autor` | texto | sim |
| `ano` | número inteiro | sim |
| `disponivel` | verdadeiro/falso | não (padrão: `true`) |

O `id` é gerado pela API.

## Exemplo

**Cadastrar um livro**

```http
POST /livros
Content-Type: application/json

{
  "titulo": "Iracema",
  "autor": "José de Alencar",
  "ano": 1865
}
```

Resposta `201 Created`:

```json
{
  "id": 4,
  "titulo": "Iracema",
  "autor": "José de Alencar",
  "ano": 1865,
  "disponivel": true
}
```

**Cadastrar sem campo obrigatório**

```http
POST /livros
Content-Type: application/json

{
  "autor": "José de Alencar",
  "ano": 1865
}
```

Resposta `400 Bad Request`:

```json
{
  "detail": ["O campo 'titulo' é obrigatório"]
}
```

**Buscar um livro que não existe**

```http
GET /livros/99
```

Resposta `404 Not Found`:

```json
{
  "detail": "Livro não encontrado"
}
```

## Observações

- Os dados ficam em memória: ao reiniciar o servidor, a lista volta aos 3 livros iniciais.
- O FastAPI responde 422 por padrão quando falta um campo. Como o trabalho pede 400, o arquivo `main.py`
  tem um tratamento (`erro_de_validacao`) que troca a resposta para 400 com uma mensagem em português.
