from django.urls.conf import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/login', views.login_view, name="login"),
    path('auth/register', views.register_view, name="register"),
    path('auth/logout', views.logout_view, name="logout"),
    path('recent/', views.view_recent_tracks, name="view_recent_tracks"),
    path('search/', views.view_search, name="view_search"),

    path('api/get_search_result', views.get_search_results, name="get_search_results"),
    path('api/track/<int:track_id>', views.get_track, name="get_track"),
    path('api/generate_from_prompt', views.generate_from_prompt, name='generate_from_prompt'),
    path('api/get_recent_tracks', views.get_recent_tracks, name='get_recent_tracks'),
]