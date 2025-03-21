from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Flight, Passenger

# Create your views here.
def index(request):
  return render(request, 'flights/index.html', {
    'flights': Flight.objects.all()
  })

def flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    passengers = flight.passengers.all()
    non_passengers = Passenger.objects.exclude(flights=flight).all()
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": passengers,
        "non_passengers": non_passengers
    })

def book(request, flight_id):
  if request.method == "POST":
    flight = Flight.objects.get(pk=flight_id)
    passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
    passenger.flights.add(flight)
    return HttpResponseRedirect(reverse('flight', args=(flight.id,)))

