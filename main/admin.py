from django.contrib import admin
from .models import MenuItem, Reservation

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_special')
    list_filter = ('category', 'is_special')
    search_fields = ('name', 'description')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'reservation_date', 'guests_count', 'status')
    list_filter = ('status', 'reservation_date')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at',)
