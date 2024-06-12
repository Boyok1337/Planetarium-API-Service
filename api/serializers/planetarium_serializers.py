from rest_framework import serializers
from django.db import transaction

from api.models import (
    ShowTheme,
    AstronomyShow,
    ShowSession,
    PlanetariumDome,
    Ticket,
    Reservation,
)
from api.validators import validate_show_time


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = (
            "id",
            "name",
        )

    def to_internal_value(self, data):
        try:
            return ShowTheme.objects.get(name=data["name"])
        except ShowTheme.DoesNotExist:
            return super().to_internal_value(data)


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Reservation
        fields = (
            "id",
            "user",
            "created_at",
        )


class ReservationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = (
            "id",
            "user",
            "created_at",
        )

    def get_tickets(self, obj):
        tickets = obj.tickets.all()
        return [ticket.show_session.astronomy_show.title for ticket in tickets]


class AstronomyShowSerializer(serializers.ModelSerializer):
    show_theme = ShowThemeSerializer(many=True, required=True)

    class Meta:
        model = AstronomyShow
        fields = (
            "id",
            "title",
            "description",
            "show_theme",
        )

    def create(self, validated_data):
        show_theme_data = validated_data.pop("show_theme")

        with transaction.atomic():
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
        slug_field="name",
        read_only=True,
        many=True,
    )

    class Meta:
        model = AstronomyShow
        fields = (
            "id",
            "title",
            "description",
            "show_theme",
        )


class PlanetariumDomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlanetariumDome
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
            "capacity",
        )


class ShowSessionSerializer(serializers.ModelSerializer):
    astronomy_show = serializers.SlugRelatedField(
        slug_field="title", queryset=AstronomyShow.objects.all()
    )
    planetarium_dome = serializers.SlugRelatedField(
        slug_field="name", queryset=PlanetariumDome.objects.all()
    )

    class Meta:
        model = ShowSession
        fields = (
            "id",
            "astronomy_show",
            "planetarium_dome",
            "show_time",
        )

    def validate(self, attrs):
        show_time = attrs.get("show_time")
        astronomy_show = attrs.get("astronomy_show")
        planetarium_dome = attrs.get("planetarium_dome")
        qs = ShowSession.objects.all()

        validate_show_time(
            show_time=show_time,
            astronomy_show=astronomy_show,
            planetarium_dome=planetarium_dome,
            qs=qs,
            instance=self.instance,
        )

        return attrs


class ShowSessionListSerializer(serializers.ModelSerializer):
    astronomy_show = serializers.CharField(source="astronomy_show.title")
    planetarium_dome = serializers.CharField(source="planetarium_dome.name")

    class Meta:
        model = ShowSession
        fields = (
            "id",
            "astronomy_show",
            "planetarium_dome",
            "show_time_formatted",
        )


class ShowSessionRetrieveSerializer(serializers.ModelSerializer):
    astronomy_show = serializers.CharField(source="astronomy_show.title")
    show_theme = serializers.CharField(source="astronomy_show.show_theme")
    description = serializers.CharField(source="astronomy_show.description")
    planetarium_dome = serializers.CharField(source="planetarium_dome.name")
    available_seats = serializers.CharField(source="get_available_seats")

    class Meta:
        model = ShowSession
        fields = (
            "id",
            "astronomy_show",
            "show_theme",
            "description",
            "planetarium_dome",
            "show_time_formatted",
            "available_seats",
        )


class TicketSerializer(serializers.ModelSerializer):
    show_session_title = serializers.CharField(write_only=True)
    show_session_time = serializers.DateTimeField(write_only=True)
    reservation = serializers.BooleanField(write_only=True, allow_null=True)
    show_session = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = (
            "id",
            "show_session_title",
            "show_session_time",
            "row",
            "seat",
            "reservation",
            "show_session",
        )

    def validate(self, data):
        show_session_title = data.get("show_session_title")
        show_session_time = data.get("show_session_time")

        show_sessions = ShowSession.objects.filter(
            astronomy_show__title=show_session_title, show_time=show_session_time
        )

        if not show_sessions.exists():
            raise serializers.ValidationError(
                {
                    "show_session": "Show session with this title and time does not exist."
                }
            )
        if show_sessions.count() > 1:
            raise serializers.ValidationError(
                {
                    "show_session": "Multiple show sessions with this title and time found. Please be more specific."
                }
            )

        data["show_session"] = show_sessions.first()
        return data

    def get_show_session(self, obj):
        show_session_serializer = ShowSessionSerializer(
            instance=obj.show_session, context=self.context
        )
        return show_session_serializer.data

    def create(self, validated_data):
        validated_data.pop("show_session_title")
        validated_data.pop("show_session_time")

        reservation_flag = validated_data.pop("reservation", False)
        show_session = validated_data.pop("show_session")

        with transaction.atomic():
            ticket = Ticket.objects.create(show_session=show_session, **validated_data)

            if reservation_flag:
                user = self.context["request"].user
                Reservation.objects.create(user=user)

        return ticket


class TicketListSerializer(serializers.ModelSerializer):
    show_session = serializers.CharField(
        source="show_session.astronomy_show.title", read_only=True
    )
    reservation = serializers.CharField(source="reservation.user", read_only=True)
    show_time = serializers.CharField(source="show_session.show_time_formatted")

    class Meta:
        model = Ticket
        fields = (
            "id",
            "show_session",
            "row",
            "seat",
            "reservation",
            "show_time",
        )


class TicketRetrieveSerializer(serializers.ModelSerializer):
    show_session = ShowSessionRetrieveSerializer()
    reservation = serializers.CharField(source="reservation.user", read_only=True)
    show_time = serializers.CharField(source="show_session.show_time_formatted")

    class Meta:
        model = Ticket
        fields = (
            "id",
            "show_session",
            "row",
            "seat",
            "reservation",
            "show_time",
        )
