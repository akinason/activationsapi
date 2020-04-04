from datetime import datetime
from rest_framework import generics, status
from rest_framework.response import Response

from activation.models import Order
from activation.public.serializers import OrderDetailSerializer, OrderUpdateSerializer


class OrderDetailView(generics.GenericAPIView):

    def get(self, request, reference, format=None):
        order = Order.get_order_using_reference(reference)
        if order is None or not order.is_paid:
            return Response({"success": False, "data": {}, "error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderDetailSerializer(order)
        return Response({"success": True, "data": serializer.data, "error": ""}, status=status.HTTP_200_OK)

    def put(self, request, reference, format=None):
        data = request.data
        order = Order.get_order_using_reference_and_license_key(reference=data.get("reference", ""), license_key=data.get('license_key'))

        if order is None or not order.is_paid or order.is_used:
            return Response({"success": False, "data": {}, "error": "Incorrect reference and license code or license code already used."}, status=status.HTTP_404_NOT_FOUND)

        order.is_used = True
        order.updated_on = datetime.utcnow()
        order.save()
        serializer = OrderDetailSerializer(order)
        return Response({"success": True, "data": serializer.data, "error": ""}, status=status.HTTP_200_OK)
