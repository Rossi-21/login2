from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from users_app.models import User
from .models import *
from .forms import LoginForm, CreateUserForm
import bcrypt


def index(request):

    form1 = CreateUserForm()
    form2 = LoginForm()

    if request.method == 'POST':

        form1 = CreateUserForm(request.POST)

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/dashboard')

        if form1.is_valid():
            form1.save()
            user = form1.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('/dashboard')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {
        'form1': form1,
        'form2': form2,
    }

    return render(request, "index.html", context)


# def register(request):
    # errors = User.objects.validator(request.POST)

    # if len(errors) > 0:

    # for key, value in errors.items():
    # messages.error(request, value)

    # return redirect('/dashboard')

   # else:

    # first_name = request.POST['first_name']
    # last_name = request.POST['last_name']
    # email = request.POST['email']
    # password = request.POST['password']
    # pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    # user = User.objects.create(
    # first_name=first_name, last_name=last_name, email=email, password=pw_hash)

    # return redirect('/dashboard', user)


# def login(request):

#     if request.method == "POST":
#         form = LoginForm(request.post)
#         if form.is_valid():
#             user = User.objects.filter(email=request.POST['email'])

#             if user:

#                 logged_user = user[0]

#                 if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
#                     request.session['userid'] = logged_user.id

#                     return redirect('/dashboard')

#                 else:
#                     form = LoginForm()

#                     return redirect('/')


def dashboard(request):
    user_id = request.session.get('userid')
    user = User.objects.get(id=user_id)
    context = {"user": user}
    return render(request, "dashboard.html", context)
