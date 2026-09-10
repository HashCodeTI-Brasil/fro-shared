<!-- @agent-touched: 2026-09-10 -->
# FRO shared schemas — contrato de treino (Wave 0)

## Envelope de evento v2

- `schema_version: 2` e `event_type: EventType` (enum fechado — sem `other`).
- **Não** é usado para payloads HTTP de webhook: `webhook_listen`/`webhook_wait` são *mecanismos de passo* do `fro-backend`; o payload recebido vai para `sessionData` (marcado *tainted*), não para `events/` como envelope v2. O contrato desse fluxo está no `fro-backend` (`webhook_gateway/`, `services/webhook_*`).
- Cliques (`click`, `right_click`, `double_click`) **exigem** `payload.element_grounding`.
- Eventos espaciais carregam pixel (`x`, `y`) e normalizado à janela (`x_norm`, `y_norm` em [0,1]) quando aplicável.

## SessionMeta

- `task_description` entre 10 e 500 caracteres; `(unlabeled session)` é o sentinela do caminho sem rótulo.
- `dataset_eligible` é derivado: não é sem rótulo e não teve `redaction_failed_any`.

## Export (referência futura — Wave 9)

Trajetórias JSONL usam passos de UI com estado + ação + grounding; capturas de webhook não são passos primários.
