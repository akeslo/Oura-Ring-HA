"""Platform for sensor integration."""
from __future__ import annotations
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.entity import Entity
from homeassistant.core import HomeAssistant
from datetime import datetime, timedelta
from homeassistant.const import CONF_API_TOKEN
import voluptuous as vol
from . import oura_api

TOKEN = ""
OURA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_TOKEN): str,
    }
)


_EMPTY_SENSOR_ATTRIBUTE = {
    "date": None,
    "bedtime_start_hour": None,
    "bedtime_end_hour": None,
    "breath_average": None,
    "temperature_delta": None,
    "resting_heart_rate": None,
    "heart_rate_average": None,
    "deep_sleep_duration": None,
    "rem_sleep_duration": None,
    "light_sleep_duration": None,
    "total_sleep_duration": None,
    "awake_duration": None,
    "in_bed_duration": None,
}


def _seconds_to_hours(time_in_seconds):
    """Parses times in seconds and converts it to hours."""
    return round(int(time_in_seconds) / (60 * 60), 2)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""
    add_entities([OuraSleep(config, hass)])


class OuraSleep(Entity):

    """Representation of a Sensor."""

    def __init__(self, config, hass):
        """Initialize the sensor."""
        self._state = 0
        self._attributes = {}
        self._oura_token = config.get(CONF_API_TOKEN)

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Oura Ring Sleep"

    @property
    def state(self) -> int:
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self) -> str:
        """Return the state of the sensor."""
        return "mdi:sleep"

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return ""

    @property
    # pylint: disable=hass-return-type
    def extra_state_attributes(self):
        return self._attributes

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        api = oura_api.OuraAPI()
        utc_now = datetime.utcnow()
        utc_now_string = utc_now.strftime("%Y-%m-%d")
        utc_yest = utc_now - timedelta(1)
        utc_yest_string = utc_yest.strftime("%Y-%m-%d")
        daily_sleep_response = api.get_data(
            self._oura_token,
            oura_api.OuraURLs.DAILY_SLEEP,
            utc_yest_string,
            utc_now_string,
        )
        self._state = daily_sleep_response["data"][0]["score"]
        sleep_response = api.get_data(
            self._oura_token, oura_api.OuraURLs.SLEEP, utc_yest_string, utc_now_string
        )["data"]
        for item in sleep_response:
            if item["type"] == "long_sleep":
                self._attributes[item["day"]] = {
                    "date": item["day"],
                    "bedtime_start_hour": item["bedtime_start"],
                    "bedtime_end_hour": item["bedtime_end"],
                    "breath_average": item["average_breath"],
                    "temperature_delta": item["readiness"]["temperature_deviation"],
                    "lowest_heart_rate": item["lowest_heart_rate"],
                    "heart_rate_average": item["average_heart_rate"],
                    "deep_sleep_duration": _seconds_to_hours(
                        item["deep_sleep_duration"]
                    ),
                    "rem_sleep_duration": _seconds_to_hours(item["rem_sleep_duration"]),
                    "light_sleep_duration": _seconds_to_hours(
                        item["light_sleep_duration"]
                    ),
                    "total_sleep_duration": _seconds_to_hours(
                        item["total_sleep_duration"]
                    ),
                    "awake_duration": _seconds_to_hours(item["awake_time"]),
                    "in_bed_duration": _seconds_to_hours(item["time_in_bed"]),
                }
