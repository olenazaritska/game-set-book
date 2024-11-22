from django.db.models import Prefetch
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from session.models import SportClub, Session
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
    serializer_class = SportClubSessionsSerializer

    def get_queryset(self):
        sport_club_id = self.request.query_params.get("sport-club")
        session_date = self.request.query_params.get("date")

        sessions_queryset = Session.objects.all()
        if session_date:
            sessions_queryset = sessions_queryset.filter(date=session_date)

        queryset = SportClub.objects.prefetch_related(
            Prefetch(
                "courts__sessions",
                queryset=sessions_queryset,
                to_attr="filtered_sessions",
            )
        )

        if sport_club_id:
            queryset = queryset.filter(id=sport_club_id)

        return queryset.distinct()
