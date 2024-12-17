from django.db.utils import DatabaseError
from django.core.management import BaseCommand

from oradja.models import ApiModProperty


class Command(BaseCommand):
    help = "Shows db connection environment"

    def handle(self, *args, **options):

        try:
            env = ApiModProperty.objects.get(name="name").value
            print(f"Connection set for: {env}.")
        except ApiModProperty.DoesNotExist:
            print(f"Connection set for unknown environment.")

        except DatabaseError as e:
            print(f"Error connecting to database: {e}")
