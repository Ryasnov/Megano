import pytz

from django.core.validators import MaxValueValidator
from django.db.models import QuerySet
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from products.models import (
    Tag,
    CategoryImage,
    Category,
    Product,
    Review,
    ProductImage,
    Sale,
    Specification,
)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели Tag"""

    class Meta:
        model = Tag
        fields = ("id", "name")


class CategoryImageSerializer(serializers.ModelSerializer):
    """Сериализатор модели CategoryImage"""

    class Meta:
        model = CategoryImage
        fields = ("src", "alt")


class SubcategorySerializer(serializers.Field):
    """Сериализатор для подкатегорий"""

    def get_attribute(self, instance: Category) -> QuerySet:
        subcategory = Category.objects.filter(parent=instance)
        return subcategory

    def to_representation(self, value: QuerySet) -> list:
        values = list()
        for subcategory in value:
            temp = {"id": subcategory.id, "title": subcategory.title}
            try:
                image = CategoryImage.objects.get(id=temp["id"])
                temp["image"] = {"src": image.src.url, "alt": image.alt}
            except ObjectDoesNotExist:
                temp["image"] = None
            values.append(temp)
        return values


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category"""

    image = CategoryImageSerializer()
    subcategories = SubcategorySerializer()

    class Meta:
        model = Category
        fields = ("id", "title", "image", "subcategories")


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review"""

    author = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ("author", "email", "text", "rate", "date")

    def get_author(self, obj: Review) -> str:
        if isinstance(obj, Review):
            return obj.author.username

    def get_email(self, obj: Review) -> str:
        if isinstance(obj, Review):
            return obj.email

    def get_text(self, obj: Review) -> str:
        if isinstance(obj, Review):
            return obj.text

    def get_date(self, obj: Review) -> str:
        if isinstance(obj, Review):
            return obj.date.strftime("%Y-%m-%d %H:%M")

    def get_attribute(self, instance: Product) -> Product:
        return instance

    def get_rate(self, obj: Review):
        if isinstance(obj, Review):
            return obj.rate


class ProductImageSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ProductImage"""

    class Meta:
        model = ProductImage
        fields = ("src", "alt")


class ProductListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка товаров"""

    reviews = ReviewSerializer()
    images = ProductImageSerializer(many=True)
    tags = TagSerializer(many=True)
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, coerce_to_string=False
    )
    rating = serializers.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=3.0,
        validators=[MaxValueValidator(5.0)],
        coerce_to_string=False,
    )
    date = SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "rating",
        )

    def get_date(self, obj: Product) -> str:
        date = obj.date.astimezone(pytz.timezone("CET"))
        return date.strftime("%a %b %d %Y %H:%M:%S")


class SaleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Sale"""

    id = serializers.SerializerMethodField()
    salePrice = serializers.DecimalField(
        max_digits=10, decimal_places=2, coerce_to_string=False
    )
    dateFrom = serializers.SerializerMethodField()
    dateTo = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    def get_dateFrom(self, obj: Sale) -> str:
        return obj.dateFrom.strftime("%m-%d")

    def get_dateTo(self, obj: Sale) -> str:
        return obj.dateTo.strftime("%m-%d")

    def get_id(self, obj: Sale) -> int:
        return obj.product.id

    def get_price(self, obj: Sale) -> float:
        return obj.product.price

    def get_images(self, obj: Sale) -> list:
        queryset = ProductImage.objects.filter(product=obj.product)
        images = list({"src": image.src.url, "alt": image.alt} for image in queryset)
        return images

    class Meta:
        model = Sale
        fields = ("id", "price", "salePrice", "dateFrom", "dateTo", "title", "images")


class CartSerializer(ProductListSerializer):
    """Сериализатор для количества товаров в корзине"""

    count = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    def get_count(self, obj):
        return int(self.context["count"][obj.id])

    def get_price(self, obj):

        return float(self.context["price"][obj.id])


class SpecificationSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Specification"""

    class Meta:
        model = Specification
        fields = ("name", "value")


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Product"""

    reviews = ReviewSerializer(many=True)
    images = ProductImageSerializer(many=True)
    tags = TagSerializer(many=True)
    specifications = SpecificationSerializer(many=True)
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, coerce_to_string=False
    )
    rating = serializers.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=3.0,
        validators=[MaxValueValidator(5.0)],
        coerce_to_string=False,
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "fullDescription",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "specifications",
            "rating",
        )
