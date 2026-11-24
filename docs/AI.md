# TubePilot AI — Modular AI Strategy & Model Guide

TubePilot AI treats AI as an **optional interpretation and ideation layer**.
**Deterministic statistical engines calculate all scores; LLMs never hallucinate numerical data.**

---

## 1. Zero Paid API Mandate
TubePilot AI does not mandate subscriptions to OpenAI, Gemini, Anthropic, or OpenRouter. The entire suite of keyword research, competition calculation, opportunity ranking, video audit, channel health, and content gaps functions without AI.

---

## 2. Local AI Architecture (Hostinger KVM 4 Target)

```
[ Research Data + Heuristics ]
              │
              ▼
   [ AI Provider Interface ]
              │
    ┌─────────┴─────────┐
    ▼                   ▼
[ Disabled ]     [ Local Ollama ]
(Pure Heuristics)(Qwen 2.5 0.5B / 4B CPU)
```

Hostinger KVM 4 has 4 vCPUs and 16 GB RAM with no dedicated GPU. Therefore, models must be:
- **Quantized**: Q4_K_M or Q5_K_M.
- **Lightweight Parameter Class**: 0.5B to 4B parameters.
- **Fast CPU Context Processing**: Avoid heavy KV caches.

### Recommended Model Benchmarks on 4 vCPU:

| Model | Parameters | Quantization | RAM Usage | Tokens/Sec (CPU) | Recommendation |
|---|---|---|---|---|---|
| **Qwen 2.5 0.5B Instruct** | 0.49B | Q4_K_M | ~650 MB | 35–50 tok/s | **Primary Choice for Speed & Minimal Footprint** |
| **Qwen 2.5 1.5B Instruct** | 1.54B | Q4_K_M | ~1.4 GB | 18–28 tok/s | Balanced quality and low latency |
| **Qwen 2.5 3B / 4B Instruct** | ~3.8B | Q4_K_M | ~3.2 GB | 8–14 tok/s | Higher creativity for title hooks |
| **Gemma 2 / 3 2B** | 2.6B | Q4_K_M | ~2.1 GB | 12–18 tok/s | Alternative clean instruction following |

---

## 3. Graceful Fallback Behavior

When `AI_ENABLED=false` or when the local Ollama instance is unreachable:
1. The web UI displays an informational badge: `AI: Deterministic Heuristics Mode`.
2. The AI Studio automatically falls back to deterministic heuristic templates:
   - 14 psychological title templates (How-To, Contrarian, Numbered List, Case Study).
   - Structured description generators with chapters and CTA blocks.
   - 3-tier video hook formulas (First 3s, Next 15s, Open loop).
   - 7/30/60/90-day content calendar matrices.
3. No exceptions or crashes occur.
