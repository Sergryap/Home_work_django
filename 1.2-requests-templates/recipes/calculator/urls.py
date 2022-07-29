from django.urls import path

from .views import recipes

urlpatterns = [
    path('<slug:recipe>/', recipes, name='recipes'),
]