import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Order


class RuleEngineTestCase(APITestCase):
    def setUp(self):
        self.order1 = Order.objects.create(total=150.00, items_count=3)
        self.order2 = Order.objects.create(total=75.50, items_count=1)
        self.order3 = Order.objects.create(total=200.00, items_count=5)

    def test_check_rules_success(self):
        url = reverse("check_rules")
        data = {"order_id": self.order1.id, "rules": ["min_total_100", "min_items_2"]}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["passed"], True)
        self.assertEqual(response.data["details"]["min_total_100"], True)
        self.assertEqual(response.data["details"]["min_items_2"], True)

    def test_check_rules_partial_fail(self):
        url = reverse("check_rules")
        data = {"order_id": self.order2.id, "rules": ["min_total_100", "min_items_2"]}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["passed"], False)
        self.assertEqual(response.data["details"]["min_total_100"], False)
        self.assertEqual(response.data["details"]["min_items_2"], False)

    def test_divisible_by_5_rule(self):
        url = reverse("check_rules")
        data = {"order_id": self.order3.id, "rules": ["divisible_by_5"]}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["passed"], True)
        self.assertEqual(response.data["details"]["divisible_by_5"], True)

    def test_order_not_found(self):
        url = reverse("check_rules")
        data = {"order_id": 999, "rules": ["min_total_100"]}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_rule(self):
        url = reverse("check_rules")
        data = {"order_id": self.order1.id, "rules": ["invalid_rule"]}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["passed"], False)
        self.assertEqual(response.data["details"]["invalid_rule"], False)
