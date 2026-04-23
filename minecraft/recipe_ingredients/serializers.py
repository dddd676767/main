from rest_framework import serializers
from .models import RecipeIngredient

class RecipeIngredientSerializer(serializers.ModelSerializer):
    recipe_name = serializers.ReadOnlyField(source='recipe.result_item.name')
    item_name = serializers.ReadOnlyField(source='item.name')
    
    class Meta:
        model = RecipeIngredient
        fields = '__all__'