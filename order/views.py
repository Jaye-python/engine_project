from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order
from .rules import RuleRegistry
from .serializers import RuleCheckRequestSerializer, RuleCheckResponseSerializer


@method_decorator(csrf_exempt, name="dispatch")
class CheckRulesView(APIView):
    @extend_schema(
        request=RuleCheckRequestSerializer,
        responses=RuleCheckResponseSerializer,
        description="Check if an order passes specified validation rules",
        summary="Validate Order Rules",
    )
    def post(self, request):
        serializer = RuleCheckRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated: dict = getattr(serializer, "validated_data", {}) or {}
        order_id = validated.get("order_id")
        rule_names = validated.get("rules", [])

        if order_id is None:
            return Response({"error": "order_id is required"}, status=status.HTTP_400_BAD_REQUEST)

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
