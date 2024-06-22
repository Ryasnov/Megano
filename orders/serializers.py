import pytz
from rest_framework import serializers

from orders.models import Order
from products.serializers import ProductSerializer
from profiles.models import Profile


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор модели Order"""

    products = ProductSerializer(many=True)
    fullName = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    createdAt = serializers.SerializerMethodField()

    def get_fullName(self, obj: Order) -> str:
        return Profile.objects.get(user=obj.profile.user).fullName

    def get_email(self, obj: Order) -> str:
        return Profile.objects.get(user=obj.profile.user).email

    def get_phone(self, obj: Order) -> str:
        return Profile.objects.get(user=obj.profile.user).phone

    def get_createdAt(self, obj: Order) -> str:
        temp = obj.createdAt.astimezone(pytz.timezone("CET"))
        return temp.strftime("%Y-%m-%d %H:%M")

    class Meta:
        model = Order
        fields = (
            "id",
            "createdAt",
            "fullName",
            "email",
            "phone",
            "deliveryType",
            "paymentType",
            "totalCost",
            "status",
            "city",
            "address",
            "products",
        )
