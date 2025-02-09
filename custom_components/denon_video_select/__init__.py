"""
Custom integration to integrate Denon Video Select with Home Assistant.

For more details about this integration, please refer to
https://github.com/jzucker2/denon-video-select
"""

from dataclasses import dataclass
import logging

from denonavr import DenonAVR
from homeassistant.components.denonavr import (
    CONF_RECEIVER,
    DOMAIN as DENON_DOMAIN,
    DenonavrConfigEntry,
)
from homeassistant.const import CONF_NAME
from homeassistant.core import Config, HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.reload import async_setup_reload_service

from .const import CONF_MAIN_RECEIVER, DOMAIN, PLATFORMS

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

_LOGGER: logging.Logger = logging.getLogger(__package__)


class DenonVideoSelectDataException(Exception):
    pass


class MissingDenonConfigEntryException(DenonVideoSelectDataException):
    pass


@dataclass
class DenonVideoSelectData:
    name: str
    main_receiver_entity: str
    main_receiver: DenonAVR

    @classmethod
    def _get_denon_domain_data(cls, hass):
        # TODO: maybe protect against no data?
        denon_domain_data = hass.data[DENON_DOMAIN]
        _LOGGER.debug("denon_domain_data: %s", denon_domain_data)
        return denon_domain_data

    @classmethod
    def _get_first_denon_config_entry(cls, hass):
        denon_data = cls._get_denon_domain_data(hass)
        if not denon_data:
            e_m = "Missing denon data"
            _LOGGER.error(e_m)
            raise MissingDenonConfigEntryException(e_m)
        _LOGGER.debug("type(denon_data): %s", type(denon_data))
        only_entries = list(denon_data.values())
        _LOGGER.debug("only_entries: %s", only_entries)
        config_entry = only_entries[0]
        _LOGGER.debug("config_entry: %s", config_entry)
        return config_entry

    @classmethod
    def _get_first_denon_receiver(cls, hass) -> DenonAVR:
        config_entry = cls._get_first_denon_config_entry(hass)
        receiver = config_entry[CONF_RECEIVER]
        _LOGGER.debug("receiver: %s", receiver)
        return receiver

    @classmethod
    def from_entry(cls, hass, entry: DenonavrConfigEntry):
        _LOGGER.debug(
            "Processing data config entry: %s with entry.data: %s", entry, entry.data
        )
        name = entry.data.get(CONF_NAME)
        main_receiver_entity = entry.data.get(CONF_MAIN_RECEIVER)

        main_receiver = cls._get_first_denon_receiver(hass)

        return cls(
            name=name,
            main_receiver_entity=main_receiver_entity,
            main_receiver=main_receiver,
        )


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: DenonavrConfigEntry,
):
    """Set up this integration using UI."""
    # if entry.runtime_data is None:
    #     _LOGGER.info(STARTUP_MESSAGE)

    # Assign the runtime_data
    entry.runtime_data = DenonVideoSelectData.from_entry(hass, entry)

    await async_setup_reload_service(hass, DOMAIN, PLATFORMS)

    # Set up all platforms for this device/entry.
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Reload entry when its updated.
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: DenonavrConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        _LOGGER.debug(
            "Unloading platforms entry: %s with unload_ok: %s", entry, unload_ok
        )

    return unload_ok


async def async_reload_entry(
    hass: HomeAssistant,
    entry: DenonavrConfigEntry,
) -> None:
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)
