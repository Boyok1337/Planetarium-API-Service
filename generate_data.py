import os
from datetime import datetime, timedelta
import random
import faker
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "planetarium.settings")
django.setup()

from api.models import ShowTheme, AstronomyShow, PlanetariumDome, ShowSession

fake = faker.Faker()


def create_show_themes():
    print("Creating show themes...")
    for _ in range(10):
        name = fake.word()
        while ShowTheme.objects.filter(name=name).exists():
            name = fake.word()
        ShowTheme.objects.create(name=name)
    print("Show themes created.")


def create_astronomy_shows():
    print("Creating astronomy shows...")
    show_themes = ShowTheme.objects.all()
    for _ in range(10):
        title = fake.sentence()
        while AstronomyShow.objects.filter(title=title).exists():
            title = fake.sentence()
        astronomy_show = AstronomyShow.objects.create(
            title=title,
            description=fake.text(),
        )
        astronomy_show.show_theme.set(random.sample(list(show_themes), 3))
    print("Astronomy shows created.")


def create_planetarium_domes():
    print("Creating planetarium domes...")
    for _ in range(10):
        name = fake.word()
        while PlanetariumDome.objects.filter(name=name).exists():
            name = fake.word()
        PlanetariumDome.objects.create(
            name=name,
            rows=fake.random_int(min=10, max=50),
            seats_in_row=fake.random_int(min=5, max=20),
        )
    print("Planetarium domes created.")


def create_show_sessions():
    print("Creating show sessions...")
    astronomy_shows = AstronomyShow.objects.all()
    planetarium_domes = PlanetariumDome.objects.all()
    for _ in range(10):
        start_date = datetime.now() + timedelta(days=1)
        end_date = datetime.now() + timedelta(days=365)
        show_time = fake.date_time_between(
            start_date=start_date,
            end_date=end_date,
        )
        astronomy_show = random.choice(list(astronomy_shows))
        planetarium_dome = random.choice(list(planetarium_domes))
        while ShowSession.objects.filter(
            show_time=show_time,
            astronomy_show=astronomy_show,
            planetarium_dome=planetarium_dome,
        ).exists():
            show_time = fake.date_time_between(
                start_date=start_date,
                end_date=end_date,
            )
        ShowSession.objects.create(
            show_time=show_time,
            astronomy_show=astronomy_show,
            planetarium_dome=planetarium_dome,
        )
    print("Show sessions created.")


if __name__ == "__main__":
    create_show_themes()
    create_astronomy_shows()
    create_planetarium_domes()
    create_show_sessions()
