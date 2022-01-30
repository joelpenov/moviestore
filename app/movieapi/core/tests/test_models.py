from django.test import TestCase
from django.contrib.auth import get_user_model


class TestModels(TestCase):
    def test_the_user_is_created_successfully_using_email(self, **args):
        email = "sample@django.com"
        password = "secretpassword2"

        user = get_user_model().objects.create_user(email=email, **args)
        user.set_password(password)

        self.assertEqual(email, user.email)
        self.assertTrue(user.check_password(password))

    def test_email_is_normalized(self):
        email = "SAMPLE@EMAIL.COM"
        objects = get_user_model().objects
        user = objects.create_user(email=email, password='whatever')

        self.assertEqual(email.lower(), user.email)

    def test_invalid_email_raises_an_error(self):
        with self.assertRaises(ValueError):
            objects = get_user_model().objects
            objects.create_user(email=None, password='whatever')

    def test_superuser_is_created_successfully(self):
        user = get_user_model().objects.create_superuser(
            "admina@django.com",
            'test1234'
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
