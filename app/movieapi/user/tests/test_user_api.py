from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")
USER_TOKEN = reverse("user:token")

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_create_valid_user_success(self):
        payload = {
            "email":"sample@user.com",
            "password":"q3552ff",
            "name": "Test User Name"
        }

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", response.data)
    
    def test_create_user_if_already_exists(self):
        payload = {
            "email": "sample@user.com",
            "password": "sdsdsd545f",
            "name": "Test User Name 1"
        }

        create_user(**payload)

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        payload = {
            "email": "sample@user.com",
            "password": "5s",
            "name": "Test User Name 1"
        }

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
                email=payload["email"]
                ).exists()
        self.assertFalse(user_exists)
    
    def test_create_token_for_user(self):
        payload = {"email":"admin@user.com", "password":"thetrick25"}
        create_user(**payload)
        response = self.client.post(USER_TOKEN, payload)

        self.assertIn("token", response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        email = "admin@user.com"
        create_user(email=email, password="validpass55")
        payload = {"email": email, "password": "invalid545"}
        response = self.client.post(USER_TOKEN, payload)

        self.assertNotIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        payload = {"email": "admin@user.com", "password": "test4454"}
        response = self.client.post(USER_TOKEN, payload)

        self.assertNotIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        payload = {"email": "admin", "password": ""}
        response = self.client.post(USER_TOKEN, payload)

        self.assertNotIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
