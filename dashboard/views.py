from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView
from movies.models import Movie
from movies.forms import MovieAddForm
from ticketbooking.models import screen, show, ticket
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q


class index(ListView):
    model = Movie
    template_name = "dashboard/index.html"
    context_object_name = "movies"
    ordering = ["-release_date"]


class MovieDetailView(DetailView):
    model = Movie
    template_name = "dashboard/movie_detail.html"
    context_object_name = "movie"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filter future shows based on show_time
        context["future_shows"] = self.object.show_set.filter(
            show_time__gt=timezone.now()
        )
        return context


@login_required
def dashboard(request):
    if hasattr(request.user, "theatre_profile"):
        # Theater admin dashboard context
        theatre_profile = request.user.theatre_profile
        theatre_name = theatre_profile.name
        num_of_screens = screen.objects.filter(theatre=theatre_profile).count()
        screens = screen.objects.filter(theatre=theatre_profile).order_by("screen_name")
        shows = show.objects.filter(screen__theatre=theatre_profile).order_by(
            "-show_time"
        )
        movies = Movie.objects.all().order_by("-release_date")

        return render(
            request,
            "dashboard/theatre_dashboard.html",
            {
                "theatre_name": theatre_name,
                "num_of_screens": num_of_screens,
                "screens": screens,
                "shows": shows,
                "movies": movies,
            },
        )

    elif hasattr(request.user, "customer_profile"):
        # Customer dashboard context
        customer_tickets = ticket.objects.filter(user=request.user.customer_profile)

        return render(
            request,
            "dashboard/customer_dashboard.html",
            {
                "customer_tickets": customer_tickets,
            },
        )

    else:
        return redirect("home")


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

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(show__screen__theatre__name__icontains=query)
            ).distinct()
        return queryset


def add_movie(request):
    if request.method == "POST":
        form = MovieAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Movie added successfully!")
            return redirect("theatre-dashboard")
    else:
        form = MovieAddForm()
    return render(request, "dashboard/add_movie.html", {"form": form})
