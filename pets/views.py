from rest_framework.pagination import PageNumberPagination
from .serializers_pets import (
    PetSerializerInput,
    PetSerializerOutput,
    TraitSerializerOutput,
    PetSerializerPatch,
)
from rest_framework.views import APIView, status
from rest_framework.response import Response
from groups.models import Group
from traits.models import Trait
from .models import Pet
import ipdb


class PetView(APIView, PageNumberPagination):
    def post(self, req):
        dict_req_pet = req.data

        serializers_post_pet = PetSerializerInput(data=dict_req_pet)

        serializers_post_pet.is_valid(raise_exception=True)

        traits = serializers_post_pet.validated_data.pop("traits")
        groups = serializers_post_pet.validated_data.pop("group")
        existing_group = Group.objects.filter(
            scientific_name__iexact=groups["scientific_name"]
        )

        if existing_group:
            pet_existing_group = Pet.objects.create(
                **serializers_post_pet.validated_data, group_id=existing_group[0].id
            )
            for trait in traits:
                existing_Trait = Trait.objects.filter(name__iexact=trait["name"])
                #
                if existing_Trait:
                    pet_existing_group.traits.add(**trait)
                #
                else:
                    create = Trait.objects.create(**trait)
                    pet_existing_group.traits.add(create)

            traits_serializer = TraitSerializerOutput(
                pet_existing_group.traits, many=True
            )
            serializer_pet_existing_group = PetSerializerOutput(pet_existing_group)

            data_serializer_pet_existing_group = {
                **serializer_pet_existing_group.data,
                "traits": traits_serializer.data,
            }

            return Response(
                data_serializer_pet_existing_group,
                status.HTTP_201_CREATED,
            )

        groups_create = Group.objects.create(**groups)
        group_id = groups_create.id

        pet = Pet.objects.create(
            **serializers_post_pet.validated_data, group_id=group_id
        )

        for trait in traits:
            create = Trait.objects.create(**trait)
            pet.traits.add(create)

        pet_serializer = PetSerializerOutput(pet)
        traits_serializer = TraitSerializerOutput(pet.traits, many=True)

        data = {
            **pet_serializer.data,
            "traits": traits_serializer.data,
        }

        return Response(data, status.HTTP_201_CREATED)

    def get(self, req):
        pets = Pet.objects.all()

        result_page = self.paginate_queryset(pets, req)
        serializer = PetSerializerOutput(result_page, many=True)

        return self.get_paginated_response(serializer.data)


class PetViewId(APIView):
    def get(self, req, pet_id):
        try:
            pet = Pet.objects.get(id=pet_id)
            serializer = PetSerializerOutput(pet)

            return Response(serializer.data, status.HTTP_200_OK)

        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND)

    def patch(self, req, pet_id):
        try:
            dict_req_pet = req.data
            pet = Pet.objects.get(id=pet_id)
            serializer = PetSerializerOutput(pet)
            id_group = []
            list_trait = []

            PetSerializerOutput(data=dict_req_pet).is_valid(raise_exception=True)

            if "group" in dict_req_pet.keys():
                group = dict_req_pet.pop("group")
                existing_group = Group.objects.filter(
                    scientific_name__iexact=group["scientific_name"]
                )
                if existing_group:
                    id_group.append(
                        {
                            "id": existing_group[0].id,
                            "scientific_name": existing_group[0].scientific_name,
                            "created_at": existing_group[0].created_at,
                        }
                    )
                else:
                    pet.group = None
                    pet.save()
                    groups_create = Group.objects.create(**group)
                    id_group.append(
                        {
                            "id": groups_create.id,
                            "scientific_name": groups_create.scientific_name,
                            "created_at": groups_create.created_at,
                        }
                    )
                    pet.save()

            if "traits" in dict_req_pet.keys():
                traits = dict_req_pet.pop("traits")
                for trait in traits:
                    existing_Trait = Trait.objects.filter(name__iexact=trait["name"])
                    if existing_Trait:
                        list_trait.append(
                            {
                                "id": existing_Trait[0].id,
                                "traits_name": existing_Trait[0].name,
                                "created_at": existing_Trait[0].created_at,
                            }
                        )
                    else:
                        pet.traits.clear()
                        traits_create = Trait.objects.create(**trait)
                        list_trait.append(
                            {
                                "id": traits_create.id,
                                "traits_name": traits_create.name,
                                "created_at": traits_create.created_at,
                            }
                        )
                        pet.traits.add(
                            {
                                "id": traits_create.id,
                                "name": traits_create.traits_name,
                                "created_at": traits_create.created_at,
                            }
                        )
                        pet.save()

            update_pet = {
                **serializer.data,
                **dict_req_pet,
                "group": id_group[0],
                "traits": list_trait,
            }
            pet_update = Pet(**update_pet)
            pet_update.save()

            return Response(
                update_pet,
                status.HTTP_201_CREATED,
            )

        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND)

    def delete(self, req, pet_id):
        try:
            pet = Pet.objects.get(id=pet_id)
            Pet.objects.filter(id=pet.id)[0].delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND)


class PetViewParams(APIView):
    def get(self, req):
        trait = req.query_params.get("trait", None)
        print(trait)

        trait_list = Pet.objects.filter(traits__name__iexact=trait)

        serializer = PetSerializerOutput(trait_list, many=True)

        return Response(serializer.data, status.HTTP_200_OK)
