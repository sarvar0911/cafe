from django.shortcuts import get_object_or_404
from rest_framework import generics, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum

from cafe import pagination
from cafeapp.models import Order
from cafeapp.serializers import OrderSerializer


class OrderListApiView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = pagination.Pagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['table_number', 'status']


class OrderDetailApiView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderCreateApiView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        items = serializer.validated_data.get('items', [])
        total_price = sum(item.get('price', 0) for item in items)
        serializer.save(total_price=total_price)


class OrderUpdateApiView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class OrderDeleteApiView(generics.DestroyAPIView):
    queryset = Order.objects.all()


class RevenueApiView(APIView):
    def get(self, request):
        total_revenue = Order.objects.filter(status='paid').aggregate(Sum('total_price'))['total_price__sum'] or 0.00
        return Response({'total_revenue': total_revenue},
                        status=status.HTTP_200_OK)


class UpdateOrderStatusAPIView(APIView):
    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        status_value = request.data.get("status")

        if status_value not in dict(Order.STATUS_CHOICES):
            return Response({"error": "Invalid status value."},
                            status=status.HTTP_400_BAD_REQUEST)

        order.status = status_value
        order.save()
        return Response({"message": "Status updated successfully.",
                        "order": OrderSerializer(order).data},
                        status=status.HTTP_200_OK)


class MarkOrderAsPaidAPIView(APIView):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        if order.status == "paid":
            return Response({"error": "Order is already paid."},
                            status=status.HTTP_400_BAD_REQUEST)

        order.status = "paid"
        order.save()
        return Response({"message": "Order marked as paid.",
                         "order": OrderSerializer(order).data},
                         status=status.HTTP_200_OK)


class MarkOrderAsDoneAPIView(APIView):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        if order.status == "done":
            return Response({"error": "Order is already done."},
                            status=status.HTTP_400_BAD_REQUEST)

        order.status = "done"
        order.save()
        return Response({"message": "Order marked as done.",
                         "order": OrderSerializer(order).data},
                         status=status.HTTP_200_OK)
