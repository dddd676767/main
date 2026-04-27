import pytest
from mobs.models import Mob

@pytest.mark.django_db
class TestMobModel:
    
    def test_create_mob(self):
        mob = Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            health=20.0,
            damage=3.0,
            behavior="hostile",
            category="monster",
            experience=5,
            description="Враждебный моб"
        )
        assert mob.name == "Zombie"
        assert mob.health == 20.0
    
    def test_mob_str_method(self):
        mob = Mob.objects.create(
            mob_id="minecraft:creeper",
            name="Creeper",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        assert str(mob) == "Creeper"
    
    def test_mob_behavior_choices(self):
        for behavior, display_name in Mob.BEHAVIOR_CHOICES:
            mob = Mob.objects.create(
                mob_id=f"test:{behavior}",
                name=display_name,
                health=10.0,
                behavior=behavior,
                category="monster"
            )
            assert mob.behavior == behavior