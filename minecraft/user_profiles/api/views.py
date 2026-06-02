from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from ..models import UserProfile
from .serializers import UserProfileSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = [SearchFilter]
    search_fields = ['user_id']

    def get_queryset(self):
        qs = UserProfile.objects.all()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            qs = qs.filter(user_id=user_id)
        return qs
