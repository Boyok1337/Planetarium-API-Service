from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_show_time(show_time, astronomy_show, planetarium_dome, qs, instance=None):
    if show_time <= timezone.now():
        raise ValidationError("Show time must be provided in the future")

    qs = qs.exclude(pk=instance.pk if instance else None)
    qs = qs.filter(
        astronomy_show=astronomy_show,
        planetarium_dome=planetarium_dome,
    )
    one_hour = timedelta(hours=1)
    if qs.filter(show_time__gte=show_time - one_hour, show_time__lt=show_time).exists():
        raise ValidationError("Show time must be at least 1 hour apart from the previous show time.")
