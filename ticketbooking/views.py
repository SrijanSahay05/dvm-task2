from django.shortcuts import render, redirect, get_object_or_404
from .forms import ScreenForm, ShowForm
from django.views.generic import UpdateView
from .models import screen, show
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def add_screen(request):
    if request.user.is_authenticated and hasattr(request.user, "theatre_profile"):
        theatre_profile = (
            request.user.theatre_profile
        )  # Get the current user's theatre profile

        if request.method == "POST":
            form = ScreenForm(request.POST)
            if form.is_valid():
                new_screen = form.save(commit=False)
                new_screen.theatre = theatre_profile  # Set the theatre attribute
                new_screen.save()
                return redirect(
                    "theatre-dashboard"
                )  # Replace with your desired redirect view name
        else:
            form = ScreenForm()

        return render(request, "ticketbooking/add_screen.html", {"form": form})
    else:
        return redirect("login")  # Redirect to login if not authenticated


def edit_screen(request, screen_id):
    screen_instance = get_object_or_404(screen, id=screen_id)

    if request.method == "POST":
        form = ScreenForm(request.POST, instance=screen_instance)
        if form.is_valid():
            form.save()
            return redirect("theatre-dashboard")  # Replace with your dashboard URL
    else:
        form = ScreenForm(instance=screen_instance)

    return render(
        request,
        "dashboard/edit_show_screen.html",
        {"form": form, "edit_type": "Screen"},
    )


def add_show(request):
    if request.user.is_authenticated and hasattr(request.user, "theatre_profile"):
        if request.method == "POST":
            form = ShowForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(
                    "theatre-dashboard"
                )  # Replace with your desired redirect view name
        else:
            form = ShowForm()

        return render(request, "ticketbooking/add_show.html", {"form": form})
    else:
        return redirect("login")


def edit_show(request, show_id):
    show_instance = get_object_or_404(show, id=show_id)

    if request.method == "POST":
        form = ShowForm(request.POST, instance=show_instance)
        if form.is_valid():
            form.save()
            return redirect("theatre-dashboard")  # Replace with your dashboard URL
    else:
        form = ShowForm(instance=show_instance)

    return render(
        request, "dashboard/edit_show_screen.html", {"form": form, "edit_type": "Show"}
    )


@login_required
def delete_screen(request, screen_id):
    screen_instance = get_object_or_404(screen, id=screen_id)
    if (
        hasattr(request.user, "theatre_profile")
        and request.user.theatre_profile == screen_instance.theatre
    ):
        screen_instance.delete()
        return redirect("theatre-dashboard")
    else:
        raise PermissionDenied("You do not have permission to delete this screen.")


@login_required
def delete_show(request, show_id):
    show_instance = get_object_or_404(show, id=show_id)
    if (
        hasattr(request.user, "theatre_profile")
        and request.user.theatre_profile == show_instance.screen.theatre
    ):
        show_instance.delete()
        return redirect("theatre-dashboard")
    else:
        raise PermissionDenied("You do not have permission to delete this show.")
