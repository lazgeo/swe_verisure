# Current state assessment

## Strengths

- Modern **GraphQL** architecture with layered repositories/use cases.  
- Comprehensive **pytest** coverage around embedded core (`custom_components/my_verisure/core/tests/unit`).  
- **Coordinator** consolidates polling + imperative alarm commands.  
- **Config flow** covers OTP branches + installation selection + options for polling/perimeter behavior.  
- **CI**: HACS validation workflow ([`.github/workflows/validate.yml`](../../.github/workflows/validate.yml)).

## Implementation realities

- Uses `hass.data[DOMAIN]` dict including coordinators plus sentinel keys (`services_setup`) — mixed patterns vs HA recommendations (`runtime_data`).  
- Logging verbosity — frequent **warning** level traces during normal operation.  
- Camera entities rely on **filesystem** snapshots — acceptable but brittle.
