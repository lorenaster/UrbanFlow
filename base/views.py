from django.shortcuts import render, redirect 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from geopy.geocoders import Nominatim

from rest_framework.views import APIView
from rest_framework.response import Response
from .tranzy_app.neo4j_client import Neo4jClient
from django.conf import settings
import folium
import json

import folium
from folium.plugins import LocateControl
import geocoder
import polyline

from .neo4j_route_functions import get_public_transport_routes

import requests
from dotenv import load_dotenv
import os 
load_dotenv()

#Tranzy API
BASE_URL = "https://api.tranzy.ai/v1/opendata"
TRANZY_API_KEY = os.getenv("TRANZY_API_KEY")
AGENCY_ID = "1"  

HEADERS = {
    "X-Agency-Id": AGENCY_ID,
    "Accept": "application/json",
    "X-API-KEY": TRANZY_API_KEY
}

#Ors API
ORS_API_KEY = os.getenv("ORS_API_KEY")

UBER_CLIENT_ID = "fcAusZdrOsx_ELifulIB4eirkE4VHerw"
UBER_CLIENT_SECRET = "ND1KBZa_xguFNVkiHMNJoVfDK3xm19tWxo4g3IZQ"

@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello from Django!"})

@api_view(['POST'])
def loginPage(request):
    if request.user.is_authenticated:
        
            return Response({"message": "User already authenticated."}, status=status.HTTP_200_OK)

    username = request.data.get('username').lower()
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return Response({'message': 'Logged in successfully', 'user': user.username})
    else:
        return Response({'error': 'Invalid credentials'}, status=400)

@api_view(['POST'])
def logoutUser(request):
    logout(request)
    return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

@api_view(['POST'])
def registerPage(request):
    username = request.data.get('username')
    password = request.data.get('password')
    password_confirm = request.data.get('password_confirm')

    # validation checks
    if password != password_confirm:
        return Response({"detail": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
    
    if not username or not password:
        return Response({"detail": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    # check if username already exists
    if get_user_model().objects.filter(username=username).exists():
        return Response({"detail": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = get_user_model().objects.create_user(username=username, password=password)
        return Response({"detail": "User successfully registered.", "username": user.username}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def get_tranzy_info(request):
    #Loading map
    # map = folium.Map(location=[47.151726, 27.587914], zoom_start=10)
    # g = geocoder.ip('me')
    # folium.Marker(
    #     location=g.latlng,
    #     popup="You",
    # ).add_to(map)
    # folium.plugins.LocateControl(auto_start=True).add_to(map)
    # map_html = map._repr_html_()

    #Get bus/tram, type, long name from api
    routes_url = f"{BASE_URL}/routes"
    routes_response = requests.get(routes_url, headers=HEADERS)

    if routes_response.status_code != 200:
        return Response({'error': 'Error fetching routes'}, status=500)

    routes_data = routes_response.json()

    routes=[]

    for route in routes_data:
        routes.append({
        "route_short_name": route["route_short_name"],  # Changed key name
        "route_type": int(route["route_type"]),
        "route_long_name": route["route_long_name"]
    })

    return Response({'routes': routes})


@api_view(['GET'])
def autocomplete(request):
    query = request.query_params.get("text", "")
    if len(query) < 3:
        return JsonResponse({"features": []})

    url = "https://api.openrouteservice.org/geocode/autocomplete"
    params = {
        "api_key": ORS_API_KEY,
        "text": query,
        "boundary.country": "RO"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        location_names = [{"label": feature["properties"]["label"]} for feature in data.get("features", [])]

        return Response({"features": location_names})
    except Exception as e:
        return Response({"error": str(e)}, status=500)

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

@api_view(['GET'])
def car_route(request):
    start_place = request.query_params.get('start')
    end_place = request.query_params.get('end')

    if not start_place or not end_place:
        return Response({"error": "Missing start or end location"}, status=400)

    start_coords=geocode(start_place)
    end_coords=geocode(end_place)

    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {"Authorization": ORS_API_KEY}
    body = {"coordinates": [start_coords, end_coords]}
    response = requests.post(url, json=body, headers=headers).json()

    duration = int(response['routes'][0]['summary']['duration'] / 60)
    geometry = response['routes'][0]['geometry']
    route_shape = polyline.decode(geometry)

    return Response({
        "car_duration": duration, 
        "car_route_shape": route_shape
    })

@api_view(['GET'])
def bike_route(request):
    start_place = request.query_params.get('start')
    end_place = request.query_params.get('end')

    if not start_place or not end_place:
        return Response({"error": "Missing start or end location"}, status=400)

    start_coords=geocode(start_place)
    end_coords=geocode(end_place)

    url = "https://api.openrouteservice.org/v2/directions/cycling-regular"
    headers = {"Authorization": ORS_API_KEY}
    body = {"coordinates": [start_coords, end_coords]}
    response = requests.post(url, json=body, headers=headers).json()

    duration = int(response['routes'][0]['summary']['duration'] / 60)
    geometry = response['routes'][0]['geometry']
    route_shape = polyline.decode(geometry)

    return Response({
        "bike_duration": duration, 
        "bike_route_shape": route_shape
    })

#returneaza o lista cu statie, autobuz, statie, autobuz etc
@api_view(['GET'])
def public_transport_route(request): 
    start_place = request.query_params.get('start')
    end_place = request.query_params.get('end')

    if not start_place or not end_place:
        return Response({"error": "Missing start or end location"}, status=400)

    start_coords=geocode(start_place)
    end_coords=geocode(end_place)
    public_transport_routes=get_public_transport_routes(start_coords[1], start_coords[0], end_coords[1], end_coords[0])

    return Response({
        "public_transport_routes": public_transport_routes
    })

        # #Render Folium Map with route 
        # encoded_geometry = route_data_car['routes'][0]['geometry']
        # #ruta masina
        # route_coords = polyline.decode(encoded_geometry)  # This gives [(lat, lon), ...]

        #     # Create the map
        # midpoint = [  # Calculate midpoint for centering the map
        #     (start_coords[1] + end_coords[1]) / 2,
        #     (start_coords[0] + end_coords[0]) / 2
        # ]
        # map = folium.Map(location=midpoint, zoom_start=12)

        # # Add route line
        # folium.PolyLine(route_coords, color="blue", weight=5, opacity=0.8).add_to(map)

        #     # Add start and end markers
        # folium.Marker(location=[start_coords[1], start_coords[0]], tooltip="Start").add_to(map)
        # folium.Marker(location=[end_coords[1], end_coords[0]], tooltip="End").add_to(map)

        # map = map._repr_html_()  # Render HTML for template

# def games(request):
#  #TO DO 
#     messages.error(request, "not implemented yet.")
#     return redirect('home')

# def notificari(request):
#  #TO DO 
#     messages.error(request, "not implemented yet.")
#     return redirect('home')

# def rapoarte(request):
#  #TO DO 
#     messages.error(request, "not implemented yet.")
#     return redirect('home')

# def personalizareProfil(request):
#  #TO DO 
#     messages.error(request, "not implemented yet.")
#     return redirect('home')

# @login_required(login_url='login')
# def controlTrafic(request):
#  #TO DO 
#     messages.error(request, "not implemented yet.")
#     return redirect('home')

# def configRute(request):
#  #TO DO 
#     messages.error(request, "not implemented yet.")
#     return redirect('home')

# def adminParteneri(request):
#  #TO DO 
#     messages.error(request, "not implemented yet.")
#     return redirect('home')

#TO DO rapoarte si sugestii tot cu socketio?
