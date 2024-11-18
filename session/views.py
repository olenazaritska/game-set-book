from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from session.models import SportClub
from session.serializers import SportClubSerializer


class SportClubViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = SportClub.objects.all()
    serializer_class = SportClubSerializer
