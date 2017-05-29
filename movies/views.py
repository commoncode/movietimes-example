from django.http import JsonResponse, HttpResponseBadRequest

from .models import Movie


def best_movies(request):
    if request.method.upper() != 'GET':
        return HttpResponseBadRequest()

    movie_titles_list = []
    for movie in Movie.objects.all():
        movie_titles_list.append(movie.title)

    return JsonResponse(movie_titles_list, safe=False)
