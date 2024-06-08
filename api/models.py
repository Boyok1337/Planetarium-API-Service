from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import (
    DateTimeField,
    ForeignKey, UniqueConstraint
)

from api.validators import validate_show_time

User = get_user_model()


class ShowTheme(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class AstronomyShow(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    show_theme = models.ManyToManyField(
        ShowTheme,
        related_name="astronomy_shows",
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

    def clean(self):
        super().clean()
        qs = ShowSession.objects.all()
        validate_show_time(
            show_time=self.show_time,
            astronomy_show=self.astronomy_show,
            planetarium_dome=self.planetarium_dome,
            qs=qs,
            instance=self
        )

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        return super().save(*args, **kwargs)

    def get_available_seats(self):
        taken_seats = self.tickets.count()
        available_seats = self.planetarium_dome.capacity - taken_seats
        return available_seats

    @property
    def show_time_formatted(self):
        return self.show_time.strftime('%Y-%m-%d %H:%M')


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=255, unique=True)
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
        null=True,
        blank=True
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=("show_session", "row", "seat"), name="unique_ticket")
        ]
        ordering = ("-reservation__created_at",)

    def __str__(self):
        return (
            f"{self.show_session.astronomy_show.title}, "
            f"row: {self.row} - "
            f"seat: {self.seat} - "
            f"reservation: {self.reservation.user.username}"
        )

    @staticmethod
    def validate_seat_and_row(seat: int, row: int, num_seats: int, num_rows: int) -> None:
        if seat > num_seats or seat < 0:
            raise ValidationError("Invalid seat")

        if row > num_rows or row < 0:
            raise ValidationError("Invalid row")

    def clean(self) -> None:
        Ticket.validate_seat_and_row(
            seat=self.seat,
            row=self.row,
            num_seats=self.show_session.planetarium_dome.seats_in_row,
            num_rows=self.show_session.planetarium_dome.rows
        )

    def save(self, *args, **kwargs) -> None:
        super().full_clean()
        return super().save(*args, **kwargs)


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    class Meta:
        ordering = ("-created_at",)
