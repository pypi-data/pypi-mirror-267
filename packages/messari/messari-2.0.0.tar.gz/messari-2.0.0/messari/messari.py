# -*- coding: utf-8 -*- #
"""This provides the Messari class implementation which acts as
Messari's Crypto Data API client."""

import requests

# --------- Constants --------- #

BASE_URL = "https://api.messari.io"

# --------- Constants --------- #


class Messari:
    """
    Messari class to act as Messari's Crypto Data API client.
    All the requests can be made through this class.
    """

    def __init__(self, key):
        """
        Initialize the object
        :param key: API key
        """
        self.key = key
        self.session = requests.Session()
        self.session.headers.update({'x-messari-api-key': key})
        self.session.headers.update({'accept': "application/json"})

    def _send_message(self, method, endpoint, params=None, data=None):
        """
        Send API request.
        :param method: HTTP method (get, post, delete, etc.)
        :param endpoint: Endpoint (to be added to base URL)
        :param params: HTTP request parameters
        :param data: JSON-encoded string payload for POST
        :return: dict/list: JSON response
        """
        url = BASE_URL + endpoint
        response = self.session.request(method, url, params=params,
                                 data=data, timeout=30)
        return response.json()

    def _get(self, endpoint, params=None):
        """
        Get API request
        :param endpoint: Endpoint (to be added to base URL)
        :param params: HTTP request parameters
        :return:
        """
        return self._send_message('GET', endpoint, params=params)

    def get_all_assets(self, **query_params):
        """
        Get the paginated list of all assets and their metrics and profiles.

        :param query_params: dict of query parameters to filter the list
        :return: JSON response
        """
        path = '/asset/v1/assets'

        return self._get(path, params=query_params)

    def get_asset_by_id(self, asset_id: str):
        """
        Returns the ID, name, symbol, slug, market cap, sector, category, and tags for a single asset.
        :return: JSON response
        """
        path = f'/asset/v1/assets/{asset_id}'

        return self._get(path)

    def get_market_data_by_asset(self, asset_id: str):
        """
        Returns market data for a specific asset.
        :return: JSON response
        """
        path = f'/marketdata/v1/assets/{asset_id}/price'

        return self._get(path)

    def get_timeseries_by_asset(self, asset_id: str, startTime: str, endTime: str, interval: str = None, vwapType: str = None):
        """
        Lists all the available timeseries for asset.

        :return: JSON response
        """
        path = f'/marketdata/v1/assets/{asset_id}/price/time-series'
        params = {
            'interval': interval,
            'vwapType': vwapType,
            'startTime': startTime,
            'endTime': endTime,
        }
        return self._get(path, params=params)

    def get_all_time_high(self):
        """
        Returns a list of all time high data for all assets.
        """
        path = '/marketdata/v1/assets/ath'

        return self._get(path)

    def get_all_time_high_by_asset(self, asset_id):
        """
        Returns a single assets ATH data.
        """
        path = f'/marketdata/v1/assets/{asset_id}/ath'

        return self._get(path)

    def get_roi(self):
        """
        Returns a list ROI data for all assets.
        """
        path = f'/marketdata/v1/assets/roi'

        return self._get(path)

    def get_roi_by_asset(self, asset_id):
        """
        Returns a single assets ROI data.
        """
        path = f'/marketdata/v1/assets/{asset_id}/roi'

        return self._get(path)

    def get_markets(self,
                    exchangeId: str = None,
                    baseAssetId: str = None,
                    quoteAssetId: str = None,
                    volumeAbove: str = None,
                    volumeBelow: str = None,
                    vwapAbove: str = None,
                    vwapBelow: str = None
                    ):
        """
        Returns a list of market specific data for all markets.
        """
        path = f'/marketdata/v1/markets'

        params = {
            'exchangeId': exchangeId,
            'baseAssetId': baseAssetId,
            'quoteAssetId': quoteAssetId,
            'volumeAbove': volumeAbove,
            'volumeBelow': volumeBelow,
            'vwapAbove': vwapAbove,
            'vwapBelow': vwapBelow
        }

        return self._get(path, params=params)

    def get_market(self, market_id: str):
        """
        Returns a list of market specific data for one market.
        """
        path = f'/marketdata/v1/markets/{market_id}'

        return self._get(path)

    def get_timeseries_by_market(
            self,
            market_id: str,
            startTime: str,
            endTime: str,
            interval: str = None,
            denominatedIn: str = None
    ):
        """
        Returns timeseries price and volume data for a given market.
        """
        path = f'/marketdata/v1/markets/{market_id}/price/time-series'

        params = {
            'interval': interval,
            'denominatedIn': denominatedIn,
            'startTime': startTime,
            'endTime': endTime
        }

        return self._get(path, params=params)

    def get_exchanges(self):
        """
        Returns a list of exchanges with market data.
        """
        path = '/marketdata/v1/exchanges'

        return self._get(path)

    def get_volume_timeseries_by_exchange(
            self,
            exchange_id: str,
            startTime: str = None,
            endTime: str = None,
            interval: str = None
    ):
        """
        Provides time series volume data for a given exchange.
        """
        path = f'/marketdata/v1/exchanges/{exchange_id}/volume/time-series'

        params = {
            'interval': interval,
            'startTime': startTime,
            'endTime': endTime
        }

        return self._get(path, params=params)

    def get_events(self, **kwargs):
        """
        Returns a list of all events and the most recent update. If there is no latest update to the event,
        the response will return updateDetails: null.
        """
        path = f'/intel/v1/events'

        return self._get(path, params=kwargs)

    def get_event_history(self, eventId: str):
        """
        Returns a single event and its entire history of updates by event ID.
        """
        path = f'/intel/v1/events/{eventId}'

        return self._get(path)

    def get_supported_assets(self, **kwargs):
        """
        Returns a list of all assets that Messari Intel actively covers.
        """
        path = f'/intel/v1/assets'

        return self._get(path, params=kwargs)
