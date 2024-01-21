from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarDealer
from .restapis import get_dealers_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

def index(request):
    return render(request, 'djangoapp/index.html')

# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')

# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')
# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/index.html', context)
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}

    if request.method == "POST":
        # Get form data
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        username = request.POST['username']
        password = request.POST['password']

        # Validate form data
        if not firstName or not lastName or not username or not password:
            context['error_message'] = 'Please fill in all required fields.'
            return render(request, 'djangoapp/registration.html', context)

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            context['error_message'] = 'Username already exists.'
            return render(request, 'djangoapp/registration.html', context)

        # Try to create a new user
        try:
            user = User.objects.create_user(username=username, password=password, first_name=firstName, last_name=lastName)
            user.save()
        except IntegrityError:
            context['error_message'] = 'Registration failed. Please try again.'
            return render(request, 'djangoapp/registration.html', context)

        # If user creation is successful, log the user in and redirect them to the main page
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')

    return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships

def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://abenxy0-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)

# def get_dealerships(request):
#     if request.method == "GET":
#         context = {}

#         state = request.GET.get("st")
#         dealerId = request.GET.get("dealerId")
#         url = "https://abenxy0-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"

#         try:
#             if state:
#                 dealerships = get_dealers_from_cf(url, st=state)
#             elif dealerId:
#                 dealerships = get_dealers_from_cf(url, dealerId=dealerId)
#             else:
#                 dealerships = get_dealers_from_cf(url)
#         except Exception as e:
#             # Handle the error and set dealerships to an empty list or display an error message
#             dealerships = []
#             context["error"] = f"An error occurred while fetching dealerships: {e}"

#         context["dealership_list"] = dealerships
#         print(context["dealership_list"])

#         return render(request, "djangoapp/index.html", context=context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

