import pytest
from rest_framework import status
from mobs.models import Mob

pytestmark = pytest.mark.django_db

class TestMobsAPI:
    
    def test_get_mobs_list(self, api_client):
        Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            name_en="Zombie",
            health=20.0,
            damage=3.0,
            behavior="hostile",
            category="monster",
            experience=5,
            description="Враждебный моб"
        )
        response = api_client.get('/api/mobs/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
    
    def test_create_mob_with_auth(self, admin_client, test_version, test_dimension):
        from biomes.models import Biome
        
        biome = Biome.objects.create(
            name="Plains",
            name_ru="Равнины",
            dimension=test_dimension,
            temperature=0.8
        )
        
        data = {
            'mob_id': 'minecraft:zombie',
            'name': 'Zombie',
            'name_en': 'Zombie',
            'health': 20.0,
            'damage': 3.0,
            'behavior': 'hostile',
            'category': 'monster',
            'experience': 5,
            'description': 'Враждебный моб',
            'spawns_in': [test_dimension.id],
            'biomes': [biome.id],
            'versions': [test_version.id]
        }
        response = admin_client.post('/api/mobs/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_get_single_mob(self, api_client):
        mob = Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            name_en="Zombie",
            health=20.0,
            damage=3.0,
            behavior="hostile",
            category="monster",
            experience=5,
            description="Враждебный моб"
        )
        response = api_client.get(f'/api/mobs/{mob.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == mob.name
    
    def test_search_mobs(self, api_client):
        Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            name_en="Zombie",
            health=20.0,
            damage=3.0,
            behavior="hostile",
            category="monster",
            experience=5,
            description="Враждебный моб"
        )
        Mob.objects.create(
            mob_id="minecraft:creeper",
            name="Creeper",
            name_en="Creeper",
            health=20.0,
            damage=3.0,
            behavior="hostile",
            category="monster",
            experience=5,
            description="Взрывается"
        )
        response = api_client.get('/api/mobs/?search=Zombie')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
    
    def test_filter_mobs_by_behavior(self, api_client):
        Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            name_en="Zombie",
            health=20.0,
            damage=3.0,
            behavior="hostile",
            category="monster",
            experience=5,
            description="Враждебный моб"
        )
        Mob.objects.create(
            mob_id="minecraft:cow",
            name="Cow",
            name_en="Cow",
            health=10.0,
            damage=0,
            behavior="passive",
            category="animal",
            experience=5,
            description="Мирный моб"
        )
        response = api_client.get('/api/mobs/?behavior=hostile')
        assert response.status_code == status.HTTP_200_OK
        behaviors = [item['behavior'] for item in response.data]
        assert 'hostile' in behaviors
    
    def test_filter_mobs_by_category(self, api_client):
        Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            name_en="Zombie",
            health=20.0,
            damage=3.0,
            behavior="hostile",
            category="monster",
            experience=5,
            description="Враждебный моб"
        )
        Mob.objects.create(
            mob_id="minecraft:cow",
            name="Cow",
            name_en="Cow",
            health=10.0,
            damage=0,
            behavior="passive",
            category="animal",
            experience=5,
            description="Мирный моб"
        )
        response = api_client.get('/api/mobs/?category=animal')
        assert response.status_code == status.HTTP_200_OK
        categories = [item['category'] for item in response.data]
        assert 'animal' in categories