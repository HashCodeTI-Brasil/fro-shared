from __future__ import annotations

import pytest
from pydantic import ValidationError

from fro_shared.events_v2 import (
    BBox01,
    ElementGrounding,
    ElementRole,
    EventEnvelope,
    EventPayload,
    EventType,
    PlatformSupport,
)


def _grounding() -> ElementGrounding:
    return ElementGrounding(
        role=ElementRole.button,
        label="OK",
        ax_path=["window", "dialog", "OK"],
        stable_id="s1",
        bbox_window_norm=BBox01(x0=0.4, y0=0.4, x1=0.5, y1=0.5),
    )


def test_event_type_rejects_arbitrary_string() -> None:
    with pytest.raises(ValidationError):
        EventEnvelope.model_validate(
            {
                "event_type": "lol",
                "payload": {},
            }
        )


def test_click_without_element_grounding_fails() -> None:
    with pytest.raises(ValidationError):
        EventEnvelope(
            event_type=EventType.click,
            payload=EventPayload(),
        )


def test_click_with_grounding_ok() -> None:
    env = EventEnvelope(
        event_type=EventType.click,
        payload=EventPayload(element_grounding=_grounding()),
    )
    assert env.schema_version == 2


def test_session_start_does_not_require_click_grounding() -> None:
    env = EventEnvelope(
        event_type=EventType.session_start,
        payload=EventPayload(meta={"task_description": "x" * 15}),
    )
    assert env.event_type == EventType.session_start


def test_spatial_event_may_set_norm_coords() -> None:
    env = EventEnvelope(
        event_type=EventType.click,
        payload=EventPayload(
            element_grounding=_grounding(),
            x=100.0,
            y=200.0,
            x_norm=0.2,
            y_norm=0.3,
        ),
    )
    assert env.payload.x_norm == 0.2


def test_platform_support_partial() -> None:
    p = EventPayload(
        element_grounding=_grounding(),
        platform_support=PlatformSupport.partial,
    )
    assert p.platform_support == PlatformSupport.partial
