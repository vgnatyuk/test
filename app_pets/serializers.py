from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from rest_framework import serializers

from app_pets.models import Pet, PetImage


# def get_full_path_to_image(obj, context):
#     queryset = PetImage.objects.filter(pet=obj)
#     return PetImageSerializer(
#         queryset,
#         many=True,
#         context=context,
#     ).data


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
