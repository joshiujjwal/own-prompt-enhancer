import { useMutation } from "@tanstack/react-query";
import type { EnhancementRequest, EnhancementResponse } from "../types/api";

const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function enhancePrompt(req: EnhancementRequest): Promise<EnhancementResponse> {
  const res = await fetch(`${API_BASE}/v1/enhance`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ message: res.statusText }));
    throw new Error(err.message ?? "Enhancement failed");
  }
  return res.json() as Promise<EnhancementResponse>;
}

export function useEnhancer() {
  return useMutation<EnhancementResponse, Error, EnhancementRequest>({
    mutationFn: enhancePrompt,
  });
}
