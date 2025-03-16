from django.shortcuts import render, redirect 
from django.contrib import messages

def home(request):
    return render(request, 'base/home.html')

def loginPage(request):
     #TO DO 
    messages.error(request, "not implemented yet.")
    return redirect('home')

def logoutUser(request):
 #TO DO 
    messages.error(request, "not implemented yet.")
    return redirect('home')

def registerPage(request):
 #TO DO 
    messages.error(request, "not implemented yet.")
    return redirect('home')

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

def vizualizareRute(request):
 #TO DO 
    messages.error(request, "not implemented yet.")
    return redirect('home')

def games(request):
 #TO DO 
    messages.error(request, "not implemented yet.")
    return redirect('home')

def personalizareProfil(request):
 #TO DO 
    messages.error(request, "not implemented yet.")
    return redirect('home')

#TO DO notificari si alerte in timp real cu socket.io??

#TO DO rapoarte si sugestii tot cu socket.io?

