from finance.utils import fn_get_cash_gl_code, fn_transfer_tran_posting, fn_cancel_tran_batch
from appauth.utils import get_business_date, fn_get_query_result
from appauth.views import get_global_data
import decimal
from edu.utils import gn_edu_get_student_branch
from django.db.models.fields import NullBooleanField
from django.utils.translation import templatize
from .validations import *
from .utils import *
from .forms import *
from .models import *
from decimal import Context, Decimal
from django.shortcuts import render

# Create your views here.
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


class hostel_bedtype_createlist(TemplateView):
    template_name = 'hostel/hostel-bedtype-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = BedTypeModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def hostel_bedtype_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = BedTypeModelForm(request.POST)
        if form.is_valid():
            bedtype_id = fn_get_bedtype_id()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.bed_type_id = bedtype_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Bed Type Name Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def hostel_bedtype_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Bed_Type, bed_type_id=id)
    template_name = 'hostel/hostel-bedtype-edit.html'
    data = dict()

    if request.method == 'POST':
        form = BedTypeModelForm(request.POST, instance=instance_data)
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
        form = BedTypeModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


class hostel_payfortype_createlist(TemplateView):
    template_name = 'hostel/hostel-payfortype-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = PayForTypeModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def hostel_payfortype_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    if request.method == 'POST':
        form = PayForTypeModelForm(request.POST)
        if form.is_valid():
            payfor_type_id = fn_get_payfor_type_id()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.pay_for_id = payfor_type_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'PayFor Type Name Added Succesfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def hostel_payfortype_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(PayFor_Types, pk=id)
    template_name = 'hostel/hostel-payfortype-edit.html'
    data = dict()
    if request.method == 'POST':
        form = PayForTypeModelForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            data['success_message'] = 'Update Successfully!'
            data['error_message'] = ''
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = PayForTypeModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


class hostel_bedmanagement_createlist(TemplateView):
    template_name = 'hostel/hostel-bedmanagement-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = BedManagementModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def hostel_bedmanagement_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    if request.method == 'POST':
        form = BedManagementModelForm(request.POST)
        if form.is_valid():
            beds_management_id = fn_get_bedmanage_id()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.beds_management_id = beds_management_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Bed Management Info Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def hostel_bedmanagement_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Beds_Management, pk=id)
    template_name = 'hostel/hostel-bedmanagement-edi.html'
    data = dict()
    if request.method == "POST":
        form = BedManagementModelForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            data['success_message'] = 'Update SuccessfullD!'
            data['error_message'] = ''
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = BedManagementModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


class hostel_roommanagement_createlist(TemplateView):
    template_name = 'hostel/hostel-roommanagement-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = RoomManagementModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def hostel_roommanagement_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_id_valid'] = False
    if request.method == 'POST':
        form = RoomManagementModelForm(request.POST)
        if form.is_valid():
            rooms_management_id = fn_get_roommanage_id()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.rooms_management_id = rooms_management_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Room Management Info Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def hostel_roommanagement_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Rooms_Management, pk=id)
    template_name = 'hostel/hostel-roommanagement-edit.html'
    data = dict()
    if request.method == 'POST':
        form = RoomManagementModelForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            data['success_message'] = 'Update Successfullay!'
            data['error_message'] = ''
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = RoomManagementModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


class hostel_paymentmanage_createlist(TemplateView):
    template_name = 'hostel/hostel-paymentmanage-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        # form = FeesMappingModelForm()
        form = PaymentManageModelForm(initial={'payment_date': cbd})
        form.files
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def hostel_paymentmanage_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    if request.method == 'POST':
        form = PaymentManageModelForm(request.POST)
        # post=form.save(commit=False)
        if form.is_valid():
            payment_management_id = fn_get_paymanage_id()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.payment_management_id = payment_management_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Payment Management Info Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def hostel_paymentmanage_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Payment_Management, pk=id)
    template_name = 'hostel/hostel-paymentmanage-edit.html'
    data = dict()
    if request.method == 'POST':
        form = PaymentManageModelForm(request.POST, instance=instance_data)
        data['form_is_valid'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            data['success_message'] = 'Update Successfully!'
            data['errora_message'] = ''
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = PaymentManageModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


class hostel_admission_createlist(TemplateView):
    template_name = 'hostel/hostel-admission-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        branch_code = request.session["branch_code"]
        app_user_id = request.session["app_user_id"]
        cbd = get_business_date(branch_code, app_user_id)
        form = HostelAdmitModelForm(initial={'admit_date': cbd})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def hostel_admission_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    proc_data = dict()
    data['form_is_valid'] = False
    if request.method == 'POST':
        form = HostelAdmitModelForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():

                    admit_id = fn_get_admit_id()
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.admit_id = admit_id
                    admission_gl = gn_hostel_get_admission_gl()
                    cash_gl_code = fn_get_cash_gl_code()
                    transaction_master = {}
                    transaction_details = {}
                    
                    tran_details = []
                    batch_number = 0
                    tran_amount = post.admit_fees
                    if tran_amount is None:
                        tran_amount=0.00
                    
                    transaction_master["tran_date"] = post.admit_date
                    transaction_master["branch_code"] = post.branch_code
                    transaction_master["tran_type"] = 'HOST_ADMIT'
                    transaction_master["transaction_screen"] = 'HOST_ADMIT'
                    transaction_master["app_user_id"] = request.session["app_user_id"]
                    transaction_master["master_narration"] = "Hostel Admission Fees : " + ( post.student_roll.student_roll)

                    if float(tran_amount) > 0.00:
                        tran_gl_code = admission_gl
                        if not tran_gl_code:
                            data['error_message'] = 'Admission Fee Ledger is Not Define!'
                            Exception(data['error_message'])
                        narration = "Hostel Admission Fees : " + \
                            (post.student_roll.student_roll)

                        transaction_details = {}
                        transaction_details["account_number"] = '0'
                        transaction_details["account_phone"] = ''
                        transaction_details["tran_gl_code"] = tran_gl_code
                        transaction_details["contra_gl_code"] = cash_gl_code
                        transaction_details["tran_debit_credit"] = 'C'
                        transaction_details["tran_amount"] = tran_amount
                        transaction_details["transaction_narration"] = narration
                        transaction_details["tran_document_number"] = ''
                        tran_details.append(transaction_details)

                        transaction_details = {}
                        transaction_details["account_number"] = '0'
                        transaction_details["account_phone"] = ''
                        transaction_details["tran_gl_code"] = cash_gl_code
                        transaction_details["contra_gl_code"] = tran_gl_code
                        transaction_details["tran_debit_credit"] = 'D'
                        transaction_details["tran_amount"] = tran_amount
                        transaction_details["transaction_narration"] = narration
                        transaction_details["tran_document_number"] = ''
                        tran_details.append(transaction_details)

                        if len(tran_details) > 0:

                            status, message, batch_number = fn_transfer_tran_posting(
                                transaction_master, tran_details)

                            if not status:
                                data['error_message'] = 'Error in Hostel Admission Fee Receive!\n'+message
                                logger.error("Error in Fee Receive hostel_admission_insert {} \nType: {} \nError:{}".format(
                                    sys.exc_info()[-1], type(message).__name__, str(message)))
                                raise Exception(data['error_message'])
                    post.tran_batch_number = batch_number
                    post.save()
                    history = Hostel_Admit_History()
                    history.admit_id = post
                    history.academic_year = post.academic_year
                    history.admit_date = post.admit_date
                    history.student_roll = post.student_roll
                    history.admit_fees = post.admit_fees
                    history.discount = post.discount
                    history.admit_status = post.admit_status
                    history.branch_code = post.branch_code
                    history.app_user_id = request.session["app_user_id"]
                    history.save()
                    process_id = fn_get_fees_processing_id(post.branch_code)

                    proc_data["process_id"] = process_id
                    proc_data["branch_code"] = post.branch_code
                    proc_data["academic_year"] = post.academic_year.academic_year

                    if post.student_roll:
                        proc_data["student_roll"] = post.student_roll.student_roll
                    else:
                        proc_data["student_roll"] = None

                    proc_data["process_date"] = post.admit_date
                    proc_data["app_user_id"] = post.app_user_id

                    status, error_message = fn_hostel_fees_processing_thread(proc_data)

                    data['form_is_valid'] = True
                    data['success_message'] = 'Hostel Admission Info Added Successfully!'
            except Exception as e:
                data['error_message'] = str(e)
                data['form_is_valid'] = False
                logger.error("Error on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                return JsonResponse(data)
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)

@transaction.atomic
def hostel_admission_cancel(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = {}
    app_user_id = request.session["app_user_id"]
    data['error_message'] = ''
    data['form_is_valid'] = False

    try:
        with transaction.atomic():

            status, error_message = fn_hostel_admission_cancel(
                id, app_user_id)
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

def hostel_admission_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Hostel_Admit, admit_id=id)
    template_name = 'hostel/hostel-admission-edit.html'
    data = dict()
    if request.method == 'POST':
        branch_code=instance_data.branch_code
        form = HostelAdmitModelForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            print(branch_code)
            obj.branch_code=instance_data.branch_code
            obj.save()
            history = Hostel_Admit_History()
            history.admit_id = obj
            history.academic_year = obj.academic_year
            history.admit_date = obj.admit_date
            history.student_roll = obj.student_roll
            history.admit_fees = obj.admit_fees
            history.discount = obj.discount
            history.admit_status = obj.admit_status
            history.branch_code = obj.branch_code
            history.app_user_id = request.session["app_user_id"]
            history.save()
            data['success_message'] = 'Update Successfully!'
            data['error_message'] = ''
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = HostelAdmitModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        context['instance_data'] = instance_data
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


class hostel_addingmeal_createlist(TemplateView):
    template_name = 'hostel/hostel-addingmeal-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = AddingMealModelForm()
        is_head_office_user = request.session["is_head_office_user"]
        if is_head_office_user == 'N':
            branch_code = request.session["branch_code"]
            print(branch_code)
            students=Hostel_Admit.objects.filter(branch_code=branch_code,admit_status='A')
        else:
            students=Hostel_Admit.objects.filter(admit_status='A')
        print(students)
        context = get_global_data(request)
        context['form'] = form
        context['students'] = students
        return render(request, self.template_name, context)


def hostel_addingmeal_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    if request.method == 'POST':
        form = AddingMealModelForm(request.POST)
        if form.is_valid():
            meal_id = request.POST.get('meal_id')
            student_roll = request.POST.get('student_roll')
            if Add_Student_To_Meal.objects.filter(meal_id=meal_id, student_roll=student_roll).exists():
                data['error_message'] = 'This info already exits'
                data['form_is_valid'] = False
                return JsonResponse(data)
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Hostel Meal to Student Info Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def hostel_addmeal_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Add_Student_To_Meal, pk=id)
    template_name = 'hostel/hostel-addmeal-edit.html'
    data = dict()
    if request.method == 'POST':
        form = AddingMealModelForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            meal_id = request.POST.get('meal_id')
            student_roll = request.POST.get('student_roll')
            if Add_Student_To_Meal.objects.filter(meal_id=meal_id, student_roll=student_roll).exists():
                data['error_message'] = 'This info already exits'
                data['form_is_valid'] = False
                return JsonResponse(data)
            obj = form.save(commit=False)
            obj.save()
            data['success_message'] = 'Update Successfully!'
            data['error_message'] = ''
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = AddingMealModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


class hostel_mealtype_createlist(TemplateView):
    template_name = 'hostel/hostel-mealtype-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = HostelMealTypeModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def hostel_mealtype_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    if request.method == 'POST':
        form = HostelMealTypeModelForm(request.POST)
        if form.is_valid():
            meal_type_id = fn_get_mealtype_id()
            # print(meal_type_id)
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.meal_type_id = meal_type_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Hostel Meal Type Name Insert Successfully'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def hostel_mealtype_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Meal_Type, pk=id)
    template_name = 'hostel/hostel-mealtype-edit.html'
    data = dict()
    if request.method == 'POST':
        form = HostelMealTypeModelForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            data['success_message'] = 'Update Succesfully!'
            data['error_message'] = ''
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = HostelMealTypeModelForm(instance=instance_data)
        context = get_global_data(request)
        context['id'] = id
        context['form'] = form
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


class hostel_meal_createlist(TemplateView):
    template_name = 'hostel/hostel-meal-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = HostelMealModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def hostel_meal_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    if request.method == 'POST':
        form = HostelMealModelForm(request.POST)
        if form.is_valid():
            meal_id = fn_get_meal_id()
            # print(meal_type_id)
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.meal_id = meal_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Hostel Meal Name Insert Successfully'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def hostel_meal_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Meal, pk=id)
    template_name = 'hostel/hostel-meal-edit.html'
    data = dict()
    if request.method == 'POST':
        form = HostelMealModelForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            data['success_message'] = 'Update Successfully!'
            data['error_message'] = ''
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = HostelMealModelForm(instance=instance_data)
        context = get_global_data(request)
        context['id'] = id
        context['form'] = form
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


class hostel_dailymeal_createlist(TemplateView):
    template_name = 'hostel/hostel-dailymeal-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        meal = Meal.objects.all()
        # students=Students_Info.objects.all()
        context = get_global_data(request)
        date = datetime.today().strftime("%Y-%m-%d")
        context['meal'] = meal
        context['today'] = date
        # context['students']=students
        return render(request, self.template_name, context)


def hostel_dailymeal_filterlist(request):
    template_name = 'hostel/hostel-dailymeal-filterlist.html'
    meal_id = request.GET.get('meal_id')
    meal_student = Add_Student_To_Meal.objects.filter(meal_id=meal_id)
    # print(meal_id)
    context = dict()
    if request.method == 'POST':
        meal_id = request.POST.get('meal_id')
        if meal_id:
            meal_student = Add_Student_To_Meal.objects.filter(meal_id=meal_id)
            context['meal_student'] = meal_student
            return render(request, template_name, context)
    context['meal_student'] = meal_student
    return render(request, template_name, context)


def hostel_dailymeal_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    if request.method == 'POST':
        meal_id = request.POST.get('meal_id')
        date = request.POST.get('date')
        Student_roll = request.POST.getlist(
            'student_roll')  # for all student roll getlist
        if not meal_id:
            data['error_message'] = 'Please Select Meal'
            return JsonResponse(data)
        if not date:
            data['error_message'] = 'Please Select Date'
            return JsonResponse(data)
        if not Student_roll:
            data['error_message'] = 'Please Select Student'
            return JsonResponse(data)
        meal_id = get_object_or_404(
            Meal, meal_id=request.POST.get('meal_id'))  # for foreign key
        for roll in Student_roll:
            # print(roll)
            st_roll = get_object_or_404(
                Students_Info, student_roll=roll)  # for foreign key
            for i in range(0, int(request.POST.get('eat_is'+str(roll)))):
                post = Daily_Meal()
                post.meal_id = meal_id
                post.meal_price = meal_id.meal_price
                post.date = date
                post.student_roll = st_roll
                post.is_eat = 1
                post.app_user_id = request.session["app_user_id"]
                post.save()
            data['form_is_valid'] = True
        data['success_message'] = 'Hostel Daily Meal Info Added Successfully!'
    else:
        data['error_message'] = 'Sorry Something went wrong!'
    return JsonResponse(data)


class hostel_dailymeal_studentlist(TemplateView):
    template_name = 'hostel/hostel-dailymeal-studentlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        students = Students_Info.objects.all()
        meals = Meal.objects.all()
        context = get_global_data(request)
        date = datetime.today().strftime("%Y-%m-%d")
        context['today'] = date
        context['students'] = students
        context['meals'] = meals
        return render(request, self.template_name, context)


def hostel_dailymeal_studentfilterlist(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    template_name = 'hostel/hostel-dailymeal-studentfilterlist.html'
    data = dict()
    context = get_global_data(request)
    if request.method == 'POST':
        datafilter = dict()
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        new_date1 = datetime.strptime(start_date, '%Y-%m-%d')
        new_date2 = datetime.strptime(end_date, '%Y-%m-%d')
        delta = new_date2-new_date1
        dates = []
        for day in range(0, delta.days+1):
            x = new_date1+timedelta(days=day)
            m = x.strftime("%b")
            d = x.strftime("%d")
            e_date = datetime.date(x)
            dates.append({'m': m, 'd': d, 'date': e_date})
        meal_id = request.POST.get('meal_id')
        student_roll = request.POST.get('student_roll')
        if meal_id:
            datafilter['meal_id'] = meal_id
        if student_roll:
            datafilter['student_roll'] = student_roll
        if start_date and end_date:
            datafilter['date__range'] = [new_date1, new_date2]
        # daily_meals=Daily_Meal.objects.filter(**datafilter)
        students = Daily_Meal.objects.values('student_roll', 'student_roll__student_name').annotate(
            data=Count('student_roll')).filter(**datafilter)
        meal_type = Meal_Type.objects.all()
        # context['daily_meals']=daily_meals
        context['dates'] = dates
        context['students'] = students
        context['meal_type'] = meal_type
        context['date_range'] = {'start': dates[0]
                                 ['date'], 'end': dates[len(dates)-1]['date']}
    else:
        daily_meals = Daily_Meal.objects.all()
        context['daily_meals'] = daily_meals
    data['html_form'] = render_to_string(
        template_name, context, request=request)
    # print(data)
    return JsonResponse(data)

def hostel_dailymeal_search_cancel(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    template_name = 'hostel/hostel-dailymeal-search-cancel.html'
    data = dict()
    context = get_global_data(request)
    if request.method == 'POST':
        datafilter = dict()
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        new_date1 = datetime.strptime(start_date, '%Y-%m-%d')
        new_date2 = datetime.strptime(end_date, '%Y-%m-%d')
        delta = new_date2-new_date1
        dates = []
        for day in range(0, delta.days+1):
            x = new_date1+timedelta(days=day)
            m = x.strftime("%b")
            d = x.strftime("%d")
            e_date = datetime.date(x)
            dates.append({'m': m, 'd': d, 'date': e_date})
        meal_id = request.POST.get('meal_id')
        student_roll = request.POST.get('student_roll')
        if meal_id:
            datafilter['meal_id'] = meal_id
        if student_roll:
            datafilter['student_roll'] = student_roll
        if start_date and end_date:
            datafilter['date__range'] = [new_date1, new_date2]
        # daily_meals=Daily_Meal.objects.filter(**datafilter)
        students = Daily_Meal.objects.values('student_roll', 'student_roll__student_name').annotate(
            data=Count('student_roll')).filter(**datafilter)
        meal_type = Meal_Type.objects.all()
        # context['daily_meals']=daily_meals
        context['dates'] = dates
        context['students'] = students
        context['meal_type'] = meal_type
        context['date_range'] = {'start': dates[0]
                                 ['date'], 'end': dates[len(dates)-1]['date']}
    else:
        daily_meals = Daily_Meal.objects.all()
        context['daily_meals'] = daily_meals
    data['html_form'] = render_to_string(
        template_name, context, request=request)
    # print(data)
    return JsonResponse(data)

def hostel_dailymeal_cancel(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    if request.method == 'POST':
        meal_id = request.POST.get('meal_id')
        qty = request.POST.get('qty')
        student_roll = request.POST.get('student_roll')
        date = request.POST.get('date')
        datetime_object = datetime.strptime(date, '%B %d, %Y')
        # for i in range(0,int(qty)):
        #     print(i)
        app_user_id = request.session["app_user_id"]
        Daily_Meal.objects.filter(student_roll=student_roll,meal_id=meal_id,date=datetime_object,cancel_on__isnull=True).update(cancel_on=timezone.now(),cancel_by=app_user_id)
        data['success_message'] = 'This Meals is cancel!'
    return JsonResponse(data)



def hostel_dailymeal_shortsummary(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    template_name = 'hostel/hostel-dailymeal-shortsummary.html'
    data = dict()
    context = get_global_data(request)
    if request.method == 'POST':
        datafilter = dict()
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        new_date1 = datetime.strptime(start_date, '%Y-%m-%d')
        new_date2 = datetime.strptime(end_date, '%Y-%m-%d')
        delta = new_date2-new_date1
        dates = []
        for day in range(0, delta.days+1):
            x = new_date1+timedelta(days=day)
            m = x.strftime("%b")
            d = x.strftime("%d")
            e_date = datetime.date(x)
            dates.append({'m': m, 'd': d, 'date': e_date})
        meal_id = request.POST.get('meal_id')
        student_roll = request.POST.get('student_roll')
        if meal_id:
            datafilter['meal_id'] = meal_id
        if student_roll:
            datafilter['student_roll'] = student_roll
        if start_date and end_date:
            datafilter['date__range'] = [start_date, end_date]
        meals=Daily_Meal.objects.filter(**datafilter,cancel_on__isnull=True)
        daily_meals = meals.annotate(
            data=Count('student_roll'))
        students = meals.values('student_roll', 'student_roll__student_name').annotate(
            data=Count('student_roll'))
        total = meals.values('student_roll').annotate(
            cost=Sum('meal_price'))
        avg_rate=meals.values('student_roll','meal_id__meal_name').annotate(
            cost=Sum('meal_price'), avg=Avg('meal_price'))
        
        context['dates'] = dates
        context['daily_meals'] = daily_meals
        context['students'] = students
        context['avg_rate'] = avg_rate
        context['total'] = total
        context['date_range'] = {'start': dates[0]
                                 ['date'], 'end': dates[len(dates)-1]['date']}
    else:
        daily_meals = Daily_Meal.objects.all()
        context['daily_meals'] = daily_meals
    data['html_form'] = render_to_string(
        template_name, context, request=request)
    return JsonResponse(data)

class hostel_hall_createlist(TemplateView):
    template_name = 'hostel/hostel-hall-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Hall_details_ModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def hostel_hall_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    if request.method == 'POST':
        form = Hall_details_ModelForm(request.POST)
        if form.is_valid():
            hall_code = fn_get_hall_code()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.app_data_time = timezone.now()
            post.hall_code = hall_code
            post.is_active = True
            post.is_deleted = False
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Hall Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def hostel_hall_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Hall_details, hall_code=id)
    template_name = 'hostel/hostel-hall-edit.html'
    data = dict()

    if request.method == 'POST':
        form = Hall_details_ModelForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
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
        form = Hall_details_ModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


def hostel_hall_delete(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Hall_details, pk=id)
    data = dict()
    instance_data.is_deleted = True
    instance_data.save()
    data['success_message'] = "Well Done"
    return JsonResponse(data)


class hostel_feesmapping_createlist(TemplateView):
    template_name = 'hostel/hostel-feesmapping-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        branch_code = request.session['branch_code']
        app_user_id = request.session["app_user_id"]
        cbd = get_business_date(branch_code, app_user_id)
        form = Hostel_Fees_Mapping_ModelForm(
            initial={'effective_date': cbd})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def hostel_feesmapping_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    if request.method == 'POST':
        form = Hostel_Fees_Mapping_ModelForm(request.POST)
        hist_form = Fees_Mapping_History_Model_Form(request.POST)
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
                    data['success_message'] = 'Fees Mapping Info Added Successfully!'
            except Exception as e:
                data['error_message'] = str(e)
                data['form_is_valid'] = False
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


@transaction.atomic
def hostel_feesmapping_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(Hostel_Fees_Mapping, pk=id)
    template_name = 'hostel/hostel-feesmapping-edit.html'
    data = dict()
    data_hist = dict()
    data['form_is_valid'] = True
    data['error_message'] = ''
    if request.method == 'POST':
        form = Hostel_Fees_Mapping_ModelForm(request.POST, instance=instance_data)
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
                        data_hist["head_code"] = obj.head_code
                        data_hist["hall_code"] = obj.hall_code
                        data_hist["effective_date"] = obj.effective_date
                        hist_post.day_serial = fn_get_hostel_fees_mapping_hist_count(
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
        form = Hostel_Fees_Mapping_ModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


def hostel_feesmapping_delete(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Fees_Mapping, pk=id)
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

class hostel_fees_processing(TemplateView):
    template_name = 'hostel/hostel-fees-processing.html'

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
def hostel_fees_processing_insert(request):
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

                if post.student_roll:
                    proc_data["student_roll"] = post.student_roll.student_roll
                else:
                    proc_data["student_roll"] = None

                proc_data["process_date"] = post.process_date
                proc_data["app_user_id"] = post.app_user_id

                if Fees_Processing_Details.objects.filter(branch_code=post.branch_code, academic_year=post.academic_year,
                                                          process_date=post.process_date,
                                                          student_roll=post.student_roll, process_status=False).exists():
                    data['form_is_valid'] = False
                    data['error_message'] = 'Process Running!'
                    return JsonResponse(data)
                status, error_message = fn_hostel_fees_processing_thread(proc_data)

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