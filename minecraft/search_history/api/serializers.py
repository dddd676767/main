from rest_framework import serializers
from ..models import SearchHistory

class SearchHistorySerializer(serializers.ModelSerializer):
    user_id_display = serializers.ReadOnlyField(source='user.user_id')
    
    class Meta:
        model = SearchHistory
        fields = '__all__'