import pytest
from mechanics.models import Mechanic
from versions.models import MinecraftVersion

pytestmark = pytest.mark.django_db

class TestMechanicModel:
    
    def test_create_mechanic(self):
        mechanic = Mechanic.objects.create(
            mechanic_id="redstone_circuit",
            title="Редстоун схема",
            title_en="Redstone Circuit",
            category="redstone",
            difficulty="beginner",
            description="Базовая схема редстоуна",
            tags='["redstone", "basic"]',
            estimated_time=10
        )
        assert mechanic.id is not None
        assert mechanic.mechanic_id == "redstone_circuit"
        assert mechanic.title == "Редстоун схема"
        assert mechanic.title_en == "Redstone Circuit"
        assert mechanic.category == "redstone"
        assert mechanic.difficulty == "beginner"
        assert mechanic.description == "Базовая схема редстоуна"
        assert mechanic.tags == '["redstone", "basic"]'
        assert mechanic.estimated_time == 10
    
    def test_mechanic_str_method(self):
        mechanic = Mechanic.objects.create(
            mechanic_id="farm",
            title="Ферма",
            title_en="Farm",
            category="farming",
            difficulty="intermediate"
        )
        assert str(mechanic) == "Ферма"
    
    def test_mechanic_categories(self):
        categories = ['redstone', 'farming', 'breeding', 'enchanting', 'brewing', 'transport', 'storage']
        for category in categories:
            mechanic = Mechanic.objects.create(
                mechanic_id=f"test_{category}",
                title=category,
                title_en=category,
                category=category,
                difficulty="beginner"
            )
            assert mechanic.category == category
    
    def test_mechanic_difficulties(self):
        difficulties = ['beginner', 'intermediate', 'advanced', 'experts']
        for difficulty in difficulties:
            mechanic = Mechanic.objects.create(
                mechanic_id=f"test_{difficulty}",
                title=difficulty,
                title_en=difficulty,
                category="redstone",
                difficulty=difficulty
            )
            assert mechanic.difficulty == difficulty
    
    def test_mechanic_with_versions(self):
        version = MinecraftVersion.objects.create(
            version_number="1.21",
            release_date="2024-06-13",
            is_latest=True
        )
        mechanic = Mechanic.objects.create(
            mechanic_id="auto_farm",
            title="Автоматическая ферма",
            title_en="Auto Farm",
            category="farming",
            difficulty="advanced"
        )
        mechanic.versions.add(version)
        
        assert mechanic.versions.count() == 1
        assert version in mechanic.versions.all()
    
    def test_estimated_time_default(self):
        mechanic = Mechanic.objects.create(
            mechanic_id="simple",
            title="Просто",
            title_en="Simple",
            category="redstone",
            difficulty="beginner"
        )
        assert mechanic.estimated_time == 10
    
    def test_estimated_time_variations(self):
        times = [5, 10, 15, 30, 60, 120]
        for time in times:
            mechanic = Mechanic.objects.create(
                mechanic_id=f"test_time_{time}",
                title=f"Time {time}",
                title_en=f"Time {time}",
                category="redstone",
                difficulty="beginner",
                estimated_time=time
            )
            assert mechanic.estimated_time == time
    
    def test_tags_optional(self):
        mechanic = Mechanic.objects.create(
            mechanic_id="no_tags",
            title="Без тегов",
            title_en="No Tags",
            category="redstone",
            difficulty="beginner"
        )
        assert mechanic.tags == []
    
    def test_update_mechanic(self):
        mechanic = Mechanic.objects.create(
            mechanic_id="test",
            title="Тест",
            title_en="Test",
            category="redstone",
            difficulty="beginner"
        )
        mechanic.difficulty = "advanced"
        mechanic.save()
        
        updated = Mechanic.objects.get(id=mechanic.id)
        assert updated.difficulty == "advanced"