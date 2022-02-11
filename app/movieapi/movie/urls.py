from django.urls import path, include
from rest_framework.routers import DefaultRouter

from movie import views

router = DefaultRouter()
router.register("tag", views.TagViewSet, basename="tag")
router.register("actor", views.ActorViewSet, basename="actor")

app_name = "movie"

urlpatterns = [
    path("", include(router.urls), name="tag-list")
]