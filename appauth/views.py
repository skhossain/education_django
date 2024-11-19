from appauth.manage_session import *
from .globalparam import *
from .myException import *
from .validations import *
from .utils import *
from .forms import *
from .models import *
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
from random import randint
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import datetime
from datetime import date, datetime, timedelta
from django.db import connection, transaction
from django.template.loader import render_to_string
from django.db.models import Count, Sum, Avg
import logging
import sys
logger = logging.getLogger(__name__)

all_permissions = {}

global_parameters = {}


def get_global_data(request):

    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    try:
        user_full_name = request.session['user_full_name']
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        application_title = request.session["application_title"]
        is_head_office_user = request.session["is_head_office_user"]

        if is_head_office_user == 'Y':
            is_head_office_user_bool = True
        else:
            is_head_office_user_bool = False

    except Exception as e:
        return render(request, 'appauth/appauth-login.html')
    user_info = User.objects.get(username=request.user)
    all_permissions = user_info.get_all_permissions()
    context = {
        'user': request.user,
        'user_full_name': user_full_name,
        'app_user_id': app_user_id,
        'all_permissions': all_permissions,
        'branch_code': branch_code,
        'branch_name': str(branch_code) + " - "+request.session["branch_name"],
        'global_branch_code': branch_code,
        'is_head_office_user': is_head_office_user_bool,
        'is_head_office_user_bool': is_head_office_user_bool,
        'application_title': application_title,
    }

    for programs in all_permissions:
        context[programs.split('.')[1]] = True

    return context


def get_global_report_data(request):

    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    try:
        user_full_name = request.session['user_full_name']
        app_user_id = request.session["app_user_id"]
        company = Global_Parameters.objects.get()
        application_title = request.session["application_title"]
        company_name = company.company_name
        company_address = company.company_address
    except Exception as e:
        return render(request, 'appauth/appauth-login.html')
    data = {
        'user': request.user,
        'user_full_name': user_full_name,
        'app_user_id': app_user_id,
        'company_name': company_name,
        'company_address': company_address,
        'application_title': application_title,
    }

    return data

class HomeView(TemplateView):
    template_name = 'appauth/appauth-login.html'


def appauth_home(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    context = get_global_data(request)
    context['is_home_page'] = True
    return render(request, "appauth/appauth-home.html", context)


def login_view(request):
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)
    global global_parameters

    delete_all_unexpired_sessions_for_user(username)

    try:

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            user_info = User.objects.get(username=username)

            request.session['user_full_name'] = user_info.first_name + \
                " "+user_info.last_name
            request.session['app_user_id'] = username
            app_setting = Global_Parameters.objects.get()
            user_setting = User_Settings.objects.get(
                app_user_id=username, is_active=True, is_deleted=False)
            reset_user_password = user_setting.reset_user_password
            request.session['application_title'] = app_setting.application_title
            request.session['branch_code'] = user_setting.branch_code
            request.session['branch_name'] = Branch.objects.get(
                branch_code=user_setting.branch_code).branch_name

            if reset_user_password:
                return render(request, "appauth/appauth-reset-password.html", {"message": "Reset Your Password!"})

            if not user_setting.is_active:

                return render(request, "appauth/appauth-login.html", {"message": "You Are Not Permitted Now."})

            if user_setting.head_office_admin:
                is_head_office_user = 'Y'
            else:
                is_head_office_user = 'N'
            request.session["is_head_office_user"] = is_head_office_user

            global_param = Globaldata(request.session['user_full_name'], request.session['application_title'],
                                      request.session["app_user_id"], '.....', user_setting.branch_code, is_head_office_user)
            global_parameters = global_param.get_global_data()

            return HttpResponseRedirect(reverse("appauth-home"))
        else:
            return render(request, "appauth/appauth-login.html", {"message": "Invalid Credentials."})

    except Exception as e:
        return render(request, "appauth/appauth-login.html", {"message": str(e)})


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
        try:
            user = User.objects.get(username=user_name)
            user_info = User_Settings.objects.get(app_user_id=user_name)
            user_info.reset_user_password = False
            user.set_password(new_password)
            user.save()
            user_info.save()
            return render(request, "appauth/appauth-login.html", {"message": "Password Reset Successfully"})
        except Exception as e:
            message = str(e)
        return render(request, "appauth/appauth-reset-password.html", {"message": message})
    else:
        return render(request, "appauth/appauth-reset-password.html", {"message": "Invalid Credentials!"})


def DashboardView(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    context = get_global_data(request)
    data = dict()
    try:
        app_user_id = request.session["app_user_id"]
    except Exception as e:
        data['form_is_valid'] = False
        logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
    return render(request, "appauth/appauth-dashboard.html", context)


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
                    app_user_id = form.cleaned_data["app_user_id"]
                    group_id = form.cleaned_data["group_id"]
                    employee_id = form.cleaned_data["employee_id"].employee_id
                    branch_code = form.cleaned_data["branch_code"]
                    employee_name = fn_get_employee_name(employee_id)
                    user_password = str(randint(1111, 9999))
                    user = User.objects.create_user(
                        app_user_id, '', user_password)
                    user.last_name = employee_name
                    user.save()
                    user_info = User.objects.get(username=app_user_id)
                    post = form.save(commit=False)
                    if group_id:
                        group_id = group_id.id
                        group = Group.objects.get(id=group_id)
                        user_info.groups.add(group)
                    post.django_user_id = user_info.id
                    post.reset_user_password = True
                    post.cash_gl_code = user_setting.cash_gl_code
                    post.employee_name = employee_name
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
        forms = AppUserModelForm()
        context = get_global_data(request)
        context['forms'] = forms
        return render(request, self.template_name, context)


@transaction.atomic
def reset_appuser_password(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    data = dict()
    data['success_message'] = ''
    data['form_is_valid'] = False
    data['error_message'] = ''
    try:
        with transaction.atomic():
            app_user_id = request.POST.get('app_user_id')
            user_info = User_Settings.objects.get(app_user_id=app_user_id)
            user = User.objects.get(username=user_info.app_user_id)
            user_info.reset_user_password = True
            new_password = str(randint(1111, 9999))
            user.set_password(new_password)
            user.save()
            user_info.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Password Reset Successfully\nNew temporary password for this user : '+new_password
    except Exception as e:
        data['form_is_valid'] = False
        data['error_message'] = str(e)
        logger.error("Error on line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        return JsonResponse(data)
    return JsonResponse(data)


def appauth_appuser_update(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    try:
        #django_user_id = request.GET.get('django_user_id')
        instance_data = get_object_or_404(
            User_Settings, django_user_id=id)
        employee_name = instance_data.employee_name
        old_group_id = instance_data.group_id
        template_name = 'appauth/appauth-appuser-update.html'
        context = {}
        data = dict()

        if request.method == 'POST':
            form = AppUserEditForm(request.POST, instance=instance_data)
            data['form_error'] = form.errors.as_json()
            if form.is_valid():

                if form.cleaned_data["group_id"]:
                    group_id = form.cleaned_data["group_id"].id
                else:
                    group_id = None
                app_user_id = form.cleaned_data["app_user_id"]

                if group_id != old_group_id and group_id:
                    group = Group.objects.get(id=group_id)
                    user = User.objects.get(username=app_user_id)
                    user.groups.clear()
                    user.groups.add(group)
                obj = form.save(commit=False)
                obj.employee_name = employee_name
                obj.save()
                delete_all_unexpired_sessions_for_user(
                    instance_data.app_user_id)
                context = get_global_data(request)
                context['success_message'] = ''
                context['error_message'] = ''
                data['form_is_valid'] = True
            else:
                data['form_is_valid'] = False
                data['error_message'] = form.errors.as_json()
                return JsonResponse(data)
        else:
            form = AppUserEditForm(instance=instance_data)
            context = get_global_data(request)
            context['form'] = form
            context['id'] = id
            data['html_form'] = render_to_string(
                template_name, context, request=request)
        return JsonResponse(data)
    except Exception as e:
        data['form_is_valid'] = False
        data['error_message'] = str(e)
        return JsonResponse(data)


class appauth_branch_view(TemplateView):
    template_name = 'appauth/appauth-branch-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = BranchModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def appauth_branch_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = BranchModelForm(request.POST)
                if form.is_valid():
                    branch_code = form.cleaned_data["branch_code"]
                    if fn_val_check_branch_exist(branch_code):
                        data['error_message'] = 'Branch Code Already Exist!'
                        return JsonResponse(data)

                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Branch Opened Successfully!'
                else:
                    data['form_is_valid'] = False
                    data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    except Exception as e:
        data['form_is_valid'] = False
        data['error_message'] = str(e)
        return JsonResponse(data)


@transaction.atomic
def appauth_branch_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    data = dict()
    try:
        with transaction.atomic():
            instance_data = get_object_or_404(Branch, branch_code=id)
            old_branch_code = instance_data.branch_code
            template_name = 'appauth/appauth-branch-edit.html'

            if request.method == 'POST':
                form = BranchModelForm(request.POST, instance=instance_data)
                data['form_error'] = form.errors.as_json()
                if form.is_valid():
                    branch_code = form.cleaned_data["branch_code"]

                    if branch_code != old_branch_code:
                        data['error_message'] = 'Branch Code Modification is Not Allowed!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

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
                form = BranchModelForm(instance=instance_data)
                context = get_global_data(request)
                context['form'] = form
                context['id'] = id
                data['html_form'] = render_to_string(
                    template_name, context, request=request)
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


class appauth_country_view(TemplateView):
    template_name = 'appauth/appauth-country-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Country_Model_Form()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def appauth_country_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = Country_Model_Form(request.POST)
                if form.is_valid():
                    country_id = fn_get_country_id()
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.country_id = country_id
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Country Added Successfully!'
                else:
                    data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


@transaction.atomic
def appauth_country_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    data = dict()
    try:
        with transaction.atomic():
            instance_data = get_object_or_404(Loc_Country, branch_code=id)
            template_name = 'appauth/appauth-country-edit.html'

            if request.method == 'POST':
                form = Country_Model_Form(request.POST, instance=instance_data)
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
                form = Country_Model_Form(instance=instance_data)
                context = get_global_data(request)
                context['form'] = form
                context['id'] = id
                data['html_form'] = render_to_string(
                    template_name, context, request=request)
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


class appauth_employee_view(TemplateView):
    template_name = 'appauth/appauth-employee-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        form = Employees_Model_Form(initial={'joining_date': cbd})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def appauth_employee_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = Employees_Model_Form(request.POST)
                if form.is_valid():
                    branch_code = form.cleaned_data["branch_code"].branch_code
                    employee_name = form.cleaned_data["employee_name"]
                    present_address = form.cleaned_data["present_address"]
                    phone_number = form.cleaned_data["mobile_num"]
                    joining_date = form.cleaned_data["joining_date"]
                    employee_id = fn_get_employee_id()

                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.employee_id = employee_id
                    post.save()

                    data['form_is_valid'] = True
                    data['success_message'] = 'Employee Added Successfully.'
                else:
                    data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    except Exception as e:
        if len(data['error_message']) > 0:
            return JsonResponse(data)
        data['error_message'] = str(e)
        return JsonResponse(data)


@transaction.atomic
def appauth_employee_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    data = dict()
    try:
        with transaction.atomic():
            instance_data = get_object_or_404(Employees, employee_id=id)
            old_employee_id = instance_data.employee_id
            template_name = 'appauth/appauth-employee-edit.html'

            if request.method == 'POST':
                form = Employees_Model_Form(
                    request.POST, instance=instance_data)
                data['form_error'] = form.errors.as_json()
                if form.is_valid():
                    employee_id = form.cleaned_data["employee_id"]

                    if employee_id != old_employee_id:
                        data['error_message'] = 'Employee Code Modification is Not Allowed!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

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
                form = Employees_Model_Form(instance=instance_data)
                context = get_global_data(request)
                context['form'] = form
                context['id'] = id
                data['html_form'] = render_to_string(
                    template_name, context, request=request)
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


class appauth_director_view(TemplateView):
    template_name = 'appauth/appauth-director-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        if not fn_is_user_permition_exist(request.session["app_user_id"], 'A20000010', 'AppAuth'):
            return HttpResponseRedirect(reverse("appauth-home"))

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        form = Directors_Model_Form(initial={'joining_date': cbd})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def appauth_director_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ''

    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = Directors_Model_Form(request.POST)
                if form.is_valid():
                    branch_code = form.cleaned_data["branch_code"]
                    director_name = form.cleaned_data["director_name"]
                    present_address = form.cleaned_data["present_address"]
                    phone_number = form.cleaned_data["mobile_num"]
                    joining_date = form.cleaned_data["joining_date"]
                    director_id = fn_get_director_id()
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.director_id = director_id
                    post.save()

                    data['form_is_valid'] = True
                    data['success_message'] = 'Director Added Successfully.'
                else:
                    data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    except Exception as e:
        if len(data['error_message']) > 0:
            return JsonResponse(data)
        data['error_message'] = str(e)
        return JsonResponse(data)


@transaction.atomic
def appauth_director_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    data = dict()
    try:
        with transaction.atomic():
            instance_data = get_object_or_404(Directors, director_id=id)
            old_director_id = instance_data.director_id
            template_name = 'appauth/appauth-director-edit.html'

            if request.method == 'POST':
                form = Directors_Model_Form(
                    request.POST, instance=instance_data)
                data['form_error'] = form.errors.as_json()
                if form.is_valid():
                    director_id = form.cleaned_data["director_id"]

                    if director_id != old_director_id:
                        data['error_message'] = 'Director ID Modification is Not Allowed!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

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
                form = Directors_Model_Form(instance=instance_data)
                context = get_global_data(request)
                context['form'] = form
                context['id'] = id
                data['html_form'] = render_to_string(
                    template_name, context, request=request)
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


def fn_get_employee_details_view(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    try:
        employee_id = request.GET.get('employee_id')
        data = fn_get_employee_details(employee_id)
        data['form_is_valid'] = True
        return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


def appauth_choice_employeelist(request):
    try:
        branch_code = request.GET.get('branch_code')
    except Exception as e:
        branch_code = request.session["branch_code"]

    list_data = Employees.objects.filter().values(
        'employee_id', 'employee_name').order_by('employee_name')
    if branch_code:
        list_data.filter(branch_code=branch_code)
    return render(request, 'appauth/appauth-choice-employeelist.html', {'list_data': list_data})


def appauth_choice_branchlist(request):
    try:
        branch_code = request.GET.get('branch_code')
    except Exception as e:
        branch_code = request.session["branch_code"]
    list_data = Branch.objects.filter().values(
        'branch_code', 'branch_name').order_by('branch_name')
    return render(request, 'appauth/appauth-choice-branchlist.html', {'list_data': list_data})


def appauth_choice_appuserlist(request):
    try:
        branch_code = request.GET.get('branch_code')
    except Exception as e:
        branch_code = request.session["branch_code"]
    if branch_code:
        list_data = User_Settings.objects.filter(branch_code=branch_code).values(
            'employee_name', 'app_user_id').order_by('employee_name')
    else:
        list_data = User_Settings.objects.filter().values(
            'employee_name', 'app_user_id').order_by('employee_name')
    return render(request, 'appauth/appauth-choice-appuserlist.html', {'list_data': list_data})


def appauth_report_submit(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()

    if request.method == 'GET':
        report_name = request.GET["report_name"]
        app_user_id = request.session["app_user_id"]
        report_config = Report_Configuration.objects.get()
        report_urls = report_config.report_url + \
            'report_name='+report_name+'&user_id='+app_user_id
        data['form_is_valid'] = True
        data['report_urls'] = report_urls
        return JsonResponse(data)

    report_data = request.POST.getlist('report_data')
    data_dict = json.loads(report_data[0])
    report_name = request.POST["report_name"]
    app_user_id = request.session["app_user_id"]
    branch_code = request.session["branch_code"]
    try:
        parameter_list = []
        for param in data_dict:
            parameter_name = param
            parameter_name_value = data_dict[parameter_name]
            row = Report_Parameter(app_user_id=app_user_id, report_name=report_name,
                                   parameter_name=parameter_name, parameter_values=parameter_name_value)
            parameter_list.append(row)

        Report_Parameter.objects.filter(app_user_id=app_user_id).delete()
        Report_Parameter.objects.bulk_create(parameter_list)

        cursor = connection.cursor()
        cursor.callproc("fn_run_report", [app_user_id, report_name])
        row = cursor.fetchone()

        if row[0] != 'S':
            logger.error("Error in fn_run_report on line {} \nType: {} \nError:{}".format(
                sys.exc_info()[-1], type(row[1]).__name__, str(row[1])))
            raise Exception(row[1])

        report_config = Report_Configuration.objects.get()
        report_urls = report_config.report_url
        data['form_is_valid'] = True
        data['report_urls'] = report_urls
        return JsonResponse(data)
    except Exception as e:
        data['form_is_valid'] = False
        logger.error("Error in appauth_report_submit on line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        data['error_message'] = 'Report Error : '+str(e)
        return JsonResponse(data)

###### For New Page ##########


class appauth_country_view(TemplateView):
    template_name = 'appauth/appauth-country-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Country_Model_Form()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def appauth_country_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = Country_Model_Form(request.POST)
        if form.is_valid():
            country_name = form.cleaned_data["country_name"]
            country_id = fn_get_country_id()
            if Loc_Country.objects.filter(country_name=country_name).exists():
                data['error_message'] = 'This country name already exits'
                data['form_is_valid'] = False
                return JsonResponse(data)
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.country_id = country_id
            post.country_name = country_name
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Country Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def appauth_country_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Loc_Country, country_id=id)
    template_name = 'appauth/appauth-country-edit.html'
    data = dict()

    if request.method == 'POST':
        form = Country_Model_Form(request.POST, instance=instance_data)
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
        form = Country_Model_Form(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)

###### For create division New Page ##########


class appauth_division_view(TemplateView):
    template_name = 'appauth/appauth-division-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Division_Model_Form()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def appauth_division_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = Division_Model_Form(request.POST)
        if form.is_valid():
            division_name = form.cleaned_data["division_name"]
            division_id = fn_get_division_id()
            if Loc_Division.objects.filter(division_name=division_name).exists():
                data['error_message'] = 'This division name already exits'
                data['form_is_valid'] = False
                return JsonResponse(data)
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.division_id = division_id
            post.division_name = division_name
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Division Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def appauth_division_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Loc_Division, division_id=id)
    template_name = 'appauth/appauth-division-edit.html'
    data = dict()

    if request.method == 'POST':
        form = Division_Model_Form(request.POST, instance=instance_data)
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
        form = Division_Model_Form(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)

###### For create district New Page ##########


class appauth_disrict_view(TemplateView):
    template_name = 'appauth/appauth-district-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = District_Model_Form()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def appauth_district_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = District_Model_Form(request.POST)
        if form.is_valid():
            district_name = form.cleaned_data["district_name"]
            district_id = fn_get_district_id()
            if Loc_District.objects.filter(district_name=district_name).exists():
                data['error_message'] = 'This district name already exits'
                data['form_is_valid'] = False
                return JsonResponse(data)
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.district_id = district_id
            post.district_name = district_name
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'District Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def appauth_district_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Loc_District, district_id=id)
    template_name = 'appauth/appauth-district-edit.html'
    data = dict()

    if request.method == 'POST':
        form = District_Model_Form(request.POST, instance=instance_data)
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
        form = District_Model_Form(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


###### For create Upazila New Page ##########

class appauth_upazila_view(TemplateView):
    template_name = 'appauth/appauth-upazila-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Upazila_Model_Form()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def appauth_upazila_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = Upazila_Model_Form(request.POST)
        if form.is_valid():
            upozila_name = form.cleaned_data["upozila_name"]
            upozila_id = fn_get_upazila_id()
            if Loc_Upazila.objects.filter(upozila_name=upozila_name).exists():
                data['error_message'] = 'This upazila name already exits'
                data['form_is_valid'] = False
                return JsonResponse(data)
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.upozila_id = upozila_id
            post.upozila_name = upozila_name
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Upazila Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def appauth_upazila_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Loc_Upazila, upozila_id=id)
    template_name = 'appauth/appauth-upazila-edit.html'
    data = dict()

    if request.method == 'POST':
        form = Upazila_Model_Form(request.POST, instance=instance_data)
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
        form = Upazila_Model_Form(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)

###### For create Union New Page ##########


class appauth_union_view(TemplateView):
    template_name = 'appauth/appauth-union-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Union_Model_Form()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def appauth_union_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = Union_Model_Form(request.POST)
        if form.is_valid():
            union_name = form.cleaned_data["union_name"]
            union_id = fn_get_union_id()
            if Loc_Union.objects.filter(union_name=union_name).exists():
                data['error_message'] = 'This union name already exits'
                data['form_is_valid'] = False
                return JsonResponse(data)
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.union_id = union_id
            post.union_name = union_name
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Union Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def appauth_union_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Loc_Union, union_id=id)
    template_name = 'appauth/appauth-union-edit.html'
    data = dict()

    if request.method == 'POST':
        form = Union_Model_Form(request.POST, instance=instance_data)
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
        form = Union_Model_Form(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


def appauth_dashboard_data(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    try:
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        data['general_info'] = fn_get_general_information(
            branch_code, app_user_id)
        data['emp_info'] = fn_get_employee_information(
            branch_code, app_user_id)
        return JsonResponse(data)

    except Exception as e:
        print(str(e))

    return JsonResponse(data)


def appauth_choice_reportlist(request):
    report_screen = request.GET.get('report_screen')
    list_data = Report_List.objects.filter(report_screen=report_screen).values(
        'id','report_name', 'report_url','report_list_name').order_by('report_list_name')
    return render(request, 'appauth/appauth-choice-reportlist.html', {'list_data': list_data})

def appauth_get_report_url(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    try:
        report_id = request.GET.get('report_id')
        report_screen = request.GET.get('report_screen')
        rep = Report_List.objects.get(id=report_id, report_screen=report_screen)
        data['report_url'] = rep.report_url
        data['report_name'] = rep.report_name
        data['form_is_valid'] = True
        return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)

