from django.db import models
from django.conf import settings
from catalog.models import Product  # если есть отдельная модель Product

class Order(models.Model):
    STATUS_CHOICES = [
        ("new", "Новый"),
        ("processing", "В обработке"),
        ("done", "Завершён"),
        ("canceled", "Отменён"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="orders"
    )
    product = models.ForeignKey(
    Product,
    null=True,         # разрешаем null
    blank=True,        # разрешаем пустое поле в формах
    on_delete=models.SET_NULL
)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ #{self.id} ({self.get_status_display()})"