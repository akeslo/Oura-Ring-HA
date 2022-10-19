"""This modules connects to the oura API v2"""

import requests
import logging
from .const import OURA_TOKEN

# Oura API config.
_OURA_API = "https://api.ouraring.com/v2/usercollection"
_OURA_CLOUD = "https://cloud.ouraring.com"
_MAX_API_RETRIES = 3


class OuraURLs:
    """Class representing Oura Endpoint URLs"""

    # Data endpoints.
    DAILY_ACTIVITY = "{}/daily_activity".format(_OURA_API)
    DAILY_READINESS = "{}/daily_readiness".format(_OURA_API)
    DAILY_SLEEP = "{}/daily_sleep".format(_OURA_API)
    HEARTRATE = "{}/heartrate".format(_OURA_API)
    PERSONAL_INFO = "{}/personal_info".format(_OURA_API)
    SESSION = "{}/session".format(_OURA_API)
    SLEEP = "{}/sleep".format(_OURA_API)
    TAG = "{}/tag".format(_OURA_API)
    WORKOUT = "{}/workout".format(_OURA_API)


class OuraAPI:
    """Class representing Oura API Calls"""

    def make_request(self, url, token, params):
        """Make request to oura api"""
        headers = {
            "Authorization": "Bearer " + token,
            "Content-type": "application/json",
        }
        retries = 0
        while retries < _MAX_API_RETRIES:
            response = requests.request(
                "GET", url, headers=headers, params=params, timeout=30
            )
            result = response.json()
            if not result:
                logging.error("No result received from API request")
                retries += 1
                continue
            return result
        return None

    def get_data(self, token, endpoint, start_date=None, end_date=None, next_token=None):
        """Setup request to Daily endpoints"""
        # end_date default to current UTC date
        # start_date default to end_date - 1 day
        params = {"start_date": start_date, "end_date": end_date,}
        return self.make_request(endpoint, token, params)
