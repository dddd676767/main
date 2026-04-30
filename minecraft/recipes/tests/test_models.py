import pytest
from recipes.models import Recipe
from items.models import Item
from versions.models import MinecraftVersion

pytestmark = pytest.mark.django_db

class TestRecipeModel:
    
    def test_create_recipe(self):
        item = Item.objects.create(
            item_id="minecraft:chest",
            name="Сундук",
            name_en="Chest",
            category="block"
        )
        recipe = Recipe.objects.create(
            result_item=item,
            result_count=1,
            recipe_type="crafting_3x3",
            shape='["WWW","W W","WWW"]',
            group="storage"
        )
        assert recipe.id is not None
        assert recipe.result_item == item
        assert recipe.result_count == 1
        assert recipe.recipe_type == "crafting_3x3"
        assert recipe.shape == '["WWW","W W","WWW"]'
        assert recipe.group == "storage"
    
    def test_recipe_str_method(self):
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
        assert str(recipe) == "Крафт: Палка x4"
    
    def test_recipe_types(self):
        item = Item.objects.create(
            item_id="minecraft:iron_ingot",
            name="Железный слиток",
            name_en="Iron Ingot",
            category="material"
        )
        recipe_types = ['crafting_2x2', 'crafting_3x3', 'smelting', 'blasting', 'smoking', 'campfire', 'smithing', 'stonecutting', 'brewing']
        
        for rtype in recipe_types:
            recipe = Recipe.objects.create(
                result_item=item,
                result_count=1,
                recipe_type=rtype
            )
            assert recipe.recipe_type == rtype
    
    def test_recipe_result_count_variations(self):
        item = Item.objects.create(
            item_id="minecraft:planks",
            name="Доски",
            name_en="Planks",
            category="material"
        )
        
        counts = [1, 4, 8, 16, 32, 64]
        for count in counts:
            recipe = Recipe.objects.create(
                result_item=item,
                result_count=count,
                recipe_type="crafting_3x3"
            )
            assert recipe.result_count == count
    
    def test_recipe_shape_can_be_null(self):
        item = Item.objects.create(
            item_id="minecraft:iron_ingot",
            name="Железный слиток",
            name_en="Iron Ingot",
            category="material"
        )
        recipe = Recipe.objects.create(
            result_item=item,
            result_count=1,
            recipe_type="smelting"
        )
        assert recipe.shape is None
    
    def test_recipe_group_optional(self):
        item = Item.objects.create(
            item_id="minecraft:diamond",
            name="Алмаз",
            name_en="Diamond",
            category="material"
        )
        recipe = Recipe.objects.create(
            result_item=item,
            result_count=1,
            recipe_type="crafting_3x3"
        )
        assert recipe.group == ""
    
    def test_recipe_with_versions(self):
        version = MinecraftVersion.objects.create(
            version_number="1.21",
            release_date="2024-06-13",
            is_latest=True
        )
        item = Item.objects.create(
            item_id="minecraft:netherite_ingot",
            name="Незеритовый слиток",
            name_en="Netherite Ingot",
            category="material"
        )
        recipe = Recipe.objects.create(
            result_item=item,
            result_count=1,
            recipe_type="crafting_3x3"
        )
        recipe.versions.add(version)
        
        assert recipe.versions.count() == 1
        assert version in recipe.versions.all()
    
    def test_recipe_requires_result_item(self):
        with pytest.raises(Exception):
            Recipe.objects.create(
                result_count=1,
                recipe_type="crafting_3x3"
            )
    
    def test_update_recipe(self):
        item = Item.objects.create(
            item_id="minecraft:stick",
            name="Палка",
            name_en="Stick",
            category="material"
        )
        recipe = Recipe.objects.create(
            result_item=item,
            result_count=2,
            recipe_type="crafting_2x2"
        )
        recipe.result_count = 4
        recipe.save()
        
        updated = Recipe.objects.get(id=recipe.id)
        assert updated.result_count == 4