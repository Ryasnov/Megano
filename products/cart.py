from django.conf import settings
from rest_framework.request import Request

from .models import Product, Sale


class Cart(object):
    """Класс корзины покупок"""

    def __init__(self, request: Request):
        """Инициализация корзины"""

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product: Product, count: int):
        """Добавить продукт в корзину или обновить его количество"""

        product_id = str(product.id)

        try:
            price = Sale.objects.filter(product=product)[0].salePrice
        except Exception:
            price = product.price

        if product_id not in self.cart.keys():
            self.cart[product_id] = {"count": count, "price": str(price)}
        else:
            self.cart[product_id]["count"] += count

        self.save()

    def save(self):
        """Сохранение изменений сессии"""

        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
        self.session.save()

    def remove(self, product: Product, count: int):
        """Удаление некоторого количества товара из корзины"""

        product_id = str(product.id)
        if product_id in self.cart.keys():
            self.cart[product_id]["count"] -= count
            self.save()

    def remove_all(self, product: Product):
        """Удаление товара из корзины"""

        if isinstance(product, Product):
            product_id = str(product.id)

        if product_id in self.cart.keys():
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Перебор элементов в корзине и получение продуктов из базы данных"""

        for item in self.cart.values():
            item["price"] = float(item["price"])
            item["total_price"] = item["price"] * item["count"]
            yield item

    def get_products_list(self) -> list:
        """Функция возвращающая список товаров в корзине"""

        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_count(self):
        """Функция подсчета товаров в корзине"""

        count = 0
        for item in self.cart.values():
            count += item["count"]
        return count

    def get_products_count(self) -> dict:
        """Функция подсчета количество каждого товара в корзине"""
        count = dict()

        for product in self.cart:
            count[int(product)] = self.cart[product]["count"]

        return count

    def get_price(self) -> dict:
        """Функция подсчета цены для каждого товара с учетом акций"""

        prices = dict()

        for product in self.cart:
            prices[int(product)] = self.cart[product]["price"]

        return prices

    def get_total_price(self):
        """Расчет общей стоимости товаров в корзине"""

        return round(
            sum(float(item["price"]) * item["count"] for item in self.cart.values()), 2
        )

    def clear(self):
        """Очистка сеанса корзины"""

        self.cart = {}
        self.save()
