from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order
from .rules import RuleRegistry
from .serializers import RuleCheckRequestSerializer, RuleCheckResponseSerializer


class CheckRulesView(APIView):
    def post(self, request):
        serializer = RuleCheckRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated = getattr(serializer, "validated_data", None) or {}
        order_id = validated.get("order_id")
        if order_id is None:
            return Response({"error": "order_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        rule_names = validated.get("rules") or []
        if not isinstance(rule_names, (list, tuple)):
            rule_names = [rule_names]

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        details = {}
        for rule_name in rule_names:
            rule_class = RuleRegistry.get_rule(rule_name)
            if rule_class:
                rule_instance = rule_class()
                details[rule_name] = rule_instance.check(order)
            else:
                details[rule_name] = False

        passed = all(details.values())

        response_data = {"passed": passed, "details": details}

        response_serializer = RuleCheckResponseSerializer(response_data)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
