import itertools
import json

from django.core.management.base import BaseCommand

from app_pets.models import Pet
from app_pets.serializers import PetSerializerToJson


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            "--has_photos",
            help="True to show only pets with photo."
                 " Use False if you need only pets without photo.",
        )

    def handle(self, *args, **options):
        has_photos = options["has_photos"]
        pets = Pet.objects.all()
        if has_photos == "True":
            pets = pets.filter(photos__isnull=False)
        elif has_photos == "False":
            pets = pets.filter(photos__isnull=True)
        elif not has_photos:
            pass
        else:
            print(f"has_photos can be only True or False not '{has_photos}'")
            return
        
        pets = pets.distinct()
        pets = self.get_response(PetSerializerToJson, pets)
        self.stdout.write(json.dumps(pets))

    @staticmethod
    def get_response(serializer_class, queryset):
        serializer = serializer_class(queryset, many=True)

        pets = []
        for obj in list(serializer.data):
            obj = dict(obj)
            if obj["photos"]:
                photos = [list(d.values()) for d in list(obj["photos"])]
                obj["photos"] = list(itertools.chain(*photos))
            pets.append(obj)
        return dict(pets=pets)
