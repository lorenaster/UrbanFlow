from neo4j import GraphDatabase
import requests
import pandas as pd

from dotenv import load_dotenv
import os 
load_dotenv()


# Connect to Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = "password"

driver = GraphDatabase.driver(uri, auth=(username, password))

BASE_URL = "https://api.tranzy.ai/v1/opendata"
API_KEY = os.getenv("TRANZY_API_KEY")
AGENCY_ID = "1"  

headers = {
    "X-Agency-Id": AGENCY_ID,
    "Accept": "application/json",
    "X-API-KEY": API_KEY
}

# Function to fetch data
def fetch_data(endpoint):
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else []

# Fetch data
routes = pd.DataFrame(fetch_data("routes"))
trips = pd.DataFrame(fetch_data("trips"))
stops = pd.DataFrame(fetch_data("stops"))
stop_times = pd.DataFrame(fetch_data("stop_times"))
shapes = pd.DataFrame(fetch_data("shapes"))

def insert_stop(tx, stop_id, name, lat, lon):
    query = """
    MERGE (s:Stop {stop_id: $stop_id})
    SET s.name = $name, s.lat = $lat, s.lon = $lon
    """
    tx.run(query, stop_id=stop_id, name=name, lat=lat, lon=lon)

def insert_stops(stops):
    with driver.session() as session:
        for _, stop in stops.iterrows():
            session.write_transaction(insert_stop, stop["stop_id"], stop["stop_name"], stop["stop_lat"], stop["stop_lon"])

def load_data():
    insert_stops(stops)

    print("Neo4j Data Inserted Successfully!")

if __name__ == "__main__":
    load_data()
