import pytest
from structures.models import Structure
from versions.models import MinecraftVersion
from dimensions.models import Dimension
from biomes.models import Biome

pytestmark = pytest.mark.django_db

class TestStructureModel:
    
    def test_create_structure(self):
        structure = Structure.objects.create(
            structure_id="minecraft:village",
            name="Village",
            name_en="Village",
            rarity="common",
            description="Структура с жителями",
            images='["village1.png", "village2.png"]'
        )
        assert structure.id is not None
        assert structure.structure_id == "minecraft:village"
        assert structure.name == "Village"
        assert structure.name_en == "Village"
        assert structure.rarity == "common"
        assert structure.description == "Структура с жителями"
        assert structure.images == '["village1.png", "village2.png"]'
    
    def test_structure_str_method(self):
        structure = Structure.objects.create(
            structure_id="minecraft:village",
            name="Village",
            name_en="Village",
            rarity="common"
        )
        assert str(structure) == "Village"
    
    def test_structure_rarity_choices(self):
        rarities = ['common', 'uncommon', 'rare', 'epic']
        for rarity in rarities:
            structure = Structure.objects.create(
                structure_id=f"minecraft:test_{rarity}",
                name=rarity,
                name_en=rarity,
                rarity=rarity
            )
            assert structure.rarity == rarity
    
    def test_structure_with_dimensions(self):
        overworld = Dimension.objects.create(name="Overworld", name_ru="Верхний мир")
        nether = Dimension.objects.create(name="Nether", name_ru="Ад")
        
        structure = Structure.objects.create(
            structure_id="minecraft:village",
            name="Village",
            name_en="Village",
            rarity="common"
        )
        structure.dimensions.add(overworld, nether)
        
        assert structure.dimensions.count() == 2
        assert overworld in structure.dimensions.all()
        assert nether in structure.dimensions.all()
    
    def test_structure_with_biomes(self):
        dimension = Dimension.objects.create(name="Overworld", name_ru="Верхний мир")
        plains = Biome.objects.create(name="Plains", name_ru="Равнины", dimension=dimension)
        desert = Biome.objects.create(name="Desert", name_ru="Пустыня", dimension=dimension)
        
        structure = Structure.objects.create(
            structure_id="minecraft:village",
            name="Village",
            name_en="Village",
            rarity="common"
        )
        structure.biomes.add(plains, desert)
        
        assert structure.biomes.count() == 2
        assert plains in structure.biomes.all()
        assert desert in structure.biomes.all()
    
    def test_structure_with_versions(self):
        version = MinecraftVersion.objects.create(
            version_number="1.21",
            release_date="2024-06-13",
            is_latest=True
        )
        structure = Structure.objects.create(
            structure_id="minecraft:village",
            name="Village",
            name_en="Village",
            rarity="common"
        )
        structure.versions.add(version)
        
        assert structure.versions.count() == 1
        assert version in structure.versions.all()
    
    def test_structure_images_optional(self):
        structure = Structure.objects.create(
            structure_id="minecraft:village",
            name="Village",
            name_en="Village",
            rarity="common"
        )
        assert structure.images == []
    
    def test_update_structure(self):
        structure = Structure.objects.create(
            structure_id="minecraft:village",
            name="Village",
            name_en="Village",
            rarity="common"
        )
        structure.rarity = "rare"
        structure.save()
        
        updated = Structure.objects.get(id=structure.id)
        assert updated.rarity == "rare"