from django.contrib import admin
from api.models import ShowTheme, AstronomyShow, ShowSession, PlanetariumDome, Ticket, Reservation


class ShowThemeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)


class AstronomyShowAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    ordering = ('title',)


class ShowSessionAdmin(admin.ModelAdmin):
    list_display = ('astronomy_show', 'show_time')
    ordering = ('-show_time',)


class PlanetariumDomeAdmin(admin.ModelAdmin):
    list_display = ('name', 'rows', 'seats_in_row')
    ordering = ('name',)


class TicketAdmin(admin.ModelAdmin):
    list_display = ('row', 'seat', 'show_session', 'reservation')
    ordering = ('-reservation__created_at',)


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    ordering = ('-created_at',)


admin.site.register(ShowTheme, ShowThemeAdmin)
admin.site.register(AstronomyShow, AstronomyShowAdmin)
admin.site.register(ShowSession, ShowSessionAdmin)
admin.site.register(PlanetariumDome, PlanetariumDomeAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Reservation, ReservationAdmin)
