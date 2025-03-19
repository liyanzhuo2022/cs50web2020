from django.urls import path

from . import views

urlpatterns = [
    path("random/", views.random_page, name="random_page"),
    path("new/", views.new_page, name="new_page"),
    path("search/", views.search, name="search"),
    path("edit/<str:title>/", views.edit_page, name="edit_page"),
    path("wiki/<str:title>/", views.entry, name="entry"),
    path("", views.index, name="index"),
]
