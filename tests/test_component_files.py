"""Static contract tests for the Swe Verisure custom integration."""

from __future__ import annotations

import ast
import json
from pathlib import Path
import runpy
import sys
from types import ModuleType
import unittest
from unittest.mock import patch


COMPONENT_DIR = Path(__file__).parents[1] / "custom_components" / "swe_verisure"


class ComponentFilesTest(unittest.TestCase):
    """Verify packaging and domain isolation without importing Home Assistant."""

    def test_manifest_identifies_custom_integration(self) -> None:
        """Manifest should expose the independent HACS domain and dependency."""
        manifest = json.loads((COMPONENT_DIR / "manifest.json").read_text("utf-8"))

        self.assertEqual("swe_verisure", manifest["domain"])
        self.assertEqual("Swe Verisure", manifest["name"])
        self.assertEqual("0.1.3", manifest["version"])
        self.assertEqual(["vsure==2.9.0"], manifest["requirements"])
        self.assertTrue(manifest["config_flow"])

    def test_python_files_parse(self) -> None:
        """Every shipped Python file should have valid syntax."""
        for path in COMPONENT_DIR.rglob("*.py"):
            with self.subTest(path=path.name):
                ast.parse(path.read_text("utf-8"), filename=str(path))

    def test_component_uses_runtime_data(self) -> None:
        """New integration code should not store coordinators in hass.data."""
        source = "\n".join(
            path.read_text("utf-8")
            for path in COMPONENT_DIR.glob("*.py")
        )

        self.assertNotIn("hass.data", source)
        self.assertIn("entry.runtime_data = coordinator", source)

    def test_service_targets_use_swe_domain(self) -> None:
        """Entity services must target only Swe Verisure entities."""
        services = (COMPONENT_DIR / "services.yaml").read_text("utf-8")

        self.assertEqual(3, services.count("integration: swe_verisure"))
        self.assertNotIn("integration: verisure", services)

    def test_cookie_namespace_is_isolated(self) -> None:
        """Session files must not collide with the built-in integration."""
        coordinator = (COMPONENT_DIR / "coordinator.py").read_text("utf-8")
        config_flow = (COMPONENT_DIR / "config_flow.py").read_text("utf-8")

        self.assertIn('f"swe_verisure_{entry.data[CONF_EMAIL]}"', coordinator)
        self.assertEqual(2, config_flow.count('f"swe_verisure_{user_input[CONF_EMAIL]}"'))

    def test_config_flow_labels_and_descriptions(self) -> None:
        """Config-flow fields should have concrete labels and step hints."""
        for filename in ("strings.json", "translations/en.json", "translations/sv.json"):
            translations = json.loads((COMPONENT_DIR / filename).read_text("utf-8"))
            steps = translations["config"]["step"]

            self.assertNotIn("%key:", json.dumps(steps))
            for step_name in ("user", "reauth_confirm"):
                self.assertEqual({"email", "password"}, set(steps[step_name]["data"]))
                self.assertIn("description", steps[step_name])
            for step_name in ("mfa", "reauth_mfa"):
                self.assertEqual({"code"}, set(steps[step_name]["data"]))
                self.assertIn("description", steps[step_name])

    def test_compatibility_with_preloaded_older_verisure(self) -> None:
        """Optional exception imports must not break config-flow loading."""
        old_verisure = ModuleType("verisure")

        class Error(Exception):
            pass

        class LoginError(Error):
            pass

        class ResponseError(Error):
            pass

        old_verisure.Error = Error
        old_verisure.LoginError = LoginError
        old_verisure.ResponseError = ResponseError
        old_verisure.Session = object

        with patch.dict(sys.modules, {"verisure": old_verisure}):
            namespace = runpy.run_path(COMPONENT_DIR / "verisure_compat.py")

        self.assertIs(namespace["VerisureLoginError"], LoginError)
        self.assertTrue(
            issubclass(namespace["VerisureAuthenticationError"], Exception)
        )

        for filename in ("config_flow.py", "coordinator.py"):
            source = (COMPONENT_DIR / filename).read_text("utf-8")
            self.assertNotIn("from verisure import", source)


if __name__ == "__main__":
    unittest.main()
