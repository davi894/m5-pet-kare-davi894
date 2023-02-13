from rest_framework.pagination import PageNumberPagination
from .serializers_pets import PetSerializer
from rest_framework.views import APIView, status
from rest_framework.response import Response
from groups.models import Group
from traits.models import Trait
from .models import Pet
import ipdb


class PetView(APIView, PageNumberPagination):
    def post(self, req):
        dict_req_pet = req.data
        serializers_post_pet = PetSerializer(data=dict_req_pet)
        serializers_post_pet.is_valid(raise_exception=True)
        traits = serializers_post_pet.validated_data.pop("traits")
        groups = serializers_post_pet.validated_data.pop("group")

        existing_group = Group.objects.filter(
            scientific_name__iexact=groups["scientific_name"]
        )
        group_id = []

        if existing_group:
            group_id.append(existing_group[0].id)
        else:
            groups_create = Group.objects.create(**groups)
            group_id.append(groups_create.id)

        pet = Pet.objects.create(
            **serializers_post_pet.validated_data, group_id=group_id[0]
        )

        for trait in traits:
            existing_Trait = Trait.objects.filter(name__iexact=trait["name"])
            if existing_Trait:
                pet.traits.add(existing_Trait[0].id)
                pet.save()
            else:
                create = Trait.objects.create(**trait)
                pet.traits.add(create.id)

        pet_serializer = PetSerializer(pet)

        return Response(pet_serializer.data, status.HTTP_201_CREATED)

    def get(self, req):

        pets = Pet.objects.all()

        tarit = req.query_params.get("trait")

        if tarit:
            aa = []
            trait_list = Pet.objects.all()

            for x in trait_list:
                for y in x.traits.all():
                    if y.name == tarit:
                        aa.append(
                            {
                                "id": x.id,
                                "name": x.name,
                                "age": x.age,
                                "weight": x.weight,
                                "sex": x.sex,
                                "group": {
                                    "id": x.group.id,
                                    "scientific_name": x.group.scientific_name,
                                    "created_at": x.group.created_at,
                                },
                                "traits": [
                                    {
                                        "id": y.id,
                                        "name": y.name,
                                        "created_at": y.created_at,
                                    }
                                ],
                            }
                        )

            result_page = self.paginate_queryset(pets, req, view=self)
            serializer = PetSerializer(result_page, many=True)
            return self.get_paginated_response(aa)

        result_page = self.paginate_queryset(pets, req, view=self)
        serializer = PetSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)


class PetViewId(APIView):
    def get(self, req, pet_id):
        try:
            pet = Pet.objects.get(id=pet_id)
            serializer = PetSerializer(pet)

            return Response(serializer.data, status.HTTP_200_OK)

        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND)

    def patch(self, req, pet_id):
        try:
            dict_req_pet = req.data
            pet = Pet.objects.get(id=pet_id)

            serializer = PetSerializer(data=dict_req_pet, partial=True)

            serializer.is_valid(raise_exception=True)

            if "group" in serializer.validated_data.keys():
                group = serializer.validated_data.pop("group")
                existing_group = Group.objects.filter(
                    scientific_name__iexact=group["scientific_name"]
                )

                if existing_group:
                    pet.group = None
                    pet.group = existing_group[0]
                else:
                    groups_create = Group.objects.create(**group)
                    pet.group = groups_create.id

            if "traits" in serializer.validated_data.keys():
                traits_req = serializer.validated_data.pop("traits")
                pet.traits.clear()
                for trait in traits_req:
                    existing_Trait = Trait.objects.filter(name__iexact=trait["name"])
                    if existing_Trait:
                        pet.traits.add(existing_Trait[0])
                    else:

                        create = Trait.objects.create(name=trait["name"])
                        pet.traits.add(create)

            for key, value in serializer.validated_data.items():
                setattr(pet, key, value)

            pet.save()
            serializer = PetSerializer(pet)

            return Response(
                serializer.data,
                status.HTTP_200_OK,
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
