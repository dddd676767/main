import pytest
from rest_framework import status
from mobs.models import Mob

@pytest.mark.django_db
class TestMobsAPI:
    
    def test_get_mobs_list(self, api_client):
        Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        Mob.objects.create(
            mob_id="minecraft:creeper",
            name="Creeper",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        response = api_client.get('/api/mobs/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 2
    
    def test_create_mob_with_auth(self, admin_client, test_version):
        data = {
            'mob_id': 'minecraft:zombie',
            'name': 'Zombie',
            'health': 20.0,
            'damage': 3.0,
            'behavior': 'hostile',
            'category': 'monster',
            'experience': 5,
            'description': 'Враждебный моб',
            'versions': [test_version.id]
        }
        response = admin_client.post('/api/mobs/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Mob.objects.count() >= 1
    
    def test_get_single_mob(self, api_client):
        mob = Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        response = api_client.get(f'/api/mobs/{mob.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == mob.name
    
    def test_search_mobs(self, api_client):
        Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        Mob.objects.create(
            mob_id="minecraft:zombie_villager",
            name="Zombie Villager",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        Mob.objects.create(
            mob_id="minecraft:creeper",
            name="Creeper",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        response = api_client.get('/api/mobs/?search=Zombie')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
    
    def test_filter_mobs_by_behavior(self, api_client):
        Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        Mob.objects.create(
            mob_id="minecraft:cow",
            name="Cow",
            health=10.0,
            behavior="passive",
            category="animal"
        )
        response = api_client.get('/api/mobs/?behavior=hostile')
        assert response.status_code == status.HTTP_200_OK
        for item in response.data:
            assert item['behavior'] == "hostile"
    
    def test_filter_mobs_by_category(self, api_client):
        Mob.objects.create(
            mob_id="minecraft:zombie",
            name="Zombie",
            health=20.0,
            behavior="hostile",
            category="monster"
        )
        Mob.objects.create(
            mob_id="minecraft:cow",
            name="Cow",
            health=10.0,
            behavior="passive",
            category="animal"
        )
        response = api_client.get('/api/mobs/?category=animal')
        assert response.status_code == status.HTTP_200_OK
        for item in response.data:
            assert item['category'] == "animal"