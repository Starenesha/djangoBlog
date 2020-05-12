from django.shortcuts import render

# Create your views here.
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

from .forms import SignUpForm, LoginForm
from .models import User


def verify(request, uuid):
    try:
        user = User.objects.get(verification_uuid=uuid, is_verified=False)
    except User.DoesNotExist:
        raise Http404("User does not exist or is already verified")

    user.is_verified = True
    user.save()
    return redirect('home')


def signup_view(request):
    form = SignUpForm(request.POST)
    print(form.errors)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        user.email = form.cleaned_data.get('email')
        user.save()

        password = form.cleaned_data.get('password1')
        user = authenticate(email=user.email, password=password)
        login(request, user)
        return redirect('home')
    else:
        form = SignUpForm(request.POST)
    return render(request, 'Signup.html', {'form': form})


def loginUser(request):
    form = LoginForm(request.POST or None)

    context = {
        "form":form
    }

    if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        user = authenticate(email = email, password = password)

        if user is None:
            messages.info(request, "User does not exist")
            return render(request, "login.html",context)

        messages.success(request,"Hello, {}!".format(user.first_name))
        login(request,user)
        return redirect("home")
    return render(request,"login.html", context)


def logoutUser(request):
    logout(request)
    messages.success(request, "You are log out")
    return redirect("home")
