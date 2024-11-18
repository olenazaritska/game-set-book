from rest_framework import routers

from session.views import SportClubViewSet

router = routers.DefaultRouter()

router.register("sport-clubs", SportClubViewSet)


urlpatterns = router.urls

app_name = "session"
