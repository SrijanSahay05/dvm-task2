from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import (
    CustomUserCreationForm,
    CustomerUserProfileForm,
    TheatreUserProfileForm,
    CustomUserLoginForm,
)
from django.contrib.auth import logout
from .models import CustomUser, CustomerUserProfile, TheatreUserProfile
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


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


@login_required
def profile(request):
    user = request.user

    if hasattr(user, "customer_profile"):
        profile = user.customer_profile
        form = CustomerUserProfileForm(instance=profile)

        if request.method == "POST":
            form = CustomerUserProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                return redirect("profile")

        return render(
            request,
            "users/profile.html",
            {
                "form": form,
                "user_type": "Customer",
            },
        )

    elif hasattr(user, "theatre_profile"):
        profile = user.theatre_profile
        form = TheatreUserProfileForm(instance=profile)

        if request.method == "POST":
            form = TheatreUserProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                return redirect("profile")

        return render(
            request,
            "users/profile.html",
            {
                "form": form,
                "user_type": "Theatre",
            },
        )

    else:
        raise PermissionDenied("Profile not found.")
