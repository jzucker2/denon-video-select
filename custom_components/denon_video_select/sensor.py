"""Sensor platform for Denon Video Select."""

import asyncio
import logging

from homeassistant.components.media_player import ATTR_INPUT_SOURCE

from .const import DEFAULT_NAME, DOMAIN, SENSOR, SERVICE_SELECT_VIDEO_SOURCE
from .entity import DenonVideoSelectEntity

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    only_video_select_sensor = DenonVideoSelectSensor(entry)
    async_add_devices([only_video_select_sensor])
    only_video_select_sensor.async_register_hass_custom_actions(hass)


class DenonVideoSelectSensor(DenonVideoSelectEntity):
    """denon_video_select Sensor class."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{SENSOR}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return "foo"

    async def async_send_telnet_commands(self, *commands: str) -> None:
        """Send telnet commands to the receiver."""
        _LOGGER.debug("async_send_telnet_commands commands: %s", commands)
        await self.main_receiver.async_send_telnet_commands(*commands)

    def _get_source(self, call_data):
        source = call_data.get(ATTR_INPUT_SOURCE)
        return source

    async def _async_select_video_source(self, input_source: str):
        await asyncio.sleep(0)
        _LOGGER.debug("_async_select_video_source input_source: %s", input_source)
        await self.async_send_telnet_commands("SVAUX2")

    async def handle_select_video_source(self, call):
        """Handle the service action call."""
        _LOGGER.debug("handle_select_video_source call: %s", call)
        source = self._get_source(call.data)
        await self._async_select_video_source(source)

    def async_register_hass_custom_actions(self, hass):
        """Register all the custom service actions."""
        hass.services.async_register(
            DOMAIN, SERVICE_SELECT_VIDEO_SOURCE, self.handle_select_video_source
        )
