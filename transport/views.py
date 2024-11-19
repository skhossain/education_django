import decimal

from django.db.models.fields import NullBooleanField
from .myException import *
from .validations import *
from .utils import *
from .forms import *
from .models import *
from decimal import Context, Decimal
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import FieldDoesNotExist
from django.core import serializers
from random import randint
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import datetime
from datetime import date, datetime, timedelta
from calendar import monthrange
from django.db import connection, transaction
from django.template.loader import render_to_string
from django.db.models import Count, Sum, Avg
import logging
import sys
logger = logging.getLogger(__name__)
from appauth.utils import fn_get_query_result
from appauth.views import get_global_data

class transport_transportation_type(TemplateView):
    template_name = 'transport/transport-transportation-type.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = TransportationTypeModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def transport_transportationtype_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = TransportationTypeModelForm(request.POST)
        if form.is_valid():
            transportation_type_id = fn_get_transportation_type()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.transportation_type_id = transportation_type_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = ' Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def transport_transportationtype_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Transportation_Type, transportation_type_id=id)
    template_name = 'transport/transport-transportationtype-edit.html'
    data = dict()

    if request.method == 'POST':
        form = TransportationTypeModelForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            data['success_message'] = 'Updated Successfully!'
            data['error_message'] = ''
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = TransportationTypeModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)



#####  Create Transportation  ########

class transport_transportation(TemplateView):
    template_name = 'transport/transport-transportation.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = TransportationModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def transport_transportation_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = TransportationModelForm(request.POST)
        if form.is_valid():
            transportation_id = fn_get_transportation()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.transportation_id = transportation_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = ' Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def transport_transportation_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Transportation, transportation_id=id)
    template_name = 'transport/transport-transportation-edit.html'
    data = dict()

    if request.method == 'POST':
        form = TransportationModelForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            data['success_message'] = 'Updated Successfully!'
            data['error_message'] = ''
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = TransportationModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)

#####  Create Location  ########

class transport_location_info(TemplateView):
    template_name = 'transport/transport-location-info.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Location_InfoModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)

def transport_locationinfo_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = Location_InfoModelForm(request.POST)
        if form.is_valid():
            location_info_id = fn_get_locationid()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.location_info_id = location_info_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = ' Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def transport_locationinfo_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Location_Info, location_info_id=id)
    template_name = 'transport/transport-locationinfo-edit.html'
    data = dict()

    if request.method == 'POST':
        form = Location_InfoModelForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            data['success_message'] = 'Updated Successfully!'
            data['error_message'] = ''
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = Location_InfoModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)
    
#####  Create Vehicle Form  ########

class transport_vehicle_info(TemplateView):
    template_name = 'transport/transport-vehicle-info.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Vehicle_InformationModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)

def transport_vehicleinfo_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = Vehicle_InformationModelForm(request.POST)
        if form.is_valid():
            vehicle_id = fn_get_vehicleid()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.vehicle_id = vehicle_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = ' Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def transport_vehicleinfo_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Vehicle_Information, vehicle_id=id)
    template_name = 'transport/transport-vehicleinfo-edit.html'
    data = dict()

    if request.method == 'POST':
        form = Vehicle_InformationModelForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            data['success_message'] = 'Updated Successfully!'
            data['error_message'] = ''
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = Vehicle_InformationModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)

#### Create Driver Form  ####

class transport_driver_info(TemplateView):
    template_name = 'transport/transport-driver-info.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = DriverModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)

def transport_driver_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = DriverModelForm(request.POST)
        if form.is_valid():
            driver_id = fn_get_driverid()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.driver_id = driver_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = ' Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def transport_driver_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Driver, driver_id=id)
    template_name = 'transport/transport-driver-edit.html'
    data = dict()

    if request.method == 'POST':
        form = DriverModelForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            data['success_message'] = 'Updated Successfully!'
            data['error_message'] = ''
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = DriverModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)

#### Create Conductor Form  ####

class transport_conductor_info(TemplateView):
    template_name = 'transport/transport-conductor-info.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = ConductorModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)

def transport_conductor_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = ConductorModelForm(request.POST)
        if form.is_valid():
            conductor_id = fn_get_conductorid()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.conductor_id = conductor_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = ' Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def transport_conductor_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Conductor, conductor_id=id)
    template_name = 'transport/transport-conductor-edit.html'
    data = dict()

    if request.method == 'POST':
        form = ConductorModelForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            data['success_message'] = 'Updated Successfully!'
            data['error_message'] = ''
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = ConductorModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)

#### Create Road Map Form  ####

class transport_roadmap_info(TemplateView):
    template_name = 'transport/transport-road-map.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Road_mapModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)

def transport_roadmap_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = Road_mapModelForm(request.POST)
        if form.is_valid():
            road_map_id = fn_get_roadmapid()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.road_map_id = road_map_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = ' Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def transport_roadmap_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Road_map, road_map_id=id)
    template_name = 'transport/transport-roadmap-edit.html'
    data = dict()

    if request.method == 'POST':
        form = Road_mapModelForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.road_map_id=id
            obj.save()
            data['success_message'] = 'Updated Successfully!'
            data['error_message'] = ''
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = Road_mapModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)

###### Road Map Details Form #####

class transport_roadmapdtl_info(TemplateView):
    template_name = 'transport/transport-roadmap-dtl.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Roadmap_DtlModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def transport_roadmapdtl_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = Roadmap_DtlModelForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def transport_roadmapdtl_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Road_map_Dtl, id=id)
    template_name = 'transport/transport-roadmapdtl-edit.html'
    data = dict()

    if request.method == 'POST':
        form = Roadmap_DtlModelForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            data['success_message'] = 'Updated Successfully!'
            data['error_message'] = ''
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = Roadmap_DtlModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        context['data'] = instance_data
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)

#### Create Admit Transportation Form  ####

class transport_admit_transportation(TemplateView):
    template_name = 'transport/transport-admit-transportation.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Admit_TransportationModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def transport_admit_transportation_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        try:
            with transaction.atomic():
                form = Admit_TransportationModelForm(request.POST)
                if form.is_valid():
                    admit_transportation_id = fn_get_admittransportationid()
                    post = form.save(commit=False)
                    data_filter=dict()
                    if post:
                        data_filter['student_roll']=post.student_roll.student_roll
                        check=Admit_Transportation.objects.filter(**data_filter).exists()
                        if check:
                            data['error_message'] = ' This data already exists.'
                            return JsonResponse(data)
                    post.app_user_id = request.session["app_user_id"]
                    post.admit_transportation_id = admit_transportation_id
                    post.save()
            
                    insertion=Admit_Tran_History()
                    insertion.admit_transportation_id=post
                    insertion.academic_year=post.academic_year
                    insertion.class_id=post.class_id
                    insertion.student_roll=post.student_roll
                    insertion.status=post.status
                    insertion.app_user_id=request.session["app_user_id"]
                    insertion.save()
                    data['form_is_valid'] = True
                    data['success_message'] = ' Added Successfully!'
                else:
                    data['error_message'] = form.errors.as_json()
        except Exception as e:
            logger.error("Error in Creating User {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
            data['error_message'] = 'Error '+str(e)
    return JsonResponse(data)


def transport_admit_transportation_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Admit_Transportation, admit_transportation_id=id)
    template_name = 'transport/transport-admit-transportation-edit.html'
    data = dict()

    if request.method == 'POST':
        form = Admit_TransportationModelForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            data_filter=dict()
            if obj:
                data_filter['student_roll']=obj.student_roll.student_roll
                    
                check=Admit_Transportation.objects.filter(~Q(admit_transportation_id=id),**data_filter).exists()
                if check:
                    data['error_message'] = ' This data already exists.'
                    return JsonResponse(data)
            obj.save()
            data['success_message'] = 'Updated Successfully!'
            data['error_message'] = ''
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = Admit_TransportationModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)





#### Create Payfor Form  ####

class transport_payfor_type(TemplateView):
    template_name = 'transport/transport-payfor-type.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = PayFor_TypesModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)

def transport_payfor_type_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = PayFor_TypesModelForm(request.POST)
        if form.is_valid():
            pay_for_id = fn_get_payforid()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.pay_for_id = pay_for_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = ' Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def transport_payfor_type_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(PayFor_Types, pk=id)
    template_name = 'transport/transport-payfor-type-edit.html'
    data = dict()

    if request.method == 'POST':
        form = PayFor_TypesModelForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            data['success_message'] = 'Updated Successfully!'
            data['error_message'] = ''
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = PayFor_TypesModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


#### Create payment Management Form  ####

class transport_payment_management(TemplateView):
    template_name = 'transport/transport-payment-management.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Payment_ManagementModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)

def transport_payment_management_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = Payment_ManagementModelForm(request.POST)
        if form.is_valid():
            payment_management_id = fn_get_paymentid()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.payment_management_id = payment_management_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = ' Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def transport_payment_management_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Payment_Management, pk=id)
    template_name = 'transport/transport-payment-management-edit.html'
    data = dict()

    if request.method == 'POST':
        form = Payment_ManagementModelForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            data['success_message'] = 'Updated Successfully!'
            data['error_message'] = ''
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = Payment_ManagementModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


#### Create Vehicle Type Form  ####

class transport_vehicle_type(TemplateView):
    template_name = 'transport/transport-vehicle-type.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Vehicle_typeModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)

def transport_vehicle_type_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = Vehicle_typeModelForm(request.POST)
        if form.is_valid():
            vehicle_type_id = fn_get_vehitypeid()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.vehicle_type_id = vehicle_type_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = ' Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def transport_vehicle_type_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Vehicle_type, pk=id)
    template_name = 'transport/transport-vehicletype-edit.html'
    data = dict()

    if request.method == 'POST':
        form = Vehicle_typeModelForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            data['success_message'] = 'Updated Successfully!'
            data['error_message'] = ''
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = Vehicle_typeModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)



class transport_student_attendance(TemplateView):
    template_name = 'transport/transport-student-attendance.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')

        form = Trans_Attendance_Form()
        year=Academic_Year.objects.all()
        classes=Academic_Class.objects.all()
        context = get_global_data(request)
        context['form']=form
        context['years']=year
        context['ssss']=classes
        return render(request, self.template_name, context)

def transport_student_list_ajax(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    template_name = 'transport/transport-student-list-ajax.html'
    context = get_global_data(request)
    data=dict()
    if request.method == 'POST':
        datafilter=dict()
        academic_year=request.POST.get('academic_year')
        class_id=request.POST.get('class_id')
        road_map_id=request.POST.get('road_map_id')
        trans_status=request.POST.get('trans_status')
        if academic_year:
            datafilter['academic_year']=int(academic_year)
        if class_id:
            datafilter['class_id']=class_id
        if road_map_id:
            datafilter['road_map_id']=road_map_id
        addmit_info=Admit_Transportation.objects.filter(**datafilter)
     
        students=[]
        locations=[]
        for index,d in enumerate(addmit_info):
            student=dict()
            location=dict()
            student["student_roll"]=d.student_roll.student_roll
            student["student_name"]=d.student_roll.student_name
            student["location_info_id"]=d.location_info_id.location_info_id
            
            location['location_info_id']=d.location_info_id.location_info_id
            location['location_name']=d.location_info_id.location_name
            students.append(student)
            if not location in locations:
                locations.append(location)
            context['students']=students
            context['locations']=locations
    data['html_form'] = render_to_string(
    template_name, context, request=request)
    return JsonResponse(data)

@transaction.atomic
def transport_student_attendance_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
   
    data=dict()
    if request.method == 'POST':
        road_map_id=request.POST.get('road_map_id')
        trans_status=request.POST.get('trans_status')
        students=request.POST.getlist('students[]')
        try:
            with transaction.atomic():
                for roll in students:
                    admit_info=get_object_or_404(Admit_Transportation,road_map_id=road_map_id,student_roll=roll)
                    data_dict=dict()
                    data_dict['student_roll']=admit_info.student_roll.student_roll
                    data_dict['trans_status']=trans_status
                    data_dict['date_time__date']=datetime.now().date()
                    check=Trans_Attendance.objects.filter(**data_dict).exists()
                    if check:
                        pass
                    else:
                        post=Trans_Attendance()
                        post.academic_year=admit_info.academic_year
                        post.class_id=admit_info.class_id
                        post.road_map_id=admit_info.road_map_id
                        post.location_info_id=admit_info.location_info_id
                        post.student_roll=admit_info.student_roll
                        post.trans_status=trans_status
                        post.app_user_id = request.session["app_user_id"]
                        post.date_time = datetime.now()
                        post.app_data_time = datetime.now()
                        post.save()
                data['form_is_valid'] = True
                data['success_message'] = ' Added Successfully!'
        except Exception as e:
            logger.error("Error in Creating User {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
            data['error_message'] = str(e)
    return JsonResponse(data)


class transport_use_summery(TemplateView):
    template_name = 'transport/transport-use-summery.html'
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Trans_Attendance_Form()
        context = get_global_data(request)
        context['form']=form
        return render(request, self.template_name, context)

    
def transport_use_summery_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Trans_Attendance, pk=id)
    template_name = 'transport/transport-use-summery-edit.html'
    data = dict()
    
    if request.method == 'POST':
        instance_data.trans_status=request.POST.get('trans_status')
        instance_data.app_user_id = request.session["app_user_id"]
        instance_data.save()
        data['form_is_valid'] = True
        data['success_message'] = ' Update Successfully!'
        
    else:
        form = Trans_Attendance_Form(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)

def transport_quick_drop(request,id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Trans_Attendance, pk=id)
    data = dict()
    if request.method == 'POST':
        data_dict=dict()
        data_dict['student_roll']=instance_data.student_roll.student_roll
        data_dict['trans_status']='Drop'
        data_dict['date_time__date']=datetime.now().date()
        check=Trans_Attendance.objects.filter(**data_dict).exists()
        if check:
            pass
        else:
            post=Trans_Attendance()
            post.academic_year=instance_data.academic_year
            post.class_id=instance_data.class_id
            post.road_map_id=instance_data.road_map_id
            post.location_info_id=instance_data.location_info_id
            post.student_roll=instance_data.student_roll
            post.trans_status='Drop'
            post.app_user_id = request.session["app_user_id"]
            post.date_time = datetime.now()
            post.app_data_time = datetime.now()
            post.save()
        data['success_message'] = ' Drop Successfully!'
    return JsonResponse(data)