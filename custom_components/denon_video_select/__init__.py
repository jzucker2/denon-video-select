"""
Custom integration to integrate Multi Zone Receiver with Home Assistant.

For more details about this integration, please refer to
https://github.com/jzucker2/multi-zone-receiver
"""

from dataclasses import dataclass
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import Config, HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.reload import async_setup_reload_service

from .const import DOMAIN, PLATFORMS

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

_LOGGER: logging.Logger = logging.getLogger(__package__)

# The type alias needs to be suffixed with 'ConfigEntry'
type DenonVideoSelectConfigEntry = ConfigEntry[DenonVideoSelectData]


@dataclass
class DenonVideoSelectData:
    name: str

    @classmethod
    def from_entry(cls, entry: DenonVideoSelectConfigEntry):
        _LOGGER.debug(
            "Processing data config entry: %s with entry.data: %s", entry, entry.data
        )
        name = entry.data.get(CONF_NAME)
        return cls(
            name=name,
        )


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: DenonVideoSelectConfigEntry,
):
    """Set up this integration using UI."""
    # if entry.runtime_data is None:
    #     _LOGGER.info(STARTUP_MESSAGE)

    # Assign the runtime_data
    entry.runtime_data = DenonVideoSelectData.from_entry(entry)

    await async_setup_reload_service(hass, DOMAIN, PLATFORMS)

    # Set up all platforms for this device/entry.
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Reload entry when its updated.
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: DenonVideoSelectConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        _LOGGER.debug(
            "Unloading platforms entry: %s with unload_ok: %s", entry, unload_ok
        )

    return unload_ok


async def async_reload_entry(
    hass: HomeAssistant,
    entry: DenonVideoSelectConfigEntry,
) -> None:
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)
