from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import (
    CustomUserCreationForm,
    CustomerUserProfileForm,
    TheatreUserProfileForm,
    CustomUserLoginForm,
)
from django.contrib.auth import logout
from .models import CustomUser, CustomerUserProfile, TheatreUserProfile


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = "customer"

            if user_type == "customer":
                CustomerUserProfile.objects.create(user=user)
            elif user_type == "theatre":
                TheatreUserProfile.objects.create(user=user)

            # Log the user in after registration
            login(request, user)
            return redirect("home")  # Replace 'home' with the name of your home view

    else:
        form = CustomUserCreationForm()

    return render(request, "users/register.html", {"form": form})


def custom_login(request):
    if request.method == "POST":
        form = CustomUserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(
                    "home"
                )  # Replace 'home' with the name of your home view

    else:
        form = CustomUserLoginForm()

    return render(request, "users/login.html", {"form": form})


def custom_logout(request):
    logout(request)
    return redirect("home")  # Replace 'home' with the name of your home view
