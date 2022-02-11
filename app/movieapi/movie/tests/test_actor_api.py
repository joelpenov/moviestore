import email
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from core.models import Actor

from rest_framework import status
from rest_framework.test import APIClient
from movie.serializers import ActorSerializer


ACTOR_API_URL = reverse("movie:actor-list")

class PublicActorApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        respose = self.client.get(ACTOR_API_URL)

        self.assertEqual(respose.status_code, status.HTTP_401_UNAUTHORIZED)

class   PrivateActorApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            name="Generic Login User",
            email = "auth@user.com",
            password = "mypass14"
        )

        self.client.force_authenticate(user = self.user)

    def test_retrieve_actor_list(self):
        Actor.objects.create(name="Brad", last_name="Pitt", user=self.user)
        Actor.objects.create(name="Al", last_name="Pacino", user=self.user)

        response = self.client.get(ACTOR_API_URL)

        actors = Actor.objects.all().order_by("-name")
        serializer = ActorSerializer(actors, many = True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    def test_retrieve_only_current_user_actors(self):
        
        second_user = get_user_model().objects.create_user(
            email="second@user.com",
            password="asa7sa5",
            name = "Second User Name"
        )

        Actor.objects.create(name="Brad", last_name="Pitt", user=self.user)
        Actor.objects.create(name="Al", last_name="Pacino", user=second_user)

        response = self.client.get(ACTOR_API_URL)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"],"Brad")


    def test_create_actor_successfully(self):
        payload = {"name":"Anderson", "last_name":"Cooper"}

        response = self.client.post(ACTOR_API_URL, payload)

        exists = Actor.objects.filter(name=payload["name"]).exists()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_create_actor_invalid_data(self):
        payload = {"name":"Anderson", "last_name":""}

        response = self.client.post(ACTOR_API_URL, payload) 

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    