from rest_framework import routers

from session.views import SportClubViewSet, SessionViewSet

router = routers.DefaultRouter()

router.register("sport-clubs", SportClubViewSet, basename="sport_club")
router.register("sessions", SessionViewSet, basename="session")


urlpatterns = router.urls

app_name = "session"
