"""Shared contracts: EventEnvelope v2, SessionMeta (DL training)."""

from fro_shared.events_v2 import (
    BBox01,
    ElementGrounding,
    ElementRole,
    EventEnvelope,
    EventPayload,
    EventType,
    PlatformSupport,
    unresolved_element_grounding,
)
from fro_shared.session_meta import SessionMeta

__all__ = [
    "BBox01",
    "ElementGrounding",
    "ElementRole",
    "EventEnvelope",
    "EventPayload",
    "EventType",
    "PlatformSupport",
    "SessionMeta",
    "unresolved_element_grounding",
]
