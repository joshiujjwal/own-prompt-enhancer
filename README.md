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

---

## 🚀 Improvement Proposals

### First-Principles Analysis
- **Using an LLM to improve prompts for another LLM introduces a meta-cost problem**: if the enhancement model is as capable as the target model, users could just prompt it directly; the value is only real when the enhancement is cheaper, faster, or more specialised than the target.
- **"Better prompts" is ill-defined without a ground-truth evaluation framework** — chain-of-thought scaffolding improves some tasks (reasoning, multi-step) and degrades others (creative, conversational); a one-size-fits-all enhancer will produce misleading improvements for a significant subset of use cases.
- **The SLM layer adds latency to every request** — users experience this as the product being slower than talking to the LLM directly; the enhancement must demonstrably improve output quality enough to justify the extra round-trip and cost.
- **Prompt enhancement is a moving target**: as frontier models improve their instruction-following, the delta between raw and enhanced prompts shrinks; long-term defensibility requires building task-specific or user-specific enhancement rather than generic rewriting.

### Key Risks & Assumptions
- **Assumes the enhancement model has enough knowledge of the target model's behaviour** — different LLMs respond differently to the same prompt structures (e.g., Claude prefers XML tags; GPT prefers numbered steps); a single enhancer trained or prompted generically may not transfer well.
- **No evaluation dataset or metric is defined** — without a way to measure "better", the system cannot be trained, tuned, or compared; this is the foundational missing piece for an ML product.
- **The "fine-tuned SLM" path and the "OpenAI/Anthropic rewrite chain" path have radically different cost, latency, and accuracy profiles** — the README treats them as equivalent alternatives, but the product strategy diverges entirely depending on which is primary.
- **Assumes users want to understand what changed** — the explain-changes feature is valuable for learning but adds tokens and latency; power users doing batch processing will disable it, so the architecture should make it optional from day one.

### Concrete Improvement Ideas
1. **Define a prompt quality benchmark before writing any model code** — curate 100 raw/enhanced prompt pairs with human-rated output quality scores; this becomes the training signal, evaluation harness, and marketing evidence simultaneously (highest leverage action).
2. **Make target-model awareness a first-class parameter** — accept a `--target-model` flag (e.g., `gpt-4o`, `claude-3-5-sonnet`) and use model-specific enhancement strategies; this turns a generic tool into a precision instrument.
3. **Add a side-by-side diff view in the UI** — show the raw vs enhanced prompt with colour-coded changes and a one-click "run both and compare outputs" feature; this makes the value proposition immediately tangible on first use.
4. **Build a feedback loop from outputs back to the enhancer** — let users rate the final LLM output (thumbs up/down) and use that signal to fine-tune or few-shot the enhancer; over time this creates a proprietary improvement dataset.
5. **Implement task-type detection as a pre-step** — classify the prompt into a task category (coding, analysis, creative, Q&A) before enhancing; apply category-specific enhancement templates; avoids applying reasoning scaffolding to creative requests.
