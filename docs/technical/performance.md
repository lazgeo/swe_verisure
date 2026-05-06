# Performance considerations

## Polling load

Default **10-minute** interval balances freshness vs API quota. Lower intervals increase risk of **service blocked** responses — vendor-dependent.

## Command bursts

Rapid sequences of `get_status` + arm/disarm operations increase throttling likelihood.

## Camera refresh

Image refresh walks filesystem and may issue multiple GraphQL operations — avoid chaining refreshes in tight loops.

## Local disk I/O

Coordinator persists JSON snapshots and camera folders — monitor disk usage on memory-constrained HA OS installs.
