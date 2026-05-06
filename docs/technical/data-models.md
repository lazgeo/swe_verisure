# Data models

Located under [`custom_components/my_verisure/core/api/models/`](../../custom_components/my_verisure/core/api/models/).

## Layers

- **`dto/`** — Serialized shapes close to API payloads.  
- **`domain/`** — Richer domain objects used internally.

DTO parsing tolerances vary — some entities still read raw dict trees for speed (technical debt noted in [roadmap](../roadmap/gaps-analysis.md)).
