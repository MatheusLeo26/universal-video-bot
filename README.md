# Universal Video Download Bot

An asynchronous Python backend to extract dynamic video URLs from any platform using Playwright and send them to a download API.

## Architecture

This project is built as a REST API using **FastAPI** to orchestrate the video extraction and downloading process.

```
├── src/
│   ├── __init__.py
│   ├── config.py       # Configuration and environment variables management via Pydantic
│   ├── api_client.py   # HTTP client for interacting with the download API (HuntAPI)
│   ├── extractor.py    # Playwright based video metadata extraction
│   ├── schemas.py      # Pydantic models for API request/response validation
│   └── main.py         # FastAPI application entrypoint and background task orchestration
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api_client.py
│   └── test_extractor.py
├── .env.example
├── .gitignore
├── requirements.txt
├── postman_collection.json # Exported Postman collection for API testing
└── README.md
```

## Setup & Installation

1. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers:**
   ```bash
   playwright install chromium
   ```

4. **Environment Variables:**
   Copy `.env.example` to `.env` and fill in your API keys.
   ```bash
   cp .env.example .env
   ```
   > **Note**: To perform real downloads, make sure `HUNTAPI_BASE_URL` in your `.env` points to your actual production download API, as the default one is a placeholder mock.

## Running the API

Start the FastAPI server using Uvicorn:
```bash
uvicorn src.main:app --reload
```

### API Endpoints

Once the server is running on `http://127.0.0.1:8000/`, you can use the following methods:

- **Swagger UI:** Visit `http://127.0.0.1:8000/` or `http://127.0.0.1:8000/docs` to test endpoints directly from your browser.
- **Postman:** Import the `postman_collection.json` file found in the root of the project to get all pre-configured endpoints and tests.

Core Routes:
- `POST /api/v1/process`: Starts the asynchronous Playwright extraction and download job. Returns a `job_id`.
- `GET /api/v1/status/{job_id}`: Polls the current status of the download (`processing`, `completed`, or `failed`).

## Running Tests

Execute the test suite using `pytest`:
```bash
pytest -v
```

## Conventional Commits Examples

This project follows [Conventional Commits](https://www.conventionalcommits.org/):

1. `feat(api): add fastapi endpoints for process and status checking`
2. `feat(extractor): implement playwright network interception`
3. `fix(client): handle timeout exceptions during api requests`
4. `test(api): add postman collection schema for route validation`
5. `chore(deps): add fastapi and uvicorn dependencies`
