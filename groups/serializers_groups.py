from rest_framework import serializers


class GroupSerializerInput(serializers.Serializer):
    scientific_name = serializers.CharField(max_length=50)


class GroupSerializerOutput(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    scientific_name = serializers.CharField(max_length=50, required=False)
    created_at = serializers.DateTimeField(required=False)
