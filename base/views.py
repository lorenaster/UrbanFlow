from django.shortcuts import render, redirect 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


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


#TO DO rapoarte si sugestii tot cu socketio?

