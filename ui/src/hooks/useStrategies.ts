import { useQuery } from "@tanstack/react-query";
import type { StrategyInfo } from "../types/api";

const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function fetchStrategies(): Promise<StrategyInfo[]> {
  const res = await fetch(`${API_BASE}/v1/strategies`);
  if (!res.ok) throw new Error("Failed to fetch strategies");
  return res.json() as Promise<StrategyInfo[]>;
}

export function useStrategies() {
  return useQuery<StrategyInfo[], Error>({
    queryKey: ["strategies"],
    queryFn: fetchStrategies,
    staleTime: Infinity,
  });
}
