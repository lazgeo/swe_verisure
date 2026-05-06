"""Smoke tests that require Home Assistant to be importable."""

from __future__ import annotations

import pytest

pytest.importorskip("homeassistant")


def test_diagnostics_exports_config_entry_helper() -> None:
    """Diagnostics module should expose the standard async helper."""
    from custom_components.my_verisure import diagnostics as diag

    assert hasattr(diag, "async_get_config_entry_diagnostics")
