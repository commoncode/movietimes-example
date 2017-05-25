from django.test import TestCase

from .factories import ActorFactory, MovieFactory
from .models import Movie


class FactoryTestCase(TestCase):

    def test_creating_movies(self):
        movie = MovieFactory()
        self.assertTrue(movie.rating < 10)
        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(Movie.objects.all()[0], movie)

    def test_movie_with_actors(self):
        # generate three actors and store them in a list
        actors = [ActorFactory() for _ in range(3)]
        movie = MovieFactory(actors=actors)
        self.assertEqual(len(movie.actors.all()), 3)

        for actor in actors:
            self.assertEqual(actor.movies.all()[0], movie)
