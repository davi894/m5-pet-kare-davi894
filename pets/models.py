from django.db import models
from traits.models import Trait

# Create your models here.


class PetGenre(models.TextChoices):
    Male = "Male"
    Female = "Female"
    Default = "Not Informed"


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=20, choices=PetGenre.choices, default=PetGenre.Default
    )

    group = models.ForeignKey(
        "groups.Group",
        related_name="pets",
        on_delete=models.PROTECT,
    )

    traits = models.ManyToManyField(
        "traits.Trait",
        related_name="pets",
    )
