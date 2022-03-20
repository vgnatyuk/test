from django.contrib import admin

# Register your models here.
from app_pets.models import Pet, PetImage


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    pass


@admin.register(PetImage)
class PetImageAdmin(admin.ModelAdmin):
    pass
