from django.urls import path
from . import views
from django.http import HttpResponse


urlpatterns=[
    # path('', views.home , name="home"),
    path('api/hello/', views.hello_world, name = "hello_world"),
    path('api/login/', views.loginPage, name="login"),
    path('api/logout/', views.logoutUser, name="logout"),
    path('api/register/', views.registerPage, name="register"),

    path('api/get_tranzy_info', views.get_tranzy_info , name="get_tranzy_info"),
    path('api/autocomplete', views.autocomplete , name="autocomplete"),
    path('api/geocode', views.geocode , name="geocode"),
    path('api/car_route', views.car_route , name="car_route"),
    path('api/bike_route', views.bike_route , name="bike_route"),
    path('api/public_transport_route', views.public_transport_route , name="public_transport_route"),

    # path( 'vizualizare-rute/', views.vizualizareRute, name="vizualizare-rute"),
    # path( 'configurare-trasee/', views.configurareTrasee, name="configurare-trasee"),
    # path("configurare-trasee/autocomplete/", views.autocomplete, name="autocomplete"),
    # path('configurare-trasee/calculate-route/', views.calculate_route, name='calculate_route'),

    # path('games/', views.games, name="games"),
    # path('notificari/', views.notificari, name="notificari"),

    # path('rapoarte/', views.rapoarte, name="rapoarte" ),
    # path('personalizare-profil/', views.personalizareProfil, name="personalizare-profil"),

    # path('control-trafic/', views.controlTrafic, name="control-trafic"),
    # path('config-rute/', views.configRute, name="config-rute"),
    # path('admin-parteneri/', views.adminParteneri, name="admin-parteneri"),
]