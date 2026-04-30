import pytest
from mechanic_materials.models import MechanicMaterial
from mechanics.models import Mechanic
from items.models import Item

pytestmark = pytest.mark.django_db

class TestMechanicMaterialModel:
    
    def test_create_mechanic_material(self):
        mechanic = Mechanic.objects.create(
            mechanic_id="auto_farm",
            title="Автоматическая ферма",
            title_en="Auto Farm",
            category="farming",
            difficulty="advanced"
        )
        item = Item.objects.create(
            item_id="minecraft:redstone",
            name="Редстоун",
            name_en="Redstone",
            category="redstone"
        )
        material = MechanicMaterial.objects.create(
            mechanic=mechanic,
            item=item,
            count=10,
            is_consumable=True
        )
        assert material.id is not None
        assert material.mechanic == mechanic
        assert material.item == item
        assert material.count == 10
        assert material.is_consumable is True
    
    def test_mechanic_material_str_method(self):
        mechanic = Mechanic.objects.create(
            mechanic_id="auto_farm",
            title="Автоматическая ферма",
            title_en="Auto Farm",
            category="farming",
            difficulty="advanced"
        )
        item = Item.objects.create(
            item_id="minecraft:stone",
            name="Камень",
            name_en="Stone",
            category="block"
        )
        material = MechanicMaterial.objects.create(
            mechanic=mechanic,
            item=item,
            count=64
        )
        assert str(material) == "Камень x64"
    
    def test_multiple_materials_per_mechanic(self):
        mechanic = Mechanic.objects.create(
            mechanic_id="auto_farm",
            title="Автоматическая ферма",
            title_en="Auto Farm",
            category="farming",
            difficulty="advanced"
        )
        stone = Item.objects.create(
            item_id="minecraft:stone",
            name="Камень",
            name_en="Stone",
            category="block"
        )
        redstone = Item.objects.create(
            item_id="minecraft:redstone",
            name="Редстоун",
            name_en="Redstone",
            category="redstone"
        )
        piston = Item.objects.create(
            item_id="minecraft:piston",
            name="Поршень",
            name_en="Piston",
            category="redstone"
        )
        
        MechanicMaterial.objects.create(mechanic=mechanic, item=stone, count=64)
        MechanicMaterial.objects.create(mechanic=mechanic, item=redstone, count=10)
        MechanicMaterial.objects.create(mechanic=mechanic, item=piston, count=4)
        
        assert MechanicMaterial.objects.filter(mechanic=mechanic).count() == 3
    
    def test_material_count_variations(self):
        mechanic = Mechanic.objects.create(
            mechanic_id="test",
            title="Test",
            title_en="Test",
            category="redstone",
            difficulty="beginner"
        )
        item = Item.objects.create(
            item_id="minecraft:stick",
            name="Палка",
            name_en="Stick",
            category="material"
        )
        
        counts = [1, 2, 4, 8, 16, 32, 64]
        for count in counts:
            material = MechanicMaterial.objects.create(
                mechanic=mechanic,
                item=item,
                count=count
            )
            assert material.count == count
    
    def test_is_consumable_default_true(self):
        mechanic = Mechanic.objects.create(
            mechanic_id="test",
            title="Test",
            title_en="Test",
            category="redstone",
            difficulty="beginner"
        )
        item = Item.objects.create(
            item_id="minecraft:stone",
            name="Камень",
            name_en="Stone",
            category="block"
        )
        material = MechanicMaterial.objects.create(
            mechanic=mechanic,
            item=item,
            count=10
        )
        assert material.is_consumable is True
    
    def test_is_consumable_false_for_tools(self):
        mechanic = Mechanic.objects.create(
            mechanic_id="test",
            title="Test",
            title_en="Test",
            category="redstone",
            difficulty="beginner"
        )
        item = Item.objects.create(
            item_id="minecraft:diamond_pickaxe",
            name="Алмазная кирка",
            name_en="Diamond Pickaxe",
            category="tool"
        )
        material = MechanicMaterial.objects.create(
            mechanic=mechanic,
            item=item,
            count=1,
            is_consumable=False
        )
        assert material.is_consumable is False
    
    def test_update_mechanic_material(self):
        mechanic = Mechanic.objects.create(
            mechanic_id="test",
            title="Test",
            title_en="Test",
            category="redstone",
            difficulty="beginner"
        )
        item = Item.objects.create(
            item_id="minecraft:stone",
            name="Камень",
            name_en="Stone",
            category="block"
        )
        material = MechanicMaterial.objects.create(
            mechanic=mechanic,
            item=item,
            count=10
        )
        material.count = 20
        material.save()
        
        updated = MechanicMaterial.objects.get(id=material.id)
        assert updated.count == 20