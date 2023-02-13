from django.urls import path
from .views import PetView, PetViewId, PetViewParams

urlpatterns = [
    path("pets/", PetView.as_view()),
    path("pets/params/", PetViewParams.as_view()),
    path("pets/<int:pet_id>/", PetViewId.as_view()),
]
