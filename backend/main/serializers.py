from django.contrib.auth.models import User
from rest_framework import serializers
from .models import MenuItem, Reservation


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'category', 'is_special', 'hit', 'image']


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'name', 'email', 'phone', 'guests_count', 'reservation_date', 'special_requests', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']