from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            validation_message = f"You must set a value email address for the user. Invalid email is '{email}'"
            raise ValueError(validation_message)

        normalized_email = self.normalize_email(email).lower()
        user = self.model(email=normalized_email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.TextField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Tag(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE
    )

    def __str__(self):
        return self.name

class Actor(models.Model):
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)

    def __str__ (self):
        return f"{self.name} {self.last_name}"


class Movie(models.Model):
    title= models.CharField(max_length=200)
    release_date = models.DateField()
    running_time = models.PositiveIntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    tags = models.ManyToManyField("Tag")
    actors = models.ManyToManyField("Actor")

    def __str__(self):
        return f"{self.title} ({str(self.release_date)}: {str(self.running_time)} minutes)"