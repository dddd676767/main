import pytest
from items.models import Item
from versions.models import MinecraftVersion

pytestmark = pytest.mark.django_db

class TestItemModel:
    
    def test_create_item(self):
        item = Item.objects.create(
            item_id="minecraft:iron_ingot",
            name="Железный слиток",
            name_en="Iron Ingot",
            category="material",
            stack_size=64,
            rarity="common"
        )
        assert item.id is not None
        assert item.item_id == "minecraft:iron_ingot"
        assert item.name == "Железный слиток"
        assert item.name_en == "Iron Ingot"
        assert item.category == "material"
        assert item.stack_size == 64
        assert item.rarity == "common"
        assert item.is_removed is False
    
    def test_item_str_method(self):
        item = Item.objects.create(
            item_id="minecraft:diamond",
            name="Алмаз",
            name_en="Diamond",
            category="material"
        )
        assert str(item) == "Алмаз"
    
    def test_all_categories(self):
        dimension = MinecraftVersion.objects.create(
            version_number="1.21",
            release_date="2024-06-13",
            is_latest=True
        )
        
        categories = ['block', 'tool', 'weapon', 'armor', 'food', 'material', 'redstone', 'potion']
        for category in categories:
            item = Item.objects.create(
                item_id=f"minecraft:test_{category}",
                name=category,
                name_en=category,
                category=category,
                stack_size=64,
                rarity="common"
            )
            item.versions.add(dimension)
            assert item.category == category
    
    def test_stack_size_variations(self):
        item_64 = Item.objects.create(
            item_id="minecraft:dirt",
            name="Земля",
            name_en="Dirt",
            category="block",
            stack_size=64
        )
        item_16 = Item.objects.create(
            item_id="minecraft:ender_pearl",
            name="Жемчуг Края",
            name_en="Ender Pearl",
            category="material",
            stack_size=16
        )
        item_1 = Item.objects.create(
            item_id="minecraft:diamond_sword",
            name="Алмазный меч",
            name_en="Diamond Sword",
            category="weapon",
            stack_size=1
        )
        
        assert item_64.stack_size == 64
        assert item_16.stack_size == 16
        assert item_1.stack_size == 1
    
    def test_rarity_levels(self):
        rarities = ['common', 'uncommon', 'rare', 'epic']
        for rarity in rarities:
            item = Item.objects.create(
                item_id=f"minecraft:{rarity}_item",
                name=rarity,
                name_en=rarity,
                category="material",
                stack_size=64,
                rarity=rarity
            )
            assert item.rarity == rarity
    
    def test_item_with_versions(self):
        version_120 = MinecraftVersion.objects.create(
            version_number="1.20",
            release_date="2023-12-07",
            is_latest=False
        )
        version_121 = MinecraftVersion.objects.create(
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
        item.versions.add(version_120, version_121)
        
        assert item.versions.count() == 2
        assert version_120 in item.versions.all()
        assert version_121 in item.versions.all()
    
    def test_item_default_values(self):
        item = Item.objects.create(
            item_id="minecraft:stick",
            name="Палка",
            name_en="Stick",
            category="material"
        )
        assert item.stack_size == 64
        assert item.rarity == "common"
        assert item.is_removed is False
    
    def test_item_id_unique(self):
        Item.objects.create(
            item_id="minecraft:diamond",
            name="Алмаз",
            name_en="Diamond",
            category="material"
        )
        with pytest.raises(Exception):
            Item.objects.create(
                item_id="minecraft:diamond",
                name="Другой алмаз",
                name_en="Other Diamond",
                category="material"
            )
    
    def test_update_item(self):
        item = Item.objects.create(
            item_id="minecraft:stone",
            name="Камень",
            name_en="Stone",
            category="block"
        )
        item.name = "Булыжник"
        item.save()
        
        updated = Item.objects.get(id=item.id)
        assert updated.name == "Булыжник"
    
    def test_mark_item_as_removed(self):
        item = Item.objects.create(
            item_id="minecraft:old_item",
            name="Старый предмет",
            name_en="Old Item",
            category="material",
            is_removed=False
        )
        assert item.is_removed is False
        item.is_removed = True
        item.save()
        
        updated = Item.objects.get(id=item.id)
        assert updated.is_removed is True