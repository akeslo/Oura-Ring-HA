"""This modules connects to the oura API v2"""

import logging

import requests

from .const import OURA_TOKEN

# Oura API config.
_OURA_API = "https://api.ouraring.com/v2/usercollection"
_OURA_CLOUD = "https://cloud.ouraring.com"
_MAX_API_RETRIES = 3


class OuraURLs:
    """Class representing Oura Endpoint URLs"""

    # Data endpoints.
    DAILY_ACTIVITY = f"{_OURA_API}/daily_activity"
    DAILY_READINESS = f"{_OURA_API}/daily_readiness"
    DAILY_SLEEP = f"{_OURA_API}/daily_sleep"
    HEARTRATE = f"{_OURA_API}/heartrate"
    PERSONAL_INFO = f"{_OURA_API}/personal_info"
    SESSION = f"{_OURA_API}/session"
    SLEEP = f"{_OURA_API}/sleep"
    TAG = f"{_OURA_API}/tag"
    WORKOUT = f"{_OURA_API}/workout"


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

    def get_data(
        self, token, endpoint, start_date=None, end_date=None, next_token=None
    ):
        """Setup request to Daily endpoints"""
        # end_date default to current UTC date
        # start_date default to end_date - 1 day
        params = {
            "start_date": start_date,
            "end_date": end_date,
        }
        return self.make_request(endpoint, token, params)
