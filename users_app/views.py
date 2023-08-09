from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users_app.models import User
import bcrypt


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
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        user = User.objects.create(
            first_name=first_name, last_name=last_name, email=email, password=pw_hash)

        return redirect('/dashboard', user)


def login(request):

    user = User.objects.filter(email=request.POST['email'])

    if user:

        logged_user = user[0]

        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id

            return redirect('/dashboard')

    return redirect('/')


def dashboard(request):
    user_id = request.session.get('userid')
    user = User.objects.get(id=user_id)
    context = {"user": user}
    return render(request, "dashboard.html", context)
