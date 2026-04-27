import pytest
from rest_framework import status
from dimensions.models import Dimension

@pytest.mark.django_db
class TestDimensionsAPI:
    
    def test_get_dimensions_list(self, api_client):
        """Тест получения списка измерений"""
        Dimension.objects.create(name="Overworld", name_ru="Верхний мир")
        Dimension.objects.create(name="Nether", name_ru="Ад")
        
        response = api_client.get('/api/dimensions/')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
    
    def test_create_dimension_with_auth(self, admin_client):
        """Тест создания измерения с авторизацией"""
        data = {
            'name': 'End',
            'name_ru': 'Энд',
            'description': 'Измерение с драконом'
        }
        response = admin_client.post('/api/dimensions/', data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Dimension.objects.count() == 1