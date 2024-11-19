from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from rest_framework import generics
from django.db.models import Case, CharField, Value, When, F
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
import datetime
from django.contrib.auth import get_user_model
# Create your views here.

from sms.models import *

from apisms.serializers import *
# from sms.utils import fn_get_transaction_account_type, fn_get_transaction_account_type_screen


class SMS_Application_Setting_ApiView(generics.ListAPIView):
    serializer_class = SMS_Application_Setting_Serializer

    def get_queryset(self):
        queryset = SMS_Application_Settings.objects.filter().order_by('id')
        return queryset


class SMS_template_ApiView(generics.ListAPIView):
    serializer_class = sms_template_Serializer

    def get_queryset(self):
        queryset = sms_template.objects.filter().order_by('id')
        return queryset


class SMS_Sent_ApiView(generics.ListAPIView):
    serializer_class = sms_sent_Serializer

    def get_queryset(self):
        template_type = self.request.query_params.get('template_type', None)
        mobile_number = self.request.query_params.get('mobile_number', None)
        from_date = self.request.query_params.get('from_date', None)
        upto_date = self.request.query_params.get('upto_date', None)

        queryset = sms_sent.objects.filter().order_by('id')
        if template_type:
            queryset = queryset.filter(template_type=template_type)

        if mobile_number:
            queryset = queryset.filter(mobile_number=mobile_number)

        if from_date:
            queryset = queryset.filter(app_data_time__gte=from_date)

        if upto_date:
            queryset = queryset.filter(app_data_time__lte=upto_date)

        return queryset

class SMS_que_ApiView(generics.ListAPIView):
    serializer_class = sms_que_Serializer

    def get_queryset(self):
        template_type = self.request.query_params.get('template_type', None)
        mobile_number = self.request.query_params.get('mobile_number', None)

        queryset = sms_que.objects.filter().order_by('id')

        if template_type:
            queryset = queryset.filter(template_type=template_type)

        if mobile_number:
            queryset = queryset.filter(mobile_number=mobile_number)

        return queryset
