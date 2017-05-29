from django.test import TestCase
from django.core.urlresolvers import reverse

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


class PaginatedMovieTestCase(TestCase):

    def test_url_without_page_returns_most_recent(self):

        [MovieFactory() for _ in range(140)]
        movies = Movie.objects.all().order_by('-release_date', 'title')[:5]
        movie_titles = [m.title for m in movies]

        response_page1 = self.client.get(reverse('movies:recent-movies')+'?page=').json()
        self.assertListEqual(response_page1, movie_titles)

        response_page2 = self.client.get(reverse('movies:recent-movies')).json()
        self.assertListEqual(response_page2, movie_titles)

    def test_url_with_page_offsets_to_correct_page(self):

        [MovieFactory() for _ in range(140)]
        movies = Movie.objects.all().order_by('-release_date', 'title')[20:25]
        movie_titles = [m.title for m in movies]

        response_page = self.client.get(reverse('movies:recent-movies')+'?page=5').json()
        self.assertListEqual(response_page, movie_titles)

    def test_url_with_page_out_of_range_display_404(self):

        [MovieFactory() for _ in range(100)]

        response = self.client.get(reverse('movies:recent-movies')+'?page=21')
        self.assertEqual(response.status_code, 404)


class RecentMoviesTestCase(TestCase):

    def test_max_number_of_movies_returned_are_5(self):

        [MovieFactory() for _ in range(10)]
        response = self.client.get(reverse('movies:recent-movies'))
        response_json = response.json()
        self.assertLessEqual(len(response_json), 5)

        [MovieFactory() for _ in range(3)]
        response = self.client.get(reverse('movies:recent-movies'))
        response_json = response.json()
        self.assertLessEqual(len(response_json), 5)

    def test_recent_movies_returned_having_same_ratings_are_sorted_by_title(self):

        movies = [
            MovieFactory(release_date='2013-01-05'),
            MovieFactory(release_date='2014-02-27', title='Spiderman'),
            MovieFactory(release_date='2014-03-15', title='Superman'),
            MovieFactory(release_date='2015-08-23'),
            MovieFactory(release_date='2017-02-05'),
        ]
        movie_titles = [m.title for m in reversed(movies)]

        response = self.client.get(reverse('movies:recent-movies'))
        response_json = response.json()

        self.assertListEqual(movie_titles, response_json)

    def test_recent_movies_returned_are_sorted_by_ratings(self):

        movies = [
            MovieFactory(release_date='2013-01-05'),
            MovieFactory(release_date='2014-02-27'),
            MovieFactory(release_date='2014-03-15'),
            MovieFactory(release_date='2015-08-23'),
            MovieFactory(release_date='2017-02-05'),
        ]
        movie_titles = [m.title for m in reversed(movies)]

        response = self.client.get(reverse('movies:recent-movies'))
        response_json = response.json()

        self.assertListEqual(movie_titles, response_json)

    def test_recent_movies_returns_a_list_of_movie_titles(self):

        movies = [MovieFactory() for _ in range(5)]
        movie_titles = [m.title for m in movies]

        response = self.client.get(reverse('movies:recent-movies'))
        response_json = response.json()

        for movie_title in movie_titles:
            self.assertIn(movie_title, response_json)

        for movie_title in response_json:
            self.assertIn(movie_title, movie_titles)

    def test_recent_movies_returns_a_list(self):
        response = self.client.get(reverse('movies:recent-movies'))
        response_json = response.json()
        self.assertIsInstance(response_json, list)

    def test_recent_movies_returns_json(self):
        response = self.client.get(reverse('movies:recent-movies'))
        self.assertEqual(response['content-type'], 'application/json')

    def test_non_get_requests_return_400(self):
        response = self.client.post(reverse('movies:recent-movies'))
        self.assertEqual(response.status_code, 400)

        response = self.client.put(reverse('movies:recent-movies'))
        self.assertEqual(response.status_code, 400)

        response = self.client.delete(reverse('movies:recent-movies'))
        self.assertEqual(response.status_code, 400)

        response = self.client.patch(reverse('movies:recent-movies'))
        self.assertEqual(response.status_code, 400)

        response = self.client.head(reverse('movies:recent-movies'))
        self.assertEqual(response.status_code, 400)

    def test_get_best_movies_url(self):
        response = self.client.get(reverse('movies:recent-movies'))
        self.assertEqual(response.status_code, 200)


class BestMoviesTestCase(TestCase):

    def test_no_pagination(self):

        [MovieFactory() for _ in range(140)]

        response_page1 = self.client.get(reverse('movies:best-movies')+'?page=1').json()
        response_page2 = self.client.get(reverse('movies:best-movies')+'?page=2').json()

        self.assertListEqual(response_page1, response_page2)

    def test_max_number_of_movies_returned_are_5(self):

        [MovieFactory() for _ in range(10)]
        response = self.client.get(reverse('movies:best-movies'))
        response_json = response.json()
        self.assertLessEqual(len(response_json), 5)

        [MovieFactory() for _ in range(3)]
        response = self.client.get(reverse('movies:best-movies'))
        response_json = response.json()
        self.assertLessEqual(len(response_json), 5)

    def test_best_movies_returned_having_same_ratings_are_sorted_by_title(self):

        movies = [
            MovieFactory(rating=5),
            MovieFactory(rating=6),
            MovieFactory(rating=7, title='Superman'),
            MovieFactory(rating=7, title='Spiderman'),
            MovieFactory(rating=9),
        ]
        movie_titles = [m.title for m in reversed(movies)]

        response = self.client.get(reverse('movies:best-movies'))
        response_json = response.json()

        self.assertListEqual(movie_titles, response_json)

    def test_best_movies_returned_are_sorted_by_ratings(self):

        movies = [
            MovieFactory(rating=5),
            MovieFactory(rating=6),
            MovieFactory(rating=7),
            MovieFactory(rating=8),
            MovieFactory(rating=9),
        ]
        movie_titles = [m.title for m in reversed(movies)]

        response = self.client.get(reverse('movies:best-movies'))
        response_json = response.json()

        self.assertListEqual(movie_titles, response_json)

    def test_best_movies_returns_a_list_of_movie_titles(self):

        movies = [MovieFactory() for _ in range(5)]
        movie_titles = [m.title for m in movies]

        response = self.client.get(reverse('movies:best-movies'))
        response_json = response.json()

        for movie_title in movie_titles:
            self.assertIn(movie_title, response_json)

        for movie_title in response_json:
            self.assertIn(movie_title, movie_titles)

    def test_best_movies_returns_a_list(self):
        response = self.client.get(reverse('movies:best-movies'))
        response_json = response.json()
        self.assertIsInstance(response_json, list)

    def test_get_best_movies_url(self):
        response = self.client.get(reverse('movies:best-movies'))
        self.assertEqual(response.status_code, 200)

    def test_best_movies_returns_json(self):
        response = self.client.get(reverse('movies:best-movies'))
        self.assertEqual(response['content-type'], 'application/json')

    def test_non_get_requests_return_400(self):
        response = self.client.post(reverse('movies:best-movies'))
        self.assertEqual(response.status_code, 400)

        response = self.client.put(reverse('movies:best-movies'))
        self.assertEqual(response.status_code, 400)

        response = self.client.delete(reverse('movies:best-movies'))
        self.assertEqual(response.status_code, 400)

        response = self.client.patch(reverse('movies:best-movies'))
        self.assertEqual(response.status_code, 400)

        response = self.client.head(reverse('movies:best-movies'))
        self.assertEqual(response.status_code, 400)
