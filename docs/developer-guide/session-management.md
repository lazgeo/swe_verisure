# Session management

Session state is centralized in [`session_manager.py`](../../custom_components/my_verisure/core/session_manager.py) (singleton accessor `get_session_manager()`).

## Responsibilities

- Store username/password/hash/refresh tokens  
- Persist JSON under HA storage paths (see coordinator — `my_verisure_{user}.json`)  
- Validate/expiry checks (`is_session_valid`, `ensure_authenticated`)  

## Interaction flow

1. Config flow login sets credentials on session manager.  
2. GraphQL clients pull tokens via `_get_current_credentials`.  
3. Coordinator calls `ensure_authenticated` / login flows when polling.

For security guidance — treat session files as **secrets**; restrict backups accordingly.

See also [session-persistence.md](../technical/session-persistence.md).
