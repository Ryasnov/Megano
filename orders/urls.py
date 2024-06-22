from django.urls import path

from orders.views import OrderAPIView, OrderDetailView, PaymentAPIView

urlpatterns = [
    path("orders/", OrderAPIView.as_view()),
    path("order/<id>/", OrderDetailView.as_view()),
    path("payment/<id>/", PaymentAPIView.as_view()),
]
