#!/usr/bin/env python
"""
Demo script for the Django Rule Engine API
"""
import json
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "engine_project.settings")
django.setup()

from order.models import Order
from order.rules import RuleRegistry

print("=== Django Pluggable Rule Engine Demo ===\n")

# Show existing orders
print("📦 Orders in database:")
for order in Order.objects.all():
    print(f"  Order {order.pk}: ${order.total}, {order.items_count} items")

print("\n🔧 Available rules:")
for rule_name, rule_class in RuleRegistry.get_all_rules().items():
    print(f"  - {rule_name}: {rule_class.__doc__ or rule_class.__name__}")

print("\n🧪 Testing rules manually:")

# Test each order against all rules
for order in Order.objects.all():
    print(f"\nOrder {order.pk} (${order.total}, {order.items_count} items):")

    for rule_name, rule_class in RuleRegistry.get_all_rules().items():
        rule_instance = rule_class()
        result = rule_instance.check(order)
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {rule_name}: {status}")

print("\n🌐 API Examples:")
print("POST /rules/check/")
print(json.dumps({"order_id": 1, "rules": ["min_total_100", "min_items_2"]}, indent=2))

print("\nExpected Response:")
print(json.dumps({"passed": True, "details": {"min_total_100": True, "min_items_2": True}}, indent=2))
