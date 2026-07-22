"""DataUpdateCoordinator for the Swe Verisure integration."""

from datetime import datetime, timedelta
from time import sleep
from typing import Any, override

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.storage import STORAGE_DIR
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import Throttle, dt as dt_util

from .const import (
    CONF_GIID,
    CONF_USER_TRACKING,
    COOKIE_REFRESH_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    LOGGER,
    METADATA_REFRESH_INTERVAL,
    RATE_LIMIT_BACKOFF,
)
from .verisure_compat import (
    Verisure,
    VerisureAuthenticationError,
    VerisureCookieReadError,
    VerisureError,
    VerisureLoginError,
    VerisureRateLimitError,
    VerisureRequestError,
    VerisureResponseError,
)

type VerisureConfigEntry = ConfigEntry[VerisureDataUpdateCoordinator]

_MFA_REQUIRED_MESSAGE = (
    "Multifactor authentication enabled, disable or create MFA cookie"
)


def _requires_mfa_reauth(exc: VerisureLoginError) -> bool:
    """Return True when password login cannot proceed without MFA."""
    return _MFA_REQUIRED_MESSAGE in str(exc)


class VerisureDataUpdateCoordinator(DataUpdateCoordinator):
    """A Verisure Data Update Coordinator."""

    config_entry: VerisureConfigEntry

    def __init__(self, hass: HomeAssistant, entry: VerisureConfigEntry) -> None:
        """Initialize the Verisure hub."""
        self.imageseries: list[dict[str, str]] = []
        self._overview: list[dict] = []
        self._rate_limit_backoff_level = 0
        self._last_successful_cookie_refresh: datetime | None = None
        self._last_metadata_refresh: datetime | None = None
        self._metadata: dict = {}
        self._user_tracking_enabled = entry.options.get(CONF_USER_TRACKING, False)

        self.verisure = Verisure(
            username=entry.data[CONF_EMAIL],
            password=entry.data[CONF_PASSWORD],
            cookie_file_name=hass.config.path(
                STORAGE_DIR, f"swe_verisure_{entry.data[CONF_EMAIL]}"
            ),
        )

        super().__init__(
            hass,
            LOGGER,
            config_entry=entry,
            name=DOMAIN,
            update_interval=timedelta(
                seconds=entry.options.get(
                    CONF_SCAN_INTERVAL, int(DEFAULT_SCAN_INTERVAL.total_seconds())
                )
            ),
        )

    async def _async_password_login_after_cookie_read(self) -> None:
        """Re-authenticate with password when the cookie file cannot be used."""
        try:
            await self.hass.async_add_executor_job(self.verisure.login)
        except VerisureAuthenticationError as login_ex:
            raise ConfigEntryAuthFailed(
                "Verisure re-authentication failed after cookie could not be read"
            ) from login_ex
        except VerisureRateLimitError as login_ex:
            self._raise_rate_limited(login_ex, "password login")
        except (VerisureRequestError, VerisureResponseError) as login_ex:
            raise UpdateFailed(
                "Could not refresh Verisure session (transient)"
            ) from login_ex
        except VerisureLoginError as login_ex:
            if _requires_mfa_reauth(login_ex):
                raise ConfigEntryAuthFailed(
                    "Verisure multifactor authentication required"
                ) from login_ex
            raise ConfigEntryAuthFailed(
                "Verisure re-authentication failed after cookie could not be read"
            ) from login_ex
        except VerisureError as login_ex:
            raise ConfigEntryAuthFailed(
                "Verisure re-authentication failed after cookie could not be read"
            ) from login_ex

    async def _async_refresh_session_after_auth_failure(self) -> None:
        """Recover session when cookie refresh indicates expired authentication."""
        try:
            await self.hass.async_add_executor_job(self.verisure.login_cookie)
        except VerisureAuthenticationError as ex:
            raise ConfigEntryAuthFailed(
                "Verisure authentication rejected (invalid or expired session)"
            ) from ex
        except VerisureCookieReadError:
            await self._async_password_login_after_cookie_read()
        except VerisureRateLimitError as ex:
            self._raise_rate_limited(ex, "session refresh")
        except VerisureLoginError as ex:
            raise ConfigEntryAuthFailed("Credentials expired for Verisure") from ex
        except (VerisureRequestError, VerisureResponseError) as ex:
            raise UpdateFailed("Could not refresh Verisure session (transient)") from ex
        except VerisureError as ex:
            raise UpdateFailed("Could not log in to Verisure") from ex

    def _rate_limit_retry_seconds(self) -> float:
        """Return the next retry delay and advance the backoff level."""
        level = min(self._rate_limit_backoff_level, len(RATE_LIMIT_BACKOFF) - 1)
        retry_after = RATE_LIMIT_BACKOFF[level].total_seconds()
        if self._rate_limit_backoff_level < len(RATE_LIMIT_BACKOFF) - 1:
            self._rate_limit_backoff_level += 1
        return retry_after

    def _raise_rate_limited(self, exc: VerisureRateLimitError, context: str) -> None:
        """Log rate limiting and defer the next poll."""
        retry_after = self._rate_limit_retry_seconds()
        LOGGER.warning(
            "Verisure rate limited during %s, %s; backing off %s seconds",
            context,
            exc,
            int(retry_after),
        )
        raise UpdateFailed(
            f"Verisure rate limited during {context}",
            retry_after=retry_after,
        ) from exc

    async def _async_refresh_cookie_if_needed(self) -> None:
        """Refresh the session cookie when it is close to expiring."""
        if (
            self._last_successful_cookie_refresh is not None
            and dt_util.utcnow() - self._last_successful_cookie_refresh
            < COOKIE_REFRESH_INTERVAL
        ):
            return

        try:
            await self.hass.async_add_executor_job(self.verisure.update_cookie)
        except VerisureAuthenticationError:
            LOGGER.debug("Cookie expired, acquiring new cookies")
            await self._async_refresh_session_after_auth_failure()
        except VerisureCookieReadError:
            LOGGER.debug("Cookie unreadable, re-authenticating with password")
            await self._async_password_login_after_cookie_read()
        except VerisureRateLimitError as ex:
            self._raise_rate_limited(ex, "cookie refresh")
        except VerisureLoginError:
            LOGGER.debug("Login token expired, refreshing session")
            await self._async_refresh_session_after_auth_failure()
        except (VerisureRequestError, VerisureResponseError) as ex:
            LOGGER.warning(
                "Verisure unreachable or server error during cookie refresh, %s", ex
            )
            raise UpdateFailed("Unable to update cookie - Verisure unreachable") from ex
        except VerisureError as ex:
            raise UpdateFailed("Unable to update cookie") from ex

        self._last_successful_cookie_refresh = dt_util.utcnow()

    async def async_login(self) -> bool:
        """Login to Verisure."""
        try:
            await self.hass.async_add_executor_job(self.verisure.login_cookie)
        except VerisureAuthenticationError as ex:
            raise ConfigEntryAuthFailed(
                "Verisure authentication rejected (invalid or expired session)"
            ) from ex
        except VerisureCookieReadError:
            try:
                await self._async_password_login_after_cookie_read()
            except UpdateFailed as ex:
                LOGGER.warning(
                    "Verisure login unavailable (likely transient), %s",
                    ex,
                )
                return False
        except VerisureRateLimitError as ex:
            LOGGER.warning(
                "Verisure login rate limited; setup will retry later, %s", ex
            )
            return False
        except VerisureLoginError as ex:
            LOGGER.error("Credentials expired for Verisure, %s", ex)
            raise ConfigEntryAuthFailed("Credentials expired for Verisure") from ex
        except (
            VerisureRequestError,
            VerisureResponseError,
        ) as ex:
            LOGGER.warning(
                "Verisure login unavailable (likely transient), %s",
                ex,
            )
            return False
        except VerisureError as ex:
            LOGGER.error("Could not log in to Verisure, %s", ex)
            return False

        await self.hass.async_add_executor_job(
            self.verisure.set_giid, self.config_entry.data[CONF_GIID]
        )

        return True

    @override
    async def _async_update_data(self) -> dict:
        """Fetch data from Verisure."""
        await self._async_refresh_cookie_if_needed()
        security_events_query = self.verisure.event_log()
        security_events_query["variables"]["eventCategories"] = [
            "INTRUSION",
            "FIRE",
            "SOS",
            "WATER",
            "ANIMAL",
            "TECHNICAL",
            "WARNING",
        ]
        activity_events_query = self.verisure.event_log()
        activity_events_query["variables"]["eventCategories"] = [
            "ARM",
            "DISARM",
            "LOCK",
            "UNLOCK",
            "PICTURE",
        ]
        now = dt_util.utcnow()
        metadata_due = (
            self._last_metadata_refresh is None
            or now - self._last_metadata_refresh >= METADATA_REFRESH_INTERVAL
        )
        operations = [
            self.verisure.arm_state(),
            self.verisure.broadband(),
            self.verisure.cameras(),
            self.verisure.climate(),
            self.verisure.door_window(),
            self.verisure.smart_lock(),
            self.verisure.smartplugs(),
            security_events_query,
            activity_events_query,
        ]
        if self._user_tracking_enabled:
            operations.append(self.verisure.user_trackings())
        if metadata_due:
            operations.extend(
                (
                    self.verisure.charge_sms(),
                    self.verisure.firmware(),
                    self.verisure.is_guardian_activated(),
                    self.verisure.remaining_sms(),
                )
            )
        try:
            overview = await self.hass.async_add_executor_job(
                self.verisure.request,
                *operations,
            )
        except VerisureRateLimitError as err:
            self._raise_rate_limited(err, "data update")
        except VerisureError as err:
            LOGGER.error("Could not read overview, %s", err)
            raise UpdateFailed("Could not read overview") from err

        def unpack(overview: list, value: str) -> Any:
            unpacked = next(
                (
                    item["data"]["installation"][value]
                    for item in overview
                    if value in item.get("data", {}).get("installation", {})
                ),
                None,
            )
            return [] if unpacked is None else unpacked

        event_logs = [
            item["data"]["installation"]["eventLog"]
            for item in overview
            if "eventLog" in item.get("data", {}).get("installation", {})
        ]
        security_event_log = event_logs[0] if event_logs else {}
        activity_event_log = event_logs[1] if len(event_logs) > 1 else {}

        if metadata_due:
            firmware = unpack(overview, "firmware")
            activated_feature = unpack(overview, "activatedFeature")
            self._metadata = {
                "sms_charges": unpack(overview, "chargeSms"),
                "firmware": (
                    firmware.get("status", {}) if isinstance(firmware, dict) else {}
                ),
                "guardian": (
                    activated_feature.get("isFeatureActivated", False)
                    if isinstance(activated_feature, dict)
                    else False
                ),
                "remaining_sms": unpack(overview, "remainingSms"),
            }
            self._last_metadata_refresh = now

        # Store data in a way Home Assistant can easily consume it
        self._overview = overview
        self._rate_limit_backoff_level = 0
        return {
            "alarm": unpack(overview, "armState"),
            "broadband": unpack(overview, "broadband"),
            "cameras": {
                device["device"]["deviceLabel"]: device
                for device in unpack(overview, "cameras")
            },
            "climate": {
                device["device"]["deviceLabel"]: device
                for device in unpack(overview, "climates")
            },
            "door_window": {
                device["device"]["deviceLabel"]: device
                for device in unpack(overview, "doorWindows")
            },
            "locks": {
                device["device"]["deviceLabel"]: device
                for device in unpack(overview, "smartLocks")
            },
            "smart_plugs": {
                device["device"]["deviceLabel"]: device
                for device in unpack(overview, "smartplugs")
            },
            "security_events": (
                security_event_log.get("pagedList", [])
                if isinstance(security_event_log, dict)
                else []
            ),
            "activity_events": (
                activity_event_log.get("pagedList", [])
                if isinstance(activity_event_log, dict)
                else []
            ),
            "user_trackings": {
                str(tracking.get("xbnContactId") or tracking.get("deviceId")): tracking
                for tracking in unpack(overview, "userTrackings")
                if tracking.get("xbnContactId") or tracking.get("deviceId")
            },
            **self._metadata,
        }

    @Throttle(timedelta(seconds=60))
    def update_smartcam_imageseries(self) -> None:
        """Update the image series."""
        image_data = self.verisure.request(self.verisure.cameras_image_series())
        self.imageseries = [
            content
            for series in (
                image_data.get("data", {})
                .get("ContentProviderMediaSearch", {})
                .get("mediaSeriesList", [])
            )
            for content in series.get("deviceMediaList", [])
            if content.get("contentType") == "IMAGE_JPEG"
        ]

    @Throttle(timedelta(seconds=30))
    def smartcam_capture(self, device_id: str) -> None:
        """Capture a new image from a smartcam."""
        capture_request = self.verisure.request(
            self.verisure.camera_get_request_id(device_id)
        )
        request_id = (
            capture_request.get("data", {})
            .get("ContentProviderCaptureImageRequest", {})
            .get("requestId")
        )
        capture_status = None
        attempts = 0
        while capture_status != "AVAILABLE":
            if attempts == 30:
                break
            if attempts > 1:
                sleep(0.5)
            attempts += 1
            capture_data = self.verisure.request(
                self.verisure.camera_capture(device_id, request_id)
            )
            capture_status = (
                capture_data.get("data", {})
                .get("installation", {})
                .get("cameraContentProvider", {})
                .get("captureImageRequestStatus", {})
                .get("mediaRequestStatus")
            )
