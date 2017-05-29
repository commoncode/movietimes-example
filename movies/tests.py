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


class BestMoviesTestCase(TestCase):

    def test_best_movies_returns_a_list_of_movie_titles(self):
        # create 5 random movies
        movies = [MovieFactory() for _ in range(140)]
        movie_titles = [m.title for m in movies]

        response = self.client.get('/movies/best/')
        response_json = response.json()

        for movie_title in movie_titles:
            self.assertIn(movie_title, response_json)

        for movie_title in response_json:
            self.assertIn(movie_title, movie_titles)

        self.assertEqual(len(movies), len(response_json))

    def test_best_movies_returns_a_list(self):
        response = self.client.get('/movies/best/')
        response_json = response.json()
        self.assertIsInstance(response_json, list)

    def test_get_best_movies_url(self):
        response = self.client.get('/movies/best/')
        self.assertEqual(response.status_code, 200)

    def test_best_movies_returns_json(self):
        response = self.client.get('/movies/best/')
        self.assertEqual(response['content-type'], 'application/json')

    def test_non_get_requests_return_400(self):
        response = self.client.post('/movies/best/')
        self.assertEqual(response.status_code, 400)

        response = self.client.put('/movies/best/')
        self.assertEqual(response.status_code, 400)

        response = self.client.delete('/movies/best/')
        self.assertEqual(response.status_code, 400)

        response = self.client.patch('/movies/best/')
        self.assertEqual(response.status_code, 400)

        response = self.client.head('/movies/best/')
        self.assertEqual(response.status_code, 400)
