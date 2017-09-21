from django.conf.urls import url
from django.contrib import admin

from movies.views import best_movies


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^movies/best/', best_movies, name="best-movies"),
]
