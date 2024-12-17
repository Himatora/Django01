from django.core.management.base import BaseCommand

from faker import Faker

from smehs.models import Smeh


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        for _ in range(1000):
            Smeh.objects.create(
                name=fake.name()
            )
