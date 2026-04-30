import pytest
from chest_loots.models import ChestLootItem
from structures.models import Structure
from structure_chests.models import StructureChest
from items.models import Item

pytestmark = pytest.mark.django_db

class TestChestLootItemModel:
    
    def test_create_chest_loot_item(self):
        structure = Structure.objects.create(
            structure_id="minecraft:village",
            name="Village",
            name_en="Village",
            rarity="common"
        )
        chest = StructureChest.objects.create(
            structure=structure,
            name="Сундук кузнеца"
        )
        item = Item.objects.create(
            item_id="minecraft:iron_ingot",
            name="Железный слиток",
            name_en="Iron Ingot",
            category="material"
        )
        loot = ChestLootItem.objects.create(
            chest=chest,
            item=item,
            min_count=1,
            max_count=5,
            chance=0.5,
            weight=10
        )
        assert loot.id is not None
        assert loot.chest == chest
        assert loot.item == item
        assert loot.min_count == 1
        assert loot.max_count == 5
        assert loot.chance == 0.5
        assert loot.weight == 10
    
    def test_chest_loot_item_str_method(self):
        structure = Structure.objects.create(
            structure_id="minecraft:village",
            name="Village",
            name_en="Village",
            rarity="common"
        )
        chest = StructureChest.objects.create(
            structure=structure,
            name="Сундук"
        )
        item = Item.objects.create(
            item_id="minecraft:diamond",
            name="Алмаз",
            name_en="Diamond",
            category="material"
        )
        loot = ChestLootItem.objects.create(
            chest=chest,
            item=item,
            min_count=1,
            max_count=1,
            chance=0.1
        )
        assert str(loot) == "Сундук: Алмаз (10.0%)"
    
    def test_multiple_loot_items_per_chest(self):
        structure = Structure.objects.create(
            structure_id="minecraft:village",
            name="Village",
            name_en="Village",
            rarity="common"
        )
        chest = StructureChest.objects.create(
            structure=structure,
            name="Сундук"
        )
        item1 = Item.objects.create(
            item_id="minecraft:iron_ingot",
            name="Железный слиток",
            name_en="Iron Ingot",
            category="material"
        )
        item2 = Item.objects.create(
            item_id="minecraft:gold_ingot",
            name="Золотой слиток",
            name_en="Gold Ingot",
            category="material"
        )
        item3 = Item.objects.create(
            item_id="minecraft:diamond",
            name="Алмаз",
            name_en="Diamond",
            category="material"
        )
        
        ChestLootItem.objects.create(chest=chest, item=item1, min_count=1, max_count=3, chance=0.5)
        ChestLootItem.objects.create(chest=chest, item=item2, min_count=1, max_count=2, chance=0.3)
        ChestLootItem.objects.create(chest=chest, item=item3, min_count=1, max_count=1, chance=0.1)
        
        assert ChestLootItem.objects.filter(chest=chest).count() == 3
    
    def test_loot_count_range(self):
        structure = Structure.objects.create(
            structure_id="minecraft:village",
            name="Village",
            name_en="Village",
            rarity="common"
        )
        chest = StructureChest.objects.create(
            structure=structure,
            name="Сундук"
        )
        item = Item.objects.create(
            item_id="minecraft:emerald",
            name="Изумруд",
            name_en="Emerald",
            category="material"
        )
        
        loot = ChestLootItem.objects.create(
            chest=chest,
            item=item,
            min_count=1,
            max_count=4,
            chance=1.0
        )
        assert loot.min_count == 1
        assert loot.max_count == 4
    
    def test_chance_range(self):
        structure = Structure.objects.create(
            structure_id="minecraft:village",
            name="Village",
            name_en="Village",
            rarity="common"
        )
        chest = StructureChest.objects.create(
            structure=structure,
            name="Сундук"
        )
        item = Item.objects.create(
            item_id="minecraft:diamond",
            name="Алмаз",
            name_en="Diamond",
            category="material"
        )
        
        chances = [0.0, 0.25, 0.5, 0.75, 1.0]
        for chance in chances:
            loot = ChestLootItem.objects.create(
                chest=chest,
                item=item,
                min_count=1,
                max_count=1,
                chance=chance
            )
            assert loot.chance == chance
    
    def test_weight_default(self):
        structure = Structure.objects.create(
            structure_id="minecraft:village",
            name="Village",
            name_en="Village",
            rarity="common"
        )
        chest = StructureChest.objects.create(
            structure=structure,
            name="Сундук"
        )
        item = Item.objects.create(
            item_id="minecraft:diamond",
            name="Алмаз",
            name_en="Diamond",
            category="material"
        )
        loot = ChestLootItem.objects.create(
            chest=chest,
            item=item,
            min_count=1,
            max_count=1,
            chance=0.1
        )
        assert loot.weight == 1
    
    def test_update_chest_loot(self):
        structure = Structure.objects.create(
            structure_id="minecraft:village",
            name="Village",
            name_en="Village",
            rarity="common"
        )
        chest = StructureChest.objects.create(
            structure=structure,
            name="Сундук"
        )
        item = Item.objects.create(
            item_id="minecraft:diamond",
            name="Алмаз",
            name_en="Diamond",
            category="material"
        )
        loot = ChestLootItem.objects.create(
            chest=chest,
            item=item,
            min_count=1,
            max_count=1,
            chance=0.5
        )
        loot.chance = 0.8
        loot.save()
        
        updated = ChestLootItem.objects.get(id=loot.id)
        assert updated.chance == 0.8