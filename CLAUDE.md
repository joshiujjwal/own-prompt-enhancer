# CLAUDE.md — OwnPromptEnhancer

Context file for Anthropic Claude and similar agents. Keep under 200 lines.  
**Start every session by running the test suite before writing any code.**

---

## Quick Commands

```bash
# Backend
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
uvicorn src.api.main:app --reload --port 8000

pytest tests/ -v --tb=short                  # run all tests
pytest tests/unit/ -v --tb=short             # unit only
pytest tests/integration/ -v --tb=short      # integration only
ruff check src/ tests/                        # lint
ruff format src/ tests/                       # format
mypy src/                                     # type-check

# Frontend
cd ui
pnpm install
pnpm dev                                      # dev server → http://localhost:5173
pnpm test                                     # vitest
pnpm lint                                     # eslint
pnpm tsc --noEmit                             # type-check

# Eval harness
python scripts/eval.py --adapter openai --strategy composite --output results.csv
```

---

## Directory Map

```
src/
  enhancer/
    strategies/       # One file per strategy: base.py, cot_injector.py, etc.
    orchestrator.py   # PromptEnhancer: composes strategy + adapter
    eval/             # Metrics and eval runner (Phase 4)
  api/
    main.py           # FastAPI app, lifespan, CORS, routes
    config.py         # Pydantic Settings (reads from .env)
    middleware.py     # Rate limiting (slowapi), structured logging (structlog)
  pipeline/
    base.py           # BasePipelineAdapter ABC
    openai_adapter.py # Async OpenAI rewriter
    anthropic_adapter.py
    local_adapter.py  # HuggingFace local model
  models/
    prompt.py         # EnhancementRequest, EnhancementResponse, StrategyInfo, etc.

tests/
  unit/               # Mirror src/ structure; mock all I/O
  integration/        # Use httpx.AsyncClient + TestClient; adapters mocked

ui/src/
  components/         # Dumb UI components (PromptInput, EnhancedOutput, etc.)
  hooks/              # useEnhancer, useStrategies (TanStack Query)
  pages/              # EnhancerPage, StrategyPage
  types/              # TypeScript interfaces mirroring Pydantic models

docs/
  spec.md             # Source of truth for what to build
  adr/                # Architecture Decision Records (numbered 0001+)

scripts/
  eval.py             # CLI eval runner
  prepare_finetune_data.py
  finetune.py
```

---

## Workflow

1. **Read TODO.md** — pick the next unchecked task
2. **Run `pytest tests/ -v`** — all existing tests must be green before you start
3. **Write failing test(s) first** — red phase; test names must describe behavior
4. **Implement** until those tests pass — green phase
5. **Run full suite** — no regressions
6. **Run linters**: `ruff check` + `mypy src/` + `cd ui && pnpm lint && pnpm tsc`
7. **Commit** with message: `feat(scope): what you did`
8. **Update this file** if you learned something non-obvious

---

## Non-Obvious Conventions

- **Async throughout**: all adapter methods are `async def`. Use `pytest-asyncio` with `asyncio_mode = "auto"` in `pyproject.toml`.
- **Strategy registry**: strategies are registered in `src/enhancer/strategies/__init__.py` as a `dict[StrategyID, type[BaseEnhancementStrategy]]`. Never import strategy classes directly in routes.
- **Config via Pydantic Settings**: `src/api/config.py` reads `.env`. Never use `os.getenv` directly elsewhere.
- **No bare `except`**: always catch specific exceptions. Unhandled adapter errors should surface as `502` with structured error body.
- **Token counting**: use `tiktoken` for OpenAI adapter, `anthropic.count_tokens` for Anthropic; local adapter uses `tokenizer.encode` length.
- **Test isolation**: each test that calls an adapter must mock it. Fixture: `@pytest.fixture def mock_openai_adapter(mocker): ...` in `conftest.py`.
- **UI ↔ API types**: keep `ui/src/types/api.ts` in sync with `src/models/prompt.py` manually (no auto-gen in v0.1).
- **CORS**: dev origin `http://localhost:5173` whitelisted; production origin set via `ALLOWED_ORIGINS` env var.
- **Rate limiting**: `slowapi` uses Redis in production (`RATE_LIMIT_STORAGE_URL`), in-memory dict in tests/dev.

---

## Environment Variables (see `.env.example`)

```
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
ADAPTER=openai                    # openai | anthropic | local
LOCAL_MODEL_PATH=models/ope-v1/   # used only when ADAPTER=local
MAX_PROMPT_LENGTH=4096
RATE_LIMIT=60/minute
ALLOWED_ORIGINS=http://localhost:5173
LOG_LEVEL=INFO
```

---

## What Claude Should NOT Do

- Do not switch adapters at runtime — adapter is selected at startup via config
- Do not skip tests or comment them out to make CI pass
- Do not add dependencies without updating `pyproject.toml` and `ui/package.json`
- Do not hardcode API keys anywhere in source
- Do not rename `EnhancementRequest`/`EnhancementResponse` — the UI TypeScript types mirror these names
