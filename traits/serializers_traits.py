from rest_framework import serializers


class TraitSerializerInput(serializers.Serializer):
    traits_name = serializers.CharField(source="name", max_length=20)


class TraitSerializerOutput(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    traits_name = serializers.CharField(source="name", max_length=20, required=False)
    created_at = serializers.DateTimeField(required=False)
