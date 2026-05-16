from django.db import models

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('appetizers', 'Закуски'),
        ('main_courses', 'Основні страви'),
        ('seafood', 'Морські страви'),
        ('drinks', 'Напої'),
        ('desserts', 'Десерти'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='main_courses', verbose_name='Категорія')
    is_special = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Страва'
        verbose_name_plural = 'Страви'

    def __str__(self):
        return self.name


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Очікує'),
        ('confirmed', 'Підтверджено'),
        ('cancelled', 'Скасовано'),
    ]

    name = models.CharField(max_length=100, verbose_name='Ім\'я')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    guests_count = models.PositiveIntegerField(verbose_name='Кількість гостей')
    reservation_date = models.DateTimeField(verbose_name='Дата бронювання')
    special_requests = models.TextField(blank=True, verbose_name='Спеціальні прохання')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Створено')

    class Meta:
        verbose_name = 'Бронювання'
        verbose_name_plural = 'Бронювання'
        ordering = ['-reservation_date']

    def __str__(self):
        return f'{self.name} - {self.reservation_date.strftime("%d.%m.%Y %H:%M")}'
