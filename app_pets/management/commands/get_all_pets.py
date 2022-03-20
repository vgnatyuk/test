import json
from pprint import pprint

from django.core.management.base import BaseCommand, CommandError
from django.core.serializers import serialize

from app_pets.models import Pet
from app_pets.serializers import PetSerializer


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument(
            '--has_photos',
            help='--has_photos=True to show only pets with photo. Use False if you need only pets without photo.',
        )

    def handle(self, *args, **options):
        has_photos = True
        pets = Pet.objects.all()
        if has_photos == "True":
            pets = pets.filter(photos__isnull=False)
        elif has_photos == "False":
            pets = pets.filter(photos__isnull=True)
        else:
            print(f"has_photos can be only True or False not '{has_photos}'")
        pets = pets.distinct()

        serializer = PetSerializer(pets, many=True)
        response = []
        for obj in list(serializer.data):
            obj = dict(obj)
            if obj["photos"]:
                obj["photos"] = dict(list(obj["photos"]))
            response.append(obj)

        pprint(response)
        # self.stdout.write(json.loads(serializer.data))
