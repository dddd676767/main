import pytest
from loot_drops.models import LootDrop
from mobs.models import Mob
from items.models import Item
from versions.models import MinecraftVersion

pytestmark = pytest.mark.django_db

class TestLootDropModel:
    
    def test_create_loot_drop(self):
        mob = Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            name_en="Zombie",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        item = Item.objects.create(
            item_id="minecraft:rotten_flesh",
            name="Гнилая плоть",
            name_en="Rotten Flesh",
            category="material"
        )
        loot = LootDrop.objects.create(
            mob=mob,
            item=item,
            min_count=0,
            max_count=2,
            chance=0.5,
            is_rare=False,
            looting_multiplier=0.1
        )
        assert loot.id is not None
        assert loot.mob == mob
        assert loot.item == item
        assert loot.min_count == 0
        assert loot.max_count == 2
        assert loot.chance == 0.5
        assert loot.is_rare is False
        assert loot.looting_multiplier == 0.1
    
    def test_loot_drop_str_method(self):
        mob = Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            name_en="Zombie",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        item = Item.objects.create(
            item_id="minecraft:iron_ingot",
            name="Железный слиток",
            name_en="Iron Ingot",
            category="material"
        )
        loot = LootDrop.objects.create(
            mob=mob,
            item=item,
            min_count=1,
            max_count=1,
            chance=0.05
        )
        assert str(loot) == "Zombie -> Железный слиток (5.0%)"
    
    def test_loot_drop_chance_range(self):
        mob = Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            name_en="Zombie",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        item = Item.objects.create(
            item_id="minecraft:diamond",
            name="Алмаз",
            name_en="Diamond",
            category="material"
        )
        
        chances = [0.0, 0.25, 0.5, 0.75, 1.0]
        for chance in chances:
            loot = LootDrop.objects.create(
                mob=mob,
                item=item,
                min_count=1,
                max_count=1,
                chance=chance
            )
            assert loot.chance == chance
    
    def test_loot_drop_count_range(self):
        mob = Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            name_en="Zombie",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        item = Item.objects.create(
            item_id="minecraft:rotten_flesh",
            name="Гнилая плоть",
            name_en="Rotten Flesh",
            category="material"
        )
        
        loot = LootDrop.objects.create(
            mob=mob,
            item=item,
            min_count=1,
            max_count=4,
            chance=1.0
        )
        assert loot.min_count == 1
        assert loot.max_count == 4
    
    def test_rare_loot_drop(self):
        mob = Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            name_en="Zombie",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        item = Item.objects.create(
            item_id="minecraft:iron_ingot",
            name="Железный слиток",
            name_en="Iron Ingot",
            category="material"
        )
        loot = LootDrop.objects.create(
            mob=mob,
            item=item,
            min_count=1,
            max_count=1,
            chance=0.025,
            is_rare=True
        )
        assert loot.is_rare is True
    
    def test_loot_drop_with_versions(self):
        version = MinecraftVersion.objects.create(
            version_number="1.21",
            release_date="2024-06-13",
            is_latest=True
        )
        mob = Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            name_en="Zombie",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        item = Item.objects.create(
            item_id="minecraft:rotten_flesh",
            name="Гнилая плоть",
            name_en="Rotten Flesh",
            category="material"
        )
        loot = LootDrop.objects.create(
            mob=mob,
            item=item,
            min_count=1,
            max_count=1,
            chance=1.0
        )
        loot.versions.add(version)
        
        assert loot.versions.count() == 1
        assert version in loot.versions.all()
    
    def test_multiple_drops_for_one_mob(self):
        mob = Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            name_en="Zombie",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        item1 = Item.objects.create(
            item_id="minecraft:rotten_flesh",
            name="Гнилая плоть",
            name_en="Rotten Flesh",
            category="material"
        )
        item2 = Item.objects.create(
            item_id="minecraft:iron_ingot",
            name="Железный слиток",
            name_en="Iron Ingot",
            category="material"
        )
        
        LootDrop.objects.create(mob=mob, item=item1, chance=1.0)
        LootDrop.objects.create(mob=mob, item=item2, chance=0.05)
        
        assert LootDrop.objects.filter(mob=mob).count() == 2
    
    def test_update_loot_drop(self):
        mob = Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            name_en="Zombie",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        item = Item.objects.create(
            item_id="minecraft:rotten_flesh",
            name="Гнилая плоть",
            name_en="Rotten Flesh",
            category="material"
        )
        loot = LootDrop.objects.create(
            mob=mob,
            item=item,
            chance=0.5
        )
        loot.chance = 0.75
        loot.save()
        
        updated = LootDrop.objects.get(id=loot.id)
        assert updated.chance == 0.75