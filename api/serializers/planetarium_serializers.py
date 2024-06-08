from rest_framework import serializers
from django.db import transaction

from api.models import (
    ShowTheme,
    AstronomyShow,
    ShowSession,
    PlanetariumDome,
    Ticket,
    Reservation
)
from api.validators import validate_show_time


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = (
            'id',
            'name',
        )

    def to_internal_value(self, data):
        try:
            return ShowTheme.objects.get(name=data['name'])
        except ShowTheme.DoesNotExist:
            return super().to_internal_value(data)


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Reservation
        fields = (
            'id',
            'user',
            'created_at',
        )


class ReservationCreateSerializer(serializers.ModelSerializer):
    tickets = serializers.SerializerMethodField

    class Meta:
        model = Reservation
        fields = (
            'id',
            'user',
            'created_at',
            'tickets',
        )

    def get_tickets(self, obj):
        tickets = obj.tickets.all()
        return [ticket.show_session.astronomy_show.title for ticket in tickets]


class AstronomyShowSerializer(serializers.ModelSerializer):
    show_theme = ShowThemeSerializer(many=True, required=True)

    class Meta:
        model = AstronomyShow
        fields = (
            'id',
            'title',
            'description',
            'show_theme',
        )

    def create(self, validated_data):
        show_theme_data = validated_data.pop('show_theme')
        astronomy_show = AstronomyShow.objects.create(**validated_data)

        for show_theme_instance in show_theme_data:
            if isinstance(show_theme_instance, ShowTheme):
                astronomy_show.show_theme.add(show_theme_instance)
            else:
                show_theme = ShowTheme.objects.create(**show_theme_instance)
                astronomy_show.show_theme.add(show_theme)

        return astronomy_show


class AstronomyShowListSerializer(serializers.ModelSerializer):
    show_theme = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
        many=True,
    )

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
            'capacity',
        )


class ShowSessionSerializer(serializers.ModelSerializer):
    astronomy_show = serializers.SlugRelatedField(
        slug_field='title',
        queryset=AstronomyShow.objects.all()
    )
    planetarium_dome = serializers.SlugRelatedField(
        slug_field='name',
        queryset=PlanetariumDome.objects.all()
    )

    class Meta:
        model = ShowSession
        fields = (
            'id',
            'astronomy_show',
            'planetarium_dome',
            'show_time',
        )

    def validate(self, attrs):
        show_time = attrs.get('show_time')
        astronomy_show = attrs.get('astronomy_show')
        planetarium_dome = attrs.get('planetarium_dome')
        qs = ShowSession.objects.all()

        validate_show_time(
            show_time=show_time,
            astronomy_show=astronomy_show,
            planetarium_dome=planetarium_dome,
            qs=qs,
            instance=self.instance
        )

        return attrs


class ShowSessionListSerializer(serializers.ModelSerializer):
    astronomy_show = serializers.CharField(source='astronomy_show.title')
    planetarium_dome = serializers.CharField(source='planetarium_dome.name')

    class Meta:
        model = ShowSession
        fields = (
            'id',
            'astronomy_show',
            'planetarium_dome',
            'show_time_formatted',
        )

    # def get_show_time(self, obj):
    #     show_time = obj.show_time.strftime('%Y-%m-%d %H:%M')
    #     return show_time


class ShowSessionRetrieveSerializer(serializers.ModelSerializer):
    astronomy_show = serializers.CharField(source='astronomy_show.title')
    show_theme = serializers.CharField(source='astronomy_show.show_theme')
    description = serializers.CharField(source='astronomy_show.description')
    planetarium_dome = serializers.CharField(source='planetarium_dome.name')
    available_seats = serializers.CharField(source='get_available_seats')

    class Meta:
        model = ShowSession
        fields = (
            'id',
            'astronomy_show',
            'show_theme',
            'description',
            'planetarium_dome',
            'show_time_formatted',
            'available_seats',
        )


class TicketSerializer(serializers.ModelSerializer):
    show_session = serializers.SerializerMethodField
    reservation = serializers.PrimaryKeyRelatedField(
        queryset=Reservation.objects.all()
    )

    class Meta:
        model = Ticket
        fields = (
            'id',
            'show_session',
            'row',
            'seat',
            'reservation',
        )

    def get_show_session(self, obj):
        return obj.show_session.astronomy_show.title


class TicketListSerializer(serializers.ModelSerializer):
    show_session = serializers.CharField(source='show_session.astronomy_show.title', read_only=True)
    reservation = serializers.CharField(source='reservation.user', read_only=True)

    class Meta:
        model = Ticket
        fields = (
            'id',
            'show_session',
            'row',
            'seat',
            'reservation',
        )
