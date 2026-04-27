from __future__ import annotations

import pytest
from pydantic import ValidationError

from fro_shared.session_meta import UNLABELED_SENTINEL, SessionMeta


def test_task_description_too_short() -> None:
    with pytest.raises(ValidationError):
        SessionMeta(task_description="short")


def test_dataset_eligible_true_when_labeled() -> None:
    m = SessionMeta(task_description="x" * 15)
    assert m.dataset_eligible is True


def test_dataset_eligible_false_for_unlabeled_sentinel() -> None:
    m = SessionMeta(task_description=UNLABELED_SENTINEL)
    assert m.dataset_eligible is False


def test_dataset_eligible_false_when_redaction_failed() -> None:
    m = SessionMeta(task_description="x" * 15, redaction_failed_any=True)
    assert m.dataset_eligible is False


def test_session_meta_disjoint_from_taint_key() -> None:
    """Contract: Firestore doc can carry `meta` + a sibling `_taint` without collision."""
    m = SessionMeta(task_description="x" * 15)
    d = m.model_dump()
    d["_taint"] = {"shell_command": "user"}
    assert "task_description" in m.model_dump()
    assert "_taint" in d
    assert m.model_dump().get("_taint") is None
