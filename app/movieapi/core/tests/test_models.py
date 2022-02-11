from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models

def get_sample_user(email="some@name.com", password="mypasswrod4"):
    return get_user_model().objects.create_user(email=email, password=password)

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
    
    def test_tag_str(self):
        tag = models.Tag.objects.create(
            name="Netflix",
            user=get_sample_user()
        )

        self.assertEqual(str(tag), tag.name)
    
    def test_actor_str(self):
        actor = models.Actor.objects.create(
            name= "Eugenio",
            last_name="Derbez",
            user= get_sample_user()
        )

        self.assertEqual(str(actor), f"{actor.name} {actor.last_name}")
    
    def test_str_movie_model(self):

        movie = models.Movie.objects.create(
            title= "La vita è bella",
            release_date = "1999-02-21",
            running_time = 116,
            user = get_sample_user()
        )

        self.assertEqual(str(movie), f"{movie.title} ({str(movie.release_date)}: {str(movie.running_time)} minutes)")
