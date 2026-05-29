# Benchmark Dataset

Prompt pairs used for evaluating the OwnPromptEnhancer pipeline.

## Format

Each line is a JSON object:

```json
{
  "id": "bp-001",
  "raw": "explain transformers",
  "gold_enhanced": "You are an expert in machine learning...",
  "domain": "machine learning",
  "difficulty": "easy"
}
```

## Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique ID, format `bp-NNN` |
| `raw` | string | Original raw prompt |
| `gold_enhanced` | string | Human-written ideal enhanced prompt |
| `domain` | string | Subject domain |
| `difficulty` | `easy` \| `medium` \| `hard` | Subjective difficulty of the raw prompt |

## Usage

```bash
python scripts/eval.py --adapter openai --strategy composite --benchmark data/benchmark_prompts.jsonl --output results.csv
```

The eval script computes per-row metrics (token delta, CoT presence, section count, Flesch score) and prints a summary.
