from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from app_pets.models import Pet, PetImage

from pets import settings


class PetSerializer(ModelSerializer):
    photos = serializers.SerializerMethodField()

    def get_photos(self, obj):
        queryset = PetImage.objects.filter(pet=obj)
        return PetImageSerializer(
            queryset,
            many=True,
            context=self.context,
        ).data

    class Meta:
        model = Pet
        fields = "id", "name", "age", "type", "photos", "created_at"


class PetImageSerializer(ModelSerializer):
    class Meta:
        model = PetImage
        exclude = "pet",


class PetImageSerializerToJson(ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        image_url = f"{settings.BASE_URL}{settings.MEDIA_URL}{obj.image}"
        return image_url

    class Meta:
        model = PetImage
        fields = "image",


class PetSerializerToJson(PetSerializer):
    photos = serializers.SerializerMethodField()

    def get_photos(self, obj):
        queryset = PetImage.objects.filter(pet=obj)
        return PetImageSerializerToJson(
            queryset,
            many=True,
            context=self.context,
        ).data
