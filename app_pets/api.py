import json

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core import serializers

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
            deleted_count, _ = Pet.objects.filter(id__in=valid_ids).delete()
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
    file_name = 'dads' + ".jpg"
    file_path = f"/images/{file_name}"
    with open(f"{settings.MEDIA_ROOT}{file_path}", "wb") as file:
        file.write(request.data['file'].file.read())
    image = PetImage.objects.create(image=file_path)
    serializer = PetImageSerializer(image, context={"request": request})
    return Response(serializer.data)


@api_view(http_method_names=["get"])
def handle(request):
    has_photos = True
    pets = Pet.objects.all()
    if has_photos == "True":
        pets = pets.filter(photos__isnull=False)
    elif has_photos == "False":
        pets = pets.filter(photos__isnull=True)
    else:
        print(f"has_photos can be only True or False not '{has_photos}'")
    pets = pets.distinct()
    # print(self.request)
    serializer = PetSerializer(pets, many=True)
    response = []
    for obj in list(serializer.data):
        obj = dict(obj)
        if obj["photos"]:
            obj["photos"] = dict(list(obj["photos"]))
        response.append(obj)

    print(serializers.serialize("json", pets))
    # self.stdout.write(json.loads(serializer.data))


class PetImageViewSet(viewsets.ModelViewSet):
    queryset = PetImage.objects.all()
    serializer_class = PetImageSerializer
