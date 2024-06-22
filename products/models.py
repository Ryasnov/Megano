from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db import models


def product_image_path(instance: "ProductImage", filename: str) -> str:
    """Функция для определения адреса картинки продукта"""

    bad_symbols = '."/]\[\\:;|=,'
    product_name = str(instance.product)

    new_name = str()
    for symbol in product_name:
        if symbol not in bad_symbols:
            new_name += symbol

    return f"app_products/products/{new_name}/{filename}"


class Tag(models.Model):
    """Модель тега"""

    name = models.CharField(max_length=100, db_index=True, verbose_name="Name")

    objects = models.Manager()

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self) -> str:
        return self.name


class CategoryImage(models.Model):
    """Модель картинки для категории"""

    src = models.ImageField(upload_to="app_products/categories/", null=True, blank=True)
    alt = models.CharField(
        max_length=128, null=False, blank=True, verbose_name="Description"
    )

    objects = models.Manager()

    class Meta:
        verbose_name = "Category image"
        verbose_name_plural = "Category images"


class Category(models.Model):
    """Модель категории товаров"""

    title = models.CharField(max_length=100, db_index=True, verbose_name="Title")
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="subcategory",
        null=True,
        blank=True,
        verbose_name="Category",
    )
    image = models.ForeignKey(
        CategoryImage,
        on_delete=models.CASCADE,
        related_name="image",
        verbose_name="CategoryImage",
    )

    objects = models.Manager()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


class Specification(models.Model):
    """Модель спецификации товара"""

    name = models.CharField(max_length=100, db_index=True, verbose_name="Name")
    value = models.TextField(db_index=True, verbose_name="Value")

    objects = models.Manager()

    class Meta:
        verbose_name = "Specification"
        verbose_name_plural = "Specifications"

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    """Модель товара"""

    ordering = ["name"]
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="products",
        verbose_name="Category",
    )
    price = models.DecimalField(
        default=0, max_digits=10, decimal_places=2, verbose_name="Price"
    )
    count = models.IntegerField(
        default=0, validators=[MinValueValidator], verbose_name="Count"
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date")
    title = models.CharField(max_length=100, db_index=True, verbose_name="Title")
    description = models.CharField(max_length=100, verbose_name="Description")
    fullDescription = models.TextField(verbose_name="Full description")
    freeDelivery = models.BooleanField(default=False, verbose_name="Free delivery")
    tags = models.ManyToManyField(
        Tag, blank=True, related_name="product_tags", verbose_name="Tags"
    )
    specifications = models.ManyToManyField(
        Specification, blank=True, related_name="Specifications"
    )
    rating = models.DecimalField(
        max_digits=2, decimal_places=1, default=3.0, validators=[MaxValueValidator(5.0)]
    )
    limited = models.BooleanField(default=False)

    objects = models.Manager()

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    """Модель картинки товара"""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images", verbose_name="Product"
    )
    src = models.ImageField(upload_to=product_image_path)
    alt = models.CharField(
        max_length=128, null=False, blank=True, verbose_name="Description"
    )

    objects = models.Manager()

    class Meta:
        verbose_name = "Product image"
        verbose_name_plural = "Product Images"

    def __str__(self) -> str:
        return f"{self.product} image {self.src}"


class Review(models.Model):
    """Модель отзыва о товаре"""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="reviews",
        verbose_name="Product",
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Author")
    email = models.EmailField(max_length=50, verbose_name="Email")
    text = models.TextField(verbose_name="Text")
    rate = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Rate",
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date")

    objects = models.Manager()

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return f"Review by {self.author} about {self.product}"


class Sale(models.Model):
    """Модель распродажи"""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="sale", verbose_name="Product"
    )
    salePrice = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        blank=True,
        db_index=True,
        verbose_name="Sale price",
    )
    dateFrom = models.DateTimeField(verbose_name="Date from")
    dateTo = models.DateTimeField(verbose_name="Date to")
    title = models.CharField(max_length=100, verbose_name="Title")

    objects = models.Manager()

    class Meta:
        verbose_name = "Sale"
        verbose_name_plural = "Sales"

    def __str__(self):
        return self.title
