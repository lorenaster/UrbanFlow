from django.urls import path
from . import views
from django.http import HttpResponse

urlpatterns=[
    path('', views.home , name="home"),

    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('control-trafic/', views.controlTrafic, name="control-trafic"),
    path('config-rute/', views.configRute, name="config-rute"),
    path('admin-parteneri/', views.adminParteneri, name="admin-parteneri"),
    
    path('vizualizare-rute/', views.vizualizareRute, name="vizualizare-rute"),
    path('games/', views.games, name="games"),
    path('personalizare-profil/', views.personalizareProfil, name="personalizare-profil"),
]