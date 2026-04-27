import pytest
from dimensions.models import Dimension

@pytest.mark.django_db
class TestDimensionModel:
    
    def test_create_dimension(self):
        """Тест создания измерения"""
        dimension = Dimension.objects.create(
            name="Overworld",
            name_ru="Верхний мир",
            description="Основной мир Minecraft"
        )
        assert dimension.name == "Overworld"
        assert dimension.name_ru == "Верхний мир"
    
    def test_dimension_str_method(self):
        """Тест строкового представления"""
        dimension = Dimension.objects.create(
            name="Nether",
            name_ru="Ад"
        )
        assert str(dimension) == "Ад"