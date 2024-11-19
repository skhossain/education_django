import json
from threading import Thread
import time
from edu.models import Degree_Info, Teacher
from logging import exception
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from decimal import Context
from django.shortcuts import render
from django.views.generic.base import TemplateView
from appauth.views import get_global_data
from django.contrib.auth.models import User

from .forms import *
from .utils import *
from django.http import JsonResponse, request
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.db import transaction
from .validations import *
from django.core.files.base import ContentFile
import base64
import os
from appauth.utils import get_business_date
# Create your views here.

# ----------------------------hrm-view-start------------------------------
# X-X-X-X-X-X-X-X-X-X-X-X------hrm-view-end-------X-X-X-X-X-X-X-X-X-X-X-X

# company info start


@method_decorator(login_required, name='dispatch')
class hrm_company_info_view(TemplateView):
    template_name = "hrm/hrm-company-create.html"

    def get(self, request):
        form = CompanyInformationForm()
        context = get_global_data(request)
        context['form'] = form
        context['title'] = 'Company Information'
        return render(request, self.template_name, context)


@transaction.atomic
def hrm_company_info_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    app_user_id = request.session['app_user_id']
    if request.method == 'POST':
        form = CompanyInformationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post = form.save(commit=False)
                    company_id = fn_get_company_id()
                    data['company_id'] = company_id
                    post.app_user_id = app_user_id
                    post.company_id = company_id
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = "company creata successfully"
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)

        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


@transaction.atomic
def hrm_company_info_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Company_Information, company_id=id)
    template_name = 'hrm/hrm-company-edit.html'
    data = dict()
    if request.method == "POST":
        form = CompanyInformationForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj = form.save(commit=False)
                    obj.save()
                    data['success_message'] = "updated successfully!"
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
        form = CompanyInformationForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        context['title'] = 'Company information'
        data['html_form'] = render_to_string(
            template_name, context, request=request
        )

    return JsonResponse(data)
# company info end


# office info start

@method_decorator(login_required, name='dispatch')
class hrm_office_info(TemplateView):
    template_name = 'hrm/hrm-offcie-create.html'

    def get(self, request):
        form = CompanyOfficeForm()
        context = get_global_data(request)
        context['form'] = form
        context['title'] = "Office Information"
        return render(request, self.template_name, context)


@login_required
@transaction.atomic
def hrm_office_info_insert(request):
    data = dict()
    data['form_is_valid'] = False
    app_user_id = request.session['app_user_id']
    if request.method == "POST":
        form = CompanyOfficeForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post = form.save(commit=False)
                    office_id = fn_get_office_id()
                    post.app_user_id = app_user_id
                    post.office_id = office_id
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = "office create successfully"
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)

        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


@login_required
@transaction.atomic
def hrm_office_info_edit(request, id):
    instance_data = get_object_or_404(Company_Office, office_id=id)
    template_name = 'hrm/hrm-office-edit.html'
    data = dict()
    if request.method == "POST":
        form = CompanyOfficeForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    form_obj = form.save(commit=False)
                    form_obj.save()
                    data['success_message'] = "update Successfully"
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
        form = CompanyOfficeForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        context['title'] = "Office Information"
        data['html_form'] = render_to_string(
            template_name, context, request=request
        )
    return JsonResponse(data)
# office info end


# departmnet info start
class Department_info_view(LoginRequiredMixin, TemplateView):
    template_name = "hrm/hrm-department_info.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = DepartmentInfoForm()
        context = get_global_data(request)
        context['form'] = form
        context['title'] = "Departments"
        return render(request, self.template_name, context)


@transaction.atomic
def department_info_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    app_user_id = request.session['app_user_id']
    if request.method == 'POST':
        form = DepartmentInfoForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post = form.save(commit=False)
                    department_id = fn_get_departmnet_id()
                    post.app_user_id = app_user_id
                    post.department_id = department_id
                    post.save()
                    data['form_is_valid'] = True
                    data['department_id'] = department_id
                    data['success_message'] = "Department added successfully"
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def department_info_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Department_Info, department_id=id)
    template_name = 'hrm/hrm-department-edit.html'
    data = dict()
    if request.method == 'POST':
        form = DepartmentInfoForm(request.POST, instance=instance_data)
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
        form = DepartmentInfoForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        context['title'] = "Departments"

        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)
# departmnet info end

# hrm-office-Shift start


class hrm_office_shift_view(LoginRequiredMixin, TemplateView):
    template_name = "hrm/hrm-shift-info.html"

    def get(self, request):
        form = ShiftInfoForm()
        context = get_global_data(request)
        context['form'] = form
        context['title'] = "Office Shift"

        return render(request, self.template_name, context)


@transaction.atomic
def hrm_office_shift_info_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    app_user_id = request.session['app_user_id']
    if request.method == 'POST':
        form = ShiftInfoForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post = form.save(commit=False)
                    shift_id = fn_get_shift_id()
                    post.app_user_id = app_user_id
                    post.shift_id = shift_id
                    post.save()
                    data['form_is_valid'] = True
                    data['shift_id'] = shift_id
                    data['success_message'] = "shift added successfully"
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


@transaction.atomic
def hrm_office_shift_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Shift_Info, shift_id=id)
    template_name = 'hrm/hrm-shift-edit.html'
    data = dict()
    if request.method == 'POST':
        form = ShiftInfoForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    form_obj = form.save(commit=False)
                    form_obj.save()
                    data['success_message'] = "update successfully"
                    data["error_message"] = ''
                    data['form_is_valid'] = True
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)

    else:
        form = ShiftInfoForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        context['title'] = "Office Shift"
        data["html_form"] = render_to_string(
            template_name, context, request=request
        )
    return JsonResponse(data)

# hrm-office-Shift end


# select 2 javascript remote serching
# plsql

# ----------------------------hrm-Degree-start------------------------------
class hrm_employee_education_degree_view(LoginRequiredMixin, TemplateView):
    template_name = 'hrm/hrm-degree-info-view.html'

    def get(self, request):
        form = EducationDegreeForm()
        context = get_global_data(request)
        context['form'] = form
        context['title'] = "Education Degree"

        return render(request, self.template_name, context)


@transaction.atomic
def hrm_employee_education_degree_info_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    data = dict()
    data['form_is_valid'] = False
    app_user_id = request.session['app_user_id']
    if request.method == 'POST':
        form = EducationDegreeForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form_obj = form.save(commit=False)
                    degree_id = fn_get_degree_id()
                    form_obj.app_user_id = app_user_id
                    form_obj.degree_id = degree_id
                    form_obj.save()
                    data['form_is_valid'] = True
                    data['degree_id'] = degree_id
                    data['success_message'] = "degree create successfully"
                    return JsonResponse(data)
            except Exception as e:
                print(str(e))
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


@transaction.atomic
def hrm_employee_education_degree_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Education_Degree, degree_id=id)
    template_name = 'hrm/hrm-degree-edit.html'
    data = dict()
    if request.method == "POST":
        form = EducationDegreeForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    form_obj = form.save(commit=False)
                    form_obj.save()
                    data['success_message'] = "update successfully"
                    data['form_is_valid'] = True
                    return JsonResponse(data)
            except Exception as e:
                print(str(e))
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)
    else:
        form = EducationDegreeForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        context['title'] = "Education Degree"

        data["html_form"] = render_to_string(
            template_name, context, request=request
        )
    return JsonResponse(data)
# X-X-X-X-X-X-X-X-X-X-X-X-------hrm-Degree-end-------X-X-X-X-X-X-X-X-X-X-X-X


# -----------------Hrm - Designation start---------------------
class hrm_designation_create_view(TemplateView):
    template_name = "hrm/hrm-designation-create.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = EmployeeDesignationForm()
        context = get_global_data(request)
        context['form'] = form
        context['title'] = "Designation"

        return render(request, self.template_name, context)


@transaction.atomic
def hrm_designation_info_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    app_user_id = request.session['app_user_id']
    if request.method == 'POST':
        form = EmployeeDesignationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post = form.save(commit=False)
                    designation_id = fn_get_designation_id()
                    post.app_user_id = app_user_id
                    post.desig_id = designation_id
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = "Designation create successfully"
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)

        else:
            data['error_message'] = form.errors.as_json()

    return JsonResponse(data)


@transaction.atomic
def hrm_designation_info_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Employee_Designation, desig_id=id)
    template_name = 'hrm/hrm-desigtion-edit.html'
    data = dict()
    if request.method == 'POST':
        form = EmployeeDesignationForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj = form.save(commit=False)
                    obj.save()
                    data['success_message'] = 'Updated Successfully!'
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
        form = EmployeeDesignationForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        context['title'] = "Designation"

        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)

# -----------------Hrm - Designation end-------------------------


# ----------------------------hrm-employee type-view-start------------------------------
class hrm_employee_type_info_view(LoginRequiredMixin, TemplateView):
    template_name = "hrm/hrm-employee-type-create.html"

    def get(self, request):
        form = EmplyeeTypeForm()
        context = get_global_data(request)
        context['form'] = form
        context['title'] = "Employee Type"

        return render(request, self.template_name, context)


@transaction.atomic
def hrm_employee_type_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    app_user_id = request.session['app_user_id']
    if request.method == 'POST':
        form = EmplyeeTypeForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    emptype_id = fn_get_employee_type_id()
                    post = form.save(commit=False)
                    data['emptype_id'] = emptype_id
                    post.app_user_id = app_user_id
                    post.emptype_id = emptype_id
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = "employee Type create successfuly"
                    return JsonResponse(data)
            except Exception as e:
                print(str(e))
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)

        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


@transaction.atomic
def hrm_employee_type(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Employment_Type, emptype_id=id)
    template_name = 'hrm/hrm-employee-type-edit.html'
    data = dict()
    if request.method == 'POST':
        form = EmplyeeTypeForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    form_obj = form.save(commit=False)
                    form_obj.save()
                    data['success_message'] = "update successfully"
                    data['error_message'] = ''
                    data['form_is_valid'] = True

                    return JsonResponse(data)
            except Exception as e:
                print(str(e))
                return JsonResponse(data)

        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = EmplyeeTypeForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        context['title'] = "Employee Type"

        data['html_form'] = render_to_string(
            template_name, context, request=request
        )
    return JsonResponse(data)


# X-X-X-X-X-X-X-X-X-X-X-X------hrm-employee type - view-end-------X-X-X-X-X-X-X-X-X-X-X-X


# ----------------------------hrm-salary scale type-view-start------------------------------
class hrm_employee_salary_scale_info_view(LoginRequiredMixin, TemplateView):
    template_name = "hrm/hrm-salary-scale-type-create.html"

    def get(self, request):
        form = SalaryScaleForm()
        context = get_global_data(request)
        context['form'] = form
        context['title'] = "Salary Scale Type"

        return render(request, self.template_name, context)


@transaction.atomic
def hrm_employee_salary_scale_info_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    app_user_id = request.session['app_user_id']
    if request.method == 'POST':
        form = SalaryScaleForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post = form.save(commit=False)
                    salscale_id = fn_get_salscale_id()
                    data['id'] = salscale_id
                    post.app_user_id = app_user_id
                    post.salscale_id = salscale_id
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = "salary scale type create successfuly"
                    return JsonResponse(data)
            except Exception as e:
                print(str(e))
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)

        else:
            data['error_message'] = form.error.as_json()
    return JsonResponse(data)


@transaction.atomic
def hrm_employee_salary_scale_info_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Salary_Scale, salscale_id=id)
    template_name = 'hrm/hrm-salary-scale-edit.html'
    data = dict()
    if request.method == 'POST':
        form = SalaryScaleForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    form_obj = form.save(commit=False)
                    form_obj.save()
                    data['success_message'] = "update successfully"
                    data['error_message'] = ''
                    data['form_is_valid'] = True

                    return JsonResponse(data)
            except Exception as e:
                print(str(e))
                return JsonResponse(data)

        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = SalaryScaleForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        context['title'] = "Salary Scale Type"

        data['html_form'] = render_to_string(
            template_name, context, request=request
        )
    return JsonResponse(data)


# X-X-X-X-X-X-X-X-X-X-X-X------hrm-salary scale type - view-end-------X-X-X-X-X-X-X-X-X-X-X-X


# ----------------------------hrm-Extra Alownce-start------------------------------
class hrm_extra_allownce_create_view(LoginRequiredMixin, TemplateView):
    template_name = 'hrm/hrm-extra-allownce.html'

    def get(self, request):
        form = ExtraAllowanceDetailsForm()
        context = get_global_data(request)
        context['form'] = form
        context['title'] = "Extra Allowance "

        return render(request, self.template_name, context)


@transaction.atomic
def hrm_extra_allownce_create_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    app_user_id = request.session['app_user_id']
    if request.method == 'POST':
        form = ExtraAllowanceDetailsForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    allowance_id = fn_get_alownce_id()
                    post = form.save(commit=False)
                    data['id'] = allowance_id
                    post.allowance_id = allowance_id
                    post.app_user_id = app_user_id
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = "extra allownce create successfully"
                    data['error_message'] = ''
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)

        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


@transaction.atomic
def hrm_extra_allownce_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Extra_Allowance, allowance_id=id)
    print(instance_data)
    template_name = 'hrm/hrm-extra-allownce-edit.html'
    data = dict()
    if request.method == "POST":
        form = ExtraAllowanceDetailsForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj = form.save(commit=False)
                    obj.save()
                    data['success_message'] = "updated successfully!"
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
        form = ExtraAllowanceDetailsForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        context['title'] = "Extra Allowance "

        data['html_form'] = render_to_string(
            template_name, context, request=request
        )

    return JsonResponse(data)
# X-X-X-X-X-X-X-X-X-X-X-X------hrm-Extra Alownce-end-------X-X-X-X-X-X-X-X-X-X-X-X


# ----------------------------hrm-bank Info-start------------------------------
class hrm_bank_info_create_view(LoginRequiredMixin, TemplateView):
    template_name = 'hrm/hrm-bank-info.html'

    def get(self, request):
        form = BankInfoDetailsForm()
        context = get_global_data(request)
        context['form'] = form
        context['title'] = "Bank Information"

        return render(request, self.template_name, context)


@transaction.atomic
def hrm_bank_info_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    app_user_id = request.session['app_user_id']
    if request.method == 'POST':
        form = BankInfoDetailsForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    bank_id = fn_get_bank_id()
                    post = form.save(commit=False)
                    data['id'] = bank_id
                    post.bank_id = bank_id
                    post.app_user_id = app_user_id
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = "Bank info create successfully"
                    data['error_message'] = ''
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)

        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


@transaction.atomic
def hrm_bank_info_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Bank_Info, bank_id=id)
    print(instance_data)
    template_name = 'hrm/hrm-bank-info-edit.html'
    data = dict()
    if request.method == "POST":
        form = BankInfoDetailsForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj = form.save(commit=False)
                    obj.save()
                    data['success_message'] = "updated successfully!"
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
        form = BankInfoDetailsForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        context['title'] = "Bank "

        data['html_form'] = render_to_string(
            template_name, context, request=request
        )

    return JsonResponse(data)


# X-X-X-X-X-X-X-X-X-X-X-X------hrm-Bnak info-end-------X-X-X-X-X-X-X-X-X-X-X-X


# ----------------------------hrm-employee Info-start------------------------------
class hrm_employee_info_create_view(LoginRequiredMixin, TemplateView):
    template_name = 'hrm/hrm-employee-info.html'

    def get(self, request):
        form = EmployeeDetailsForm()
        second_form = EmployeeEducationForm()
        third_form = EmployeeNomineeForm()
        context = get_global_data(request)
        image_data = Image_temp_emp.objects.filter(
            app_user_id=app_user_id).first()
        context['form'] = form
        context['second_form'] = second_form
        context['third_form'] = third_form
        context['image_data'] = image_data
        context['title'] = "Employee Registration "
        return render(request, self.template_name, context)


@transaction.atomic
def hrm_employee_info_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    app_user_id = request.session['app_user_id']
    if request.method == 'POST':
        is_teacher = request.POST.get('is_teacher',None)
        form = EmployeeDetailsForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    id = fn_get_employee_id()
                    post = form.save(commit=False)
                    data['id'] = id
                    post.employee_id = id
                    post.app_user_id = id
                    post.app_data_time = timezone.now()
                    post.save()
                    serial_no = fn_serial_no_id()
                    employee_id_fg = Employee_Details.objects.get(pk=id)
                    img_temp = Image_temp_emp.objects.filter(
                        app_user_id=request.session["app_user_id"]).first()
                    if img_temp:
                        if img_temp.image_1:
                            picture_copy = ContentFile(img_temp.image_1.read())
                            new_picture_name = img_temp.image_1.name.split(
                                "/")[-1]
                            employee_id_fg.profile_image.save(
                                new_picture_name, picture_copy, save=True)

                        if img_temp.image_2:
                            sign_copy = ContentFile(img_temp.image_2.read())
                            sign_name = img_temp.image_2.name.split("/")[-1]
                            employee_id_fg.employee_signature.save(
                                sign_name, sign_copy, save=True)

                    edu_count = int(request.POST.get('eduId'))
                    if edu_count:
                        for i in range(1, edu_count+1):
                            if request.POST.get('degree_name'+str(i)):
                                second_form = EmployeeEducationForm(
                                    request.POST)
                                post_second_form = second_form.save(
                                    commit=False)
                                post_second_form.employee_id = employee_id_fg
                                post_second_form.degree_name = request.POST.get(
                                    'degree_name'+str(i))
                                post_second_form.board_name = request.POST.get(
                                    'board_name'+str(i))
                                post_second_form.result_point = request.POST.get(
                                    'result_point'+str(i))
                                post_second_form.result_grate = request.POST.get(
                                    'result_grate'+str(i))
                                post_second_form.passing_year = request.POST.get(
                                    'passing_year'+str(i))
                                post_second_form.institute_name = request.POST.get(
                                    'institute_name'+str(i))
                                post_second_form.serial_no = serial_no
                                post_second_form.app_data_time = timezone.now()
                                post_second_form.save()
                    employee_experience = request.POST.getlist('experienceList')[
                        0]
                    data_dict = json.loads(employee_experience)
                    if data_dict:
                        for i in data_dict:
                            if i['company_name']:
                                third_form = EmployeeExperinceInfoForm()
                                # if third_form.is_valid():
                                post_third_form = third_form.save(commit=False)
                                post_third_form.employee_id = employee_id_fg
                                post_third_form.serial_no = serial_no
                                post_third_form.company_name = i['company_name']
                                post_third_form.company_address = i['company_address']
                                post_third_form.company_type = i['company_type']
                                post_third_form.position = i['position']
                                post_third_form.department = i['department']
                                post_third_form.responsibility = i['responsibility']
                                post_third_form.achievement = i['achievement']
                                post_third_form.phone_number = i['phone_number']
                                post_third_form.contact_person = i['contact_person']
                                post_third_form.start_date = i['start_date']
                                post_third_form.end_date = i['end_date']
                                post_third_form.app_user_id = app_user_id
                                post_third_form.app_data_time = timezone.now()
                                post_third_form.save()
                    fourth_form = EmployeeNomineeForm()
                    post_fourth_form = fourth_form.save(commit=False)
                    post_fourth_form.employee_id = employee_id_fg
                    post_fourth_form.nominee_serial = serial_no
                    post_fourth_form.nominee_name = request.POST['nominee_name']
                    post_fourth_form.nominee_sex = request.POST['nominee_sex']
                    post_fourth_form.nominee_father_name = request.POST['nominee_father_name']
                    post_fourth_form.nominee_mother_name = request.POST['nominee_mother_name']
                    post_fourth_form.nominee_present_addr = request.POST['nominee_present_addr']
                    post_fourth_form.nominee_permanent_addr = request.POST['nominee_permanent_addr']
                    post_fourth_form.app_user_id = app_user_id
                    
                    nomineeBirth = request.POST.get('nominee_birth_date',None)
                    
                    if(len(nomineeBirth) > 0):        
                        post_fourth_form.nominee_birth_date = nomineeBirth

                    post_fourth_form.nominee_nid_num = request.POST['nominee_nid_num']
                    post_fourth_form.app_data_time = timezone.now()
                    post_fourth_form.save()
                    if(is_teacher is not None):
                        Teacher.objects.create(teacher_id=fn_get_teacher_id(), employee_id=employee_id_fg, app_user_id=app_user_id)
                    else:
                        print("is teacher none")
                    data['form_is_valid'] = True
                    data['success_message'] = "Employee create successfully"
                    data['error_message'] = ''
                    return JsonResponse(data)
            except Exception as e:
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)
            finally:
                thread = Thread(target=temp_image_delete, args=[
                    request.session["app_user_id"]])
                thread.start()
        else:
            data['error_message']=form.errors.as_json()
            return JsonResponse(data)


def temp_image_delete(app_user_id):
    time.sleep(3)
    img_temp = Image_temp_emp.objects.filter(app_user_id=app_user_id).first()
    if img_temp:
        if img_temp.image_1 and os.path.exists(img_temp.image_1.path):
            os.remove(img_temp.image_1.path)
        if img_temp.image_2 and os.path.exists(img_temp.image_2.path):
            os.remove(img_temp.image_2.path)
        img_temp.delete()
    return


def hrm_studentinfo_profile_image_temp(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    image_data = request.POST.get('image')
    format, imgstr = image_data.split(';base64,')
    ext = "webp"

    data = ContentFile(base64.b64decode(imgstr))
    app_user_id = request.session["app_user_id"]
    # file_name = get_random_string(8, allowed_chars='0123456789')+"."+ext #get the filename of desired excel file
    instance_data = Image_temp_emp.objects.filter(
        app_user_id=app_user_id).first()
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
        image_table = Image_temp_emp()
        # get the filename of desired excel file
        file_name = app_user_id+"_profile."+ext
        image_table.app_user_id = app_user_id
        image_table.save()
        image_table.image_1.save(file_name, data, save=True)
    data = dict()
    data['success'] = "Image upload successfull."
    return JsonResponse(data)


def hrm_employee_signature_image_temp(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    image_data = request.POST.get('signature')
    format, imgstr = image_data.split(';base64,')
    ext = "webp"

    data = ContentFile(base64.b64decode(imgstr))
    app_user_id = request.session["app_user_id"]
    # file_name = get_random_string(8, allowed_chars='0123456789')+"."+ext #get the filename of desired excel file
    instance_data = Image_temp_emp.objects.filter(
        app_user_id=app_user_id).first()
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
        image_table = Image_temp_emp()
        # get the filename of desired excel file
        file_name = app_user_id+"_signature."+ext
        image_table.app_user_id = app_user_id
        image_table.save()
        image_table.image_2.save(file_name, data, save=True)
    data = dict()
    data['success'] = "Image upload successfull."
    return JsonResponse(data)


def hrm_employee_info_image_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    try:
        if request.method == "POST":
            img_temp = Image_temp_emp.objects.filter(
                app_user_id=request.session["app_user_id"]).first()
            employee_id_fg = Employee_Details.objects.get(pk=id)
            data = dict()
            if img_temp:
                if img_temp.image_1:
                    picture_copy = ContentFile(img_temp.image_1.read())
                    new_picture_name = img_temp.image_1.name.split("/")[-1]
                    employee_id_fg.profile_image.save(
                        new_picture_name, picture_copy, save=True)

                if img_temp.image_2:
                    sign_copy = ContentFile(img_temp.image_2.read())
                    sign_name = img_temp.image_2.name.split("/")[-1]
                    employee_id_fg.employee_signature.save(
                        sign_name, sign_copy, save=True)
                    data['form_is_valid'] = True
                    data['success_message'] = "upload successfully"
                    return JsonResponse(data)
            else:
                data['form_is_valid'] = True
                data['success_message'] = "upload successfully"
                return JsonResponse(data)
    except Exception as e:
        data['form_is_valid'] = False
        data['success_message'] = "upload Fail"
        return JsonResponse(data)
    finally:
        thread = Thread(target=temp_image_delete, args=[
                        request.session["app_user_id"]])
        thread.start()
        print("work done")
        # return JsonResponse(data)


# ----------------------------hrm-employee experiance Info-start------------------------------
# class hrm_employee_experiance_info_create_view(LoginRequiredMixin, TemplateView):
#     template_name = 'hrm/hrm-employee-experiance-info.html'

#     def get(self, request):
#         form = EmployeeExperinceInfoForm()
#         context = get_global_data(request)
#         context['form'] = form
#         context['title'] = "Employee Experiance "

#         return render(request, self.template_name, context)


# @transaction.atomic
# def hrm_employee_experiance_info_insert(request):
#     if not request.user.is_authenticated:
#         return render(request, 'appauth/appauth-login.html')
#     data = dict()
#     data['form_is_valid'] = False
#     app_user_id = request.session['app_user_id']
#     if request.method == 'POST':
#         form = EmployeeExperinceInfoForm(request.POST)
#         if form.is_valid():
#             try:
#                 with transaction.atomic():
#                     post = form.save(commit=False)
#                     post.app_user_id = app_user_id
#                     post.save()
#                     data['form_is_valid'] = True
#                     data['success_message'] = "Experiance create successfully"
#                     data['error_message'] = ''
#                     return JsonResponse(data)

#             except Exception as e:
#                 print(str(e))
#                 data['form_is_valid'] = False
#                 data['error_message'] = str(e)
#                 return JsonResponse(data)

#         else:
#             data['error_message'] = form.errors.as_json()
#     return JsonResponse(data)


# @transaction.atomic
# def hrm_employee_experiance_info_edit(request, id):
#     if not request.user.is_authenticated:
#         return render(request, 'appauth/appauth-login.html')
#     instance_data = get_object_or_404(Employee_Experience, id=id)
#     print(instance_data)
#     template_name = 'hrm/hrm-employee-experiance-info-edit.html'
#     data = dict()
#     if request.method == "POST":
#         form = EmployeeExperinceInfoForm(request.POST, instance=instance_data)
#         data['form_error'] = form.errors.as_json()
#         if form.is_valid():
#             try:
#                 with transaction.atomic():
#                     obj = form.save(commit=False)
#                     obj.save()
#                     data['success_message'] = "updated successfully!"
#                     data['error_message'] = ''
#                     data['form_is_valid'] = True
#                     return JsonResponse(data)
#             except Exception as e:
#                 print(str(e))
#                 data['form_is_valid'] = False
#                 data['error_message'] = str(e)
#                 return JsonResponse(data)
#         else:
#             data['form_is_valid'] = False
#             data['error_message'] = form.errors.as_json()
#             return JsonResponse(data)

#     else:
#         is_techer = True
#         form = EmployeeExperinceInfoForm(instance=instance_data)
#         context = get_global_data(request)
#         context['form'] = form
#         context['id'] = id
#         context['title'] = "Employee Experiance "

#         data['html_form'] = render_to_string(
#             template_name, context, request=request
#         )

#     return JsonResponse(data)


# X-X-X-X-X-X-X-X-X-X-X-X------hrm-employee-experiance info-end-------X-X-X-X-X-X-X-X-X-X-X-X

# ----------------------------hrm-employee Nomene Info-start------------------------------
# class hrm_employee_nominee_info_create_view(LoginRequiredMixin, TemplateView):
#     template_name = 'hrm/hrm-employee-nominee-info.html'

#     def get(self, request):
#         form = EmployeeNomineeForm()
#         context = get_global_data(request)
#         context['form'] = form
#         context['title'] = "Employee Nominee "
#         return render(request, self.template_name, context)


# @transaction.atomic
# def hrm_employee_nominee_info_edit(request, id=0):
#     print(id)
#     if not request.user.is_authenticated:
#         return render(request, 'appauth/appauth-login.html')
#     instance_data = get_object_or_404(Employee_Nominee, id=id)
#     print(instance_data)
#     template_name = 'hrm/hrm-employee-nominee-info-edit.html'
#     data = dict()
#     if request.method == "POST":
#         form = EmployeeNomineeForm(request.POST, instance=instance_data)
#         data['form_error'] = form.errors.as_json()
#         if form.is_valid():
#             try:
#                 with transaction.atomic():
#                     obj = form.save(commit=False)
#                     obj.save()
#                     data['success_message'] = "updated successfully!"
#                     data['error_message'] = ''
#                     data['form_is_valid'] = True
#                     return JsonResponse(data)
#             except Exception as e:
#                 print(str(e))
#                 data['form_is_valid'] = False
#                 data['error_message'] = str(e)
#                 return JsonResponse(data)
#         else:
#             data['form_is_valid'] = False
#             data['error_message'] = form.errors.as_json()
#             return JsonResponse(data)

#     else:
#         form = EmployeeNomineeForm(instance=instance_data)
#         context = get_global_data(request)
#         context['form'] = form
#         context['title'] = "Employee Nominee"
#         data['html_form'] = render_to_string(
#             template_name, context, request=request
#         )

#         return JsonResponse(data)
# X-X-X-X-X-X-X-X-X-X-X-X------hrm-employee-nomene info-end-------X-X-X-X-X-X-X-X-X-X-X-X


# ----------------------------hrm-document type-start------------------------------
class hrm_document_type_create_view(LoginRequiredMixin, TemplateView):
    template_name = 'hrm/hrm-document-type-info.html'

    def get(self, request):
        form = EmployeeDocumentTypeForm()
        context = get_global_data(request)
        context['form'] = form
        context['title'] = "Document Type "

        return render(request, self.template_name, context)


@transaction.atomic
def hrm_document_type_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    app_user_id = request.session['app_user_id']
    if request.method == 'POST':
        form = EmployeeDocumentTypeForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post = form.save(commit=False)
                    document_type_id = fn_get_document_id()
                    post.document_type_id = document_type_id
                    post.app_user_id = app_user_id
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = "document type create successfully"
                    data['error_message'] = ''
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)

        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


@transaction.atomic
def hrm_document_type_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(
        Employee_Document_Type, document_type_id=id)
    print(instance_data)
    template_name = 'hrm/hrm-document-type-edit.html'
    data = dict()
    if request.method == "POST":
        form = EmployeeDocumentTypeForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj = form.save(commit=False)
                    obj.save()
                    data['success_message'] = "updated successfully!"
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
        form = EmployeeDocumentTypeForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        context['title'] = "Document Type "

        data['html_form'] = render_to_string(
            template_name, context, request=request
        )

    return JsonResponse(data)
# X-X-X-X-X-X-X-X-X-X-X-X------hrm-document type-end-------X-X-X-X-X-X-X-X-X-X-X-X


# ----------------------------hrm-employee document Info-start------------------------------
class hrm_employee_document_info_create_view(LoginRequiredMixin, TemplateView):
    template_name = 'hrm/hrm-employee-document-info.html'

    def get(self, request):
        form = EmployeeDocumentForm()
        context = get_global_data(request)
        context['form'] = form
        context['title'] = "Employee Document "

        return render(request, self.template_name, context)


@transaction.atomic
def hrm_employee_document_info_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    app_user_id = request.session['app_user_id']
    if request.method == 'POST':
        form = EmployeeDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post = form.save(commit=False)
                    file_obj = request.GET.get('file')
                    post.document_location = file_obj
                    print(file_obj)
                    post.app_user_id = app_user_id
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = "document insert successfully"
                    data['error_message'] = ''
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)

        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


@transaction.atomic
def hrm_employee_document_info_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Employee_Document, id=id)
    print(instance_data)
    template_name = 'hrm/hrm-employee-document-info-edit.html'
    data = dict()
    if request.method == "POST":
        form = EmployeeDocumentForm(
            request.POST, request.FILES, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj = form.save(commit=False)
                    obj.save()
                    data['success_message'] = "updated successfully!"
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
        form = EmployeeDocumentForm(
            request.POST, request.FILES, instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        context['title'] = "Employee Document "

        data['html_form'] = render_to_string(
            template_name, context, request=request
        )

    return JsonResponse(data)

# X-X-X-X-X-X-X-X-X-X-X-X------hrm-employee-document info-end-------X-X-X-X-X-X-X-X-X-X-X-X


# ----------------------------hrm-leave-info-start------------------------------
class hrm_employee_leave_info_create_view(LoginRequiredMixin, TemplateView):
    template_name = 'hrm/hrm-emp-leave-info.html'

    def get(self, request):
        form = LeaveInfoForm()
        context = get_global_data(request)
        context['form'] = form
        context['title'] = "Employee Leave "

        return render(request, self.template_name, context)


@transaction.atomic
def hrm_employee_leave_info_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    app_user_id = request.session['app_user_id']
    if request.method == 'POST':
        form = LeaveInfoForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post = form.save(commit=False)
                    leave_id = fn_get_leave_id()
                    post.leave_id = leave_id
                    post.app_user_id = app_user_id
                    post.save()
                    data['id'] = leave_id
                    data['form_is_valid'] = True
                    data['success_message'] = "Leave info create successfully"
                    data['error_message'] = ''
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)

        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


@transaction.atomic
def hrm_employee_leave_info_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Leave_Info, leave_id=id)
    print(instance_data)
    template_name = 'hrm/hrm-emp-leave-edit.html'
    data = dict()
    if request.method == "POST":
        form = LeaveInfoForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj = form.save(commit=False)
                    obj.save()
                    data['success_message'] = "Updated Successfully!"
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
        form = LeaveInfoForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        context['title'] = "Employee Leave "

        data['html_form'] = render_to_string(
            template_name, context, request=request
        )

    return JsonResponse(data)
# X-X-X-X-X-X-X-X-X-X-X-X------hrm-leave-info-end-------X-X-X-X-X-X-X-X-X-X-X-X
# ----------------------------hrm-leave-application-start------------------------------


class hrm_employee_leave_application_create_view(LoginRequiredMixin, TemplateView):
    template_name = 'hrm/hrm-emp-leave-application.html'

    def get(self, request):
        form = LeaveApplicationForm()
        context = get_global_data(request)
        context['form'] = form
        context['title'] = "Employee Leave Application "

        return render(request, self.template_name, context)


@transaction.atomic
def hrm_employee_leave_application_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    app_user_id = request.session['app_user_id']
    if request.method == 'POST':
        form = LeaveApplicationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post = form.save(commit=False)
                    post.app_user_id = app_user_id
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = "Leave info create successfully"
                    data['error_message'] = ''
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)

        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


@transaction.atomic
def hrm_employee_leave_application_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Leave_Application, id=id)
    print(instance_data)
    template_name = 'hrm/hrm-emp-leave-application-edit.html'
    data = dict()
    if request.method == "POST":
        form = LeaveApplicationForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj = form.save(commit=False)
                    obj.save()
                    data['success_message'] = "Updated Successfully!"
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
        form = LeaveApplicationForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        context['title'] = "Employee Leave Application "

        data['html_form'] = render_to_string(
            template_name, context, request=request
        )

    return JsonResponse(data)


@transaction.atomic
def hrm_employee_leave_application_approve(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Leave_Application, id=id)
    print(instance_data)
    template_name = 'hrm/hrm-emp-leave-application-approve.html'
    data = dict()
    if request.method == "POST":
        comments = request.POST.get('comments')
        approve = request.POST.get('approve')
        print(approve)
        try:
            with transaction.atomic():
                if approve == 'true':
                    instance_data.approval_comments = comments
                    instance_data.approval_status = 'Approved'
                else:
                    instance_data.approval_comments = comments
                    instance_data.approval_status = 'unapprove'
                instance_data.save()

                data['success_message'] = "Updated Successfully!"
                data['error_message'] = ''
                data['form_is_valid'] = True
                return JsonResponse(data)
        except Exception as e:
            print(str(e))
            data['form_is_valid'] = False
            data['error_message'] = str(e)
            return JsonResponse(data)

    else:
        context = get_global_data(request)
        context['id'] = id
        context['title'] = "Employee Leave Application "

        data['html_form'] = render_to_string(
            template_name, context, request=request
        )

    return JsonResponse(data)


# X-X-X-X-X-X-X-X-X-X-X-X------hrm-leave-application-end-------X-X-X-X-X-X-X-X-X-X-X-X

# ----------------------------hrm-employee-traning-info-start------------------------------
class hrm_employee_training_info_create_view(LoginRequiredMixin, TemplateView):
    template_name = 'hrm/hrm-emp-Training-info.html'

    def get(self, request):
        form = EmployeeTrainingForm()
        context = get_global_data(request)
        context['form'] = form
        context['title'] = "Employee  Tranining "

        return render(request, self.template_name, context)


@transaction.atomic
def hrm_employee_training_info_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    app_user_id = request.session['app_user_id']
    if request.method == 'POST':
        form = EmployeeTrainingForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post = form.save(commit=False)
                    post.app_user_id = app_user_id
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = "Traning Info Create Successfully"
                    data['error_message'] = ''
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)

        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


@transaction.atomic
def hrm_employee_training_info_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Employee_Training, id=id)
    print(instance_data)
    template_name = 'hrm/hrm-emp-Training-edit.html'
    data = dict()
    if request.method == "POST":
        form = EmployeeTrainingForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj = form.save(commit=False)
                    obj.save()
                    data['success_message'] = "Updated Successfully!"
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
        form = EmployeeTrainingForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        context['title'] = "Employee  Tranining "

        data['html_form'] = render_to_string(
            template_name, context, request=request
        )

    return JsonResponse(data)
# X-X-X-X-X-X-X-X-X-X-X-X------hrm-traning-info-end-------X-X-X-X-X-X-X-X-X-X-X-X

# ----------------------------hrm-pay-bill-info-start------------------------------


class hrm_pay_bill_info_create_view(LoginRequiredMixin, TemplateView):
    template_name = 'hrm/hrm-pay-bill-info.html'

    def get(self, request):
        form = PayBillForm()
        context = get_global_data(request)
        context['form'] = form
        context['title'] = "Bill info "
        return render(request, self.template_name, context)


@transaction.atomic
def hrm_pay_bill_info_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    app_user_id = request.session['app_user_id']
    if request.method == 'POST':
        form = PayBillForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post = form.save(commit=False)
                    post.app_user_id = app_user_id
                    bill_id = fn_get_bill_id()
                    post.bill_id = bill_id
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = "Traning Info Create Successfully"
                    data['error_message'] = ''
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)

        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


@transaction.atomic
def hrm_pay_bill_info_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Pay_Bill, bill_id=id)
    template_name = 'hrm/hrm-paybill-edit.html'
    data = dict()
    if request.method == "POST":
        form = PayBillForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj = form.save(commit=False)
                    obj.save()
                    data['success_message'] = "Updated Successfully!"
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
        form = PayBillForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id

        context['title'] = "Bill info "

        data['html_form'] = render_to_string(
            template_name, context, request=request
        )

    return JsonResponse(data)



@transaction.atomic
def hrm_salary_scale_details_modal(request, id=0):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    salary_scale_details_list=Salary_Scale_Details.objects.filter(salscale_id=id)
    branch_code = request.session['branch_code']
    app_user_id = request.session["app_user_id"]
    if request.method == "GET":
        template_name = 'hrm/hrm-salary-scale-details.html'
        cbd = get_business_date(branch_code, app_user_id)
        form = SalaryScaleDetailsForm(initial={'effective_date': cbd})
        context = get_global_data(request)
        context['salary_scale_details_list'] = salary_scale_details_list
        context['form'] = form
        context['id'] = id
        context['title'] = "Salary Scale Type"
        data['html_form'] = render_to_string(
            template_name, context, request=request
        )
        return JsonResponse(data)

@transaction.atomic
def hrm_salary_Scale_details_insert(request, id=0):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    if(request.method == "POST"):
        app_user_id = request.session['app_user_id']
        form = SalaryScaleDetailsForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    post = form.save(commit=False)
                    salsdtlcale_id = fn_get_salsdtlcale_id()
                    post.salsdtlcale_id = salsdtlcale_id
                    post.app_user_id = app_user_id
                    post.app_date_time = timezone.now()
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = "Salary Scale Details Add Successfully"
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)

        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


@transaction.atomic
def hrm_salary_scale_details_edit(request, id=0):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    try:
        with transaction.atomic():
            instance_data=get_object_or_404(Salary_Scale_Details,salsdtlcale_id=id)
            salscale_id=instance_data.salscale_id
            if(request.method == "POST"):
                app_user_id = request.session['app_user_id']
                form = SalaryScaleDetailsForm(request.POST, instance=instance_data)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.salscale_id=salscale_id
                    post.app_user_id = app_user_id
                    post.app_date_time = timezone.now()
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = "Salary Scale Details Update Successfully"
                    data['salscale_id'] = instance_data.salscale_id
                    return JsonResponse(data)
                else:
                    data['error_message'] = form.errors.as_json()
            else:
                template_name = 'hrm/hrm-salary-scale-details-edit.html'
                form = SalaryScaleDetailsForm(instance=instance_data)
                form.fields['salscale_id'].disabled = True
                context = get_global_data(request)
                context['form'] = form
                context['id'] = id
                context['title'] = "Salary Scale Details"
                data['html_form'] = render_to_string(
                    template_name, context, request=request
                )
                return JsonResponse(data)
    except Exception as e:
        print(str(e))
        data['form_is_valid'] = False
        data['error_message'] = str(e)
        return JsonResponse(data)
    return JsonResponse(data)



def hrm_salary_scale_bonus_modal(request, id=0):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    salary_scale_details= Salary_Scale_Details.objects.get(salsdtlcale_id=id)
    if(request.method == "GET"):
        template_name = 'hrm/hrm-salary-bonus-create.html'
        salary_scale_bonous = Salary_Scale_Bonous.objects.filter(salsdtlcale_id=id)
        form = SalaryBonusDetailsForm()    
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        context['salary_scale_bonous'] = salary_scale_bonous
        context['salary_scale_details'] = salary_scale_details
        data['html_form'] = render_to_string(
            template_name, context, request=request
        )
        return JsonResponse(data)
    data['error_message'] = ""
    return JsonResponse(data)


@transaction.atomic
def hrm_salary_scale_bonus_create(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    if(request.method == "POST"):
        form = SalaryBonusDetailsForm(request.POST) 
        if form.is_valid():
            try:
                with transaction.atomic():
                    branch_code = request.session['branch_code']
                    app_user_id = request.session['app_user_id']
                    obj = form.save(commit=False)
                    obj.bonus_id = fn_get_salsbonus_id(branch_code)
                    obj.salscale_id = obj.salsdtlcale_id.salscale_id
                    obj.app_data_time = timezone.now()
                    obj.app_user_id = app_user_id
                    obj.save()
                    data['success_message'] = "Create Bonus Successfully!"
                    data['error_message'] = ''
                    data['form_is_valid'] = True
                    return JsonResponse(data)
            except Exception as e:
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = ""
            return JsonResponse(data)


@transaction.atomic
def hrm_salary_bonus_details_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    instance_data=get_object_or_404(Salary_Scale_Bonous,bonus_id=id)
    if(request.method == "POST"):
        form = SalaryBonusDetailsForm(request.POST,instance=instance_data) 
        if form.is_valid():
            try:
                with transaction.atomic():
                    app_user_id = request.session['app_user_id']
                    obj = form.save(commit=False)
                    obj.app_data_time = timezone.now()
                    obj.app_user_id = app_user_id
                    obj.save()
                    data['success_message'] = "Update Bonus Successfully!"
                    data['error_message'] = ''
                    data['form_is_valid'] = True
                    return JsonResponse(data)
            except Exception as e:
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)
        data['error_message'] = "Some error"
        return JsonResponse(data)
    else:
        template_name = 'hrm/hrm-salary-bonus-edit.html'
        salary_scale_bonous = Salary_Scale_Bonous.objects.filter(salsdtlcale_id=instance_data.salsdtlcale_id.salsdtlcale_id)
        form = SalaryBonusDetailsForm(instance=instance_data)    
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        context['salary_scale_bonous'] = salary_scale_bonous
        context['salary_scale_details'] = instance_data.salsdtlcale_id
        data['html_form'] = render_to_string(
            template_name, context, request=request
        )
        return JsonResponse(data)


def hrm_salary_scale_slip_modal(request, id=0):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
   
    salaryScale = Salary_Scale.objects.get(salscale_id=id)
    if(request.method == "GET"):
        template_name = 'hrm/hrm-salary-scale-slip.html'
        
        context = get_global_data(request)
        context['salaryScale'] = salaryScale
        context['title'] = "Salary Scale Slip"
        data['html_form'] = render_to_string(
            template_name, context, request=request
        )
        return JsonResponse(data)


class hrm_employee_list_form(LoginRequiredMixin, TemplateView):
    template_name = 'hrm/hrm-employee-list-form.html'

    def get(self, request):
        context = get_global_data(request)
        context['title'] = "Employee List"
        return render(request, self.template_name, context)


@transaction.atomic
def hrm_employee_list_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    instance_data2 = dict()
    try:
        with transaction.atomic():
            instance_data2 = Employee_Nominee.objects.filter(
                employee_id=id).first()
            instance_data = Employee_Details.objects.filter(
                employee_id=id).first()
            template_name = 'hrm/hrm-employee-list-edit.html'
            if request.method == 'POST':
                print('Post')
                is_teacher = request.POST.get('is_teacher', None)
                form = EmployeeDetailsForm(
                    request.POST, instance=instance_data)
                third_form = EmployeeNomineeForm(
                    request.POST, instance=instance_data2)
                print(third_form.is_valid)
                print(third_form.errors.as_json())
                if form.is_valid() and third_form.is_valid():
                    print(is_teacher)
                    obj = form.save(commit=False)
                    obj2 = third_form.save(commit=False)
                    if(instance_data2 is not None):
                        obj2.employee_id = instance_data
                        obj2.nominee_serial = instance_data2.nominee_serial
                    else:
                        obj2.employee_id = instance_data
                        obj2.nominee_serial = fn_serial_no_id()
                    obj2.save()
                    obj.save()
                    teacher_row = Teacher.objects.filter(
                        employee_id=instance_data).first()
                    print("teacher", teacher_row)
                    if(is_teacher is not None):
                        if(is_teacher == 'A'):
                            if(teacher_row is not None):
                                teacher_row.status = 'A'
                                teacher_row.save()
                            else:
                                Teacher.objects.create(teacher_id=fn_get_teacher_id(
                                ), employee_id=instance_data, status='I')
                        else:
                            if(teacher_row is not None):
                                teacher_row.status = 'I'
                                teacher_row.save()
                            else:
                                Teacher.objects.create(teacher_id=fn_get_teacher_id(
                                ), employee_id=instance_data, status='I')
                    else:
                        if(teacher_row is not None):
                            teacher_row.status = 'I'
                            teacher_row.save()
                        else:
                            Teacher.objects.create(
                                teacher_id=fn_get_teacher_id(), employee_id=instance_data, status='I')

                    data['success_message'] = "Updated Successfully!"
                    data['error_message'] = ''
                    data['form_is_valid'] = True
                    return JsonResponse(data)
                else:
                    data['error_message'] = form.errors.as_json()
                    data['error_message'] = third_form.errors.as_json()
                    data['form_is_valid'] = False
                    print(form.errors.as_json())
                    print(third_form.errors.as_json())
                    return JsonResponse(data)
            else:
                form = EmployeeDetailsForm(instance=instance_data)
                if instance_data2:
                    third_form = EmployeeNomineeForm(instance=instance_data2)
                else:
                    third_form = EmployeeNomineeForm()
                education_degree = Employee_Education.objects.filter(
                    employee_id=id)
                degree_info = Degree_Info.objects.all()
                context = get_global_data(request)
                context['form'] = form
                context['third_form'] = third_form
                context['employee_id'] = id
                context['degree_info'] = degree_info
                context['employee_data'] = instance_data
                context['education_degree'] = education_degree
                return render(request, template_name, context)
    except Exception as e:
        print(e)
        data['error_message'] = str(e)
        data['form_is_valid'] = False
        return JsonResponse(data)


@transaction.atomic
def hrm_employee_nominee_info_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    app_user_id = request.session['app_user_id']
    if request.method == 'POST':
        form = EmployeeNomineeForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post = form.save(commit=False)
                    post.app_user_id = app_user_id
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = "Nomenee Create Successfully"
                    data['error_message'] = ''
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)

        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)
