import pytest
from recipes.models import Recipe
from items.models import Item

@pytest.mark.django_db
class TestRecipeModel:
    
    def test_create_recipe(self):
        """Тест создания рецепта"""
        item = Item.objects.create(
            item_id="minecraft:chest",
            name="Сундук",
            name_en="Chest",
            category="block"
        )
        recipe = Recipe.objects.create(
            result_item=item,
            result_count=1,
            recipe_type="crafting_3x3"
        )
        assert recipe.result_item.name == "Сундук"
        assert recipe.recipe_type == "crafting_3x3"
    
    def test_recipe_str_method(self):
        """Тест строкового представления"""
        item = Item.objects.create(
            item_id="minecraft:stick",
            name="Палка",
            name_en="Stick",
            category="material"
        )
        recipe = Recipe.objects.create(
            result_item=item,
            result_count=4,
            recipe_type="crafting_2x2"
        )
        assert str(recipe) == f"Крафт: Палка x4"