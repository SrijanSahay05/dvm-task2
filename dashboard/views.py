from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from movies.models import Movie


class index(ListView):
    model = Movie
    template_name = "dashboard/index.html"
    context_object_name = "movies"
    ordering = ["-release_date"]


def dashboard(request):
    if request.user.is_authenticated:
        try:
            if hasattr(request.user, "theatre_profile"):
                return render(request, "dashboard/theatre_dashboard.html")
            elif hasattr(request.user, "customer_profile"):
                return render(request, "dashboard/customer_dashboard.html")
            else:
                return redirect("home")
        except Exception as e:
            print(f"Error checking user profile: {e}")
            return redirect("home")
    else:
        return redirect("login")
