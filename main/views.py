from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import MenuItem, Reservation
from .serializers import MenuItemSerializer, ReservationSerializer


def home(request):
    menu_items = MenuItem.objects.all().order_by('category', 'name')[:6]
    return render(request, 'home.html', {
        'title': 'Ресторан «Чорна Вітрильна»',
        'headline': 'Пірнати в смаки морів',
        'tagline': 'Піратська їжа, морські легенди та затишна атмосфера.',
        'menu_items': menu_items,
    })


def menu(request):
    menu_items = MenuItem.objects.all().order_by('category', 'name')
    categories = MenuItem.CATEGORY_CHOICES
    return render(request, 'menu.html', {
        'title': 'Меню - Ресторан «Чорна Вітрильна»',
        'menu_items': menu_items,
        'categories': categories,
    })


def booking(request):
    menu_items = MenuItem.objects.all().order_by('category', 'name')
    return render(request, 'booking.html', {
        'title': 'Бронювання - Ресторан «Чорна Вітрильна»',
        'menu_items': menu_items,
    })


class MenuItemViewSet(viewsets.ModelViewSet):
    """CRUD для пунктів меню. List/retrieve доступні всім, create/update/delete — лише авторизованим."""
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'specials', 'categories']:
            return [AllowAny()]
        return [IsAuthenticated()]


class ReservationViewSet(viewsets.ModelViewSet):
    """CRUD для бронювань. Створення й редагування — лише для авторизованих користувачів."""
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status']
    ordering_fields = ['reservation_date']
    ordering = ['-reservation_date']

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def confirm(self, request, pk=None):
        reservation = self.get_object()
        reservation.status = 'confirmed'
        reservation.save()
        return Response({'status': 'confirmed'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        reservation.status = 'cancelled'
        reservation.save()
        return Response({'status': 'cancelled'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def categories(request):
    data = [{'key': k, 'label': v} for k, v in MenuItem.CATEGORY_CHOICES]
    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def specials(request):
    specials_qs = MenuItem.objects.filter(is_special=True)
    serializer = MenuItemSerializer(specials_qs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def availability(request):
    # Простий приклад: повернути доступність столиків на дату (query param: date)
    date = request.query_params.get('date')
    # Заглушка: завжди повертаємо available=true (реальну логіку можна додати пізніше)
    return Response({'date': date, 'available': True})
