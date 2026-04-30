import pytest
from biomes.models import Biome
from dimensions.models import Dimension

pytestmark = pytest.mark.django_db

class TestBiomeModel:
    
    def test_create_biome(self):
        dimension = Dimension.objects.create(name="Overworld", name_ru="Верхний мир")
        biome = Biome.objects.create(
            name="Plains",
            name_ru="Равнины",
            dimension=dimension,
            temperature=0.8,
            description="Равнинный биом"
        )
        assert biome.id is not None
        assert biome.name == "Plains"
        assert biome.name_ru == "Равнины"
        assert biome.dimension == dimension
        assert biome.temperature == 0.8
        assert biome.description == "Равнинный биом"
    
    def test_biome_str_method(self):
        dimension = Dimension.objects.create(name="Overworld", name_ru="Верхний мир")
        biome = Biome.objects.create(
            name="Desert",
            name_ru="Пустыня",
            dimension=dimension
        )
        assert str(biome) == "Пустыня"
    
    def test_biome_belongs_to_dimension(self):
        overworld = Dimension.objects.create(name="Overworld", name_ru="Верхний мир")
        nether = Dimension.objects.create(name="Nether", name_ru="Ад")
        
        plains = Biome.objects.create(name="Plains", name_ru="Равнины", dimension=overworld)
        wastes = Biome.objects.create(name="Nether Wastes", name_ru="Пустоши", dimension=nether)
        
        assert plains.dimension.name == "Overworld"
        assert wastes.dimension.name == "Nether"
    
    def test_biome_temperature_default(self):
        dimension = Dimension.objects.create(name="Overworld", name_ru="Верхний мир")
        biome = Biome.objects.create(
            name="Forest",
            name_ru="Лес",
            dimension=dimension
        )
        assert biome.temperature == 0.5
    
    def test_biome_temperature_range(self):
        dimension = Dimension.objects.create(name="Overworld", name_ru="Верхний мир")
        
        cold_biome = Biome.objects.create(
            name="Ice Plains",
            name_ru="Ледяные равнины",
            dimension=dimension,
            temperature=0.0
        )
        hot_biome = Biome.objects.create(
            name="Desert",
            name_ru="Пустыня",
            dimension=dimension,
            temperature=2.0
        )
        
        assert cold_biome.temperature == 0.0
        assert hot_biome.temperature == 2.0
    
    def test_multiple_biomes_same_dimension(self):
        overworld = Dimension.objects.create(name="Overworld", name_ru="Верхний мир")
        
        biomes = ["Plains", "Desert", "Forest", "Jungle"]
        for biome_name in biomes:
            Biome.objects.create(
                name=biome_name,
                name_ru=biome_name,
                dimension=overworld
            )
        
        assert Biome.objects.filter(dimension=overworld).count() == 4
    
    def test_delete_dimension_cascades_to_biomes(self):
        dimension = Dimension.objects.create(name="Overworld", name_ru="Верхний мир")
        Biome.objects.create(name="Plains", name_ru="Равнины", dimension=dimension)
        Biome.objects.create(name="Forest", name_ru="Лес", dimension=dimension)
        
        assert Biome.objects.count() == 2
        dimension.delete()
        assert Biome.objects.count() == 0