# App Auth
from itertools import count
import threading
from appauth.views import get_global_data
from appauth.utils import fn_get_query_result
from appauth.forms import *
import time
import os
# from turtle import position
# from ..hrm.validations import app_user_id
import pdfkit
import imgkit
from PIL import Image
from django.core.files.base import ContentFile
import base64
from django.utils.crypto import get_random_string
import mimetypes
from fpdf import FPDF, HTMLMixin
import io
import decimal
from django.db.models.fields import NullBooleanField
from .myException import *
from .validations import *
from .utils import *
from .forms import *
from .models import *
from .models import Application_Settings as Academy_info
from .models import Shift_Info as Edu_Shift_Info
from finance.utils import *
from decimal import Context, Decimal
from django.core.files import File
# Create your views here.
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, request
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
from django.db.models import Count, Sum, Avg, Q, F,FloatField
import logging
import sys
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from threading import Thread
from PIL import Image
from django.db.models.functions import Cast
logger = logging.getLogger(__name__)
all_permissions = {}

def edu_choice_classlist(request):
    class_id = request.GET.get('class_id')
    list_data = Academic_Class.objects.filter().values(
        'class_id', 'class_name').order_by('class_name')
    return render(request, 'edu/edu-choice-classlist.html', {'list_data': list_data})


def edu_choice_classgrouplist(request):
    class_id = request.GET.get('class_id')
    list_data = Academic_Class_Group.objects.filter().values(
        'class_group_id', 'class_group_name').order_by('class_group_name')
    if class_id:
        list_data = list_data.filter(class_id=class_id)
    return render(request, 'edu/edu-choice-classgrouplist.html', {'list_data': list_data})


def edu_choice_sessionlist(request):
    class_id = request.GET.get('class_id')
    list_data = Academic_Class_Group.objects.filter().values(
        'session_id', 'session_name').order_by('session_name')
    if class_id:
        list_data = list_data.filter(class_id=class_id)
    return render(request, 'edu/edu-choice-sessionlist.html', {'list_data': list_data})


def edu_choice_feesheadlist(request):
    head_code = request.GET.get('head_code')
    list_data = Fees_Head_Settings.objects.filter(is_deleted=False).values(
        'head_code', 'head_name').order_by('head_name')
    return render(request, 'edu/edu-choice-feesheadlist.html', {'list_data': list_data})


def edu_choice_sectionlist(request):
    class_id = request.GET.get('class_id')
    list_data = Section_Info.objects.filter().values(
        'section_id', 'section_name').order_by('section_name')
    if class_id:
        list_data = list_data.filter(class_id=class_id)
    return render(request, 'edu/edu-choice-sectionlist.html', {'list_data': list_data})


def edu_choice_subjectlist(request):
    class_id = request.GET.get('class_id')
    class_group_id = request.GET.get('class_group_id')
    subject_id = request.GET.get('subject_id')
    subject_type_id = request.GET.get('subject_type_id')
    category_id = request.GET.get('category_id')
    list_data = Subject_List.objects.filter().values(
        'subject_id', 'subject_name').order_by('subject_name')
    if class_id:
        list_data = list_data.filter(class_id=class_id)
    if class_group_id:
        list_data = list_data.filter(class_group_id=class_group_id)
    if subject_type_id:
        list_data = list_data.filter(subject_type_id=subject_type_id)
    if category_id:
        list_data = list_data.filter(category_id=category_id)
    return render(request, 'edu/edu-choice-subjectlist.html', {'list_data': list_data})


def edu_choice_categorylist(request):
    category_id = request.GET.get('category_id')
    list_data = Subject_Category.objects.filter().values(
        'category_id', 'category_name').order_by('category_name')
    if category_id:
        list_data = list_data.filter(category_id=category_id)
    return render(request, 'edu/edu-choice-categorylist.html', {'list_data': list_data})


def temp_image_delete(app_user_id):
    time.sleep(3)
    img_temp = Image_temp.objects.filter(app_user_id=app_user_id).first()
    if img_temp:
        if img_temp.image_1 and os.path.exists(img_temp.image_1.path):
            os.remove(img_temp.image_1.path)
        if img_temp.image_2 and os.path.exists(img_temp.image_2.path):
            os.remove(img_temp.image_2.path)
        img_temp.delete()
    return


def login_view(request):
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)
    global all_permissions
    branch_code = ''

    try:

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            user_info = User.objects.get(username=username)
            all_permissions = user_info.get_all_permissions()

            request.session['user_full_name'] = user_info.first_name + \
                " "+user_info.last_name
            request.session['app_user_id'] = username
            app_setting = Global_Parameters.objects.get()
            request.session['application_title'] = app_setting.application_title
            return HttpResponseRedirect(reverse("appauth-home"))
        else:
            return render(request, "appauth/appauth-login.html", {"message": "Invalid credentials."})

    except Exception as e:
        print(str(e))
        return render(request, "appauth/appauth-login.html", {"message": "Invalid credentials."})


def logout_view(request):
    logout(request)
    return render(request, "appauth/appauth-login.html", {"message": "Logged out."})


class reset_password(TemplateView):
    template_name = 'appauth/appauth-reset-password.html'


def reset_user_password(request):

    new_password = request.POST.get('new_password', False)
    old_password = request.POST.get('password', False)
    user_name = request.POST.get('username', False)
    confirm_password = request.POST.get('new_password_confirm', False)

    if new_password != confirm_password:
        return render(request, "appauth/appauth-reset-password.html", {"message": "New password and confirm password does not match!"})

    user = authenticate(request, username=user_name, password=old_password)

    if user is not None:
        user = User.objects.get(username=user_name)
        user_info = User_Settings.objects.get(app_user_name=user_name)
        user_info.reset_user_password = False
        user.set_password(new_password)
        user.save()
        user_info.save()
        return render(request, "appauth/appauth-login.html", {"message": "Password Reset Successfully"})
    else:
        return render(request, "appauth/appauth-reset-password.html", {"message": "Invalid Credentials!"})


def DashboardView(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    context = get_global_data(request)
    data = dict()
    try:
        app_user_id = request.session["app_user_id"]
        #cbd = get_business_date(branch_code)
        #cursor = connection.cursor()
        #cursor.callproc("fn_fin_dashboard_data",[branch_code, somity_code, app_user_id, cbd])
        #row = cursor.fetchone()
    except Exception as e:
        data['form_is_valid'] = False
        logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))


class CreateUser(TemplateView):
    template_name = 'appauth/appauth-app-user.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = AppUserModelForm()
        context = get_global_data(request)
        context['success_message'] = ''
        context['error_message'] = ''
        context['form'] = form
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        context = get_global_data(request)
        form = AppUserModelForm(request.POST)
        error_message = "Please check the error"
        success_message = ""
        if form.is_valid():

            try:
                with transaction.atomic():
                    user_setting = Global_Parameters.objects.get()
                    user_name = form.cleaned_data["app_user_name"]
                    employee_name = form.cleaned_data["employee_name"]
                    user_password = 'Pass'+str(randint(1111, 9999))
                    user = User.objects.create_user(
                        user_name, '', user_password)
                    user.last_name = employee_name
                    user.save()

                    user_info = User.objects.get(username=user_name)
                    post = form.save(commit=False)
                    post.app_user_id = user_info.id
                    post.reset_user_password = True
                    post.cash_gl_code = user_setting.cash_gl_code

                    post.save()
                    success_message = "User Created Successfully! \nTemporary password for the User : "+user_password
                    error_message = ""
                    form = AppUserModelForm()
            except Exception as e:
                logger.error("Error in Creating User {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                context['form'] = form
                context['success_message'] = success_message
                context['error_message'] = 'Error '+str(e)+' in Creating User!'
                return render(request, self.template_name, context)
        else:
            error_message = form.errors.as_json()

        context['form'] = form
        context['success_message'] = success_message
        context['error_message'] = error_message
        return render(request, self.template_name, context)


class ApplicationUserList(TemplateView):
    template_name = 'appauth/appauth-application-users.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        forms = AppUserSearch()
        context = get_global_data(request)
        context['forms'] = forms
        return render(request, self.template_name, context)


@csrf_exempt
@transaction.atomic
def reset_appuser_password(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    data = dict()
    data['success_message'] = ''
    data['form_is_valid'] = False
    data['error_message'] = ''
    try:
        with transaction.atomic():
            user_info = User_Settings.objects.get(id=id)
            user = User.objects.get(username=user_info.app_user_name)
            user_info.reset_user_password = True
            new_password = 'Pass'+str(randint(1111, 9999))
            user.set_password(new_password)
            user.save()
            user_info.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Password Reset Successfylly\nNew temporary password for this user : '+new_password
    except Exception as e:
        data['form_is_valid'] = False
        data['error_message'] = str(e)
        logger.error("Error on line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        return JsonResponse(data)

    return JsonResponse(data)


# (((((((((((((((((((((((((((((((new page create)))))))))))))))))))))))))))))))


class edu_academicyear_createlist(TemplateView):
    template_name = 'edu/edu-academicyear-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = AcademicYearModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_academicyear_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = AcademicYearModelForm(request.POST)
        print(form, '/////')
        if form.is_valid():
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Academic Year Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_academicyear_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Academic_Year, academic_year=id)
    template_name = 'edu/edu-academicyear-edit.html'
    data = dict()

    if request.method == 'POST':
        form = AcademicYearModelForm(request.POST, instance=instance_data)
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
        form = AcademicYearModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


# (((((((((((((((((((((((((((Academic Class Informations)))))))))))))))))))))))))))

class edu_academicclass_createlist(TemplateView):
    template_name = 'edu/edu-academicclass-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = AcademicClassModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def edu_academicclass_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = AcademicClassModelForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    class_id = fn_get_class_id()
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.class_id = class_id
                    post.app_data_time = timezone.now()
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Academic Class Added Successfully!'
            except Exception as e:
                data['error_message'] = str(e)
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


@transaction.atomic
def edu_academicclass_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Academic_Class, class_id=id)
    template_name = 'edu/edu-academicclass-edit.html'
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = AcademicClassModelForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj = form.save(commit=False)
                    obj.save()
                    data['success_message'] = 'Updated Successfully!'
                    data['error_message'] = ''
                    data['form_is_valid'] = True
            except Exception as e:
                data['error_message'] = str(e)
        else:
            data['error_message'] = form.errors.as_json()
    else:
        form = AcademicClassModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


class edu_academicgroup_createlist(TemplateView):
    template_name = 'edu/edu-academicgroup-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = AcademicGroupModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_academicgroup_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    print(request.POST)
    if request.method == 'POST':
        form = AcademicGroupModelForm(request.POST)
        if form.is_valid():
            class_group_id = fn_get_class_group_id()
            post = form.save(commit=False)
            check = Academic_Class_Group.objects.filter(
                class_id=post.class_id.class_id, class_group_name=post.class_group_name).exists()
            if check:
                data['error_message'] = 'This Group name already exist'
                return JsonResponse(data)
            post.app_user_id = request.session["app_user_id"]
            post.app_data_time = timezone.now()
            post.class_group_id = class_group_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Academic Group Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_academicgroup_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Academic_Class_Group, class_group_id=id)
    template_name = 'edu/edu-academicgroup-edit.html'
    data = dict()

    if request.method == 'POST':
        form = AcademicGroupModelForm(request.POST, instance=instance_data)
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
        form = AcademicGroupModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


# ((((((((((((((((((((((((((((((Section Info Create))))))))))))))))))))))))))))


class edu_sectionInfo_createlist(TemplateView):
    template_name = 'edu/edu-sectioninfo-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = SectionInfoModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_sectionInfo_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = SectionInfoModelForm(request.POST)
        if form.is_valid():
            section_id = fn_get_section_id()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.section_id = section_id
            post.app_data_time = timezone.now()
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Section Info Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_sectionInfo_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    template_name = 'edu/edu-sectioninfo-edit.html'
    data = dict()
    context = get_global_data(request)
    if request.method == 'POST':
        instance_data = get_object_or_404(Section_Info, section_id=id)
        form = SectionInfoModelForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            data['success_message'] = 'Updated Successfully!'
            data['error_message'] = ''
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)

    instance_data = get_object_or_404(Section_Info, section_id=id)
    form = SectionInfoModelForm(instance=instance_data)
    context['form'] = form
    context['id'] = id
    context['class_start_time'] = str(instance_data.class_start_time)
    context['class_end_time'] = str(instance_data.class_end_time)
    return render(request, template_name, context)


# (((((((((((((((((((((((((((((((((((((((Session Create)))))))))))))))))))))))))))))))))))))))


class edu_session_createlist(TemplateView):
    template_name = 'edu/edu-session-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = SessionModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_session_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = SessionModelForm(request.POST)
        if form.is_valid():
            session_id = fn_get_session_id()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.session_id = session_id
            post.app_data_time = timezone.now()
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Session Info Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_session_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Session, pk=id)
    template_name = 'edu/edu-session-edit.html'
    data = dict()

    if request.method == 'POST':
        form = SessionModelForm(request.POST, instance=instance_data)
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
        form = SessionModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)

    # (((((((((((((((((((((((((((((((((((((((Subject Category Create)))))))))))))))))))))))))))))))))))))))


class edu_subcategory_createlist(TemplateView):
    template_name = 'edu/edu-subcategory-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = SubjectCategoryModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_subcategory_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = SubjectCategoryModelForm(request.POST)
        if form.is_valid():
            category_id = fn_get_subcategory_id()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.category_id = category_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Subject Category Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_subcategory_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Subject_Category, pk=id)
    template_name = 'edu/edu-subcategory-edit.html'
    data = dict()

    if request.method == 'POST':
        form = SubjectCategoryModelForm(request.POST, instance=instance_data)
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
        form = SubjectCategoryModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


# (((((((((((((((((((((((((((((((((((((((Category Info Create)))))))))))))))))))))))))))))))))))))))


class edu_category_createlist(TemplateView):
    template_name = 'edu/edu-category-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = CategoryModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_category_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = CategoryModelForm(request.POST)
        if form.is_valid():
            catagory_id = fn_get_category_id()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.catagory_id = catagory_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Category Info Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_category_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Catagory_info, pk=id)
    template_name = 'edu/edu-category-edit.html'
    data = dict()

    if request.method == 'POST':
        form = CategoryModelForm(request.POST, instance=instance_data)
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
        form = CategoryModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


# ((((((((((((((((((((((((((((((((((Subject Type create))))))))))))))))))))))))))))))))))

class edu_subtype_view(TemplateView):
    template_name = 'edu/edu-subjecttype-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = SubjectTypeModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_subtype_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = SubjectTypeModelForm(request.POST)
        if form.is_valid():
            subject_type_id = fn_get_subject_type_id()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.subject_type_id = subject_type_id
            post.app_data_time = timezone.now()
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Subject Type Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_subtype_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Subject_Type, subject_type_id=id)
    template_name = 'edu/edu-subjecttype-edit.html'
    data = dict()

    if request.method == 'POST':
        form = SubjectTypeModelForm(request.POST, instance=instance_data)
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
        form = SubjectTypeModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


# (((((((((((((((((((((((((((((((((Subject List Create)))))))))))))))))))))))))))))))))

class edu_sublist_createlist(TemplateView):
    template_name = 'edu/edu-sublist-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = SubjectListModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_sublist_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = SubjectListModelForm(request.POST)
        check_data = dict()
        if form.is_valid():
            subject_id = fn_get_subject_id()
            post = form.save(commit=False)
            check_data['class_id'] = post.class_id.class_id
            check_data['subject_name'] = post.subject_name
            if post.class_group_id:
                check_data['class_group_id'] = post.class_group_id.class_group_id
            else:
                check_data['class_group_id'] = None
            check = Subject_List.objects.filter(**check_data).exists()
            if check:
                data['error_message'] = 'This subject already exist.'
                return JsonResponse(data)
            post.app_user_id = request.session["app_user_id"]
            post.app_data_time = datetime.now()
            post.subject_id = subject_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Subject List Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_sublist_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Subject_List, subject_id=id)
    template_name = 'edu/edu-sublist-edit.html'
    data = dict()
    check_data = dict()
    if request.method == 'POST':
        form = SubjectListModelForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            check_data['class_id'] = obj.class_id.class_id
            check_data['subject_name'] = obj.subject_name
            if obj.class_group_id:
                check_data['class_group_id'] = obj.class_group_id.class_group_id
            else:
                check_data['class_group_id'] = None
            check = Subject_List.objects.filter(
                ~Q(subject_id=id), **check_data).exists()
            if check:
                data['error_message'] = 'This subject already exist.'
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
        form = SubjectListModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        context['instance_data'] = instance_data
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


# ((((((((((((((((((((((((((((Department Info Create))))))))))))))))))))))))))))


class edu_department_createlist(TemplateView):
    template_name = 'edu/edu-department-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = DepartmentInfoModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_department_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = DepartmentInfoModelForm(request.POST)
        if form.is_valid():
            department_id = fn_get_department_id()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.department_id = department_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Department Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_department_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Department_Info, department_id=id)
    template_name = 'edu/edu-department-edit.html'
    data = dict()

    if request.method == 'POST':
        form = DepartmentInfoModelForm(request.POST, instance=instance_data)
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
        form = DepartmentInfoModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)

# (((((((((((((((((((((((((((((((((((((((Shift Info create)))))))))))))))))))))))))))))))))))))))


class edu_shift_createlist(TemplateView):
    template_name = 'edu/edu-shift-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = ShiftInfoModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_shift_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = ShiftInfoModelForm(request.POST)
        if form.is_valid():
            shift_id = fn_get_shift_id()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.shift_id = shift_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Shift Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_shift_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Edu_Shift_Info, shift_id=id)
    template_name = 'edu/edu-shift-edit.html'
    data = dict()

    if request.method == 'POST':
        form = ShiftInfoModelForm(request.POST, instance=instance_data)
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
        form = ShiftInfoModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        context['shift_start_time'] = instance_data.shift_start_time
        context['shift_end_time'] = instance_data.shift_end_time
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


# (((((((((((((((((((((((((((((Degree Info Create)))))))))))))))))))))))))))))

class edu_degree_createlist(TemplateView):
    template_name = 'edu/edu-degree-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = DegreeInfoModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_degree_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = DegreeInfoModelForm(request.POST)
        if form.is_valid():
            degree_id = fn_get_degree_id()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.degree_id = degree_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Degree Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_degree_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Degree_Info, degree_id=id)
    template_name = 'edu/edu-degree-edit.html'
    data = dict()

    if request.method == 'POST':
        form = DegreeInfoModelForm(request.POST, instance=instance_data)
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
        form = DegreeInfoModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


# (((((((((((((((((((((((((((((((Occupation Info Create)))))))))))))))))))))))))))))))


class edu_occupation_createlist(TemplateView):
    template_name = 'edu/edu-occupation-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = OccupationInfoModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_occupation_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = OccupationInfoModelForm(request.POST)
        if form.is_valid():
            occupation_id = fn_get_occupation_id()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.occupation_id = occupation_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Occupation Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_occupation_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Occupation_Info, occupation_id=id)
    template_name = 'edu/edu-occupation-edit.html'
    data = dict()

    if request.method == 'POST':
        form = OccupationInfoModelForm(request.POST, instance=instance_data)
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
        form = OccupationInfoModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


# (((((((((((((((((((((((((((((Educations Institute Create)))))))))))))))))))))))))))))

class edu_education_createlist(TemplateView):
    template_name = 'edu/edu-education-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = EducationInstituteModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_education_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = EducationInstituteModelForm(request.POST)
        if form.is_valid():
            institute_id = fn_get_institute_id()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.institute_id = institute_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Education Institute Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_education_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Education_Institute, institute_id=id)
    template_name = 'edu/edu-education-edit.html'
    data = dict()

    if request.method == 'POST':
        form = EducationInstituteModelForm(
            request.POST, instance=instance_data)
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
        form = EducationInstituteModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


# ((((((((((((((((((((((((((((((((Student Information))))))))))))))))))))))))))))))))

class edu_studentinfo_createlist(TemplateView):
    template_name = 'edu/edu-studentinfo-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        context = get_global_data(request)
        visited_id = self.request.GET.get('visited', None)
        if visited_id:
            instance_data = get_object_or_404(
                Visited_Student_Info, pk=visited_id)
            form = StudentInfoModelForm(instance=instance_data)
            educations = json.loads(instance_data.education_qualifications)
            all_degree = Degree_Info.objects.all()
            all_institut = Education_Institute.objects.all()
            context['educations'] = educations
            context['all_degree'] = all_degree
            context['all_institut'] = all_institut
        else:
            app_user_id = request.session["app_user_id"]
            branch_code = request.session["branch_code"]
            # cbd = get_business_date(branch_code, app_user_id)
            # form = StudentInfoModelForm(initial={'student_joining_date': cbd})
            form = StudentInfoModelForm()
        app_user_id = request.session["app_user_id"]
        image_data = Image_temp.objects.filter(app_user_id=app_user_id).first()
        image_form = ImageTempModelForm()
        context['form'] = form
        context['image_form'] = image_form
        context['image_data'] = image_data
        return render(request, self.template_name, context)


@transaction.atomic
def edu_studentinfo_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    proc_data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = StudentInfoModelForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    branch_code = request.POST.get('branch_code')
                    addmission_date = request.POST.get('student_joining_date')
                    app_user_id = request.session["app_user_id"]
                    post = form.save(commit=False)
                    if post.student_joining_date:
                        if off_future_date(post.student_joining_date):
                            data['error_message'] = 'Please select correct date'
                            return JsonResponse(data)
                    if post.student_date_of_birth:
                        if off_future_date(post.student_date_of_birth):
                            data['error_message'] = 'Please select correct date'
                            return JsonResponse(data)
                    if len(addmission_date[:4]) == 4:
                        student_roll = fn_gen_student_id(
                            addmission_date[:4], branch_code, request.POST.get('class_id'))
                    else:
                        data['error_message'] = 'Enter Admission Date'
                        return JsonResponse(data)

                    status, error_message = fn_open_account_transaction_screen(p_transaction_screen='STUDENT_ADMISSION', p_branch_code=post.branch_code,
                                                                               p_app_user_id=app_user_id, p_client_id=student_roll, p_client_name=post.student_name,
                                                                               p_client_address=post.student_present_address, p_phone_number=post.student_phone,
                                                                               p_cbd=post.student_joining_date, p_limit_amount=0.00)
                    if not status:
                        data['error_message'] = error_message
                        raise Exception(error_message)

                    account_type, client_type = fn_get_transaction_account_type(
                        p_transaction_screen='STUDENT_ADMISSION')

                    account_number, _, _, _ = fn_get_account_info_byactype(
                        p_client_id=student_roll, p_account_type=account_type)

                    post.student_roll = student_roll
                    post.app_user_id = app_user_id
                    post.app_data_time = timezone.now()
                    post.account_number = account_number
                    post.save()
                    student = Students_Info.objects.get(
                        student_roll=student_roll)

                    img_temp = Image_temp.objects.filter(
                        app_user_id=app_user_id).first()
                    if img_temp:
                        if img_temp.image_1:
                            picture_copy = ContentFile(img_temp.image_1.read())
                            new_picture_name = img_temp.image_1.name.split(
                                "/")[-1]
                            student.profile_image.save(
                                new_picture_name, picture_copy, save=True)

                        if img_temp.image_2:
                            sign_copy = ContentFile(img_temp.image_2.read())
                            sign_name = img_temp.image_2.name.split("/")[-1]
                            student.student_signature.save(
                                sign_name, sign_copy, save=True)

                    edu_count = int(request.POST.get('edu_count'))
                    for i in range(1, edu_count+1):

                        student = Students_Info.objects.get(
                            student_roll=student_roll)
                        edu_count = int(request.POST.get('edu_count'))
                        for i in range(1, edu_count+1):
                            if request.POST.get('degree'+str(i)):
                                edu = Education_Qualification()
                                edu.student_roll = student
                                edu.degree_name = Degree_Info.objects.get(
                                    degree_id=request.POST.get('degree'+str(i)))
                                edu.board_name = request.POST.get(
                                    'board'+str(i))
                                edu.result_point = request.POST.get(
                                    'point'+str(i))
                                edu.result_grate = request.POST.get(
                                    'grate'+str(i))
                                edu.passing_year = request.POST.get(
                                    'year'+str(i))
                                edu.institute_id = Education_Institute.objects.get(
                                    institute_id=request.POST.get('institute'+str(i)))
                                edu.app_user_id = app_user_id
                                edu.save()
                    if(not request.POST.get('father_address')):
                        student.father_address = student.student_permanent_address
                    if(not request.POST.get('mother_address')):
                        student.mother_address = student.student_permanent_address

                    if(request.POST.get('legal_guardians') == 'Father'):
                        student.legal_guardian_name = student.student_father_name
                        student.legal_guardian_contact = student.father_phone_number
                        student.legal_guardian_relation = 'Father'
                        student.legal_guardian_nid = student.father_nid
                        student.legal_guardian_occupation_id = student.father_occupation_id
                        student.legal_guardian_address = student.father_address

                    if(request.POST.get('legal_guardians') == 'Mother'):
                        student.legal_guardian_name = student.student_mother_name
                        student.legal_guardian_contact = student.mother_phone_number
                        student.legal_guardian_relation = 'Mother'
                        student.legal_guardian_nid = student.mother_nid
                        student.legal_guardian_occupation_id = student.mother_occupation_id
                        student.legal_guardian_address = student.mother_address
                    student.save()

                    proc_data["class_id"] = request.POST.get('class_id')
                    proc_data["branch_code"] = branch_code
                    process_id = fn_get_fees_processing_id(branch_code)
                    proc_data["process_id"] = process_id
                    proc_data["academic_year"] = post.academic_year.academic_year
                    if student.class_group_id:
                        proc_data["class_group_id"] = student.class_group_id.class_group_id
                    else:
                        proc_data["class_group_id"] = None
                    if student.section_id:
                        proc_data["section_id"] = student.section_id
                    else:
                        proc_data["section_id"] = None

                    proc_data["student_roll"] = student_roll

                    proc_data["process_date"] = addmission_date
                    proc_data["app_user_id"] = app_user_id
                    print(proc_data)

                    status, error_message = fn_fees_processing_thread(
                        proc_data)

                    data['form_is_valid'] = True
                    data['success_message'] = 'Student Information Added Successfully!'
            except Exception as e:
                logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                data['error_message'] = str(e)
                return JsonResponse(data)
        else:
            data['error_message'] = form.errors.as_json()
    thread = threading.Thread(target=temp_image_delete, args=[
        request.session["app_user_id"]])
    thread.start()
    return JsonResponse(data)


# (((((((((((((((((((((((((((((((((((Student Admission)))))))))))))))))))))))))))))))))))

class edu_admission_createlist(TemplateView):
    template_name = 'edu/edu-admission-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = StudentAdmissionModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)

@transaction.atomic
def edu_admission_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        try:
            with transaction.atomic():
                form = StudentAdmissionModelForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Student Admission Successfully!'
                else:
                    data['error_message'] = form.errors.as_json()
        except Exception as e:
                logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                data['error_message'] = str(e)
                return JsonResponse(data)
    return JsonResponse(data)


def edu_admission_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Student_Admission, student_roll=id)
    template_name = 'edu/edu-admission-edit.html'
    data = dict()

    if request.method == 'POST':
        form = StudentAdmissionModelForm(request.POST, instance=instance_data)
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
        form = StudentAdmissionModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)

# (((((((((((((((((((((((((((((((((((Result Grade)))))))))))))))))))))))))))))))))))


class edu_resultgrade_createlist(TemplateView):
    template_name = 'edu/edu-resultgrade-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = ResultGradeModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_resultgrade_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = ResultGradeModelForm(request.POST)
        if form.is_valid():
            grade_id = fn_get_result_id()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.grade_id = grade_id
            post.app_data_time = timezone.now()
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Result Grade Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_resultgrade_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Result_Grade, grade_id=id)
    template_name = 'edu/edu-resultgrade-edit.html'
    data = dict()

    if request.method == 'POST':
        form = ResultGradeModelForm(request.POST, instance=instance_data)
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
        form = ResultGradeModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


# (((((((((((((((((((((((((((((Exam Type Create)))))))))))))))))))))))))))))

class edu_examtype_createlist(TemplateView):
    template_name = 'edu/edu-examtype-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = ExamTypeModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_examtype_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = ExamTypeModelForm(request.POST)
        if form.is_valid():
            examtype_id = fn_get_examtype_id()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.examtype_id = examtype_id
            post.app_data_time = timezone.now()
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Exam Type Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_examtype_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Exam_Type, examtype_id=id)
    template_name = 'edu/edu-examtype-edit.html'
    data = dict()

    if request.method == 'POST':
        form = ExamTypeModelForm(request.POST, instance=instance_data)
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
        form = ExamTypeModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


# (((((((((((((((((((((Exam Term Create)))))))))))))))))))))

class edu_examterm_createlist(TemplateView):
    template_name = 'edu/edu-examterm-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = ExamTermModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_examterm_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = ExamTermModelForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.app_data_time = timezone.now()
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Exam Term Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_examterm_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Exam_Term, id=id)
    template_name = 'edu/edu-examterm-edit.html'
    data = dict()

    if request.method == 'POST':
        form = ExamTermModelForm(request.POST, instance=instance_data)
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
        form = ExamTermModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


# (((((((((((((((((((((((((((((Exam Setup Create)))))))))))))))))))))))))))))

class edu_examsetup_createlist(TemplateView):
    template_name = 'edu/edu-examsetup-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = ExamSetupModelForm()
        subjects = Subject_List.objects.all()
        context = get_global_data(request)
        context['form'] = form
        context['subjects'] = subjects
        return render(request, self.template_name, context)


def edu_examsetup_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    if request.method == 'POST':
        form = ExamSetupModelForm(request.POST)
        if form.is_valid():
            for sub in request.POST.getlist('subject_ids[]'):
                check = Exam_Setup.objects.filter(branch_code=request.POST.get(
                    'branch_code'),academic_year=request.POST.get('academic_year'), subject_id=sub, exam_name=request.POST.get('exam_name'), term_id=request.POST.get('term_id')).exists()
                if check:
                    data['error_message'] = "This exam is already exist."
                    return JsonResponse(data)
                post = form.save(commit=False)
                post.exam_id = fn_get_examsetup_id()
                post.subject_id = get_object_or_404(
                    Subject_List, subject_id=sub)
                post.app_user_id = request.session["app_user_id"]
                post.app_data_time = timezone.now()
                post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Exam Setup Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_examsetup_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Exam_Setup, exam_id=id)
    template_name = 'edu/edu-examsetup-edit.html'
    data = dict()

    if request.method == 'POST':
        form = ExamSetupModelForm(request.POST, instance=instance_data)
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
        form = ExamSetupModelForm(instance=instance_data)
        class_groups = Academic_Class_Group.objects.filter(
            class_id=instance_data.class_id.class_id)
        sub_filter=dict()
        if instance_data.class_id:
            sub_filter['class_id']=instance_data.class_id
        if instance_data.class_group_id:
            sub_filter['class_group_id']=instance_data.class_group_id.class_group_id
        subjects = Subject_List.objects.filter(**sub_filter)
        context = get_global_data(request)

        context['subjects'] = subjects
        context['exam_mark'] = instance_data
        context['form'] = form
        context['id'] = id
        context['subjects'] = subjects
        context['branch_code'] = instance_data.branch_code
        context['exam'] = instance_data
        context['class_groups'] = class_groups
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


# (((((((((((((((((((((((((((((Exam Marks Entry)))))))))))))))))))))))))))))


class edu_marksdetails_filterlist(TemplateView):
    template_name = 'edu/edu-exam-marks-entry.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = StudentInfoModelForm()
        subjects = Subject_List.objects.all()
        grad_table = Result_Grade.objects.values(
            'out_of').annotate(Count("out_of"))
        context = get_global_data(request)
        context['form'] = form
        context['grade'] = grad_table
        context['subjects'] = subjects
        return render(request, self.template_name, context)


def edu_marksdetails_filtertable(request):
    template_name = 'edu/edu-markdetails-filtertable.html'
    context = dict()
    if request.method == 'POST':
        academic_year = request.POST.get('academic_year')
        class_id = request.POST.get('class_id')
        class_group_id = request.POST.get('class_group_id')
        subject_id = request.POST.get('subject_id')
        branch_code = request.POST.get('branch_code')
        session_id = request.POST.get('session_id')

        filter_data = dict()
        if branch_code:
            filter_data['branch_code'] = branch_code
        if academic_year:
            filter_data['academic_year'] = academic_year
        if session_id:
            filter_data['session_id'] = session_id
        if class_id:
            filter_data['class_id'] = class_id
        if class_group_id:
            filter_data['class_group_id'] = class_group_id
        if subject_id:
            filter_data['subject_id'] = subject_id

        students = Subject_Choice.objects.filter(
            **filter_data).filter(student_roll__student_status='A').order_by('student_roll__class_roll')
        context['students_rolls'] = fn_student_rolls(students)
        context['students'] = students
        return render(request, template_name, context)

    return render(request, template_name, context)

@transaction.atomic
def edu_studentmark_insert(request):
    data = {}
    if request.method == 'POST':
        try:
            with transaction.atomic():
                exam_id = Exam_Setup.objects.get(exam_id=request.POST.get('exam_id'))
                branch_code = request.POST.get('branch_code')
                session_id = request.POST.get('session_id')
                exam_no = request.POST.get('exam_no')
                class_id=request.POST.get('class_id')
                class_group_id=request.POST.get('class_group_id')
                academic_year=request.POST.get('academic_year')

                total_exam_marks = request.POST.get('total_exam_marks')
                obtain_marks = request.POST.get('obtain_marks')
                student_roll = Students_Info.objects.get(
                    student_roll=request.POST.get('student_roll'))
                if(float(obtain_marks) > float(total_exam_marks)):
                    data['error_message'] = "obtain-marks is larger fixed-total-marks"
                    return JsonResponse(data)
                mark_percent = (float(obtain_marks)/float(total_exam_marks))*100
                result_grade = Result_Grade.objects.filter(
                    lowest_mark__lte=mark_percent, highest_mark__gte=mark_percent, out_of=exam_id.class_id.out_of)


                dataFilter=dict()
                if branch_code:
                    dataFilter['branch_code']=branch_code
                if academic_year:
                    dataFilter['academic_year']=academic_year
                if session_id:
                    dataFilter['session_id']=session_id
                if student_roll:
                    dataFilter['student_roll']=student_roll.student_roll
                if class_id:
                    dataFilter['class_id']=class_id
                if class_group_id:
                    dataFilter['class_group_id']=class_group_id
                if request.POST.get('subject_id'):
                    dataFilter['subject_id']=request.POST.get('subject_id')
                if request.POST.get('exam_id'):
                    dataFilter['exam_id']=request.POST.get('exam_id')
                if exam_no:
                    dataFilter['exam_no']=exam_no

                if Exam_Marks_Details.objects.filter(**dataFilter).exists():
                    exam_marks = Exam_Marks_Details.objects.get(**dataFilter)
                    exam_marks.obtain_marks = obtain_marks
                    exam_marks.result_grade = result_grade[0].grade_name
                    exam_marks.grade_point_average = result_grade[0].result_gpa
                    exam_marks.app_user_id = request.session["app_user_id"]
                    exam_marks.save()
                else:
                    exam_marks = Exam_Marks_Details()
                    exam_marks.branch_code=int(branch_code)
                    if session_id:
                        exam_marks.session_id=exam_id.session_id
                    exam_marks.class_id = exam_id.class_id
                    exam_marks.class_group_id = student_roll.class_group_id
                    exam_marks.academic_year = exam_id.academic_year
                    exam_marks.term_id = exam_id.term_id
                    exam_marks.student_roll = student_roll
                    exam_marks.subject_id = exam_id.subject_id
                    exam_marks.exam_id = exam_id
                    exam_marks.exam_no = exam_no
                    exam_marks.total_exam_marks = total_exam_marks
                    exam_marks.obtain_marks = obtain_marks
                    exam_marks.result_grade = result_grade[0].grade_name
                    exam_marks.grade_point_average = result_grade[0].result_gpa
                    exam_marks.app_user_id = request.session["app_user_id"]
                    exam_marks.save()
                if student_roll.class_group_id:
                    class_group = student_roll.class_group_id.class_group_id
                else:
                    class_group = student_roll.class_group_id
                cursor = connection.cursor()
                cursor.callproc("fn_set_single_exam_mark", [
                    exam_id.academic_year.academic_year, int(branch_code), request.POST.get('class_id'), class_group, request.POST.get('student_roll'), request.POST.get('subject_id'), request.POST.get('exam_id'), exam_id.class_id.out_of, request.session["app_user_id"]])
                data['exam_result'] = cursor.fetchone()
                data['exam'] = {'no_of_exam': exam_id.no_of_exam,
                                'cal_condition': exam_id.cal_condition}
                data['result_grade'] = str(exam_marks.result_grade)
                # data['result_grade']={'result_grade':exam_marks.result_grade}
                data['grade_point'] = str(exam_marks.grade_point_average)
        except Exception as e:
                logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                data['error_message'] = str(e)
                return JsonResponse(data)
    return JsonResponse(data)

# ((((((((((((((((((get gpa grade function))))))))))))))))))


def edu_get_single_exam_mark(request):
    data = {}
    exam_id = request.GET.get('exam_id')
    student_roll = request.GET.get('student_roll')
    subject_id = request.GET.get('subject_id')
    mark = Exam_Single_Mark.objects.filter(
        exam_id=exam_id, student_roll=student_roll, subject_id=subject_id)
    if mark:
        mark_data = Exam_Single_Mark.objects.get(
            exam_id=exam_id, student_roll=student_roll, subject_id=subject_id)
        data['mark'] = {
            'total_exam_marks': mark_data.total_exam_marks,
            'obtain_marks': mark_data.obtain_marks,
            'result_grade': mark_data.result_grade,
            'grade_point': mark_data.grade_point_average}
    return JsonResponse(data)


def edu_get_single_subject_exam_mark(request):
    data = {}
    academic_year = request.GET.get('academic_year', None)
    term_id = request.GET.get('term_id', None)
    class_id = request.GET.get('class_id', None)
    subject_id = request.GET.get('subject_id', None)
    student_roll = request.GET.get('student_roll', None)
    app_user_id = request.session["app_user_id"]
    class_info = get_object_or_404(Academic_Class, class_id=class_id)
    result = get_student_subject_mark(
        academic_year, term_id, class_id, student_roll, subject_id, class_info.out_of, app_user_id)
    data['result'] = result
    return JsonResponse(data)


@transaction.atomic
def edu_result_view_setting(request):
    if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
    data=dict()
    if request.method == 'POST':
        try:
            with transaction.atomic():
                branch_code= request.POST.get('branch_code')
                academic_year = request.POST.get('academic_year')
                session_id= request.POST.get('session_id')
                class_id= request.POST.get('class_id')
                class_group_id= request.POST.get('class_group_id')
                term_id= request.POST.get('term_id')
                short_number= request.POST.get('short_number')
                subject_one_id= request.POST.get('subject_one_id')
                subject_two_id= request.POST.get('subject_two_id')
                subject_three_id= request.POST.get('subject_three_id')
                dataFilter=dict()
                dataFilter['branch_code'] = branch_code
                dataFilter['academic_year'] = academic_year
                dataFilter['class_id'] = class_id
                dataFilter['term_id'] = term_id
                dataFilter['short_number'] = short_number
                dataFilter['subject_one_id'] = subject_one_id
                if session_id:
                    dataFilter['session_id']=session_id
                if class_group_id:
                    dataFilter['class_group_id']=class_group_id
                if subject_two_id:
                    dataFilter['subject_two_id']=subject_two_id
                if subject_three_id:
                    dataFilter['subject_three_id']=subject_three_id

                if not result_view_setting.objects.filter(**dataFilter).exists():
                    form = ResultViewSettingForm(request.POST)
                    obj = form.save(commit=False)
                    obj.result_view_id=fn_result_view_id()
                    obj.app_user_id=request.session["app_user_id"]
                    obj.app_data_time=timezone.now()
                    obj.save()
                    data['success_message'] = 'Create Successfully!'
                    data['error_message'] = ''
                    data['form_is_valid'] = True
                    return JsonResponse(data)

        except Exception as e:
                logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                data['error_message'] = str(e)
                return JsonResponse(data)
    else:
        template_name = 'edu/edu-result-view-setting.html'
        form = ResultViewSettingForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, template_name, context)
        
    return JsonResponse(data)
    
@transaction.atomic
def edu_result_view_setting_delete(request):
    if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
    data=dict()
    if request.method == 'POST':
        try:
            with transaction.atomic():
                id=request.POST.get('id')
                if subject_mark_with_marge.objects.filter(result_view_id=id).exists():
                    subject_mark_with_marge.objects.filter(result_view_id=id).delete()
                if result_view_setting.objects.filter(result_view_id=id).exists():
                    result_view_setting.objects.filter(result_view_id=id).delete()
                data['success_message'] = 'Delete Successfully!'
                data['error_message'] = ''
                data['form_is_valid'] = True
                return JsonResponse(data)

        except Exception as e:
                logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                data['error_message'] = str(e)
                return JsonResponse(data)

    return JsonResponse(data)
#Threding
@transaction.atomic
class Result_Process_Thread(Thread):
    def run(self):
        try:
            with transaction.atomic():
                self.data['app_user_id']
                branch_code=self.data['branch_code']
                academic_year=self.data['academic_year']
                class_id=self.data['class_id']
                term_id=self.data['term_id']
                if self.data['class_group_id']:
                    class_group_id=self.data['class_group_id']
                else:
                    class_group_id=None
                if self.data['session_id']:
                    session_id=self.data['session_id']
                else:
                    session_id=None

                cursor = connection.cursor()
                cursor.callproc("fn_edu_result_processing_final",
                [int(branch_code),
                int(academic_year),
                class_id,
                class_group_id,
                session_id,
                term_id,
                None,
                date.today(),
                self.data['app_user_id']
                    ])
                status = cursor.fetchone()
                
                if status[0] == 'S':
                    process=Process_Status_History.objects.filter(process_id=self.process_id).first()
                    process.status='Finish'
                    process.save()
                
        except Exception as e:
            print(e)
            process = Process_Status_History.objects.filter(process_id=self.process_id).first()
            process.status = 'Fail'
            process.save()
            

    
@transaction.atomic
def edu_edu_result_process(request):
    if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
    data=dict()
    if request.method == 'POST':
        try:
            with transaction.atomic():
                branch_code= request.POST.get('branch_code')
                academic_year= request.POST.get('academic_year')
                session_id= request.POST.get('session_id')
                class_id= request.POST.get('class_id')
                class_group_id= request.POST.get('class_group_id')
                term_id= request.POST.get('term_id')
    
                if not class_group_id:
                    class_group_id=None
    
                if not session_id:
                    session_id=None
                dataFilter={
                    'branch_code':branch_code,
                    'academic_year':academic_year,
                    'session_id':session_id,
                    'class_id':class_id,
                    'class_group_id':class_group_id,
                    'term_id':term_id,
                    'app_user_id':request.session["app_user_id"]
                }
                process_id =request.POST.get('process_id')
                t1=Result_Process_Thread()
                t1.data=dataFilter
                t1.process_id=process_id
                t1.start()
    
                data['success_message'] = 'Result process started. \n Please wait few minutes. '
                data['error_message'] = ''
                data['form_is_valid'] = True
                print('Complete')
                return JsonResponse(data)
        except Exception as e:
                logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                data['error_message'] = str(e)
                print(str(e))
                return JsonResponse(data)
    else:
        template_name = 'edu/edu-result-process.html'
        form = ResultViewSettingForm()
        process_status=Process_Status_History.objects.filter(process_name='Result Process').order_by('-app_data_time')[:10]
        context = get_global_data(request)
        context['form'] = form
        context['process_status'] = process_status
        return render(request, template_name, context)

    return JsonResponse(data)
    
@transaction.atomic
def edu_edu_result_process_status_create(request):
    if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
    data=dict()
    if request.method == 'POST':
        try:
            with transaction.atomic():
                time_now=timezone.now()
                check=Process_Status_History.objects.filter(process_name='Result Process',
                                                            status='Start',
                                                            start_data_time__gte=time_now-timedelta(minutes=10)).exists()
                if check:
                    data['error_message']='Another result process is running.'
                else:
                    process_id = fn_result_process_id()
                    process = Process_Status_History()
                    process.process_id = process_id
                    process.process_name = 'Result Process'
                    process.status = 'Start'
                    process.start_data_time = time_now
                    process.app_user_id = request.session["app_user_id"]
                    process.save()
                    data['process_id']=process_id
                return JsonResponse(data)
        except Exception as e:
                logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                data['error_message'] = str(e)
                print(str(e))
                return JsonResponse(data)
    else:
        template_name = 'edu/edu-result-process.html'
        form = ResultViewSettingForm()
        process_status=Process_Status_History.objects.all()
        context = get_global_data(request)
        context['form'] = form
        context['process_status'] = process_status
        return render(request, template_name, context)

    return JsonResponse(data)

@transaction.atomic
def edu_result_view_template1(request):
    if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
    data=dict()
    if request.method == 'POST':
        try:
            with transaction.atomic():
                data['success_message'] = 'Create Successfully!'
                data['error_message'] = ''
                data['form_is_valid'] = True
                return JsonResponse(data)

        except Exception as e:
                logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                data['error_message'] = str(e)
                return JsonResponse(data)
    else:
        template_name = 'edu/edu-result-view-template1.html'
        branch_code = request.GET.get('branch_code')
        academic_year = request.GET.get('academic_year')
        session_id = request.GET.get('session_id')
        class_id = request.GET.get('class_id')
        class_group_id = request.GET.get('class_group_id')
        term_id = request.GET.get('term_id')

        dataFilter = dict()
        dataFilter['branch_code'] = branch_code
        dataFilter['academic_year'] = academic_year
        dataFilter['class_id'] = class_id
        dataFilter['term_id'] = term_id

        if session_id:
            dataFilter['session_id'] = session_id
        if class_group_id:
            dataFilter['class_group_id'] = class_group_id
        formHeader=Admission_form_header.objects.filter(branch_code=branch_code).first()
        result_info=Exam_Marks_Final.objects.filter(**dataFilter).first()

        context = get_global_data(request)
        context['formHeader'] = formHeader
        context['result_info'] = result_info
        return render(request, template_name, context)

    return JsonResponse(data)

@transaction.atomic
def edu_result_summary(request):
    if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
    data=dict()
    if request.method == 'POST':
        try:
            with transaction.atomic():
                data['success_message'] = 'Create Successfully!'
                data['error_message'] = ''
                data['form_is_valid'] = True
                return JsonResponse(data)

        except Exception as e:
                logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                data['error_message'] = str(e)
                return JsonResponse(data)
    else:
        template_name = 'edu/edu-result-summary.html'
        branch_code = request.GET.get('branch_code')
        academic_year = request.GET.get('academic_year')
        session_id = request.GET.get('session_id')
        class_id = request.GET.get('class_id')
        class_group_id = request.GET.get('class_group_id')
        term_id = request.GET.get('term_id')

        dataFilter = dict()
        dataFilter['branch_code'] = branch_code
        dataFilter['academic_year'] = academic_year
        dataFilter['class_id'] = class_id
        dataFilter['term_id'] = term_id

        if session_id:
            dataFilter['session_id'] = session_id
        if class_group_id:
            dataFilter['class_group_id'] = class_group_id
        formHeader=Admission_form_header.objects.filter(branch_code=branch_code).first()
        result_info=Exam_Marks_Final.objects.filter(**dataFilter).first()

        context = get_global_data(request)
        context['formHeader'] = formHeader
        context['result_info'] = result_info
        return render(request, template_name, context)


@transaction.atomic
def edu_result_summary_data(request):
    if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
    data=dict()
    if request.method == 'POST':
        try:
            with transaction.atomic():
                branch_code = request.POST.get('branch_code')
                academic_year = request.POST.get('academic_year')
                session_id = request.POST.get('session_id')
                class_id = request.POST.get('class_id')
                class_group_id = request.POST.get('class_group_id')
                term_id = request.POST.get('term_id')

                dataFilter = dict()
                dataFilter['branch_code'] = branch_code
                dataFilter['academic_year'] = academic_year
                dataFilter['class_id'] = class_id
                dataFilter['term_id'] = term_id
                class_info=get_object_or_404(Academic_Class, class_id=class_id)
                
                if session_id:
                    dataFilter['session_id'] = session_id
                if class_group_id:
                    dataFilter['class_group_id'] = class_group_id

                final_result=Exam_Marks_Final.objects.values(
                    'student_roll',
                    'total_exam_marks',
                    'obtain_marks',
                    'result_grade',
                    'grade_point_average',
                    'merit_position',
                    'point_without_optional',
                    student_name=F('student_roll__student_name'),
                    gander=F('student_roll__student_gender'),
                    class_name=F('class_id__class_name'),
                    class_group=F('class_group_id__class_group_name'),
                    year=F('academic_year'),
                    session=F('session_id__session_name'),
                    term=F('term_id__term_name')
                ).filter(**dataFilter).order_by('-grade_point_average','-obtain_marks','merit_position')
                
                form_header=Admission_form_header.objects.filter(branch_code=branch_code)
                logo=''
                for header in form_header:
                    if header.logo:
                        logo=header.logo.url
                
                data['results']=list(final_result)
                data['form_header']=list(form_header.values())[0]
                data['logo']=logo
                result_grade=Result_Grade.objects.filter(out_of=class_info.out_of)
                data['result_grades']=list(result_grade.values())

        except Exception as e:
                logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                data['error_message'] = str(e)
                return JsonResponse(data)
    return JsonResponse(data)


@transaction.atomic
def edu_result_mark_sheet_data(request):
    if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
    data=dict()
    if request.method == 'POST':
        try:
            with transaction.atomic():
                branch_code = request.POST.get('branch_code')
                academic_year = request.POST.get('academic_year')
                session_id = request.POST.get('session_id')
                class_id = request.POST.get('class_id')
                class_group_id = request.POST.get('class_group_id')
                term_id = request.POST.get('term_id')

                dataFilter = dict()
                dataFilter['branch_code'] = branch_code
                dataFilter['academic_year'] = academic_year
                dataFilter['class_id'] = class_id
                dataFilter['term_id'] = term_id

                if session_id:
                    dataFilter['session_id'] = session_id
                if class_group_id:
                    dataFilter['class_group_id'] = class_group_id

                final_result=Exam_Marks_Final.objects.values(
                    'student_roll',
                    'total_exam_marks',
                    'obtain_marks',
                    'result_grade',
                    'grade_point_average',
                    'merit_position',
                    'point_without_optional',
                    student_name=F('student_roll__student_name'),
                    father_name=F('student_roll__student_father_name'),
                    mother_name=F('student_roll__student_mother_name'),
                    class_roll=F('student_roll__class_roll'),
                    date_of_birth=F('student_roll__student_date_of_birth'),
                    class_name=F('class_id__class_name'),
                    class_group=F('class_group_id__class_group_name'),
                    year=F('academic_year'),
                    session=F('session_id__session_name'),
                    term=F('term_id__term_name')
                ).filter(**dataFilter).order_by('-grade_point_average','-obtain_marks','merit_position')
                subject_results=subject_mark_with_marge.objects.values(
                    'result_view_id',
                    'student_roll',
                    'total_exam_marks',
                    'obtain_marks',
                    'result_grade',
                    'grade_point_average',
                    'is_optional',
                    'out_of',
                    short_number=F('result_view_id__short_number'),
                    subject_one_id=F('result_view_id__subject_one_id'),
                    subject_two_id=F('result_view_id__subject_two_id'),
                    subject_three_id=F('result_view_id__subject_three_id'),
                    
                ).filter(**dataFilter).order_by('short_number')
                subject_filter=dict()
                subject_filter['class_id']=class_id
                if class_group_id:
                    subject_filter['class_group_id']=class_group_id

                subjects=Subject_List.objects.filter(**subject_filter)
                form_header=Admission_form_header.objects.filter(branch_code=branch_code)
                logo=''
                for header in form_header:
                    if header.logo:
                        logo=header.logo.url
                resultViewSetting=result_view_setting.objects.filter(**dataFilter).order_by('short_number')
                data['results']=list(final_result)
                data['subject_results']=list(subject_results)
                data['subjects']=list(subjects.values())
                data['result_view_setting']=list(resultViewSetting.values())
                data['form_header']=list(form_header.values())[0]
                data['logo']=logo
                result_grade=Result_Grade.objects.filter(out_of=data['subject_results'][0]['out_of'])
                data['result_grades']=list(result_grade.values())

        except Exception as e:
                logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                data['error_message'] = str(e)
                return JsonResponse(data)
    return JsonResponse(data)



class edu_term_result_marge(TemplateView):
    template_name = 'edu/edu-term-result-marge.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = ResultViewSettingForm()
        process_status=Process_Status_History.objects.filter(process_name='Result Process').order_by('-app_data_time')[:10]
        terms=Exam_Term.objects.filter()
        context = get_global_data(request)
        context['form'] = form
        context['terms'] = terms
        context['process_status'] = process_status
        return render(request, self.template_name, context)

@transaction.atomic
def edu_result_marge_summary(request):
    if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
    data=dict()
    if request.method == 'POST':
        try:
            with transaction.atomic():
                data['success_message'] = 'Create Successfully!'
                data['error_message'] = ''
                data['form_is_valid'] = True
                return JsonResponse(data)

        except Exception as e:
                logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                data['error_message'] = str(e)
                return JsonResponse(data)
    else:
        template_name = 'edu/edu-marge-result-summary.html'
        branch_code = request.GET.get('branch_code')
        academic_year = request.GET.get('academic_year')
        session_id = request.GET.get('session_id')
        class_id = request.GET.get('class_id')
        class_group_id = request.GET.get('class_group_id')
        term_1 = request.GET.get('term_1')
        term_2 = request.GET.get('term_2')
        dataFilter = dict()
        dataFilter['branch_code'] = branch_code
        dataFilter['academic_year'] = academic_year
        dataFilter['class_id'] = class_id
        dataFilter['one_term_id'] = term_1
        dataFilter['two_term_id'] = term_2
        
        if session_id:
            dataFilter['session_id'] = session_id
        if class_group_id:
            dataFilter['class_group_id'] = class_group_id
        formHeader=Admission_form_header.objects.filter(branch_code=branch_code).first()
        result_info=Term_Result_Marge_Final.objects.filter(**dataFilter).first()
        context = get_global_data(request)
        context['formHeader'] = formHeader
        context['result_info'] = result_info
        return render(request, template_name, context)


@transaction.atomic
def edu_result_marge_summary_data(request):
    if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
    data=dict()
    if request.method == 'POST':
        try:
            with transaction.atomic():
                branch_code = request.POST.get('branch_code')
                academic_year = request.POST.get('academic_year')
                session_id = request.POST.get('session_id')
                class_id = request.POST.get('class_id')
                class_group_id = request.POST.get('class_group_id')
                term_1 = request.POST.get('term_1')
                term_2 = request.POST.get('term_2')
                dataFilter = dict()
                Term_ids = []
                dataFilter['branch_code'] = branch_code
                dataFilter['academic_year'] = academic_year
                dataFilter['class_id'] = class_id
                dataFilter['one_term_id'] = term_1
                dataFilter['two_term_id'] = term_2
                Term_ids.append(int(term_1))
                Term_ids.append(int(term_2))
                
                if session_id:
                    dataFilter['session_id'] = session_id
                if class_group_id:
                    dataFilter['class_group_id'] = class_group_id
                    

                final_result=Term_Result_Marge_Final.objects.values(
                    'marge_tilte',
                    'student_roll',
                    'total_marks',
                    'obtain_marks',
                    'result_grade',
                    'grade_point',
                    'merit_position',
                    'grade_point_without_furth',
                    'one_term_id',
                    'one_total_marks',
                    'one_obtain_marks',
                    'one_result_grade',
                    'one_grade_point',
                    'two_term_id',
                    'two_total_marks',
                    'two_obtain_marks',
                    'two_result_grade',
                    'two_grade_point',
                    'three_term_id',
                    'three_total_marks',
                    'three_obtain_marks',
                    'three_result_grade',
                    'three_grade_point',
                    student_name=F('student_roll__student_name'),
                    gander=F('student_roll__student_gender'),
                    class_name=F('class_id__class_name'),
                    class_group=F('class_group_id__class_group_name'),
                    year=F('academic_year'),
                    session=F('session_id__session_name'),
                    one_term_name=F('one_term_id__term_name'),
                    two_term_name=F('two_term_id__term_name'),
                    three_term_name=F('three_term_id__term_name')
                ).filter(**dataFilter).order_by('-grade_point','-obtain_marks','merit_position')
                
                
                
                form_header=Admission_form_header.objects.filter(branch_code=branch_code)
                logo=''
                for header in form_header:
                    if header.logo:
                        logo=header.logo.url
                class_info=get_object_or_404(Academic_Class, class_id=class_id)
                
                data['results']=list(final_result)
                data['form_header']=list(form_header.values())[0]
                data['logo']=logo
                result_grade=Result_Grade.objects.filter(out_of=class_info.out_of)
                data['result_grades']=list(result_grade.values())
                
        except Exception as e:
                logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                data['error_message'] = str(e)
                return JsonResponse(data)
    return JsonResponse(data)


@transaction.atomic
def edu_result_marge_summary_total(request):
    if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
    data=dict()
    
    template_name = 'edu/edu-marge-result-summary-total.html'
    branch_code = request.GET.get('branch_code')
    academic_year = request.GET.get('academic_year')
    session_id = request.GET.get('session_id')
    term_1 = request.GET.get('term_1')
    term_2 = request.GET.get('term_2')
    dataFilter = dict()
    dataFilter['branch_code'] = branch_code
    dataFilter['academic_year'] = academic_year
    dataFilter['one_term_id'] = term_1
    dataFilter['two_term_id'] = term_2
    
    if session_id:
        dataFilter['session_id'] = session_id
    formHeader=Admission_form_header.objects.filter(branch_code=branch_code).first()
    result_info=Term_Result_Marge_Final.objects.filter(**dataFilter).first()
    context = get_global_data(request)
    context['formHeader'] = formHeader
    context['result_info'] = result_info
    return render(request, template_name, context)

@transaction.atomic
def edu_result_marge_summary_total_data(request):
    if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
    data=dict()
    if request.method == 'POST':
        try:
            with transaction.atomic():
                branch_code = request.POST.get('branch_code')
                academic_year = request.POST.get('academic_year')
                session_id = request.POST.get('session_id')
                marge_tilte = request.POST.get('marge_tilte')
                term_1 = request.POST.get('term_1')
                term_2 = request.POST.get('term_2')
                
                dataFilter = dict()
                dataFilter2 = dict()
                dataFilter['branch_code'] = branch_code
                dataFilter2['branch_code'] = branch_code
                dataFilter['academic_year'] = academic_year
                dataFilter2['academic_year'] = academic_year
                dataFilter['one_term_id'] = term_1
                dataFilter['two_term_id'] = term_2
                
                if session_id:
                    dataFilter['session_id'] = session_id                    
                    dataFilter2['session_id'] = session_id
                
                term_id=0
                term=Exam_Term.objects.filter(term_name = marge_tilte).first()
                if term:
                   term_id=term.id
                class_list=Academic_Class.objects.filter().annotate(class_id_uint=Cast('class_id', output_field=FloatField())).order_by('class_id_uint')
                final_result=[]
                for cl in class_list:             
                    if Term_Result_Marge_Final.objects.filter(**dataFilter,class_id=cl.class_id).exists():
                        class_result=Term_Result_Marge_Final.objects.values(
                            'marge_tilte',
                            'student_roll',
                            'total_marks',
                            'obtain_marks',
                            'result_grade',
                            'grade_point',
                            'merit_position',
                            'class_id',
                            'one_term_id',
                            'two_term_id',
                            student_name=F('student_roll__student_name'),
                            gander=F('student_roll__student_gender'),
                            class_name=F('class_id__class_name'),
                            class_group=F('class_group_id__class_group_name'),
                            year=F('academic_year'),
                            session=F('session_id__session_name'),
                            out_of=F('class_id__out_of')
                        ).filter(**dataFilter,class_id=cl.class_id).order_by('class_id')
                        result_grade=Result_Grade.objects.filter(out_of=cl.out_of)
                        cl_lg=[list(class_result.values()),list(result_grade.values())]
                        final_result.append(cl_lg)
                    elif Exam_Marks_Final.objects.filter(**dataFilter2,class_id=cl.class_id,term_id=term_id).exists():
                        class_result=Exam_Marks_Final.objects.values(
                            'student_roll',
                            'obtain_marks',
                            'result_grade',
                            'merit_position',
                            'class_id',
                            total_marks=F('total_exam_marks'),
                            grade_point=F('grade_point_average'),
                            gander=F('student_roll__student_gender'),
                            class_name=F('class_id__class_name'),
                            class_group=F('class_group_id__class_group_name'),
                            year=F('academic_year'),
                            session=F('session_id__session_name'),
                            out_of=F('class_id__out_of')
                        ).filter(**dataFilter2,class_id=cl.class_id,term_id=term.id)
                        result_grade=Result_Grade.objects.filter(out_of=cl.out_of)
                        cl_lg=[list(class_result.values()),list(result_grade.values())]
                        final_result.append(cl_lg)
                
                form_header=Admission_form_header.objects.filter(branch_code=branch_code)
                logo=''
                for header in form_header:
                    if header.logo:
                        logo=header.logo.url
                data['results']=final_result
                data['form_header']=list(form_header.values())[0]
                data['logo']=logo
        except Exception as e:
                logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                data['error_message'] = str(e)
                return JsonResponse(data)
    return JsonResponse(data)

class edu_online_exam_createlist(TemplateView):
    template_name = 'edu/edu-online-exam-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = OnlineExamModelForm()
        exams = Exam_Setup.objects.filter(exam_type_status__in=[2, 3])
        context = get_global_data(request)
        context['form'] = form
        context['exams'] = exams
        return render(request, self.template_name, context)


@transaction.atomic
def edu_online_exam_insert(request):
    data = {}
    data['form_is_valid'] = False
    try:
        with transaction.atomic():
            exam = Exam_Setup.objects.get(
                exam_id=request.POST.get('exam_id'))
            if request.method == 'POST':
                form = OnlineExamModelForm(request.POST)
                online_exam_id = fn_get_online_exam_id()
                # print(form)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.exam_id = exam
                    post.online_exam_id = online_exam_id
                    post.app_user_id = request.session["app_user_id"]
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Online exam create Successfully!'
                    mass = 'Online exam create Successfully!'
                else:
                    data['error_message'] = form.errors.as_json()
                    mass = form.errors.as_json()
                    return redirect('/edu-online-exam-createlist?message='+mass)
    except Exception as e:
        data['form_is_valid'] = False
        logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        mass = str(e)
    return redirect('/edu-online-exam-createlist?message='+mass)


def edu_online_exam_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(
        Online_Exam_Information, online_exam_id=id)
    template_name = 'edu/edu-online-exam-edit.html'
    data = dict()

    if request.method == 'POST':
        form = OnlineExamModelForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.app_user_id = request.session["app_user_id"]
            obj.save()
            data['success_message'] = 'Updated Successfully!'
            data['error_message'] = ''
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()

    else:
        form = OnlineExamModelForm(instance=instance_data)
    exams = Exam_Setup.objects.filter(exam_type_status__in=[2, 3])
    data = get_global_data(request)
    data['exams'] = exams
    data['form'] = form
    data['id'] = id
    data['instance'] = instance_data
    return render(request, template_name, data)


def edu_online_exam_question(request, online_exam_id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(
        Online_Exam_Information, online_exam_id=online_exam_id)
    template_name = 'edu/edu-online-exam-question.html'
    if instance_data.publish_status != 'Locked':
        return redirect('/edu-online-exam-createlist')
    data = dict()
    que = Online_Exam_Questions.objects.filter(
        online_exam_id=online_exam_id).count()
    total_question_mark = Online_Exam_Questions.objects.filter(
        online_exam_id=online_exam_id).aggregate(Sum('question_marks'))['question_marks__sum']
    form = OnlineExamQueModelForm()
    data['online_exam_info'] = instance_data
    data['form'] = form
    data['questions'] = que
    data['total_question_mark'] = total_question_mark
    return render(request, template_name, data)


@transaction.atomic
def edu_online_exam_question_create(request, online_exam_id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(
        Online_Exam_Information, online_exam_id=online_exam_id)
    template_name = 'edu/edu-online-exam-question.html'
    data = dict()
    if request.method == 'POST':
        try:
            with transaction.atomic():
                question_id = fn_get_online_que_id()
                online_exam_id = online_exam_id
                question = request.POST.get('question')
                question_type = request.POST.get('question_type')
                question_marks = request.POST.get('question_marks')
                if not question_marks:
                    question_marks = 0
                app_user_id = request.session["app_user_id"]
                total_question_mark = Online_Exam_Questions.objects.filter(
                    online_exam_id=online_exam_id).aggregate(Sum('question_marks'))['question_marks__sum']
                print(total_question_mark)
                if not total_question_mark:
                    total_question_mark = 0
                if(instance_data.total_marks < total_question_mark+Decimal(question_marks)):
                    data['error_message'] = 'Total marks is over.'
                    return HttpResponse('Total marks is over.')
                que = Online_Exam_Questions()
                que.question_id = question_id
                que.online_exam_id = instance_data
                que.question = question
                que.question_type = question_type
                que.question_marks = question_marks
                que.app_user_id = app_user_id
                que.save()
                new_question = Online_Exam_Questions.objects.get(
                    question_id=question_id)
                if question_type == 'MCQ':
                    ans_len = int(request.POST.get('answer_count'))
                    for ans in range(1, ans_len+1):
                        count = "ans_"+str(ans)
                        ansdata = Online_Exam_Qstn_Dtl()
                        ansdata.question_details_id = fn_get_online_que_dtl_id()
                        ansdata.question_id = new_question
                        ansdata.question_option = request.POST.get(count)
                        if request.POST.get('right_ans') and ans == int(request.POST.get('right_ans')):
                            ansdata.is_correct_answer = 1
                        else:
                            ansdata.is_correct_answer = 0
                        ansdata.app_data_time = timezone.now()
                        ansdata.app_user_id = request.session["app_user_id"]
                        ansdata.save()
                if question_type == 'MCQS':
                    ans_len = int(request.POST.get('answer_count'))
                    for ans in range(1, ans_len+1):
                        count = "ans_"+str(ans)
                        ansdata = Online_Exam_Qstn_Dtl()
                        ansdata.question_details_id = fn_get_online_que_dtl_id()
                        ansdata.question_id = new_question
                        ansdata.question_option = request.POST.get(count)
                        if request.POST.get('right_ans_'+str(ans)):
                            ansdata.is_correct_answer = 1
                        else:
                            ansdata.is_correct_answer = 0

                        ansdata.app_user_id = request.session["app_user_id"]
                        ansdata.save()
                return redirect('/edu-online-exam-question/'+str(online_exam_id))
        except Exception as e:
            logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
                sys.exc_info()[-1], type(e).__name__, str(e)))
            data['error_message'] = e
            return HttpResponse(str(e))
    form = OnlineExamQueModelForm()
    data['online_exam_info'] = instance_data
    data['form'] = form
    return render(request, template_name, data)


def edu_online_exam_question_list(request, online_exam_id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(
        Online_Exam_Information, online_exam_id=online_exam_id)
    template_name = 'edu/edu-online-exam-question-list.html'
    data = dict()
    que = Online_Exam_Questions.objects.filter(
        online_exam_id=online_exam_id).count()
    que_list = Online_Exam_Questions.objects.filter(
        online_exam_id=online_exam_id)
    total_question_mark = Online_Exam_Questions.objects.filter(
        online_exam_id=online_exam_id).aggregate(Sum('question_marks'))['question_marks__sum']
    data['online_exam_info'] = instance_data
    data['question_list'] = que_list
    data['questions'] = que
    data['total_question_mark'] = total_question_mark
    return render(request, template_name, data)


def edu_online_exam_question_edit(request, online_exam_id, que_id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(
        Online_Exam_Information, online_exam_id=online_exam_id)
    template_name = 'edu/edu-online-exam-question-edit.html'
    data = dict()
    if request.method == 'POST':
        question = Online_Exam_Questions.objects.get(question_id=que_id)
        question.question = request.POST.get('question')
        question.question_marks = request.POST.get('question_marks')
        question.app_user_id = request.session["app_user_id"]
        question.save()
        return redirect('/edu-online-exam-question-edit/'+str(online_exam_id)+'/'+str(que_id))
    else:
        que = Online_Exam_Questions.objects.filter(
            online_exam_id=online_exam_id).count()
        question = Online_Exam_Questions.objects.get(question_id=que_id)
        total_question_mark = Online_Exam_Questions.objects.filter(
            online_exam_id=online_exam_id).aggregate(Sum('question_marks'))['question_marks__sum']
        ans = Online_Exam_Qstn_Dtl.objects.filter(question_id=que_id)
        form = OnlineExamQueModelForm(instance=question)
        data['online_exam_info'] = instance_data
        data['form'] = form
        data['questions'] = que
        data['answers'] = ans
        data['question'] = question
        data['total_question_mark'] = total_question_mark
    return render(request, template_name, data)


@transaction.atomic
def edu_online_exam_mcq_answer_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    try:
        with transaction.atomic():
            ans = Online_Exam_Qstn_Dtl.objects.get(pk=id)
            if request.POST.get('ansChange') == "yes":
                ans.question_option = request.POST.get('value')
                ans.app_user_id = request.session["app_user_id"]
                ans.save()
            elif request.POST.get('ansChange') == "multiAns":
                ans.is_correct_answer = request.POST.get('value')
                ans.app_user_id = request.session["app_user_id"]
                ans.save()
            else:
                all_false = Online_Exam_Qstn_Dtl.objects.filter(
                    question_id=ans.question_id)
                for A in all_false:
                    A.is_correct_answer = 0
                    A.save()
                ans.is_correct_answer = request.POST.get('value')
                ans.app_user_id = request.session["app_user_id"]
                ans.save()
            data['success_message'] = 'Updated Successfully!'
    except Exception as e:
        data['error_message'] = e
    return JsonResponse(data)


def edu_online_exam_create_mcq_answer_field(request, que_id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    try:
        question = Online_Exam_Questions.objects.get(question_id=que_id)
        ans = Online_Exam_Qstn_Dtl()
        ans.question_details_id = fn_get_online_que_dtl_id()
        ans.question_id = question
        ans.question_option = ""
        ans.is_correct_answer = 0
        ans.app_data_time = timezone.now()
        ans.app_user_id = request.session["app_user_id"]
        ans.save()
        data['success_message'] = 'Create Successfully!'
    except Exception as e:
        data['error_message'] = str(e)
    return JsonResponse(data)


def edu_online_exam_question_delete(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    try:
        que = get_object_or_404(Online_Exam_Questions, question_id=id)
        ans = Online_Exam_Qstn_Dtl.objects.filter(question_id=que)
        ans.delete()
        que.delete()
        data['success_message'] = 'Delete Successfully!'
    except Exception as e:
        data['error_message'] = e
    return JsonResponse(data)


def edu_online_exam_answer_delete(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    try:
        ans = Online_Exam_Qstn_Dtl.objects.get(pk=id)
        ans.delete()
        data['success_message'] = 'Delete Successfully!'
    except Exception as e:
        data['error_message'] = e
    return JsonResponse(data)

##### Visited Student Information View taskwithout PK######


class edu_visited_studentInfo(TemplateView):
    template_name = 'edu/edu-visited-studentInfo.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Visited_Student_InfoModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_visited_studentInfo_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = Visited_Student_InfoModelForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            edu_count = int(request.POST.get('edu_count'))
            edu_ql_list = list()
            for i in range(1, edu_count+1):
                if(request.POST.get('degree'+str(i)) and request.POST.get('institute'+str(i))):
                    edu_ql = dict()
                    edu_ql['degree_id'] = request.POST.get('degree'+str(i))
                    edu_ql['board_name'] = request.POST.get('board'+str(i))
                    edu_ql['result_point'] = request.POST.get('point'+str(i))
                    edu_ql['result_grate'] = request.POST.get('grate'+str(i))
                    edu_ql['passing_year'] = request.POST.get('year'+str(i))
                    edu_ql['institute_id'] = request.POST.get(
                        'institute'+str(i))
                    edu_ql_list.append(edu_ql)
            post.education_qualifications = json.dumps(edu_ql_list)
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Added Successfully!'
            return JsonResponse(data)
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_visited_studentinfo_view(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Visited_Student_Info, pk=id)
    template_name = 'edu/edu-visited-studentinfo-view.html'
    data = dict()
    educations = json.loads(instance_data.education_qualifications)
    student = instance_data
    context = get_global_data(request)
    context['educations'] = educations
    context['student'] = student
    context['id'] = id
    data['html_form'] = render_to_string(
        template_name, context, request=request)
    return JsonResponse(data)


def edu_visited_studentinfo_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Visited_Student_Info, pk=id)
    template_name = 'edu/edu-visited-studentinfo-edit.html'
    data = dict()

    if request.method == 'POST':
        form = Visited_Student_InfoModelForm(
            request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():

            obj = form.save(commit=False)
            edu_count = int(request.POST.get('edu_count'))
            edu_ql_list = list()
            for i in range(1, edu_count+1):
                if(request.POST.get('degree'+str(i)) and request.POST.get('institute'+str(i))):
                    edu_ql = dict()
                    edu_ql['degree_id'] = request.POST.get('degree'+str(i))
                    edu_ql['board_name'] = request.POST.get('board'+str(i))
                    edu_ql['result_point'] = request.POST.get('point'+str(i))
                    edu_ql['result_grate'] = request.POST.get('grate'+str(i))
                    edu_ql['passing_year'] = request.POST.get('year'+str(i))
                    edu_ql['institute_id'] = request.POST.get(
                        'institute'+str(i))
                    edu_ql_list.append(edu_ql)
            obj.education_qualifications = json.dumps(edu_ql_list)
            obj.app_user_id = request.session["app_user_id"]
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
        form = Visited_Student_InfoModelForm(instance=instance_data)
        student = instance_data
        context = get_global_data(request)
        context['form'] = form
        context['student'] = student
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


def edu_visited_studentInfo_delete(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    student = Visited_Student_Info.objects.get(pk=id)
    student.delete()
    data['success_message'] = "Delete Successfully"
    return JsonResponse(data)


def edu_studentinfo_list(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    template_name = 'edu/edu-studentinfo-list.html'
    data = dict()
    form = StudentInfoModelForm()
    data = get_global_data(request)
    form.fields['student_phone'].required = False
    branchs = Branch.objects.all().order_by('branch_code')
    data['form'] = form
    data['branchs'] = branchs
    return render(request, template_name, data)


def edu_studentinfo_list_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    is_head_office_user = request.session["is_head_office_user"]

    instance_data = get_object_or_404(Students_Info, student_roll=id)
    if is_head_office_user == 'N':
        if instance_data.branch_code != request.session["branch_code"]:
            return redirect("/edu-studentinfo-list")
    template_name = 'edu/edu-studentinfo-list-edit.html'
    data = dict()

    if request.method == 'POST':
        form = StudentInfoModelForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            if off_future_date(obj.student_joining_date):
                data['error_message'] = 'Please select correct date'
                return JsonResponse(data)
            if off_future_date(obj.student_date_of_birth):
                data['error_message'] = 'Please select correct date'
                return JsonResponse(data)

            obj.student_roll = id
            form_data = dict(request.POST)
            # if obj.local_guardian_relation == 'Father':

            obj.student_present_address = form_data['student_present_address'][0]
            obj.student_permanent_address = form_data['student_permanent_address'][0]
            obj.student_date_of_birth = form_data['student_date_of_birth'][0]
            obj.student_status = form_data['student_status'][0]
            if form_data['legal_guardians'][0] == 'Father' or form_data['legal_guardians'][0] == 'Mother':
                obj.legal_guardian_relation = form_data['legal_guardians'][0]
            else:
                obj.legal_guardian_relation = form_data['legal_guardian_relation'][0]

            obj.save()
            data['status'] = obj.student_status
            data['success_message'] = 'Updated Successfully!'
            data['error_message'] = ''
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = StudentInfoModelForm(instance=instance_data)
        context = get_global_data(request)
        degree_info = Degree_Info.objects.all()
        institute = Education_Institute.objects.all()
        branchs = Branch.objects.all()
        context['form'] = form
        context['id'] = id
        context['degree_info'] = degree_info
        context['instituts'] = institute
        context['student'] = instance_data
        context['branchs'] = branchs
        return render(request, template_name, context)


def edu_studentinfo_profile_image(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    image_data = request.POST.get('image')
    format, imgstr = image_data.split(';base64,')
    ext = "png"

    img_data = ContentFile(base64.b64decode(imgstr))
    # get the filename of desired excel file
    # file_name = get_random_string(8, allowed_chars='0123456789')+"."+ext
    instance_data = get_object_or_404(Students_Info, student_roll=id)
    old_image = ""
    if instance_data.profile_image:
        old_image = instance_data.profile_image.path
    if old_image:
        if os.path.exists(old_image):
            os.remove(old_image)
    file_name = id+"_profile."+ext  # get the filename of desired excel file
    instance_data.profile_image.save(file_name, img_data, save=True)
    data = dict()
    data['success'] = "Image upload successfull."
    return JsonResponse(data)


def edu_studentinfo_profile_signature(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    signature_data = request.POST.get('signature')
    format, imgstr = signature_data.split(';base64,')
    ext = "png"

    data = ContentFile(base64.b64decode(imgstr))
    # file_name = get_random_string(8, allowed_chars='0123456789')+"."+ext #get the filename of desired excel file
    instance_data = get_object_or_404(Students_Info, student_roll=id)
    old_image = ""
    if instance_data.student_signature:
        old_image = instance_data.student_signature.path
    file_name = id+"_signature."+ext  # get the filename of desired excel file
    instance_data.student_signature.save(file_name, data, save=True)
    if old_image:
        if os.path.exists(old_image):
            os.remove(old_image)
    data = dict()
    data['success'] = "Signature upload successfull."
    return JsonResponse(data)


def edu_studentinfo_profile_image_temp(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    image_data = request.POST.get('image')
    format, imgstr = image_data.split(';base64,')
    ext = "png"

    data = ContentFile(base64.b64decode(imgstr))
    app_user_id = request.session["app_user_id"]
    # file_name = get_random_string(8, allowed_chars='0123456789')+"."+ext #get the filename of desired excel file
    instance_data = Image_temp.objects.filter(app_user_id=app_user_id).first()
    if instance_data:
        if instance_data.image_1:
            old_image = instance_data.image_1.path
            # get the filename of desired excel file
            file_name = app_user_id+"_profile."+ext
            instance_data.image_1.save(file_name, data, save=True)
            if os.path.exists(old_image):
                os.remove(old_image)
        else:
            # get the filename of desired excel file
            file_name = app_user_id+"_profile."+ext
            instance_data.image_1.save(file_name, data, save=True)
    else:
        image_table = Image_temp()
        # get the filename of desired excel file
        file_name = app_user_id+"_profile."+ext
        image_table.app_user_id = app_user_id
        image_table.save()
        image_table.image_1.save(file_name, data, save=True)
    data = dict()
    data['success'] = "Image upload successfull."
    return JsonResponse(data)


def edu_studentinfo_signature_image_temp(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    image_data = request.POST.get('signature')
    format, imgstr = image_data.split(';base64,')
    ext = "png"

    data = ContentFile(base64.b64decode(imgstr))
    app_user_id = request.session["app_user_id"]
    # file_name = get_random_string(8, allowed_chars='0123456789')+"."+ext #get the filename of desired excel file
    instance_data = Image_temp.objects.filter(app_user_id=app_user_id).first()
    if instance_data:
        if instance_data.image_2:
            old_image = instance_data.image_2.path
            # get the filename of desired excel file
            file_name = app_user_id+"_signature."+ext
            instance_data.image_2.save(file_name, data, save=True)
            if os.path.exists(old_image):
                os.remove(old_image)
        else:
            # get the filename of desired excel file
            file_name = app_user_id+"_signature."+ext
            instance_data.image_2.save(file_name, data, save=True)
    else:
        image_table = Image_temp()
        # get the filename of desired excel file
        file_name = app_user_id+"_signature."+ext
        image_table.app_user_id = app_user_id
        image_table.save()
        image_table.image_2.save(file_name, data, save=True)
    data = dict()
    data['success'] = "Image upload successfull."
    return JsonResponse(data)


def edu_studentinfo_profile_signature(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    signature_data = request.POST.get('signature')
    format, imgstr = signature_data.split(';base64,')
    ext = "png"

    data = ContentFile(base64.b64decode(imgstr))
    # file_name = get_random_string(8, allowed_chars='0123456789')+"."+ext #get the filename of desired excel file
    instance_data = get_object_or_404(Students_Info, student_roll=id)
    old_image = ""
    if instance_data.student_signature:
        old_image = instance_data.student_signature.path
    if os.path.exists(old_image):
        os.remove(old_image)
    file_name = id+"_signature."+ext  # get the filename of desired excel file
    instance_data.student_signature.save(file_name, data, save=True)
    data = dict()
    data['success'] = "Signature upload successfull."
    return JsonResponse(data)


class edu_last_institute(TemplateView):
    template_name = 'edu/edu-last-institute.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = EducationInstituteModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_online_question_preview(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    template_name = 'edu/edu-online-question-preview.html'
    data = dict()
    que = get_object_or_404(Online_Exam_Information, online_exam_id=id)
    data = get_global_data(request)
    data['question'] = que
    return render(request, template_name, data)


def edu_online_exam_question_update(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    if request.method == 'POST':
        que = get_object_or_404(Online_Exam_Questions, question_id=id)
        print(request.POST.get('question'))
        que.question = request.POST.get('question')
        que.app_user_id = request.session["app_user_id"]
        que.save()
        data['success'] = 'This question update successfull.'
    return JsonResponse(data)


def edu_student_exam_question(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    template_name = 'edu/edu-student-exam-question.html'
    data = dict()
    students = StudentInfoModelForm()
    online_exam = OnlineExam_Ans_Info.objects.all()
    data = get_global_data(request)
    data['form'] = students
    data['online_exam'] = online_exam
    return render(request, template_name, data)


class edu_exam_question_html(TemplateView):
    template_name = 'edu/edu-exam-question-html.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        student_roll = request.GET.get('student_roll')
        online_exam_id = request.GET.get('online_exam_id')
        ans_info = OnlineExam_Ans_Info.objects.filter(
            student_roll=student_roll, online_exam_id=online_exam_id, publish_status="Live")
        context = get_global_data(request)
        context['ans_info'] = ans_info
        return render(request, self.template_name, context)


@transaction.atomic
def edu_online_exam_ans_by_student(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    try:
        with transaction.atomic():
            question_type = request.POST.get('question_type')

            if(question_type == 'MCQ'):
                value = request.POST.get('value')
                answer = get_object_or_404(OnlineExam_Qstn_Ansdtl, pk=id)
                answer_all = OnlineExam_Qstn_Ansdtl.objects.filter(
                    answer_id=answer.answer_id)
                for ans in answer_all:
                    ans.is_correct_answer = 0
                    ans.app_user_id = request.session["app_user_id"]
                    ans.save()
                answer.is_correct_answer = value
                answer.app_user_id = request.session["app_user_id"]
                answer.save()
                data['success_message'] = 'success'
            elif question_type == 'MCQS':
                value = request.POST.get('value')
                answer = get_object_or_404(OnlineExam_Qstn_Ansdtl, pk=id)
                answer.is_correct_answer = value
                answer.app_user_id = request.session["app_user_id"]
                answer.save()
                data['success_message'] = 'success'
            elif question_type == 'Short' or question_type == 'Creative':
                value = request.POST.get('value')
                answer_exists = OnlineExam_Qstn_Ansdtl.objects.filter(
                    answer_id=id).exists()
                if answer_exists:
                    answer = OnlineExam_Qstn_Ansdtl.objects.get(answer_id=id)
                    answer.answer_option = value
                    answer.app_user_id = request.session["app_user_id"]
                    answer.save()
                    data['success_message'] = 'success'
                else:
                    print(value)
                    new_ans = OnlineExam_Qstn_Ansdtl()
                    new_ans.answer_id = get_object_or_404(
                        OnlineExam_Question_Ans, answer_id=id)
                    new_ans.answer_option = value
                    new_ans.app_user_id = request.session["app_user_id"]
                    new_ans.save()
                    data['success_message'] = 'success'

    except Exception as e:
        logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        data['error_message'] = str(e)
    return JsonResponse(data)


def edu_studentinfo_print(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Students_Info, student_roll=id)
    template_name = 'edu/edu-studentinfo-print.html'
    data = dict()
    # educations=json.loads(instance_data.student_roll)
    data['students'] = instance_data
    # data['educations']=educations
    return render(request, template_name, data)


def edu_new_education_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    data = dict()
    institute_id = fn_get_institute_id()
    institute_name = request.POST.get('institute')
    institute_code = request.POST.get('institute_code')
    institute_address = request.POST.get('institute_address')
    institute_mobile = request.POST.get('institute_contact')
    lower_degree = request.POST.get('lowest_degree')
    higher_degree = request.POST.get('highest_degree')

    insertion = Education_Institute()
    insertion.institute_id = institute_id
    insertion.institute_name = institute_name
    insertion.institute_code = institute_code
    insertion.institute_address = institute_address
    insertion.institute_mobile = institute_mobile
    insertion.lower_degree = lower_degree
    insertion.higher_degree = higher_degree
    insertion.app_user_id = request.session["app_user_id"]
    insertion.save()

    data['new_institute'] = {
        'institute_id': institute_id, 'institute_name': institute_name}
    data['form_is_valid'] = True
    data['success_message'] = 'Institute Added Successfully!'
    return JsonResponse(data)
#### Visited Student form r Education qualification New Institute Adding###


class edu_visited_institute(TemplateView):
    template_name = 'edu/edu-visited-institute.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = EducationInstituteModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_visited_institute_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    data = dict()
    institute_id = fn_get_institute_id()
    institute_name = request.POST.get('institute')
    institute_code = request.POST.get('institute_code')
    institute_address = request.POST.get('institute_address')
    institute_mobile = request.POST.get('institute_contact')
    lower_degree = request.POST.get('lowest_degree')
    higher_degree = request.POST.get('highest_degree')

    insertion = Education_Institute()
    insertion.institute_id = institute_id
    insertion.institute_name = institute_name
    insertion.institute_code = institute_code
    insertion.institute_address = institute_address
    insertion.institute_mobile = institute_mobile
    insertion.lower_degree = lower_degree
    insertion.higher_degree = higher_degree
    insertion.app_user_id = request.session["app_user_id"]
    insertion.save()

    data['new_institute'] = {
        'institute_id': institute_id, 'institute_name': institute_name}
    data['form_is_valid'] = True
    data['success_message'] = 'Institute Added Successfully!'
    return JsonResponse(data)


def edu_questionSubmit_button(request, ans_info_id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()

    OnlineExamAnsInfo = OnlineExam_Ans_Info.objects.filter(
        ans_info_id=ans_info_id)
    for status in OnlineExamAnsInfo:
        status.publish_status = "Submitted"
        status.save()
        data['publish_status'] = status.publish_status
        return JsonResponse(data)
    return JsonResponse(data)


@transaction.atomic
def edu_online_exam_ans_by_student(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    try:
        with transaction.atomic():
            question_type = request.POST.get('question_type')

            if(question_type == 'MCQ'):
                value = request.POST.get('value')
                answer = get_object_or_404(OnlineExam_Qstn_Ansdtl, pk=id)
                answer_all = OnlineExam_Qstn_Ansdtl.objects.filter(
                    answer_id=answer.answer_id)
                for ans in answer_all:
                    ans.is_correct_answer = 0
                    ans.app_user_id = request.session["app_user_id"]
                    ans.save()
                answer.is_correct_answer = value
                answer.app_user_id = request.session["app_user_id"]
                answer.save()
                data['success_message'] = 'success'
            elif question_type == 'MCQS':
                value = request.POST.get('value')
                answer = get_object_or_404(OnlineExam_Qstn_Ansdtl, pk=id)
                answer.is_correct_answer = value
                answer.app_user_id = request.session["app_user_id"]
                answer.save()
                data['success_message'] = 'success'
            elif question_type == 'Short' or question_type == 'Creative':
                value = request.POST.get('value')
                answer_exists = OnlineExam_Qstn_Ansdtl.objects.filter(
                    answer_id=id).exists()
                if answer_exists:
                    answer = OnlineExam_Qstn_Ansdtl.objects.get(answer_id=id)
                    answer.answer_option = value
                    answer.app_user_id = request.session["app_user_id"]
                    answer.save()
                    data['success_message'] = 'success'
                else:
                    new_ans = OnlineExam_Qstn_Ansdtl()
                    new_ans.answer_id = get_object_or_404(
                        OnlineExam_Question_Ans, answer_id=id)
                    new_ans.answer_option = value
                    new_ans.app_user_id = request.session["app_user_id"]
                    new_ans.save()
                    data['success_message'] = 'success'

    except Exception as e:
        logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        data['error_message'] = str(e)
    return JsonResponse(data)


def edu_studentinfo_print(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Students_Info, student_roll=id)
    branch_code = request.GET.get('branch_code')
    
    institute = Academy_info.objects.first()
    template_name = 'edu/edu-studentinfo-print.html'
    form_header=Admission_form_header.objects.filter(branch_code=branch_code).first()
    data = dict()
    data['students'] = instance_data
    data['institute'] = institute
    data['form_header'] = form_header
    return render(request, template_name, data)

### All Students Result List Subjectwise#####


class edu_student_result_subjectwise(TemplateView):
    template_name = 'edu/edu-student-result-subjectwise.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = StudentInfoModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


class edu_student_result_beforepunlish(TemplateView):
    template_name = 'edu/edu-student-result-beforepublish.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = StudentInfoModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_student_result_beforepunlish_data(request):
    template_name = "edu/rsult-table-beforepublish.html"
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    if request.method == 'POST':
        branch_code = request.POST.get('branch_code')
        academic_year = request.POST.get('academic_year')
        term_id = request.POST.get('term_id')
        class_id = request.POST.get('class_id')
        class_group_id = request.POST.get('class_group_id')
        limit = request.POST.get('limit')
        page = request.POST.get('page')
        json = request.POST.get('json')
        with_position = request.POST.get('with_position')
        app_user_id = request.session["app_user_id"]
        datafilter = dict()
        datafilter['branch_code'] = branch_code
        datafilter['academic_year'] = academic_year
        datafilter['term_id'] = term_id
        datafilter['class_id'] = class_id

        if class_group_id:
            datafilter['class_group_id'] = class_group_id
        data = dict()
        class_info = Academic_Class.objects.filter(class_id=class_id).first()
        results = Exam_Marks_Details.objects.filter(
            **datafilter).order_by('student_roll__class_roll')
        subjectResults = results.values('student_roll', 'student_roll__class_roll', 'student_roll__student_name', 'class_group_id__class_group_name', 'subject_id__subject_name', 'subject_id__maximum_marks', 'subject_id').annotate(
            total_sub=Count('subject_id'), total_students=Count('student_roll'),
            total=Sum('total_exam_marks'), obtain=Sum('obtain_marks'))
        for result in subjectResults:
            gpa = get_result_great(
                result['obtain'], result['subject_id__maximum_marks'], class_info.out_of)
            result['gpa'] = gpa[0]
            result['lg'] = gpa[1]

        students = subjectResults.values('student_roll', 'student_roll__class_roll','student_roll__class_id__class_name', 
                                         'student_roll__student_name', 'class_group_id__class_group_name','student_roll__student_father_name',
                                         'student_roll__student_mother_name',
                                         'student_roll__student_date_of_birth').annotate(
            subject_count=Count('student_roll'), subjectTotalMarks=Sum('subject_id__maximum_marks'), totalObtain=Sum('obtain_marks'))

        for s in students:
            gpa = get_final_result_great(
                academic_year, term_id, class_id, s['student_roll'], app_user_id)
            s['total'] = s['subjectTotalMarks']
            s['obtain'] = s['totalObtain']
            s['gpa'] = gpa[2]
            s['lg'] = gpa[3]
            
        if with_position == 'true':
            #Position Calculation
            position = 1
            student_list_withMarks=list(students)
            student_list_withMarks.sort(key=lambda x: (
                        x['gpa'], x['obtain']), reverse=True)
            for index, m in enumerate(student_list_withMarks):
                for st in students:
                    if st['student_roll'] == m['student_roll']:
                        if st['gpa'] > 0:
                            st['position'] = position
                            position+=1
                        else:
                            st['position'] = 0
        
        paginator = Paginator(students, limit)
        paginat_data = paginator.page(page)
        institute = Admission_form_header.objects.filter(branch_code=branch_code)
        term = Exam_Term.objects.filter(id=term_id).first()
        data['subject_results'] = subjectResults
        data['students_results'] = paginat_data
        data['class_name'] = class_info.class_name
        data['institute'] = institute.first()
        data['term'] = term.term_name
        data['academic_year'] = academic_year
        if json:
            grade_list=Result_Grade.objects.filter(out_of=class_info.out_of)
            jsonData=dict()
            jsonData['subject_results']=list(subjectResults)
            jsonData['students_results']=list(paginat_data)
            jsonData['class_name']=class_info.class_name
            jsonData['institute'] = list(institute.values())
            jsonData['grade_list'] = list(grade_list.values())
            jsonData['term'] = term.term_name
            jsonData['academic_year'] = academic_year
            jsonData['page_info'] = str(paginat_data).replace('Page','Sheet').replace('<','_').replace('>','')
            return JsonResponse(jsonData)
    return render(request, template_name, data)


def edu_student_result_beforepunlish_data_list(request):
    template_name = "edu/edu-exam-marks-before-publish-data-list.html"
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    if request.method == 'GET':
        branch_code = request.GET.get('branch_code')
        academic_year = request.GET.get('academic_year')
        term_id = request.GET.get('term_id')
        class_id = request.GET.get('class_id')
        class_group_id = request.GET.get('class_group_id')
        limit = request.GET.get('limit')
        page = request.GET.get('page')
        app_user_id = request.session["app_user_id"]
        datafilter = dict()
        datafilter['branch_code'] = branch_code
        datafilter['academic_year'] = academic_year
        datafilter['term_id'] = term_id
        datafilter['class_id'] = class_id

        if class_group_id:
            datafilter['class_group_id'] = class_group_id
        data = dict()
        subjects = list()
        class_info = Academic_Class.objects.filter(class_id=class_id).first()
        results = Exam_Marks_Details.objects.filter(
            **datafilter).order_by('student_roll__class_roll')
        subjectResults = results.values('student_roll', 'student_roll__class_roll', 'student_roll__student_name', 'class_id__class_name', 'class_group_id__class_group_name', 'subject_id__subject_name', 'subject_id__sort_name', 'subject_id__maximum_marks', 'subject_id').annotate(
            total_sub=Count('subject_id'), total_students=Count('student_roll'),
            total=Sum('total_exam_marks'), obtain=Sum('obtain_marks'))
        for result in subjectResults:
            gpa = get_result_great(
                result['obtain'], result['subject_id__maximum_marks'], class_info.out_of)
            result['gpa'] = gpa[0]
            result['lg'] = gpa[1]
            subData = dict()
            subData['subject_sort_name'] = result['subject_id__sort_name']
            subData['subject_id'] = result['subject_id']
            if not subData in subjects:
                subjects.append(subData)

        students = subjectResults.values('student_roll', 'student_roll__class_roll', 'student_roll__student_name', 'class_group_id__class_group_name').annotate(
            subject_count=Count('student_roll'), subjectTotalMarks=Sum('subject_id__maximum_marks'), totalObtain=Sum('obtain_marks'))

        for s in students:
            gpa = get_final_result_great(
                academic_year, term_id, class_id, s['student_roll'], app_user_id)
            s['total'] = s['subjectTotalMarks']
            s['obtain'] = s['totalObtain']
            s['gpa'] = gpa[2]
            s['lg'] = gpa[3]
        
        #Position Calculation
        position = 1
        student_list_withMarks=list(students)
        student_list_withMarks.sort(key=lambda x: (
                    x['gpa'], x['obtain']), reverse=True)
        for index, m in enumerate(student_list_withMarks):
            for st in students:
                if st['student_roll'] == m['student_roll']:
                    if st['gpa'] > 0:
                        st['position'] = position
                        position+=1
                    else:
                        st['position'] = 0
        
        paginator = Paginator(students, limit)
        paginat_data = paginator.page(page)
        institute = Admission_form_header.objects.filter(branch_code=branch_code).first()
        term = Exam_Term.objects.filter(id=term_id).first()
        data['subject_results'] = subjectResults
        data['students_results'] = paginat_data
        data['institute'] = institute
        data['subjects'] = subjects
        data['term'] = term.term_name
        data['academic_year'] = academic_year

    return render(request, template_name, data)


class edu_student_result_table(TemplateView):
    template_name = 'edu/edu-student-result-table.html'

    @transaction.atomic
    def get(self, request):
        data = {}
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')

        academic_year = request.GET.get('academic_year')
        term_id = request.GET.get('term_id')
        class_id = request.GET.get('class_id')
        class_group_id = request.GET.get('class_group_id')
        if not class_group_id:
            class_group_id = None
        subject_id = request.GET.get('subject_id')
        app_user_id = request.session["app_user_id"]
        try:
            with transaction.atomic():
                data['func_result_subjectwise'] = fn_result_subjectwise(
                    int(academic_year), int(term_id), class_id, class_group_id, app_user_id)
        except Exception as e:
            print(str(e))

        sql = '''SELECT total_subject item_count,
      (CASE WHEN subject_serial = 1 THEN 'Y' ELSE NULL END) row_span,
      subject_serial,
      student_roll,
      class_roll,
      student_name,
      subject_name,
      total_obtain_marks,
      total_marks,
      final_result_gpa,
      final_grade_name,
      result_gpa,
      grade_name,
      academic_year,
      class_id,
      class_group_id,
      subject_id
 FROM (SELECT count (student_roll)
              OVER (PARTITION BY student_roll
                    ORDER BY cast (student_roll AS BIGINT))
                 total_subject,
              ROW_NUMBER ()
              OVER (PARTITION BY student_roll
                    ORDER BY cast (student_roll AS BIGINT), subject_name)
                 subject_serial,
              student_roll,
              class_roll,
              student_name,
              final_result_gpa,
              final_grade_name,
              subject_name,
              total_obtain_marks,
              sum (total_obtain_marks)
              OVER (PARTITION BY student_roll
                    ORDER BY cast (student_roll AS BIGINT))
              total_obtain_marks_subject,
              sum (total_marks)
              OVER (PARTITION BY student_roll
                    ORDER BY cast (student_roll AS BIGINT))
              total_marks_subject,
              total_marks,
              result_gpa,
              grade_name,
              academic_year,
              class_id,
              class_group_id,
              subject_id
         FROM (  SELECT s.student_roll,
                        s.class_roll,
                        s.student_name,
                        s.final_result_gpa,
                        s.final_grade_name,
                        sub.subject_name,
                        t.total_obtain_marks,
                        t.total_marks,
                        t.result_gpa,
                        t.grade_name,
                        t.academic_year,
                        t.class_id,
                        t.class_group_id,
                        t.subject_id
                   FROM edu_subjectmarktemp t,
                        (SELECT s.student_roll,
                                 s.class_roll,
                                 s.student_name,
                                 s.final_result_gpa,
                                 s.final_grade_name
                            FROM edu_students_info s
                           WHERE     s.academic_year = '''+"'"+academic_year+"'"+'''
                                 AND s.class_id = '''+"'"+class_id+"'"+''') s,
                        edu_subject_list sub
                  WHERE     t.student_roll = s.student_roll
                        AND sub.subject_id = t.subject_id'''
        if academic_year:
            sql = sql + " and t.academic_year='"+academic_year+"'"
        if class_id:
            sql = sql + " and t.class_id='"+class_id+"'"
        if class_group_id:
            sql = sql + " and t.class_group_id='"+class_group_id+"'"
        if subject_id:
            sql = sql + " and t.subject_id='"+subject_id+"'"

        sql = sql + " and t.app_user_id='"+app_user_id+"'"

        sql = sql + '''
               ORDER BY cast (s.class_roll AS BIGINT)) data) final_data '''

        query = dict()

        if class_id:
            query['class_id'] = class_id
        if subject_id:
            query['subject_id'] = subject_id
        # exam_names=Exam_Setup.objects.values('exam_name').annotate(col_num=Count('exam_name')).filter(academic_year=academic_year,term_id=term_id,**query).order_by('exam_name')
        total_marks = SubjectMarkTemp.objects.values('student_roll').annotate(mark=Sum(
            'total_obtain_marks'), gpa=Sum('result_gpa')).filter(academic_year=academic_year, app_user_id=app_user_id)
        total_mark = list(total_marks)
        institute = Academy_info.objects.first()
        datafilter = dict()
        datafilter['academic_year'] = academic_year
        datafilter['class_id'] = class_id
        datafilter['term_id'] = term_id
        if class_group_id:
            datafilter['class_group_id'] = class_group_id
        result_period = Exam_Setup.objects.filter(**datafilter).first()
        total_mark.sort(key=lambda x: (x['gpa'], x['mark']), reverse=True)

        mark = fn_get_query_result(sql)
        # print(mark)
        Fail = 0
        position = 0
        for index, m in enumerate(total_mark):
            Pass = [x for x in mark if x['final_result_gpa'] and x['final_result_gpa']
                    > 0 and x['student_roll'] == m['student_roll']]
            if Pass:
                position += 1
                m['position'] = position
            else:
                Fail += 1
                m['position'] = 0
        total_student = len(total_mark)
        context = get_global_data(request)
        # context['exam_names'] = exam_names
        context['total_mark'] = total_mark
        context['mark'] = mark
        context['institute'] = institute
        context['result_period'] = result_period
        context['Pass_Percentage'] = format(
            (position/(total_student if total_student else 1))*100, ".2f")
        context['Fail_Percentage'] = format(
            (Fail/(total_student if total_student else 1))*100, ".2f")
        return render(request, self.template_name, context)


class edu_onestudent_result_allsubjects(TemplateView):
    template_name = 'edu/edu-onestudent-result-allsubjects.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')

        app_user_id = request.session["app_user_id"]
        academic_year = request.GET.get('academic_year')
        term_id = request.GET.get('term_id')
        class_id = request.GET.get('class_id')
        student_roll = request.GET.get('student_roll')
        m_position = request.GET.get('m_position')
        sql = '''SELECT total_subject item_count,
      (CASE WHEN subject_serial = 1 THEN 'Y' ELSE NULL END) row_span,
      subject_serial,
      student_roll,
      student_name,
      subject_name,
      total_obtain_marks,
      total_marks,
      (select result_gpa from fn_get_final_result_gpa('''+"'"+academic_year+"'"+''','''+"'"+term_id+"'"+''',class_id,student_roll,'''+"'"+app_user_id+"'"+''')) final_result_gpa,
      (select grade_name from fn_get_final_result_gpa('''+"'"+academic_year+"'"+''','''+"'"+term_id+"'"+''',class_id,student_roll,'''+"'"+app_user_id+"'"+''')) final_grade_name,
      result_gpa,
      grade_name,
      academic_year,
      class_id,
      class_group_id,
      subject_id
 FROM (SELECT count (student_roll)
              OVER (PARTITION BY student_roll
                    ORDER BY cast (student_roll AS BIGINT))
                 total_subject,
              ROW_NUMBER ()
              OVER (PARTITION BY student_roll
                    ORDER BY cast (student_roll AS BIGINT), subject_name)
                 subject_serial,
              student_roll,
              student_name,
              subject_name,
              total_obtain_marks,
              sum (total_obtain_marks)
              OVER (PARTITION BY student_roll
                    ORDER BY cast (student_roll AS BIGINT))
              total_obtain_marks_subject,
              sum (total_marks)
              OVER (PARTITION BY student_roll
                    ORDER BY cast (student_roll AS BIGINT))
              total_marks_subject,
              total_marks,
              result_gpa,
              grade_name,
              academic_year,
              class_id,
              class_group_id,
              subject_id
         FROM (  SELECT s.student_roll,
                        s.student_name,
                        sub.subject_name,
                        t.total_obtain_marks,
                        t.total_marks,
                        t.result_gpa,
                        t.grade_name,
                        t.academic_year,
                        t.class_id,
                        t.class_group_id,
                        t.subject_id
                   FROM edu_subjectmarktemp t,
                        edu_students_info s,
                        edu_subject_list sub
                  WHERE     t.student_roll = s.student_roll
                        AND sub.subject_id = t.subject_id'''
        if academic_year:
            sql = sql + " and t.academic_year='"+academic_year+"'"
        if class_id:
            sql = sql + " and t.class_id='"+class_id+"'"
        if student_roll:
            sql = sql + " and t.student_roll='"+student_roll+"'"

        sql = sql + " and t.app_user_id='"+app_user_id+"'"
        sql = sql + '''
               ORDER BY cast (s.student_roll AS BIGINT)) data) final_data '''

        mark = fn_get_query_result(sql)
        subject_mark = Exam_Single_Mark.objects.filter(
            academic_year=academic_year,
            term_id=term_id, class_id=class_id, student_roll=student_roll)
        subjects = subject_mark.values(
            'subject_id', 'subject_id__subject_name', 'obtain_marks', 'student_roll').annotate(Count('subject_id'))
        for subject in subjects:
            m = []
            for sm in subject_mark:
                if subject['subject_id'] == sm.subject_id.subject_id:
                    m.append(sm)
            subject['result'] = m
            # print(subject)

        total_obtain_mark = subjects.values(
            'student_roll').annotate(total=Sum('obtain_marks'))
        total_mark = subjects.values('student_roll').annotate(
            total=Sum('subject_id__maximum_marks'))
        institute = get_object_or_404(Academy_info)
        out_of = Academic_Class.objects.values(
            'out_of').filter(class_id=class_id).first()
        grade_table = Result_Grade.objects.filter(
            out_of=out_of['out_of']).order_by('-result_gpa')
        context = get_global_data(request)
        context['mark'] = mark
        context['institute'] = institute
        context['grade_table'] = grade_table
        context['subject_marks'] = subjects
        context['m_position'] = m_position
        context['total_mark'] = total_mark[0]['total']
        context['total_obtain_mark'] = total_obtain_mark[0]['total']
        return render(request, self.template_name, context)


class edu_onesubject_allexammark(TemplateView):
    template_name = 'edu/edu-onesubject-allexammark.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')

        academic_year = request.GET.get('academic_year')
        term_id = request.GET.get('term_id')
        class_id = request.GET.get('class_id')
        student_roll = request.GET.get('student_roll')
        subject_id = request.GET.get('subject_id')

        exam = Exam_Single_Mark.objects.filter(academic_year=academic_year, term_id=term_id, class_id=class_id,
                                               subject_id=subject_id, student_roll=student_roll)
        institute = get_object_or_404(Academy_info)
        context = get_global_data(request)
        context['exam'] = exam
        context['institute'] = institute
        return render(request, self.template_name, context)


def edu_studentInfo_education_edit(request):
    data = dict()
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    id = request.POST.get("id")
    degree_id = request.POST.get("degree_id")
    institute_id = request.POST.get("institute_id")
    student_roll = request.POST.get("student_roll")

    if id:
        education = Education_Qualification.objects.get(pk=id)
        if degree_id:
            education.degree_name = get_object_or_404(
                Degree_Info, degree_id=degree_id)
        education.result_point = request.POST.get("result_point")
        education.result_grate = request.POST.get("result_grate")
        education.passing_year = request.POST.get("passing_year")
        education.board_name = request.POST.get("board_name")
        if institute_id:
            education.institute_id = get_object_or_404(
                Education_Institute, institute_id=institute_id)
        education.app_user_id = request.session["app_user_id"]
        education.save()
        data['education_id'] = education.pk
        return JsonResponse(data)
    else:
        education = Education_Qualification()
        education.student_roll = get_object_or_404(
            Students_Info, student_roll=student_roll)
        education.app_user_id = request.session["app_user_id"]
        education.save()
        data['education_id'] = education.pk
        return JsonResponse(data)


def edu_studentInfo_education_delete(request, id):
    data = dict()
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    education = get_object_or_404(Education_Qualification, pk=id)
    education.delete()
    return JsonResponse(data)


@transaction.atomic
def edu_result_publish_button(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    academic_year = request.POST.get('academic_year')
    class_id = request.POST.get('class_id')
    class_group_id = request.POST.get('class_group_id')
    term_id = request.POST.get('term_id')
    app_user_id = request.session["app_user_id"]
    if not class_group_id:
        class_group_id = None
    try:
        with transaction.atomic():
            cursor = connection.cursor()
            cursor.callproc("fn_exam_mark_publish", [
                int(academic_year), int(term_id), class_id, class_group_id, app_user_id])
            status = cursor.fetchone()
            if status[0] == 'S':
                total_marks = Store_Exam_Single_Mark.objects.values('student_roll').annotate(mark=Sum('obtain_marks'), gpa=Sum(
                    'grade_point_average')).filter(academic_year=academic_year, class_id=class_id, term_id=term_id)
                total_mark = list(total_marks)
                total_mark.sort(key=lambda x: (
                    x['gpa'], x['mark']), reverse=True)
                position = 1
                for index, m in enumerate(total_mark):
                    f_exam_mark = Exam_Marks_Final.objects.filter(
                        academic_year=academic_year, class_id=class_id, term_id=term_id, student_roll=m['student_roll']).first()
                    if f_exam_mark.grade_point_average > 0:
                        f_exam_mark.merit_position = position
                        position += 1
                    else:
                        f_exam_mark.merit_position = 0
                    f_exam_mark.save()
                data['success_message'] = status
            else:
                data['error_message'] = status
            return JsonResponse(data)
    except Exception as e:
        logger.error("Error in Result Publist {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        data['error_message'] = str(e)
    return JsonResponse(data)


def edu_submitted_question(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    template_name = 'edu/edu-submitted-question.html'
    context = dict()
    academic_year = Academic_Year.objects.all()
    academic_Class = Academic_Class.objects.all()
    online_exam = Online_Exam_Information.objects.all()
    context = {
        'academic_year': academic_year,
        'academic_Class': academic_Class,
        'online_exam': online_exam
    }

    return render(request, template_name, context)


def edu_submitted_questionlist(request):
    template_name = 'edu/edu-submitted-questionlist.html'
    context = dict()
    academic_year = request.GET.get('academic_year')
    class_id = request.GET.get('class_id')
    online_exam_id = request.GET.get('online_exam_id')
    exam_info = OnlineExam_Ans_Info.objects.filter(
        online_exam_id__exam_id__academic_year=academic_year, online_exam_id__exam_id__class_id=class_id, online_exam_id=online_exam_id)
    context = {
        'exam_info': exam_info
    }
    return render(request, template_name, context)


def edu_submitted_questionLive(request, ans_info_id):
    data = dict()
    ans_info = get_object_or_404(OnlineExam_Ans_Info, ans_info_id=ans_info_id)
    publish_status = ans_info.publish_status
    if(publish_status == 'Submitted'):
        ans_info.publish_status = 'Live'
        ans_info.save()
    data['status'] = ans_info.publish_status
    return JsonResponse(data)


def edu_submitted_questionView(request, ans_info_id):
    template_name = 'edu/edu-submitted-questionView.html'
    data = dict()
    que = get_object_or_404(OnlineExam_Ans_Info, ans_info_id=ans_info_id)
    for single_question in que.ans_info.all():
        if single_question.question_id.question_type == 'MCQ':
            for answer in single_question.oqadtl_answer_id.all():
                true_is = answer.is_correct_answer*answer.question_details_id.is_correct_answer
                if true_is:
                    mark = single_question.question_id.question_marks
                    single_question.obtain_marks = mark
                    single_question.save()

        if single_question.question_id.question_type == 'MCQS':
            true_ans = True
            mark = single_question.question_id.question_marks
            for answer in single_question.oqadtl_answer_id.all():
                if (answer.is_correct_answer == 1 and answer.question_details_id.is_correct_answer == 0) or (answer.is_correct_answer == 0 and answer.question_details_id.is_correct_answer == 1):
                    true_ans = False
                    break
            if true_ans:
                single_question.obtain_marks = mark
                single_question.save()

    obtain_marks = OnlineExam_Question_Ans.objects.filter(
        ans_info_id=que.ans_info_id).aggregate(Sum('obtain_marks'))['obtain_marks__sum']
    que.total_obtain_marks = obtain_marks
    que.save()
    data = get_global_data(request)
    data['question'] = que
    return render(request, template_name, data)


@transaction.atomic
def edu_publish_online_question_preview(request, online_exam_id):
    branch_code = 100
    data = dict()
    try:
        with transaction.atomic():
            online_exam_info = Online_Exam_Information.objects.get(
                online_exam_id=online_exam_id)

            class_id = online_exam_info.exam_id.class_id.class_id
            app_user_id = request.session["app_user_id"]
            students = Students_Info.objects.filter(class_id=class_id)
            for student in students:
                cursor = connection.cursor()
                cursor.callproc("fn_onlineexam_live", [
                    branch_code, student.student_roll, online_exam_id, app_user_id])
                result = cursor.fetchone()
            online_exam_info.publish_status = "Live"
            online_exam_info.save()
            data['online_exam'] = result
    except Exception as e:
        logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        data['error_message'] = str(e)
        return HttpResponse(data)
    return redirect('/edu-online-question-preview/'+str(online_exam_id))


def edu_test(request):
    data = OnlineExam_Ans_Info.objects.filter(
        online_exam_id__exam_id__class_id='000003')
    student = ""
    for s in data:
        student = s.online_exam_id
    # data=Online_Exam_Information.objects.filter(exam_id__class_id='000003')
    return HttpResponse(student)


@transaction.atomic
def edu_onlineexam_queansmarking(request, ans_id):
    data = dict()
    try:
        with transaction.atomic():
            quee_ans = get_object_or_404(
                OnlineExam_Question_Ans, answer_id=ans_id)
            obtain_mark = request.POST.get('obtain_marks')
            quee_ans.obtain_marks = obtain_mark
            quee_ans.save()

            ans_info = get_object_or_404(
                OnlineExam_Ans_Info, ans_info_id=quee_ans.ans_info_id.ans_info_id)
            obtain_marks = OnlineExam_Question_Ans.objects.filter(
                ans_info_id=quee_ans.ans_info_id.ans_info_id).aggregate(Sum('obtain_marks'))['obtain_marks__sum']
            ans_info.total_obtain_marks = obtain_marks
            ans_info.save()
    except Exception as e:
        logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        data['error_message'] = str(e)
        return JsonResponse(data)
    data['success'] = 'Save successfull'
    return JsonResponse(data)


@transaction.atomic
def edu_onlineexam_result_publish(request):
    data = dict()
    try:
        with transaction.atomic():
            academic_year = request.GET.get('academic_year')
            class_id = request.GET.get('class_id')
            online_exam_id = request.GET.get('online_exam_id')
            exam_info = OnlineExam_Ans_Info.objects.filter(
                online_exam_id__exam_id__academic_year=academic_year,
                online_exam_id__exam_id__class_id=class_id,
                online_exam_id=online_exam_id,
                publish_status='Submitted',
                total_obtain_marks__gt=0)
            for online_exam in exam_info:
                online_exam.publish_status = 'Finish'
                online_exam.save()
            data['success'] = 'Save successfull'
            return JsonResponse(data)
    except Exception as e:
        logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        data['error_message'] = str(e)
        return JsonResponse(data)


class edu_student_attendence_sheet(TemplateView):
    template_name = 'edu/edu-attendence-sheet-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')

        year = Academic_Year.objects.all()
        classes = Academic_Class.objects.all()
        sec = Section_Info.objects.all()
        subject = Subject_List.objects.all()
        grp = Academic_Class_Group.objects.all()
        context = get_global_data(request)
        context['years'] = year
        context['ssss'] = classes
        context['ttt'] = sec
        context['subjects'] = subject
        context['grps'] = grp

        return render(request, self.template_name, context)


@transaction.atomic
def edu_student_attendencesheet_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    try:
        with transaction.atomic():
            check_filter = dict()
            student_filter = dict()
            month_number = request.POST.get('month_name')
            academic_year = get_object_or_404(
                Academic_Year, pk=request.POST.get('academic_year'))
            classs = get_object_or_404(
                Academic_Class, class_id=request.POST.get('class_id'))

            if request.POST.get('class_group_id'):
                class_group = get_object_or_404(
                    Academic_Class_Group, pk=request.POST.get('class_group_id'))
                check_filter['class_group_id'] = request.POST.get(
                    'class_group_id')
                student_filter['class_group_id'] = request.POST.get(
                    'class_group_id')
            else:
                class_group = None
            if request.POST.get('section_id'):
                section = get_object_or_404(
                    Section_Info, pk=request.POST.get('section_id'))
                check_filter['section_id'] = request.POST.get('section_id')
                student_filter['section_id'] = request.POST.get('section_id')
            else:
                section = None
            if request.POST.get('subject_id'):
                subject = get_object_or_404(
                    Subject_List, pk=request.POST.get('subject_id'))
                check_filter['subject_id'] = request.POST.get('subject_id')
            else:
                subject = None

            check_filter['academic_year'] = request.POST.get('academic_year')
            check_filter['month_number'] = month_number
            check_filter['class_id'] = request.POST.get('class_id')

            check = Present_sheet_info.objects.filter(**check_filter).exists()
            if check:
                data['error_message'] = 'This present sheet already exists!'
                return JsonResponse(data)
            present_sheet_info_id = fn_get_present_sheet_info_id()
            insertion = Present_sheet_info()
            insertion.present_sheet_info_id = present_sheet_info_id
            insertion.academic_year = academic_year
            insertion.month_number = month_number
            insertion.class_id = classs
            if class_group:
                insertion.class_group_id = class_group
            if section:
                insertion.section_id = section
            if subject:
                insertion.subject_id = subject
            insertion.app_user_id = request.session["app_user_id"]
            insertion.app_data_time = datetime.now()
            insertion.save()
            days = monthrange(int(academic_year.academic_year),
                              int(month_number))[1]

            student_filter['academic_year'] = request.POST.get('academic_year')
            student_filter['class_id'] = request.POST.get('class_id')
            students = Students_Info.objects.filter(**student_filter)
            for student in students:
                for day in range(1, days+1):
                    attendence = Present_sheet_dtl()
                    attendence.present_sheet_info_id = insertion
                    attendence.student_roll = student

                    df = (academic_year.academic_year) + \
                        '/'+(month_number)+'/'+str(day)
                    date_obj = datetime.strptime(df, '%Y/%m/%d').date()
                    attendence.date = date_obj
                    attendence.is_present = 0
                    attendence.app_data_time = datetime.now()
                    attendence.app_user_id = request.session["app_user_id"]
                    attendence.save()

            data['form_is_valid'] = True
            data['success_message'] = 'Added Successfully!'
            return JsonResponse(data)
    except Exception as e:
        logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        data['error_message'] = str(e)
        return JsonResponse(data)


class edu_published_result(TemplateView):
    template_name = 'edu/edu-published-result.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = StudentInfoModelForm()
        rolls = Students_Info.objects.all()
        context = get_global_data(request)
        context['form'] = form
        context['rolls'] = rolls
        return render(request, self.template_name, context)


class edu_allstudents_attendencelist(TemplateView):
    template_name = 'edu/edu-allstudents-attendencelist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        academic_year = request.GET.get('academic_year')
        month_number = request.GET.get('month_number')
        class_id = request.GET.get('class_id')
        class_group_id = request.GET.get('class_group_id')
        section_id = request.GET.get('section_id')
        subject_id = request.GET.get('subject_id')
        context = get_global_data(request)

        Filter = dict()
        if academic_year:
            Filter['academic_year'] = academic_year
        if month_number:
            Filter['month_number'] = month_number
        if class_id:
            Filter['class_id'] = class_id
        if class_group_id:
            Filter['class_group_id'] = class_group_id
        if section_id:
            Filter['section_id'] = section_id
        if subject_id:
            Filter['subject_id'] = subject_id

        present_sheet = Present_sheet_info.objects.filter(
            **Filter).order_by('-present_sheet_info_id')
        context['present_sheet'] = present_sheet
        return render(request, self.template_name, context)


def edu_published_result_filter(request):
    template_name = 'edu/edu-published-result-filter.html'
    academy = get_object_or_404(Academy_info)
    context = dict()
    academic_year = request.GET.get('academic_year')
    term_id = request.GET.get('term_id')
    class_id = request.GET.get('class_id')
    class_group_id = request.GET.get('class_group_id')
    student_roll = request.GET.get('student_roll')
    data_filter = dict()
    if academic_year and class_id:
        data_filter['academic_year'] = academic_year
        data_filter['class_id'] = class_id
        data_filter['term_id'] = term_id
    else:
        return render(request, template_name, context)
    if student_roll:
        data_filter['student_roll'] = student_roll
    if class_group_id:
        data_filter['class_group_id'] = class_group_id

    if academic_year and class_id:
        final_table = Exam_Marks_Final.objects.filter(
            **data_filter).order_by('student_roll__class_roll')

    context = get_global_data(request)
    context['final_table'] = final_table
    context['academy'] = academy
    return render(request, template_name, context)


def edu_published_result_student_roll(request):
    template_name = 'edu/edu-published-result-student_roll.html'
    context = dict()
    academic_year = request.GET.get('academic_year')
    term_id = request.GET.get('term_id')
    class_id = request.GET.get('class_id')
    student_roll = request.GET.get('student_roll')
    subject_id = request.GET.get('subject_id')
    m_position = request.GET.get('m_position')
    class_info = get_object_or_404(Academic_Class, class_id=class_id)
    if academic_year and term_id and class_id and student_roll:
        final_table = Exam_Marks_Final.objects.filter(
            academic_year=academic_year, term_id=term_id, class_id=class_id, student_roll=student_roll)
        exam_list = Store_Exam_Single_Mark.objects.filter(
            academic_year=academic_year, term_id=term_id, class_id=class_id, student_roll=student_roll)
        branch_code = final_table[0].branch_code
        institute = IdCard_form_header.objects.filter(
            branch_code=branch_code).first()
        institute.address = institute.address.split(';')

        subject_marks = exam_list.values('subject_id', 'subject_id__subject_name').annotate(total_mark=Sum(
            'total_exam_marks'), ob_mark=Sum('obtain_marks'), gpa=Sum('grade_point_average'),)
        total_mark = {'total': 0, 'obtain': 0}
        for sm in subject_marks:
            result = get_result_great(
                sm['ob_mark'], sm['total_mark'], class_info.out_of)
            total_mark['obtain'] += sm['ob_mark']
            total_mark['total'] += sm['total_mark']
            sm['subject_gpa'] = result[0]
            sm['subject_lg'] = result[1]
    else:
        final_table = Exam_Marks_Final.objects.all()

    student = get_object_or_404(Students_Info, student_roll=student_roll)
    grade_table = Result_Grade.objects.filter(
        out_of=class_info.out_of).order_by('-result_gpa')

    context = get_global_data(request)
    context['final_table'] = final_table
    context['student'] = student
    context['institute'] = institute
    context['m_position'] = m_position
    context['grade_table'] = grade_table
    context['subject_marks'] = subject_marks
    context['total_mark'] = total_mark
    return render(request, template_name, context)


def edu_published_result_subject(request):
    template_name = 'edu/edu-published-result-subject.html'
    academic_year = request.GET.get('academic_year')
    class_id = request.GET.get('class_id')
    student_roll = request.GET.get('student_roll')
    subject_id = request.GET.get('subject_id')
    term_id = request.GET.get('term_id')
    # student = get_object_or_404(Students_Info, student_roll=student_roll)
    # subject = get_object_or_404(Subject_List, subject_id=subject_id)
    institute = Academy_info.objects.first()
    exam = Store_Exam_Single_Mark.objects.filter(
        academic_year=academic_year,
        class_id=class_id, term_id=term_id,
        subject_id=subject_id,
        student_roll=student_roll)
    # exam = Exam_Single_Mark.objects.filter(academic_year=academic_year,term_id=term_id,class_id=class_id,
    #     subject_id=subject_id, student_roll=student_roll)
    # institute = get_object_or_404(Academy_info)
    # context = get_global_data(request)
    context = get_global_data(request)
    # context['exam'] = exam
    # context['student'] = student
    # context['subject'] = subject
    context['exam'] = exam
    context['institute'] = institute
    return render(request, template_name, context)


class edu_attendance_sheet(TemplateView):
    template_name = 'edu/edu-attendence-sheet.html'

    def get(self, request, id):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')

        sheets = get_object_or_404(
            Present_sheet_info, present_sheet_info_id=id)
        student_list = []
        attendances = sheets.psd_present_sheet_info_id.all()
        for sheet in attendances:
            student = dict()
            if not list(filter(lambda d: d['student_roll'] == sheet.student_roll.student_roll, student_list)):
                student['student_roll'] = sheet.student_roll.student_roll
                student['student_name'] = sheet.student_roll.student_name
                student['present_sheet_info_id'] = id
                student['presents'] = attendances.filter(
                    student_roll=sheet.student_roll.student_roll)
                student_list.append(student)

        student_list.sort(key=lambda x: (x['student_roll']), reverse=False)
        days = monthrange(int(sheets.academic_year.academic_year),
                          int(sheets.month_number))[1]
        context = get_global_data(request)
        context['sheet'] = sheets
        context['student_list'] = student_list
        context['days'] = range(1, days+1)
        return render(request, self.template_name, context)


def edu_attendance_sheet_pdf(request, id):
    def get(self, request, id):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')

    sheets = get_object_or_404(Present_sheet_info, present_sheet_info_id=id)
    data = dict()
    present_dtl = Present_sheet_dtl.objects.filter(present_sheet_info_id=id)
    students = present_dtl.values('student_roll', 'student_roll__student_name')
    student_list = []
    for student in students:
        if not list(filter(lambda d: d['student']['student_roll'] == student['student_roll'], student_list)):
            attendance = dict()
            attendance['student'] = student
            attendance['day'] = present_dtl.filter(
                present_sheet_info_id=id, student_roll=student['student_roll']).aggregate(day=Count('student_roll'))
            student_list.append(attendance)

    basic_data = {
        'academic_year': sheets.academic_year.academic_year,
        'Month': sheets.get_month_number_display(),
        'Class': sheets.class_id.class_name
    }
    if sheets.subject_id:
        basic_data['subject'] = sheets.subject_id.subject_name
    if sheets.class_group_id:
        basic_data['class_group'] = sheets.class_group_id.class_group_name
    if sheets.section_id:
        basic_data['section_id'] = sheets.section_id.section_name
    data['basic_data'] = basic_data
    data['attendance'] = student_list
    return JsonResponse(data)


@transaction.atomic
def edu_attendance_change(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    try:
        with transaction.atomic():
            sheet = get_object_or_404(
                Present_sheet_info, present_sheet_info_id=id)
            day = request.POST.get('day')
            student_roll = request.POST.get('student_roll')
            present = request.POST.get('present')
            action_date = str(sheet.academic_year.academic_year) + \
                '-'+str(sheet.month_number)+'-'+str(day)
            # date_obj=datetime.strptime(df,'%Y/%m/%d').date()
            # action_date=sheet
            if student_roll:
                present_dtl = get_object_or_404(Present_sheet_dtl,
                                                present_sheet_info_id=id,
                                                date=action_date,
                                                student_roll=student_roll)
                present_dtl.is_present = present
                present_dtl.save()
            else:
                present_dtl = Present_sheet_dtl.objects.filter(
                    present_sheet_info_id=id,
                    date=action_date).update(is_present=present)
            data['success'] = "Change"
    except Exception as e:
        logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        data['error_message'] = str(e)
        return JsonResponse(data)
    return JsonResponse(data)


# (((((((((((((((((((((((((((((((((((Libraray Rack)))))))))))))))))))))))))))))))))))

class edu_libraryrack_createlist(TemplateView):
    template_name = 'edu/edu-libraryrack-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = LibraryRackModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_libraryrack_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = LibraryRackModelForm(request.POST)
        if form.is_valid():
            rack_id = fn_get_rack_id()
            post = form.save(commit=False)
            post.rack_id = rack_id
            post.is_active = True
            post.app_user_id = request.session["app_user_id"]
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Library Rack Info Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_libraryrack_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Library_Rack, pk=id)
    template_name = 'edu/edu-libraryrack-edit.html'
    data = dict()

    if request.method == 'POST':
        form = LibraryRackModelForm(request.POST, instance=instance_data)
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
        form = LibraryRackModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


# (((((((((((((((((((((((((((((((((((Libraray Author)))))))))))))))))))))))))))))))))))

class edu_libraryauthor_createlist(TemplateView):
    template_name = 'edu/edu-libraryauthor-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = LibraryAuthorModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_libraryauthor_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = LibraryAuthorModelForm(request.POST)
        if form.is_valid():
            author_id = fn_get_author_id()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.author_id = author_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Library Author Info Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_libraryauthor_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Library_Author, pk=id)
    template_name = 'edu/edu-libraryauthor-edit.html'
    data = dict()

    if request.method == 'POST':
        form = LibraryAuthorModelForm(request.POST, instance=instance_data)
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
        form = LibraryAuthorModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


# (((((((((((((((((((((((((((((((((((Libraray Editor)))))))))))))))))))))))))))))))))))

class edu_libraryeditor_createlist(TemplateView):
    template_name = 'edu/edu-libraryeditor-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = LibraryEditorModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_libraryeditor_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = LibraryEditorModelForm(request.POST)
        if form.is_valid():
            editor_id = fn_get_editor_id()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.editor_id = editor_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Library Editor Info Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_libraryeditor_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Library_Editor, pk=id)
    template_name = 'edu/edu-libraryeditor-edit.html'
    data = dict()

    if request.method == 'POST':
        form = LibraryEditorModelForm(request.POST, instance=instance_data)
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
        form = LibraryEditorModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


# (((((((((((((((((((((((((((((((((((Libraray Books)))))))))))))))))))))))))))))))))))

class edu_librarybook_createlist(TemplateView):
    template_name = 'edu/edu-librarybook-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = LibraryBookModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_librarybook_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = LibraryBookModelForm(request.POST)
        if form.is_valid():
            book_id = fn_get_book_id()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.book_id = book_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Library Books Info Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_librarybook_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Library_Books, pk=id)
    template_name = 'edu/edu-librarybook-edit.html'
    data = dict()

    if request.method == 'POST':
        form = LibraryBookModelForm(request.POST, instance=instance_data)
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
        form = LibraryBookModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


# (((((((((((((((((((((((((((((((((((Libraray Card)))))))))))))))))))))))))))))))))))

class edu_librarycard_createlist(TemplateView):
    template_name = 'edu/edu-librarycard-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = LibraryCardModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_librarycard_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = LibraryCardModelForm(request.POST)
        if form.is_valid():
            card_number = fn_get_card_id()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.card_number = card_number
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Library Card Info Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_librarycard_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Library_Card, pk=id)
    template_name = 'edu/edu-librarycard-edit.html'
    data = dict()

    if request.method == 'POST':
        form = LibraryCardModelForm(request.POST, instance=instance_data)
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
        form = LibraryCardModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)

# (((((((((((((((((((((((Libraray Book Issue)))))))))))))))))))))))))))


class edu_librarybookissue_createlist(TemplateView):
    template_name = 'edu/edu-librarybookissue-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = LibraryBookIssueModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_librarybookissue_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = LibraryBookIssueModelForm(request.POST)
        if form.is_valid():
            issue_id = fn_get_bissue_id()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.issue_id = issue_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Library Book Issue Info Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_librarybookissue_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Library_Book_Issue, pk=id)
    template_name = 'edu/edu-librarybookissue-edit.html'
    data = dict()

    if request.method == 'POST':
        form = LibraryBookIssueModelForm(request.POST, instance=instance_data)
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
        form = LibraryBookIssueModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


# (((((((((((((((((((((((Libraray Book Request))))))))))))))))))))))))))

class edu_librarybookrequest_createlist(TemplateView):
    template_name = 'edu/edu-librarybookrequest-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = LibraryBookRequestModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_librarybookrequest_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = LibraryBookRequestModelForm(request.POST)
        if form.is_valid():
            request_id = fn_get_request_id()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.request_id = request_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Library Book Request Info Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_librarybookrequest_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Library_Book_Request, pk=id)
    template_name = 'edu/edu-librarybookrequest-edit.html'
    data = dict()

    if request.method == 'POST':
        form = LibraryBookRequestModelForm(
            request.POST, instance=instance_data)
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
        form = LibraryBookRequestModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


# (((((((((((((((((((((((((((Class Room))))))))))))))))))))))))))))))))

class edu_classroom_createlist(TemplateView):
    template_name = 'edu/edu-classroom-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = ClassRoomModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_classroom_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = ClassRoomModelForm(request.POST)
        if form.is_valid():
            room_id = fn_get_room_id()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.room_id = room_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Class Room Info Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_classroom_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Class_Room, pk=id)
    template_name = 'edu/edu-classroom-edit.html'
    data = dict()

    if request.method == 'POST':
        form = ClassRoomModelForm(request.POST, instance=instance_data)
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
        form = ClassRoomModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


# (((((((((((((((((((((((((Class Routine))))))))))))))))))))))))))))

class edu_classroutine_createlist(TemplateView):
    template_name = 'edu/edu-classroutine-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = ClassRoutineModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_classroutine_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = ClassRoutineModelForm(request.POST)
        if form.is_valid():
            routine_id = fn_get_routine_id()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.routine_id = routine_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Class Routine Info Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_classroutine_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Class_Routine, pk=id)
    template_name = 'edu/edu-classroutine-edit.html'
    data = dict()

    if request.method == 'POST':
        form = ClassRoutineModelForm(request.POST, instance=instance_data)
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
        form = ClassRoutineModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


# ((((((((((((((((((((((((Class Routine Details))))))))))))))))))))))

class edu_routinedetails_createlist(TemplateView):
    template_name = 'edu/edu-routinedetails-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = ClassRoutineDetailsModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_routinedetails_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = ClassRoutineDetailsModelForm(request.POST)
        if form.is_valid():
            routines = []
            select_routine = Class_Routine.objects.filter(
                routine_id=request.POST.get('routine_id'))
            for routine in select_routine:
                routines.append(routine)
            # print(datetime.strptime(str(routines[0].start_date),'%Y-%m-%d').date())
            get_all_routing = Class_Routine.objects.filter(Q(start_date__lte=str(
                routines[0].end_date), end_date__gte=str(routines[0].start_date)))
            for r in get_all_routing:
                if not r in routines:
                    routines.append(r)
            for routine in routines:
                # Check teacher is free
                check_t = Class_Routine_Details.objects.filter(Q(start_time__lte=request.POST.get('end_time'), end_time__gte=request.POST.get('start_time')),
                                                               routine_id=routine.routine_id,
                                                               teacher_id=request.POST.get(
                                                                   'teacher_id'),
                                                               day__in=request.POST.getlist('day')).exists()
                if check_t:
                    data['error_message'] = 'This teacher is busy for other class'
                    return JsonResponse(data)
                # Check Room is free
                check_r = Class_Routine_Details.objects.filter(Q(start_time__lte=request.POST.get('end_time'), end_time__gte=request.POST.get('start_time')),
                                                               routine_id=routine.routine_id,
                                                               room_id=request.POST.get(
                                                                   'room_id'),
                                                               day__in=request.POST.getlist('day')).exists()
                if check_r:
                    data['error_message'] = 'This class room is busy for other class'
                    return JsonResponse(data)
                # Check Students is free
                students_ab = dict()
                students_ab['class_id'] = request.POST.get('class_id')
                if request.POST.get('class_group_id'):
                    students_ab['class_group_id'] = request.POST.get(
                        'class_group_id')
                else:
                    students_ab['class_group_id'] = None
                if request.POST.get('shift_id'):
                    students_ab['shift_id'] = request.POST.get('shift_id')
                else:
                    students_ab['shift_id'] = None
                check_s = Class_Routine_Details.objects.filter(Q(start_time__lte=request.POST.get('end_time'), end_time__gte=request.POST.get('start_time')),
                                                               routine_id=routine.routine_id,
                                                               day__in=request.POST.getlist(
                                                                   'day'),
                                                               **students_ab).exists()
                if check_s:
                    data['error_message'] = 'This class students is busy for other class'
                    return JsonResponse(data)
            for d in request.POST.getlist('day'):
                routine_details_id = fn_get_routine_dtl_id()
                post = form.save(commit=False)
                post.day = d
                post.app_user_id = request.session["app_user_id"]
                post.routine_details_id = routine_details_id
                post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Class Routine Details Info Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_routinedetails_list(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    template_name = 'edu/edu-routinedetails-list.html'
    data = dict()
    routine_id = request.GET.get('routine_id')
    academic_year = request.GET.get('academic_year')
    class_id = request.GET.get('class_id')
    subject_id = request.GET.get('subject_id')
    teacher_id = request.GET.get('teacher_id')
    room_id = request.GET.get('room_id')
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    day = request.GET.get('day')
    class_group_id = request.GET.get('class_group_id')
    shift_id = request.GET.get('shift_id')
    section_id = request.GET.get('section_id')

    data_set = dict()
    if routine_id:
        data_set['routine_id'] = routine_id
    if academic_year:
        data_set['academic_year'] = academic_year
    if class_id:
        data_set['class_id'] = class_id
    if subject_id:
        data_set['subject_id'] = subject_id
    if teacher_id:
        data_set['teacher_id'] = teacher_id
    if room_id:
        data_set['room_id'] = room_id
    if day:
        data_set['day__in'] = day.split(',')
    if class_group_id:
        data_set['class_group_id'] = class_group_id
    if shift_id:
        data_set['shift_id'] = shift_id
    if section_id:
        data_set['section_id'] = section_id
    time_q = dict()
    if start_time and end_time:
        time_q['start_time__lte'] = end_time
        time_q['end_time__gte'] = start_time
    routines = Class_Routine_Details.objects.filter(
        Q(**time_q), **data_set).order_by('class_id', '-app_data_time')
    context = get_global_data(request)
    context['routines'] = routines
    data['html_form'] = render_to_string(
        template_name, context, request=request)
    return JsonResponse(data)


def edu_routinedetails_delete(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['error_message'] = "Something wrong!"
    if request.method == 'POST':
        routine = get_object_or_404(
            Class_Routine_Details, routine_details_id=id)
        routine.delete()
        data['success_message'] = "Your record has been deleted."
    return JsonResponse(data)
# ((((((((((((((((((((( Routine Query ))))))))))))))))))))))))


class edu_routine_query(TemplateView):
    template_name = 'edu/edu-routine-query.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = ClassRoutineDetailsModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_routine_query_view(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    template_name = 'edu/edu-routine-query-view.html'
    data = dict()
    context = get_global_data(request)
    routine_view = request.GET.get('routine_view')
    routines = []
    periods = []
    title_name = ""
    if routine_view == '1' and request.GET.get('teacher_id'):
        routines = Class_Routine_Details.objects.filter(routine_id=request.GET.get(
            'routine_id'), teacher_id=request.GET.get('teacher_id')).order_by('start_time')
        title_name = routines[0].teacher_id
        for routine in routines:
            t = dict()
            t['start_time'] = routine.start_time
            t['end_time'] = routine.end_time
            if not t in periods:
                periods.append(t)
    if routine_view == '2' and request.GET.get('class_id'):
        filter_data = dict()
        filter_data['class_id'] = request.GET.get('class_id')
        if request.GET.get('class_group_id'):
            filter_data['class_group_id'] = request.GET.get('class_group_id')
        if request.GET.get('shift_id'):
            filter_data['shift_id'] = request.GET.get('shift_id')
        class_info = Academic_Class.objects.filter(
            class_id=request.GET.get('class_id'))
        # Get Section Info
        if request.GET.get('section_id'):
            sections = Section_Info.objects.filter(
                section_id=request.GET.get('section_id'))
        else:
            sections = class_info[0].sec_class_id.all
        title_name = class_info[0].class_name
        context['sections'] = sections
        routines = Class_Routine_Details.objects.filter(
            routine_id=request.GET.get('routine_id'), **filter_data).order_by('start_time')
        for routine in routines:
            t = dict()
            t['start_time'] = routine.start_time
            t['end_time'] = routine.end_time
            if not t in periods:
                periods.append(t)
    if routine_view == '3' and request.GET.getlist('day'):
        routines = Class_Routine_Details.objects.filter(routine_id=request.GET.get(
            'routine_id'), day__in=request.GET.getlist('day')).order_by('start_time', 'class_id')
        classs = []
        for routine in routines:
            single_class = dict()
            single_class['class_id'] = routine.class_id.class_id
            single_class['class_name'] = routine.class_id.class_name
            if not single_class in classs:
                classs.append(single_class)
            t = dict()
            t['start_time'] = routine.start_time
            t['end_time'] = routine.end_time
            if not t in periods:
                periods.append(t)
        context['search_days'] = request.GET.getlist('day')
        context['classs'] = classs
    # print(datetime.now().strftime("%A"))
    context['routine_view'] = routine_view
    context['title_name'] = title_name
    context['routines'] = routines
    context['periods'] = periods
    context['days'] = range(1, 8)
    data['html_form'] = render_to_string(
        template_name, context, request=request)
    return JsonResponse(data)


def edu_routine_query_pdf(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    pdf = FPDF('L', 'mm', 'A4')

    routine_view = request.GET.get('routine_view')
    if routine_view == '1':
        teachers = Teacher.objects.all()
        for teacher in teachers:
            routines = Class_Routine_Details.objects.filter(routine_id=request.GET.get(
                'routine_id'), teacher_id=teacher.employee_id.employee_id).order_by('start_time')
            periods = []

            title_name = str(teacher.employee_id)
            for routine in routines:
                t = dict()
                t['start_time'] = routine.start_time
                t['end_time'] = routine.end_time
                if not t in periods:
                    periods.append(t)

            pdf.add_page()
            pdf.set_font('helvetica', 'B', 16)
            pdf.cell(277, 10, 'Class routine for ' +
                     str(title_name), border=False, align='C', ln=1)
            pdf.set_font('helvetica', '', 14-len(periods))
            pdf.cell(int(277/(len(periods)+1)), 10,
                     'Date/time', border=True, align='L', ln=0)
            for index, p in enumerate(periods, start=1):
                len_period = 0
                if index == len(periods):
                    len_period = 1
                pdf.cell(int(277/(len(periods)+1)), 10, str(p['start_time'])+" to "+str(
                    p['end_time']), border=True, align='C', ln=len_period)

            days = {1: 'Saturday', 2: 'Sunday', 3: 'Monday',
                    4: 'Tuesday', 5: 'Wednesday', 6: 'Thursday', 7: 'Friday'}
            for d in days:
                pdf.cell(int(277/(len(periods)+1)), 5,
                         days[d], border=True, align='L', ln=0)
                for index, p in enumerate(periods, start=1):
                    r_data = ""
                    for r in routines:
                        if r.day == d and r.start_time == p['start_time'] and r.end_time == p['end_time']:
                            r_data += str(r.class_id)+"-" + \
                                str(r.room_id)+" "+str(r.subject_id)
                            if r.subject_id.subject_code:
                                r_data += "-"+str(r.subject_id.subject_code)
                    pdf.cell(int(277/(len(periods)+1)), 5,
                             r_data, border=True, align='C', ln=0)
                pdf.ln()
    if routine_view == '2':
        Classs = Academic_Class.objects.all()
        for ac_class in Classs:
            routines = Class_Routine_Details.objects.filter(routine_id=request.GET.get(
                'routine_id'), class_id=ac_class.class_id).order_by('start_time')
            if routines.count():
                periods = []
                title_name = str(ac_class)
                for routine in routines:
                    t = dict()
                    t['start_time'] = routine.start_time
                    t['end_time'] = routine.end_time
                    if not t in periods:
                        periods.append(t)

                pdf.add_page()
                pdf.set_font('helvetica', 'B', 16)
                pdf.cell(277, 10, 'Class routine for ' +
                         str(title_name), border=False, align='C', ln=1)
                pdf.set_font('helvetica', '', 14-len(periods))
                pdf.cell(int(277/(len(periods)+1)), 10,
                         'Date/time', border=True, align='L', ln=0)
                for index, p in enumerate(periods, start=1):
                    len_period = 0
                    if index == len(periods):
                        len_period = 1
                    pdf.cell(int(277/(len(periods)+1)), 10, str(p['start_time'])+" to "+str(
                        p['end_time']), border=True, align='C', ln=len_period)

                days = {1: 'Saturday', 2: 'Sunday', 3: 'Monday',
                        4: 'Tuesday', 5: 'Wednesday', 6: 'Thursday', 7: 'Friday'}
                for d in days:
                    pdf.cell(int(277/(len(periods)+1)), 5,
                             days[d], border=True, align='L', ln=0)
                    for index, p in enumerate(periods, start=1):
                        r_data = ""
                        for r in routines:
                            if r.day == d and r.start_time == p['start_time'] and r.end_time == p['end_time']:
                                r_data += str(r.room_id)+" " + \
                                    str(r.subject_id)[0:3]
                                if r.subject_id.subject_code:
                                    r_data += "-" + \
                                        str(r.subject_id.subject_code)
                                r_data += " ("+str(r.teacher_id)[0:3]+")"
                        pdf.cell(int(277/(len(periods)+1)), 5,
                                 r_data, border=True, align='C', ln=0)
                    pdf.ln()

    pdf.output('media/PDF/'+str(request.session["app_user_id"])+'.pdf', 'F')
    if pdf:
        # get the filename of desired excel file
        file_name = get_random_string(8, allowed_chars='0123456789')+".pdf"
        # get the path of desired excel file
        path_to_file = 'media/PDF/'+str(request.session["app_user_id"])+'.pdf'
        path = open(path_to_file, 'rb')
        mime_type, _ = mimetypes.guess_type(path_to_file)
        response = HttpResponse(path, content_type=mime_type)
        response['Content-Disposition'] = 'attachment; filename=%s' % file_name
        return response
# ((((((((((((((((((((( Teacher ))))))))))))))))))))))))


class edu_teacher_createlist(TemplateView):
    template_name = 'edu/edu-teacher-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = TeacherModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_teacherchoice_searchstudent(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    template_name = 'edu/edu-teacherchoice-searchstudent.html'
    context = get_global_data(request)
    data = dict()
    if request.method == 'POST':
        datafilter = dict()
        academic_year = request.POST.get('academic_year')
        class_id = request.POST.get('class_id')
        class_group_id = request.POST.get('class_group_id')
        student_roll = request.POST.get('student_roll')
        teacher_id = request.POST.get('teacher_id')
        if academic_year:
            datafilter['academic_year'] = academic_year
        if class_id:
            datafilter['class_id'] = class_id
        if class_group_id:
            datafilter['class_group_id'] = class_group_id
        if student_roll:
            datafilter['student_roll'] = student_roll
        students = Students_Info.objects.filter(**datafilter)
        context['students'] = students
        context['datafilter'] = datafilter
        context['teacher_id'] = teacher_id
    data['html_form'] = render_to_string(
        template_name, context, request=request)
    return JsonResponse(data)


@transaction.atomic
def edu_studentschoice_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = {}
    if request.method == 'POST':
        try:
            with transaction.atomic():
                class_group_id = ""
                branch_code=request.POST.get('branch_code')
                academic_year = get_object_or_404(
                    Academic_Year, pk=request.POST.get('academic_year'))
                teacher = get_object_or_404(
                    Teacher, pk=request.POST.get('teacher_id'))
                class_id = get_object_or_404(
                    Academic_Class, class_id=request.POST.get('class_id'))
                if request.POST.get('class_group_id'):
                    class_group_id = get_object_or_404(
                        Academic_Class_Group, class_group_id=request.POST.get('class_group_id'))
                students = request.POST.getlist('student_roll[]')
                for student_data in students:
                    student = json.loads(student_data)
                    student_status = student['student_status']
                    student_roll = student['student_roll']

                    if Mapping_Guide_Teacher.objects.filter(academic_year=request.POST.get('academic_year'), student_roll=student_roll, teacher_id=teacher.teacher_id).exists():
                        choice = Mapping_Guide_Teacher.objects.get(academic_year=request.POST.get(
                            'academic_year'), student_roll=student_roll, teacher_id=teacher.teacher_id)
                        choice.student_status = student_status
                        choice.app_user_id = request.session["app_user_id"]
                        choice.save()
                    else:
                        if student_status == 'A':
                            choice = Mapping_Guide_Teacher()
                            choice.class_id = class_id
                            choice.academic_year = academic_year
                            if class_group_id:
                                choice.class_group_id = class_group_id
                            choice.student_roll = get_object_or_404(
                                Students_Info, student_roll=student_roll)
                            choice.teacher_id = teacher
                            choice.student_status = student_status
                            choice.app_user_id = request.session["app_user_id"]
                            choice.save()
                data['success_message'] = 'Students Choice Info added Successfully'
        except Exception as e:
            logger.error("Error in Mapping Guide Teacher {} \nType: {} \nError:{}".format(
                sys.exc_info()[-1], type(e).__name__, str(e)))
            data['error_message'] = 'Error '+str(e)+' Mapping Guide Teacher!'
    return JsonResponse(data)


# ((((((((((((((((((((Student Registration Form)))))))))))))))))))))

class edu_quick_admit_createlist(TemplateView):
    template_name = 'edu/edu-quick-admit-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = StudentInfoModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_registrationinfo_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        if request.POST.get('academic_year'):
            academic_year = get_object_or_404(
                Academic_Year, pk=request.POST.get('academic_year'))
        else:
            data['error_message'] = 'Academic year is required.'
            return JsonResponse(data)
        if request.POST.get('class_id'):
            class_id = get_object_or_404(
                Academic_Class, class_id=request.POST.get('class_id'))
        else:
            data['error_message'] = 'Class name is required.'
            return JsonResponse(data)
        if request.POST.get('class_group_id'):
            class_group_id = get_object_or_404(
                Academic_Class_Group, class_group_id=request.POST.get('class_group_id'))
        else:
            class_group_id = None

        if request.POST.get('section_id'):
            section_id = get_object_or_404(
                Section_Info, section_id=request.POST.get('section_id'))
        else:
            section_id = None
        if request.POST.get('catagory_id'):
            catagory_id = get_object_or_404(
                Catagory_info, catagory_id=request.POST.get('catagory_id'))
        else:
            data['error_message'] = 'Student category is required.'
            return JsonResponse(data)
        if request.POST.get('session_id'):
            session_id = get_object_or_404(
                Session, session_id=request.POST.get('session_id'))
        else:
            session_id = None
        row_no = int(request.POST.get('row_no'))

        branch_code = request.POST.get('branch_code')
        if not branch_code or branch_code is None:
            branch_code = request.session['branch_code']
        process_date=''
        for i in range(1, row_no+1):
            addmission_date = request.POST.get('admission'+str(i))
            if i == 1:
                process_date=addmission_date
            class_roll = request.POST.get('class_roll'+str(i))
            student_name = request.POST.get('student_name'+str(i))
            f_name = request.POST.get('f_name'+str(i))
            m_name = request.POST.get('m_name'+str(i))
            mobile_no = request.POST.get('mobile_no'+str(i))
            gender = request.POST.get('gender'+str(i))
            birthday = request.POST.get('birthday'+str(i))
            if len(addmission_date) > 0 and len(student_name) > 0 and len(f_name) > 0 and len(m_name) > 0 and len(mobile_no) > 0 and len(birthday):
                student_roll = fn_gen_student_id(
                    addmission_date[:4], branch_code, class_id.class_id)
                if addmission_date and birthday:
                    add_date = datetime.strptime(
                        addmission_date, '%Y-%m-%d').date()
                    birth_day = datetime.strptime(birthday, '%Y-%m-%d').date()
                    post = Students_Info()
                    post.student_roll = student_roll
                    post.academic_year = academic_year
                    post.class_id = class_id
                    post.class_group_id = class_group_id
                    post.section_id = section_id
                    post.catagory_id = catagory_id
                    post.session_id = session_id
                    post.class_roll = class_roll
                    post.student_name = student_name
                    post.student_father_name = f_name
                    post.student_mother_name = m_name
                    post.student_phone = mobile_no
                    post.student_gender = gender
                    post.student_joining_date = add_date
                    post.student_date_of_birth = birth_day
                    post.branch_code = int(branch_code)
                    post.app_user_id = request.session["app_user_id"]
                    post.app_data_time = timezone.now()
                    post.save()
                else:
                    data['error_message'] = 'Date Field is Required!'
        proc_data=dict()
        proc_data["class_id"] = request.POST.get('class_id')
        proc_data["branch_code"] = branch_code
        process_id = fn_get_fees_processing_id(branch_code)
        proc_data["process_id"] = process_id
        proc_data["academic_year"] = post.academic_year.academic_year
        if class_group_id:
            proc_data["class_group_id"] = class_group_id.class_group_id
        else:
            proc_data["class_group_id"] = None
        if section_id:
            proc_data["section_id"] = section_id.section_id
        else:
            proc_data["section_id"] = None

        proc_data["process_date"] = process_date
        proc_data["app_user_id"] = request.session["app_user_id"]
        print(proc_data)

        status, error_message = fn_fees_processing_thread(proc_data)
        print(status)
        data['form_is_valid'] = True
        data['success_message'] = 'Student Short Info Added Successfully!'
    else:
        data['error_message'] = 'Something Went Wrong!'
    return JsonResponse(data)


class edu_subjectchoice_createlist(TemplateView):
    template_name = 'edu/edu-subjectchoice-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = StudentInfoModelForm()
        students = Students_Info.objects.all()
        context = get_global_data(request)
        context['form'] = form
        context['students'] = students
        return render(request, self.template_name, context)


def edu_subjectchoice_searchstudent(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    template_name = 'edu/edu-subjectchoice-searchstudent.html'
    context = get_global_data(request)
    data = dict()
    if request.method == 'POST':
        datafilter = dict()
        subfilter = dict()
        branch_code = request.POST.get('branch_code')
        academic_year = request.POST.get('academic_year')
        class_id = request.POST.get('class_id')
        class_group_id = request.POST.get('class_group_id')
        session_id = request.POST.get('session_id')
        student_roll = request.POST.get('student_roll')
        if academic_year:
            datafilter['academic_year'] = academic_year
            datafilter['branch_code'] = branch_code
        if class_id:
            datafilter['class_id'] = class_id
            subfilter['class_id'] = class_id
        if class_group_id:
            datafilter['class_group_id'] = class_group_id
            subfilter['class_group_id'] = class_group_id
        else:
            subfilter['class_group_id'] = None
        if session_id:
            datafilter['session_id'] = session_id
        if student_roll:
            datafilter['student_roll'] = student_roll
        students = Students_Info.objects.filter(
            **datafilter).order_by('student_roll')
        context['students'] = students
        subjects = Subject_List.objects.filter(
            **subfilter).order_by('subject_name')
        context['subjects'] = subjects
    data['html_form'] = render_to_string(
        template_name, context, request=request)
    return JsonResponse(data)


@transaction.atomic
def edu_subchoice_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = {}
    if request.method == 'POST':
        try:
            with transaction.atomic():
                class_group_id = ""
                session_id = ""
                branch_code = request.POST.get('branch_code')
                academic_year = get_object_or_404(
                    Academic_Year, pk=request.POST.get('academic_year'))
                class_id = get_object_or_404(
                    Academic_Class, class_id=request.POST.get('class_id'))
                if request.POST.get('class_group_id'):
                    class_group_id = get_object_or_404(
                        Academic_Class_Group, class_group_id=request.POST.get('class_group_id'))
                if request.POST.get('session_id'):
                    session_id = get_object_or_404(
                        Session, session_id=request.POST.get('session_id'))

                subjects = request.POST.getlist('subjects[]')
                students = request.POST.getlist('student_roll[]')
                for student_roll in students:
                    choice_filter=dict()
                    choice_filter['academic_year']=request.POST.get('academic_year')
                    choice_filter['class_id']=class_id.class_id
                    choice_filter['student_roll']=student_roll
                    if request.POST.get('class_group_id'):
                        choice_filter['class_group_id']=request.POST.get('class_group_id')
                    Subject_Choice.objects.filter(**choice_filter).delete()
                    for subject in subjects:
                        subject = json.loads(subject)
                        subject_id = subject['subject_id']
                        subject_info = get_object_or_404(
                            Subject_List, subject_id=subject_id)
                        if branch_code:
                            choice = Subject_Choice()
                            choice.branch_code = branch_code
                            choice.class_id = class_id
                            choice.academic_year = academic_year
                            if class_group_id:
                                choice.class_group_id = class_group_id
                            if session_id:
                                choice.session_id = session_id
                            choice.student_roll = get_object_or_404(
                                Students_Info, student_roll=student_roll)
                            choice.subject_id = subject_info
                            if subject['is_main']:
                                main_cat = Subject_Category.objects.filter(
                                    Q(category_name='Main') | Q(category_name='Compulsory')).first()
                                choice.category_id = main_cat
                            else:
                                choice.category_id = subject_info.category_id

                            choice.app_user_id = request.session["app_user_id"]
                            choice.save()
                data['success_message'] = 'Subject Choice Info added Successfully'
        except Exception as e:
            logger.error("Error in Subject Choice {} \nType: {} \nError:{}".format(
                sys.exc_info()[-1], type(e).__name__, str(e)))
            data['error_message'] = 'Error '+str(e)+' Subject Choice!'
    return JsonResponse(data)


class edu_choices_subjectlist(TemplateView):
    template_name = 'edu/edu-choices-subjectlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = StudentInfoModelForm()
        students = Students_Info.objects.all()
        context = get_global_data(request)
        context['form'] = form
        context['students'] = students
        return render(request, self.template_name, context)


def edu_choicesubject_edit(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    template_name = 'edu/edu-choicesubject-edit.html'
    data = dict()
    if request.method == 'POST':
        # print(request.POST.getlist('subject[]'))
        student_roll = get_object_or_404(
            Students_Info, student_roll=request.POST.get('student_roll'))
        if request.POST.get('class_id'):
            class_id = get_object_or_404(
                Academic_Class, class_id=request.POST.get('class_id'))
        if request.POST.get('academic_year'):
            academic_year = get_object_or_404(
                Academic_Year, pk=request.POST.get('academic_year'))
        if request.POST.get('class_group_id'):
            class_group_id = get_object_or_404(
                Academic_Class_Group, class_group_id=request.POST.get('class_group_id'))
        else:
            class_group_id = None
        if request.POST.get('session_id'):
            session_id = get_object_or_404(
                Session, session_id=request.POST.get('session_id'))
        else:
            session_id = None

        for i in range(0, int(request.POST.get('total_subject'))):
            subject = request.POST.getlist("subject["+str(i)+"][]")

            if subject[1] == '1':
                check = Subject_Choice.objects.filter(
                    student_roll=student_roll.student_roll, subject_id=subject[0]).exists()
                subject_info = get_object_or_404(
                    Subject_List, subject_id=subject[0])
                if not check:
                    choice = Subject_Choice()
                    choice.class_id = class_id
                    choice.academic_year = academic_year
                    if class_group_id:
                        choice.class_group_id = class_group_id
                    if session_id:
                        choice.session_id = session_id
                    choice.student_roll = student_roll
                    choice.subject_id = subject_info
                    if subject[2] == '1':
                        main_cat = get_object_or_404(
                            Subject_Category, category_name='Main')
                        choice.category_id = main_cat
                    else:
                        choice.category_id = subject_info.category_id
                    choice.app_user_id = request.session["app_user_id"]
                    choice.save()
                else:
                    choice = Subject_Choice.objects.get(
                        student_roll=student_roll.student_roll, subject_id=subject[0])
                    if subject[2] == '1':
                        main_cat = get_object_or_404(
                            Subject_Category, category_name='Main')
                        choice.category_id = main_cat
                    else:
                        choice.category_id = subject_info.category_id
                    choice.app_user_id = request.session["app_user_id"]
                    choice.save()
            else:
                check = Subject_Choice.objects.filter(
                    student_roll=student_roll.student_roll, subject_id=subject[0]).exists()
                if check:
                    Subject_Choice.objects.get(
                        student_roll=student_roll.student_roll, subject_id=subject[0]).delete()
        data['success_message'] = 'Subject Choice Info Update Successfully'
    else:
        student = get_object_or_404(
            Students_Info, student_roll=request.GET.get('student_roll'))
        class_id = request.GET.get('class_id')
        subjects = Subject_List.objects.filter(class_id=class_id)
        context = get_global_data(request)
        context['subjects'] = subjects
        context['student'] = student
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


def edu_choicesubject_view(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    template_name = 'edu/edu-choices-subjectlist-html.html'
    data = dict()
    if request.method == 'POST':
        datafilter = dict()
        academic_year = request.POST.get('academic_year')
        class_id = request.POST.get('class_id')
        class_group_id = request.POST.get('class_group_id')
        session_id = request.POST.get('session_id')
        student_roll = request.POST.get('student_roll')
        if academic_year:
            datafilter['academic_year'] = academic_year
        if class_id:
            datafilter['class_id'] = class_id
        if class_group_id:
            datafilter['class_group_id'] = class_group_id
        if session_id:
            datafilter['session_id'] = session_id
        if student_roll:
            datafilter['student_roll'] = student_roll
        choice_data = Subject_Choice.objects.filter(**datafilter)
        students = []
        for D in choice_data:
            student = dict()
            subject = dict()
            check = list(
                filter(lambda s: s['student_roll'] == D.student_roll.student_roll, students))
            if check:
                subject_data = check[0]['subjects']
                subject['subject_id'] = D.subject_id.subject_id
                subject['subject_name'] = D.subject_id.subject_name
                subject_data.append(subject)
            else:
                student['student_roll'] = D.student_roll.student_roll
                student['student_name'] = D.student_roll.student_name
                # student['class_id']=D.class_id.class_id
                # student['class_name']=D.class_id.class_name
                subject['subject_id'] = D.subject_id.subject_id
                subject['subject_name'] = D.subject_id.subject_name
                student['subjects'] = [subject]
                students.append(student)
        data = dict()
        context = get_global_data(request)
        context['data'] = students
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


class edu_quick_admit_filterlist(TemplateView):
    template_name = 'edu/edu-quick-admit-filterlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = StudentInfoModelForm()
        students = Students_Info.objects.all()
        context = get_global_data(request)
        context['form'] = form
        context['students'] = students
        return render(request, self.template_name, context)


def edu_quick_admit_editinsert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    branch_code = request.session['branch_code']
    app_user_id = request.session["app_user_id"]
    if request.method == 'POST':
        if request.POST.get('academic_year'):
            academic_year = get_object_or_404(
                Academic_Year, pk=request.POST.get('academic_year'))
        else:
            data['error_message'] = 'Academic year is required.'
            return JsonResponse(data)
        if request.POST.get('class_id'):
            class_id = get_object_or_404(
                Academic_Class, class_id=request.POST.get('class_id'))
        else:
            data['error_message'] = 'Class name is required.'
            return JsonResponse(data)
        if request.POST.get('class_group_id'):
            class_group_id = get_object_or_404(
                Academic_Class_Group, class_group_id=request.POST.get('class_group_id'))
        else:
            class_group_id = None

        if request.POST.get('section_id'):
            section_id = get_object_or_404(
                Section_Info, section_id=request.POST.get('section_id'))
        else:
            section_id = None

        if request.POST.get('catagory_id'):
            catagory_id = get_object_or_404(
                Catagory_info, catagory_id=request.POST.get('catagory_id'))
        else:
            data['error_message'] = 'Student category is required.'
            return JsonResponse(data)
        if request.POST.get('session_id'):
            session_id = get_object_or_404(
                Session, session_id=request.POST.get('session_id'))
        else:
            session_id = None
        row_no = int(request.POST.get('row_number'))

        for i in range(0, row_no-1):
            student_roll = request.POST.get('student_roll'+str(i))
            class_roll = request.POST.get('class_roll'+str(i))
            student_reg = request.POST.get('student_reg'+str(i))
            student_name = request.POST.get('student_name'+str(i))
            f_name = request.POST.get('f_name'+str(i))
            m_name = request.POST.get('m_name'+str(i))
            mobile_no = request.POST.get('mobile_no'+str(i))
            gender = request.POST.get('gender'+str(i))
            addmission_date = request.POST.get('admission'+str(i))
            birthday = request.POST.get('birthday'+str(i))

            if addmission_date and birthday:
                add_date = datetime.strptime(
                    addmission_date, '%Y-%m-%d').date()
                birth_day = datetime.strptime(birthday, '%Y-%m-%d').date()
                post = get_object_or_404(
                    Students_Info, student_roll=student_roll)
                post.student_roll = student_roll
                post.academic_year = academic_year
                post.class_id = class_id
                post.class_group_id = class_group_id
                post.section_id = section_id
                post.catagory_id = catagory_id
                post.session_id = session_id
                post.class_roll = class_roll
                post.student_reg = student_reg
                post.student_name = student_name
                post.student_father_name = f_name
                post.student_mother_name = m_name
                post.student_phone = mobile_no
                post.student_gender = gender
                post.student_joining_date = add_date
                post.student_date_of_birth = birth_day
                post.branch_code = branch_code
                post.app_user_id = app_user_id
                post.app_data_time = timezone.now()
                post.save()
            else:
                data['error_message'] = 'Date field required'
        data['form_is_valid'] = True
        data['success_message'] = 'Student Short Info Update Successfully!'
    else:
        data['error_message'] = 'Something went wrong'
    return JsonResponse(data)


class edu_student_attendence_addstudent(TemplateView):
    template_name = 'edu/edu-attendence-addstudent.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')

        year = Academic_Year.objects.all()
        classes = Academic_Class.objects.all()
        context = get_global_data(request)
        context['years'] = year
        context['ssss'] = classes

        return render(request, self.template_name, context)


@transaction.atomic
def edu_attendence_addstudent_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = {}
    if request.method == 'POST':
        try:
            with transaction.atomic():
                academic_year = get_object_or_404(
                    Academic_Year, pk=request.POST.get('academic_year'))
                class_id = get_object_or_404(
                    Academic_Class, class_id=request.POST.get('class_id'))
                student_info = get_object_or_404(
                    Students_Info, student_roll=request.POST.get('student_roll'))
                atten_sheet = Present_sheet_info.objects.filter(
                    academic_year=academic_year.pk, class_id=class_id.class_id)
                for sheet in atten_sheet:
                    if sheet.class_group_id and sheet.class_group_id != student_info.class_group_id:
                        continue
                    if sheet.section_id and sheet.section_id != student_info.section_id:
                        continue
                    days = monthrange(
                        int(academic_year.academic_year), sheet.month_number)[1]
                    for d in range(1, days+1):
                        df = (academic_year.academic_year)+'/' + \
                            str(sheet.month_number)+'/'+str(d)
                        date_obj = datetime.strptime(df, '%Y/%m/%d').date()
                        check = Present_sheet_dtl.objects.filter(
                            present_sheet_info_id=sheet.present_sheet_info_id, date=date_obj, student_roll=student_info.student_roll).exists()
                        if check:
                            pass
                        else:
                            attendence = Present_sheet_dtl()
                            attendence.present_sheet_info_id = sheet
                            attendence.student_roll = student_info
                            attendence.date = date_obj
                            attendence.is_present = 0
                            attendence.app_data_time = datetime.now()
                            attendence.app_user_id = request.session["app_user_id"]
                            attendence.save()
                data['success_message'] = 'Student added Successfully'
        except Exception as e:
            logger.error("Error in Add student in pressent sheet {} \nType: {} \nError:{}".format(
                sys.exc_info()[-1], type(e).__name__, str(e)))
            data['error_message'] = 'Error ' + \
                str(e)+'  Add student in pressent sheet!'
    return JsonResponse(data)


class edu_attendance_access_createlist(TemplateView):
    template_name = 'edu/edu-attendence-access-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')

        year = Academic_Year.objects.all()
        classes = Academic_Class.objects.all()
        sec = Section_Info.objects.all()
        subject = Subject_List.objects.all()
        grp = Academic_Class_Group.objects.all()
        teachers = Teacher.objects.all()
        context = get_global_data(request)
        context['years'] = year
        context['ssss'] = classes
        context['ttt'] = sec
        context['subjects'] = subject
        context['grps'] = grp
        context['teachers'] = teachers

        return render(request, self.template_name, context)


class edu_attendance_list_modifierview(TemplateView):
    template_name = 'edu/edu-attendance-list-modifierview.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        academic_year = request.GET.get('academic_year')
        month_number = request.GET.get('month_number')
        class_id = request.GET.get('class_id')
        class_group_id = request.GET.get('class_group_id')
        section_id = request.GET.get('section_id')
        subject_id = request.GET.get('subject_id')
        context = get_global_data(request)

        Filter = dict()
        if academic_year:
            Filter['academic_year'] = academic_year
        if month_number:
            Filter['month_number'] = month_number
        if class_id:
            Filter['class_id'] = class_id
        if class_group_id:
            Filter['class_group_id'] = class_group_id
        if section_id:
            Filter['section_id'] = section_id
        if subject_id:
            Filter['subject_id'] = subject_id

        present_sheet = Present_sheet_info.objects.filter(**Filter)
        context['present_sheet'] = present_sheet
        return render(request, self.template_name, context)


@transaction.atomic
def edu_attendance_access_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = {}
    if request.method == 'POST':
        try:
            with transaction.atomic():
                employee_id = request.POST.get('employee_id')
                employee = get_object_or_404(
                    Employee_Details, employee_id=employee_id)
                present_sheet_info_ids = request.POST.getlist(
                    'present_sheet_info_ids[]')
                for sheet_info in present_sheet_info_ids:
                    sheet = json.loads(sheet_info)
                    sheet_id = get_object_or_404(
                        Present_sheet_info, present_sheet_info_id=sheet['id'])
                    if sheet['status']:
                        check = Present_sheet_Access.objects.filter(
                            teacher_id=employee_id, present_sheet_info_id=sheet['id']).exists()
                        if check:
                            get_sheet = Present_sheet_Access.objects.get(
                                teacher_id=employee_id, present_sheet_info_id=sheet['id'])
                            get_sheet.is_access = 1
                            get_sheet.save()
                        else:
                            post = Present_sheet_Access()
                            post.teacher_id = employee
                            post.present_sheet_info_id = sheet_id
                            post.is_access = 1
                            post.save()
                    else:
                        check = Present_sheet_Access.objects.filter(
                            teacher_id=employee_id, present_sheet_info_id=sheet['id']).exists()
                        if check:
                            get_sheet = Present_sheet_Access.objects.get(
                                teacher_id=employee_id, present_sheet_info_id=sheet['id'])
                            get_sheet.is_access = 0
                            get_sheet.save()
                data['success_message'] = 'Access parmission update Successfully'
        except Exception as e:
            logger.error("Error in Add student in pressent sheet {} \nType: {} \nError:{}".format(
                sys.exc_info()[-1], type(e).__name__, str(e)))
            data['error_message'] = 'Error '+str(e)+'  Access parmission!'
    return JsonResponse(data)


# (((((((((((((((((((((((Academic Setting)))))))))))))))))))))))

class edu_application_setting_createlist(TemplateView):
    template_name = 'edu/edu-application-setting-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        context = get_global_data(request)
        setting = Academy_info.objects.all()
        if len(setting):
            form = ApplicationSettingModelForm(instance=setting[0])
            context['ap_setting'] = instance = setting[0]
        else:
            form = ApplicationSettingModelForm()

        context['form'] = form
        return render(request, self.template_name, context)


def edu_application_setting_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        setting = Academy_info.objects.all()
        if len(setting):
            form = ApplicationSettingModelForm(
                request.POST, instance=setting[0])
            if form.is_valid():
                post = form.save(commit=False)
                post.app_user_id = request.session["app_user_id"]
                if(request.FILES.get('academic_logo')):
                    post.academic_logo = request.FILES.get('academic_logo')
                if(request.FILES.get('web_header_banner')):
                    post.web_header_banner = request.FILES.get('web_header_banner')
                post.save()
                data['form_is_valid'] = True
                data['success_message'] = 'Application Setting Info Added Successfully!'
            else:
                data['error_message'] = form.errors.as_json()
        else:
            form = ApplicationSettingModelForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.app_user_id = request.session["app_user_id"]
                post.academic_logo = request.FILES.get('academic_logo')
                post.save()
                data['form_is_valid'] = True
                data['success_message'] = 'Application Setting Info Added Successfully!'
            else:
                data['error_message'] = form.errors.as_json()
    return redirect('/edu-application-setting-createlist')

class edu_create_testimonial(TemplateView):
    template_name = 'edu/edu-create-testimonial.html'

    def get(self, request, id,branch_code):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')

        student=Students_Info.objects.filter(student_roll=id).first()
        edu_boards=Education_Board.objects.filter(branch_code=branch_code)
        certificats=Certificat_Name.objects.filter(branch_code=branch_code)
        
        context = get_global_data(request)       
        context['student'] = student
        context['edu_boards'] = edu_boards
        context['certificats'] = certificats
        return render(request, self.template_name, context)

def edu_create_testimonial_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    if request.method == 'POST':
        student=Students_Info.objects.filter(student_roll=request.POST.get('student_roll')).first()
        if Testimonial.objects.filter(branch_code=student.branch_code,student_roll=student.student_roll,cert_name_id=request.POST.get('cert_name_id')).exists():
            data={'error_message':'This testimonial already created.'}
            return JsonResponse(data)
        academic_year=request.POST.get('academic_year')
        
        testimonial_id=fn_get_testmonial_number(student.branch_code,academic_year)
        testimonial=Testimonial()
        testimonial.testmonial_id = testimonial_id
        testimonial.student_roll = student
        testimonial.education_board_id = get_object_or_404(Education_Board, pk=request.POST.get('education_board_id'))
        testimonial.cert_name_id = get_object_or_404(Certificat_Name, pk=request.POST.get('cert_name_id'))
        testimonial.academic_year = request.POST.get('academic_year')
        testimonial.group_name = request.POST.get('group_name')
        testimonial.grade_name = request.POST.get('grade_name')
        testimonial.grade_point = request.POST.get('grade_point')
        testimonial.board_roll = request.POST.get('board_roll')
        testimonial.board_reg = request.POST.get('board_reg')
        testimonial.branch_code = request.POST.get('branch_code')
        testimonial.app_user_id = request.session["app_user_id"]
        testimonial.save()
        data={'redirect_url':'edu-student-testimonial/'+testimonial_id}
        return JsonResponse(data)

def edu_edit_testimonial(request,id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    if request.method == 'POST':
        testimonial=Testimonial.objects.filter(testmonial_id=id).first()
        testimonial.education_board_id = get_object_or_404(Education_Board, pk=request.POST.get('education_board_id'))
        testimonial.cert_name_id = get_object_or_404(Certificat_Name, pk=request.POST.get('cert_name_id'))
        testimonial.academic_year = request.POST.get('academic_year')
        testimonial.group_name = request.POST.get('group_name')
        testimonial.grade_name = request.POST.get('grade_name')
        testimonial.grade_point = request.POST.get('grade_point')
        testimonial.board_roll = request.POST.get('board_roll')
        testimonial.board_reg = request.POST.get('board_reg')
        testimonial.app_user_id = request.session["app_user_id"]
        testimonial.save()
        data={'redirect_url':'edu-student-testimonial/'+testimonial.student_roll.student_roll}
        return JsonResponse(data)
        
def edu_student_testimonial(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    template_name = 'edu/edu-student-testimonial.html'
    data = dict()
    testimonial=Testimonial.objects.filter(testmonial_id=id).first()
    if testimonial:
        header= Certificat_Header_Address.objects.filter(branch_code=testimonial.branch_code).first()
        addare_array = header.address.split(";")
        userSetting=User_Settings.objects.filter(app_user_id = testimonial.app_user_id).first()
        data['header']=header
        data['addare_array']=addare_array
        data['testimonial']=testimonial
        data['composer_name']=userSetting.employee_name
    return render(request, template_name, data)


def edu_student_tc(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Academy_info)
    students = Students_Info.objects.filter(student_roll=id).first()
    grade = Exam_Marks_Final.objects.filter(student_roll=id).first()
    template_name = 'edu/edu-student-tc.html'
    data = dict()
    data['testimonial'] = instance_data
    data['student'] = students
    data['grade'] = grade
    return render(request, template_name, data)


def edu_student_TcGenerate_form(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    template_name = 'edu/edu-student-tc-createform.html'
    data = dict()
    form = TcModelForm()
    students = Students_Info.objects.all()
    data = get_global_data(request)
    data['form'] = form
    data['students'] = students
    return render(request, template_name, data)


def edu_student_TcData_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    if request.method == 'POST':
        form = TcModelForm(request.POST)
        if form.is_valid():
            tc_id = fn_get_tc_id()
            student_roll = request.POST.get("student_roll")
            print(student_roll)
            if Transfer_Certificate.objects.filter(student_roll=student_roll).exists():
                data['error_message'] = 'This Student TC already created'
                data['form_is_valid'] = False
                return JsonResponse(data)
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.tc_id = tc_id
            post.student_roll = Students_Info.objects.filter(
                student_roll=student_roll).first()
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'TC Info Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_tc_viewform(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    # instance_data = get_object_or_404(Transfer_Certificate, pk=id)
    instance_data = get_object_or_404(Academy_info)
    students = Students_Info.objects.filter(student_roll=id).first()
    tc_info = Transfer_Certificate.objects.filter(student_roll=id).first()
    print(id)
    template_name = 'edu/edu-tc-viewform.html'
    data = dict()
    context = get_global_data(request)
    context['student'] = students
    context['tc_info'] = tc_info
    context['institute'] = instance_data
    data['html_form'] = render_to_string(
        template_name, context, request=request)
    return JsonResponse(data)


def edu_tc_editform(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Transfer_Certificate, student_roll=id)
    template_name = 'edu/edu-tc-edit.html'
    data = dict()

    if request.method == 'POST':
        form = TcModelForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            data['success_message'] = 'Edit Successfully!'
            data['error_message'] = ''
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = TcModelForm(instance=instance_data)
        students = Students_Info.objects.filter(student_roll=id).first()
        context = get_global_data(request)
        context['form'] = form
        context['students'] = students
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)

# (((((((((((((((((Exam Attendance)))))))))))))))))


def edu_examattendance_createform(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    template_name = 'edu/edu-examattendance-createform.html'
    data = dict()
    form = ExamAttenModelForm()
    data = get_global_data(request)
    data['form'] = form
    return render(request, template_name, data)


@transaction.atomic
def edu_examattendance_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    if request.method == 'POST':
        try:
            with transaction.atomic():
                form = ExamAttenModelForm(request.POST)
                if form.is_valid():
                    exam_atten_id = fn_get_exam_atten_id()
                    # student_roll=request.POST.get("student_roll")
                    # if Students_Info.objects.filter(student_roll=student_roll).exists():
                    #     data['error_message'] = 'This Student TC already created'
                    #     data['form_is_valid'] = False
                    #     return JsonResponse(data)
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.exam_atten_id = exam_atten_id
                    # post.student_roll = Students_Info.objects.filter(student_roll=student_roll).first()
                    post.save()
                    students = Students_Info.objects.filter(
                        class_id=post.class_id.class_id)
                    for student in students:
                        print(student)
                        ex_details = Exam_attendence_Details()
                        ex_details.exam_atten_id = post
                        ex_details.student_roll = student
                        ex_details.student_name = student.student_name
                        ex_details.app_user_id = request.session["app_user_id"]
                        ex_details.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Exam Attendance Info Added Successfully!'
                else:
                    data['error_message'] = form.errors.as_json()
        except Exception as e:
            logger.error("Error in Add student in pressent sheet {} \nType: {} \nError:{}".format(
                sys.exc_info()[-1], type(e).__name__, str(e)))
            data['error_message'] = 'Error ' + \
                str(e)+'  Add student in pressent sheet!'
    return JsonResponse(data)


def edu_examattendance_editform(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Exam_Attendance, pk=id)
    template_name = 'edu/edu-examattendance-edit.html'
    data = dict()

    if request.method == 'POST':
        form = ExamAttenModelForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            data['success_message'] = 'Edit Successfully!'
            data['error_message'] = ''
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = ExamAttenModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


def edu_examattendance_viewform(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    # instance_data = get_object_or_404(Transfer_Certificate, pk=id)
    instance_data = get_object_or_404(Academy_info)
    atten_info = Exam_attendence_Details.objects.filter(exam_atten_id=id)
    attendance = Exam_Attendance.objects.filter(exam_atten_id=id).first()
    # print(id)
    # students=[]
    # if atten_info.class_id:
    #     students = Students_Info.objects.filter(class_id=atten_info.class_id)

    # # print(students)
    students = Students_Info.objects.all()
    template_name = 'edu/edu-examattendance-viewform.html'
    data = dict()
    context = get_global_data(request)
    context['student'] = students
    context['attendance'] = attendance
    context['atten_info'] = atten_info
    context['institute'] = instance_data
    data['html_form'] = render_to_string(
        template_name, context, request=request)
    return JsonResponse(data)


def edu_examattendance_pdfview(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    # instance_data = get_object_or_404(Transfer_Certificate, pk=id)
    instance_data = get_object_or_404(Academy_info)
    atten_info = Exam_attendence_Details.objects.filter(exam_atten_id=id)
    attendance = Exam_Attendance.objects.filter(exam_atten_id=id).first()
    # print(id)
    # students=[]
    # if atten_info.class_id:
    #     students = Students_Info.objects.filter(class_id=atten_info.class_id)

    # # print(students)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Times', '', 12)
    for i in range(1, 41):
        pdf.cell(0, 10, 'abcdefghijklmnopqrstuvwxyz ' + str(i), 0, 1)
    pdf.output('tuto2.pdf', 'F')

    students = Students_Info.objects.all()
    template_name = 'edu/edu-examattendance-viewform.html'
    data = dict()
    context = get_global_data(request)
    context['student'] = students
    context['attendance'] = attendance
    context['atten_info'] = atten_info
    context['institute'] = instance_data
    data['html_form'] = render_to_string(
        template_name, context, request=request)
    return JsonResponse(data)


# (((((((((((((((fees head setting)))))))))))))))


class edu_feesheadsetting_createlist(TemplateView):
    template_name = 'edu/edu-feesheadsetting-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = FeesHeadSettingModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_feesheadsetting_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    if request.method == 'POST':
        form = FeesHeadSettingModelForm(request.POST)
        if form.is_valid():
            head_code = fn_get_fees_head_code()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.head_ledger = request.POST.get('head_ledger')
            post.app_data_time = timezone.now()
            post.head_code = head_code
            post.is_active = True
            post.is_deleted = False
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Fees Head Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_feesheadsetting_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Fees_Head_Settings, head_code=id)
    template_name = 'edu/edu-feesheadsetting-edit.html'
    data = dict()

    if request.method == 'POST':
        form = FeesHeadSettingModelForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.head_ledger = request.POST.get('head_ledger')
            obj.is_deleted = False
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
        form = FeesHeadSettingModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


def edu_feesheadsetting_delete(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Fees_Head_Settings, pk=id)
    data = dict()
    instance_data.is_deleted = True
    instance_data.save()
    data['success_message'] = "Well Done"
    return JsonResponse(data)


class edu_feesweiver_mapping_createlist(TemplateView):
    template_name = 'edu/edu-feesweiver-mapping-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        branch_code = request.session['branch_code']
        app_user_id = request.session["app_user_id"]
        cbd = get_business_date(branch_code, app_user_id)
        form = Fees_Waiver_Mapping_ModelForm(initial={'effective_date': cbd})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_feesweiver_mapping_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    if request.method == 'POST':
        form = Fees_Waiver_Mapping_ModelForm(request.POST)
        hist_form = Fees_Waiver_Mapping_Hist_ModelForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.app_data_time = timezone.now()
                    post.is_active = True
                    post.is_deleted = False
                    post.save()
                    hist_post = hist_form.save(commit=False)
                    hist_post.app_user_id = request.session["app_user_id"]
                    hist_post.day_serial = 1
                    hist_post.is_active = True
                    hist_post.is_deleted = False
                    hist_post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Fees Waiver Mapping Successfully!'
            except Exception as e:
                data['error_message'] = str(e)
                data['form_is_valid'] = False
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_feesweiver_mapping_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Fees_Waiver_Mapping, pk=id)
    template_name = 'edu/edu-feesweiver-mapping-edit.html'
    data = dict()
    data_hist = dict()

    if request.method == 'POST':
        form = Fees_Waiver_Mapping_ModelForm(
            request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            if form.has_changed():
                try:
                    with transaction.atomic():
                        hist_form = Fees_Waiver_Mapping_Hist_ModelForm(
                            request.POST)
                        obj = form.save(commit=False)
                        obj.save()
                        hist_post = hist_form.save(commit=False)
                        hist_post.app_user_id = request.session["app_user_id"]
                        data_hist["head_code"] = obj.head_code
                        data_hist["catagory_id"] = obj.catagory_id
                        data_hist["class_id"] = obj.class_id
                        data_hist["class_group_id"] = obj.class_group_id
                        data_hist["section_id"] = obj.section_id
                        data_hist["effective_date"] = obj.effective_date
                        hist_post.day_serial = fn_get_feeswaive_mapping_hist_count(
                            data_hist)
                        hist_post.save()
                        data['success_message'] = 'Updated Successfully!'
                        data['error_message'] = ''
                        data['form_is_valid'] = True
                except Exception as e:
                    data['error_message'] = str(e)
                    data['form_is_valid'] = False
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
    else:
        form = Fees_Waiver_Mapping_ModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


def edu_feesweiver_mapping_delete(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Fees_Waiver_Mapping, id=id)
    data = dict()
    instance_data.is_deleted = True
    instance_data.save()
    data['success_message'] = "Well Done"
    return JsonResponse(data)


class edu_feesmapping_createlist(TemplateView):
    template_name = 'edu/edu-feesmapping-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        branch_code = request.session['branch_code']
        app_user_id = request.session["app_user_id"]
        cbd = get_business_date(branch_code, app_user_id)
        form = FeesMappingModelForm(
            initial={'effective_date': cbd})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def edu_feesmapping_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    if request.method == 'POST':
        form = FeesMappingModelForm(request.POST)
        hist_form = Fees_Mapping_History_Model_Form(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    fees_mapping_id=fn_get_fees_mapping_id()
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.is_active = True
                    post.is_deleted = False
                    post.fees_mapping_id= fees_mapping_id
                    post.save()
                    hist_post = hist_form.save(commit=False)
                    hist_post.app_user_id = request.session["app_user_id"]
                    hist_post.day_serial = 1
                    hist_post.is_active = True
                    hist_post.is_deleted = False
                    hist_post.fees_mapping_id= fees_mapping_id
                    hist_post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Fees Mapping Info Added Successfully!'
            except Exception as e:
                data['error_message'] = str(e)
                data['form_is_valid'] = False
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


@transaction.atomic
def edu_feesmapping_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Fees_Mapping, fees_mapping_id=id)
    fees_mapping_id = instance_data.fees_mapping_id
    template_name = 'edu/edu-feesmapping-edit.html'
    data = dict()
    data_hist = dict()
    data['form_is_valid'] = True
    data['error_message'] = ''
    if request.method == 'POST':
        form = FeesMappingModelForm(request.POST, instance=instance_data)
        if form.is_valid():
            if form.has_changed():
                try:
                    with transaction.atomic():
                        hist_form = Fees_Mapping_History_Model_Form(
                            request.POST)
                        obj = form.save(commit=False)
                        obj.save()
                        hist_post = hist_form.save(commit=False)
                        hist_post.app_user_id = request.session["app_user_id"]
                        data_hist["fees_mapping_id"] = fees_mapping_id
                        data_hist["effective_date"] = obj.effective_date
                        hist_post.day_serial = fn_get_fees_mapping_hist_count(
                            data_hist)
                        hist_post.fees_mapping_id=fees_mapping_id
                        hist_post.save()
                        data['success_message'] = 'Updated Successfully!'
                        data['error_message'] = ''
                        data['form_is_valid'] = True
                except Exception as e:
                    data['error_message'] = str(e)
                    data['form_is_valid'] = False
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
    else:
        form = FeesMappingModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


def edu_feesmapping_delete(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Fees_Mapping, fees_mapping_id=id)
    data = dict()
    try:
        with transaction.atomic():
            instance_data.is_deleted = True
            instance_data.save()
            Fees_Mapping_History.objects.filter(head_code=instance_data.head_code,
                                                class_id=instance_data.class_id, class_group_id=instance_data.class_group_id, section_id=instance_data.section_id).delete()
            data['success_message'] = "Well Done"
    except Exception as e:
        data['error_message'] = str(e)
        data['form_is_valid'] = False
    return JsonResponse(data)


class edu_absfinesmapping_createlist(TemplateView):
    template_name = 'edu/edu-absfinesmapping-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        branch_code = request.session['branch_code']
        app_user_id = request.session["app_user_id"]
        cbd = get_business_date(branch_code, app_user_id)
        form = AbsFineMappingModelForm(
            initial={'effective_date': cbd})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def edu_absfinesmapping_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    if request.method == 'POST':
        form = AbsFineMappingModelForm(request.POST)
        hist_form = Absent_Fine_History_Model_Form(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.is_active = True
                    post.is_deleted = False
                    post.save()
                    hist_post = hist_form.save(commit=False)
                    hist_post.app_user_id = request.session["app_user_id"]
                    hist_post.day_serial = 1
                    hist_post.is_active = True
                    hist_post.is_deleted = False
                    hist_post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Absent Fine Mapping Info Added Successfully!'
            except Exception as e:
                data['error_message'] = str(e)
                data['form_is_valid'] = False
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


@transaction.atomic
def edu_absfinesmapping_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Absent_Fine_Mapping, pk=id)
    template_name = 'edu/edu-absfinesmapping-edit.html'
    data = dict()
    data['form_is_valid'] = True
    data['error_message'] = ''
    if request.method == 'POST':
        form = AbsFineMappingModelForm(request.POST, instance=instance_data)
        if form.is_valid():
            if form.has_changed():
                try:
                    with transaction.atomic():
                        hist_form = Absent_Fine_History_Model_Form(
                            request.POST)
                        obj = form.save(commit=False)
                        obj.save()
                        hist_post = hist_form.save(commit=False)
                        hist_post.app_user_id = request.session["app_user_id"]
                        hist_post.day_serial = fn_get_absent_fine_hist_count(
                            obj.head_code, obj.effective_date)
                        hist_post.save()
                        data['success_message'] = 'Updated Successfully!'
                        data['error_message'] = ''
                        data['form_is_valid'] = True
                except Exception as e:
                    data['error_message'] = str(e)
                    data['form_is_valid'] = False
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
    else:
        form = AbsFineMappingModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


def edu_absfinesmapping_delete(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Absent_Fine_Mapping, pk=id)
    data = dict()
    instance_data.is_deleted = True
    instance_data.save()
    data['success_message'] = "Well Done"
    return JsonResponse(data)


class edu_feeswaivestudent_createlist(TemplateView):
    template_name = 'edu/edu-feeswaivestudent-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session['branch_code']
        transaction_date = get_business_date(branch_code, app_user_id)
        form = FeesReceiveStudentModelForm(
            initial={'due_date': transaction_date})
        form.fields['due_date'].label = 'Effective Date'
        form.fields['student_roll'].label = 'Search a Student ID'
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_feeswaivestudent_update_temp(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    id = request.GET.get('id')
    taka = request.GET.get('taka')
    fess = Fees_Receive_Temp.objects.filter(id=id).first()
    fess.fees_waive = Decimal(taka)
    fess.total_waive = max(fess.total_waive+Decimal(taka), 0)
    fess.save()
    return JsonResponse(data)


class edu_feeswaivestudent_createlist_old(TemplateView):
    template_name = 'edu/edu-feeswaivestudent-createlist-old.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        branch_code = request.session['branch_code']
        app_user_id = request.session["app_user_id"]
        cbd = get_business_date(branch_code, app_user_id)
        form = FeesWaiveStudentModelForm(
            initial={'effective_date': cbd})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)

@transaction.atomic
def edu_feeswaivestudent_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    student_roll = request.POST.get('student_roll')
    effective_date = request.POST.get('effective_date')
    # branch_code = request.POST.get('branch_code')
    app_user_id = request.session["app_user_id"]
    try:
        with transaction.atomic():
            temp_data=Fees_Receive_Temp.objects.filter(student_roll=student_roll,app_user_id=app_user_id)
            waive_data=Fees_Waive_Student.objects.filter(student_roll=student_roll)
            for td in temp_data:
                if td.fees_waive>0:
                    if(waive_data.filter(head_code=td.head_code,ledger_code=td.ledger_code,fees_year=td.due_date.year,fees_month=td.due_date.month).exists()):
                        Waive=waive_data.get(head_code=td.head_code,ledger_code=td.ledger_code,fees_year=td.due_date.year,fees_month=td.due_date.month)
                        Waive.effective_date=effective_date
                        Waive.waive_amount=td.fees_waive
                        Waive.fee_amount=td.fees_due
                        Waive.app_user_id=app_user_id
                        Waive.app_data_time=timezone.now()
                        Waive.cancel_by = None
                        Waive.cancel_on = None
                        Waive.save()
                    else:
                        Waive= Fees_Waive_Student()
                        Waive.effective_date=effective_date
                        Waive.waive_amount=td.fees_waive
                        Waive.head_code=td.head_code
                        Waive.ledger_code=td.ledger_code
                        Waive.student_roll=td.student_roll
                        Waive.fee_amount=td.fees_due
                        Waive.fees_month=td.due_date.month
                        Waive.fees_year=td.due_date.year
                        Waive.app_user_id=app_user_id
                        Waive.branch_code=td.branch_code
                        Waive.app_data_time=timezone.now()
                        Waive.save()
    except Exception as e:
        data['error_message'] = str(e)
        data['form_is_valid'] = False
        return JsonResponse(data)
        print(str(e))
    data['form_is_valid'] = True
    data['success_message'] = 'Save Successfully!'
    return JsonResponse(data)

class edu_feeswaivestudent_list(TemplateView):
    template_name = 'edu/edu-feeswaivestudent-list.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session['branch_code']
        form = FeesWaiveStudentModelForm()
        form.fields['effective_date'].label = 'Effective Date'
        form.fields['student_roll'].label = 'Search a Student ID'
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_feeswaivestudent_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Fees_Waive_Student, pk=id)
    template_name = 'edu/edu-feeswaivestudent-edit.html'
    data = dict()

    if request.method == 'POST':
        instance_data.app_data_time=datetime.now()
        instance_data.cancel_on=datetime.now()
        instance_data.cancel_by=request.session["app_user_id"]
        instance_data.save()
        data['form_is_valid'] = True
        # data['error_message'] = form.errors.as_json()
        return JsonResponse(data)
    else:
        form = FeesWaiveStudentModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


# (((((((((((((((((((((((Student Quick Collection)))))))))))))))))))))))

class edu_quick_collection(TemplateView):
    template_name = 'edu/edu-quick-collection.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session['branch_code']
        transaction_date = get_business_date(branch_code, app_user_id)
        form = FeesReceiveStudentModelForm(
            initial={'receive_date': transaction_date,'due_date':transaction_date})
        form.fields['student_roll'].label = 'Search a Student ID'
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_quick_collection_student_info(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    data = dict()
    student_roll = request.GET.get('student_roll')
    receive_date = request.GET.get('receive_date')
    due_date = request.GET.get('due_date')
    branch_code = request.session['branch_code']
    app_user_id = request.session["app_user_id"]
    # transaction_date = get_business_date(branch_code, app_user_id)
    status, error_message = fn_search_student_fees(
        student_roll, due_date, app_user_id)
    if status:
        pass
    else:
        data['error_message'] = error_message
        return JsonResponse(data)

    # fn_search_student_fees
    student_info = Students_Info.objects.values('student_roll', 'student_name',
                                                'class_id__class_name', 'class_group_id__class_group_name',
                                                'student_father_name', 'class_roll', 'session_id__session_name', 'student_phone',
                                                'profile_image', 'catagory_id__catagory_name').filter(student_roll=student_roll).first()
    fees = Fees_Receive_Temp.objects.filter(
        student_roll=student_roll, app_user_id=app_user_id)
    
    data['student_info'] = student_info
    data['fees'] = list(fees.values())
    return JsonResponse(data)



def edu_quick_collection_update_temp(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    id = request.GET.get('id')
    taka = request.GET.get('taka')
    fess = Fees_Receive_Temp.objects.filter(id=id).first()
    fess.total_paid = Decimal(taka)
    fess.total_overdue = max(fess.total_due-fess.total_paid, 0)
    fess.save()
    return JsonResponse(data)

@transaction.atomic
def edu_quick_collection_submit(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    student_roll = request.GET.get('student_roll')
    receive_date = request.GET.get('receive_date')
    branch_code = request.GET.get('branch_code')
    app_user_id = request.session["app_user_id"]
    data['form_is_valid'] = False
    data['transaction_id'] = None
    try:
        with transaction.atomic():
            status, error_message, transaction_id = fn_edu_fees_submit(
                branch_code, student_roll, receive_date, app_user_id)
            if status:
                data['transaction_id'] = transaction_id
            else:
                data['form_is_valid'] = False
                data['error_message'] = error_message
                return JsonResponse(data)
            data['form_is_valid'] = True
            data['success_message'] = 'Save Successfully!'
    except Exception as e:
        data['error_message'] = str(e)
        data['form_is_valid'] = False
        return JsonResponse(data)
    return JsonResponse(data)
    

@transaction.atomic
def edu_one_time_fees_receive(request, student_id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    template_name = 'edu/edu-one-time-fees-receive.html'
    data = dict()
    branch_code = request.session['branch_code']
    app_user_id = request.session["app_user_id"]
    cbd = get_business_date(branch_code, app_user_id)
    if request.method == 'POST':
        form = OneTimeFeesReceiveStudentModelForm(request.POST)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj = form.save(commit=False)
                    status, error_message, batch_number = fn_edu_fees_others_receive(
                        obj.student_roll.student_roll, obj.receive_date, obj.head_code.head_code, obj.receive_amount, app_user_id)
                    if not status:
                        data['error_message'] = 'Fees Posting Error '+error_message
                        data['form_is_valid'] = False
                        return JsonResponse(data)
                    obj.save()
                    data['success_message'] = 'Payment Received Successfully!'
                    data['error_message'] = ''
                    data['form_is_valid'] = True
                    return JsonResponse(data)
            except Exception as e:
                data['error_message'] = str(e)
                data['form_is_valid'] = False
                return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        receive_date = request.GET.get('receive_date')
        form = OneTimeFeesReceiveStudentModelForm(
            initial={'student_roll': student_id, 'receive_date': receive_date})
        context = get_global_data(request)
        context['form'] = form
        context['student_id'] = student_id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


class edu_idcard_createform(TemplateView):
    template_name = 'edu/edu-idcard-createform.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = StudentIDCardModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def edu_idcard_datainsert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    if request.method == 'POST':
        form = StudentIDCardModelForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    student_roll = request.POST.get('student_roll')
                    class_id = request.POST.get('class_id')
                    academic_year = request.POST.get('academic_Year')
                    expire_date = request.POST.get('expire_date')
                    if student_roll:
                        if Student_ID_Card.objects.filter(student_roll=student_roll, class_id=class_id, academic_Year=academic_year, expire_date=expire_date).exists():
                            data['error_message'] = 'This Student Info Allready Created'
                            return JsonResponse(data)
                        id_card_no = fn_get_id_card_no()
                        post = form.save(commit=False)
                        post.app_user_id = request.session["app_user_id"]
                        post.app_data_time = timezone.now()
                        post.id_card_no = id_card_no
                        post.save()
                        data['form_is_valid'] = True
                        data['success_message'] = 'Student ID Card Info Added Successfully!'
                    else:
                        students = Students_Info.objects.filter(
                            class_id=class_id, academic_year=academic_year)
                        for student in students:
                            if Student_ID_Card.objects.filter(student_roll=student.student_roll, class_id=class_id, academic_Year=academic_year, expire_date=expire_date).exists():
                                pass
                            else:
                                id_card_no = fn_get_id_card_no()
                                post = form.save(commit=False)
                                post.app_user_id = request.session["app_user_id"]
                                post.app_data_time = timezone.now()
                                post.id_card_no = id_card_no
                                post.student_roll = student
                                post.save()
                        data['form_is_valid'] = True
                        data['success_message'] = 'Student ID Card Info Added Successfully!'

            except Exception as e:
                data['error_message'] = str(e)
                data['form_is_valid'] = False
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


@transaction.atomic
def edu_idcard_update(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    if request.method == 'POST':
        form = StudentIDCardModelForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    student_roll = request.POST.get('student_roll')
                    class_id = request.POST.get('class_id')
                    class_group_id = request.POST.get('class_group_id')
                    academic_year = request.POST.get('academic_Year')
                    expire_date = request.POST.get('expire_date')
                    branch_code = request.POST.get('branch_code')
                    section_id = request.POST.get('section_id')
                    session_id = request.POST.get('session_id')
                    back_text = request.POST.get('back_text')
                    if not class_group_id:
                        class_group_id = None
                    if not section_id:
                        section_id = None
                    if not session_id:
                        session_id = None
                    if student_roll:
                        Student_ID_Card.objects.filter(branch_code=branch_code, student_roll=student_roll, class_id=class_id, academic_Year=academic_year, expire_date=expire_date).update(
                            class_group_id=class_group_id,
                            section_id=section_id,
                            session_id=session_id,
                            back_text=back_text,
                            app_user_id=request.session["app_user_id"]
                        )
                    elif class_group_id:
                        Student_ID_Card.objects.filter(branch_code=branch_code, class_id=class_id, academic_Year=academic_year, expire_date=expire_date, class_group_id=class_group_id).update(
                            section_id=section_id,
                            session_id=session_id,
                            back_text=back_text,
                            app_user_id=request.session["app_user_id"]
                        )
                    else:
                        Student_ID_Card.objects.filter(branch_code=branch_code, class_id=class_id, academic_Year=academic_year, expire_date=expire_date).update(
                            section_id=section_id,
                            session_id=session_id,
                            back_text=back_text,
                            app_user_id=request.session["app_user_id"]
                        )
                        data['form_is_valid'] = True
                        data['success_message'] = 'Student ID Card Update Successfully!'

            except Exception as e:
                data['error_message'] = str(e)
                data['form_is_valid'] = False
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_idcard_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Student_ID_Card, id_card_no=id)
    template_name = 'edu/edu-idcard-edit.html'
    data = dict()

    if request.method == 'POST':
        form = StudentIDCardModelForm(request.POST, instance=instance_data)
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
        form = StudentIDCardModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        context['global_branch_code'] = instance_data.branch_code
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


# //Result Marge


class edu_published_result_marge_form(TemplateView):
    template_name = 'edu/edu-result-marge-form.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        academic_year = Academic_Year.objects.all()
        academic_class = Academic_Class.objects.all()
        exam_terms = Exam_Term.objects.all().order_by('id')
        data = dict()
        data['years'] = academic_year
        data['academic_class'] = academic_class
        data['exam_terms'] = exam_terms
        return render(request, self.template_name, data)


class edu_published_result_marge_view(TemplateView):
    template_name = 'edu/edu-result-marge-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        header_title = request.GET.get('header_title')
        academic_year = request.GET.get('academic_year')
        class_id = request.GET.get('class_id')
        app_user_id = request.session["app_user_id"]
        terms_str = request.GET.get('terms')
        class_info = get_object_or_404(Academic_Class, class_id=class_id)
        data = dict()
        if not terms_str:
            data['mass'] = "Exam term not select"
            return render(request, self.template_name, data)
        terms = []
        for i in terms_str.split(','):
            terms.append(int(i))
        term_list = Exam_Term.objects.all()
        exam_list = Store_Exam_Single_Mark.objects.filter(academic_year=academic_year,
                                                          class_id=class_id, term_id__in=terms)
        subjects = exam_list.values('subject_id', 'subject_id__subject_name').annotate(
            Count('subject_id')).order_by('subject_id__subject_name')

        exam_names = exam_list.values(
            'exam_id__exam_name').annotate(Count('exam_id'))

        final_result = Exam_Marks_Final.objects.values('student_roll', 'student_roll__student_name').annotate(
            final_total_exam_mark=Sum('total_exam_marks'),
            final_obtain_marks=Sum('obtain_marks'),
            gpa=Sum('grade_point_average')).filter(academic_year=academic_year,
                                                   class_id=class_id, term_id__in=terms
                                                   )
        total_mark = list(final_result)
        total_mark.sort(key=lambda x: (
            x['gpa'], x['final_obtain_marks']), reverse=True)
        for index, m in enumerate(total_mark):
            gpa = get_result_great(
                m['final_obtain_marks'], m['final_total_exam_mark'], class_info.out_of)
            m['final_gpa'] = gpa[0]
            m['final_grade'] = gpa[1]
            m['position'] = index+1
            m['subjects'] = subjects
            m['term_list'] = term_list
            m['exam_names'] = exam_names
            m['term_exam_colspan'] = len(exam_names)+3
            shearch = []
            for t in terms:
                s_term = dict()
                s_term['academic_year'] = academic_year
                s_term['class_id'] = class_id
                s_term['term_id'] = t
                s_term['student_roll'] = m['student_roll']
                shearch.append(s_term)
            m['shearch'] = shearch
        institute = Academy_info.objects.first()

        data['total_mark'] = total_mark
        data['institute'] = institute
        data['header_title'] = header_title
        data['class_info'] = class_info
        return render(request, self.template_name, data)


@transaction.atomic
def edu_published_result_marge_publish(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    try:
        with transaction.atomic():
            header_title = request.GET.get('header_title')
            academic_year = request.GET.get('academic_year')
            class_id = request.GET.get('class_id')
            app_user_id = request.session["app_user_id"]
            terms_str = request.GET.get('terms')
            class_info = get_object_or_404(Academic_Class, class_id=class_id)
            data = dict()
            terms = []
            for i in terms_str.split(','):
                terms.append(int(i))

            final_result = Exam_Marks_Final.objects.values('student_roll', 'academic_year').annotate(
                final_total_exam_mark=Sum('total_exam_marks'),
                final_obtain_marks=Sum('obtain_marks'),
                gpa=Sum('grade_point_average')).filter(academic_year=academic_year,
                                                       class_id=class_id, term_id__in=terms
                                                       )
            total_mark = list(final_result)
            total_mark.sort(key=lambda x: (
                x['gpa'], x['final_obtain_marks']), reverse=True)
            for index, m in enumerate(total_mark):
                gpa = get_result_great(
                    m['final_obtain_marks'], m['final_total_exam_mark'], class_info.out_of)
                m['final_gpa'] = gpa[0]
                m['final_grade'] = gpa[1]
                m['position'] = index+1
                m['terms'] = terms
            academic_Year = get_object_or_404(Academic_Year, pk=academic_year)
            for mark in total_mark:
                if not Marge_Result.objects.filter(academic_year=mark['academic_year'], class_id=class_id, term_id=mark['terms'], title=header_title, student_roll=mark['student_roll']).exists():
                    marge_result = Marge_Result()
                    marge_result.academic_year = academic_Year
                    marge_result.class_id = class_info
                    marge_result.student_roll = get_object_or_404(
                        Students_Info, student_roll=mark['student_roll'])
                    marge_result.term_id = mark['terms']
                    marge_result.title = header_title
                    marge_result.total_exam_marks = mark['final_total_exam_mark']
                    marge_result.total_obtain_marks = mark['final_obtain_marks']
                    marge_result.gpa = mark['final_gpa']
                    marge_result.lg = mark['final_grade']
                    marge_result.position = mark['position']
                    marge_result.app_user_id = app_user_id
                    marge_result.save()
                    data['success_message'] = "Result Save and Published!"
                else:
                    data['error_message'] = "This Result already Published!"
    except Exception as e:
        data['error_message'] = str(e)
    return JsonResponse(data)
# (((((((((((((((((Student Admit Card)))))))))))))))))


class edu_admitcard_createform(TemplateView):
    template_name = 'edu/edu-admitcard-createform.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = StudentAdmitCardModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def edu_admitcard_datainsert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    if request.method == 'POST':
        form = StudentAdmitCardModelForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    branch_code = request.POST.get('branch_code')
                    student_roll = request.POST.get('student_roll')
                    academic_year = request.POST.get('academic_year')
                    class_id = request.POST.get('class_id')
                    class_group_id = request.POST.get('class_group_id')
                    session_id = request.POST.get('session_id')
                    exam_term_id = request.POST.get('exam_term_id')
                    dataFilter=dict()
                    stdFilter=dict()
                    stdFilter['student_status']='A'
                    if branch_code and academic_year and class_id:
                        dataFilter['branch_code']=branch_code
                        dataFilter['academic_year']=academic_year
                        dataFilter['class_id']=class_id
                        stdFilter['branch_code']=branch_code
                        stdFilter['academic_year']=academic_year
                        stdFilter['class_id']=class_id
                    else:
                        data['error_message'] = 'Branch,Year and class required'
                        data['form_is_valid'] = False
                        
                    if student_roll:
                        dataFilter['student_roll']=student_roll
                    if exam_term_id:
                        dataFilter['exam_term_id']=exam_term_id
                    if class_group_id:
                        dataFilter['class_group_id']=class_group_id
                        stdFilter['class_group_id']=class_group_id
                    if session_id:
                        dataFilter['session_id']=session_id
                        stdFilter['session_id']=session_id
                        
                        
                    if student_roll:
                        if Student_Admit_Card.objects.filter(*dataFilter).exists():
                            data['error_message'] = 'This Student Admit Card Allready Created'
                            return JsonResponse(data)
                        admit_card_id = fn_get_admit_card_no()
                        post = form.save(commit=False)
                        post.app_user_id = request.session["app_user_id"]
                        post.app_data_time = timezone.now()
                        post.admit_card_id = admit_card_id
                        post.save()
                        data['form_is_valid'] = True
                        data['success_message'] = 'Student Admit Card Info Added Successfully!'
                    else:
                        students=Students_Info.objects.filter(**stdFilter)
                        
                        for student in students:
                            dataFilter['student_roll']=student.student_roll
                            if Student_Admit_Card.objects.filter(**dataFilter).exists():
                                pass
                            else:
                                admit_card_id = fn_get_admit_card_no()
                                post = form.save(commit=False)
                                post.app_user_id = request.session["app_user_id"]
                                post.app_data_time = timezone.now()
                                post.admit_card_id = admit_card_id
                                post.student_roll = student
                                post.save()
                        data['form_is_valid'] = True
                        data['success_message'] = 'Student Admit Card Info Added Successfully!'

            except Exception as e:
                data['error_message'] = str(e)
                data['form_is_valid'] = False
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


@transaction.atomic
def edu_admitcard_update(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    if request.method == 'POST':
        form = StudentAdmitCardModelForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    
                    student_roll=request.POST.get('student_roll')
                    class_id=request.POST.get('class_id')
                    academic_year_id=request.POST.get('academic_year_id')
                    class_group_id=request.POST.get('class_group_id')
                    session_id=request.POST.get('session_id')
                    branch_code=request.POST.get('branch_code')
                    dataFilter=dict()
                    if branch_code and class_id and academic_year_id:
                        dataFilter['branch_code']=branch_code
                        dataFilter['academic_year_id']=academic_year_id
                        dataFilter['class_id']=class_id
                    else:
                        data['error_message'] = 'Branch,Year and class required'
                        return JsonResponse(data)
                    if student_roll:
                        dataFilter['student_roll']=student_roll
                    if class_group_id:
                        dataFilter['class_group_id']=class_group_id
                    if session_id:
                        dataFilter['session_id']=session_id
                        
                    admitCards= Student_Admit_Card.objects.filter(**dataFilter)
                    exam_term=Exam_Term.objects.get(id=request.POST.get('exam_term_id'))
                    for admit in admitCards:
                        admit.exam_term_id = exam_term
                        admit.trams_con = request.POST.get('trams_con')
                        admit.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Student Admit Card Info Update Successfully!'
            except Exception as e:
                data['error_message'] = str(e)
                data['form_is_valid'] = False
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)

# ((((((((((((((((((((Course Registrations Create))))))))))))))))))))


class edu_coursereg_createform(TemplateView):
    template_name = 'edu/edu-coursereg-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = CourseRegModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_coursereg_datainsert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    if request.method == 'POST':
        form = CourseRegModelForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.app_data_time = timezone.now()
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Course Registrations Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_coursereg_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Course_Registrations, pk=id)
    template_name = 'edu/edu-coursereg-edit.html'
    data = dict()

    if request.method == 'POST':
        form = CourseRegModelForm(request.POST, instance=instance_data)
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
        instance_data = get_object_or_404(Course_Registrations, pk=id)
        form = CourseRegModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        context['issue_date'] = str(instance_data.issue_date)
        context['expire_date'] = str(instance_data.expire_date)
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


# ((((((((((((((((((((((Marks Blank Sheet))))))))))))))))))))))

class edu_marks_blanksheet(TemplateView):
    template_name = 'edu/edu-marks-blanksheet.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = StudentInfoModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


# (((((((((((((((((All Download Forms)))))))))))))))))

class edu_allform_download(TemplateView):
    template_name = 'edu/edu-allform-download.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = AdmissionFormHeaderModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


# (((((((((((((((Students Seat Plane)))))))))))))))

class edu_seat_plane(TemplateView):
    template_name = 'edu/edu-seat-plane.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = StudentSeatPlaneModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def edu_seat_plane_datainsert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    if request.method == 'POST':
        form = StudentSeatPlaneModelForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    datafilter = dict()
                    student_roll = request.POST.get('student_roll')
                    class_id = request.POST.get('class_id')
                    academic_year = request.POST.get('academic_year')
                    class_group_id = request.POST.get('class_group_id')
                    if academic_year:
                        datafilter['academic_year'] = academic_year
                    if class_id:
                        datafilter['class_id'] = class_id
                    if class_group_id:
                        datafilter['class_group_id'] = class_group_id
                    if student_roll:
                        datafilter['student_roll'] = student_roll
                    if student_roll:
                        if Student_Seat_plane.objects.filter(**datafilter).exists():
                            data['error_message'] = 'This Student Info Allready Created'
                            return JsonResponse(data)
                        post = form.save(commit=False)
                        post.app_user_id = request.session["app_user_id"]
                        post.app_data_time = timezone.now()
                        post.save()
                        data['form_is_valid'] = True
                        data['success_message'] = 'Student Seat Plane Info Added Successfully!'
                    else:
                        students = Students_Info.objects.filter(**datafilter)

                        for student in students:
                            datafilter['student_roll'] = student.student_roll
                            if Student_Seat_plane.objects.filter(**datafilter).exists():
                                pass
                            else:
                                form = StudentSeatPlaneModelForm(request.POST)
                                post = form.save(commit=False)
                                post.app_user_id = request.session["app_user_id"]
                                post.app_data_time = timezone.now()
                                post.student_roll = student
                                post.save()
                        data['form_is_valid'] = True
                        data['success_message'] = 'Student Seat Plane Info Added Successfully!'

            except Exception as e:
                data['error_message'] = str(e)
                data['form_is_valid'] = False
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_seat_plane_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Student_Seat_plane, id=id)
    template_name = 'edu/edu-seat-plane-edit.html'
    data = dict()

    if request.method == 'POST':
        form = StudentSeatPlaneModelForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            data['success_message'] = 'Updated Successfully!'
            data['error_message'] = 'Something Went Wrong!'
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = StudentSeatPlaneModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)

# ((((((((((((((((((Students Name plate))))))))))))))))))


class edu_name_plate(TemplateView):
    template_name = 'edu/edu-name-plate.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = StudentNamePlateModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_nameplate_searchstudent(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    template_name = 'edu/edu-nameplate-searchstudent.html'
    context = get_global_data(request)
    data = dict()
    if request.method == 'POST':
        datafilter = dict()
        academic_year = request.POST.get('academic_year')
        class_id = request.POST.get('class_id')
        class_group_id = request.POST.get('class_group_id')
        student_roll = request.POST.get('student_roll')
        if academic_year:
            datafilter['academic_year'] = academic_year
        if class_id:
            datafilter['class_id'] = class_id
        if class_group_id:
            datafilter['class_group_id'] = class_group_id
        if student_roll:
            datafilter['student_roll'] = student_roll
        students = Students_Info.objects.filter(**datafilter)
        context['students'] = students
        context['datafilter'] = datafilter
    data['html_form'] = render_to_string(
        template_name, context, request=request)
    return JsonResponse(data)


@transaction.atomic
def edu_nameplate_studentinsert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = {}
    if request.method == 'POST':
        try:
            with transaction.atomic():
                datafilter = dict()
                class_group_id = ""
                academic_year = get_object_or_404(
                    Academic_Year, pk=request.POST.get('academic_year'))
                class_id = get_object_or_404(
                    Academic_Class, class_id=request.POST.get('class_id'))
                slogan = request.POST.get('slogan')
                if academic_year:
                    datafilter['academic_year'] = academic_year.pk
                if class_id:
                    datafilter['class_id'] = class_id.class_id
                if request.POST.get('class_group_id'):
                    class_group_id = get_object_or_404(
                        Academic_Class_Group, class_group_id=request.POST.get('class_group_id'))
                    datafilter['class_group_id'] = class_group_id.class_group_id
                if slogan:
                    datafilter['slogan'] = slogan
                students = request.POST.getlist('student_roll[]')
                for student_data in students:
                    student = json.loads(student_data)
                    student_status = student['student_status']
                    student_roll = student['student_roll']
                    datafilter['student_roll'] = student_roll

                    if Student_Name_Plate.objects.filter(**datafilter).exists():
                        choice = Student_Name_Plate.objects.get(**datafilter)
                        choice.student_status = student_status
                        choice.app_user_id = request.session["app_user_id"]
                        choice.save()
                    else:
                        if student_status == 'A':
                            choice = Student_Name_Plate()
                            choice.class_id = class_id
                            choice.academic_year = academic_year
                            if class_group_id:
                                choice.class_group_id = class_group_id
                            choice.student_roll = get_object_or_404(
                                Students_Info, student_roll=student_roll)
                            choice.slogan = slogan
                            choice.student_status = student_status
                            choice.app_user_id = request.session["app_user_id"]
                            choice.save()
                data['success_message'] = 'Students Name Plate Info Added Successfully'
        except Exception as e:
            logger.error("Error in Students Name Plate {} \nType: {} \nError:{}".format(
                sys.exc_info()[-1], type(e).__name__, str(e)))
            data['error_message'] = 'Error '+str(e)+' Students Name Plate!'
    return JsonResponse(data)


# ((((((((((((((((((((((((((((((((((Final Resultsheet))))))))))))))))))))))))))))))))))


class edu_resultsheet_createlist(TemplateView):
    template_name = 'edu/edu-resultsheet-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = StudentInfoModelForm()
        exam_terms = Exam_Term.objects.all()
        context = get_global_data(request)
        context['form'] = form
        context['exam_terms'] = exam_terms
        return render(request, self.template_name, context)


class edu_quick_collectionlist(TemplateView):
    template_name = 'edu/edu-quick-collectionlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        form = Students_Query_Form(
            initial={'from_date': cbd, 'upto_date': cbd})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def edu_quick_collection_cancel(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = {}
    app_user_id = request.session["app_user_id"]
    data['error_message'] = ''
    data['form_is_valid'] = False

    try:
        with transaction.atomic():

            status, error_message = fn_edu_fees_cancel(id, app_user_id)
            if not status:
                data['error_message'] = error_message
                data['form_is_valid'] = False
                return JsonResponse(data)

            data['form_is_valid'] = True
            data['success_message'] = 'Cancel Successfully!'
            return JsonResponse(data)

    except Exception as e:
        data['form_is_valid'] = False
        data['error_message'] = str(e)
        logger.error("Error on line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        return JsonResponse(data)


def edu_student_id_reset(request):
    institute = Academy_info.objects.first()
    data = []
    if institute.reset_student_id == 1:
        institute.reset_student_id = 0
        institute.save()
        Number_Gen.objects.filter(name='Student_ID').delete()
        students = Students_Info.objects.all().order_by('student_roll')

        def set_student_id(student):
            number = fn_gen_student_id(str(
                student.student_joining_date.year), student.branch_code, student.class_id.class_id)
            old_number = student.student_roll
            if not students.filter(student_roll=number).exists():
                old_data = students.filter(student_roll=old_number).get()
                old_data.delete()
                student.student_roll = number
                student.save()
            else:
                if old_number != number:
                    set_student_id(student)
        for student in students:
            if student.student_joining_date and student.branch_code and student.class_id.class_id:
                set_student_id(student)
        data.append('Reset Successfull')
    else:
        data.append('Reset Off')
    return HttpResponse(data)


class edu_fees_processing(TemplateView):
    template_name = 'edu/edu-fees-processing.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        form = Fees_Processing_Details_ModelForm(
            initial={'process_date': cbd})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def edu_fees_processing_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    proc_data = dict()
    data['form_is_valid'] = False
    try:

        if request.method == 'POST':
            form = Fees_Processing_Details_ModelForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.app_user_id = request.session["app_user_id"]
                post.app_data_time = timezone.now()
                process_id = fn_get_fees_processing_id(post.branch_code)
                post.process_id = process_id

                if post.branch_code is None or not post.branch_code:
                    data['form_is_valid'] = False
                    data['error_message'] = 'Please Select Branch Name!'
                    return JsonResponse(data)

                if post.academic_year is None or not post.academic_year:
                    data['form_is_valid'] = False
                    data['error_message'] = 'Please Select Academic Year!'
                    return JsonResponse(data)

                if post.process_date is None or not post.process_date:
                    data['form_is_valid'] = False
                    data['error_message'] = 'Please Select Process Date!'
                    return JsonResponse(data)

                proc_data["process_id"] = process_id
                proc_data["branch_code"] = post.branch_code
                proc_data["academic_year"] = post.academic_year.academic_year

                if post.class_id:
                    proc_data["class_id"] = post.class_id.class_id
                else:
                    proc_data["class_id"] = None

                if post.class_group_id:
                    proc_data["class_group_id"] = post.class_group_id.class_group_id
                else:
                    proc_data["class_group_id"] = None

                if post.section_id:
                    proc_data["section_id"] = post.section_id.section_id
                else:
                    proc_data["section_id"] = None

                if post.student_roll:
                    proc_data["student_roll"] = post.student_roll.student_roll
                else:
                    proc_data["student_roll"] = None

                proc_data["process_date"] = post.process_date
                proc_data["app_user_id"] = post.app_user_id

                if Fees_Processing_Details.objects.filter(branch_code=post.branch_code, academic_year=post.academic_year,
                                                          class_id=post.class_id, class_group_id=post.class_group_id,
                                                          section_id=post.section_id, process_date=post.process_date,
                                                          student_roll=post.student_roll, process_status=False).exists():
                    data['form_is_valid'] = False
                    data['error_message'] = 'Process Running!'
                    return JsonResponse(data)
                status, error_message = fn_fees_processing_thread(proc_data)

                if not status:
                    data['form_is_valid'] = False
                    data['error_message'] = error_message
                    return JsonResponse(data)

                post.process_status = False
                post.save()
                data['form_is_valid'] = True
                data['success_message'] = 'Process Submit Successfully!'
            else:
                data['error_message'] = form.errors.as_json()
    except Exception as e:
        data['error_message'] = str(e)
        data['form_is_valid'] = False
    return JsonResponse(data)


def edu_fess_processing_delete(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    fees_data = get_object_or_404(Fees_Processing_Details, process_id=id)
    fees_data.delete()
    data['success_message'] = 'delete successfully'
    return JsonResponse(data)


class edu_admission_form_header(TemplateView):
    template_name = 'edu/edu-admission-form-header.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')

        context = get_global_data(request)
        branch_code = request.session["branch_code"]
        is_head_office_user = request.session["is_head_office_user"]

        if is_head_office_user == 'Y':
            forms = Admission_form_header.objects.all()
            form = AdmissionFormHeaderModelForm()
        else:
            forms = Admission_form_header.objects.filter(
                branch_code=branch_code).first()
            if forms:
                form = AdmissionFormHeaderModelForm(instance=forms)
            else:
                form = AdmissionFormHeaderModelForm()

        context['form'] = form
        context['forms'] = forms
        return render(request, self.template_name, context)


def edu_admission_form_header_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    branch_code = request.session["branch_code"]
    is_head_office_user = request.session["is_head_office_user"]
    if request.method == 'POST':
        if is_head_office_user == 'Y':
            form = AdmissionFormHeaderModelForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                Admission_form_header.objects.filter(
                    branch_code=post.branch_code).delete()
                post.app_user_id = request.session["app_user_id"]
                post.logo = request.FILES.get('logo')
                post.save()
                data['form_is_valid'] = True
                data['success_message'] = 'Added Successfully!'
            else:
                data['error_message'] = form.errors.as_json()

        else:
            forms = Admission_form_header.objects.filter(
                branch_code=branch_code).first()
            if forms:
                form = AdmissionFormHeaderModelForm(
                    request.POST, instance=forms)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    if(request.FILES.get('logo')):
                        post.logo = request.FILES.get('logo')
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Application Setting Info Added Successfully!'
                else:
                    data['error_message'] = form.errors.as_json()
            else:
                form = AdmissionFormHeaderModelForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.logo = request.FILES.get('logo')
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Added Successfully!'
                else:
                    data['error_message'] = form.errors.as_json()
    return redirect('/edu-admission-form-header')


############id crad header form############

class edu_idcard_form_header(TemplateView):
    template_name = 'edu/edu-idcard-form-header.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')

        context = get_global_data(request)
        branch_code = request.session["branch_code"]
        is_head_office_user = request.session["is_head_office_user"]

        if is_head_office_user == 'Y':
            forms = IdCard_form_header.objects.all()
            form = IdCardFormHeaderModelForm()
        else:
            forms = IdCard_form_header.objects.filter(
                branch_code=branch_code).first()
            if forms:
                form = IdCardFormHeaderModelForm(instance=forms)
            else:
                form = IdCardFormHeaderModelForm()

        context['form'] = form
        context['forms'] = forms
        return render(request, self.template_name, context)


def edu_idcard_form_header_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    data = dict()
    data['form_is_valid'] = False

    is_head_office_user = request.session["is_head_office_user"]
    if request.method == 'POST':
        if is_head_office_user == 'Y':
            form = IdCardFormHeaderModelForm(request.POST)
            branch_code = request.POST.get("branch_code")
            if IdCard_form_header.objects.filter(branch_code=branch_code).exists():
                idCardData = IdCard_form_header.objects.filter(
                    branch_code=branch_code).first()
                if form.is_valid():
                    post = form.save(commit=False)
                    idCardData.academic_name = post.academic_name
                    idCardData.logo = request.FILES.get('logo')
                    idCardData.sing = request.FILES.get('sing')
                    idCardData.address = post.address
                    idCardData.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Added Successfully!'
                else:
                    data['error_message'] = form.errors.as_json()
                    idCardData.academic_name
            else:
                if form.is_valid():
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.logo = request.FILES.get('logo')
                    post.sing = request.FILES.get('sing')
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Added Successfully!'
                else:
                    data['error_message'] = form.errors.as_json()

        else:
            branch_code = request.session["branch_code"]
            forms = IdCard_form_header.objects.filter(
                branch_code=branch_code).first()
            if forms:
                form = IdCardFormHeaderModelForm(
                    request.POST, instance=forms)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    if(request.FILES.get('logo')):
                        post.logo = request.FILES.get('logo')
                    if(request.FILES.get('sing')):
                        post.sing = request.FILES.get('sing')
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Application Setting Info Added Successfully!'
                else:
                    data['error_message'] = form.errors.as_json()
            else:
                form = IdCardFormHeaderModelForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.logo = request.FILES.get('logo')
                    post.sing = request.FILES.get('sing')
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Added Successfully!'
                else:
                    data['error_message'] = form.errors.as_json()
    return redirect('/edu-idcard-form-header')


########### students migrations ###########
class edu_stdent_migration_createform(TemplateView):
    template_name = 'edu/edu-student_migration-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = student_migration_historyForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_students_migrations(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    if request.method == 'POST':
        form = student_migration_historyForm(request.POST)
        
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        
        student_rolls = request.POST.getlist('selected_students[]')
        
        if request.POST.get('class_id'):
            class_id = get_object_or_404(
                Academic_Class, class_id=request.POST.get('class_id'))

        if request.POST.get('academic_year'):
            academic_year = get_object_or_404(
                Academic_Year, academic_year=request.POST.get('academic_year'))

        if request.POST.get('class_group'):
            class_group_id = get_object_or_404(
                Academic_Class_Group, class_group_id=request.POST.get('class_group'))
        else:
            class_group_id = None

        if request.POST.get('section'):
            section_id = get_object_or_404(
                Section_Info, section_id=request.POST.get('section'))
        else:
            section_id = None

        for role in student_rolls:
            student = get_object_or_404(Students_Info, student_roll=role)
            #Set History
            post = student_migration_history()
            post.app_user_id = app_user_id
            post.student_roll = student
            #from 
            post.from_accademic_year = student.academic_year
            post.from_class = student.class_id
            post.from_class_group = student.class_group_id
            post.from_section = student.section_id
            #To
            post.to_accademic_year = academic_year
            post.to_class = class_id
            post.to_class_group = class_group_id
            post.to_section = section_id
            post.comments = request.POST.get('comments')
            post.save()
            
            student.academic_year = academic_year
            student.class_id = class_id
            student.class_group_id = class_group_id
            student.section_id = section_id
            student.save()

        message = " Student Migrations Successfully!"
        data['success_message'] = message
        data['form_is_valid'] = True
        return JsonResponse(data)
    else:
        data['error_message'] = form.errors.as_json()
        return JsonResponse(data)


class edu_teacherlist_view(TemplateView):
    template_name = 'edu/edu-teacher-list.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        context = get_global_data(request)
        forms = edu_teachersearch_Form()
        context['forms'] = forms
        return render(request, self.template_name, context)


def edu_teacherlist_edit(request, id):

    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Teacher, teacher_id=id)
    template_name = 'edu/edu-teacherlist-edit.html'
    data = dict()

    if request.method == 'POST':
        form = edu_teacherForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            app_user_id = request.session["app_user_id"]
            obj = form.save(commit=False)
            obj.app_user_id = app_user_id
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
        form = edu_teacherForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


# subject mapping teacher

class edu_submapping_teacher_createlist(TemplateView):
    template_name = 'edu/edu-subject-maping-teacher.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = SubjectmapingteacherModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_submapping_teacher_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = SubjectmapingteacherModelForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Academic Year Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)

def edu_teacherlists_edit(request, id):
    print('edit', id)
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(subject_mapping_teacher, id=id)
    template_name = 'edu/edu-submapping-teacher-edit.html'
    data = dict()

    if request.method == 'POST':
        form = SubjectmapingteacherModelForm(
            request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            app_user_id = request.session["app_user_id"]
            obj = form.save(commit=False)
            obj.app_user_id = app_user_id
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
        form = SubjectmapingteacherModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


class edu_hefz_exam_markenrty_form(TemplateView):
    template_name = 'edu/edu-hefz-exam-markentry-form.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        
        form = ExamMarksDetailsForm()
        context = get_global_data(request)
        subjects=Subject_List.objects.values('subject_name').filter(
             Q(class_id__class_name='Moktob') | Q(class_id__class_name='Hefz')
             | Q(class_id__class_name='Najera')
             | Q(class_id__class_name='Nursery')
             ).annotate(Count('subject_name')).order_by('subject_name')
        
        context['form'] = form
        context['subjects'] = subjects
        return render(request, self.template_name, context)

class edu_hefz_mark_position_form(TemplateView):
    template_name = 'edu/edu-hefz-mark-position-form.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        
        form = ExamMarksDetailsForm()
        context = get_global_data(request)
        subjects=Subject_List.objects.values('subject_name').filter(
             Q(class_id__class_name='Moktob') | Q(class_id__class_name='Hefz')
             | Q(class_id__class_name='Najera')
             | Q(class_id__class_name='Nursery')
             ).annotate(Count('subject_name')).order_by('subject_name')
        
        context['form'] = form
        context['subjects'] = subjects
        return render(request, self.template_name, context)
def edu_hefz_students_for_markentry(request):
    template_name = "edu/edu-hefz-rsult-table-beforepublish.html"
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    if request.method == 'POST':
        branch_code = request.POST.get('branch_code')
        academic_year = request.POST.get('academic_year')
        term_id = request.POST.get('term_id')
        class_name = request.POST.get('class_name')
        subject_name = request.POST.get('subject_name')
        data=dict()
        class_group_ids=[]
        class_ids=[]
        subject_list=[]
        exam_ids=[]
        subjects=""
        students=""
        exams=""
        if class_name == 'Moktob' or class_name == 'Najera' or class_name == 'Hefz':
            students=Students_Info.objects.filter(
                branch_code=branch_code,
                academic_year=academic_year,
                class_id__class_name=class_name,
                student_status='A'
                ).order_by('class_roll')
        elif class_name =='Nursery':
            students=Students_Info.objects.filter(
                branch_code=branch_code,
                academic_year=academic_year,
                class_id__class_name=class_name,
                class_group_id__class_group_name='None',
                student_status='A'
                ).order_by('class_roll')
        else:
            students=Students_Info.objects.filter(
                branch_code=branch_code,
                academic_year=academic_year,
                class_group_id__class_group_name=class_name,
                student_status='A'
                ).order_by('class_roll')
            
        class_and_group=students.values('class_group_id','class_id').annotate(gr=Count('class_group_id'))
        
        for gr in class_and_group:
            if not gr['class_group_id'] in class_group_ids:
                class_group_ids.append(gr['class_group_id'])
            if not gr['class_id'] in class_ids:
                class_ids.append(gr['class_id'])
        
        subjects=Subject_List.objects.filter(subject_name=subject_name,class_id__in=class_ids,class_group_id__in=class_group_ids)
        for subject in subjects:
            if not subject.subject_id in subject_list:
                subject_list.append(subject.subject_id)
        
        exams=Exam_Setup.objects.filter(branch_code=branch_code,academic_year=academic_year,term_id=term_id,subject_id__in=subject_list, class_id__in=class_ids,class_group_id__in=class_group_ids)
        for exam in exams:
            if not exam.exam_id in exam_ids:
                exam_ids.append(exam.exam_id)
        marks_details=Exam_Marks_Details.objects.filter(branch_code=branch_code,academic_year=academic_year,term_id=term_id,exam_id__in=exam_ids,subject_id__in=subject_list, class_id__in=class_ids,class_group_id__in=class_group_ids)
        single_exam_marks=Exam_Single_Mark.objects.filter(branch_code=branch_code,academic_year=academic_year,term_id=term_id,exam_id__in=exam_ids,subject_id__in=subject_list, class_id__in=class_ids,class_group_id__in=class_group_ids)
        subject_marks=Exam_Marks_By_Subject.objects.filter(branch_code=branch_code,academic_year=academic_year,term_id=term_id,subject_id__in=subject_list, class_id__in=class_ids,class_group_id__in=class_group_ids)
        data['students']=list(students.values())
        data['subjects']=list(subjects.values())
        data['exams']=list(exams.values())
        data['marks_details']=list(marks_details.values())
        data['single_exam_marks']=list(single_exam_marks.values())
        data['subject_marks']=list(subject_marks.values())
    return JsonResponse(data)

@transaction.atomic
def edu_hefz_markentry_insert(request):
    data = {}
    if request.method == 'POST':
        try:
            with transaction.atomic():
                exam_id = Exam_Setup.objects.get(exam_id=request.POST.get('exam_id'))
                branch_code = request.POST.get('branch_code')
                session_id = None
                exam_no = request.POST.get('exam_no')
                class_id=request.POST.get('class_id')
                class_group_id=request.POST.get('class_group_id')
                academic_year=request.POST.get('academic_year')
                total_exam_marks = request.POST.get('total_exam_marks')
                obtain_marks = request.POST.get('obtain_marks')
                student_roll = Students_Info.objects.get(
                    student_roll=request.POST.get('student_roll'))
                if(float(obtain_marks) > float(total_exam_marks)):
                    data['error_message'] = "obtain-marks is larger fixed-total-marks"
                    return JsonResponse(data)
                mark_percent = (float(obtain_marks)/float(total_exam_marks))*100
                result_grade = Result_Grade.objects.filter(
                    lowest_mark__lte=mark_percent, highest_mark__gte=mark_percent, out_of=exam_id.class_id.out_of)


                dataFilter=dict()
                if branch_code:
                    dataFilter['branch_code']=branch_code
                if academic_year:
                    dataFilter['academic_year']=academic_year
                if session_id:
                    dataFilter['session_id']=session_id
                if student_roll:
                    dataFilter['student_roll']=student_roll.student_roll
                if class_id:
                    dataFilter['class_id']=class_id
                if class_group_id:
                    dataFilter['class_group_id']=class_group_id
                if request.POST.get('subject_id'):
                    dataFilter['subject_id']=request.POST.get('subject_id')
                if request.POST.get('exam_id'):
                    dataFilter['exam_id']=request.POST.get('exam_id')
                if exam_no:
                    dataFilter['exam_no']=exam_no

                if Exam_Marks_Details.objects.filter(**dataFilter).exists():
                    exam_marks = Exam_Marks_Details.objects.get(**dataFilter)
                    exam_marks.obtain_marks = obtain_marks
                    exam_marks.result_grade = result_grade[0].grade_name
                    exam_marks.grade_point_average = result_grade[0].result_gpa
                    exam_marks.app_user_id = request.session["app_user_id"]
                    exam_marks.save()
                else:
                    exam_marks = Exam_Marks_Details()
                    exam_marks.branch_code=int(branch_code)
                    if session_id:
                        exam_marks.session_id=exam_id.session_id
                    exam_marks.class_id = exam_id.class_id
                    exam_marks.class_group_id = student_roll.class_group_id
                    exam_marks.academic_year = exam_id.academic_year
                    exam_marks.term_id = exam_id.term_id
                    exam_marks.student_roll = student_roll
                    exam_marks.subject_id = exam_id.subject_id
                    exam_marks.exam_id = exam_id
                    exam_marks.exam_no = exam_no
                    exam_marks.total_exam_marks = total_exam_marks
                    exam_marks.obtain_marks = obtain_marks
                    exam_marks.result_grade = result_grade[0].grade_name
                    exam_marks.grade_point_average = result_grade[0].result_gpa
                    exam_marks.app_user_id = request.session["app_user_id"]
                    exam_marks.save()
                if student_roll.class_group_id:
                    class_group = student_roll.class_group_id.class_group_id
                else:
                    class_group = student_roll.class_group_id
                cursor = connection.cursor()
                cursor.callproc("fn_set_single_exam_mark", [
                    exam_id.academic_year.academic_year, int(branch_code), request.POST.get('class_id'), class_group, request.POST.get('student_roll'), request.POST.get('subject_id'), request.POST.get('exam_id'), exam_id.class_id.out_of, request.session["app_user_id"]])
                data['exam_result'] = cursor.fetchone()
                
                cursor = connection.cursor()
                cursor.callproc("fn_set_subject_mark_by_student", [
                    exam_id.academic_year.academic_year,
                     request.POST.get('term_id'), 
                     None, 
                     request.POST.get('class_id'), 
                     class_group, 
                     request.POST.get('student_roll'), 
                     request.POST.get('subject_id'), 
                     request.session["app_user_id"]])
                data['subject_result'] = cursor.fetchone()

                data['exam'] = {'no_of_exam': exam_id.no_of_exam,
                                'cal_condition': exam_id.cal_condition}
                data['result_grade'] = str(exam_marks.result_grade)
                # data['result_grade']={'result_grade':exam_marks.result_grade}
                data['grade_point'] = str(exam_marks.grade_point_average)
        except Exception as e:
                logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                data['error_message'] = str(e)
                return JsonResponse(data)
    return JsonResponse(data)
@transaction.atomic
class Hefz_Result_Process_Thread(Thread):
    def run(self):
        try:
            with transaction.atomic():
                app_user_id=self.data['app_user_id']
                branch_code=self.data['branch_code']
                academic_year=self.data['academic_year']
                class_name=self.data['class_name']
                term_id=self.data['term_id']
                students=""
                subjects=""
                class_group_ids=[]
                class_ids=[]
                subject_list=[]
                if class_name == 'Moktob' or class_name == 'Najera' or class_name == 'Hefz':
                    students=Students_Info.objects.filter(
                        branch_code=branch_code,
                        academic_year=academic_year,
                        class_id__class_name=class_name,
                        student_status='A'
                        ).order_by('class_roll')
                    none_group_subjects=Subject_List.objects.filter(class_id__class_name=class_name,class_group_id__class_group_name='None')
                    subject_name=[]
                    for ngs in none_group_subjects:
                        subject_name.append(ngs.subject_name)
                    subjects=Subject_List.objects.filter(class_id__class_name=class_name,subject_name__in=subject_name)
                elif class_name =='Nursery':
                    students=Students_Info.objects.filter(
                        branch_code=branch_code,
                        academic_year=academic_year,
                        class_id__class_name=class_name,
                        class_group_id__class_group_name='None',
                        student_status='A'
                        ).order_by('class_roll')
                    subjects=Subject_List.objects.filter(class_id__class_name=class_name,class_group_id__class_group_name='None')
                else:
                    students=Students_Info.objects.filter(
                        branch_code=branch_code,
                        academic_year=academic_year,
                        class_group_id__class_group_name=class_name,
                        student_status='A'
                        ).order_by('class_roll')
                    NoneGroupSubjects=Subject_List.objects.exclude(class_group_id='000032').filter(class_group_id__class_group_name='None').values('subject_id','subject_name')
                    none_group_subject_name=[]
                    for ngs in NoneGroupSubjects:
                        if not ngs['subject_name'] in none_group_subject_name:
                            none_group_subject_name.append(ngs['subject_name'])
                    subjects=Subject_List.objects.filter(class_group_id__class_group_name=class_name).exclude(subject_name__in=none_group_subject_name)
                    
                    
                class_and_group=students.values('class_group_id','class_id').annotate(gr=Count('class_group_id'))
        
                for gr in class_and_group:
                    if not gr['class_group_id'] in class_group_ids:
                        class_group_ids.append(gr['class_group_id'])
                    if not gr['class_id'] in class_ids:
                        class_ids.append(gr['class_id'])
                
                for subject in subjects:
                    if not subject.subject_id in subject_list:
                        subject_list.append(subject.subject_id)
                
                Exam_Marks_Final_Hefz.objects.filter(
                    branch_code=branch_code,
                    academic_year=academic_year,
                    term_id=term_id,
                    class_name=class_name
                    ).delete()
                
                for stud in students:
                    allsubject_mark=Exam_Marks_By_Subject.objects.filter(student_roll=stud.student_roll,academic_year=academic_year,term_id=term_id,subject_id__in= subject_list)
                    total_result=allsubject_mark.values('student_roll','out_of').annotate(
                        total_marks=Sum('total_exam_marks'),
                        total_obtain_marks=Sum('obtain_marks'),
                        total_subject=Count('student_roll'),
                        total_gpa=Sum('grade_point_average'),

                        )
                    faild_subject=allsubject_mark.filter(result_grade='F',student_roll=stud.student_roll).exists()
                    
                    if total_result:
                        
                        final_gpa= total_result[0]['total_gpa']/total_result[0]['total_subject']
                        cursor = connection.cursor()
                        cursor.callproc("fn_get_grade_nameby_point",
                        [final_gpa,total_result[0]['out_of']])
                        result_grade = cursor.fetchone()
                       
                        first_result=allsubject_mark.first()
                        final_result=Exam_Marks_Final_Hefz()
                        final_result.branch_code=branch_code
                        final_result.academic_year=first_result.academic_year
                        final_result.term_id=first_result.term_id
                        final_result.class_name=class_name
                        final_result.student_roll=stud
                        final_result.total_exam_marks=total_result[0]['total_marks']
                        final_result.obtain_marks=total_result[0]['total_obtain_marks']
                        if faild_subject:
                            final_result.grade_point_average=0
                            final_result.result_grade='F'
                        else:
                            final_result.grade_point_average=final_gpa
                            final_result.result_grade=result_grade[0]
                        final_result.app_user_id=app_user_id
                        final_result.save()
                #Merit Position
                
                total_marks=Exam_Marks_Final_Hefz.objects.values('student_roll').annotate(mark=Sum('obtain_marks'), gpa=Sum(
                    'grade_point_average')).filter(branch_code=branch_code,
                    academic_year=academic_year,
                    term_id=term_id,
                    class_name=class_name)
                total_mark = list(total_marks)
                total_mark.sort(key=lambda x: (
                    x['gpa'], x['mark']), reverse=True)
                position = 1
                for index, m in enumerate(total_mark):
                    f_exam_mark = Exam_Marks_Final_Hefz.objects.filter(branch_code=branch_code,
                    academic_year=academic_year,
                    term_id=term_id,
                    class_name=class_name,student_roll=m['student_roll']).first()
                    if f_exam_mark:
                        if f_exam_mark.grade_point_average > 0:
                            f_exam_mark.merit_position = position
                            position += 1
                        else:
                            f_exam_mark.merit_position = 0
                        f_exam_mark.save()
                # print(subject_list)
                # print(class_ids)
                # cursor = connection.cursor()
                # cursor.callproc("fn_edu_result_processing_final",
                # [])
                # status = cursor.fetchone()
                 
                process=Process_Status_History.objects.filter(process_id=self.process_id).first()
                process.status='Finish'
                process.save()
                
        except Exception as e:
            print(e)
            process = Process_Status_History.objects.filter(process_id=self.process_id).first()
            process.status = 'Fail'
            process.save()

@transaction.atomic
class Hefz_Result_Position_Thread(Thread):
    def run(self):
        try:
            with transaction.atomic():
                app_user_id=self.data['app_user_id']
                branch_code=self.data['branch_code']
                academic_year=self.data['academic_year']
                class_name=self.data['class_name']
                term_id=self.data['term_id']
                subjects=self.data['subjects']
                dataFilter={
                    'branch_code':branch_code,
                    'academic_year':academic_year,
                    'class_name':class_name,
                    'term_id':term_id,
                }
                subject_names=[]
                for subject in subjects:
                        subject = json.loads(subject)
                        subject_names.append(subject['subject'])
                
                if class_name == 'Moktob' or class_name == 'Najera' or class_name == 'Hefz' or class_name =='Nursery':
                    subject_results=Exam_Marks_By_Subject.objects.filter(
                    branch_code=branch_code,
                    academic_year=academic_year,
                    term_id=term_id,
                    class_id__class_name=class_name,
                    class_group_id__class_group_name='None',
                    subject_id__subject_name__in=subject_names
                )
                else:
                    subject_results=Exam_Marks_By_Subject.objects.filter(
                    branch_code=branch_code,
                    academic_year=academic_year,
                    term_id=term_id,
                    class_group_id__class_group_name=class_name,
                    subject_id__subject_name__in=subject_names
                    )
                    
                # print(subject_results)
                Result_Position_Temp.objects.filter(app_user_id=app_user_id).delete()
                get_students=[]
                for student in subject_results:
                    if not student.student_roll.student_roll in get_students:
                        get_students.append(student.student_roll.student_roll)
                        result_position_temp=Result_Position_Temp()
                        result_position_temp.branch_code=branch_code
                        result_position_temp.student_roll=student.student_roll
                        class_roll=student.student_roll.class_roll
                        result_position_temp.class_roll=class_roll if class_roll else 0
                                                
                        for count, subject in enumerate(subject_names,start=1):
                            student_subjectResult=subject_results.filter(
                                student_roll=student.student_roll.student_roll,
                                subject_id__subject_name=subject).first()
                            if student_subjectResult:
                                if count == 1:
                                    result_position_temp.subject_1=student_subjectResult.obtain_marks
                                elif count == 2:
                                    result_position_temp.subject_2=student_subjectResult.obtain_marks
                                elif count == 3:
                                    result_position_temp.subject_3=student_subjectResult.obtain_marks
                                elif count == 4:
                                    result_position_temp.subject_4=student_subjectResult.obtain_marks
                                elif count == 5:
                                    result_position_temp.subject_5=student_subjectResult.obtain_marks
                                elif count == 6:
                                    result_position_temp.subject_6=student_subjectResult.obtain_marks
                                elif count == 7:
                                    result_position_temp.subject_7=student_subjectResult.obtain_marks
                                elif count == 8:
                                    result_position_temp.subject_8=student_subjectResult.obtain_marks
                                elif count == 9:
                                    result_position_temp.subject_9=student_subjectResult.obtain_marks
                                elif count == 10:
                                    result_position_temp.subject_10=student_subjectResult.obtain_marks
                                elif count == 11:
                                    result_position_temp.subject_11=student_subjectResult.obtain_marks
                                elif count == 12:
                                    result_position_temp.subject_12=student_subjectResult.obtain_marks
                                elif count == 13:
                                    result_position_temp.subject_13=student_subjectResult.obtain_marks
                                elif count == 14:
                                    result_position_temp.subject_14=student_subjectResult.obtain_marks
                        final_results=Exam_Marks_Final_Hefz.objects.filter(**dataFilter,student_roll=student.student_roll.student_roll).first()
                        if final_results:
                            result_position_temp.total_marks=final_results.total_exam_marks
                            result_position_temp.obtain_marks=final_results.obtain_marks
                            result_position_temp.result_grade=final_results.result_grade
                            result_position_temp.grade_point=final_results.grade_point_average
                            result_position_temp.app_user_id=app_user_id
                            result_position_temp.save()
                if not subject_names:
                    final_results=Exam_Marks_Final_Hefz.objects.filter(**dataFilter)
                    for final_result in final_results:
                        result_position_temp=Result_Position_Temp()
                        result_position_temp.branch_code=branch_code
                        result_position_temp.student_roll=final_result.student_roll
                        class_roll=final_result.student_roll.class_roll
                        result_position_temp.class_roll=class_roll if class_roll else 0
                        result_position_temp.total_marks=final_result.total_exam_marks
                        result_position_temp.obtain_marks=final_result.obtain_marks
                        result_position_temp.result_grade=final_result.result_grade
                        result_position_temp.grade_point=final_result.grade_point_average
                        result_position_temp.app_user_id=app_user_id
                        result_position_temp.save()
                # fn_edu_result_position_set
                cursor = connection.cursor()
                cursor.callproc("fn_edu_result_position_set",
                [branch_code,app_user_id])
                status = cursor.fetchone()
                print(status)
                if status[0] == 'S':
                    result_positions= Result_Position_Temp.objects.filter(branch_code=branch_code,app_user_id=app_user_id)
                    for position in result_positions:
                        final_result=Exam_Marks_Final_Hefz.objects.filter(**dataFilter,student_roll=position.student_roll.student_roll).first()
                        final_result.merit_position=position.merit_position
                        final_result.save()
                    result_positions.delete()
                process=Process_Status_History.objects.filter(process_id=self.process_id).first()
                process.status='Finish'
                process.save()
                
        except Exception as e:
            print(e)
            process = Process_Status_History.objects.filter(process_id=self.process_id).first()
            process.status = 'Fail'
            process.save()


@transaction.atomic
def edu_hefz_mark_process(request):
    data = {}
    if request.method == 'POST':
        try:
            with transaction.atomic():
                branch_code = request.POST.get('branch_code')
                academic_year=request.POST.get('academic_year')
                term_id=request.POST.get('term_id')
                class_name=request.POST.get('class_name')
                dataFilter={
                    'branch_code':branch_code,
                    'academic_year':academic_year,
                    'class_name':class_name,
                    'term_id':term_id,
                    'app_user_id':request.session["app_user_id"]
                }
                process_id =request.POST.get('process_id')
                t1=Hefz_Result_Process_Thread()
                t1.data=dataFilter
                t1.process_id=process_id
                t1.start()
    
                data['success_message'] = 'Result process started. \n Please wait few minutes. '
                data['error_message'] = ''
                data['form_is_valid'] = True
        except Exception as e:
                logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                data['error_message'] = str(e)
                return JsonResponse(data)
    return JsonResponse(data)
@transaction.atomic
def edu_hefz_mark_position_process(request):
    data = {}
    if request.method == 'POST':
        try:
            with transaction.atomic():
                branch_code = request.POST.get('branch_code')
                academic_year=request.POST.get('academic_year')
                term_id=request.POST.get('term_id')
                class_name=request.POST.get('class_name')
                subjects = request.POST.getlist('subjects[]')
                dataFilter={
                    'branch_code':branch_code,
                    'academic_year':academic_year,
                    'class_name':class_name,
                    'term_id':term_id,
                    'app_user_id':request.session["app_user_id"],
                    'subjects':subjects
                }
                # print(dataFilter)
                process_id =request.POST.get('process_id')
                t1=Hefz_Result_Position_Thread()
                t1.data=dataFilter
                t1.process_id=process_id
                t1.start()
    
                data['success_message'] = 'Result process started. \n Please wait few minutes. '
                data['error_message'] = ''
                data['form_is_valid'] = True
        except Exception as e:
                logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                data['error_message'] = str(e)
                return JsonResponse(data)
    return JsonResponse(data)

@transaction.atomic
def edu_result_view_template1_hefz(request):
    if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
    data=dict()
    if request.method == 'POST':
        try:
            with transaction.atomic():
                data['success_message'] = 'Create Successfully!'
                data['error_message'] = ''
                data['form_is_valid'] = True
                return JsonResponse(data)

        except Exception as e:
                logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                data['error_message'] = str(e)
                return JsonResponse(data)
    else:
        template_name = 'edu/edu-result-view-template1-hefz.html'
        branch_code = request.GET.get('branch_code')
        academic_year=request.GET.get('academic_year')
        term_id=request.GET.get('term_id')
        class_name=request.GET.get('class_name')
        dataFilter={
            'branch_code':branch_code,
            'academic_year':academic_year,
            'class_name':class_name,
            'term_id':term_id,
        }
        formHeader=Admission_form_header.objects.filter(branch_code=branch_code).first()
        result_info=Exam_Marks_Final_Hefz.objects.filter(**dataFilter).first()

        context = get_global_data(request)
        context['formHeader'] = formHeader
        context['result_info'] = result_info
        return render(request, template_name, context)

    return JsonResponse(data)

@transaction.atomic
def edu_hefz_mark_final_data(request):
    data = {}
    if request.method == 'POST':
        try:
            with transaction.atomic():
                branch_code = request.POST.get('branch_code')
                academic_year=request.POST.get('academic_year')
                term_id=request.POST.get('term_id')
                class_name=request.POST.get('class_name')
                dataFilter={
                    'branch_code':branch_code,
                    'academic_year':academic_year,
                    'class_name':class_name,
                    'term_id':term_id,
                }
                
                final_results=Exam_Marks_Final_Hefz.objects.values(
                    'academic_year','class_name','student_roll',
                    'student_roll__student_name',
                    'student_roll__class_roll',
                    'total_exam_marks',
                    'obtain_marks',
                    'result_grade',
                    'grade_point_average',
                    'merit_position'

                ).filter(**dataFilter).order_by('-grade_point_average','merit_position')
                subjects=""
                if class_name == 'Moktob' or class_name == 'Najera' or class_name == 'Hefz':
                    none_group_subjects=Subject_List.objects.filter(class_id__class_name=class_name,class_group_id__class_group_name='None')
                    ng_subject_name=[]
                    for ngs in none_group_subjects:
                        ng_subject_name.append(ngs.subject_name)
                    subjects=Subject_List.objects.filter(class_id__class_name=class_name,subject_name__in=ng_subject_name)
                elif class_name =='Nursery':
                    subjects=Subject_List.objects.filter(class_id__class_name=class_name,class_group_id__class_group_name='None')
                else:
                    NoneGroupSubjects=Subject_List.objects.exclude(class_group_id='000032').filter(class_group_id__class_group_name='None').values('subject_id','subject_name')
                    none_group_subject_name=[]
                    for ngs in NoneGroupSubjects:
                        if not ngs['subject_name'] in none_group_subject_name:
                            none_group_subject_name.append(ngs['subject_name'])
                    subjects=Subject_List.objects.filter(class_group_id__class_group_name=class_name).exclude(subject_name__in=none_group_subject_name)
                subject_names=[]
                subject_list=[]
                for sub in subjects:
                    if not sub.subject_id in subject_list:
                        subject_list.append(sub.subject_id)
                    if not sub.subject_name in subject_names:
                        subject_names.append(sub.subject_name)
                subject_results=Exam_Marks_By_Subject.objects.filter(
                    branch_code=branch_code,
                    academic_year=academic_year,
                    term_id=term_id,
                    subject_id__subject_name__in=subject_names
                )
                sub_result_values= subject_results.values('student_roll','total_exam_marks','obtain_marks','result_grade','grade_point_average','subject_id__subject_name')
                data['final_results']= list(final_results)
                data['subject_results']= list(sub_result_values)
                data['subject_names']= subject_names
                return JsonResponse(data)
        except Exception as e:
                logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                data['error_message'] = str(e)
                return JsonResponse(data)
    return JsonResponse(data)
 
@transaction.atomic
def edu_hefz_marksheet_data(request):
    data = {}
    if request.method == 'POST':
        try:
            with transaction.atomic():
                branch_code = request.POST.get('branch_code')
                academic_year=request.POST.get('academic_year')
                term_id=request.POST.get('term_id')
                class_name=request.POST.get('class_name')
                dataFilter={
                    'branch_code':branch_code,
                    'academic_year':academic_year,
                    'class_name':class_name,
                    'term_id':term_id,
                }
                formHeader=Admission_form_header.objects.filter(branch_code=branch_code)
                subjects=""
                none_group_subject_name=[]
                if class_name == 'Moktob' or class_name == 'Najera' or class_name == 'Hefz' or class_name =='Nursery':
                    subjects=Subject_List.objects.filter(class_id__class_name=class_name,class_group_id__class_group_name='None')
                else:
                    NoneGroupSubjects=Subject_List.objects.exclude(class_group_id='000032').filter(class_group_id__class_group_name='None').values('subject_id','subject_name')
                    for ngs in NoneGroupSubjects:
                        if not ngs['subject_name'] in none_group_subject_name:
                            none_group_subject_name.append(ngs['subject_name'])
                    subjects=Subject_List.objects.filter(class_group_id__class_group_name=class_name)
                
                subject_ids=[]
                subject_names=[]
                for sub in subjects:
                    if not sub.subject_id in subject_ids:
                        subject_ids.append(sub.subject_id)
                    if not sub.subject_name in subject_names:
                        subject_names.append(sub.subject_name)
                
                subject_results=Exam_Marks_By_Subject.objects.filter(
                    branch_code=branch_code,
                    academic_year=academic_year,
                    term_id=term_id,
                    subject_id__in=subject_ids
                )
                get_students=[]
                for student in subject_results:
                    if not student.student_roll.student_roll in get_students:
                        get_students.append(student.student_roll.student_roll)
                
                final_results=Exam_Marks_Final_Hefz.objects.values(
                    'academic_year','class_name','student_roll',
                    'total_exam_marks',
                    'obtain_marks',
                    'result_grade',
                    'grade_point_average',
                    'merit_position',
                    'term_id__term_name',
                    student_name=F('student_roll__student_name'),
                    father_name=F('student_roll__student_father_name'),
                    mother_name=F('student_roll__student_mother_name'),
                    class_roll=F('student_roll__class_roll'),
                    date_of_birth=F('student_roll__student_date_of_birth'),
                    img=F('student_roll__profile_image')
                ).filter(**dataFilter,student_roll__in=get_students).order_by('-grade_point_average','merit_position')
                sub_result_values= subject_results.values('student_roll','total_exam_marks',
                'obtain_marks','result_grade','grade_point_average',
                'subject_id','out_of',
                group_name=F('class_group_id__class_group_name'),
                subject_name=F('subject_id__subject_name')
                ).order_by('subject_name')
                out_of=sub_result_values.first()
                if out_of:
                    out_of=out_of['out_of']
                    result_grade=Result_Grade.objects.filter(out_of=out_of)
                    data['result_grades']= list(result_grade.values())
                data['final_results']= list(final_results)
                data['subject_results']= list(sub_result_values)
                data['subject_names']= subject_names
                data['form_header']= list(formHeader.values())[0]
                data['none_group_subjects']= none_group_subject_name
                logo=formHeader.first()
                data['logo']= logo.logo.url if logo.logo else ""
                return JsonResponse(data)
        except Exception as e:
                logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                data['error_message'] = str(e)
                return JsonResponse(data)
    return JsonResponse(data)
 

class edu_hefz_result_form(TemplateView):
    template_name = 'edu/edu-hefz-result-form.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        
        form = ExamMarksDetailsForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def edu_hefz_result_before_publish_data(request):
    template_name = "edu/edu-hefz-rsult-table-beforepublish.html"
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    if request.method == 'POST':
        branch_code = request.POST.get('branch_code')
        academic_year = request.POST.get('academic_year')
        term_id = request.POST.get('term_id')
        class_name = request.POST.get('class_name')
        limit = request.POST.get('limit')
        page = request.POST.get('page')
        json = request.POST.get('json')
        with_position = request.POST.get('with_position')
        app_user_id = request.session["app_user_id"]
        datafilter = dict()
        datafilter['academic_year'] = academic_year
        datafilter['term_id'] = term_id
        datafilter['branch_code'] = branch_code
        
        if class_name == 'Moktob' or class_name == 'Najera' or class_name == 'Hefz' or class_name == 'Nursery':
            datafilter['class_id__class_name'] = class_name
  
        data = dict()
        results = Exam_Marks_Details.objects.filter(
            **datafilter).order_by('student_roll__class_roll')
                        
        if class_name == 'Moktob' or class_name == 'Najera' or class_name == 'Hefz' or class_name == 'Nursery':
            subject_names=results.values('subject_id__subject_name').filter(class_group_id__class_group_name='None').annotate(Count('subject_id__subject_name'))
            none_group_subject_list=[]           
            for subject in subject_names:
                if subject['subject_id__subject_name'] not in none_group_subject_list:
                    none_group_subject_list.append(subject['subject_id__subject_name'])
            results = results.filter(subject_id__subject_name__in=none_group_subject_list)
        else:
            subject_names=results.values('subject_id__subject_name').filter(class_group_id__class_group_name='None').exclude(class_id__class_name='Nursery').annotate(Count('subject_id__subject_name'))
            none_group_subject_list=[]           
            for subject in subject_names:
                if subject['subject_id__subject_name'] not in none_group_subject_list:
                    none_group_subject_list.append(subject['subject_id__subject_name'])
            results = results.exclude(subject_id__subject_name__in=none_group_subject_list).filter(class_group_id__class_group_name=class_name)
        
        subjectResults = results.values('student_roll', 'student_roll__class_roll', 'student_roll__student_name','student_roll__student_father_name','student_roll__student_mother_name', 'class_group_id__class_group_name', 'subject_id__subject_name', 'subject_id__maximum_marks', 'subject_id').annotate(
            total_sub=Count('subject_id'), total_students=Count('student_roll'),
            total=Sum('total_exam_marks'), obtain=Sum('obtain_marks'))
        
        total_result=list()
        for result in subjectResults:
            gpa = get_result_great(
                result['obtain'], result['total'], 5)
            multi_exam = results.values('exam_id','exam_id__exam_name','total_exam_marks','obtain_marks','grade_point_average','result_grade').filter(subject_id=result['subject_id'],student_roll=result['student_roll'])
            if multi_exam.count() > 1:
                result['exams'] = multi_exam 
            result['gpa'] = gpa[0]
            result['lg'] = gpa[1]
            
            check_total=next((item for item in total_result if item["student_roll"] == result['student_roll']),None)
            if check_total:
                check_total['gpa'] += gpa[0]
                check_total['subject_count'] += 1
            else:
                total_r={'student_roll':result['student_roll'],'gpa':gpa[0],'subject_count':1}
                total_result.append(total_r)
                    
        students = subjectResults.values('student_roll', 'student_roll__class_roll','student_roll__student_date_of_birth', 'student_roll__student_name','student_roll__student_father_name','student_roll__student_mother_name', 'class_group_id__class_group_name').annotate(
            subject_count=Count('student_roll'), subjectTotalMarks=Sum('total_exam_marks'), totalObtain=Sum('obtain_marks'))
        
        for s in students:
            s['total'] = s['subjectTotalMarks']
            s['obtain'] = s['totalObtain']
            check_total=next((item for item in total_result if item["student_roll"] == s['student_roll']),None)
            if check_total:
                s['gpa'] =float("%.2f" % (check_total['gpa']/check_total['subject_count']))
                gpa = fn_get_grade_nameby_point(s['gpa'], 5)
                s['lg'] = gpa[0]
            else:
                break
            for sub_result in subjectResults:
                if sub_result['student_roll'] == s['student_roll']:
                   if sub_result['lg'] == 'F':
                       s['gpa'] = 0.00
                       s['lg'] = 'F'
                       break
            
           
        if with_position == 'true':
            #Position Calculation
            position = 1
            student_list_withMarks=list(students)
            student_list_withMarks.sort(key=lambda x: (
                        x['gpa'], x['obtain']), reverse=True)
            for index, m in enumerate(student_list_withMarks):
                for st in students:
                    if st['student_roll'] == m['student_roll']:
                        if st['gpa'] > 0:
                            st['position'] = position
                            position+=1
                        else:
                            st['position'] = 0
        paginator = Paginator(students, limit)
        paginat_data = paginator.page(page)
       
        institute = Admission_form_header.objects.filter(branch_code=branch_code)
        term = Exam_Term.objects.filter(id=term_id).first()
        data['subject_results'] = subjectResults
        data['students_results'] = paginat_data
        data['class_name'] = class_name
        data['institute'] = institute.first()
        data['term'] = term.term_name
        if json:
            grade_list=Result_Grade.objects.filter(out_of=5)
            jsonData=dict()
            jsonData['subject_results']=list(subjectResults)
            jsonData['students_results']=list(paginat_data)
            jsonData['class_name']=class_name
            jsonData['institute'] = list(institute.values())
            jsonData['grade_list'] = list(grade_list.values())
            jsonData['term'] = term.term_name
            jsonData['page_info'] = str(paginat_data).replace('Page','Sheet').replace('<','_').replace('>','')
            print(class_name)
            return JsonResponse(jsonData)
    return render(request, template_name, data)

def edu_hefz_result_before_publish_data_list(request):
    template_name = "edu/edu-hefz-marks-before-publish-data-list.html"
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    if request.method == 'GET':
        branch_code = request.GET.get('branch_code')
        academic_year = request.GET.get('academic_year')
        term_id = request.GET.get('term_id')
        class_name = request.GET.get('class_name')
        limit = request.GET.get('limit')
        page = request.GET.get('page')
        app_user_id = request.session["app_user_id"]
        datafilter = dict()
        datafilter['academic_year'] = academic_year
        datafilter['term_id'] = term_id
        datafilter['branch_code'] = branch_code
        
        if class_name == 'Moktob' or class_name == 'Najera' or class_name == 'Hefz' or class_name == 'Nursery':
            datafilter['class_id__class_name'] = class_name
  
        data = dict()
        subjects=list()
        subjects_name=list()
        results = Exam_Marks_Details.objects.filter(
            **datafilter).order_by('student_roll__class_roll')
                        
        if class_name == 'Moktob' or class_name == 'Najera' or class_name == 'Hefz' or class_name == 'Nursery':
            subject_names=results.values('subject_id__subject_name').filter(class_group_id__class_group_name='None').annotate(Count('subject_id__subject_name'))
            none_group_subject_list=[]           
            for subject in subject_names:
                if subject['subject_id__subject_name'] not in none_group_subject_list:
                    none_group_subject_list.append(subject['subject_id__subject_name'])
            final_results = results.filter(subject_id__subject_name__in=none_group_subject_list)
        else:
            NoneGroupSubjects=Subject_List.objects.exclude(class_group_id='000032').filter(class_group_id__class_group_name='None').values('subject_id','subject_name')
            
            # subject_exclude=results.values('subject_id').filter(class_group_id__class_group_name='None')
            none_group_subject_list=[]       
            for subject in NoneGroupSubjects:
                if subject['subject_name'] not in none_group_subject_list:
                    none_group_subject_list.append(subject['subject_name'])
            groups=Academic_Class_Group.objects.filter(class_group_name=class_name)
            class_group_id=[]
            for group in groups:
                class_group_id.append(group.class_group_id)
            final_results = results.exclude(subject_id__subject_name__in=none_group_subject_list).filter(class_group_id__in=class_group_id)
            
        total_result=list()
        subjectResults = final_results.values('student_roll', 'student_roll__class_roll', 'student_roll__student_name', 'class_group_id__class_group_name', 'subject_id__subject_name','subject_id__sort_name', 'subject_id__maximum_marks', 'subject_id').annotate(
            total_sub=Count('subject_id'), total_students=Count('student_roll'),
            total=Sum('total_exam_marks'), obtain=Sum('obtain_marks'))
        
        for result in subjectResults:
            subData=dict()
            subData['subject_id']=result['subject_id']
            subData['subject_sort_name']=result['subject_id__sort_name']
            if not subData in subjects:
                subjects.append(subData)
                
            gpa = get_result_great(
                result['obtain'], result['total'], 5)
            multi_exam = final_results.values('exam_id','exam_id__exam_name','total_exam_marks','obtain_marks','grade_point_average','result_grade').filter(subject_id=result['subject_id'],student_roll=result['student_roll'])
            if multi_exam.count() > 1:
                result['exams'] = multi_exam 
            result['gpa'] = gpa[0]
            result['lg'] = gpa[1]
            check_total=next((item for item in total_result if item["student_roll"] == result['student_roll']),None)
            if check_total:
                check_total['gpa'] += gpa[0]
                check_total['subject_count'] += 1
            else:
                total_r={'student_roll':result['student_roll'],'gpa':gpa[0],'subject_count':1}
                total_result.append(total_r)
                
            if not result['subject_id__sort_name'] in subjects_name:
                if result['subject_id__sort_name']:
                    subjects_name.append(result['subject_id__sort_name'])
            
        students = subjectResults.values('student_roll', 'student_roll__class_roll', 'student_roll__student_name', 'class_group_id__class_group_name').annotate(
            subject_count=Count('student_roll'), subjectTotalMarks=Sum('total_exam_marks'), totalObtain=Sum('obtain_marks'))
        
        for s in students:
            s['total'] = s['subjectTotalMarks']
            s['obtain'] = s['totalObtain']
            check_total=next((item for item in total_result if item["student_roll"] == s['student_roll']),None)
            if check_total:
                s['gpa'] =float("%.2f" % (check_total['gpa']/check_total['subject_count']))
                gpa = fn_get_grade_nameby_point(s['gpa'], 5)
                s['lg'] = gpa[0]
            else:
                break
            for sub_result in subjectResults:
                if sub_result['student_roll'] == s['student_roll']:
                   if sub_result['lg'] == 'F':
                       s['gpa'] = 0.00
                       s['lg'] = 'F'
                       break
            
        
        student_list_withMarks=list(students)
        student_list_withMarks.sort(key=lambda x: (
                    x['gpa'], x['obtain']), reverse=True)
        
        position = 1
        for index, m in enumerate(student_list_withMarks):
            for st in students:
                if st['student_roll'] == m['student_roll']:
                    if st['gpa'] > 0:
                        st['position'] = position
                        position+=1
                    else:
                        st['position'] = 0
        paginator = Paginator(students, limit)
        paginat_data = paginator.page(page)
        institute = Admission_form_header.objects.filter(branch_code=branch_code).first()
        term = Exam_Term.objects.filter(id=term_id).first()
        # print(subjects)
        data['subject_results'] = subjectResults
        data['students_results'] = paginat_data
        data['institute'] = institute
        data['subjects'] = subjects
        data['subjects_name'] = subjects_name
        data['class_name'] = class_name
        data['term'] = term.term_name

    return render(request, template_name, data)

def edu_image_file_convert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    students = Students_Info.objects.all()
    for student in students:
        if student.profile_image:
            url = student.profile_image.path
            if os.path.exists(url):
                print(url)
                im = Image.open(url).convert("RGB")
                os.remove(url)
                im.save(url.replace('.webp', '.png'),'png')

    return HttpResponse("ok")

#Threding
@transaction.atomic
class Term_Result_Marge_Thread(Thread):
    def run(self):
        try:
            with transaction.atomic():
                self.data['app_user_id']
                dataFilter=dict()
                dataFilter['branch_code']=self.data['branch_code']
                dataFilter['academic_year']=self.data['academic_year']
                dataFilter['class_id']=self.data['class_id']
                dataFilter['class_group_id']=self.data['class_group_id']
                if self.data['session_id']:
                    dataFilter['session_id']=self.data['session_id']

                examData=subject_mark_with_marge.objects.filter(**dataFilter)
                resultViewSettings=result_view_setting.objects.filter(**dataFilter)
                Term_One_ViewSetting=resultViewSettings.filter(term_id=self.data['term_1'])
                Term_Two_ViewSetting=resultViewSettings.filter(term_id=self.data['term_2'])
                Term_Three_ViewSetting=resultViewSettings.filter(term_id=self.data['term_3'])
                # students=examData.values('student_roll').annotate(Count('student_roll'))
                students=Students_Info.objects.filter(**dataFilter,student_status='A')
                
                if Term_One_ViewSetting and Term_Two_ViewSetting and Term_Three_ViewSetting:
                    pass
                elif Term_One_ViewSetting and Term_Two_ViewSetting:
                    for Term_One in Term_One_ViewSetting:
                        
                        Term_Two=Term_Two_ViewSetting.filter(
                            subject_one_id=Term_One.subject_one_id,
                            subject_two_id=Term_One.subject_two_id,
                            subject_three_id=Term_One.subject_three_id
                            ).first()
                        if Term_Two:
                            Term_Result_Marge.objects.filter(**dataFilter,one_term_id=Term_One.term_id,
                            two_term_id=Term_Two.term_id,
                            one_result_view_id=Term_One.result_view_id,
                            two_result_view_id=Term_Two.result_view_id
                            ).delete()
                                                        
                            subject_total_marks=0
                            term_one_total_marks=0
                            term_two_total_marks=0
                            if Term_One.subject_one_id:
                                subject_total_marks += Term_One.subject_one_id.maximum_marks
                                term_one_total_marks += Term_One.subject_one_id.maximum_marks
                            if Term_One.subject_two_id:
                                subject_total_marks += Term_One.subject_two_id.maximum_marks
                                term_one_total_marks += Term_One.subject_two_id.maximum_marks
                            if Term_One.subject_three_id:
                                subject_total_marks += Term_One.subject_three_id.maximum_marks
                                term_one_total_marks += Term_One.subject_three_id.maximum_marks
                            
                            if Term_Two.subject_one_id:
                                subject_total_marks += Term_Two.subject_one_id.maximum_marks
                                term_two_total_marks += Term_Two.subject_one_id.maximum_marks
                            if Term_Two.subject_two_id:
                                subject_total_marks += Term_Two.subject_two_id.maximum_marks
                                term_two_total_marks += Term_Two.subject_two_id.maximum_marks
                            if Term_Two.subject_three_id:
                                subject_total_marks += Term_Two.subject_three_id.maximum_marks
                                term_two_total_marks += Term_Two.subject_three_id.maximum_marks
                            
                            count=0
                            for student in students:
                                count+=1
                                print('First Loop'+str(count))
                                term_one_result = examData.filter(result_view_id=Term_One.result_view_id,student_roll=student.student_roll).first()
                                term_two_result = examData.filter(result_view_id=Term_Two.result_view_id,student_roll=student.student_roll).first()
                                result_marge= Term_Result_Marge()
                                result_marge.branch_code= int(self.data['branch_code'])
                                result_marge.academic_year= Term_One.academic_year
                                result_marge.class_id= Term_One.class_id
                                result_marge.class_group_id= Term_One.class_group_id
                                result_marge.session_id= Term_One.session_id
                                result_marge.student_roll= student
                                out_of=0
                                is_optional=0
                                # Term One
                                result_marge.one_term_id= Term_One.term_id
                                result_marge.one_result_view_id= Term_One
                                if term_one_result:
                                    result_marge.one_total_marks= term_one_total_marks
                                    result_marge.one_obtain_marks= term_one_result.obtain_marks
                                    result_marge.one_result_grade= term_one_result.result_grade
                                    result_marge.one_grade_point= term_one_result.grade_point_average
                                    out_of=term_one_result.out_of
                                    is_optional=term_one_result.is_optional
                                else:
                                    result_marge.one_result_grade='F'
                                    result_marge.one_grade_point=0.0
                                # Term Two
                                result_marge.two_result_view_id= Term_Two
                                result_marge.two_term_id= Term_Two.term_id
                                if term_two_result:
                                    result_marge.two_total_marks= term_two_total_marks
                                    result_marge.two_obtain_marks= term_two_result.obtain_marks
                                    result_marge.two_result_grade= term_two_result.result_grade
                                    result_marge.two_grade_point= term_two_result.grade_point_average
                                    out_of=term_two_result.out_of
                                    is_optional=term_two_result.is_optional
                                else:
                                    result_marge.two_result_grade='F'
                                    result_marge.two_grade_point=0.0
                                
                                #Total
                                subject_obtain_marks= 0
                                if term_one_result and term_one_result.obtain_marks:
                                    subject_obtain_marks+=term_one_result.obtain_marks
                                    
                                if term_two_result and term_two_result.obtain_marks:
                                    subject_obtain_marks+=term_two_result.obtain_marks
                                if out_of >0:
                                    cursor = connection.cursor()
                                    cursor.callproc("fn_get_result_gpa",
                                    [subject_obtain_marks,subject_total_marks,out_of
                                    ])
                                    gpa = cursor.fetchone()
                                else:
                                    gpa=[0,'F']
                                
                                result_marge.total_marks= subject_total_marks
                                result_marge.obtain_marks= subject_obtain_marks
                                result_marge.grade_point= gpa[0]
                                result_marge.result_grade= gpa[1]
                                result_marge.is_optional= is_optional
                                result_marge.save()
                    print('loop 1 compited')
                    #Final Result Insert
                    student_results=Term_Result_Marge.objects.filter(**dataFilter,
                        one_term_id=self.data['term_1'],
                        two_term_id=self.data['term_2'])
                    term_finals=Exam_Marks_Final.objects.filter(**dataFilter)    
                    Term_Result_Marge_Final.objects.filter(**dataFilter,
                        one_term_id=self.data['term_1'],two_term_id=self.data['term_2']).delete()
                    for student in students:
                        
                        student_result=student_results.filter(student_roll=student.student_roll
                        ).values('student_roll','out_of').annotate(total_subject=Count('student_roll'),
                        one_total_marks=Sum('one_total_marks'),
                        one_obtain_marks=Sum('one_obtain_marks'),
                        two_total_marks=Sum('two_total_marks'),
                        two_obtain_marks=Sum('two_obtain_marks'),
                        total_marks=Sum('total_marks'),
                        obtain_marks=Sum('obtain_marks'),
                        grade_point=Sum('grade_point')
                        )
                        if not student_result:
                            continue
                        term_one_final=term_finals.filter(student_roll=student.student_roll,term_id=self.data['term_1']).first()
                        term_two_final=term_finals.filter(student_roll=student.student_roll,term_id=self.data['term_2']).first()
                        
                        optional_gpa_above2=0
                        optional_subject=0
                        optional_gpa=0
                        is_faild=student_results.filter(student_roll=student.student_roll,is_optional=0,result_grade='F').exists()
                        
                        if not is_faild:
                            optional=student_results.filter(student_roll=student.student_roll,is_optional=1).values('student_roll').annotate(grade_point=Sum('grade_point'),total_optional_subject=Count('is_optional'))
                            if optional:
                                optional_subject=optional[0]['total_optional_subject']
                                optional_gpa=optional[0]['grade_point']
                            if optional_gpa and (optional_gpa/optional_subject)>2:
                                optional_gpa_above2=(optional_gpa/optional_subject)-2
                        
                        subjects=(student_result[0]['total_subject']-optional_subject)
                        final_gpa=((student_result[0]['grade_point']-optional_gpa)+optional_gpa_above2)/subjects
                        if final_gpa<1:
                            final_gpa=0.0
                        final_gpa=round(final_gpa, 2)
                        grade_name='F'
                        if final_gpa > 5:
                            final_gpa=5.00
                        gpa_without_furth=(student_result[0]['grade_point']-optional_gpa)/subjects
                        if gpa_without_furth<1:
                            gpa_without_furth=0.0
                        if is_faild:
                            final_gpa=0
                            gpa_without_furth=0
                        else:
                            print(final_gpa)
                            cursor = connection.cursor()
                            cursor.callproc("fn_get_grade_nameby_point",
                            [final_gpa,student_result[0]['out_of']])
                            grade = cursor.fetchone()
                            if grade:
                                grade_name=grade[0]
                            
                        marge_final= Term_Result_Marge_Final()
                        marge_final.marge_tilte= self.data['marge_tilte']
                        marge_final.branch_code= int(self.data['branch_code'])
                        marge_final.academic_year= student.academic_year
                        marge_final.class_id= student.class_id
                        marge_final.class_group_id= student.class_group_id
                        marge_final.session_id= student.session_id
                        marge_final.student_roll= student
                        
                        #Term One
                        if term_one_final:
                            marge_final.one_term_id= term_one_final.term_id
                            marge_final.one_total_marks= term_one_final.total_exam_marks
                            marge_final.one_obtain_marks= term_one_final.obtain_marks
                            marge_final.one_result_grade= term_one_final.result_grade
                            marge_final.one_grade_point= term_one_final.grade_point_average
                        else:
                            marge_final.one_term_id= get_object_or_404(Exam_Term, id = self.data['term_1'])
                        #Term Two
                        if term_two_final:
                            marge_final.two_term_id= term_two_final.term_id
                            marge_final.two_total_marks= term_two_final.total_exam_marks
                            marge_final.two_obtain_marks= term_two_final.obtain_marks
                            marge_final.two_result_grade= term_two_final.result_grade
                            marge_final.two_grade_point= term_two_final.grade_point_average
                        else:
                            marge_final.two_term_id= get_object_or_404(Exam_Term, id = self.data['term_2'])
                        #Total
                        marge_final.total_marks= student_result[0]['total_marks']
                        marge_final.obtain_marks= student_result[0]['obtain_marks']
                        marge_final.result_grade= grade_name
                        marge_final.grade_point= final_gpa
                        marge_final.grade_point_without_furth= gpa_without_furth
                        marge_final.save()
                        print('loop 2')

                    print('loop 2 Finish')   
                    #Merit Position
                    total_marks=Term_Result_Marge.objects.values('student_roll').annotate(mark=Sum('obtain_marks'), gpa=Sum(
                        'grade_point')).filter(**dataFilter,
                            one_term_id=self.data['term_1'],
                            two_term_id=self.data['term_2'])
                    total_mark = list(total_marks)
                    total_mark.sort(key=lambda x: (
                        x['gpa'], x['mark']), reverse=True)
                    position = 1
                    for index, m in enumerate(total_mark):
                        f_exam_mark = Term_Result_Marge_Final.objects.filter(**dataFilter,
                        one_term_id=self.data['term_1'],two_term_id=self.data['term_2'],student_roll=m['student_roll']).first()
                        if f_exam_mark:
                            if f_exam_mark.grade_point > 0:
                                f_exam_mark.merit_position = position
                                position += 1
                            else:
                                f_exam_mark.merit_position = 0
                            f_exam_mark.save()
                process=Process_Status_History.objects.filter(process_id=self.process_id).first()
                process.status='Finish'
                process.save()
                print('Finish')
                
        except Exception as e:
            print(e)
            process = Process_Status_History.objects.filter(process_id=self.process_id).first()
            process.status = 'Fail'
            process.save()
            

@transaction.atomic
def edu_term_result_marge_insert(request):
    if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
    data=dict()
    if request.method == 'POST':
        try:
            with transaction.atomic():
                branch_code= request.POST.get('branch_code')
                academic_year= request.POST.get('academic_year')
                session_id= request.POST.get('session_id')
                class_id= request.POST.get('class_id')
                class_group_id= request.POST.get('class_group_id')
                term_1= request.POST.get('term_1')
                term_2= request.POST.get('term_2')
                term_3= request.POST.get('term_3')
                marge_tilte= request.POST.get('marge_tilte')

                if not class_group_id:
                    class_group_id=None
    
                if not session_id:
                    session_id=None
                dataFilter={
                    'branch_code':branch_code,
                    'academic_year':academic_year,
                    'session_id':session_id,
                    'class_id':class_id,
                    'class_group_id':class_group_id,
                    'term_1':term_1,
                    'term_2':term_2,
                    'term_3':term_3,
                    'marge_tilte':marge_tilte,
                    'app_user_id':request.session["app_user_id"]
                }
               
                process_id =request.POST.get('process_id')
                t1=Term_Result_Marge_Thread()
                t1.data=dataFilter
                t1.process_id=process_id
                t1.start()
    
                data['success_message'] = 'Result process started. \n Please wait few minutes. '
                data['error_message'] = ''
                data['form_is_valid'] = True
                print('Complete')
                return JsonResponse(data)
        except Exception as e:
                logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                data['error_message'] = str(e)
                print(str(e))
                return JsonResponse(data)
    return JsonResponse(data)
 
@transaction.atomic
def edu_term_result_marge_view_template1(request):
    if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
    data=dict()
    if request.method == 'POST':
        pass
    else:
        template_name = 'edu/edu-term-result-marge-view-template1.html'
        branch_code = request.GET.get('branch_code')
        academic_year = request.GET.get('academic_year')
        session_id = request.GET.get('session_id')
        class_id = request.GET.get('class_id')
        class_group_id = request.GET.get('class_group_id')
        term_1 = request.GET.get('term_1')
        term_2 = request.GET.get('term_2')
        

        dataFilter = dict()
        dataFilter['branch_code'] = branch_code
        dataFilter['academic_year'] = academic_year
        dataFilter['class_id'] = class_id
        dataFilter['one_term_id'] = term_1
        dataFilter['two_term_id'] = term_2
        
        if session_id:
            dataFilter['session_id'] = session_id
        if class_group_id:
            dataFilter['class_group_id'] = class_group_id
        formHeader=Admission_form_header.objects.filter(branch_code=branch_code).first()
        result_info=Term_Result_Marge_Final.objects.filter(**dataFilter).first()
        context = get_global_data(request)
        context['formHeader'] = formHeader
        context['result_info'] = result_info
        return render(request, template_name, context)

    return JsonResponse(data)


@transaction.atomic
def edu_result_marge_mark_sheet_data(request):
    if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
    data=dict()
    if request.method == 'POST':
        try:
            with transaction.atomic():
                branch_code = request.POST.get('branch_code')
                academic_year = request.POST.get('academic_year')
                session_id = request.POST.get('session_id')
                class_id = request.POST.get('class_id')
                class_group_id = request.POST.get('class_group_id')
                term_1 = request.POST.get('term_1')
                term_2 = request.POST.get('term_2')
                

                dataFilter = dict()
                viewSettingFilter = dict()
                Term_ids = []
                dataFilter['branch_code'] = branch_code
                viewSettingFilter['branch_code'] = branch_code
                dataFilter['academic_year'] = academic_year
                viewSettingFilter['academic_year'] = academic_year
                dataFilter['class_id'] = class_id
                viewSettingFilter['class_id'] = class_id
                dataFilter['one_term_id'] = term_1
                dataFilter['two_term_id'] = term_2
                Term_ids.append(int(term_1))
                Term_ids.append(int(term_2))
                terms=Exam_Term.objects.filter(id__in=Term_ids)
                if session_id:
                    dataFilter['session_id'] = session_id
                    viewSettingFilter['session_id'] = session_id
                if class_group_id:
                    dataFilter['class_group_id'] = class_group_id
                    viewSettingFilter['class_group_id'] = class_group_id

                final_result=Term_Result_Marge_Final.objects.values(
                    'marge_tilte',
                    'student_roll',
                    'total_marks',
                    'obtain_marks',
                    'result_grade',
                    'grade_point',
                    'merit_position',
                    'grade_point_without_furth',
                    'one_term_id',
                    'one_total_marks',
                    'one_obtain_marks',
                    'one_result_grade',
                    'one_grade_point',
                    'two_term_id',
                    'two_total_marks',
                    'two_obtain_marks',
                    'two_result_grade',
                    'two_grade_point',
                    'three_term_id',
                    'three_total_marks',
                    'three_obtain_marks',
                    'three_result_grade',
                    'three_grade_point',
                    student_name=F('student_roll__student_name'),
                    father_name=F('student_roll__student_father_name'),
                    mother_name=F('student_roll__student_mother_name'),
                    class_roll=F('student_roll__class_roll'),
                    date_of_birth=F('student_roll__student_date_of_birth'),
                    class_name=F('class_id__class_name'),
                    class_group=F('class_group_id__class_group_name'),
                    year=F('academic_year'),
                    session=F('session_id__session_name'),
                    one_term_name=F('one_term_id__term_name'),
                    two_term_name=F('two_term_id__term_name'),
                    three_term_name=F('three_term_id__term_name')
                ).filter(**dataFilter).order_by('-grade_point','-obtain_marks','merit_position')
                
                subject_results=Term_Result_Marge.objects.values(
                    'student_roll',
                    'total_marks',
                    'obtain_marks',
                    'result_grade',
                    'grade_point',
                    'is_optional',
                    'out_of',
                    'one_result_view_id',
                    'one_total_marks',
                    'one_obtain_marks',
                    'one_result_grade',
                    'one_grade_point',
                    'two_result_view_id',
                    'two_total_marks',
                    'two_obtain_marks',
                    'two_result_grade',
                    'two_grade_point',
                    'three_result_view_id',
                    'three_total_marks',
                    'three_obtain_marks',
                    'three_result_grade',
                    'three_grade_point',
                    short_number=F('one_result_view_id__short_number'),
                    subject_one_id=F('one_result_view_id__subject_one_id'),
                    subject_two_id=F('one_result_view_id__subject_two_id'),
                    subject_three_id=F('one_result_view_id__subject_three_id'),
                    
                ).filter(**dataFilter).order_by('short_number')
                
                subject_filter=dict()
                subject_filter['class_id']=class_id
                if class_group_id:
                    subject_filter['class_group_id']=class_group_id

                subjects=Subject_List.objects.filter(**subject_filter)
                form_header=Admission_form_header.objects.filter(branch_code=branch_code)
                logo=''
                for header in form_header:
                    if header.logo:
                        logo=header.logo.url
                resultViewSetting=result_view_setting.objects.filter(**viewSettingFilter,term_id=term_1).order_by('short_number')
                data['results']=list(final_result)
                data['subject_results']=list(subject_results)
                data['subjects']=list(subjects.values())
                data['result_view_setting']=list(resultViewSetting.values())
                data['form_header']=list(form_header.values())[0]
                data['logo']=logo
                result_grade=Result_Grade.objects.filter(out_of=data['subject_results'][0]['out_of'])
                data['result_grades']=list(result_grade.values())
                data['terms']=list(terms.values())

        except Exception as e:
                logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                data['error_message'] = str(e)
                return JsonResponse(data)
    return JsonResponse(data)


class edu_certificat_header_address(TemplateView):
    template_name = 'edu/edu-certificat-header-address.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')

        context = get_global_data(request)
        branch_code = request.session["branch_code"]
        is_head_office_user = request.session["is_head_office_user"]

        if is_head_office_user == 'Y':
            forms = Certificat_Header_Address.objects.all()
            form = CertificatHeaderAddressModelForm()
        else:
            forms = Certificat_Header_Address.objects.filter(
                branch_code=branch_code).first()
            if forms:
                form = CertificatHeaderAddressModelForm(instance=forms)
            else:
                form = CertificatHeaderAddressModelForm()

        context['form'] = form
        context['forms'] = forms
        return render(request, self.template_name, context)


def edu_certificat_header_address_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    data = dict()
    data['form_is_valid'] = False

    is_head_office_user = request.session["is_head_office_user"]
    if request.method == 'POST':
        if is_head_office_user == 'Y':
            form = CertificatHeaderAddressModelForm(request.POST)
            branch_code = request.POST.get("branch_code")
            if Certificat_Header_Address.objects.filter(branch_code=branch_code).exists():
                idCardData = Certificat_Header_Address.objects.filter(
                    branch_code=branch_code).first()
                if form.is_valid():
                    post = form.save(commit=False)
                    idCardData.academic_name = post.academic_name
                    idCardData.logo = request.FILES.get('logo')
                    idCardData.sing = request.FILES.get('sing')
                    idCardData.address = post.address
                    idCardData.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Added Successfully!'
                else:
                    data['error_message'] = form.errors.as_json()
                    idCardData.academic_name
            else:
                if form.is_valid():
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.logo = request.FILES.get('logo')
                    post.sing = request.FILES.get('sing')
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Added Successfully!'
                else:
                    data['error_message'] = form.errors.as_json()

        else:
            branch_code = request.session["branch_code"]
            forms = Certificat_Header_Address.objects.filter(
                branch_code=branch_code).first()
            if forms:
                form = CertificatHeaderAddressModelForm(
                    request.POST, instance=forms)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    if(request.FILES.get('logo')):
                        post.logo = request.FILES.get('logo')
                    if(request.FILES.get('sing')):
                        post.sing = request.FILES.get('sing')
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Application Setting Info Added Successfully!'
                else:
                    data['error_message'] = form.errors.as_json()
            else:
                form = CertificatHeaderAddressModelForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.logo = request.FILES.get('logo')
                    post.sing = request.FILES.get('sing')
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Added Successfully!'
                else:
                    data['error_message'] = form.errors.as_json()
    return redirect('/edu-certificat-header-address')

class edu_board_name_createlist(TemplateView):
    template_name = 'edu/edu-board-name-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Education_BoardModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)

def edu_board_name_createlist_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = Education_BoardModelForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Certificate Name Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_board_name_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Education_Board, pk=id)
    template_name = 'edu/edu-board-name-edit.html'
    data = dict()

    if request.method == 'POST':
        form = Education_BoardModelForm(request.POST, instance=instance_data)
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
        form = Education_BoardModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        context['branch_code'] = instance_data.branch_code
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)

class edu_certificate_name_createlist(TemplateView):
    template_name = 'edu/edu_certificate-name-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Certificat_NameModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)

def edu_certificate_name_createlist_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = Certificat_NameModelForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Certificate Name Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def edu_certificate_name_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Certificat_Name, pk=id)
    template_name = 'edu/edu-certificate-name-edit.html'
    data = dict()

    if request.method == 'POST':
        form = Certificat_NameModelForm(request.POST, instance=instance_data)
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
        form = Certificat_NameModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        context['branch_code'] = instance_data.branch_code
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)

def edu_studentinfo_search(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    template_name = 'edu/edu-studentinfo-search.html'
    data = dict()
    form = StudentInfoModelForm()
    data = get_global_data(request)
    form.fields['student_phone'].required = False
    branchs = Branch.objects.all().order_by('branch_code')
    data['form'] = form
    data['branchs'] = branchs
    return render(request, template_name, data)

def edu_student_testimonial_list(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    is_head_office_user = request.session["is_head_office_user"]
    if is_head_office_user == 'Y':
        certificate_names=Certificat_Name.objects.all()
    else:
        branch_code = request.session["branch_code"]
        certificate_names=Certificat_Name.objects.filter(branch_code=branch_code)
    template_name = 'edu/edu-testimonial-list.html'
    data = get_global_data(request)
    data['certificate_names']=certificate_names
    return render(request, template_name, data)
