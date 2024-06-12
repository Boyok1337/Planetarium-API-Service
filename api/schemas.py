from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

from api.serializers.planetarium_serializers import (
    AstronomyShowSerializer,
    ShowSessionListSerializer,
    PlanetariumDomeSerializer,
    TicketListSerializer,
)


class AstronomyShowSchema:
    list = extend_schema(
        parameters=[
            OpenApiParameter(
                name="show_theme",
                description="Filter by show theme name " "(ex. ?show_theme=Mars)",
                required=False,
                type={"type": "array", "items": {"type": "string"}},
            ),
            OpenApiParameter(
                name="title",
                description="Filter by title",
                required=False,
                type={"type": "string"},
            ),
        ],
        responses={
            200: AstronomyShowSerializer(),
        },
    )


class ShowSessionSchema:
    list = extend_schema(
        parameters=[
            OpenApiParameter(
                name="astronomy_show",
                description="Filter by astronomy show title",
                required=False,
                type={"type": "string"},
            ),
            OpenApiParameter(
                name="planetarium_dome",
                description="Filter by planetarium dome name",
                required=False,
                type={"type": "string"},
            ),
            OpenApiParameter(
                name="show_time_year",
                description="Filter by year",
                required=False,
                type={"type": "integer"},
            ),
            OpenApiParameter(
                name="show_time_month",
                description="Filter by month",
                required=False,
                type={"type": "integer"},
            ),
            OpenApiParameter(
                name="show_time_day",
                description="Filter by day",
                required=False,
                type={"type": "integer"},
            ),
            OpenApiParameter(
                name="show_time_hour",
                description="Filter by hour",
                required=False,
                type={"type": "integer"},
            ),
        ],
        responses={200: ShowSessionListSerializer(many=True)},
    )


class PlanetariumDomeSchema:
    list = extend_schema(
        parameters=[
            OpenApiParameter(
                name="name",
                description="Filter by name",
                required=False,
                type={"type": "string"},
            ),
            OpenApiParameter(
                name="rows",
                description="Filter by rows",
                required=False,
                type={"type": "integer"},
            ),
            OpenApiParameter(
                name="rowsgt",
                description="Filter rows greater than a value",
                required=False,
                type={"type": "integer"},
            ),
            OpenApiParameter(
                name="rowslt",
                description="Filter rows less than a value",
                required=False,
                type={"type": "integer"},
            ),
            OpenApiParameter(
                name="rows_range",
                description="Filter rows within a range",
                required=False,
                type={"type": "string"},
            ),
            OpenApiParameter(
                name="seats_in_row",
                description="Filter by seats in a row",
                required=False,
                type={"type": "integer"},
            ),
            OpenApiParameter(
                name="seats_in_rowgt",
                description="Filter seats in a row greater than a value",
                required=False,
                type={"type": "integer"},
            ),
            OpenApiParameter(
                name="seats_in_rowlt",
                description="Filter seats in a row less than a value",
                required=False,
                type={"type": "integer"},
            ),
            OpenApiParameter(
                name="seats_range",
                description="Filter seats within a range",
                required=False,
                type={"type": "string"},
            ),
        ],
        responses={200: PlanetariumDomeSerializer(many=True)},
    )


class TicketSchema:
    list = extend_schema(
        parameters=[
            OpenApiParameter(
                name="title",
                description="Filter by title",
                required=False,
                type={"type": "string"},
            ),
        ],
        responses={200: TicketListSerializer(many=True)},
    )


class ReservationSchema:
    list = extend_schema(
        parameters=[
            OpenApiParameter(
                name="user",
                description="User making the request",
                required=True,
                type={"type": "object"},
            ),
        ],
        responses={
            200: OpenApiResponse(
                description="A list of queryset objects with user-specific annotations"
            ),
            403: OpenApiResponse(
                description="Forbidden if the user does not have permission"
            ),
        },
    )


class ShowSessionUploadSchema:
    show_session_upload_schema = extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "format": "binary",
                        "description": "CSV file containing show session data",
                    }
                },
                "required": ["file"],
            }
        },
        responses={
            201: OpenApiResponse(description="Successfully created show sessions"),
            400: OpenApiResponse(
                description="Bad request due to missing or invalid file"
            ),
            400: OpenApiResponse(
                description="Bad request due to invalid data within the file"
            ),
        },
    )
