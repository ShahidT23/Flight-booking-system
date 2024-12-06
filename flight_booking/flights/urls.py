from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlightViewSet  
from . import views

router = DefaultRouter()
router.register(r'api/flights', FlightViewSet)

urlpatterns = [
    #path('', include(router.urls)),
    path('', views.home, name='home'),  # Default home route
    path('signup/', views.signup_view, name='signup'),  # Signup route
    path('login/', views.login_view, name='login'),  # Login route
    path('logout/', views.logout_view, name='logout'),  # Logout route 
    path('search-flights/', views.search_flights, name='search-flights'), 
]