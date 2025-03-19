from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>/", views.listing_view, name="listing"),
    path("listing/<int:listing_id>/bid/", views.submit_bid, name="submit_bid"),
    path("listing/<int:listing_id>/comment/", views.submit_comment, name="submit_comment"),
    path("listing/<int:listing_id>/close/", views.close_auction, name="close_auction"),
    path("toggle_watchlist/<int:listing_id>", views.toggle_watchlist, name="toggle_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories_view, name="categories"),
    path("category/<int:category_id>/", views.category_listings_view, name="category_listings"),
]
