# recipes/service.py
from typing import List, Dict, Optional
from .models import Recipe
from items.models import Item
from versions.models import MinecraftVersion


class RecipeService:
    """Сервис для работы с рецептами"""
    
    @staticmethod
    def get_recipes_by_type(recipe_type: str, version: str = None) -> List[Recipe]:
        """Получить рецепты по типу"""
        queryset = Recipe.objects.filter(recipe_type=recipe_type)
        
        if version:
            version_obj = MinecraftVersion.objects.filter(version_number=version).first()
            if version_obj:
                queryset = queryset.filter(versions=version_obj)
        
        return list(queryset.select_related('result_item').all())
    
    @staticmethod
    def get_recipes_for_item(item_id: str) -> List[Dict]:
        """Получить все рецепты для предмета (где он результат)"""
        item = Item.objects.filter(item_id=item_id).first()
        if not item:
            return []
        
        recipes = Recipe.objects.filter(result_item=item).prefetch_related('ingredients')
        
        result = []
        for recipe in recipes:
            result.append({
                'id': recipe.id,
                'result_count': recipe.result_count,
                'recipe_type': recipe.get_recipe_type_display(),
                'shape': recipe.shape,
                'ingredients': [
                    {
                        'item': ing.item.name,
                        'item_id': ing.item.item_id,
                        'count': ing.count,
                        'row': ing.position_row,
                        'col': ing.position_col,
                    }
                    for ing in recipe.ingredients.all()
                ]
            })
        
        return result
    
    @staticmethod
    def get_recipe_grid(recipe_id: int, size: int = 3) -> List[List[Optional[Dict]]]:
        """Получить сетку крафта для отображения"""
        recipe = Recipe.objects.filter(id=recipe_id).prefetch_related('ingredients').first()
        if not recipe:
            return []
        
        grid = [[None for _ in range(size)] for _ in range(size)]
        
        for ingredient in recipe.ingredients.all():
            if ingredient.position_row is not None and ingredient.position_col is not None:
                if ingredient.position_row < size and ingredient.position_col < size:
                    grid[ingredient.position_row][ingredient.position_col] = {
                        'item': ingredient.item.name,
                        'item_id': ingredient.item.item_id,
                        'count': ingredient.count,
                    }
        
        return grid