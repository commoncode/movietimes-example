import pytest


@pytest.mark.django_db
def test_get_best_movies_url(client):
    response = client.get('/movies/best/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_best_movies_returns_json(client):
    response = client.get('/movies/best/')
    assert response['content-type'] == 'application/json'
