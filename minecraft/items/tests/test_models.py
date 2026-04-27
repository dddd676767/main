import pytest
from items.models import Item

@pytest.mark.django_db
class TestItemModel:
    
    def test_create_item(self):
        item = Item.objects.create(
            item_id="minecraft:iron_ingot",
            name="Железный слиток",
            name_en="Iron Ingot",
            category="material"
        )
        assert item.name == "Железный слиток"
    
    def test_item_str_method(self):
        item = Item.objects.create(
            item_id="minecraft:diamond",
            name="Алмаз",
            name_en="Diamond",
            category="material"
        )
        assert str(item) == "Алмаз"
    
    def test_item_category_choices(self):
        for category, display_name in Item.CATEGORY_CHOICES:
            item = Item.objects.create(
                item_id=f"test:{category}",
                name=display_name,
                name_en=category,
                category=category
            )
            assert item.category == category
    
    def test_item_with_versions(self, test_version):
        item = Item.objects.create(
            item_id="minecraft:netherite_ingot",
            name="Незеритовый слиток",
            name_en="Netherite Ingot",
            category="material"
        )
        item.versions.add(test_version)
        assert item.versions.count() == 1
        assert test_version in item.versions.all()