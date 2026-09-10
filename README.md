<!-- @agent-touched: 2026-09-10 -->
# fro-shared

Contratos Python compartilhados da plataforma FRO. Versão `0.1.2`. Consumido **por tag git**, não pelo PyPI:

```
fro-shared @ git+https://github.com/HashCodeTI-Brasil/fro-shared.git@v0.1.2
```

## Conteúdo

| Módulo | O que define | Quem usa |
|---|---|---|
| `fro_shared/events_v2.py` | `EventEnvelope`, `EventPayload` (`extra="forbid"`), `EventType`, `ElementGrounding`, `ElementRole`, `PlatformSupport`, `FocusInfo`, `BBox01`, `unresolved_element_grounding()` — o formato dos eventos gravados (JSONL) | `fro-agent` (gravação e upload em fluxo); o `fro-backend` grava os envelopes como recebe |
| `fro_shared/session_meta.py` | `SessionMeta` (`task_description` 10–500 chars, `UNLABELED_SENTINEL`, `dataset_eligible` derivado) | `fro-agent` e `fro-backend` |

O contrato do **robô** (mecanismos, condições, passos) **não** está aqui: vive em `fro-backend/fro_backend/schemas/work.py` e é copiado à mão no Studio e no agente.

## Versionar

1. Ajuste `version` em `pyproject.toml`.
2. `git tag vX.Y.Z && git push origin vX.Y.Z`.
3. Atualize o pin nos consumidores (`fro-agent/pyproject.toml`, `fro-backend/pyproject.toml`).

Como `EventPayload` recusa campo desconhecido, qualquer campo novo no evento exige um release aqui antes de chegar ao agente. Tags são mutáveis: nunca mova uma tag já consumida.

## Testes

```
pip install -e '.[dev]'
pytest
```
