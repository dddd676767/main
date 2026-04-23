from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    selected_version_number = serializers.ReadOnlyField(source='selected_version.version_number')
    
    class Meta:
        model = UserProfile
        fields = '__all__'