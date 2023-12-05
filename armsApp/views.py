import datetime
from django.shortcuts import redirect, render,HttpResponse

import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from armsApp import models, forms
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.utils import timezone


def context_data():
    context = {
        'page_name' : '',
        'page_title' : '',
        'system_name' : 'Airlines Reservation Managament System',
        'topbar' : True,
        'footer' : True,
    }

    return context
    
def userregister(request):
    context = context_data()
    context['topbar'] = False
    context['footer'] = False
    context['page_title'] = "User Registration"
    if request.user.is_authenticated:
        return redirect("home-page")
    return render(request, 'register.html', context)

@login_required
def upload_modal(request):
    context = context_data()
    return render(request, 'upload.html', context)

def save_register(request):
    resp={'status':'failed', 'msg':''}
    if not request.method == 'POST':
        resp['msg'] = "No data has been sent on this request"
    else:
        form = forms.SaveUser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Account has been created succesfully")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if resp['msg'] != '':
                        resp['msg'] += str('<br />')
                    resp['msg'] += str(f"[{field.name}] {error}.")
            
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def update_profile(request):
    context = context_data()
    context['page_title'] = 'Update Profile'
    user = User.objects.get(id = request.user.id)
    if not request.method == 'POST':
        form = forms.UpdateProfile(instance=user)
        context['form'] = form
        print(form)
    else:
        form = forms.UpdateProfile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated")
            return redirect("profile-page")
        else:
            context['form'] = form
            
    return render(request, 'manage_profile.html',context)

@login_required
def update_password(request):
    context =context_data()
    context['page_title'] = "Update Password"
    if request.method == 'POST':
        form = forms.UpdatePasswords(user = request.user, data= request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your Account Password has been updated successfully")
            update_session_auth_hash(request, form.user)
            return redirect("profile-page")
        else:
            context['form'] = form
    else:
        form = forms.UpdatePasswords(request.POST)
        context['form'] = form
    return render(request,'update_password.html',context)

# Create your views here.
def login_page(request):
    context = context_data()
    context['topbar'] = False
    context['footer'] = False
    context['page_name'] = 'login'
    context['page_title'] = 'Login'
    return render(request, 'login.html', context)

def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')

def search_flight(request):
    context = context_data()
    context['page'] = 'Search Available Flight'
    airlines = models.Airlines.objects.filter(delete_flag = 0, status = 1).all()
    airports = models.Airport.objects.filter(delete_flag = 0, status = 1).all()
    context['airlines'] = airlines
    context['airports'] = airports
    
    return render(request,'search_flight.html', context)

def search_result(request, fromA=None, toA=None, departure = None):
    context = context_data()
    context['page'] = 'Search Result'
    if fromA is None and toA is None and departure is None:
        messages.error(request, "Invalid Search Inputs")
        return redirect('public-page')
    else:
        departure = datetime.datetime.strptime(departure, "%Y-%m-%d")
        year = departure.strftime("%Y")
        month = departure.strftime("%m")
        day = departure.strftime("%d")
        context['flights'] = models.Flights.objects.filter(delete_flag=0,
                        departure__year = year,
                        departure__month = month,
                        departure__day = day,
                        ).order_by('departure').all()
        return render(request, 'search_result.html', context)

def save_reservation(request):
    resp = { 'status': 'failed', 'msg':'' }
    if not request.method == 'POST':
       resp['msg'] = "No data has been sent."
    else:
        form = forms.SaveReservation(request.POST)
        if form.is_valid():
            form.save()
            resp['status'] = 'success'
            resp['msg'] = "Your Reservation has been sent. Our staff will reach as soon we sees your reservation. Thank you!"
            messages.success(request,f"{resp['msg']}")
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str("<br />")

                    resp['msg'] += str(f"[{field.name}] {error}")
    return HttpResponse(json.dumps(resp), content_type="application/json")

def reserve_form(request, pk=None):
    context = context_data()
    context['page'] = 'Search Result'
    if pk is None:
        messages.error(request, "Invalid Flight ID")
        return redirect('public-page')
    else:
        context['flight'] = models.Flights.objects.get(id=pk)
        return render(request, 'reservation.html', context)


@login_required
def home(request):
    context = context_data()
    context['page'] = 'home'
    context['page_title'] = 'Home'
    context['airlines'] = models.Airlines.objects.filter(delete_flag=0, status=1).count()
    context['airport'] = models.Airport.objects.filter(delete_flag=0, status=1).count()

    now = datetime.datetime.now()
    print(f"Now: {now}")
    upcoming_flights_count  = models.Flights.objects.filter(
        delete_flag=0,
        departure__gt=now,
    ).count()
    print(f"Upcoming Flights Count: {upcoming_flights_count}")

    context['flight'] = upcoming_flights_count

    return render(request, 'home.html', context)

def logout_user(request):
    logout(request)
    return redirect('login-page')
    
@login_required
def profile(request):
    context = context_data()
    context['page'] = 'profile'
    context['page_title'] = "Profile"
    return render(request,'profile.html', context)

#Airline
@login_required
def list_airline(request):
    context = context_data()
    context['page_title'] ="Airlines"
    context['airlines'] = models.Airlines.objects.filter(delete_flag = 0).all()
    return render(request, 'airlines.html', context) 

@login_required
def manage_airline(request, pk = None):
    if pk is None:
        airline = {}
    else:
        airline = models.Airlines.objects.get(id = pk)
    context = context_data()
    context['page_title'] ="Manage Airline"
    context['airline'] = airline
    return render(request, 'manage_airline.html', context) 

@login_required
def save_airline(request):
    resp = { 'status': 'failed', 'msg':'' }
    if not request.method == 'POST':
       resp['msg'] = "No data has been sent."
    else:
        post = request.POST
        if not post['id'] == '':
            airline = models.Airlines.objects.get(id = post['id'])
            form = forms.SaveAirlines(request.POST, request.FILES, instance = airline)
        else:
            form = forms.SaveAirlines(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            resp['status'] = 'success'
            if post['id'] == '':
                resp['msg'] = "New Airline has been added successfully."
            else:
                resp['msg'] = "Airline Details has been updated successfully."
            messages.success(request,f"{resp['msg']}")
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str("<br />")

                    resp['msg'] += str(f"[{field.name}] {error}")
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_airline(request, pk=None):
    resp = { 'status' : 'failed', 'msg' : '' }
    if pk is None:
        resp['msg'] = 'No ID has been sent'
    else:
        try:
            models.Airlines.objects.filter(id = pk).update(delete_flag = 1)
            resp['status'] = 'success'
            messages.success(request, "Airline has been deleted successfully")
        except:
            resp['msg'] = 'Airline has failed to delete'
    return HttpResponse(json.dumps(resp), content_type="application/json")

    
#Airport
@login_required
def list_airport(request):
    context = context_data()
    context['page_title'] ="Airports"
    context['airports'] = models.Airport.objects.filter(delete_flag = 0).all()
    return render(request, 'airports.html', context) 

@login_required
def manage_airport(request, pk = None):
    if pk is None:
        airport = {}
    else:
        airport = models.Airport.objects.get(id = pk)
    context = context_data()
    context['page_title'] ="Manage Airport"
    context['airport'] = airport
    return render(request, 'manage_airport.html', context) 

@login_required
def save_airport(request):
    resp = { 'status': 'failed', 'msg':'' }
    if not request.method == 'POST':
       resp['msg'] = "No data has been sent."
    else:
        post = request.POST
        if not post['id'] == '':
            airport = models.Airport.objects.get(id = post['id'])
            form = forms.SaveAirports(request.POST, instance = airport)
        else:
            form = forms.SaveAirports(request.POST)

        if form.is_valid():
            form.save()
            resp['status'] = 'success'
            if post['id'] == '':
                resp['msg'] = "New Airport has been added successfully."
            else:
                resp['msg'] = "Airport Details has been updated successfully."
            messages.success(request,f"{resp['msg']}")
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str("<br />")

                    resp['msg'] += str(f"[{field.name}] {error}")
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_airport(request, pk=None):
    resp = { 'status' : 'failed', 'msg' : '' }
    if pk is None:
        resp['msg'] = 'No ID has been sent'
    else:
        try:
            models.Airport.objects.filter(id = pk).update(delete_flag = 1)
            resp['status'] = 'success'
            messages.success(request, "Airport has been deleted successfully")
        except:
            resp['msg'] = 'airport has failed to delete'
    return HttpResponse(json.dumps(resp), content_type="application/json")

#Flight
@login_required
def list_flight(request):
    context = context_data()
    context['page_title'] ="Flights"
    context['flights'] = models.Flights.objects.filter(delete_flag = 0).all()
    return render(request, 'flights.html', context) 

@login_required
def manage_flight(request, pk = None):
    if pk is None:
        flight = {}
    else:
        flight = models.Flights.objects.get(id = pk)
    airlines = models.Airlines.objects.filter(delete_flag = 0, status = 1).all()
    airports = models.Airport.objects.filter(delete_flag = 0, status = 1).all()
    context = context_data()
    context['page_title'] ="Manage Flight"
    context['flight'] = flight
    context['airlines'] = airlines
    context['airports'] = airports
    return render(request, 'manage_flight.html', context) 

@login_required
def save_flight(request):
    resp = { 'status': 'failed', 'msg':'' }
    if not request.method == 'POST':
       resp['msg'] = "No data has been sent."
    else:
        post = request.POST
        if not post['id'] == '':
            Flight = models.Flights.objects.get(id = post['id'])
            form = forms.SaveFlights(request.POST, instance = Flight)
        else:
            form = forms.SaveFlights(request.POST)

        if form.is_valid():
            form.save()
            resp['status'] = 'success'
            if post['id'] == '':
                resp['msg'] = "New Flight has been added successfully."
            else:
                resp['msg'] = "Flight Details has been updated successfully."
            messages.success(request,f"{resp['msg']}")
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str("<br />")

                    resp['msg'] += str(f"[{field.name}] {error}")
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_flight(request, pk = None):
    if pk is None:
        flight = {}
    else:
        flight = models.Flights.objects.get(id = pk)
    context = context_data()
    context['page_title'] ="Flight Details"
    context['flight'] = flight
    return render(request, 'view_flight_details.html', context) 

@login_required
def delete_flight(request, pk=None):
    resp = { 'status' : 'failed', 'msg' : '' }
    if pk is None:
        resp['msg'] = 'No ID has been sent'
    else:
        try:
            models.Flights.objects.filter(id = pk).update(delete_flag = 1)
            resp['status'] = 'success'
            messages.success(request, "Flight has been deleted successfully")
        except:
            resp['msg'] = 'Flight has failed to delete'
    return HttpResponse(json.dumps(resp), content_type="application/json")

#Reservation
@login_required
def list_reservation(request):
    context = context_data()
    context['page_title'] ="Reservations"
    context['reservations'] = models.Reservation.objects.all()
    return render(request, 'reservation_list.html', context) 

@login_required
def view_reservation(request, pk = None):
    if pk is None:
        reservation = {}
    else:
        reservation = models.Reservation.objects.get(id = pk)
    context = context_data()
    context['page_title'] ="Reservation Details"
    context['reservation'] = reservation
    return render(request, 'view_reservation_details.html', context) 

@login_required
def delete_reservation(request, pk=None):
    resp = { 'status' : 'failed', 'msg' : '' }
    if pk is None:
        resp['msg'] = 'No ID has been sent'
    else:
        try:
            models.Reservation.objects.filter(id = pk).delete()
            resp['status'] = 'success'
            messages.success(request, "Reservation has been deleted successfully")
        except:
            resp['msg'] = 'Reservation has failed to delete'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def update_reservation(request):
    resp = { 'status' : 'failed', 'msg' : '' }
    if not request.method == 'POST':
        resp['msg'] = 'No ID has been sent'
    else:
        try:
            models.Reservation.objects.filter(id = request.POST['id']).update(status=request.POST['status'])
            resp['status'] = 'success'
            messages.success(request, "Reservation Status has been updated successfully")
        except:
            resp['msg'] = 'Reservation Status has failed to update'
    return HttpResponse(json.dumps(resp), content_type="application/json")
    
