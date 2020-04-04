from datetime import datetime

from rest_framework import generics, status
from rest_framework.response import Response

from workers.client import gm_client
from .serializers import SoftwareSerializer, OrderSerializer, OrderUpdateSerializer, OrderCreateSerializer
from . import models
from contrib.authentication import HTTPAuthentication
from contrib.lib.flutterwave import Flutterwave


class SoftwareListView(generics.GenericAPIView):
    authentication_classes = (HTTPAuthentication, )

    def get(self, request, format=None):
        """URL to get all softwares."""
        softwares = models.Software.objects.filter(is_active=True)
        serializer = SoftwareSerializer(softwares, many=True)
        return Response({"success": True, "data": serializer.data, "error": ""}, status=status.HTTP_200_OK)


class SoftwareDetailView(generics.GenericAPIView):
    authentication_classes = (HTTPAuthentication,)

    def get(self, request, pk, format=None):
        try:
            software = models.Software.objects.filter(pk=pk, is_active=True).get()
        except models.Software.DoesNotExist:
            return Response({"success": False, "data": {}, "error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SoftwareSerializer(software)
        return Response({"success": True, "data": serializer.data, "error": ""}, status=status.HTTP_200_OK)


class OrderListView(generics.GenericAPIView):
    authentication_classes = (HTTPAuthentication,)

    def post(self, request, format=None):
        serializer = OrderCreateSerializer(data=request.data)

        if serializer.is_valid():
            obj = serializer.save()
            obj.set_reference()
            obj.save()
            serializer = OrderCreateSerializer(obj)
            return Response({"success": True, "data": serializer.data, "error": "", "flutterwave_public_key": obj.software.author.rave_public_key}, status=status.HTTP_200_OK)

        return Response({"success": True, "data": {}, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(generics.GenericAPIView):
    authentication_classes = (HTTPAuthentication,)

    def put(self, request, pk, format=None):
        """Generate the license key and mark mark the order as paid."""
        try:
            order = models.Order.objects.get(pk=pk)
        except models.Order.DoesNotExist:
            return Response({"success": False, "data": {}, "error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

        if order.is_paid or order.is_used:
            return Response({"success": False, "data": {}, "error": "Order already paid or License key already used."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderUpdateSerializer(order, data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            obj.set_license_key()
            obj.is_paid = True
            obj.save()

            rave_secret_key = obj.software.author.rave_secret_key
            send_license_key = False

            if rave_secret_key:
                flutterwave = Flutterwave(secret_key=rave_secret_key)
                if flutterwave.verify_payment(reference=obj.reference)["success"]:  # if the payment is successful.
                    send_license_key = True
                    obj.is_verified = True
                else:
                    return Response({"success": False, "data": {}, "error": "Payment could not be verified."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                obj.is_verified = True
                send_license_key = True

            # save modified object.
            obj.updated_on = datetime.utcnow()
            obj.save()
            serializer = OrderCreateSerializer(obj)

            if send_license_key:
                data = {
                    "reference": obj.reference, "name": obj.name, "email": obj.email, "duration": obj.license.duration,
                    "amount": str(serializer.data.get('amount')), "currency": obj.currency, "software": obj.software.name,
                    "license_key": models.Order.format_license_key(obj.license_key)
                }
                gm_client.submit_job('mail.license_key', data=data, wait_until_complete=False)
                return Response({"success": True, "data": serializer.data, "error": ""}, status=status.HTTP_200_OK)

        return Response({"success": False, "data": {}, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ResendEmailView(generics.GenericAPIView):

    authentication_classes = (HTTPAuthentication, )

    def post(self, request, format=None):
        order = models.Order.get_order_using_reference(request.data.get('reference'))
        if order is None:
            return Response({"success": False, "data": {}, "error": "Order Not Found"}, status=status.HTTP_404_NOT_FOUND)

        if order.is_paid and not order.is_used and order.is_verified:
            obj = order
            serializer = OrderCreateSerializer(obj)
            data = {
                "reference": obj.reference, "name": obj.name, "email": obj.email, "duration": obj.license.duration,
                "amount": str(serializer.data.get('amount')), "currency": obj.currency, "software": obj.software.name,
                "license_key": models.Order.format_license_key(obj.license_key)
            }
            gm_client.submit_job('mail.license_key', data=data, wait_until_complete=False)
            return Response({"success": True, "data": serializer.data, "error": ""}, status=status.HTTP_200_OK)

        return Response({"success": False, "data": {}, "error": "Order not paid or license key already used."}, status=status.HTTP_400_BAD_REQUEST)