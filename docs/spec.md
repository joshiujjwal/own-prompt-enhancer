# OwnPromptEnhancer — Feature Specification

**Version:** 0.1.0-draft  
**Author:** joshiujjwal  
**Status:** 🟡 In Review

---

## 1. Overview

### Problem Statement

Large language models are sensitive to prompt quality. A poorly structured prompt produces mediocre output even from a capable model. Most users lack the expertise to write rich, chain-of-thought-laden, context-rich prompts on demand.

### Solution

OwnPromptEnhancer (OPE) is a lightweight **SLM enhancement layer** that intercepts raw user prompts and rewrites them before forwarding to the target LLM. Enhancement strategies include:

1. **CoT Injection** — adds chain-of-thought scaffolding
2. **Structure Formatting** — converts vague sentences into `Goal / Context / Constraints` blocks
3. **Context Enrichment** — injects domain vocabulary, expert role framing, and relevant caveats

Enhancement can be powered by:
- **API Pipeline** — uses OpenAI or Anthropic to do the rewrite
- **Local SLM** — uses a fine-tuned ≤7B model (Phi-3-mini / Mistral) via HuggingFace

---

## 2. Functional Requirements

### Core Enhancement
- [ ] `FR-01` Accept a raw text prompt (1–4096 characters)
- [ ] `FR-02` Apply one or more `EnhancementStrategy` to the raw prompt
- [ ] `FR-03` Return the enhanced prompt as a string
- [ ] `FR-04` Support strategies: `cot_injector`, `structure_formatter`, `context_enricher`, `composite` (all three)
- [ ] `FR-05` Enhancement strategies must be composable (apply in sequence)
- [ ] `FR-06` Each strategy must be independently testable with deterministic mocked adapters

### API
- [ ] `FR-07` `POST /v1/enhance` — single prompt enhancement
- [ ] `FR-08` `POST /v1/enhance/batch` — batch enhancement (max 20 prompts per request)
- [ ] `FR-09` `GET /v1/strategies` — list available strategies with descriptions
- [ ] `FR-10` `GET /health` — liveness check returns `{"status": "ok"}`
- [ ] `FR-11` API must return structured errors with `code`, `message`, and `details`

### Adapters
- [ ] `FR-12` OpenAI adapter: configurable model (`gpt-4o-mini` default), temperature 0.3
- [ ] `FR-13` Anthropic adapter: configurable model (`claude-haiku-3` default)
- [ ] `FR-14` Local HuggingFace adapter: loads model from path, runs inference on CPU/GPU
- [ ] `FR-15` Adapter is injected at startup via config; no adapter switching at runtime in v0.1

### Demo UI
- [ ] `FR-16` Two-panel layout: raw input (editable) + enhanced output (read-only)
- [ ] `FR-17` Strategy selector with descriptions
- [ ] `FR-18` Copy-to-clipboard for enhanced output
- [ ] `FR-19` Character counter on input with 4096 limit warning
- [ ] `FR-20` Keyboard shortcut `Cmd+Enter` to trigger enhancement

---

## 3. Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| API latency (API pipeline) | < 3s p95 for single prompt |
| API latency (local SLM, GPU) | < 2s p95 |
| Max input size | 4096 characters |
| Max batch size | 20 prompts |
| Rate limit | 60 req/min per IP |
| Test coverage | ≥ 80% (backend), ≥ 70% (frontend) |
| Python version | 3.11+ |
| Node version | 20+ |

---

## 4. Data Model

### `EnhancementRequest`

```python
class EnhancementRequest(BaseModel):
    text: str                          # 1–4096 chars
    strategy: StrategyID               # "cot_injector" | "structure_formatter" | "context_enricher" | "composite"
    metadata: EnhancementMetadata | None = None

class EnhancementMetadata(BaseModel):
    domain: str | None = None          # e.g. "software engineering", "medicine"
    target_model: str | None = None    # hint for adapter; e.g. "gpt-4o"
    verbosity: int = 2                 # 1 (concise) – 3 (verbose)
```

### `EnhancementResponse`

```python
class EnhancementResponse(BaseModel):
    original: str
    enhanced: str
    strategy_used: StrategyID
    tokens_original: int
    tokens_enhanced: int
    latency_ms: float
```

### `StrategyInfo`

```python
class StrategyInfo(BaseModel):
    id: StrategyID
    name: str
    description: str
    example_before: str
    example_after: str
```

---

## 5. API Design

### `POST /v1/enhance`

**Request:**
```json
{
  "text": "explain transformers",
  "strategy": "composite",
  "metadata": { "domain": "machine learning", "verbosity": 2 }
}
```

**Response (200):**
```json
{
  "original": "explain transformers",
  "enhanced": "You are an expert machine learning engineer...\n\n## Goal\nProvide a thorough explanation of the Transformer architecture...\n\n## Context\n...\n\n## Constraints\n...\n\nLet's think step by step:\n1. ...",
  "strategy_used": "composite",
  "tokens_original": 3,
  "tokens_enhanced": 147,
  "latency_ms": 812.4
}
```

**Errors:**
| HTTP Code | `code` | Condition |
|-----------|--------|-----------|
| 422 | `VALIDATION_ERROR` | `text` empty or missing |
| 400 | `PROMPT_TOO_LONG` | `text` > 4096 chars |
| 400 | `UNKNOWN_STRATEGY` | `strategy` not in registry |
| 429 | `RATE_LIMITED` | > 60 req/min from same IP |
| 502 | `ADAPTER_ERROR` | upstream LLM API failure |

### `POST /v1/enhance/batch`

```json
{
  "prompts": [
    { "text": "summarize this", "strategy": "structure_formatter" },
    { "text": "write python code", "strategy": "cot_injector" }
  ]
}
```

Response: list of `EnhancementResponse` in same order.

---

## 6. Enhancement Strategy Details

### `cot_injector`

Wraps the prompt in a chain-of-thought scaffold:

```
{original_prompt}

Think through this carefully, step by step:
1. First, identify the core question or task.
2. Consider relevant context, constraints, and assumptions.
3. Work through the problem methodically before providing your answer.
```

### `structure_formatter`

Parses the raw prompt intent and emits:

```
## Goal
{extracted_goal}

## Context
{inferred_context}

## Constraints
{implicit_constraints}

## Expected Output Format
{inferred_format}
```

### `context_enricher`

Prepends domain-aware role framing:

```
You are an expert in {domain}. {role_detail}

{original_prompt}

Please draw on deep domain knowledge and provide a precise, thorough response.
```

### `composite`

Applies: `context_enricher` → `structure_formatter` → `cot_injector` in sequence.

---

## 7. Test Plan

### Unit Tests (pytest)

| Test | Input | Expected |
|------|-------|----------|
| CoT injector | `"what is recursion"` | Output contains "step by step" |
| Structure formatter | `"explain REST APIs"` | Output contains `## Goal`, `## Context`, `## Constraints` |
| Context enricher with domain | `text="explain DNS", domain="networking"` | Output contains "You are an expert in networking" |
| Orchestrator chain | `[cot, structure]` mocked | Both strategies called in order |
| Empty input | `""` | Raises `ValueError` |
| Input > 4096 chars | `"a" * 4097` | Raises `PromptTooLongError` |
| OpenAI adapter | Mocked API call | Returns mocked enhanced string |
| Batch endpoint | 3 prompts | Returns 3 responses |
| Batch > 20 prompts | 21 prompts | 400 response |

### Integration Tests (httpx + FastAPI TestClient)

- Full round-trip `POST /v1/enhance` with mocked OpenAI adapter
- `GET /v1/strategies` returns non-empty list
- Rate limit enforcement (mock time, 61 requests)
- Health check endpoint

### Frontend Tests (Vitest + React Testing Library)

- `PromptInput` updates state on typing
- Submit disabled when input empty
- `useEnhancer` hook: loading → success → error states
- Copy button triggers clipboard API

### Edge Cases

- Unicode and emoji in prompt
- Newline-heavy input (code blocks)
- Non-ASCII languages (Japanese, Arabic)
- Prompt that is already well-structured (should still pass through, enriched)
- Adapter timeout (mock 30s timeout → 502 returned to user in < 5s)

---

## 8. Open Questions

- [ ] **Q1:** Should composite strategy be configurable (order of strategies selectable by user)?
- [ ] **Q2:** Rate limit scope — per IP or per API key (for future auth)?
- [ ] **Q3:** Should enhanced prompt be streamed back character-by-character via SSE (better UX)?
- [ ] **Q4:** Fine-tuned local model vs. few-shot API rewriting — which gives better CoT quality? (needs eval data)
- [ ] **Q5:** Should OPE store enhancement history for a feedback flywheel (thumbs up/down → future fine-tune)?
