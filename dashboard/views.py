from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from movies.models import Movie
from ticketbooking.models import screen, show
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib import messages


class index(ListView):
    model = Movie
    template_name = "dashboard/index.html"
    context_object_name = "movies"
    ordering = ["-release_date"]


def dashboard(request):
    if request.user.is_authenticated:
        try:
            if hasattr(request.user, "theatre_profile"):
                theatre_profile = request.user.theatre_profile
                theatre_name = theatre_profile.name
                num_of_screens = screen.objects.filter(theatre=theatre_profile).count()
                screens = screen.objects.filter(theatre=theatre_profile)
                shows = show.objects.filter(screen__theatre=theatre_profile)
                movies = Movie.objects.all()
                return render(
                    request,
                    "dashboard/theatre_dashboard.html",
                    {
                        "num_of_screens": num_of_screens,
                        "theatre_profile": theatre_profile,
                        "theatre_name": theatre_name,
                        "screens": screens,
                        "shows": shows,
                        "movies": movies,
                    },
                )
            elif hasattr(request.user, "customer_profile"):
                return render(request, "dashboard/customer_dashboard.html")
            else:
                return redirect("home")
        except Exception as e:
            print(f"Error checking user profile: {e}")
            return redirect("home")
    else:
        return redirect("login")


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


class MovieBrowseView(ListView):
    model = Movie
    template_name = "dashboard/browse_movies.html"
    context_object_name = "movies"
    paginate_by = 10
    ordering = ["-release_date"]


@login_required
def book_ticket(request, show_id):
    show_instance = get_object_or_404(show, id=show_id)
    available_seats = show_instance.screen.available_seats

    if request.method == "POST":
        form = TicketBookingForm(request.POST, show_instance=show_instance)
        if form.is_valid():
            num_of_seats = form.cleaned_data["num_of_seats"]

            if num_of_seats > available_seats:
                form.add_error("num_of_seats", "Not enough seats available.")
            else:
                # Create the ticket and update available seats
                ticket_instance = ticket.objects.create(
                    show=show_instance,
                    user=request.user.customer_profile,  # Assuming only customers can book tickets
                    num_of_seats=num_of_seats,
                    status="Booked",
                )
                # Update the available seats
                show_instance.screen.available_seats -= num_of_seats
                show_instance.screen.save()

                messages.success(request, "Ticket booked successfully!")
                return redirect("booking_confirmation", ticket_id=ticket_instance.id)

    else:
        form = TicketBookingForm(show_instance=show_instance)

    return render(
        request,
        "ticketbooking/book_ticket.html",
        {
            "form": form,
            "show": show_instance,
            "available_seats": available_seats,
        },
    )


@login_required
def booking_confirmation(request, ticket_id):
    ticket_instance = get_object_or_404(
        ticket, id=ticket_id, user=request.user.customer_profile
    )
    return render(
        request,
        "ticketbooking/booking_confirmation.html",
        {
            "ticket": ticket_instance,
        },
    )
