# AGENTS.md — OwnPromptEnhancer

Setup and workflow instructions for OpenAI Codex and compatible coding agents.

---

## Setup

```bash
# 1. Clone and enter repo
git clone https://github.com/joshiujjwal/own-prompt-enhancer.git
cd own-prompt-enhancer

# 2. Backend
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
cp .env.example .env

# 3. Frontend
cd ui && pnpm install && cd ..
```

---

## Running Tests

```bash
# All backend tests
pytest tests/ -v --tb=short

# Watch mode (requires pytest-watch)
ptw tests/

# Frontend tests
cd ui && pnpm test

# Frontend watch
cd ui && pnpm test --watch
```

**Rule: write tests first. Never implement before a failing test exists.**

---

## Linting & Type Checking

```bash
ruff check src/ tests/           # lint
ruff format src/ tests/          # auto-format
mypy src/                        # strict type checking
cd ui && pnpm lint               # ESLint
cd ui && pnpm tsc --noEmit       # TypeScript check
```

All commands must pass before committing.

---

## Code Style — Python

- Python 3.11+; use `X | None` over `Optional[X]`; use `match` statements where appropriate
- All public functions/methods have type annotations — no `Any` unless unavoidable
- All async functions use `async def`; no `asyncio.run()` inside library code
- Pydantic v2 models: use `model_validator`, `field_validator`, `model_config`
- Line length: 100. Imports: sorted by `ruff` (isort-compatible)
- Docstrings: one-line for simple functions; Google style for complex ones
- Exception hierarchy: define custom exceptions in `src/enhancer/exceptions.py`

## Code Style — TypeScript / React

- TypeScript strict mode; no `any`; prefer `unknown` + narrowing
- React functional components only; hooks for all state
- TanStack Query for all API calls — no raw `fetch` in components
- Component files: PascalCase. Hook files: `use` prefix camelCase
- Props interfaces defined in same file as component (or in `types/` if shared)
- No `useEffect` for data fetching — use `useQuery`/`useMutation`

---

## PR Instructions

Every pull request must include:

1. **Evidence section** — paste `pytest -v` output (all green) in PR description
2. **Before/After example** — at least one raw → enhanced prompt pair demonstrating the feature
3. **Checklist:**
   - [ ] Tests written before implementation (red → green)
   - [ ] No new `mypy` or `ruff` errors
   - [ ] `pnpm tsc --noEmit` passes (if UI touched)
   - [ ] `.env.example` updated if new env vars added
   - [ ] `CLAUDE.md` / `AGENTS.md` updated if non-obvious convention added

---

## Architecture Invariants

- `src/enhancer/` must have **zero imports** from `src/api/` — the enhancement engine is framework-agnostic
- `src/pipeline/` adapters must be **mockable**: accept injected clients, not global singletons
- All routes in `src/api/` must go through the `PromptEnhancer` orchestrator — no direct adapter calls in route handlers
- The UI `types/api.ts` must stay in sync with `src/models/prompt.py`

---

## File Ownership

| Path | Responsibility |
|------|---------------|
| `src/enhancer/strategies/` | Strategy authors |
| `src/api/` | API layer only; no ML logic here |
| `src/pipeline/` | Adapter authors; external API integration |
| `tests/unit/` | Must mirror `src/` 1:1 |
| `docs/spec.md` | Source of truth — ask before changing |
| `TODO.md` | Living task tracker — update as you go |
