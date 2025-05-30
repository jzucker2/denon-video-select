"""Constants for Denon Video Select."""

# Base component constants
NAME = "Denon Video Select"
DOMAIN = "denon_video_select"
VERSION = "0.8.5"

ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"
ISSUE_URL = "https://github.com/jzucker2/denon-video-select/issues"

# Icons
ICON = "mdi:format-quote-close"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
BINARY_SENSOR = "binary_sensor"
SENSOR = "sensor"
MEDIA_PLAYER = "media_player"
PLATFORMS = [BINARY_SENSOR, SENSOR]

# Services
SERVICE_SELECT_VIDEO_SOURCE = "select_video_source"


# Configuration and options
CONF_ENABLED = "enabled"
CONF_MAIN_RECEIVER = "main_receiver"

# Defaults
DEFAULT_NAME = DOMAIN


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
