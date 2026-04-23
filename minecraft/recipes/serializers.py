from rest_framework import serializers
from .models import Recipe
from recipe_ingredients.models import RecipeIngredient
from recipe_ingredients.serializers import RecipeIngredientSerializer

class RecipeSerializer(serializers.ModelSerializer):
    result_item_name = serializers.ReadOnlyField(source='result_item.name')
    recipe_type_display = serializers.CharField(source='get_recipe_type_display', read_only=True)
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    
    class Meta:
        model = Recipe
        fields = '__all__'