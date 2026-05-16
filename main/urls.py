from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'menu', views.MenuItemViewSet)
router.register(r'reservations', views.ReservationViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('booking/', views.booking, name='booking'),
    path('api/', include(router.urls)),
    path('api/categories/', views.categories, name='api-categories'),
    path('api/specials/', views.specials, name='api-specials'),
    path('api/availability/', views.availability, name='api-availability'),
]
