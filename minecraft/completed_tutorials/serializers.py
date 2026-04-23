from rest_framework import serializers
from .models import CompletedTutorial

class CompletedTutorialSerializer(serializers.ModelSerializer):
    user_id_display = serializers.ReadOnlyField(source='user.user_id')
    mechanic_title = serializers.ReadOnlyField(source='mechanic.title')
    
    class Meta:
        model = CompletedTutorial
        fields = '__all__'