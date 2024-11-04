from django.urls import path
from . import views as dashboard_view
import users.views as user_view

urlpatterns = [
    path("", dashboard_view.index.as_view(), name="home"),
    path("dashboard/", dashboard_view.dashboard, name="theatre-dashboard"),
    path("register/", user_view.register, name="register"),
    path("login/", user_view.custom_login, name="login"),
    path("logout/", user_view.custom_logout, name="logout"),
]
