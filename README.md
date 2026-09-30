# ComicCraft AI — Complete Generative AI Comic Story Creator

This project implements a complete working ComicCraft application based on the supplied smoke-test PDF. The reference story is “Milo the Brave Little Fox”, with Milo, a village/enchanted-forest setting, a warm/funny tone, colorful comic-book art, five story pages, and the moral about being kind, brave, and continuing to try.

## Stack

- Frontend: Streamlit
- Backend API: FastAPI
- LLM: OpenAI-compatible API, optional
- Image generation: OpenAI image API, optional
- Offline fallback: deterministic story + SVG comic panels
- PDF export: ReportLab
- Configuration: `.env`

## Windows / VS Code setup

Open the project folder in VS Code, then open Terminal.

```powershell
cd D:\DCIM\Documents\ComicCraftAI
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### Start backend

Terminal 1:

```powershell
python -m uvicorn app.main:app --reload --port 8000
```

Test:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

### Start frontend

Terminal 2:

```powershell
.\.venv\Scripts\Activate.ps1
python -m streamlit run frontend.py
```

Open the Streamlit URL, normally `http://localhost:8501`.

### Run smoke test

Keep the backend running, then:

```powershell
python smoke_test.py
```

Expected:

```text
ComicCraft smoke test passed.
```

## AI configuration

The app works without an API key. For external AI generation, put your provider key in `.env`:

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
OPENAI_IMAGE_MODEL=gpt-image-1
```

Never commit `.env`.

## Main API routes

- `GET /health`
- `POST /api/story/generate`
- `POST /api/comic/generate`
- `POST /api/comic/pdf`
