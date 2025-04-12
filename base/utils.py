from dotenv import load_dotenv
import os 
import requests 
import polyline
from .neo4j_route_functions import get_public_transport_routes

load_dotenv()


ORS_API_KEY = os.getenv("ORS_API_KEY")

def geocode(place):
    geocode_url = "https://api.openrouteservice.org/geocode/search"
    params = {
        "text": place,
        "size": 1,
        "api_key": ORS_API_KEY,
        "boundary.country": "RO"
    }
    response = requests.get(geocode_url, params=params)
    data = response.json()

    if data.get("features"):
        return data["features"][0]["geometry"]["coordinates"]  # [lon, lat]
    else:
        return None
    
def get_car_route(start_coords, end_coords):
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {"Authorization": ORS_API_KEY}
    body = {"coordinates": [start_coords, end_coords]}
    response = requests.post(url, json=body, headers=headers).json()

    duration = int(response['routes'][0]['summary']['duration'] / 60)
    geometry = response['routes'][0]['geometry']
    route_shape = polyline.decode(geometry)
    distance_km = response['routes'][0]['summary']['distance'] / 1000

    #calculate price like uber

    base_fare = 1.3  
    distance_rate = 1.3  
    time_rate = 0.22 
    distance_charge = distance_km * distance_rate
    time_charge = duration* time_rate
    estimated_fare = base_fare + distance_charge + time_charge

    price=round(estimated_fare, 2)

    return {
        "mode": "car",
        "duration": duration,
        "price": price, 
        "eco_score": 3,
        "route_shape": route_shape
    }
def get_bike_route(start_coords, end_coords):
    url = "https://api.openrouteservice.org/v2/directions/cycling-regular"
    headers = {"Authorization": ORS_API_KEY}
    body = {"coordinates": [start_coords, end_coords]}
    response = requests.post(url, json=body, headers=headers).json()

    duration = int(response['routes'][0]['summary']['duration'] / 60)
    geometry = response['routes'][0]['geometry']
    route_shape = polyline.decode(geometry)

    return {
        "mode": "bike",
        "duration": duration,
        "price": 0,
        "eco_score": 1,
        "route_shape": route_shape
    }

def get_public_transport_route_data(start_coords, end_coords):
    public_transport_routes = get_public_transport_routes(
        start_coords[1], start_coords[0], end_coords[1], end_coords[0]
    )

    #calculate route shape

    #
    url = "https://api.openrouteservice.org/v2/directions/foot-walking"
    headers = {
        "Authorization": ORS_API_KEY
    }
    body = {
        "coordinates": [start_coords, end_coords]
    }
    
    response = requests.post(url, json=body, headers=headers)

    return {
        "mode": "public_transport",
        "duration": "-",
        "price": "-",
        "eco_score": 2,
        "route_info": public_transport_routes,
        "route_shape":"-"
    }