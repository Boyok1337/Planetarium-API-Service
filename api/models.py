from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import (
    DateTimeField,
    ForeignKey
)


User = get_user_model()


class ShowTheme(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class AstronomyShow(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    show_theme = models.ManyToManyField(
        ShowTheme,
        related_name="astronomy_shows"
    )

    class Meta:
        ordering = ("title",)

    def __str__(self):
        return self.title


class ShowSession(models.Model):
    astronomy_show = ForeignKey(
        AstronomyShow,
        on_delete=models.CASCADE,
        related_name="show_sessions"
    )
    planetarium_dome = ForeignKey(
        "PlanetariumDome",
        on_delete=models.SET_NULL,
        related_name="show_sessions",
        null=True
    )
    show_time = DateTimeField()

    class Meta:
        ordering = ("-show_time",)

    def __str__(self):
        return self.astronomy_show.title


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=255)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()

    class Meta:
        ordering = ("name",)

    @property
    def capacity(self):
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    show_session = models.ForeignKey(
        ShowSession,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    reservation = models.ForeignKey(
        "Reservation",
        on_delete=models.SET_NULL,
        related_name="tickets",
        null=True
    )


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    class Meta:
        ordering = ("-created_at",)
