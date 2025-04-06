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
# Merge trips with routes to get route_short_name
trips_with_route = trips.merge(routes[['route_id', 'route_short_name']], on='route_id', how='left')


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

# Function to insert stop sequences
def insert_stop_sequences(stop_times):
    with driver.session() as session:
        for trip_id, group in stop_times.groupby("trip_id"):
            sorted_group = group.sort_values("stop_sequence")  # Order by stop_sequence
            
            previous_stop = None
            for _, stop_time in sorted_group.iterrows():
                current_stop = stop_time["stop_id"]
                
                if previous_stop:
                    session.write_transaction(insert_stop_sequence, trip_id, previous_stop, current_stop)
                
                previous_stop = current_stop

# Function to insert stop sequences in order
def insert_stop_sequence(tx, trip_id, stop1_id, stop2_id):
    query = """
    MATCH (s1:Stop {stop_id: $stop1_id}), (s2:Stop {stop_id: $stop2_id})
    MERGE (s1)-[:NEXT {trip_id: $trip_id}]->(s2)
    """
    tx.run(query, stop1_id=stop1_id, stop2_id=stop2_id, trip_id=trip_id)

def insert_bus(tx, trip_id, direction_id, name, shape_id):
    query = """
    MERGE (b:Bus {trip_id: $trip_id})
    SET b.direction_id = $direction_id,
        b.name = $name,
        b.shape_id = $shape_id
    """
    tx.run(query, trip_id=trip_id, direction_id=direction_id, name=name, shape_id=shape_id)

def insert_stops_at(tx, trip_id, stop_id):
    query = """
    MATCH (b:Bus {trip_id: $trip_id}), (s:Stop {stop_id: $stop_id})
    MERGE (b)-[:STOPS_AT]->(s)
    """
    tx.run(query, trip_id=trip_id, stop_id=stop_id)

def insert_buses_and_relationships(trips_with_route, stop_times):
    with driver.session() as session:
        for _, row in trips_with_route.iterrows():
           session.write_transaction(insert_bus, row["trip_id"], row["direction_id"], row["route_short_name"], row["shape_id"])

        for _, stop_time in stop_times.iterrows():
            session.write_transaction(insert_stops_at, stop_time["trip_id"], stop_time["stop_id"])


def load_data():
    insert_stops(stops)
    insert_stop_sequences(stop_times)  # Insert stop sequences
    insert_buses_and_relationships(trips_with_route, stop_times)

    print("Neo4j Data Inserted Successfully!")


if __name__ == "__main__":
    load_data()
