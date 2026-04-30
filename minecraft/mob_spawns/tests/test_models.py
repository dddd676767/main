import pytest
from mob_spawns.models import MobSpawnCondition
from mobs.models import Mob
from dimensions.models import Dimension
from biomes.models import Biome

pytestmark = pytest.mark.django_db

class TestMobSpawnConditionModel:
    
    def test_create_mob_spawn_condition(self):
        mob = Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            name_en="Zombie",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        dimension = Dimension.objects.create(name="Overworld", name_ru="Верхний мир")
        biome = Biome.objects.create(name="Plains", name_ru="Равнины", dimension=dimension)
        
        condition = MobSpawnCondition.objects.create(
            mob=mob,
            biome=biome,
            dimension=dimension,
            min_y=0,
            max_y=64,
            light_level_max=7,
            only_at_night=True
        )
        assert condition.id is not None
        assert condition.mob == mob
        assert condition.biome == biome
        assert condition.dimension == dimension
        assert condition.min_y == 0
        assert condition.max_y == 64
        assert condition.light_level_max == 7
        assert condition.only_at_night is True
    
    def test_mob_spawn_condition_str_method(self):
        mob = Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            name_en="Zombie",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        dimension = Dimension.objects.create(name="Overworld", name_ru="Верхний мир")
        condition = MobSpawnCondition.objects.create(
            mob=mob,
            dimension=dimension
        )
        # Исправлено: используем name (английское), так как __str__ использует dimension.name
        assert str(condition) == "Спавн Zombie в Overworld"
    
    def test_spawn_condition_without_biome(self):
        mob = Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            name_en="Zombie",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        dimension = Dimension.objects.create(name="Nether", name_ru="Ад")
        condition = MobSpawnCondition.objects.create(
            mob=mob,
            dimension=dimension
        )
        assert condition.biome is None
    
    def test_spawn_condition_y_level_range(self):
        mob = Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            name_en="Zombie",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        dimension = Dimension.objects.create(name="Overworld", name_ru="Верхний мир")
        
        condition = MobSpawnCondition.objects.create(
            mob=mob,
            dimension=dimension,
            min_y=0,
            max_y=128
        )
        assert condition.min_y == 0
        assert condition.max_y == 128
    
    def test_spawn_condition_y_level_optional(self):
        mob = Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            name_en="Zombie",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        dimension = Dimension.objects.create(name="Overworld", name_ru="Верхний мир")
        condition = MobSpawnCondition.objects.create(
            mob=mob,
            dimension=dimension
        )
        assert condition.min_y is None
        assert condition.max_y is None
    
    def test_light_level_max_default(self):
        mob = Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            name_en="Zombie",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        dimension = Dimension.objects.create(name="Overworld", name_ru="Верхний мир")
        condition = MobSpawnCondition.objects.create(
            mob=mob,
            dimension=dimension
        )
        assert condition.light_level_max == 7
    
    def test_light_level_max_variations(self):
        mob = Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            name_en="Zombie",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        dimension = Dimension.objects.create(name="Overworld", name_ru="Верхний мир")
        
        light_levels = [0, 4, 7, 11, 15]
        for light in light_levels:
            condition = MobSpawnCondition.objects.create(
                mob=mob,
                dimension=dimension,
                light_level_max=light
            )
            assert condition.light_level_max == light
    
    def test_only_at_night_default_false(self):
        mob = Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            name_en="Zombie",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        dimension = Dimension.objects.create(name="Overworld", name_ru="Верхний мир")
        condition = MobSpawnCondition.objects.create(
            mob=mob,
            dimension=dimension
        )
        assert condition.only_at_night is False
    
    def test_multiple_spawn_conditions_for_one_mob(self):
        mob = Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            name_en="Zombie",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        overworld = Dimension.objects.create(name="Overworld", name_ru="Верхний мир")
        nether = Dimension.objects.create(name="Nether", name_ru="Ад")
        
        MobSpawnCondition.objects.create(mob=mob, dimension=overworld)
        MobSpawnCondition.objects.create(mob=mob, dimension=nether)
        
        assert MobSpawnCondition.objects.filter(mob=mob).count() == 2
    
    def test_update_spawn_condition(self):
        mob = Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            name_en="Zombie",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        dimension = Dimension.objects.create(name="Overworld", name_ru="Верхний мир")
        condition = MobSpawnCondition.objects.create(
            mob=mob,
            dimension=dimension,
            light_level_max=7
        )
        condition.light_level_max = 0
        condition.save()
        
        updated = MobSpawnCondition.objects.get(id=condition.id)
        assert updated.light_level_max == 0