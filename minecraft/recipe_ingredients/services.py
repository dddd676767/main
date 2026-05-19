# recipe_ingredients/service.py
from typing import List, Dict, Set
from .models import RecipeIngredient
from items.models import Item


class RecipeIngredientService:
    """Сервис для работы с ингредиентами рецептов"""
    
    @staticmethod
    def get_ingredients_for_recipe(recipe_id: int) -> List[Dict]:
        """Получить все ингредиенты для рецепта"""
        ingredients = RecipeIngredient.objects.filter(recipe_id=recipe_id).select_related('item')
        
        return [
            {
                'item': ing.item.name,
                'item_id': ing.item.item_id,
                'count': ing.count,
                'row': ing.position_row,
                'col': ing.position_col,
                'alternatives': ing.alternatives,
                'tag': ing.tag,
            }
            for ing in ingredients
        ]
    
    @staticmethod
    def get_recipes_using_item(item_id: str) -> List[int]:
        """Получить ID всех рецептов, где используется предмет"""
        item = Item.objects.filter(item_id=item_id).first()
        if not item:
            return []
        
        return list(
            RecipeIngredient.objects.filter(item=item)
            .values_list('recipe_id', flat=True)
            .distinct()
        )
    
    @staticmethod
    def check_ingredients_available(recipe_id: int, available_items: Set[int]) -> bool:
        """Проверить, доступны ли все ингредиенты для рецепта"""
        ingredients = RecipeIngredient.objects.filter(recipe_id=recipe_id)
        
        for ing in ingredients:
            if ing.item.id not in available_items:
                return False
        
        return True