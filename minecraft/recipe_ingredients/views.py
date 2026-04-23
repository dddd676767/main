from rest_framework import viewsets
from .models import RecipeIngredient
from .serializers import RecipeIngredientSerializer

class RecipeIngredientViewSet(viewsets.ModelViewSet):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer
    filterset_fields = ['recipe', 'item']