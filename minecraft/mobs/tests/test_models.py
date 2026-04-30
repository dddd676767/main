import pytest
from mobs.models import Mob
from versions.models import MinecraftVersion
from dimensions.models import Dimension
from biomes.models import Biome

pytestmark = pytest.mark.django_db

class TestMobModel:
    
    def test_create_mob(self):
        mob = Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            name_en="Zombie",
            health=20.0,
            damage=3.0,
            behavior="hostile",
            category="monster",
            experience=5,
            description="Классический враждебный моб"
        )
        assert mob.id is not None
        assert mob.mob_id == "minecraft:zombie"
        assert mob.name == "Zombie"
        assert mob.health == 20.0
        assert mob.damage == 3.0
        assert mob.behavior == "hostile"
        assert mob.category == "monster"
        assert mob.experience == 5
        assert mob.description == "Классический враждебный моб"
    
    def test_mob_str_method(self):
        mob = Mob.objects.create(
            mob_id="minecraft:creeper",
            name="Creeper",
            name_en="Creeper",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        assert str(mob) == "Creeper"
    
    def test_mob_behavior_choices(self):
        behaviors = ['passive', 'neutral', 'hostile', 'boss', 'tameable']
        for behavior in behaviors:
            mob = Mob.objects.create(
                mob_id=f"test:{behavior}",
                name=behavior,
                name_en=behavior,
                health=10.0,
                behavior=behavior,
                category="monster"
            )
            assert mob.behavior == behavior
    
    def test_mob_category_choices(self):
        categories = ['animal', 'monster', 'ambient', 'aquatic', 'villager', 'undead', 'arthropod', 'illager']
        for category in categories:
            mob = Mob.objects.create(
                mob_id=f"test:{category}",
                name=category,
                name_en=category,
                health=10.0,
                behavior="passive",
                category=category
            )
            assert mob.category == category
    
    def test_mob_health_variations(self):
        mobs_data = [
            ("zombie", 20.0),
            ("bat", 6.0),
            ("ender_dragon", 200.0),
            ("wither", 300.0),
        ]
        for mob_id, health in mobs_data:
            mob = Mob.objects.create(
                mob_id=f"minecraft:{mob_id}",
                name=mob_id,
                name_en=mob_id,
                health=health,
                behavior="hostile",
                category="monster"
            )
            assert mob.health == health
    
    def test_mob_damage_variations(self):
        mobs_data = [
            ("zombie", 3.0),
            ("creeper", 0.0),
            ("ender_dragon", 15.0),
        ]
        for mob_id, damage in mobs_data:
            mob = Mob.objects.create(
                mob_id=f"minecraft:{mob_id}",
                name=mob_id,
                name_en=mob_id,
                health=20.0,
                damage=damage,
                behavior="hostile",
                category="monster"
            )
            assert mob.damage == damage
    
    def test_mob_with_versions(self):
        version = MinecraftVersion.objects.create(
            version_number="1.21",
            release_date="2024-06-13",
            is_latest=True
        )
        mob = Mob.objects.create(
            mob_id="minecraft:warden",
            name="Warden",
            name_en="Warden",
            health=500.0,
            behavior="hostile",
            category="monster"
        )
        mob.versions.add(version)
        
        assert mob.versions.count() == 1
        assert version in mob.versions.all()
    
    def test_mob_with_spawns_in(self):
        overworld = Dimension.objects.create(name="Overworld", name_ru="Верхний мир")
        nether = Dimension.objects.create(name="Nether", name_ru="Ад")
        
        mob = Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            name_en="Zombie",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        mob.spawns_in.add(overworld, nether)
        
        assert mob.spawns_in.count() == 2
        assert overworld in mob.spawns_in.all()
        assert nether in mob.spawns_in.all()
    
    def test_mob_with_biomes(self):
        overworld = Dimension.objects.create(name="Overworld", name_ru="Верхний мир")
        plains = Biome.objects.create(name="Plains", name_ru="Равнины", dimension=overworld)
        desert = Biome.objects.create(name="Desert", name_ru="Пустыня", dimension=overworld)
        
        mob = Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            name_en="Zombie",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        mob.biomes.add(plains, desert)
        
        assert mob.biomes.count() == 2
        assert plains in mob.biomes.all()
        assert desert in mob.biomes.all()
    
    def test_mob_light_level_spawn(self):
        mob = Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            name_en="Zombie",
            health=20.0,
            behavior="hostile",
            category="monster",
            light_level=7
        )
        assert mob.light_level == 7
    
    def test_mob_experience_default(self):
        mob = Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            name_en="Zombie",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        assert mob.experience == 0
    
    def test_mob_experience_variations(self):
        mobs_data = [
            ("zombie", 5),
            ("ender_dragon", 12000),
            ("villager", 0),
        ]
        for mob_id, exp in mobs_data:
            mob = Mob.objects.create(
                mob_id=f"minecraft:{mob_id}",
                name=mob_id,
                name_en=mob_id,
                health=20.0,
                behavior="passive",
                category="animal",
                experience=exp
            )
            assert mob.experience == exp
    
    def test_update_mob(self):
        mob = Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            name_en="Zombie",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        mob.health = 30.0
        mob.save()
        
        updated = Mob.objects.get(id=mob.id)
        assert updated.health == 30.0