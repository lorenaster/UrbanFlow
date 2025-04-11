from django.shortcuts import render, redirect 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
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



def home(request):
    return render(request, 'base/home.html')

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
            messages.success(request, 'User loged in')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)
    messages.error(request, "not implemented yet.")
    return redirect('home')

def logoutUser(request):
    logout(request)
    messages.success(request, "user logged out")
    return redirect('home')
    messages.error(request, "not implemented yet.")
    return redirect('home')

def registerPage(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'base/login_register.html', {'form': form})
    messages.error(request, "not implemented yet.")
    return redirect('home')

@login_required(login_url='login')
def vizualizareRute(request):
    #Loading map
    map = folium.Map(location=[47.151726, 27.587914], zoom_start=10)
    g = geocoder.ip('me')
    folium.Marker(
        location=g.latlng,
        popup="You",
    ).add_to(map)
    folium.plugins.LocateControl(auto_start=True).add_to(map)
    map_html = map._repr_html_()

    #Get bus/tram, type, long name from api
    routes_url = f"{BASE_URL}/routes"
    routes_response = requests.get(routes_url, headers=HEADERS)

    if routes_response.status_code != 200:
        message.error(request, "Error fetching routes")
        exit()

    routes_data = routes_response.json()

    routes=[]

    for route in routes_data:
        routes.append({
        "route_short_name": route["route_short_name"],  # Changed key name
        "route_type": int(route["route_type"]),
        "route_long_name": route["route_long_name"]
    })

    return render(request, 'base/vizualizare_rute.html', {'map': map_html, 'routes': routes})
 #TO DO 
    messages.error(request, "not implemented yet.")
    return redirect('home')

def configurareTrasee(request):
    return render(request, 'base/configurare_trasee.html', {'ORS_API_KEY': ORS_API_KEY})

def autocomplete(request):
    query = request.GET.get("text", "")
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
        return JsonResponse(response.json())
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def calculate_route(request):
    UBER_AUTH_URL = 'https://login.uber.com/oauth/v2/token'
    UBER_API_URL = 'https://api.uber.com/v1.2'
    duration = None  # Initialize the duration to None
    map=None
    uber_price = None
    uber_time = None

    if request.method == 'POST':
        start_location = request.POST.get('start')
        end_location = request.POST.get('end')

        # Function to geocode a place name using ORS Geocoding API
        def geocode_place(place):
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

        # Get coordinates for both locations
        start_coords = geocode_place(start_location)
        end_coords = geocode_place(end_location)

        print(f"start: {start_coords}, finish: {end_coords}")

        # ORS API request to calculate the route
        route_url_car = "https://api.openrouteservice.org/v2/directions/driving-car"
        headers = {
        "Authorization": ORS_API_KEY
        }

        body = {
            "coordinates": [start_coords, end_coords]
        }

        #pentru masini
        try:
            response = requests.post(route_url_car, json=body, headers=headers)
            response.raise_for_status()  # Raise an error for non-2xx codes
            route_data_car = response.json()
        except Exception as e:
            print(f"Error with the API request: {e}")
            route_data_car = {}

        if 'routes' in route_data_car and len(route_data_car['routes']) > 0 and start_coords!=end_coords:
            duration_in_seconds = route_data_car['routes'][0]['summary']['duration']
            duration_car = int(duration_in_seconds / 60)  # Convert to minutes
       
        #pentru biciclete
        route_url_bicl = "https://api.openrouteservice.org/v2/directions/cycling-regular"

        try:
            response = requests.post(route_url_bicl, json=body, headers=headers)
            response.raise_for_status()  # Raise an error for non-2xx codes
            route_data_bicl = response.json()
        except Exception as e:
            print(f"Error with the API request: {e}")
            route_data_bicl = {}

        duration = None  # default in case of error
        if 'routes' in route_data_bicl and len(route_data_bicl['routes']) > 0 and start_coords != end_coords:
            duration_in_seconds = route_data_bicl['routes'][0]['summary']['duration']
            duration_bicl = int(duration_in_seconds / 60)  # Convert to minutes

        #public transport
        public_transport_routes=get_public_transport_routes(start_coords[1], start_coords[0], end_coords[1], end_coords[0])


        #Render Folium Map with route 
        encoded_geometry = route_data_car['routes'][0]['geometry']
        #ruta masina
        route_coords = polyline.decode(encoded_geometry)  # This gives [(lat, lon), ...]

            # Create the map
        midpoint = [  # Calculate midpoint for centering the map
            (start_coords[1] + end_coords[1]) / 2,
            (start_coords[0] + end_coords[0]) / 2
        ]
        map = folium.Map(location=midpoint, zoom_start=12)

        # Add route line
        folium.PolyLine(route_coords, color="blue", weight=5, opacity=0.8).add_to(map)

            # Add start and end markers
        folium.Marker(location=[start_coords[1], start_coords[0]], tooltip="Start").add_to(map)
        folium.Marker(location=[end_coords[1], end_coords[0]], tooltip="End").add_to(map)

        map = map._repr_html_()  # Render HTML for template

        return render(request, 'base/configurare_trasee.html', {'duration_car': duration_car, 'duration_bicl': duration_bicl,
                                                                 'map': map, 'routes': public_transport_routes})
    else:
        return render(request, 'base/configurare_trasee.html')

def games(request):
 #TO DO 
    messages.error(request, "not implemented yet.")
    return redirect('home')

def notificari(request):
 #TO DO 
    messages.error(request, "not implemented yet.")
    return redirect('home')

def rapoarte(request):
 #TO DO 
    messages.error(request, "not implemented yet.")
    return redirect('home')

def personalizareProfil(request):
 #TO DO 
    messages.error(request, "not implemented yet.")
    return redirect('home')

@login_required(login_url='login')
def controlTrafic(request):
 #TO DO 
    messages.error(request, "not implemented yet.")
    return redirect('home')

def configRute(request):
 #TO DO 
    messages.error(request, "not implemented yet.")
    return redirect('home')

def adminParteneri(request):
 #TO DO 
    messages.error(request, "not implemented yet.")
    return redirect('home')

#TO DO rapoarte si sugestii tot cu socketio?

