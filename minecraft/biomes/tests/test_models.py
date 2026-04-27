import pytest
from biomes.models import Biome
from dimensions.models import Dimension

@pytest.mark.django_db
class TestBiomeModel:
    
    def test_create_biome(self):
        """Тест создания биома"""
        dimension = Dimension.objects.create(name="Overworld", name_ru="Верхний мир")
        biome = Biome.objects.create(
            name="Plains",
            name_ru="Равнины",
            dimension=dimension,
            temperature=0.8
        )
        assert biome.name_ru == "Равнины"
        assert biome.temperature == 0.8
    
    def test_biome_str_method(self):
        """Тест строкового представления"""
        dimension = Dimension.objects.create(name="Overworld", name_ru="Верхний мир")
        biome = Biome.objects.create(
            name="Desert",
            name_ru="Пустыня",
            dimension=dimension
        )
        assert str(biome) == "Пустыня"