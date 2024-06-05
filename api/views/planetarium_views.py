from rest_framework import viewsets

from api.models import ShowTheme, AstronomyShow, ShowSession, PlanetariumDome
from api.serializers.planetarium_serializers import ShowThemeSerializer, AstronomyShowSerializer, \
    AstronomyShowReadSerializer, ShowSessionSerializer, ShowSessionReadSerializer, ShowSessionRetrieveSerializer, \
    PlanetariumDomeSerializer


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all()
    serializer_class = AstronomyShowSerializer

    def get_queryset(self):
        queryset = self.queryset

        queryset.prefetch_related('show_theme')

        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == "list":
            serializer_class = AstronomyShowReadSerializer

        if self.action == "create":
            serializer_class = AstronomyShowSerializer

        if self.action == "retrieve":
            serializer_class = AstronomyShowReadSerializer

        return serializer_class


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all()
    serializer_class = ShowSessionSerializer

    def get_queryset(self):
        queryset = self.queryset

        queryset.prefetch_related('astronomy_show', 'planetarium_dome')

        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == "list":
            serializer_class = ShowSessionReadSerializer

        if self.action == "create":
            serializer_class = ShowSessionSerializer

        if self.action == "retrieve":
            serializer_class = ShowSessionRetrieveSerializer

        return serializer_class


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer
