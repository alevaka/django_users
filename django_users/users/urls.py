from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "users"

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("profile/", views.profile, name="profile"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("profile/<pk>/", views.UserProfileView.as_view(), name="user_detail"),
    path("user_list/", views.UserListView.as_view(), name="user_list"),
]
