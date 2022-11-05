"""Platform for sensor integration."""
from __future__ import annotations

from datetime import datetime, timedelta
from dateutil import parser
import voluptuous as vol
import logging
from homeassistant.const import CONF_API_TOKEN
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from . import oura_api

TOKEN = ""
OURA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_TOKEN): str,
    }
)


def tdelta_to_hour_min(td):
    return str(td.seconds // 3600) + "hr " + str((td.seconds // 60) % 60) + "min"


def _seconds_to_hours(time_in_seconds):
    """Parses times in seconds and converts it to hours."""
    return round(int(time_in_seconds) / (60 * 60), 2)


def _get_date_string(days_from_now):
    if days_from_now < 0:
        days_from_now = days_from_now * -1
        date_delta = datetime.now() - timedelta(days_from_now)
    else:
        date_delta = datetime.now() + timedelta(days_from_now)
    return date_delta.strftime("%Y-%m-%d")


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""
    add_entities(
        [
            OuraSleep(config, hass),
            OuraReadiness(config, hass),
            OuraActivity(config, hass),
            OuraHeartRate(config, hass),
        ]
    )


# SLEEP
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
    def unique_id(self) -> str:
        """Return a unique id for the sensor."""
        return "oura_ring_sleep"

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
        yest_string = _get_date_string(-1)
        tom_string = _get_date_string(1)
        tod_string = _get_date_string(0)
        daily_sleep_response = api.get_data(
            self._oura_token, oura_api.OuraURLs.DAILY_SLEEP, yest_string, tom_string
        )
        if "data" in daily_sleep_response:
            sleep = daily_sleep_response["data"][(len(daily_sleep_response["data"]) - 1)]
            day = daily_sleep_response["data"][(len(daily_sleep_response["data"]) - 1)]["day"]
            score = daily_sleep_response["data"][(len(daily_sleep_response["data"]) - 1)]["score"]
            if day == tod_string:

                self._state = score
                logging.info("OuraRing: Sleep Score Data: %s", sleep)
                logging.info("OuraRing: Sleep Score Updated: %s", self._state)
                sleep_response = api.get_data(
                    self._oura_token, oura_api.OuraURLs.SLEEP, yest_string, tom_string
                )["data"]

                for item in sleep_response:
                    if item["type"] == "long_sleep":
                        bedtime_start = parser.parse(item["bedtime_start"])
                        bedtime_end = parser.parse(item["bedtime_end"])

                        self._attributes["data"] = {
                            "date": item["day"],
                            "bedtime_start_hour": bedtime_start.strftime("%H:%M"),
                            "bedtime_end_hour": bedtime_end.strftime("%H:%M"),
                            "breath_average": item["average_breath"],
                            "temperature_delta": item["readiness"]["temperature_deviation"],
                            "lowest_heart_rate": item["lowest_heart_rate"],
                            "heart_rate_average": item["average_heart_rate"],
                            "deep_sleep_duration": _seconds_to_hours(
                                item["deep_sleep_duration"]
                            ),
                            "rem_sleep_duration": _seconds_to_hours(
                                item["rem_sleep_duration"]
                            ),
                            "light_sleep_duration": _seconds_to_hours(
                                item["light_sleep_duration"]
                            ),
                            "total_sleep_duration": _seconds_to_hours(
                                item["total_sleep_duration"]
                            ),
                            "awake_duration": _seconds_to_hours(item["awake_time"]),
                            "in_bed_duration": _seconds_to_hours(item["time_in_bed"]),
                        }
                        logging.info("OuraRing: Updated Sleep Data: %s", self._attributes)

# ACTIVITY
class OuraReadiness(Entity):

    """Representation of a Sensor."""

    def __init__(self, config, hass):
        """Initialize the sensor."""
        self._state = 0
        self._attributes = {}
        self._oura_token = config.get(CONF_API_TOKEN)

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Oura Ring Readiness"

    @property
    def unique_id(self) -> str:
        """Return a unique id for the sensor."""
        return "oura_ring_readiness"

    @property
    def state(self) -> int:
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self) -> str:
        """Return the state of the sensor."""
        return "mdi:account-alert"

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
        yest_string = _get_date_string(-1)
        tom_string = _get_date_string(1)
        tod_string = _get_date_string(0)
        daily_readiness_response = api.get_data(
            self._oura_token, oura_api.OuraURLs.DAILY_READINESS, yest_string, tom_string
        )

        if "data" in daily_readiness_response:
            index = len(daily_readiness_response["data"]) - 1
            score = daily_readiness_response["data"][index]["score"]
            day = daily_readiness_response["data"][index]["day"]
            if day == tod_string:
                self._state = score
                logging.info("OuraRing: Readiness Score Updated: %s", self._state)

# READINESS
class OuraActivity(Entity):

    """Representation of a Sensor."""

    def __init__(self, config, hass):
        """Initialize the sensor."""
        self._state = 0
        self._attributes = {}
        self._oura_token = config.get(CONF_API_TOKEN)

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Oura Ring Activity"

    @property
    def unique_id(self) -> str:
        """Return a unique id for the sensor."""
        return "oura_ring_activity"

    @property
    def state(self) -> int:
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self) -> str:
        """Return the state of the sensor."""
        return "mdi:run-fast"

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
        one_week_ago = _get_date_string(-8)
        yest_string = _get_date_string(-1)
        tom_string = _get_date_string(1)
        tod_string = _get_date_string(0)
        daily_activity_response = api.get_data(
            self._oura_token, oura_api.OuraURLs.DAILY_ACTIVITY, yest_string, tom_string
        )

        if "data" in daily_activity_response:
            index = len(daily_activity_response["data"]) - 1
            day =  daily_activity_response["data"][index]["day"]
            if day == tod_string:
                score =  daily_activity_response["data"][index]["score"]
                self._state = score
                logging.info("OuraRing: Activity Score Updated: %s", self._state)

                self._attributes["data"] = {
                    "active_calories": daily_activity_response["data"][index][
                        "active_calories"
                    ],
                    "total_calories": daily_activity_response["data"][index][
                        "total_calories"
                    ],
                    "inactivity_alerts": daily_activity_response["data"][index][
                        "inactivity_alerts"
                    ],
                    "non_wear_time": daily_activity_response["data"][index][
                        "non_wear_time"
                    ],
                    "steps": daily_activity_response["data"][index]["steps"],
                    "target_calories": daily_activity_response["data"][index][
                        "target_calories"
                    ],
                    "date": daily_activity_response["data"][index]["day"],
                }
                logging.info("OuraRing: Updated Activity Data: %s", self._attributes)

            # Get Workout Data
            daily_workout_response = api.get_data(
                self._oura_token, oura_api.OuraURLs.WORKOUT, one_week_ago, tom_string
            )
            if "data" in daily_workout_response:
                workouts = daily_workout_response["data"]
                i = 1
                for item in workouts[
                    ::-1
                ]:  # reverse array before loop so newest go first
                    end_datetime = parser.parse(item["end_datetime"]).strftime("%H:%M")
                    start_datetime = parser.parse(item["start_datetime"]).strftime(
                        "%H:%M"
                    )
                    FMT = "%H:%M"
                    tdelta = datetime.strptime(end_datetime, FMT) - datetime.strptime(
                        start_datetime, FMT
                    )
                    self._attributes["workout_" + str(i)] = {
                        "activity": item["activity"],
                        "calories": item["calories"],
                        "distance": item["distance"],
                        "start_datetime": start_datetime,
                        "end_datetime": end_datetime,
                        "duration": tdelta_to_hour_min(tdelta),
                        "intensity": item["intensity"],
                        "label": item["label"],
                        "source": item["source"],
                        "date": item["day"],
                    }
                    logging.info(
                        "OuraRing: Updated Workout Data: %s",
                        self._attributes["workout_" + str(i)],
                    )
                    i = i + 1

# HeartRate
class OuraHeartRate(Entity):

    """Representation of a Sensor."""

    def __init__(self, config, hass):
        """Initialize the sensor."""
        self._state = 0
        self._attributes = {}
        self._oura_token = config.get(CONF_API_TOKEN)

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Oura Heart Activity"

    @property
    def unique_id(self) -> str:
        """Return a unique id for the sensor."""
        return "oura_ring_heart_activity"

    @property
    def state(self) -> int:
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self) -> str:
        """Return the state of the sensor."""
        return "mdi:heart"

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
        yest_string = _get_date_string(-7)
        tom_string = _get_date_string(1)
        heartrate_response = api.get_data(
            self._oura_token, oura_api.OuraURLs.HEARTRATE, yest_string, tom_string
        )
        if "data" in heartrate_response:

            index = len(heartrate_response["data"]) - 1
            self._state = heartrate_response["data"][index]["bpm"]
            logging.info("OuraRing: Heartrate Updated: %s", self._state)

            #make array of bpm
            bpm_array = []
            for item in heartrate_response["data"]:
                bpm_array.append(item["bpm"])

            #make array of timestamp
            timestamp_array = []
            for item in heartrate_response["data"]:
                timestamp_array.append(item["timestamp"])

            self._attributes["state_timestamp"] = heartrate_response["data"][index]["timestamp"]
            self._attributes["period_start"] = heartrate_response["data"][0]["timestamp"]
            self._attributes["period_end"] = heartrate_response["data"][index]["timestamp"]
            self._attributes["bpm"] = bpm_array
            self._attributes["timestamps"] = timestamp_array
            logging.info("OuraRing: Heartrate Stats Updated: %s", bpm_array)
