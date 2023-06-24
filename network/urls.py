
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post", views.create_post, name="create_post"),
    path("view_posts", views.view_posts, name="view_posts"),
    path("follow/<int:user_id>", views.set_follow_status, name="set_follow_status"),
    path("profile/<int:user_id>", views.view_profile, name="view_profile"),
    path("view_posts_by_user/<int:user_id>", views.view_posts_by_user, name="view_posts_by_user"),
    path("following", views.view_following, name="view_following"),
    path("get_following_posts", views.get_following_posts, name="get_following_posts"),
    path("update_post/<int:post_id>", views.update_post, name="update_post"),
    path("like/<int:post_id>", views.set_like_status, name="update_like_status"),
]
