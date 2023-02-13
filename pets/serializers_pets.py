from rest_framework import serializers
from groups.serializers_groups import GroupSerializerInput, GroupSerializerOutput
from traits.serializers_traits import TraitSerializerInput, TraitSerializerOutput
from .models import PetGenre


class PetSerializerInput(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(choices=PetGenre.choices, default=PetGenre.Default)

    group = GroupSerializerInput()
    traits = TraitSerializerInput(many=True)


class PetSerializerOutput(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=50, required=False)
    age = serializers.IntegerField(required=False)
    weight = serializers.FloatField(required=False)
    sex = serializers.ChoiceField(
        choices=PetGenre.choices, default=PetGenre.Default, required=False
    )

    group = GroupSerializerOutput(required=False)
    traits = TraitSerializerOutput(many=True, required=False)


class PetSerializerPatch(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=50, required=False)
    age = serializers.IntegerField(required=False)
    weight = serializers.FloatField(required=False)
    sex = serializers.ChoiceField(
        choices=PetGenre.choices, default=PetGenre.Default, required=False
    )


# o write_only não permite que um dado seja enviado no response ex.:password
# o read_only não permite que um dano chegue na
# rm */migrations/0*
# python manage.py makemigrations
# python manage.py migrate
