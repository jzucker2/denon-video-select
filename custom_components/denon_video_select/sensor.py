"""Sensor platform for Denon Video Select."""

from .const import DEFAULT_NAME, SENSOR
from .entity import DenonVideoSelectEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    async_add_devices([DenonVideoSelectSensor(entry)])


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
