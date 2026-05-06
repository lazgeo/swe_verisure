# Authentication

Flow outline:

1. **Username/password** submitted via config flow.  
2. `AuthUseCase.login` obtains tokens via GraphQL.  
3. **OTP path** — vendor raises OTP requirement → phone selection → OTP verification storing refreshed tokens in session manager.  
4. Subsequent calls attach hash token inside HTTP headers.

See diagrams [authentication-flow.md](../architecture/diagrams/authentication-flow.md).

## Failure modes

- Invalid credentials → `MyVerisureAuthenticationError`.  
- OTP mismatch → `MyVerisureOTPError`.  
- Vendor temporary lockouts → `MyVerisureServiceBlockedError`.
