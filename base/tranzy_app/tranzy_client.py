import requests
import pandas as pd
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class TranzyClient:
    def __init__(self, city=None, agency_id=None):
        self.base_url = settings.TRANZY_BASE_URL
        self.api_key = settings.TRANZY_API_KEY
        
        if city and not agency_id:
            self.agency_id = settings.TRANZY_AGENCY_MAPPING.get(city, settings.TRANZY_AGENCY_ID)
        else:
            self.agency_id = agency_id or settings.TRANZY_AGENCY_ID

        if isinstance(self.agency_id, dict):
            self.agency_id = self.agency_id.get('agency_id')
            
        self.agency_id = str(self.agency_id)    
        self.headers = {
            "X-Agency-Id": self.agency_id,
            "Accept": "application/json",
            "X-API-KEY": self.api_key
        }
        logger.info(f"TranzyClient initialized with agency_id: {self.agency_id}")

    def fetch_data(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        logger.info(f"Fetching data from: {url}")
        logger.debug(f"Headers: {self.headers}")
        
        try:
            response = requests.get(url, headers=self.headers)
            logger.info(f"Response status code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Fetched {len(data)} records from {endpoint}")
                return data
            else:
                logger.error(f"API error: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            logger.error(f"Exception during API request: {str(e)}")
            return []

    def get_routes(self):
        data = self.fetch_data("routes")
        df = pd.DataFrame(data)
        logger.info(f"Created routes dataframe with shape: {df.shape}")
        return df

    def get_trips(self):
        data = self.fetch_data("trips")
        df = pd.DataFrame(data)
        logger.info(f"Created trips dataframe with shape: {df.shape}")
        return df

    def get_stops(self):
        data = self.fetch_data("stops")
        df = pd.DataFrame(data)
        logger.info(f"Created stops dataframe with shape: {df.shape}")
        return df

    def get_stop_times(self):
        data = self.fetch_data("stop_times")
        df = pd.DataFrame(data)
        logger.info(f"Created stop_times dataframe with shape: {df.shape}")
        return df

    def get_shapes(self):
        data = self.fetch_data("shapes")
        df = pd.DataFrame(data)
        logger.info(f"Created shapes dataframe with shape: {df.shape}")
        return df