from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction

from .forms import ScreenForm, ShowForm, TicketBookingForm
from .models import screen, show, ticket
from transactions.models import Wallet, Transactions
from transactions.views import make_payment
from datetime import timedelta


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


@login_required
def add_show(request):
    if request.user.is_authenticated and hasattr(request.user, "theatre_profile"):
        if request.method == "POST":
            form = ShowForm(request.POST)
            if form.is_valid():
                new_show = form.save(commit=False)

                # Calculate end time using movie duration
                start_time = new_show.show_time
                end_time = start_time + timedelta(minutes=new_show.movie.duration)

                # Check for overlapping shows on the same screen
                conflicting_shows = show.objects.filter(
                    screen=new_show.screen,
                    show_time__lt=end_time,  # Show start time is before new show end time
                    show_time__gt=start_time
                    - timedelta(
                        minutes=new_show.movie.duration
                    ),  # Show end time is after new show start time
                )

                if conflicting_shows.exists():
                    form.add_error(
                        "show_time",
                        "This screen is already booked for another show at the selected time.",
                    )
                else:
                    # Initialize available seats based on screen's total seats
                    new_show.available_seats = new_show.screen.total_seats
                    new_show.save()
                    return redirect("theatre-dashboard")
        else:
            form = ShowForm()

        return render(request, "ticketbooking/add_show.html", {"form": form})
    else:
        return redirect("login")


@login_required
def edit_show(request, show_id):
    show_instance = get_object_or_404(show, id=show_id)

    if request.method == "POST":
        form = ShowForm(request.POST, instance=show_instance)
        if form.is_valid():
            updated_show = form.save(commit=False)

            # Calculate the end time with updated start time and movie duration
            start_time = updated_show.show_time
            end_time = start_time + timedelta(minutes=updated_show.movie.duration)

            # Exclude the current show instance from the conflict check
            conflicting_shows = show.objects.filter(
                screen=updated_show.screen,
                show_time__lt=end_time,
                show_time__gt=start_time
                - timedelta(minutes=updated_show.movie.duration),
            ).exclude(id=show_id)

            if conflicting_shows.exists():
                form.add_error(
                    "show_time",
                    "This screen is already booked for another show at the selected time.",
                )
            else:
                updated_show.save()
                return redirect("theatre-dashboard")
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


# Booking function with atomic transaction handling
@login_required
def book_ticket(request, show_id):
    show_instance = get_object_or_404(show, id=show_id)
    customer_wallet = Wallet.objects.get(user=request.user)
    theatre_wallet = Wallet.objects.get(user=show_instance.screen.theatre.user)

    if request.method == "POST":
        form = TicketBookingForm(request.POST)
        if form.is_valid():
            num_of_seats = form.cleaned_data["num_of_seats"]
            total_price = show_instance.price * num_of_seats

            if num_of_seats > show_instance.available_seats:
                form.add_error("num_of_seats", "Not enough seats available.")
            else:
                with transaction.atomic():
                    # Call make_payment and capture the transaction record if successful
                    transaction_record = make_payment(
                        customer_wallet,
                        theatre_wallet,
                        total_price,
                        transaction_type="ticket_booking",
                        description=f"Ticket booking for {show_instance.movie.title} ({num_of_seats} seats)",
                    )

                    if transaction_record:
                        # Create the ticket instance if payment was successful
                        ticket_instance = ticket.objects.create(
                            show=show_instance,
                            user=request.user.customer_profile,
                            num_of_seats=num_of_seats,
                            status="Booked",
                        )

                        # Update available seats
                        show_instance.available_seats -= num_of_seats
                        show_instance.save()

                        messages.success(request, "Ticket booked successfully!")
                        return redirect(
                            "booking-confirmation", ticket_id=ticket_instance.id
                        )
                    else:
                        # Handle the case where payment was unsuccessful
                        messages.error(request, "Insufficient funds in your wallet.")
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
