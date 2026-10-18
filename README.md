# SupportFlow AI Service â€” contract foundation

This repository contains the pinned v1 classification contract and offline fixtures.
No AI server, provider connection or business write access is implemented in this phase.

The canonical contract is owned by `supportflow-ai/ai-it-service-desk`.
Update this copy only by importing a released backend contract and updating
`contract.lock.json`; CI verifies both the checksum and upstream bytes.

```sh
python -m pip install -r contracts/requirements.txt
python scripts/validate_ai_contract.py
```

Backend owns authorization, ticket transitions, priority, confidence bands and human
review decisions. AI receives only an authorized snapshot and returns suggestions.
It must not receive database credentials or end-user JWTs and cannot modify business data.
See the backend ADR for service authentication and resilience defaults before implementing
the real service. Contract v1 has no implied running endpoint.
