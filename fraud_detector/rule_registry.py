from __future__ import annotations

from importlib import import_module
import os
from typing import Callable, Dict, Any, Iterator, List, Tuple, Sequence

Rule = Callable[[Dict[str, Any], Dict[str, Any]], bool]
RuleEntry = Tuple[str, Rule]


class RuleRegistry:
    """Registry for fraud detection rules."""

    def __init__(self) -> None:
        self._rules: List[RuleEntry] = []

    def register(self, name: str | None = None) -> Callable[[Rule], Rule]:
        """Decorator to register a rule function.

        Parameters
        ----------
        name: optional explicit rule name. Defaults to the function's ``__name__``.
        """

        def decorator(func: Rule) -> Rule:
            rule_name = name or func.__name__
            self._rules.append((rule_name, func))
            return func

        return decorator

    def __iter__(self) -> Iterator[RuleEntry]:  # pragma: no cover - simple iteration
        return iter(self._rules)

    def __len__(self) -> int:  # pragma: no cover - trivial
        return len(self._rules)

    def load_modules(self, modules: Sequence[str]) -> None:
        """Import modules that register additional rules."""
        for module in modules:
            import_module(module)

    def load_from_env(self, env_var: str = "FRAUD_RULE_MODULES") -> None:
        """Load rule modules listed in the ``env_var`` environment variable."""
        modules = os.environ.get(env_var)
        if modules:
            self.load_modules([m.strip() for m in modules.split(",") if m.strip()])


rules_registry = RuleRegistry()
