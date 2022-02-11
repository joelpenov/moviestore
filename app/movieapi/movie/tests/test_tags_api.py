from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from core.models import Tag

from rest_framework import status
from rest_framework.test import APIClient
from movie.serializers import TagSerializer

TAGS_API_URL = reverse("movie:tag-list")

class PublicTagApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_unauthenticated_user_return_non_authorized(self):
        response = self.client.get(TAGS_API_URL)
    
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagApiTests(TestCase):
   
    def setUp(self):
        email = "sample@email.com"
        password = "easypass35"

        self.client = APIClient()

        self.user = get_user_model().objects.create_user(
            email= email,
            password= password,
            name="Authenticated User Name"
        )

        self.client.force_authenticate(user=self.user)
    
    def test_retrieve_tags(self):
        Tag.objects.create(user=self.user, name="Adult")
        Tag.objects.create(user=self.user, name="Kids")

        response = self.client.get(TAGS_API_URL)

        tags = Tag.objects.all().order_by("-name")
        serializer = TagSerializer(tags, many= True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(serializer.data, response.data)
    
    def test_retrieve_is_limited_to_current_user(self):
        other_user = get_user_model().objects.create_user(
            email ="another@user.com",
            password = "alkd5200",
            name = "Fake Second User"
        )

        Tag.objects.create(name = "Jungle",user = self.user)
        Tag.objects.create(name = "Animals",user = other_user)

        response = self.client.get(TAGS_API_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Jungle")

    def test_tag_created_successfully(self):
        payload = {"name":"Forest"}

        response = self.client.post(TAGS_API_URL, payload)

        exists = Tag.objects.filter(
            name=payload["name"],
            user = self.user
        ).exists()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)
    
    def test_tag_with_invalid_data(self):
        payload = {"name":""}
        response = self.client.post(TAGS_API_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

