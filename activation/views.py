from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.views import generic
from django.shortcuts import HttpResponse, HttpResponseRedirect

from rest_framework import generics, status
from rest_framework.response import Response

from workers.client import gm_client
from .serializers import SoftwareSerializer, OrderSerializer, OrderUpdateSerializer, OrderCreateSerializer
from . import models
from contrib.authentication import HTTPAuthentication
from contrib.lib.flutterwave import Flutterwave
from contrib.lib.gloxon import gloxonAuth


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


class OauthReturnView(generic.View):

    def get(self, request, *args, **kwargs):
        authorization_code = request.GET.get('authorization_code')
        _status = request.GET.get('status')

        if _status != "accepted":
            messages.warning(request, "Authentication was not successful, please try again.")
            return HttpResponseRedirect('/login')
        else:
            res = gloxonAuth.exchangeAuthorizationCode(authorization_code)
            if not res['success']:
                messages.warning(request, "Authentication was not successful, please try again.")
                return HttpResponseRedirect('/login')

            _user = res.get('user')
            email = _user.get('email')

            if models.User.objects.filter(gloxon_id=_user.get('public_id')).exists():
                user = models.User.objects.get(gloxon_id=_user.get('public_id'))
            else:
                user = models.User(
                    email=email, first_name=_user.get('first_name'), last_name=_user.get('last_name'), username=email
                )
                user.mobile = _user.get('phone')
                user.gloxon_id = _user.get('public_id')
                user.is_active = True
                user.is_staff = True
                user.gloxon_data = res
                user.generate_api_keys()
                user.set_password(user.access_secret)
                user.save()
                group = Group.objects.get(name="developer")
                user.groups.add(group)

            user_ = authenticate(request, username=user.email, password=user.access_secret)

            if user_:
                login(request, user_)
                return HttpResponseRedirect('/')
            else:
                messages.warning(request, "Authentication was not successful, please try again.")
                return HttpResponseRedirect('/login')


oauth_return_view = OauthReturnView.as_view()
