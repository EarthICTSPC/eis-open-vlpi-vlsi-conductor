"""Shape derivation for a pinned Qwen3 configuration.

This is configuration arithmetic, not a model loader and not a physical
hardware model. Projection weights use [out_features, in_features].
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Qwen3Shape:
    hidden_size: int
    num_attention_heads: int
    num_key_value_heads: int
    head_dim: int
    num_hidden_layers: int
    intermediate_size: int
    vocab_size: int
    max_position_embeddings: int

    @classmethod
    def from_mapping(cls, cfg: dict[str, Any]) -> "Qwen3Shape":
        required = (
            "hidden_size", "num_attention_heads", "num_key_value_heads",
            "num_hidden_layers", "intermediate_size", "vocab_size",
            "max_position_embeddings",
        )
        missing = [key for key in required if key not in cfg]
        if missing:
            raise ValueError(f"missing config keys: {', '.join(missing)}")
        heads = int(cfg["num_attention_heads"])
        head_dim = int(cfg.get("head_dim", int(cfg["hidden_size"]) // heads))
        result = cls(
            hidden_size=int(cfg["hidden_size"]),
            num_attention_heads=heads,
            num_key_value_heads=int(cfg["num_key_value_heads"]),
            head_dim=head_dim,
            num_hidden_layers=int(cfg["num_hidden_layers"]),
            intermediate_size=int(cfg["intermediate_size"]),
            vocab_size=int(cfg["vocab_size"]),
            max_position_embeddings=int(cfg["max_position_embeddings"]),
        )
        result.validate()
        return result

    @classmethod
    def from_json(cls, path: str | Path) -> "Qwen3Shape":
        return cls.from_mapping(json.loads(Path(path).read_text(encoding="utf-8")))

    def validate(self) -> None:
        if self.hidden_size != self.num_attention_heads * self.head_dim:
            raise ValueError("hidden_size must equal query_heads * head_dim")
        if self.num_key_value_heads <= 0:
            raise ValueError("num_key_value_heads must be positive")
        if self.num_attention_heads % self.num_key_value_heads:
            raise ValueError("query heads must be divisible by KV heads")
        if min(self.num_hidden_layers, self.intermediate_size, self.vocab_size) <= 0:
            raise ValueError("layer, intermediate and vocabulary dimensions must be positive")

    @property
    def queries_per_kv_head(self) -> int:
        return self.num_attention_heads // self.num_key_value_heads

    @property
    def q_projection_weight_shape(self) -> tuple[int, int]:
        return (self.num_attention_heads * self.head_dim, self.hidden_size)

    @property
    def k_projection_weight_shape(self) -> tuple[int, int]:
        return (self.num_key_value_heads * self.head_dim, self.hidden_size)

    @property
    def v_projection_weight_shape(self) -> tuple[int, int]:
        return (self.num_key_value_heads * self.head_dim, self.hidden_size)

    @property
    def o_projection_weight_shape(self) -> tuple[int, int]:
        return (self.hidden_size, self.num_attention_heads * self.head_dim)

    def kv_head_for_query_head(self, query_head: int) -> int:
        if not 0 <= query_head < self.num_attention_heads:
            raise ValueError("query_head out of range")
        return query_head // self.queries_per_kv_head

    def tensor_shapes(self, batch: int, sequence: int) -> dict[str, tuple[int, ...]]:
        if batch <= 0 or sequence <= 0:
            raise ValueError("batch and sequence must be positive")
        return {
            "hidden": (batch, sequence, self.hidden_size),
            "q": (batch, self.num_attention_heads, sequence, self.head_dim),
            "k": (batch, self.num_key_value_heads, sequence, self.head_dim),
            "v": (batch, self.num_key_value_heads, sequence, self.head_dim),
            "attention_scores": (
                batch, self.num_attention_heads, sequence, sequence
            ),
            "attention_output": (
                batch, self.num_attention_heads, sequence, self.head_dim
            ),
        }

    def tile_ledger(self, query_tile: int = 64, key_tile: int = 64) -> dict[str, int]:
        if query_tile <= 0 or key_tile <= 0:
            raise ValueError("tile dimensions must be positive")
        scores_per_head = query_tile * key_tile
        scores_all_heads = self.num_attention_heads * scores_per_head
        scalar_pair_terms = scores_all_heads * self.head_dim
        return {
            "query_tile": query_tile,
            "key_tile": key_tile,
            "scores_per_head": scores_per_head,
            "scores_all_query_heads": scores_all_heads,
            "qk_scalar_pair_terms": scalar_pair_terms,
            "av_scalar_pair_terms": scalar_pair_terms,
            "kv_cache_elements_per_token_per_layer": (
                2 * self.num_key_value_heads * self.head_dim
            ),
        }


def load_pinned_config() -> Qwen3Shape:
    root = Path(__file__).resolve().parents[1]
    return Qwen3Shape.from_json(root / "models/qwen3-8b/config.json")
