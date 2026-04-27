import pytest
from datetime import date
from rest_framework import status
from versions.models import MinecraftVersion

pytestmark = pytest.mark.django_db

class TestVersionsAPI:
    
    def test_get_versions_list(self, api_client):
        MinecraftVersion.objects.create(
            version_number="1.20",
            release_date=date(2023, 12, 7),
            is_latest=False
        )
        MinecraftVersion.objects.create(
            version_number="1.21",
            release_date=date(2024, 6, 13),
            is_latest=True
        )
        response = api_client.get('/api/versions/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 2
    
    def test_create_version_without_auth(self, api_client):
        data = {
            'version_number': '1.22',
            'release_date': '2025-01-01',
            'is_latest': True
        }
        response = api_client.post('/api/versions/', data)
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_create_version_with_auth(self, admin_client):
        data = {
            'version_number': '1.22',
            'release_date': '2025-01-01',
            'is_latest': True
        }
        response = admin_client.post('/api/versions/', data)
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_get_single_version(self, api_client):
        version = MinecraftVersion.objects.create(
            version_number="1.20",
            release_date=date(2023, 12, 7),
            is_latest=False
        )
        response = api_client.get(f'/api/versions/{version.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['version_number'] == version.version_number
    
    def test_update_version(self, admin_client):
        version = MinecraftVersion.objects.create(
            version_number="1.20",
            release_date=date(2023, 12, 7),
            is_latest=False
        )
        response = admin_client.patch(
            f'/api/versions/{version.id}/',
            {'version_number': '1.20.1'},
            format='json'
        )
        assert response.status_code == status.HTTP_200_OK
        version.refresh_from_db()
        assert version.version_number == "1.20.1"
    
    def test_delete_version(self, admin_client):
        version = MinecraftVersion.objects.create(
            version_number="1.20",
            release_date=date(2023, 12, 7),
            is_latest=False
        )
        response = admin_client.delete(f'/api/versions/{version.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    def test_filter_versions_by_latest(self, api_client):
        MinecraftVersion.objects.create(
            version_number="1.20",
            release_date=date(2023, 12, 7),
            is_latest=False
        )
        MinecraftVersion.objects.create(
            version_number="1.21",
            release_date=date(2024, 6, 13),
            is_latest=True
        )
        response = api_client.get('/api/versions/?is_latest=true')
        assert response.status_code == status.HTTP_200_OK
        latest = [item for item in response.data if item['is_latest'] == True]
        assert len(latest) >= 1