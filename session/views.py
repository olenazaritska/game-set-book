from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from session.models import SportClub
from session.serializers import (
    SportClubSerializer,
    SportClubSessionsSerializer,
)


class SportClubViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = SportClub.objects.prefetch_related("working_hours")
    serializer_class = SportClubSerializer


class SessionViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = SportClub.objects.prefetch_related("courts__sessions")
    serializer_class = SportClubSessionsSerializer
