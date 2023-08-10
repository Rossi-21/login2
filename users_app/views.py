from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from users_app.models import User
from .forms import LoginForm, CreateUserForm
import bcrypt


def index(request):

    form1 = CreateUserForm()
    form2 = LoginForm()

    if request.method == 'POST':
        form1 = CreateUserForm(request.POST)
        if form1.is_valid():
            form1.save()
            return redirect()

    context = {
        'form1': form1,
        'form2': form2,
    }

    return render(request, "index.html", context)


def register(request):
    errors = User.objects.validator(request.POST)

    if len(errors) > 0:

        for key, value in errors.items():
            messages.error(request, value)

        return redirect('/dashboard')

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

    if request.method == "POST":
        form = LoginForm(request.post)
        if form.is_valid():
            user = User.objects.filter(email=request.POST['email'])

            if user:

                logged_user = user[0]

                if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                    request.session['userid'] = logged_user.id

                    return redirect('/dashboard')

                else:
                    form = LoginForm()

                    return redirect('/')


def dashboard(request):
    user_id = request.session.get('userid')
    user = User.objects.get(id=user_id)
    context = {"user": user}
    return render(request, "dashboard.html", context)
