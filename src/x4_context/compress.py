"""Core context compression strategies."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass
class CompressionResult:
    original_tokens: int
    compressed_tokens: int
    ratio: float
    strategy: str
    kept_keys: list[str]


def compress_tool_output(payload: dict[str, Any], max_tokens: int = 512) -> CompressionResult:
    """Naive but effective: keep schema + summary, drop bulk text."""
    # Placeholder implementation — replace with real tokenizer + policies
    text = str(payload)
    original = len(text) // 4  # rough token estimate
    summary = {k: (v if not isinstance(v, str) or len(v) < 200 else v[:200] + "…") for k, v in payload.items()}
    compressed = len(str(summary)) // 4
    return CompressionResult(
        original_tokens=original,
        compressed_tokens=min(compressed, max_tokens),
        ratio=round(compressed / max(original, 1), 3),
        strategy="schema+truncate",
        kept_keys=list(summary.keys()),
    )
