"""Built-in fraud detection rules."""
from __future__ import annotations

from typing import Dict, Any

from .rule_registry import rules_registry


@rules_registry.register()
def amount_gt_1000(tx: Dict[str, Any], feats: Dict[str, Any]) -> bool:
    """Flag transactions where the amount exceeds $1000."""
    return tx.get("amount", 0) > 1000


@rules_registry.register()
def velocity_score_high(tx: Dict[str, Any], feats: Dict[str, Any]) -> bool:
    """Flag when the velocity score feature is above 0.8."""
    return feats.get("velocity_score", 0) > 0.8


@rules_registry.register()
def high_risk_country(tx: Dict[str, Any], feats: Dict[str, Any]) -> bool:
    """Flag transactions originating from high risk countries."""
    return bool(feats.get("is_high_risk_country"))
