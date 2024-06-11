from datetime import datetime, timedelta

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from api.models import ShowTheme, PlanetariumDome, AstronomyShow, ShowSession

API_SHOW_THEME = 'api:show-theme-list'
API_SHOW_SESSION = 'api:show-session-list'
API_ASTRONOMY_SHOW = 'api:astronomy-show-list'
API_PLANETARIUM_DOME = 'api:planetarium-dome-list'
API_TICKET = 'api:ticket-list'
API_RESERVATION = 'api:reservation-list'
API_UPLOAD_SHOW_SESSION = 'api:upload-show-sessions'


def sample_show_theme(**params):
    defaults = {
        "name": "Sample Theme"
    }
    defaults.update(params)
    return ShowTheme.objects.create(**defaults)


def sample_astronomy_show(**params):
    show_theme = ShowTheme.objects.create(name="Sample Theme")
    defaults = {
        "title": "Sample Astronomy",
        "description": "Sample description",
    }
    defaults.update(params)
    astronomy_show = AstronomyShow.objects.create(**defaults)
    astronomy_show.show_theme.add(show_theme)
    return astronomy_show


def sample_planetarium_dome(**params):
    defaults = {
        "name": "Sample Planetarium",
        "rows": 10,
        "seats_in_row": 10
    }
    defaults.update(params)
    return PlanetariumDome.objects.create(**defaults)


def sample_show_session(**params):
    defaults = {
        "astronomy_show": sample_astronomy_show(),
        "planetarium_dome": sample_planetarium_dome(),
        "show_time": datetime.now() + timedelta(days=1)
    }
    defaults.update(params)
    return ShowSession.objects.create(**defaults)


class ShowThemeTests(TestCase):

    def test_unique_name(self):
        sample_show_theme()
        with self.assertRaises(Exception):
            sample_show_theme()

    def test_ordering(self):
        theme1 = sample_show_theme(name="Sample Theme2")
        theme2 = sample_show_theme()
        themes = ShowTheme.objects.all()
        self.assertEqual(themes[0], theme2)
        self.assertEqual(themes[1], theme1)


class AstronomyShowTests(TestCase):

    def test_unique_name(self):
        sample_astronomy_show()
        with self.assertRaises(Exception):
            sample_astronomy_show()

    def test_ordering(self):
        show_theme1 = sample_show_theme(name="Sample Theme1")
        show_theme2 = sample_show_theme(name="Sample Theme2")
        show_themes = ShowTheme.objects.all()
        self.assertEqual(show_themes[0], show_theme1)
        self.assertEqual(show_themes[1], show_theme2)


class PlanetariumDomeTests(TestCase):

    def test_unique_name(self):
        sample_planetarium_dome()
        with self.assertRaises(Exception):
            sample_planetarium_dome()

    def test_ordering(self):
        planetarium_dome1 = sample_planetarium_dome(name="Planetarium Dome2")
        planetarium_dome2 = sample_planetarium_dome(name="Planetarium Dome1")
        planetarium_domes = PlanetariumDome.objects.all()
        self.assertEqual(planetarium_domes[0], planetarium_dome2)
        self.assertEqual(planetarium_domes[1], planetarium_dome1)

    def test_capacity(self):
        planetarium_dome = sample_planetarium_dome()
        self.assertEqual(planetarium_dome.capacity, 100)


class UnauthorizedAccessTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unauthorized_access(self):
        endpoints = [
            (API_SHOW_THEME, 'get'),
            (API_ASTRONOMY_SHOW, 'get'),
            (API_SHOW_SESSION, 'get'),
            (API_PLANETARIUM_DOME, 'get'),
            (API_TICKET, 'get'),
            (API_RESERVATION, 'get'),
            (API_UPLOAD_SHOW_SESSION, 'post'),
        ]

        for endpoint, method in endpoints:
            url = reverse(endpoint)
            response = getattr(self.client, method)(url)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
