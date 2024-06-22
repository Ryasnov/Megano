from django.urls import path

from products.views import (
    TagListAPIView,
    CategoryListAPIView,
    ProductListAPIView,
    ProductsPopularAPIView,
    ProductsLimitedAPIView,
    SalesListAPIView,
    BannersAPIVIew,
    BasketAPIView,
    ProductDetailAPIView,
    ReviewAPIView,
)

urlpatterns = [
    path("tags/", TagListAPIView.as_view()),
    path("categories/", CategoryListAPIView.as_view()),
    path("catalog/", ProductListAPIView.as_view()),
    path("product/<int:pk>/", ProductDetailAPIView.as_view()),
    path("product/<int:pk>/reviews/", ReviewAPIView.as_view()),
    path("products/popular/", ProductsPopularAPIView.as_view()),
    path("products/limited/", ProductsLimitedAPIView.as_view()),
    path("sales/", SalesListAPIView.as_view()),
    path("banners/", BannersAPIVIew.as_view()),
    path("basket/", BasketAPIView.as_view()),
]
