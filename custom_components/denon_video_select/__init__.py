"""
Custom integration to integrate Denon Video Select with Home Assistant.

For more details about this integration, please refer to
https://github.com/jzucker2/denon-video-select
"""

from dataclasses import dataclass
import logging

from homeassistant.components.denonavr import DOMAIN as DENON_DOMAIN
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import Config, HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.reload import async_setup_reload_service

from .const import CONF_MAIN_RECEIVER, DOMAIN, PLATFORMS

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

_LOGGER: logging.Logger = logging.getLogger(__package__)

# The type alias needs to be suffixed with 'ConfigEntry'
type DenonVideoSelectConfigEntry = ConfigEntry[DenonVideoSelectData]


@dataclass
class DenonVideoSelectData:
    name: str
    main_receiver: str

    @classmethod
    def _get_denon_domain_data(cls, hass):
        # TODO: maybe protect against no data?
        denon_domain_data = hass.data[DENON_DOMAIN]
        _LOGGER.debug("denon_domain_data: %s", denon_domain_data)
        return denon_domain_data

    @classmethod
    def from_entry(cls, entry: DenonVideoSelectConfigEntry):
        _LOGGER.debug(
            "Processing data config entry: %s with entry.data: %s", entry, entry.data
        )
        name = entry.data.get(CONF_NAME)
        main_receiver = entry.data.get(CONF_MAIN_RECEIVER)
        return cls(
            name=name,
            main_receiver=main_receiver,
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

    denon_domain_data = DenonVideoSelectData._get_denon_domain_data(hass)
    _LOGGER.debug(
        "async_setup_entry entry: %s for denon_domain_data: %s with entry.data: %s",
        entry,
        denon_domain_data,
        entry.data,
    )

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
