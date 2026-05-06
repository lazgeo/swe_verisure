# Overview

My Verisure is a **cloud-polled hub integration**. Home Assistant entities reflect remote alarm state; commands round-trip through Securitas GraphQL.

```mermaid
flowchart TB
  subgraph ha [Home Assistant]
    UI[Dashboards and automations]
    Ent[Entities]
    Svc[Services]
    Coord[Coordinator]
  end
  subgraph core [Integration core]
    UC[Use cases]
    Rep[Repositories]
    Cli[GraphQL clients]
  end
  Cloud[(Securitas GraphQL)]

  UI --> Ent
  UI --> Svc
  Ent --> Coord
  Svc --> Coord
  Coord --> UC
  UC --> Rep
  Rep --> Cli
  Cli --> Cloud
```

**Integration types:** `integration_type: hub` in [`manifest.json`](../../custom_components/my_verisure/manifest.json).  
**IoT class:** `cloud_polling`.
