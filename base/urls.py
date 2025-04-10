from django.urls import path
from . import views
from django.http import HttpResponse


urlpatterns=[
    # path('', views.home , name="home"),
    path('hello/', views.hello_world, name = "hello_world"),


    # path('login/', views.loginPage, name="login"),
    # path('logout/', views.logoutUser, name="logout"),
    # path('register/', views.registerPage, name="register"),
    
    path('cities/', views.CityListView.as_view(), name='city-list'),
    path('towns/<str:city>/', views.TownListView.as_view(), name='town-list'),
    path('routes/<str:town>/<str:city>/', views.RouteListView.as_view(), name='route-list'),
    path('route/<str:route_id>/<str:city>/', views.RouteDetailView.as_view(), name='route-detail'),
    path('shape/<str:shape_id>/<str:city>/', views.ShapeView.as_view(), name='shape-detail'),

    # path( 'vizualizare-rute/', views.vizualizareRute, name="vizualizare-rute"),
    # path('games/', views.games, name="games"),
    # path('notificari/', views.notificari, name="notificari"),

    # path('rapoarte/', views.rapoarte, name="rapoarte" ),
    # path('personalizare-profil/', views.personalizareProfil, name="personalizare-profil"),

    # path('control-trafic/', views.controlTrafic, name="control-trafic"),
    # path('config-rute/', views.configRute, name="config-rute"),
    # path('admin-parteneri/', views.adminParteneri, name="admin-parteneri"),
]