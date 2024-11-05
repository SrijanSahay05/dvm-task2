from django.shortcuts import render, redirect, get_object_or_404
from .forms import ScreenForm, ShowForm, TicketBookingForm
from django.views.generic import UpdateView
from .models import screen, show, ticket
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .forms import TicketBookingForm
from django.contrib import messages


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


@login_required
def book_ticket(request, show_id):
    show_instance = get_object_or_404(show, id=show_id)

    if request.method == "POST":
        form = TicketBookingForm(request.POST)
        if form.is_valid():
            new_ticket = form.save(commit=False)
            new_ticket.show = show_instance
            new_ticket.user = (
                request.user.customer_profile
            )  # Assumes only customers can book tickets
            new_ticket.save()
            messages.success(request, "Ticket booked successfully!")
            return redirect("home")
    else:
        form = TicketBookingForm()

    return render(
        request, "ticketbooking/book_ticket.html", {"form": form, "show": show_instance}
    )


@login_required
def book_ticket(request, show_id):
    show_instance = get_object_or_404(show, id=show_id)

    if request.method == "POST":
        form = TicketBookingForm(request.POST)
        if form.is_valid():
            num_of_seats = form.cleaned_data["num_of_seats"]

            if num_of_seats > show_instance.available_seats:
                form.add_error("num_of_seats", "Not enough seats available.")
            else:
                # Create a new ticket
                ticket_instance = ticket.objects.create(
                    show=show_instance,
                    user=request.user.customer_profile,  # Assuming only customers can book tickets
                    num_of_seats=num_of_seats,
                    status="Booked",
                )

                # Update available seats
                show_instance.available_seats -= num_of_seats
                show_instance.save()

                messages.success(request, "Ticket booked successfully!")
                return redirect("booking-confirmation", ticket_id=ticket_instance.id)
    else:
        form = TicketBookingForm()

    return render(
        request, "ticketbooking/book_ticket.html", {"form": form, "show": show_instance}
    )


@login_required
def booking_confirmation(request, ticket_id):
    ticket_instance = get_object_or_404(
        ticket, id=ticket_id, user=request.user.customer_profile
    )
    return render(
        request, "ticketbooking/booking_confirmation.html", {"ticket": ticket_instance}
    )
