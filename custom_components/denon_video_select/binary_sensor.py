"""Binary sensor platform for Denon Video Select."""

from homeassistant.components.binary_sensor import BinarySensorEntity

from .const import BINARY_SENSOR, DEFAULT_NAME
from .entity import DenonVideoSelectEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup binary_sensor platform."""
    async_add_devices([DenonVideoSelectBinarySensor(entry)])


class DenonVideoSelectBinarySensor(DenonVideoSelectEntity, BinarySensorEntity):
    """denon_video_select binary_sensor class."""

    @property
    def name(self):
        """Return the name of the binary_sensor."""
        return f"{DEFAULT_NAME}_{BINARY_SENSOR}"

    @property
    def is_on(self):
        """Return true if the binary_sensor is on."""
        return True
