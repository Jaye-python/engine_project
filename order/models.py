from django.db import models


class Order(models.Model):
    total = models.DecimalField(max_digits=10, decimal_places=2)
    items_count = models.IntegerField()

    def __str__(self):
        return f"Order {self.pk}: ${self.total}, {self.items_count} items"
