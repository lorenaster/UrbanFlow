from django.shortcuts import render, redirect 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

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
    map = folium.Map(location=[47.151726, 27.587914], zoom_start=20)
    g = geocoder.ip('me')
    folium.Marker(
        location=g.latlng,
        popup="You",
    ).add_to(map)
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

