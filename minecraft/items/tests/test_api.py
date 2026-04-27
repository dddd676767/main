import pytest
from rest_framework import status
from items.models import Item

pytestmark = pytest.mark.django_db

class TestItemsAPI:
    
    def test_get_items_list(self, api_client):
        Item.objects.create(
            item_id="minecraft:diamond",
            name="Алмаз",
            name_en="Diamond",
            category="material",
            stack_size=64,
            rarity="common"
        )
        response = api_client.get('/api/items/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
    
    def test_create_item_without_auth(self, api_client, test_version):
        data = {
            'item_id': 'minecraft:diamond',
            'name': 'Алмаз',
            'name_en': 'Diamond',
            'category': 'material',
            'stack_size': 64,
            'rarity': 'common',
            'versions': [test_version.id]
        }
        response = api_client.post('/api/items/', data, format='json')
        print("ERROR:", response.data)
        assert response.status_code == status.HTTP_201_CREATED
    
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
        print("ERROR:", response.data)
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_get_single_item(self, api_client, test_item):
        response = api_client.get(f'/api/items/{test_item.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == test_item.name
    
    def test_search_items(self, api_client):
        Item.objects.create(
            item_id="minecraft:diamond_sword",
            name="Алмазный меч",
            name_en="Diamond Sword",
            category="weapon",
            stack_size=1,
            rarity="rare"
        )
        Item.objects.create(
            item_id="minecraft:stone",
            name="Камень",
            name_en="Stone",
            category="block",
            stack_size=64,
            rarity="common"
        )
        response = api_client.get('/api/items/?search=алмаз')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
    
    def test_filter_items_by_category(self, api_client):
        Item.objects.create(
            item_id="minecraft:diamond_sword",
            name="Алмазный меч",
            name_en="Diamond Sword",
            category="weapon",
            stack_size=1,
            rarity="rare"
        )
        Item.objects.create(
            item_id="minecraft:apple",
            name="Яблоко",
            name_en="Apple",
            category="food",
            stack_size=64,
            rarity="common"
        )
        response = api_client.get('/api/items/?category=weapon')
        assert response.status_code == status.HTTP_200_OK
        categories = [item['category'] for item in response.data]
        assert 'weapon' in categories
    
    def test_filter_items_by_version(self, api_client):
        from versions.models import MinecraftVersion
        from datetime import date
        
        version_121 = MinecraftVersion.objects.create(
            version_number="1.21",
            release_date=date(2024, 6, 13),
            is_latest=True
        )
        
        new_item = Item.objects.create(
            item_id="minecraft:new_item",
            name="Новый предмет",
            name_en="New Item",
            category="material",
            stack_size=64,
            rarity="common"
        )
        new_item.versions.add(version_121)
        
        response = api_client.get('/api/items/?version=1.21')
        assert response.status_code == status.HTTP_200_OK
    
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