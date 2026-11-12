# Tasks API

API REST para cadastro e gerenciamento de usuários e tarefas. Cada tarefa pertence a um usuário e pode ser marcada como concluída. O projeto demonstra uma organização em camadas com Flask, validação de dados e persistência relacional.

<!-- > **Atenção:** a API ainda não implementa autenticação e atualmente armazena e devolve senhas sem proteção. Use apenas em desenvolvimento/estudo; não a utilize com dados reais sem implementar, no mínimo, hash de senhas e autenticação. -->

## Funcionalidades

- Criar, consultar, atualizar e excluir usuários.
- Criar, listar, filtrar, consultar, atualizar e excluir tarefas.
- Validar corpos e parâmetros com Pydantic.
- Persistir os dados com SQLAlchemy; o banco pode ser SQLite ou outro banco compatível com a URL configurada.
- Consultar a documentação interativa gerada pelo Flasgger.
- Verificar a disponibilidade da API por uma rota de health check.

## Tecnologias

- **Python 3.12** — versão usada pela imagem Docker do projeto.
- **Flask** — servidor HTTP e roteamento.
- **SQLAlchemy** — mapeamento e acesso ao banco de dados.
- **Pydantic 2** e **pydantic-settings** — validação dos dados e leitura das configurações.
- **Flasgger** — documentação Swagger/OpenAPI, definida em [`swagger.yml`](./swagger.yml).
- **pytest** — testes das rotas.
- **SQLite** — opção simples para desenvolvimento local.

## Como funciona

As rotas recebem as requisições HTTP e chamam os serviços, que aplicam as regras da aplicação. Os repositórios concentram as consultas e alterações no banco; os modelos SQLAlchemy representam as tabelas e os schemas Pydantic validam os dados de entrada e saída.

Ao iniciar, a aplicação registra as rotas e cria as tabelas que ainda não existem no banco configurado. As configurações são carregadas do arquivo `.env` na raiz do projeto. `ENV=test` faz a conexão usar `TEST_DATABASE_URL`; nos demais ambientes, usa `DATABASE_URL`.

## Pré-requisitos

- Python 3.12
- `pip`

## Executar localmente

Na raiz do repositório:

1. Crie e ative um ambiente virtual:

   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   ```

   No Windows PowerShell, use:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Crie um arquivo `.env` na raiz com as configurações necessárias:

   ```dotenv
   APP_NAME=Tasks API
   ENV=development
   DATABASE_URL=sqlite:///./tasks_database.db
   TEST_DATABASE_URL=sqlite:///./test_tasks.db
   ```

   As duas URLs de banco são necessárias porque as configurações são obrigatórias. Os caminhos SQLite acima criam os arquivos na raiz do projeto.

4. Inicie o servidor:

   ```bash
   python app.py
   ```

   A aplicação roda em modo debug em `http://127.0.0.1:5000`. A interface Swagger fica disponível em `http://127.0.0.1:5000/apidocs/`.

## Rotas

Todas as rotas de negócio estão sob `/v1`.

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/health/` | Verifica se a API está disponível. |
| `POST` | `/v1/users` | Cria um usuário. |
| `GET` | `/v1/users/{id_ou_email}` | Busca um usuário por ID numérico ou e-mail. |
| `PATCH` | `/v1/users` | Atualiza um usuário; o corpo deve incluir `id` e `password`. |
| `DELETE` | `/v1/users/{user_id}` | Exclui um usuário. A operação é recusada se ele tiver tarefas associadas. |
| `POST` | `/v1/tasks` | Cria uma tarefa para um usuário existente. |
| `GET` | `/v1/tasks?user_id={id}` | Lista as tarefas de um usuário. |
| `GET` | `/v1/tasks?user_id={id}&completed={true\|false}` | Filtra as tarefas do usuário pelo estado de conclusão. |
| `GET` | `/v1/tasks/{task_id}` | Busca uma tarefa por ID. |
| `PATCH` | `/v1/tasks` | Atualiza uma tarefa; o corpo deve incluir `id`. |
| `DELETE` | `/v1/tasks/{task_id}` | Exclui uma tarefa. |

### Exemplos

Criar um usuário:

```bash
curl -X POST http://127.0.0.1:5000/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ana",
    "email": "ana@example.com",
    "password": "senha-de-exemplo"
  }'
```

Na resposta, copie o `id` retornado e use-o para criar uma tarefa:

```bash
curl -X POST http://127.0.0.1:5000/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Revisar documentação",
    "description": "Conferir os exemplos da API",
    "user_id": 1
  }'
```

Listar as tarefas do usuário e filtrar as concluídas:

```bash
curl "http://127.0.0.1:5000/v1/tasks?user_id=1"
curl "http://127.0.0.1:5000/v1/tasks?user_id=1&completed=true"
```

As respostas de criação usam HTTP `201`; consultas e atualizações usam `200`; exclusões bem-sucedidas usam `204`. Dados ou parâmetros inválidos normalmente retornam `400`, e recursos não encontrados retornam `404`.

## Testes

Com as dependências instaladas e o arquivo `.env` configurado:

```bash
python -m pytest
```

O `pytest.ini` define `ENV=test`, então os testes usam a URL indicada em `TEST_DATABASE_URL`.

## Docker

Há um [`Dockerfile`](./Dockerfile) que expõe a porta `5000` e configura o Gunicorn como servidor. Para executar essa imagem, configure as variáveis `APP_NAME`, `ENV`, `DATABASE_URL` e `TEST_DATABASE_URL` no contêiner. Observe que `gunicorn` não está listado atualmente em `requirements.txt`; portanto, a inicialização configurada no Dockerfile exige que essa dependência esteja disponível na imagem.
