from rest_framework import viewsets

from api.models import ShowTheme, AstronomyShow, ShowSession, PlanetariumDome, Ticket, Reservation
from api.serializers.planetarium_serializers import ShowThemeSerializer, AstronomyShowSerializer, \
    ShowSessionSerializer, ShowSessionListSerializer, ShowSessionRetrieveSerializer, \
    PlanetariumDomeSerializer, TicketSerializer, TicketListSerializer, ReservationSerializer, \
    ReservationCreateSerializer, AstronomyShowListSerializer, TicketRetrieveSerializer


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all()
    serializer_class = AstronomyShowSerializer

    def get_queryset(self):
        queryset = self.queryset

        queryset = queryset.prefetch_related('show_theme')

        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == "list":
            serializer_class = AstronomyShowListSerializer

        if self.action == "create":
            serializer_class = AstronomyShowSerializer

        if self.action == "retrieve":
            serializer_class = AstronomyShowListSerializer

        return serializer_class


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all()
    serializer_class = ShowSessionSerializer

    def get_queryset(self):
        queryset = self.queryset

        queryset = queryset.select_related('astronomy_show', 'planetarium_dome')

        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == "list":
            serializer_class = ShowSessionListSerializer

        if self.action == "create":
            serializer_class = ShowSessionSerializer

        if self.action == "retrieve":
            serializer_class = ShowSessionRetrieveSerializer

        return serializer_class


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_queryset(self):
        queryset = self.queryset

        queryset = queryset.select_related('show_session', 'reservation')

        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == "list":
            serializer_class = TicketListSerializer

        if self.action == "create":
            serializer_class = TicketSerializer

        if self.action == "retrieve":
            serializer_class = TicketRetrieveSerializer

        return serializer_class


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        queryset = self.queryset

        queryset = queryset.select_related('user')

        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == "list":
            serializer_class = ReservationSerializer

        if self.action == "create":
            serializer_class = ReservationCreateSerializer

        return serializer_class
