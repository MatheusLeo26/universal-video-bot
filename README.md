# Universal Video Download Bot

Um backend assíncrono em Python para extrair URLs dinâmicas de vídeos de qualquer plataforma usando o Playwright e enviá-las para uma API de download.

## Arquitetura

Este projeto foi construído como uma API REST usando **FastAPI** para orquestrar o processo de extração e download de vídeos.

```text
├── src/
│   ├── __init__.py
│   ├── config.py       # Configurações e variáveis de ambiente via Pydantic
│   ├── api_client.py   # Client HTTP para interagir com a API de download (HuntAPI)
│   ├── extractor.py    # Extração de metadados do vídeo baseada no Playwright
│   ├── schemas.py      # Modelos Pydantic para validação de requisições/respostas da API
│   └── main.py         # Ponto de entrada da aplicação FastAPI e orquestração das tarefas em background
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api_client.py
│   └── test_extractor.py
├── .env.example
├── .gitignore
├── requirements.txt
├── postman_collection.json # Coleção do Postman exportada para testes da API
└── README.md
```

## Configuração e Instalação

1. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: .\venv\Scripts\activate
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Instale os navegadores do Playwright:**
   ```bash
   playwright install chromium
   ```

4. **Variáveis de Ambiente:**
   Copie o arquivo `.env.example` para `.env` e preencha com as suas chaves de API.
   ```bash
   cp .env.example .env
   ```
   > **Aviso**: Para realizar downloads reais, certifique-se de que a variável `HUNTAPI_BASE_URL` no seu `.env` aponte para a sua API de download em produção real, pois o valor padrão é um mock (simulação).

## Executando a API

Você pode iniciar o servidor de duas maneiras: diretamente na sua máquina local ou através do Docker.

### Opção 1: Via Máquina Local (Uvicorn)
Inicie o servidor FastAPI localmente:
```bash
uvicorn src.main:app --reload
```

### Opção 2: Via Docker (Recomendado para Produção)
Se você possui o Docker instalado, basta executar o Docker Compose na raiz do projeto. Ele já cuidará de todas as dependências complexas de navegadores e criará um volume para a sua pasta de downloads:
```bash
docker-compose up --build -d
```
O servidor estará rodando perfeitamente e acessível na mesma porta (8000). Para ver os logs, use `docker-compose logs -f`.

---

### Endpoints da API

Assim que o servidor estiver rodando em `http://127.0.0.1:8000/`, você poderá utilizar os seguintes métodos:

- **Swagger UI:** Acesse `http://127.0.0.1:8000/` ou `http://127.0.0.1:8000/docs` para testar os endpoints diretamente do seu navegador.
- **Postman:** Importe o arquivo `postman_collection.json` localizado na raiz do projeto para obter todos os endpoints e testes pré-configurados.

Rotas Principais:
- `POST /api/v1/process`: Inicia a tarefa assíncrona de extração via Playwright e o download do vídeo. Retorna um `job_id`.
- `GET /api/v1/status/{job_id}`: Consulta o status atual do download (`processing`, `completed` ou `failed`).

## Executando os Testes

Execute a suíte de testes utilizando o `pytest`:
```bash
pytest -v
```

## Exemplos de Conventional Commits

Este projeto segue as boas práticas de [Conventional Commits](https://www.conventionalcommits.org/):

1. `feat(api): add fastapi endpoints for process and status checking`
2. `feat(extractor): implement playwright network interception`
3. `fix(client): handle timeout exceptions during api requests`
4. `test(api): add postman collection schema for route validation`
5. `chore(deps): add fastapi and uvicorn dependencies`
