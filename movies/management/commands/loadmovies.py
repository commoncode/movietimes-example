import os
import time

import requests

from django.core.management.base import BaseCommand
from movies.models import Movie, Actor


API_KEY = os.environ['TVDB_KEY']
TMDB_BASE = 'https://api.themoviedb.org/3/'


class Command(BaseCommand):

    def handle(self, *args, **options):
        for x in range(1, 11):
            response = requests.get(TMDB_BASE + 'discover/movie', {
                'api_key': API_KEY,
                'sort_by': 'popularity.desc',
                'page': x
            })
            movies_json = response.json()

            for m in movies_json['results']:
                print(m)
                movie, _ = Movie.objects.get_or_create(
                    title=m['title'],
                    release_date=m['release_date']
                )
                movie.rating = m['vote_average']
                movie.save()
                print(movie)

                response = requests.get(TMDB_BASE + 'movie/{}/credits'.format(m['id']), {
                    'api_key': API_KEY,
                })
                cast_json = response.json()

                for c in cast_json['cast']:
                    a, _ = Actor.objects.get_or_create(name=c['name'])
                    movie.actors.add(a)
                    print(a)
                time.sleep(2)
