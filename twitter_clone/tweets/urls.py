from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.tweet_create, name="tweet_create"),

    path("edit/<int:tweet_id>/", views.tweet_edit, name="tweet_edit"),
    path("delete/<int:tweet_id>/", views.tweet_delete, name="tweet_delete"),
    
    path("<int:tweet_id>/", views.tweet_detail, name="tweet_detail"),
]