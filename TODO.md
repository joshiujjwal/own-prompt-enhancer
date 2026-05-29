# OwnPromptEnhancer — Task Breakdown

## How to Use This File

Every task follows this loop:
1. **Read** `docs/spec.md` for acceptance criteria
2. **Run existing tests** — they must stay green before you start
3. **Write failing tests first** (red phase)
4. **Implement** until tests pass (green phase)
5. **Review diff manually** — check for regressions, hardcoded values, dead code
6. **Commit** with a descriptive message referencing the task
7. **Update** `CLAUDE.md`/`AGENTS.md` with anything non-obvious you learned (compound loop)

Evidence required before closing any phase:
- All tests in that phase pass (`pytest -v` or `pnpm test`)
- At least one before/after prompt pair demonstrating the feature works
- Manual review signed off in PR description

---

## Phase 0: Foundation ⬜

### Package & Build Setup
- [ ] Create `pyproject.toml` with `[project]`, `[project.optional-dependencies]` (dev), and tool configs (ruff, mypy, pytest)
- [ ] Create `uv.lock` via `uv pip install -e ".[dev]"`
- [ ] Create `ui/package.json` with Vite + React + TypeScript + Vitest
- [ ] Add `pnpm-lock.yaml` via `pnpm install`

### Linting & Formatting
- [ ] Configure `ruff` (line-length 100, select E/F/I/UP, target py311)
- [ ] Configure `mypy` (strict mode, `src/` layout)
- [ ] Configure ESLint with TypeScript + React rules in `ui/eslint.config.ts`
- [ ] Verify `ruff check src/` and `mypy src/` pass on empty scaffold

### Test Framework
- [ ] Write first smoke test: `tests/unit/test_smoke.py` — imports `src.enhancer` without error
- [ ] Write first frontend smoke test: `ui/src/__tests__/smoke.test.ts` — renders `<App />` without throwing
- [ ] Both suites run green

### CI
- [ ] Create `.github/workflows/ci.yml` — runs `pytest` + `ruff` + `mypy` + `pnpm test` + `pnpm tsc`
- [ ] CI passes on `main` branch

### Review AI Config
- [ ] Read `CLAUDE.md`, `AGENTS.md`, `.github/copilot-instructions.md`
- [ ] Update any commands that don't match actual setup

---

## Phase 1: Core Enhancement Engine ⬜

### Pydantic Schemas
- [ ] `src/models/prompt.py` — `RawPrompt`, `EnhancedPrompt`, `EnhancementRequest`, `EnhancementResponse`
  - Fields: `text`, `metadata` (model target, domain hint, verbosity), `enhancement_strategy`
  - Evidence: unit tests for serialization/validation edge cases (empty string, very long input, special chars)

### Enhancement Strategies (red → green each)
- [ ] `src/enhancer/strategies/base.py` — `BaseEnhancementStrategy` abstract class with `enhance(raw: str) -> str`
- [ ] `src/enhancer/strategies/cot_injector.py` — wraps prompt in chain-of-thought scaffolding
  - Tests: given 3 raw prompts, output contains "Let's think step by step" or equivalent CoT marker
- [ ] `src/enhancer/strategies/structure_formatter.py` — converts vague sentence into `## Goal / ## Context / ## Constraints` blocks
  - Tests: output always contains the three section headers
- [ ] `src/enhancer/strategies/context_enricher.py` — injects domain vocabulary and role framing ("You are an expert in...")
  - Tests: output contains role prefix; domain hint is reflected in vocabulary

### Pipeline Adapters
- [ ] `src/pipeline/base.py` — `BasePipelineAdapter` with `rewrite(prompt: str) -> str`
- [ ] `src/pipeline/openai_adapter.py` — uses OpenAI Chat API with system prompt to rewrite
  - Tests: mock `openai.AsyncOpenAI`; assert correct system prompt sent; assert response text returned
- [ ] `src/pipeline/anthropic_adapter.py` — uses Anthropic Messages API
  - Tests: mock `anthropic.AsyncAnthropic`; same assertions
- [ ] `src/pipeline/local_adapter.py` — loads a local HuggingFace model (e.g., `Phi-3-mini`) for rewriting
  - Tests: mock `transformers.pipeline`; assert tokenizer called, output decoded

### Enhancer Orchestrator
- [ ] `src/enhancer/orchestrator.py` — `PromptEnhancer` class: accepts strategy + adapter, runs them in order
  - Tests: compose CoT injector + OpenAI adapter mock; assert chain executed in correct order
  - Tests: empty input raises `ValueError`; input > 4096 chars raises `PromptTooLongError`

---

## Phase 2: FastAPI Service ⬜

### App Bootstrap
- [ ] `src/api/main.py` — FastAPI app with lifespan handler, CORS, and `/health` route
  - Tests: `GET /health` returns `{"status": "ok"}`

### Routes
- [ ] `POST /v1/enhance` — accepts `EnhancementRequest`, returns `EnhancementResponse`
  - Tests: valid request → 200 + enhanced text present
  - Tests: empty `text` → 422 Unprocessable Entity
  - Tests: unknown `strategy` → 400 Bad Request
- [ ] `GET /v1/strategies` — returns list of available strategies with descriptions
  - Tests: response is a list; each item has `id` and `description`
- [ ] `POST /v1/enhance/batch` — accepts list of prompts (max 20), returns list of enhanced prompts
  - Tests: batch of 3 → 3 responses; batch of 21 → 400

### Middleware & Config
- [ ] `src/api/config.py` — Pydantic `Settings` from env (API keys, model name, max prompt length, rate limit)
- [ ] Rate-limiting middleware: max 60 req/min per IP (use `slowapi`)
  - Tests: 61st request in 60s → 429 Too Many Requests
- [ ] Request/response logging middleware (structured JSON via `structlog`)

### Integration Tests
- [ ] `tests/integration/test_api.py` — `httpx.AsyncClient` against live FastAPI app (all adapters mocked)
  - Tests cover: happy path, validation errors, rate limit, health check

---

## Phase 3: Demo UI ⬜

### Layout & Routing
- [ ] `ui/src/pages/EnhancerPage.tsx` — two-panel layout: raw prompt input (left) + enhanced output (right)
- [ ] `ui/src/pages/StrategyPage.tsx` — strategy selector with descriptions fetched from `GET /v1/strategies`
- [ ] React Router v6 setup; routes: `/` → EnhancerPage, `/strategies` → StrategyPage
  - Tests: routes render correct page components (Vitest + React Testing Library)

### Core Components
- [ ] `ui/src/components/PromptInput.tsx` — textarea with char counter, max 4096
  - Tests: typing updates state; over limit shows warning; submit button disabled when empty
- [ ] `ui/src/components/EnhancedOutput.tsx` — read-only display with diff highlighting (original vs enhanced)
  - Tests: renders enhanced text; copy-to-clipboard button copies correct text
- [ ] `ui/src/components/StrategySelector.tsx` — radio group bound to strategy ID
  - Tests: selecting option fires `onChange`; default is `cot_injector`
- [ ] `ui/src/components/MetadataPanel.tsx` — collapsible panel: domain hint, verbosity slider, target model selector

### API Hook
- [ ] `ui/src/hooks/useEnhancer.ts` — `useMutation` hook (TanStack Query) calling `POST /v1/enhance`
  - Tests: loading state set during fetch; error state set on 4xx; data state set on 200
- [ ] `ui/src/hooks/useStrategies.ts` — `useQuery` hook for `GET /v1/strategies`

### UX Polish
- [ ] Loading skeleton while enhancement in-flight
- [ ] Toast notification on copy success / API error
- [ ] Keyboard shortcut: `Cmd+Enter` submits enhancement
  - Tests: keydown event triggers submission

---

## Phase 4: Evaluation Harness ⬜

### Metrics
- [ ] `src/enhancer/eval/metrics.py` — compute: token delta, CoT marker presence, structural section count, readability score (Flesch)
  - Tests: known input → known metric values
- [ ] `src/enhancer/eval/runner.py` — run enhancement pipeline on a JSONL benchmark file, output metrics CSV
  - Tests: mock pipeline; assert CSV rows match input count

### Benchmark Dataset
- [ ] `data/benchmark_prompts.jsonl` — 50 raw prompts with human-written gold enhanced versions (diverse domains)
- [ ] `data/README.md` — explains format: `{"id", "raw", "gold_enhanced", "domain", "difficulty"}`

### Eval CLI
- [ ] `scripts/eval.py` — CLI: `python scripts/eval.py --adapter openai --strategy cot_injector --output results.csv`
  - Tests: argparse config; output file created; summary printed to stdout

---

## Phase 5: Fine-Tuning Pipeline ⬜

> Optional path: use if you want a local SLM instead of API-based rewriting

- [ ] `scripts/prepare_finetune_data.py` — converts benchmark JSONL to HuggingFace `datasets` format (instruction-following)
- [ ] `scripts/finetune.py` — LoRA fine-tune Phi-3-mini (or similar ≤7B model) on the prepared dataset
  - Uses `peft` + `trl` + `transformers`
  - Saves adapter to `models/ope-enhancer-v1/`
- [ ] `src/pipeline/local_adapter.py` — update to load LoRA adapter from `models/` path
- [ ] Eval fine-tuned model vs. API-based pipeline; document delta in `docs/adr/0002-model-choice.md`

---

## Phase 6: Polish & Harden ⬜

- [ ] OpenAPI docs auto-generated at `/docs` — verify all routes documented with examples
- [ ] `Dockerfile` — multi-stage: builder installs deps, runtime runs uvicorn on port 8000
- [ ] `docker-compose.yml` — `api` service + optional `ui` service behind nginx
- [ ] Secrets never in source; `.env.example` documents all required keys
- [ ] `SECURITY.md` — responsible disclosure policy
- [ ] All tests pass in CI with `--tb=short`; coverage ≥ 80%

---

## Phase 7: Ship ⬜

- [ ] Tag `v0.1.0` once Phase 0–3 complete with passing CI
- [ ] Write `CHANGELOG.md` entry for v0.1.0
- [ ] Deploy API to Railway / Fly.io / Modal (document in `docs/deployment.md`)
- [ ] Deploy UI to Vercel (document in `docs/deployment.md`)
- [ ] Post demo: 5 before/after prompt pairs showing measurable quality improvement

---

## Parking Lot 🅿️

- Streaming endpoint: `POST /v1/enhance/stream` with SSE for real-time rewrite display
- Prompt versioning: store original + all enhanced variants per session
- User feedback loop: thumbs up/down on enhanced prompts → fine-tuning data flywheel
- Plugin system: allow custom strategy plugins loaded from `~/.ope/strategies/`
- VS Code extension for in-editor prompt enhancement

---

## Lessons Learned 📝

_Update this section as you discover non-obvious truths about the codebase._

- [ ] _(empty — add your first lesson here)_
