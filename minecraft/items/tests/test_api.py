import pytest
from rest_framework import status
from items.models import Item

@pytest.mark.django_db
class TestItemsAPI:
    
    def test_get_items_list(self, api_client):
        Item.objects.create(
            item_id="minecraft:diamond",
            name="Алмаз",
            name_en="Diamond",
            category="material"
        )
        Item.objects.create(
            item_id="minecraft:iron_ingot",
            name="Железный слиток",
            name_en="Iron Ingot",
            category="material"
        )
        response = api_client.get('/api/items/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 2
    
    def test_create_item_without_auth(self, api_client):
        data = {
            'item_id': 'minecraft:diamond',
            'name': 'Алмаз',
            'name_en': 'Diamond',
            'category': 'material'
        }
        response = api_client.post('/api/items/', data)
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
    
    def test_create_item_with_auth(self, admin_client, test_version):
        data = {
            'item_id': 'minecraft:diamond',
            'name': 'Алмаз',
            'name_en': 'Diamond',
            'category': 'material',
            'stack_size': 64,
            'rarity': 'rare',
            'versions': [test_version.id]
        }
        response = admin_client.post('/api/items/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Item.objects.count() >= 1
    
    def test_get_single_item(self, api_client, test_item):
        response = api_client.get(f'/api/items/{test_item.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == test_item.name
    
    def test_search_items(self, api_client):
        Item.objects.create(
            item_id="minecraft:diamond_sword",
            name="Алмазный меч",
            name_en="Diamond Sword",
            category="weapon"
        )
        Item.objects.create(
            item_id="minecraft:diamond_pickaxe",
            name="Алмазная кирка",
            name_en="Diamond Pickaxe",
            category="tool"
        )
        Item.objects.create(
            item_id="minecraft:stone",
            name="Камень",
            name_en="Stone",
            category="block"
        )
        response = api_client.get('/api/items/?search=алмаз')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
    
    def test_filter_items_by_category(self, api_client):
        Item.objects.create(
            item_id="minecraft:diamond_sword",
            name="Алмазный меч",
            name_en="Diamond Sword",
            category="weapon"
        )
        Item.objects.create(
            item_id="minecraft:apple",
            name="Яблоко",
            name_en="Apple",
            category="food"
        )
        response = api_client.get('/api/items/?category=weapon')
        assert response.status_code == status.HTTP_200_OK
        for item in response.data:
            assert item['category'] == "weapon"
    
    def test_filter_items_by_version(self, api_client):
        from versions.models import MinecraftVersion
        from datetime import date
        
        version_120 = MinecraftVersion.objects.create(
            version_number="1.20",
            release_date=date(2023, 12, 7),
            is_latest=False
        )
        version_121 = MinecraftVersion.objects.create(
            version_number="1.21",
            release_date=date(2024, 6, 13),
            is_latest=True
        )
        
        new_item = Item.objects.create(
            item_id="minecraft:new_item",
            name="Новый предмет",
            name_en="New Item",
            category="material"
        )
        new_item.versions.add(version_121)
        
        old_item = Item.objects.create(
            item_id="minecraft:old_item",
            name="Старый предмет",
            name_en="Old Item",
            category="material"
        )
        old_item.versions.add(version_120)
        
        response = api_client.get('/api/items/?version=1.21')
        assert response.status_code == status.HTTP_200_OK
        for item in response.data:
            assert item['name'] == "Новый предмет"
    
    def test_update_item(self, admin_client, test_item):
        response = admin_client.patch(
            f'/api/items/{test_item.id}/',
            {'name': 'Обновленные доски'},
            format='json'
        )
        assert response.status_code == status.HTTP_200_OK
        test_item.refresh_from_db()
        assert test_item.name == "Обновленные доски"
    
    def test_delete_item(self, admin_client, test_item):
        response = admin_client.delete(f'/api/items/{test_item.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Item.objects.count() == 0