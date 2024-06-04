from rest_framework import serializers

from api.models import ShowTheme, AstronomyShow, ShowSession, PlanetariumDome, Ticket, Reservation


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = (
            'id',
            'name',
        )


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = (
            'id',
            'created_at',
            'user',
        )


class AstronomyShowSerializer(serializers.ModelSerializer):
    show_theme = ShowThemeSerializer(many=True, read_only=True)

    class Meta:
        model = AstronomyShow
        fields = (
            'id',
            'title',
            'description',
            'show_theme',
        )


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = (
            'id',
            'name',
            'rows',
            'seats_in_row',
        )


class ShowSessionSerializer(serializers.ModelSerializer):
    astronomy_show = AstronomyShowSerializer(read_only=True)
    planetarium_dome = PlanetariumDomeSerializer(read_only=True)

    class Meta:
        model = ShowSession
        fields = (
            'id',
            'astronomy_show',
            'planetarium_dome',
            'show_time',
        )


class TicketSerializer(serializers.ModelSerializer):
    show_session = ShowSessionSerializer(read_only=True)
    reservations = ReservationSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = (
            'id',
            'row',
            'seat',
            'show_session',
            'reservation',
        )
