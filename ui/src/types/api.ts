/* OwnPromptEnhancer UI Types — mirror src/models/prompt.py */

export type StrategyID =
  | "cot_injector"
  | "structure_formatter"
  | "context_enricher"
  | "composite";

export interface EnhancementMetadata {
  domain?: string;
  target_model?: string;
  verbosity?: 1 | 2 | 3;
}

export interface EnhancementRequest {
  text: string;
  strategy: StrategyID;
  metadata?: EnhancementMetadata;
}

export interface EnhancementResponse {
  original: string;
  enhanced: string;
  strategy_used: StrategyID;
  tokens_original: number;
  tokens_enhanced: number;
  latency_ms: number;
}

export interface StrategyInfo {
  id: StrategyID;
  name: string;
  description: string;
  example_before: string;
  example_after: string;
}

export interface ErrorResponse {
  code: string;
  message: string;
  details?: Record<string, unknown>;
}
