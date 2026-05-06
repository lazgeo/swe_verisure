# API clients (GraphQL)

All HTTP traffic uses **`aiohttp`** asynchronous sessions inside client classes derived from [`BaseClient`](../../custom_components/my_verisure/core/api/base_client.py).

## Endpoint

Configured in [`core/const.py`](../../custom_components/my_verisure/core/const.py):

`VERISURE_GRAPHQL_URL = https://customers.securitasdirect.es/owa-api/graphql`

(`fields.py` may re-export — verify imports in clients.)

## Headers / auth

`BaseClient` builds:

- JSON content type  
- Custom **App / Extension** headers mimicking native app metadata  
- **`auth` header** JSON payload including `hash` token from `SessionManager`

## Clients

| Client | Responsibility |
|--------|----------------|
| `AuthClient` | Login, OTP, session lifecycle |
| `InstallationClient` | Installations, services |
| `AlarmClient` | Alarm status, arm/disarm mutations |
| `CameraClient` | Camera refresh / image retrieval |

Exact GraphQL strings live alongside each client implementation — treat them as **vendor-private** and subject to change.

## Errors

Raised as `MyVerisure*` exceptions from [`api/exceptions.py`](../../custom_components/my_verisure/core/api/exceptions.py); coordinators translate them into HA exceptions.
