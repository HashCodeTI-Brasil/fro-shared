# FRO shared schemas — DL training contract (Wave 0)

## Event envelope v2

- `schema_version: 2` and `event_type: EventType` (closed enum — no `other`).
- **Not** used for inbound webhook HTTP payloads; `webhook_listen` / `webhook_wait` are *step mechanisms* in `fro-backend` (see `fro-workspace/.claude/contracts/event-envelope-v2-vs-webhook-payload.md`) — payload goes to `sessionData`, not to `events/` as v2 envelopes.
- Clicks (`click`, `right_click`, `double_click`) **require** `payload.element_grounding`.
- Spatial events carry both pixel (`x`, `y`) and window-normalized (`x_norm`, `y_norm` in [0,1]) where applicable.

## SessionMeta

- `task_description` length 10–500 characters; use `(unlabeled session)` for the default unlabeled path (see migration table in sprint refinamento).
- `dataset_eligible` is derived: not unlabeled, no `redaction_failed_any`.

## Export (forward reference — Wave 9)

JSONL trajectories use UI steps with state+action+grounding; webhook captures are not primary steps (Wave 9 + contract `event-envelope-v2-vs-webhook-payload.md`).
