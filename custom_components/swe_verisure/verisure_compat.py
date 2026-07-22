"""Compatibility imports for Verisure library versions loaded by Home Assistant."""

from __future__ import annotations

import verisure


class _UnavailableVerisureError(Exception):
    """Placeholder for exceptions absent from older Verisure releases."""


# Home Assistant's built-in Verisure integration can preload an older vsure
# module before this custom integration's requirement is installed. Resolve the
# newer exception types without making config-flow import fail in that process.
VerisureAuthenticationError = getattr(
    verisure, "AuthenticationError", _UnavailableVerisureError
)
VerisureCookieReadError = getattr(
    verisure, "CookieReadError", _UnavailableVerisureError
)
VerisureRateLimitError = getattr(
    verisure, "RateLimitError", _UnavailableVerisureError
)
VerisureRequestError = getattr(
    verisure, "RequestError", _UnavailableVerisureError
)
VerisureError = verisure.Error
VerisureLoginError = verisure.LoginError
VerisureResponseError = verisure.ResponseError
Verisure = verisure.Session
