from django.conf.urls import url

from .views import best_movies, recent_movies

app_name = 'movies'
urlpatterns = [
    url(r'^best/', best_movies, name="best-movies"),
    url(r'^recent/', recent_movies, name="recent-movies"),
]
