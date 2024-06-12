import csv
from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema_view
from rest_framework import viewsets, status
from django.db.models import BooleanField, Case, When, Value
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import ShowTheme, AstronomyShow, ShowSession, PlanetariumDome, Ticket, Reservation
from api.schemas import AstronomyShowSchema, ShowSessionSchema, PlanetariumDomeSchema, TicketSchema, ReservationSchema, \
    ShowSessionUploadSchema
from api.serializers.planetarium_serializers import ShowThemeSerializer, AstronomyShowSerializer, \
    ShowSessionSerializer, ShowSessionListSerializer, ShowSessionRetrieveSerializer, \
    PlanetariumDomeSerializer, TicketSerializer, TicketListSerializer, ReservationSerializer, \
    ReservationCreateSerializer, AstronomyShowListSerializer, TicketRetrieveSerializer
from api.validators import validate_show_time


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer


@extend_schema_view(list=AstronomyShowSchema.list)
class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all()
    serializer_class = AstronomyShowSerializer

    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.prefetch_related('show_theme')
        show_theme = self.request.query_params.get('show_theme')
        title = self.request.query_params.get('title')

        if show_theme:
            queryset = queryset.filter(show_theme__name=show_theme)

        if title:
            queryset = queryset.filter(title=title)

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


@extend_schema_view(list=ShowSessionSchema.list)
class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all()
    serializer_class = ShowSessionSerializer

    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.select_related('astronomy_show', 'planetarium_dome')
        astronomy_show = self.request.query_params.get('astronomy_show')
        planetarium_dome = self.request.query_params.get('planetarium_dome')
        show_time_year = self.request.query_params.get('show_time_year')
        show_time_month = self.request.query_params.get('show_time_month')
        show_time_day = self.request.query_params.get('show_time_day')
        show_time_hour = self.request.query_params.get('show_time_hour')

        if astronomy_show:
            queryset = queryset.filter(astronomy_show__title=astronomy_show)

        if planetarium_dome:
            queryset = queryset.filter(planetarium_dome__name=planetarium_dome)

        if show_time_year:
            queryset = queryset.filter(show_time__year=show_time_year)

        if show_time_month:
            queryset = queryset.filter(show_time__month=show_time_month)

        if show_time_day:
            queryset = queryset.filter(show_time__day=show_time_day)

        if show_time_hour:
            queryset = queryset.filter(show_time__hour=show_time_hour)

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


@extend_schema_view(list=PlanetariumDomeSchema.list)
class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer

    def get_queryset(self):
        queryset = self.queryset

        name = self.request.query_params.get("name")
        rows = self.request.query_params.get("rows")
        rowsgt = self.request.query_params.get("rowsgt")
        rowslt = self.request.query_params.get("rowslt")
        rows_range = self.request.query_params.get('rows_range')
        seats_in_row = self.request.query_params.get("seats_in_row")
        seats_in_rowgt = self.request.query_params.get("seats_in_rowgt")
        seats_in_rowlt = self.request.query_params.get("seats_in_rowlt")
        seats_range = self.request.query_params.get("seats_range")

        if name:
            queryset = queryset.filter(name=name)

        if rows:
            queryset = queryset.filter(rows=rows)

        if rowsgt:
            queryset = queryset.filter(rows__gt=rowsgt)

        if rowslt:
            queryset = queryset.filter(rows__lt=rowslt)

        if seats_in_row:
            queryset = queryset.filter(seats_in_row=seats_in_row)

        if seats_in_rowgt:
            queryset = queryset.filter(seats_in_row__gt=seats_in_rowgt)

        if seats_in_rowlt:
            queryset = queryset.filter(seats_in_row__lt=seats_in_rowlt)

        if rows_range:
            rows_range = rows_range.split('-')
            if len(rows_range) == 2:
                min_seats = int(rows_range[0])
                max_seats = int(rows_range[1])
                queryset = queryset.filter(rows__range=(min_seats, max_seats))

        if seats_range:
            seats_range = seats_range.split('-')
            if len(seats_range) == 2:
                min_seats = int(seats_range[0])
                max_seats = int(seats_range[1])
                queryset = queryset.filter(rows__range=(min_seats, max_seats))

        return queryset


@extend_schema_view(list=TicketSchema.list)
class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.select_related('show_session', 'reservation')
        title = self.request.query_params.get('title')

        if title:
            queryset = queryset.filter(show_session__astronomy_show__title=title)

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


@extend_schema_view(list=ReservationSchema.list)
class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.select_related('user')

        queryset = queryset.annotate(
            is_user_staff=Case(
                When(user=user, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )

        if user.is_staff:
            queryset = queryset.order_by('-is_user_staff')
        else:
            queryset = queryset.filter(user=user)

        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == "list":
            serializer_class = ReservationSerializer

        if self.action == "create":
            serializer_class = ReservationCreateSerializer

        return serializer_class


class ShowSessionUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @ShowSessionUploadSchema.show_session_upload_schema
    def post(self, request, *args, **kwargs):
        csv_file = request.FILES.get('file')
        if not csv_file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        if not csv_file.name.endswith('.csv'):
            return Response({'error': 'This is not a CSV file'}, status=status.HTTP_400_BAD_REQUEST)

        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        sessions_created = []
        errors = []

        for row in reader:
            serializer = ShowSessionSerializer(data=row)
            if serializer.is_valid():
                show_time_str = row['show_time']
                try:
                    show_time = datetime.strptime(show_time_str, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    errors.append('Invalid datetime format for show_time: {}'.format(show_time_str))
                    continue

                try:
                    validate_show_time(
                        show_time=show_time,
                        astronomy_show=serializer.validated_data['astronomy_show'],
                        planetarium_dome=serializer.validated_data['planetarium_dome'],
                        qs=ShowSession.objects.all(),
                        instance=None
                    )
                except ValidationError as e:
                    errors.append(str(e))
                    continue

                show_session = serializer.save()
                sessions_created.append(show_session)
            else:
                errors.append(serializer.errors)

        if errors:
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'created_sessions': ShowSessionSerializer(sessions_created, many=True).data},
                        status=status.HTTP_201_CREATED)


@csrf_exempt
def get_tickets_by_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = get_user_model().objects.get(email=email)
            tickets = Ticket.objects.filter(reservation_id=user.id)
            ticket_data = list(tickets.values())
            return JsonResponse({'status': 'success', 'data': ticket_data}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
