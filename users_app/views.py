from django.shortcuts import render, redirect
from django.contrib import messages
from users_app.models import User


def index(request):
    return render(request, "index.html")


def register(request):
    errors = User.objects.validator(request.POST)

    if len(errors) > 0:

        for key, value in errors.items():
            messages.error(request, value)

        return redirect('/')

    else:

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create(
            first_name=first_name, last_name=last_name, email=email, password=password)

        return redirect('dashboard/')


def dashboard(request):
    return render(request, "dashboard.html")
