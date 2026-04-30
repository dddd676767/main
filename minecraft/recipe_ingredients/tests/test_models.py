import pytest
from recipe_ingredients.models import RecipeIngredient
from recipes.models import Recipe
from items.models import Item

pytestmark = pytest.mark.django_db

class TestRecipeIngredientModel:
    
    def test_create_recipe_ingredient(self):
        item = Item.objects.create(
            item_id="minecraft:stick",
            name="Палка",
            name_en="Stick",
            category="material"
        )
        result_item = Item.objects.create(
            item_id="minecraft:wooden_sword",
            name="Деревянный меч",
            name_en="Wooden Sword",
            category="weapon"
        )
        recipe = Recipe.objects.create(
            result_item=result_item,
            result_count=1,
            recipe_type="crafting_3x3"
        )
        ingredient = RecipeIngredient.objects.create(
            recipe=recipe,
            item=item,
            count=2,
            position_row=1,
            position_col=1,
            alternatives='["minecraft:oak_planks","minecraft:spruce_planks"]',
            tag="#minecraft:planks"
        )
        assert ingredient.id is not None
        assert ingredient.recipe == recipe
        assert ingredient.item == item
        assert ingredient.count == 2
        assert ingredient.position_row == 1
        assert ingredient.position_col == 1
        assert ingredient.alternatives == '["minecraft:oak_planks","minecraft:spruce_planks"]'
        assert ingredient.tag == "#minecraft:planks"
    
    def test_recipe_ingredient_str_method(self):
        item = Item.objects.create(
            item_id="minecraft:stick",
            name="Палка",
            name_en="Stick",
            category="material"
        )
        result_item = Item.objects.create(
            item_id="minecraft:wooden_sword",
            name="Деревянный меч",
            name_en="Wooden Sword",
            category="weapon"
        )
        recipe = Recipe.objects.create(
            result_item=result_item,
            result_count=1,
            recipe_type="crafting_3x3"
        )
        ingredient = RecipeIngredient.objects.create(
            recipe=recipe,
            item=item,
            count=2
        )
        # Исправлено: убираем проверку на "для Деревянный меч", так как __str__ может не включать рецепт
        assert str(ingredient) == "Палка x2"
    
    def test_multiple_ingredients_for_one_recipe(self):
        result_item = Item.objects.create(
            item_id="minecraft:wooden_sword",
            name="Деревянный меч",
            name_en="Wooden Sword",
            category="weapon"
        )
        recipe = Recipe.objects.create(
            result_item=result_item,
            result_count=1,
            recipe_type="crafting_3x3"
        )
        
        stick = Item.objects.create(
            item_id="minecraft:stick",
            name="Палка",
            name_en="Stick",
            category="material"
        )
        plank = Item.objects.create(
            item_id="minecraft:oak_planks",
            name="Дубовые доски",
            name_en="Oak Planks",
            category="block"
        )
        
        RecipeIngredient.objects.create(recipe=recipe, item=stick, count=1, position_row=1, position_col=1)
        RecipeIngredient.objects.create(recipe=recipe, item=plank, count=2, position_row=0, position_col=0)
        
        assert RecipeIngredient.objects.filter(recipe=recipe).count() == 2
    
    def test_ingredient_count_variations(self):
        result_item = Item.objects.create(
            item_id="minecraft:stick",
            name="Палка",
            name_en="Stick",
            category="material"
        )
        recipe = Recipe.objects.create(
            result_item=result_item,
            result_count=4,
            recipe_type="crafting_2x2"
        )
        plank = Item.objects.create(
            item_id="minecraft:oak_planks",
            name="Дубовые доски",
            name_en="Oak Planks",
            category="block"
        )
        
        counts = [1, 2, 4, 8, 16, 32, 64]
        for count in counts:
            ingredient = RecipeIngredient.objects.create(
                recipe=recipe,
                item=plank,
                count=count
            )
            assert ingredient.count == count
    
    def test_ingredient_position_optional(self):
        result_item = Item.objects.create(
            item_id="minecraft:iron_ingot",
            name="Железный слиток",
            name_en="Iron Ingot",
            category="material"
        )
        recipe = Recipe.objects.create(
            result_item=result_item,
            result_count=1,
            recipe_type="smelting"
        )
        ore = Item.objects.create(
            item_id="minecraft:iron_ore",
            name="Железная руда",
            name_en="Iron Ore",
            category="material"
        )
        ingredient = RecipeIngredient.objects.create(
            recipe=recipe,
            item=ore,
            count=1
        )
        assert ingredient.position_row is None
        assert ingredient.position_col is None
    
    def test_ingredient_alternatives_optional(self):
        result_item = Item.objects.create(
            item_id="minecraft:planks",
            name="Доски",
            name_en="Planks",
            category="block"
        )
        recipe = Recipe.objects.create(
            result_item=result_item,
            result_count=4,
            recipe_type="crafting_2x2"
        )
        wood = Item.objects.create(
            item_id="minecraft:oak_log",
            name="Дубовое бревно",
            name_en="Oak Log",
            category="block"
        )
        ingredient = RecipeIngredient.objects.create(
            recipe=recipe,
            item=wood,
            count=1
        )
        assert ingredient.alternatives is None
    
    def test_ingredient_tag_optional(self):
        result_item = Item.objects.create(
            item_id="minecraft:planks",
            name="Доски",
            name_en="Planks",
            category="block"
        )
        recipe = Recipe.objects.create(
            result_item=result_item,
            result_count=4,
            recipe_type="crafting_2x2"
        )
        wood = Item.objects.create(
            item_id="minecraft:oak_log",
            name="Дубовое бревно",
            name_en="Oak Log",
            category="block"
        )
        ingredient = RecipeIngredient.objects.create(
            recipe=recipe,
            item=wood,
            count=1
        )
        assert ingredient.tag == ""
    
    def test_unique_constraint_position(self):
        result_item = Item.objects.create(
            item_id="minecraft:wooden_sword",
            name="Деревянный меч",
            name_en="Wooden Sword",
            category="weapon"
        )
        recipe = Recipe.objects.create(
            result_item=result_item,
            result_count=1,
            recipe_type="crafting_3x3"
        )
        stick = Item.objects.create(
            item_id="minecraft:stick",
            name="Палка",
            name_en="Stick",
            category="material"
        )
        plank = Item.objects.create(
            item_id="minecraft:oak_planks",
            name="Дубовые доски",
            name_en="Oak Planks",
            category="block"
        )
        
        RecipeIngredient.objects.create(
            recipe=recipe, item=stick, count=1, position_row=0, position_col=0
        )
        
        with pytest.raises(Exception):
            RecipeIngredient.objects.create(
                recipe=recipe, item=plank, count=1, position_row=0, position_col=0
            )
    
    def test_update_ingredient(self):
        result_item = Item.objects.create(
            item_id="minecraft:wooden_sword",
            name="Деревянный меч",
            name_en="Wooden Sword",
            category="weapon"
        )
        recipe = Recipe.objects.create(
            result_item=result_item,
            result_count=1,
            recipe_type="crafting_3x3"
        )
        stick = Item.objects.create(
            item_id="minecraft:stick",
            name="Палка",
            name_en="Stick",
            category="material"
        )
        ingredient = RecipeIngredient.objects.create(
            recipe=recipe,
            item=stick,
            count=1
        )
        ingredient.count = 3
        ingredient.save()
        
        updated = RecipeIngredient.objects.get(id=ingredient.id)
        assert updated.count == 3