from .smsthread import *
from .forms import *
from .models import *
from .utils import *
from appauth.utils import get_business_date
from django.utils import timezone
from decimal import Decimal
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import FieldDoesNotExist
from django.core import serializers
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db import connection, transaction
from django.template.loader import render_to_string
from django.db.models import Count, Sum, Avg, Subquery, Q, F
import logging
import sys
from appauth.views import get_global_data
logger = logging.getLogger(__name__)

# ********************** SMS Application Setting Form  *******************************

class sms_application_settings_view(TemplateView):
    template_name = 'sms/sms-application-settings.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        context = dict()
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        form = SMS_Application_Settings_Form()
        context = get_global_data(request)
        context['form'] = form
        context['title'] = 'Samity Admin view'
        return render(request, self.template_name, context)


def sms_application_settings_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    try:
        if request.method == 'POST':
            setting = SMS_Application_Settings.objects.all()
            if len(setting):
                form = SMS_Application_Settings_Form(request.POST, instance=setting[0])
                if form.is_valid():
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Added Successfully!'
                    return JsonResponse(data)
                else:
                    data['error_message'] = form.errors.as_json()
                    return JsonResponse(data)  
            else:
                form = SMS_Application_Settings_Form(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Added Successfully!'
                    return JsonResponse(data)
                else:
                    data['form_is_valid'] = False
                    data['error_message'] = form.errors.as_json()
                    print(data)
                    return JsonResponse(data)
    except Exception as e:
        data['form_is_valid'] = False
        data['error_message'] = str(e)
        return JsonResponse(data)
    
    

      

# ********************** SMS Template ****************************
   
class sms_template_view(TemplateView):
    template_name = 'sms/sms-template-form.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        context=dict()
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        form = sms_template_Form()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)
    
    
@transaction.atomic
def sms_template_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = sms_template_Form(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Create Successfully.'
                else:
                    data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    except Exception as e:
        data['form_is_valid'] = False
        data['error_message'] = str(e)
        return JsonResponse(data)   
    
def sms_template_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(sms_template, id=id)
    template_name = 'sms/sms-template-form-edit.html'
    data = dict()
    if request.method == "POST":
        form = sms_template_Form(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    form_obj = form.save(commit=False)
                    form_obj.save()
                    data['success_message'] = "Update Successfully"
                    data['error_message'] = ''
                    data['form_is_valid'] = True
                    return JsonResponse(data)
            except Exception as e:
                print(str(e))
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)

    else:
        form = sms_template_Form(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request
        )
    return JsonResponse(data) 


# ******************     SMS Send ***********************

class sms_sent_view(TemplateView):
    template_name = 'sms/sms-sent-form.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        context=dict()
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        balance = fn_get_sms_balance()
        form = SMS_Sent_Form(initial={'sms_balance': balance})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def sms_sent_form_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    balance = fn_get_sms_balance()
    data['balance'] = balance
    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = SMS_Sent_Form(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Create Successfully.'
                else:
                    data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    except Exception as e:
        data['form_is_valid'] = False
        data['error_message'] = str(e)
        return JsonResponse(data)   
    
def sms_sent_form_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(sms_sent, id=id)
    template_name = 'sms/sms-sent-form-edit.html'
    data = dict()
    if request.method == "POST":
        form = SMS_Sent_Form(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    form_obj = form.save(commit=False)
                    form_obj.save()
                    data['success_message'] = "Update Successfully"
                    data['error_message'] = ''
                    data['form_is_valid'] = True
                    return JsonResponse(data)
            except Exception as e:
                print(str(e))
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)

    else:
        form = SMS_Sent_Form(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request
        )
    return JsonResponse(data) 


class sms_que_view(TemplateView):
    template_name = 'sms/sms-que-form.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        context = dict()
        balance = fn_get_sms_balance()
        form = SMS_Que_Form(initial={'sms_balance': balance})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def sms_que_form_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    balance = fn_get_sms_balance()
    data['balance'] = balance
    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = SMS_Que_Form(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.template_type='00'
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Send Request Successfully.'
                else:
                    data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    except Exception as e:
        data['form_is_valid'] = False
        data['error_message'] = str(e)
        return JsonResponse(data)

def sms_que_form_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(sms_que, id=id)
    template_name = 'sms/sms-que-form-edit.html'
    data = dict()
    data['form_is_valid'] = False
    if request.method == "POST":
        form = SMS_Que_Form(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    form_obj = form.save(commit=False)
                    form_obj.save()
                    post.template_type='manual-sms'
                    data['success_message'] = "Update Successfully"
                    data['error_message'] = ''
                    data['form_is_valid'] = True
                    return JsonResponse(data)
            except Exception as e:
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = SMS_Que_Form(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request
        )
    return JsonResponse(data)


def sms_que_delete(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    try:
        sms_que.objects.filter(id=id).delete()
        data['form_is_valid'] = True
        data['success_message'] = 'Request Delete Successfully!'
    except Exception as e:
        data['error_message'] = str(e)
        data['form_is_valid'] = False
    return JsonResponse(data)

class sms_sent_query(TemplateView):
    template_name = 'sms/sms-sent-query.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        context = dict()
        balance = fn_get_sms_balance()
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        form = SMS_Sent_Form(initial={'sms_balance': balance, 'from_date':cbd,'upto_date':cbd})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)
