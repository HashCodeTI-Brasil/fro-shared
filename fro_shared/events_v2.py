"""Event envelope v2 — closed vocabulary for DL training.

`webhook_listen` / `webhook_wait` are Step *mechanisms* (fro-backend), not EventType
values — external webhook payloads never use this envelope.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

# --- Enums (closed) ---


class EventType(StrEnum):
    click = "click"
    right_click = "right_click"
    double_click = "double_click"
    scroll = "scroll"
    key_press = "key_press"
    key_combo = "key_combo"
    typed_text = "typed_text"
    screen_changed = "screen_changed"
    focus_changed = "focus_changed"
    dialog_opened = "dialog_opened"
    dialog_closed = "dialog_closed"
    clipboard_copy = "clipboard_copy"
    clipboard_paste = "clipboard_paste"
    frame_sampling_paused = "frame_sampling_paused"
    frame_sampling_capped = "frame_sampling_capped"
    screen_sampling_unavailable = "screen_sampling_unavailable"
    session_start = "session_start"
    session_end = "session_end"


_CLICK_TYPES: frozenset[EventType] = frozenset(
    {
        EventType.click,
        EventType.right_click,
        EventType.double_click,
    }
)


class ElementRole(StrEnum):
    button = "button"
    text_field = "text_field"
    secure_field = "secure_field"
    link = "link"
    checkbox = "checkbox"
    radio = "radio"
    combobox = "combobox"
    menu_item = "menu_item"
    tab = "tab"
    list_item = "list_item"
    tree_item = "tree_item"
    image = "image"
    text = "text"
    dialog = "dialog"
    window = "window"
    unknown = "unknown"


class PlatformSupport(StrEnum):
    full = "full"
    partial = "partial"
    missing = "missing"


# --- Models ---


class BBox01(BaseModel):
    """Axis-aligned rectangle in [0,1] normalized to window (DL contract)."""

    model_config = ConfigDict(extra="forbid")

    x0: float = Field(ge=0.0, le=1.0)
    y0: float = Field(ge=0.0, le=1.0)
    x1: float = Field(ge=0.0, le=1.0)
    y1: float = Field(ge=0.0, le=1.0)

    @model_validator(mode="after")
    def _order(self) -> BBox01:
        if self.x0 > self.x1 or self.y0 > self.y1:
            raise ValueError("bbox must have x0<=x1 and y0<=y1")
        return self


class ElementGrounding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    role: ElementRole
    label: str | None = None
    ax_path: list[str] = Field(default_factory=list)
    stable_id: str
    bbox_window_norm: BBox01


class EventPayload(BaseModel):
    """Per-event payload. Spatial events should set pixel + normalized coords."""

    model_config = ConfigDict(extra="forbid")

    element_grounding: ElementGrounding | None = None
    platform_support: PlatformSupport = PlatformSupport.full
    x: float | None = None
    y: float | None = None
    x_norm: float | None = Field(default=None, ge=0.0, le=1.0)
    y_norm: float | None = Field(default=None, ge=0.0, le=1.0)
    # session_start / session_end: embed meta in JSON-compatible dict
    meta: dict[str, Any] | None = None
    # session_start: monitor layout (not part of SessionMeta)
    monitors: list[dict[str, Any]] | None = None
    timestamp: str | None = None
    key: str | None = None
    modifiers: list[str] = Field(default_factory=list)
    text: str | None = None
    char_count: int | None = None
    ended_at: str | None = None
    dx: int | None = None
    dy: int | None = None
    button: str | None = None
    button_name: str | None = None
    screenshot_full: str | None = None
    screenshot_crop: str | None = None
    crop_origin_x: int | None = None
    crop_origin_y: int | None = None
    scale: float | None = None
    app_name: str | None = None
    window_title: str | None = None
    element_role_raw: str | None = None
    ocr_text: str | None = None
    ocr_confidence: float | None = None
    ocr_detections: list[dict[str, Any]] | None = None


class EventEnvelope(BaseModel):
    """Single recorded event (v2). Not used for inbound webhook HTTP payloads."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal[2] = 2
    event_type: EventType
    payload: EventPayload

    @model_validator(mode="after")
    def _click_needs_grounding(self) -> EventEnvelope:
        if self.event_type in _CLICK_TYPES:
            if self.payload.element_grounding is None:
                raise ValueError(
                    f"element_grounding is required for event_type={self.event_type!s}"
                )
        return self


def unresolved_element_grounding() -> ElementGrounding:
    """Minimal grounding when the platform cannot resolve the element (partial support)."""

    return ElementGrounding(
        role=ElementRole.unknown,
        label=None,
        ax_path=[],
        stable_id="unresolved",
        bbox_window_norm=BBox01(x0=0.0, y0=0.0, x1=0.0, y1=0.0),
    )


__all__ = [
    "BBox01",
    "ElementGrounding",
    "ElementRole",
    "EventEnvelope",
    "EventPayload",
    "EventType",
    "PlatformSupport",
    "unresolved_element_grounding",
]
