from django.db import models

from products.models import Product
from profiles.models import Profile


class Order(models.Model):
    """Модель заказа"""

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        verbose_name="Profile",
        related_name="profile",
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    deliveryChoice = (
        ("free", "free"),
        ("express", "express"),
        ("ordinary", "ordinary"),
    )
    paymentChoice = (("online", "online"), ("offline", "offline"))
    deliveryType = models.CharField(
        max_length=50, choices=deliveryChoice, default="free", blank=True, null=True
    )
    paymentType = models.CharField(
        max_length=50, choices=paymentChoice, default="online", blank=True, null=True
    )
    totalCost = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Total price",
    )
    status = models.CharField(max_length=50, verbose_name="Status")
    city = models.CharField(max_length=50, verbose_name="City")
    address = models.CharField(max_length=250, verbose_name="Address")
    products = models.ManyToManyField(Product, related_name="orders")

    objects = models.Manager()

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order №{self.pk} from {self.createdAt}: {self.profile} - {self.city}, {self.address}"


class OrderProducts(models.Model):
    """Модель для создания заказа с товарами"""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Order")
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, verbose_name="Product"
    )
    count = models.PositiveIntegerField(verbose_name="Count")

    objects = models.Manager()
