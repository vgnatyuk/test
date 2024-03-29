from app_pets.routers import MyRouter
from app_pets.api import PetViewSet, PetImageViewSet
from django.urls import path

from app_pets.api import photo

router = MyRouter()
router.register("pets", PetViewSet)
router.register("pets_images", PetImageViewSet)

urlpatterns = [
    path("pets/<str:id>/photo/", photo, name="photo"),
] + router.urls
