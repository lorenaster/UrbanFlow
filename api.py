import requests
import os
from dotenv import load_dotenv
load_dotenv()
url = "https://api.tranzy.ai/v1/opendata/vehicles"
headers = {
    "X-Agency-Id": "",
    "Accept": "application/json",
    "X-API-KEY": os.getenv("TRANZY_API_KEY")
}

response = requests.get(url, headers=headers)

print(response.json())