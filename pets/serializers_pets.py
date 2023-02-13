from rest_framework import serializers
from groups.serializers_groups import GroupSerializer
from traits.serializers_traits import TraitSerializer
from .models import PetGenre


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(choices=PetGenre.choices, default=PetGenre.Default)

    group = GroupSerializer()
    traits = TraitSerializer(many=True)
