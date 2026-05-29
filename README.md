# OwnPromptEnhancer

> 🚧 **Status: Early Development**

A small language model (SLM) layer that sits between a user and a larger LLM. It takes raw, rough prompts and rewrites them with better structure, context injection, and chain-of-thought scaffolding — giving users "more thinking" from every prompt, effortlessly.

```
User Prompt → [OwnPromptEnhancer SLM Layer] → Enriched Prompt → [Main LLM] → Response
```

---

## Why This Exists

Most users write underdeveloped prompts. A dedicated enhancement layer can:
- Add chain-of-thought scaffolding automatically
- Inject relevant context and constraints
- Reformat vague requests into structured instructions
- Improve LLM output quality without user effort

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Enhancement API | Python 3.11+, FastAPI |
| ML Pipeline | Transformers (fine-tuned SLM) or OpenAI/Anthropic rewrite chain |
| Demo UI | React 18 + TypeScript + Vite |
| Testing | pytest (backend), Vitest (frontend) |
| Linting | ruff + mypy (Python), ESLint + tsc (TS) |
| Packaging | uv (Python), pnpm (Node) |

---

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 20+
- `uv` (`pip install uv`)
- `pnpm` (`npm install -g pnpm`)
- API key: `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` (for pipeline mode)

### Backend

```bash
cd own-prompt-enhancer
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
cp .env.example .env          # fill in API keys
uvicorn src.api.main:app --reload --port 8000
```

### Frontend (Demo UI)

```bash
cd ui
pnpm install
pnpm dev                      # starts at http://localhost:5173
```

### Run Tests

```bash
# Backend
pytest tests/ -v --tb=short

# Frontend
cd ui && pnpm test
```

### Lint & Type-Check

```bash
ruff check src/ tests/
mypy src/
cd ui && pnpm lint && pnpm tsc --noEmit
```

---

## Project Structure

```
own-prompt-enhancer/
├── src/
│   ├── enhancer/         # Core prompt enhancement logic
│   ├── api/              # FastAPI app, routes, schemas
│   ├── pipeline/         # LLM pipeline adapters (OpenAI, Anthropic, local)
│   └── models/           # Pydantic models and DB schemas
├── tests/
│   ├── unit/             # Unit tests (mirror src/)
│   └── integration/      # End-to-end API + pipeline tests
├── ui/                   # React + TypeScript demo UI
│   └── src/
│       ├── components/   # UI components
│       ├── hooks/        # Custom React hooks
│       ├── pages/        # Page-level components
│       └── types/        # TypeScript types
├── docs/
│   ├── spec.md           # Feature specification
│   └── adr/              # Architecture Decision Records
├── .github/
│   ├── copilot-instructions.md
│   └── instructions/
├── CLAUDE.md             # Anthropic agent context
├── AGENTS.md             # OpenAI Codex context
└── TODO.md               # Evidence-gated task breakdown
```

---

## Contributing

1. Read `TODO.md` and `docs/spec.md` before writing a line of code
2. **Write failing tests first** (red phase), then implement (green phase)
3. Every PR must include evidence: test output, before/after prompt examples
4. Keep PRs small and focused — one logical change per PR
5. Update `CLAUDE.md` or `AGENTS.md` if you learn something non-obvious
6. Do not remove or skip tests under any circumstances
