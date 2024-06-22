from django.contrib import admin

from products.models import (
    Tag,
    Category,
    Product,
    Review,
    Specification,
    ProductImage,
    Sale,
    CategoryImage,
)

admin.site.register(Tag)


admin.site.register(CategoryImage)


@admin.register(Category)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "parent", "image")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("author", "product")


admin.site.register(Specification)
admin.site.register(ProductImage)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "count", "rating", "limited", "category")


admin.site.register(Sale)
