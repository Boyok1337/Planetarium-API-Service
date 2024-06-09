from django.urls import path, include
from rest_framework import routers

from api.views.planetarium_views import ShowThemeViewSet, AstronomyShowViewSet, ShowSessionViewSet, \
    PlanetariumDomeViewSet, TicketViewSet, ReservationViewSet, ShowSessionUploadView

router = routers.DefaultRouter()
router.register('show_theme', ShowThemeViewSet, basename='show-theme')
router.register('astronomy_show', AstronomyShowViewSet, basename='astronomy-show')
router.register('show_session', ShowSessionViewSet, basename="show-session")
router.register('planetarium_dome', PlanetariumDomeViewSet, basename='planetarium-dome')
router.register('ticket', TicketViewSet, basename='ticket')
router.register('reservation', ReservationViewSet, basename="reservation")

urlpatterns = [
    path('', include(router.urls)),
    path('upload-show-sessions/', ShowSessionUploadView.as_view(), name='upload-show-sessions'),
]

app_name = 'api'
