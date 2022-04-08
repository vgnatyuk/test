import json
import os
import time

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app_pets.serializers import PetSerializer, PetImageSerializer
from app_pets.models import Pet, PetImage
from pets import settings


class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as exc:
            return Response(json.dumps(exc.args), status=400)
        pet = serializer.save()
        return Response(self.serializer_class(pet).data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset(query_params=request.query_params)

        count = queryset.count()
        items = PetSerializer(queryset, many=True, context={"request": request})
        response = {
            "count": count,
            "items": items.data,
        }
        return Response(response)

    def get_queryset(self, *args, **kwargs):
        default_limit = 20
        default_offset = 0

        limit = kwargs["query_params"].get("limit", "")
        offset = kwargs["query_params"].get("offset", "")
        has_photos = kwargs["query_params"].get("has_photos", None)

        queryset = super().get_queryset()
        photos_isnull = self.get_photos_isnull(has_photos) if has_photos else None
        if photos_isnull is not None:
            queryset = queryset.filter(photos__isnull=photos_isnull).distinct()

        offset = int(offset) if offset.isdigit() else default_offset
        limit = int(limit) if limit.isdigit() else default_limit
        queryset = queryset[offset:offset + limit]
        return queryset

    @staticmethod
    def get_photos_isnull(has_photos):
        if has_photos == "true":
            return False
        elif has_photos == "false":
            return True
        else:
            return None

    @staticmethod
    def destroy_list(request, *args, **kwargs):
        ids = dict(request.data.lists()).get("ids")
        if ids:
            valid_ids, errors = check_ids(ids)
            pets = Pet.objects.filter(id__in=valid_ids)
            deleted_count = pets.count()
            pets.delete()
            response = {"deleted": deleted_count, "errors": errors}
            return Response(response)
        else:
            return Response("You haven't sent ids to delete.")


def check_ids(ids):
    errors = []
    valid_ids = []
    for id in ids:
        uuid = id.replace("-", "")
        if len(uuid) != 32 or not Pet.objects.filter(id=id):
            errors.append({"id": id, "error": "Pet with the matching ID was not found."})
        else:
            valid_ids.append(id)
    return valid_ids, errors


@api_view(http_method_names=["post"])
def photo(request, id):
    id, error = check_ids([id])
    if error:
        return Response({"error": error}, status=400)
    pet = Pet.objects.get(id=id[0])
    file_path = f"images/{pet.name}_{int(time.time())}.jpg"
    full_path = os.path.join(settings.BASE_DIR, file_path)
    with open(full_path, "wb") as file:
        file.write(request.data['file'].file.read())

    image = PetImage.objects.create(image=f"{settings.BASE_URL}/{file_path}", pet=pet)
    serializer = PetImageSerializer(image, context={"request": request})
    return Response(serializer.data)


class PetImageViewSet(viewsets.ModelViewSet):
    queryset = PetImage.objects.all()
    serializer_class = PetImageSerializer
