import pytest
from dimensions.models import Dimension

pytestmark = pytest.mark.django_db

class TestDimensionModel:
    
    def test_create_dimension(self):
        dimension = Dimension.objects.create(
            name="Overworld",
            name_ru="Верхний мир",
            description="Основной мир Minecraft",
            icon_path="icons/overworld.png"
        )
        assert dimension.id is not None
        assert dimension.name == "Overworld"
        assert dimension.name_ru == "Верхний мир"
        assert dimension.description == "Основной мир Minecraft"
        assert dimension.icon_path == "icons/overworld.png"
    
    def test_dimension_str_method(self):
        dimension = Dimension.objects.create(
            name="Nether",
            name_ru="Ад"
        )
        assert str(dimension) == "Ад"
    
    def test_dimension_without_description(self):
        dimension = Dimension.objects.create(
            name="End",
            name_ru="Энд"
        )
        assert dimension.description == ""
    
    def test_all_dimensions_can_be_created(self):
        dimensions_data = [
            ("Overworld", "Верхний мир"),
            ("Nether", "Ад"),
            ("End", "Энд"),
        ]
        for name, name_ru in dimensions_data:
            Dimension.objects.create(name=name, name_ru=name_ru)
        
        assert Dimension.objects.count() == 3
    
    def test_dimension_name_can_duplicate(self):
        """Поле name не имеет unique=True, поэтому дубликаты разрешены"""
        Dimension.objects.create(name="Overworld", name_ru="Верхний мир")
        dimension2 = Dimension.objects.create(name="Overworld", name_ru="Другой мир")
        assert Dimension.objects.filter(name="Overworld").count() == 2
    
    def test_dimension_icon_path_optional(self):
        dimension = Dimension.objects.create(
            name="Custom",
            name_ru="Кастомный"
        )
        assert dimension.icon_path == ""
    
    def test_update_dimension(self):
        dimension = Dimension.objects.create(
            name="Overworld",
            name_ru="Верхний мир"
        )
        dimension.name_ru = "Мир"
        dimension.save()
        
        updated = Dimension.objects.get(id=dimension.id)
        assert updated.name_ru == "Мир"