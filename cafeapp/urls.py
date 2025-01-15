from django.urls import path
from cafeapp.views import (
    OrderListApiView, OrderDetailApiView, OrderCreateApiView,
    OrderUpdateApiView, OrderDeleteApiView,
    RevenueApiView, UpdateOrderStatusAPIView,
    MarkOrderAsPaidAPIView, MarkOrderAsDoneAPIView
)

urlpatterns = [
    path('orders/', OrderListApiView.as_view(), name='order-list'),
    path('orders/<int:pk>', OrderDetailApiView.as_view(), name='order-detail'),
    path('orders/create/', OrderCreateApiView.as_view(), name='order-create'),
    path('orders/<int:pk>/update/', OrderUpdateApiView.as_view(), name='order-update'),
    path("orders/<int:pk>/update-status/", UpdateOrderStatusAPIView.as_view(), name="update-order-status"),
    path('orders/<int:pk>/delete/', OrderDeleteApiView.as_view(), name='order-delete'),
    path('orders/revenue/', RevenueApiView.as_view(), name='order-revenue'),
    path("orders/<int:pk>/mark-paid/", MarkOrderAsPaidAPIView.as_view(), name="mark-order-paid"),
    path("orders/<int:pk>/mark-done/", MarkOrderAsDoneAPIView.as_view(), name="mark-order-done"),

]
