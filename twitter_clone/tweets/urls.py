from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.tweet_create, name="tweet_create"),

    path("edit/<int:tweet_id>/", views.tweet_edit, name="tweet_edit"),
    path("delete/<int:tweet_id>/", views.tweet_delete, name="tweet_delete"),
    
    path("<int:tweet_id>/", views.tweet_detail, name="tweet_detail"),
    path("register/", views.register, name="register"),
    path("login/", LoginView.as_view(template_name='registration/login.html'), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]