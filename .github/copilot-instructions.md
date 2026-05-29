# OwnPromptEnhancer — GitHub Copilot Instructions

## Project Context

OwnPromptEnhancer is a Python + FastAPI backend with a React + TypeScript frontend.
It provides an SLM-based enhancement layer that rewrites raw prompts into structured,
chain-of-thought-rich prompts before passing them to a main LLM.

Architecture: `User → POST /v1/enhance → PromptEnhancer → Strategy(s) → PipelineAdapter → Enhanced Prompt`

---

## Stack

- **Backend:** Python 3.11, FastAPI, Pydantic v2, uvicorn, slowapi, structlog, httpx
- **ML:** transformers, peft, trl, tiktoken (OpenAI), anthropic SDK
- **Testing (backend):** pytest, pytest-asyncio, pytest-mock, httpx
- **Frontend:** React 18, TypeScript 5, Vite, TanStack Query v5, React Router v6
- **Testing (frontend):** Vitest, React Testing Library
- **Linting:** ruff (Python), ESLint + typescript-eslint (TS)

---

## Coding Conventions

### Python
- Use `async def` for all adapter and route functions
- All Pydantic models live in `src/models/`; never define inline in routes
- Custom exceptions in `src/enhancer/exceptions.py`; catch them in middleware and return structured HTTP errors
- Inject dependencies via FastAPI `Depends()` — never instantiate adapters inside route functions
- Use `src.api.config.Settings` (singleton via `lru_cache`) for all config; never call `os.getenv` directly

### TypeScript / React
- Prefer `const` arrow functions for components: `const MyComponent: React.FC<Props> = ({ ... }) => ...`
- All API response types must be in `ui/src/types/api.ts` — no inline types in hook files
- Use `useQuery` for GET endpoints, `useMutation` for POST — never raw `fetch` or `axios`
- Error boundaries required for page-level components

---

## Testing Conventions

- **Write the test first** — red then green
- Test file names: `test_<module_name>.py` / `<ComponentName>.test.tsx`
- Every strategy must have tests for: happy path, empty input, oversized input
- Mock adapters at the boundary: mock `openai.AsyncOpenAI` client, not the adapter class itself
- Use `pytest.mark.asyncio` (or `asyncio_mode = "auto"`) for all async tests
- Minimum coverage: 80% backend, 70% frontend — enforced in CI

---

## Boundaries

- **Do not** refactor working code unless explicitly asked
- **Do not** remove or skip tests to fix CI — fix the underlying code
- **Do not** add new dependencies without updating `pyproject.toml` (backend) or `ui/package.json` (frontend)
- **Do not** hardcode API keys, model names, or URLs — use `Settings` / env vars
- **Do not** change `EnhancementRequest` / `EnhancementResponse` field names without also updating `ui/src/types/api.ts`
- **Do not** add business logic to route handlers — routes call orchestrator, orchestrator calls strategies/adapters
- **Do not** generate random data or fake metrics in eval scripts — only real pipeline output
