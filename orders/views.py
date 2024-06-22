from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from orders.models import Order, OrderProducts
from orders.serializers import OrderSerializer
from products.cart import Cart
from products.models import Product
from profiles.models import Profile


class OrderAPIView(APIView):
    """Class-Based View для заполнения анкеты заказа"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        data = Order.objects.filter(profile_id=request.user.profile.pk)
        serializer = OrderSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        cart = Cart(request=request)
        profile = Profile.objects.filter(user=request.user)[0]
        request_data = [
            (data["id"], data["price"], data["count"]) for data in request.data
        ]
        products = Product.objects.filter(id__in=[data[0] for data in request_data])
        order = Order.objects.create(profile=profile, totalCost=cart.get_total_price())
        response = {"orderId": order.pk}
        order.products.set(products)
        order.save()
        return Response(response, status=status.HTTP_200_OK)


class OrderDetailView(APIView):
    """Class-Based View для отображения страницы заказа"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, id: int) -> Response:
        order = Order.objects.get(pk=id)
        serializer = OrderSerializer(order)
        cart = Cart(request=request).cart
        data = serializer.data
        products = data["products"]

        try:
            query = OrderProducts.objects.filter(order_id=id)
            unic_products = {obj.product.pk: obj.count for obj in query}
            for product in products:
                product["count"] = unic_products[product["id"]]
        except Exception:
            for product in products:
                product["count"] = cart[str(product["id"])]["count"]

        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request: Request, id: int) -> Response:
        cart = Cart(request=request)
        order = Order.objects.get(id=id)
        data = request.data
        order.fullName = data["fullName"]
        order.phone = data["phone"]
        order.email = data["email"]
        order.deliveryType = data["deliveryType"]
        order.city = data["city"]
        order.address = data["address"]
        order.paymentType = data["paymentType"]
        order.status = "expecting payment"

        if order.deliveryType == "express":
            order.totalCost += 15
        else:
            order.totalCost += 5

        for i_product in data["products"]:
            product = Product.objects.get(id=i_product["id"])
            product.count -= i_product["count"]
            product.save()
            OrderProducts.objects.get_or_create(
                order_id=order.pk, product_id=i_product["id"], count=i_product["count"]
            )

        order.save()
        cart.clear()
        return Response({"orderId": order.id}, status=status.HTTP_201_CREATED)


class PaymentAPIView(APIView):
    """Class-Based View для оплаты заказа"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request, id: int) -> Response:
        order = Order.objects.get(id=id)
        order.status = "paid"
        order.save()
        return Response(request.data, status=status.HTTP_200_OK)
