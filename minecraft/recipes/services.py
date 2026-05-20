from .models import Recipe
from recipe_ingredients.models import RecipeIngredient
from items.models import Item
from versions.models import MinecraftVersion
from django.db import models

class RecipeService:
    
    @staticmethod
    def get_all():
        return Recipe.objects.all()
    
    @staticmethod
    def get_by_id(recipe_id):
        return Recipe.objects.filter(id=recipe_id).first()
    
    @staticmethod
    def filter_by_type(recipe_type):
        return Recipe.objects.filter(recipe_type=recipe_type)
    
    @staticmethod
    def get_for_item(item_id):
        return Recipe.objects.filter(result_item__item_id=item_id)
    
    @staticmethod
    def get_where_ingredient(item_id):
        item = Item.objects.filter(item_id=item_id).first()
        if not item:
            return Recipe.objects.none()
        ingredient_recipes = RecipeIngredient.objects.filter(item=item).values_list('recipe_id', flat=True)
        return Recipe.objects.filter(id__in=ingredient_recipes)
    
    @staticmethod
    def get_recipe_types():
        return [
            {"id": "crafting_2x2", "name": "Верстак 2x2"},
            {"id": "crafting_3x3", "name": "Верстак 3x3"},
            {"id": "smelting", "name": "Печь"},
            {"id": "blasting", "name": "Плавильная печь"},
            {"id": "smoking", "name": "Коптильня"},
            {"id": "campfire", "name": "Костёр"},
            {"id": "smithing", "name": "Кузнечный стол"},
            {"id": "stonecutting", "name": "Камнерез"},
            {"id": "brewing", "name": "Варочная стойка"},
        ]
    
    @staticmethod
    def get_recipe_with_ingredients(recipe_id):
        recipe = Recipe.objects.filter(id=recipe_id).first()
        if not recipe:
            return None
        return {
            "id": recipe.id,
            "result_item": recipe.result_item,
            "result_count": recipe.result_count,
            "recipe_type": recipe.recipe_type,
            "recipe_type_display": recipe.get_recipe_type_display(),
            "shape": recipe.shape,
            "group": recipe.group,
            "ingredients": [
                {
                    "item": ing.item,
                    "count": ing.count,
                    "row": ing.position_row,
                    "col": ing.position_col,
                    "alternatives": ing.alternatives,
                    "tag": ing.tag
                }
                for ing in recipe.ingredients.all()
            ],
            "versions": [v.version_number for v in recipe.versions.all()]
        }
    
    @staticmethod
    def search(query):
        if not query:
            return Recipe.objects.none()
        return Recipe.objects.filter(
            models.Q(result_item__name__icontains=query) |
            models.Q(result_item__name_en__icontains=query)
        )