"""Session-level semantic labels for DL (task, outcome, export eligibility)."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, computed_field

Outcome = Literal["success", "failure", "abandoned", "unknown"]

UNLABELED_SENTINEL = "(unlabeled session)"


class SessionMeta(BaseModel):
    """Persisted on session document — disjoint from E1 `SessionData._taint` (see `.claude/contracts/taint-vs-session-meta.md`)."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    task_description: str = Field(min_length=10, max_length=500)
    task_tags: list[str] = Field(default_factory=list)
    outcome: Outcome = "unknown"
    outcome_notes: str | None = None
    redaction_failed_any: bool = False

    @computed_field
    @property
    def dataset_eligible(self) -> bool:
        if self.redaction_failed_any:
            return False
        if self.task_description == UNLABELED_SENTINEL:
            return False
        return True
