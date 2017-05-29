from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Movie


def best_movies(request):
    if request.method.upper() != 'GET':
        return HttpResponseBadRequest()

    movie_titles_list = []
    for movie in Movie.objects.all().order_by('-rating', 'title')[:5]:
        movie_titles_list.append(movie.title)

    return JsonResponse(movie_titles_list, safe=False)


def recent_movies(request):
    if request.method.upper() != 'GET':
        return HttpResponseBadRequest()

    paginator = Paginator(Movie.objects.all().order_by('-release_date', 'title'), 5)
    page = request.GET.get('page')

    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        return HttpResponseNotFound()

    movie_titles_list = []
    for movie in movies:
        movie_titles_list.append(movie.title)

    return JsonResponse(movie_titles_list, safe=False)
