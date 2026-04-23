from rest_framework import serializers
from .models import Favorite

class FavoriteSerializer(serializers.ModelSerializer):
    user_id_display = serializers.ReadOnlyField(source='user.user_id')
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = Favorite
        fields = '__all__'