from unittest import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from core.models import Movie
from movie.serializers import MovieSerializer

MOVIE_API_URL = reverse("movie:movie-list")

def create_default_movie(user, **params):
    defaults = {
        "title":"Avatar",
        "release_date" : "2009-12-10",
        "running_time": 162
    }

    defaults.update(params)

    return Movie.objects.create(
        user= user,
        **defaults
    )

class PublicMovieApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_requires_authentication(self):
        create_default_movie(self.user)
        create_default_movie(self.user, title = "Casablanca")
        response = self.client.get(MOVIE_API_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMovieApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@user.com",
            name="Test User Name",
            password = "TestPass227"
        )

        create_default_movie(self.user)

        self.cleint.force_authenticate(self.user)
        self.cleint.force_authenticate(self.user, "The Godfather")

    
    def test_retrieve_movie_list(self):

        response = self.client.get(MOVIE_API_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)