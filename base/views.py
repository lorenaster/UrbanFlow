from django.shortcuts import render, redirect 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
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
import geocoder

import requests
from dotenv import load_dotenv
import os 
load_dotenv()

BASE_URL = "https://api.tranzy.ai/v1/opendata"
API_KEY = os.getenv("TRANZY_API_KEY")
AGENCY_ID = "1"  

HEADERS = {
    "X-Agency-Id": AGENCY_ID,
    "Accept": "application/json",
    "X-API-KEY": API_KEY
}



class CityListView(APIView):
    def get(self, request):
        return Response(list(settings.TRANZY_AGENCY_MAPPING.keys()))


class TownListView(APIView):
    def get(self, request, city):
        agency_info = settings.TRANZY_AGENCY_MAPPING.get(city)
        if not agency_info:
            return Response({'error': 'Invalid city'}, status=400)

        client = Neo4jClient()
        towns = client.get_towns_by_city(city)
        client.close()
        return Response(towns)


class RouteListView(APIView):
    def get(self, request, town, city):
        agency_info = settings.TRANZY_AGENCY_MAPPING.get(city)
        if not agency_info:
            return Response({'error': 'Invalid city'}, status=400)

        agency_id = agency_info['agency_id']
        client = Neo4jClient()
        routes = client.get_routes_by_town(town, agency_id)
        client.close()
        return Response(routes)


class RouteDetailView(APIView):
    def get(self, request, route_id, city):
        agency_info = settings.TRANZY_AGENCY_MAPPING.get(city)
        if not agency_info:
            return Response({'error': 'Invalid city'}, status=400)

        agency_id = agency_info['agency_id']
        client = Neo4jClient()
        route_details = client.get_route_details(route_id, agency_id)
        client.close()
        return Response(route_details)


class ShapeView(APIView):
    def get(self, request, shape_id, city):
        agency_info = settings.TRANZY_AGENCY_MAPPING.get(city)
        if not agency_info:
            return Response({'error': 'Invalid city'}, status=400)

        client = Neo4jClient()
        shape_points = client.get_shape_points(shape_id)
        client.close()
        
        if shape_points:
            m = folium.Map(location=[shape_points[0]['lat'], shape_points[0]['lon']], zoom_start=13, tiles='Stamen Toner')
            folium.PolyLine(
                locations=[[point['lat'], point['lon']] for point in shape_points],
                color='black',
                weight=3,
                opacity=0.8
            ).add_to(m)

            map_html = m._repr_html_()
            
            return Response({
                'shape_points': shape_points,
                'map_html': map_html
            })
        
        return Response({'error': 'No shape points found'}, status=404)

@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello from Django!"})





# def home(request):
#     return render(request, 'base/home.html')

# def loginPage(request):
#     page = 'login'

#     if request.user.is_authenticated:
#         return redirect('home')

#     if request.method == 'POST':
#         username = request.POST.get('username').lower()
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect("home")
#             messages.success(request, 'User loged in')
#         else:
#             messages.error(request, 'Username OR password does not exit')

#     context = {'page': page}
#     return render(request, 'base/login_register.html', context)
#     messages.error(request, "not implemented yet.")
#     return redirect('home')

# def logoutUser(request):
#     logout(request)
#     messages.success(request, "user logged out")
#     return redirect('home')
#     messages.error(request, "not implemented yet.")
#     return redirect('home')

# def registerPage(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Your account has been created successfully!')
#             return redirect('login')
#     else:
#         form = UserCreationForm()
#     return render(request, 'base/login_register.html', {'form': form})
#     messages.error(request, "not implemented yet.")
#     return redirect('home')

# @login_required(login_url='login')
# def vizualizareRute(request):
#     #Loading map
#     map = folium.Map(location=[47.151726, 27.587914], zoom_start=20)
#     g = geocoder.ip('me')
#     folium.Marker(
#         location=g.latlng,
#         popup="You",
#     ).add_to(map)
#     map_html = map._repr_html_()

#     #Get bus/tram, type, long name from api
#     routes_url = f"{BASE_URL}/routes"
#     routes_response = requests.get(routes_url, headers=HEADERS)

#     if routes_response.status_code != 200:
#         message.error(request, "Error fetching routes")
#         exit()

#     routes_data = routes_response.json()

#     routes=[]

#     for route in routes_data:
#         routes.append({
#         "route_short_name": route["route_short_name"],  # Changed key name
#         "route_type": int(route["route_type"]),
#         "route_long_name": route["route_long_name"]
#     })

#     return render(request, 'base/vizualizare_rute.html', {'map': map_html, 'routes': routes})
#  #TO DO 
#     messages.error(request, "not implemented yet.")
#     return redirect('home')

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

# #TO DO rapoarte si sugestii tot cu socketio?
