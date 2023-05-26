from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.view_listing, name="view_listing"),
    path("watchlist/<int:listing_id>", views.manipulateWatchlist, name="manipulate_watchlist"),
    path("closeListing/<int:listing_id>", views.close_listing, name="close_listing"),
    path("bid/<int:listing_id>", views.bid, name="place_bid"),
    path("comment/<int:listing_id>", views.comment, name="place_comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories/<str:category>", views.categories, name="view_category"),
    path("allCategories", views.allCategories, name="all_categories")
]
