import uuid

from django.db import models

# Create your models here.


class Pet(models.Model):
    DOG = "dog"
    CAT = "cat"

    TYPE = (
        (CAT, "Cat"),
        (DOG, "Dog"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=32)
    age = models.PositiveSmallIntegerField()
    type = models.CharField(choices=TYPE, max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type}: {self.name}"


class PetImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pet = models.ForeignKey(Pet, blank=True, null=True, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to='images/', blank=True)
