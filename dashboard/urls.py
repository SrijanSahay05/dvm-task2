from django.urls import path
from . import views as dashboard_view
import users.views as user_view
import ticketbooking.views as ticketbooking_view

urlpatterns = [
    path("", dashboard_view.index.as_view(), name="home"),
    path("dashboard/", dashboard_view.dashboard, name="theatre-dashboard"),
    path(
        "browse-movies/", dashboard_view.MovieBrowseView.as_view(), name="browse-movies"
    ),
    path("register/", user_view.register, name="register"),
    path("login/", user_view.custom_login, name="login"),
    path("logout/", user_view.custom_logout, name="logout"),
    path("dashboard/add-screen/", ticketbooking_view.add_screen, name="add-screen"),
    path("dashboard/add-show/", ticketbooking_view.add_show, name="add-show"),
    path(
        "dashboard/edit-screen/<int:screen_id>/",
        ticketbooking_view.edit_screen,
        name="edit_screen",
    ),
    path(
        "dashboard/edit-show/<int:show_id>/",
        ticketbooking_view.edit_show,
        name="edit_show",
    ),
    path("dashboard/add-movie/", dashboard_view.add_movie, name="add-movie"),
    path("profile/", user_view.profile, name="profile"),
    path(
        "delete-screen/<int:screen_id>/",
        ticketbooking_view.delete_screen,
        name="delete_screen",
    ),
    path(
        "delete-show/<int:show_id>/", ticketbooking_view.delete_show, name="delete_show"
    ),
    path(
        "movie/<int:pk>/", dashboard_view.MovieDetailView.as_view(), name="movie-detail"
    ),
    path(
        "book-ticket/<int:show_id>/", ticketbooking_view.book_ticket, name="book-ticket"
    ),
    path(
        "booking-confirmation/<int:ticket_id>/",
        ticketbooking_view.booking_confirmation,
        name="booking-confirmation",
    ),
]
