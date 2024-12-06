import requests
from rest_framework import viewsets  
from .models import Flight
from django.conf import settings
from django.shortcuts import render , redirect
from django.views.decorators.csrf import csrf_exempt
from .serializers import FlightSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

def home(request):
    return render(request, 'flights/home.html')
    
# Signup View
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        # Create the user
        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, "Signup successful! Please login.")
        return redirect('login')

    return render(request, 'flights/signup-login.html')

# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('search-flights')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'flights/signup-login.html')

# Logout View (Optional)
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

# Search Flights View (Placeholder)
def search_flights(request):
    return render(request, 'flight_search.html')


@login_required 
@csrf_exempt
def search_flights(request):
    if request.method == 'POST':
        source_airport_code = request.POST.get('from')
        destination_airport_code = request.POST.get('to')
        departure_date = request.POST.get('departure_date')
        num_adults = request.POST.get('adults')
        cabin_class = request.POST.get('class')
        print("from request : -----------",request.POST)

        url = "https://booking-com15.p.rapidapi.com/api/v1/flights/searchFlights"
        querystring = {
            "sourceAirportCode": f"{source_airport_code}",
            "destinationAirportCode": f"{destination_airport_code}",
            "pageNo": "1",
            "numAdults": num_adults,
            "numSeniors":"0",
            # "children": "0,17",  # Assuming no children for simplicity
            "sortOrder": "ML_BEST_VALUE",
            "date":departure_date,
            "itineraryType":"ONE_WAY",
            
            "classOfService": "ECONOMY",
            # "currency_code": "USD"
        }
        print("querystring:----------------------",querystring)
        headers = {
            "x-rapidapi-key": settings.TRIPADVISOR_API_KEY,
            "x-rapidapi-host": "tripadvisor16.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        flights_data = response.json()
        print("flights--------------------------------: 00-------------------",flights_data)

        
        flights = flights_data.get('data', {}).get('flights', [])
        
        return render(request, 'flights/flight_list.html', {'flights': flights})
    else:
        return render(request, 'flights/flight_search.html')
