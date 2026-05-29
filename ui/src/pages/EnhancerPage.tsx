import React, { useState, useCallback } from "react";
import { useEnhancer } from "../hooks/useEnhancer";
import type { StrategyID } from "../types/api";

const MAX_LENGTH = 4096;

export const EnhancerPage: React.FC = () => {
  const [text, setText] = useState("");
  const [strategy, setStrategy] = useState<StrategyID>("composite");
  const { mutate, data, isPending, error } = useEnhancer();

  const handleSubmit = useCallback(() => {
    if (!text.trim()) return;
    mutate({ text, strategy });
  }, [text, strategy, mutate]);

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "Enter") handleSubmit();
    },
    [handleSubmit]
  );

  return (
    <div className="enhancer-page">
      <h1>OwnPromptEnhancer</h1>
      <div className="panels">
        {/* Input panel */}
        <div className="panel">
          <label htmlFor="raw-input">Raw Prompt</label>
          <textarea
            id="raw-input"
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={handleKeyDown}
            maxLength={MAX_LENGTH}
            placeholder="Type your prompt here…"
            rows={12}
          />
          <span className={text.length > MAX_LENGTH * 0.9 ? "warn" : ""}>
            {text.length} / {MAX_LENGTH}
          </span>
          <select value={strategy} onChange={(e) => setStrategy(e.target.value as StrategyID)}>
            <option value="composite">Composite (all strategies)</option>
            <option value="cot_injector">CoT Injector</option>
            <option value="structure_formatter">Structure Formatter</option>
            <option value="context_enricher">Context Enricher</option>
          </select>
          <button onClick={handleSubmit} disabled={isPending || !text.trim()}>
            {isPending ? "Enhancing…" : "Enhance (⌘↵)"}
          </button>
        </div>

        {/* Output panel */}
        <div className="panel">
          <label>Enhanced Prompt</label>
          <textarea readOnly value={data?.enhanced ?? ""} rows={12} placeholder="Enhanced output appears here…" />
          {data && (
            <button
              onClick={() => navigator.clipboard.writeText(data.enhanced)}
            >
              Copy to clipboard
            </button>
          )}
          {data && (
            <small>
              {data.tokens_original} → {data.tokens_enhanced} tokens · {data.latency_ms.toFixed(0)}ms
            </small>
          )}
          {error && <p className="error">{error.message}</p>}
        </div>
      </div>
    </div>
  );
};
