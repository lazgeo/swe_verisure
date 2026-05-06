# GraphQL API

**Endpoint:** `https://customers.securitasdirect.es/owa-api/graphql` (`VERISURE_GRAPHQL_URL`).

## Transport

[`BaseClient`](../../custom_components/my_verisure/core/api/base_client.py) issues POST requests with JSON payloads `{ "query": ..., "variables": ... }` via **aiohttp**.

## Headers

Includes synthetic native-app headers (`App`, `Extension`) plus serialized **`auth`** JSON (`loginTimestamp`, user id, country `ES`, hash token, …).

## Queries / mutations

Concrete GraphQL documents reside beside each specialized client (`AuthClient`, `AlarmClient`, …). Treat them as **private contracts** — upstream may change field names without notice.

## Errors

HTTP/API failures normalize into `MyVerisure*` exceptions ([exceptions.py](../../custom_components/my_verisure/core/api/exceptions.py)).
