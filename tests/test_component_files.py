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
REPO_DIR = COMPONENT_DIR.parents[1]


class ComponentFilesTest(unittest.TestCase):
    """Verify packaging and domain isolation without importing Home Assistant."""

    def test_manifest_identifies_custom_integration(self) -> None:
        """Manifest should expose the independent HACS domain and dependency."""
        manifest = json.loads((COMPONENT_DIR / "manifest.json").read_text("utf-8"))

        self.assertEqual("swe_verisure", manifest["domain"])
        self.assertEqual("Swe Verisure", manifest["name"])
        self.assertEqual("0.3.0", manifest["version"])
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

    def test_event_polling_contract(self) -> None:
        """Security and activity records should share the coordinator poll."""
        coordinator = (COMPONENT_DIR / "coordinator.py").read_text("utf-8")
        component = (COMPONENT_DIR / "__init__.py").read_text("utf-8")
        event = (COMPONENT_DIR / "event.py").read_text("utf-8")

        self.assertIn('"INTRUSION"', coordinator)
        self.assertIn('"FIRE"', coordinator)
        self.assertIn('"activity_events"', coordinator)
        self.assertIn('"security_events"', coordinator)
        self.assertIn("Platform.EVENT", component)
        self.assertIn("_trigger_event(event_type", event)

    def test_additional_graphql_features_are_exposed(self) -> None:
        """Metadata and opt-in tracking should have matching HA platforms."""
        coordinator = (COMPONENT_DIR / "coordinator.py").read_text("utf-8")
        component = (COMPONENT_DIR / "__init__.py").read_text("utf-8")

        for query in (
            "firmware",
            "is_guardian_activated",
            "remaining_sms",
            "user_trackings",
        ):
            self.assertIn(f"self.verisure.{query}()", coordinator)
        self.assertIn("Platform.DEVICE_TRACKER", component)
        self.assertIn("Platform.UPDATE", component)

    def test_tracking_is_opt_in_and_redacted(self) -> None:
        """Location tracking should default off and stay out of diagnostics."""
        constants = (COMPONENT_DIR / "const.py").read_text("utf-8")
        coordinator = (COMPONENT_DIR / "coordinator.py").read_text("utf-8")
        tracker = (COMPONENT_DIR / "device_tracker.py").read_text("utf-8")
        diagnostics = (COMPONENT_DIR / "diagnostics.py").read_text("utf-8")

        self.assertIn('CONF_USER_TRACKING = "user_tracking"', constants)
        self.assertIn("entry.options.get(CONF_USER_TRACKING, False)", coordinator)
        self.assertIn("_attr_entity_registry_enabled_default = False", tracker)
        for key in ("currentLocationName", "deviceId", "webAccount"):
            self.assertIn(f'"{key}"', diagnostics)

    def test_rate_limits_are_caught_before_login_errors(self) -> None:
        """Rate-limit subclasses must not be treated as expired credentials."""

        def exception_names(node: ast.expr | None) -> set[str]:
            if isinstance(node, ast.Name):
                return {node.id}
            if isinstance(node, ast.Tuple):
                return {
                    name
                    for item in node.elts
                    for name in exception_names(item)
                }
            return set()

        for filename in ("config_flow.py", "coordinator.py"):
            tree = ast.parse((COMPONENT_DIR / filename).read_text("utf-8"))
            for try_node in (node for node in ast.walk(tree) if isinstance(node, ast.Try)):
                handlers = [exception_names(handler.type) for handler in try_node.handlers]
                rate_indexes = [
                    index
                    for index, names in enumerate(handlers)
                    if "VerisureRateLimitError" in names
                ]
                login_indexes = [
                    index
                    for index, names in enumerate(handlers)
                    if "VerisureLoginError" in names
                ]
                if rate_indexes and login_indexes:
                    self.assertLess(rate_indexes[0], login_indexes[0], filename)

    def test_public_documentation_covers_extended_features(self) -> None:
        """Public guides and changelog should cover the integration surfaces."""
        documents = {
            "configuration": REPO_DIR / "docs" / "configuration.md",
            "entities": REPO_DIR / "docs" / "entities.md",
            "automations": REPO_DIR / "docs" / "automations.md",
            "operations": REPO_DIR / "docs" / "operations.md",
            "changelog": REPO_DIR / "CHANGELOG.md",
        }
        for name, path in documents.items():
            with self.subTest(document=name):
                self.assertTrue(path.is_file())

        self.assertIn("user location tracking", documents["configuration"].read_text("utf-8"))
        entities = documents["entities"].read_text("utf-8")
        for event_type in ("intrusion", "fire", "sos", "water", "technical"):
            self.assertIn(f"`{event_type}`", entities)
        self.assertIn("event.example_security_alarm", documents["automations"].read_text("utf-8"))
        operations = documents["operations"].read_text("utf-8")
        self.assertIn("AUT_00021", operations)
        self.assertIn("Guardian SOS", operations)
        self.assertIn("## Unreleased", documents["changelog"].read_text("utf-8"))

    def test_poll_interval_option_is_bounded(self) -> None:
        """The polling interval should be configurable with finite bounds."""
        config_flow = (COMPONENT_DIR / "config_flow.py").read_text("utf-8")
        coordinator = (COMPONENT_DIR / "coordinator.py").read_text("utf-8")

        self.assertIn("CONF_SCAN_INTERVAL", config_flow)
        self.assertIn("MIN_SCAN_INTERVAL_SECONDS", config_flow)
        self.assertIn("MAX_SCAN_INTERVAL_SECONDS", config_flow)
        self.assertIn("CONF_SCAN_INTERVAL", coordinator)


if __name__ == "__main__":
    unittest.main()
