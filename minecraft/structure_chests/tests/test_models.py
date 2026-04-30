import pytest
from structure_chests.models import StructureChest
from structures.models import Structure

pytestmark = pytest.mark.django_db

class TestStructureChestModel:
    
    def test_create_structure_chest(self):
        structure = Structure.objects.create(
            structure_id="minecraft:village",
            name="Village",
            name_en="Village",
            rarity="common"
        )
        chest = StructureChest.objects.create(
            structure=structure,
            name="Сундук кузнеца",
            position_description="В кузнице",
            average_value=50
        )
        assert chest.id is not None
        assert chest.structure == structure
        assert chest.name == "Сундук кузнеца"
        assert chest.position_description == "В кузнице"
        assert chest.average_value == 50
    
    def test_structure_chest_str_method(self):
        structure = Structure.objects.create(
            structure_id="minecraft:village",
            name="Village",
            name_en="Village",
            rarity="common"
        )
        chest = StructureChest.objects.create(
            structure=structure,
            name="Сундук"
        )
        assert str(chest) == "Village - Сундук"
    
    def test_multiple_chests_per_structure(self):
        structure = Structure.objects.create(
            structure_id="minecraft:village",
            name="Village",
            name_en="Village",
            rarity="common"
        )
        StructureChest.objects.create(structure=structure, name="Сундук кузнеца")
        StructureChest.objects.create(structure=structure, name="Сундук мясника")
        StructureChest.objects.create(structure=structure, name="Сундук картографа")
        
        assert StructureChest.objects.filter(structure=structure).count() == 3
    
    def test_position_description_optional(self):
        structure = Structure.objects.create(
            structure_id="minecraft:village",
            name="Village",
            name_en="Village",
            rarity="common"
        )
        chest = StructureChest.objects.create(
            structure=structure,
            name="Сундук"
        )
        assert chest.position_description == ""
    
    def test_average_value_default(self):
        structure = Structure.objects.create(
            structure_id="minecraft:village",
            name="Village",
            name_en="Village",
            rarity="common"
        )
        chest = StructureChest.objects.create(
            structure=structure,
            name="Сундук"
        )
        assert chest.average_value == 0
    
    def test_update_structure_chest(self):
        structure = Structure.objects.create(
            structure_id="minecraft:village",
            name="Village",
            name_en="Village",
            rarity="common"
        )
        chest = StructureChest.objects.create(
            structure=structure,
            name="Сундук",
            average_value=50
        )
        chest.average_value = 100
        chest.save()
        
        updated = StructureChest.objects.get(id=chest.id)
        assert updated.average_value == 100