from django_filters import FilterSet
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend, DateFromToRangeFilter
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Advertisement
from .permissions import IsOwnerOrReadOnly
from .serializers import AdvertisementSerializer


class F(FilterSet):
    created_at = DateFromToRangeFilter()

    class Meta:
        model = Advertisement
        fields = ['title', 'status', 'creator', 'created_at']


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter, ]
    filterset_class = F
    # filterset_fields = ['title', 'status', 'creator', 'created_at']
    search_fields = ['title', 'description', ]
    ordering_fields = ['-created_at', '-updated_at', 'title', ]

    def get_permissions(self):
        """Получение прав для действий."""
        if self.request.user.is_superuser:  # отменяем все ограничения для суперпользователей
            return []
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return []

    @action(methods=['get'], detail=False)
    def favorites(self, request):
        favorite_advertisements = (
            Advertisement.objects.filter(favorite_users=request.user.pk)
        )
        return Response({'Избранные объявления': favorite_advertisements.values()})

    @action(methods=['patch'], detail=True)
    def add_favorite(self, request, pk=None):
        favorite_advertisement = Advertisement.objects.get(pk=pk)
        if favorite_advertisement.creator_id == request.user.pk:
            return Response({'error': "Нельзя добавить свое объявление в избранное!"})
        favorite_user = User.objects.get(pk=request.user.pk)
        favorite_advertisement.favorite_users.add(favorite_user)

        return Response({'Добавлено в избранное': Advertisement.objects.filter(pk=pk).values()})
