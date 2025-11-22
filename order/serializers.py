from rest_framework import serializers


class RuleCheckRequestSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    rules = serializers.ListField(child=serializers.CharField(), allow_empty=False)


class RuleCheckResponseSerializer(serializers.Serializer):
    passed = serializers.BooleanField()
    details = serializers.DictField()
