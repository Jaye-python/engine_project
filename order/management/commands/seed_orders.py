from django.core.management.base import BaseCommand

from order.models import Order


class Command(BaseCommand):
    help = "Seed the database with example orders"

    def handle(self, *args, **options):
        Order.objects.all().delete()

        orders = [
            Order(total=150.00, items_count=3),
            Order(total=75.50, items_count=1),
            Order(total=200.00, items_count=5),
        ]

        Order.objects.bulk_create(orders)
        self.stdout.write(self.style.SUCCESS("Successfully seeded 3 orders"))
