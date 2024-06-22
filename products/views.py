import json
import random
from collections import Counter

from django.db.models import QuerySet
from rest_framework import status, generics, permissions
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from products.cart import Cart
from products.filters import products_filter, products_sort
from products.models import Tag, Category, Product, Review, Sale
from products.pagination import ProductPagination
from products.serializers import (
    TagSerializer,
    CategorySerializer,
    ProductSerializer,
    SaleSerializer,
    ReviewSerializer,
    CartSerializer,
)


class TagListAPIView(ListAPIView):
    """Class-based view для отображения списка тегов"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CategoryListAPIView(ListAPIView):
    """Class-based view для отображения списка категорий товаров"""

    serializer_class = CategorySerializer

    def get_queryset(self) -> QuerySet:
        queryset = Category.objects.filter(parent_id=None)
        return queryset


class ProductListAPIView(ListAPIView):
    """Class-based view для отображения списка товаров"""

    pagination_class = ProductPagination
    serializer_class = ProductSerializer

    def get_queryset(self):
        data_request = self.request.GET
        products = products_filter(data_request)
        query = Product.objects.filter(**products)
        products_sorted = products_sort(data_request, query=query)
        return products_sorted


class ProductsPopularAPIView(APIView):
    """Class-based view для сортировки товаров по количеству отзывов"""

    def get(self, request: Request) -> Response:
        data = (
            Review.objects.prefetch_related("product")
            .all()
            .values_list("product", flat=True)
            .order_by("id")
        )
        popular_list = list(i[0] for i in Counter(data).most_common(4))
        serialized = ProductSerializer(
            Product.objects.filter(id__in=popular_list), many=True
        )
        return Response(serialized.data, status=status.HTTP_200_OK)


class ProductsLimitedAPIView(APIView):
    """Class-based view для сортировки товаров по полю limited"""

    def get(self, request: Request) -> Response:
        data = Product.objects.filter(limited=True)
        serialized = ProductSerializer(data, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class SalesListAPIView(ListAPIView):
    """Class-based view для отображения списка товаров по акции"""

    pagination_class = ProductPagination
    queryset = Sale.objects.prefetch_related("product").all().order_by("-id")
    serializer_class = SaleSerializer


class BannersAPIVIew(APIView):
    """Class-based view для отображения рекламных баннеров на сайте"""

    def get(self, request: Request) -> Response:
        products_list = list(Product.objects.all())
        random_products = random.sample(products_list, 3)
        serializer = ProductSerializer(random_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BasketAPIView(APIView):
    """Class-based view для отображения корзины покупок"""

    def get(self, request: Request) -> Response:
        cart = Cart(request=request)
        products_list = cart.get_products_list()
        price = cart.get_price()
        products_count = cart.get_products_count()
        serializer = CartSerializer(
            products_list, many=True, context={"count": products_count, "price": price}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        cart = Cart(request=request)
        product_id = request.data.get("id")
        count = request.data.get("count")
        product = Product.objects.get(id=product_id)
        cart.add(product=product, count=count)
        products_list = cart.get_products_list()
        products_count = cart.get_products_count()
        price = cart.get_price()
        serializer = CartSerializer(
            products_list, many=True, context={"count": products_count, "price": price}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request) -> Response:
        body = json.loads(request.body)
        cart = Cart(request=request)
        product_id = body["id"]
        count = body["count"]
        price = cart.get_price()
        product = Product.objects.get(id=product_id)
        if cart.get_products_count()[product_id] == count:
            cart.remove_all(product=product)
        else:
            cart.remove(product=product, count=count)

        products_list = cart.get_products_list()
        products_count = cart.get_products_count()
        serializer = CartSerializer(
            products_list, many=True, context={"count": products_count, "price": price}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailAPIView(generics.RetrieveAPIView):
    """Class-based view для отображения товара"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ReviewAPIView(APIView):
    """Class-based view для отображение отзывов"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request, **kwargs) -> Response:
        email = request.data["email"]
        text = request.data["text"]
        rate = request.data["rate"]
        product = Product.objects.get(id=kwargs["pk"])
        author = request.user
        data = Review.objects.create(
            product=product, author=author, email=email, text=text, rate=rate
        )
        serializer = ReviewSerializer(data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
