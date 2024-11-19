
from threading import Thread
import time
import os
import pdfkit
import imgkit
from PIL import Image
from django.core.files.base import ContentFile
import base64
from django.utils.crypto import get_random_string
import mimetypes
from fpdf import FPDF, HTMLMixin
import io
from appauth.utils import fn_get_query_result
import decimal
from django.db.models.fields import NullBooleanField
from .myException import *
from .validations import *
from .utils import *
from .forms import *
from .models import *
from .models import Application_Settings as Academy_info
from finance.utils import *
from decimal import Context, Decimal
from django.shortcuts import render
from django.core.files import File
# Create your views here.
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
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
from django.db.models import Count, Sum, Avg, Q
import logging
import sys
logger = logging.getLogger(__name__)
from .views import get_global_data
from appauth.utils import fn_get_reports_parameter
from appauth.views import get_global_report_data

from .report_data import *

class edu_filter_student_print_report_form(TemplateView):
    template_name = 'edu/edu-filter-student-print-report-form.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = CommonReportForm()
        branchs = Branch.objects.all().order_by('branch_code')
        context = get_global_data(request)
        context['form'] = form
        context['branchs'] = branchs
        return render(request, self.template_name, context)
    


def edu_filter_student_print_report_view(request):
    template_name = "edu/edu-filter-student-print-report-view.html"
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    gender = request.GET['gender']
    branch_code = request.GET['branch_code']
    academic_year = request.GET['academic_year']
    class_id = request.GET['class_name']
    class_group_id = request.GET['id_class_group_id']
    p_class_name=""
    p_class_group=""
    dtl_data = Students_Info.objects.filter(branch_code=branch_code,student_status='A').order_by('student_roll')
    header=Admission_form_header.objects.filter(branch_code=branch_code).first()
    if(academic_year!=""):
        dtl_data=dtl_data.filter(academic_year=academic_year)    
    if(class_id != ""):
        p_class_name = Academic_Class.objects.get(class_id=class_id)
        dtl_data = dtl_data.filter(class_id=class_id)
    if(class_group_id != ""):
        p_class_group = Academic_Class_Group.objects.get(class_group_id=class_group_id)
        dtl_data = dtl_data.filter(class_group_id=class_group_id)
    if(gender != ""):
        dtl_data = dtl_data.filter(student_gender=gender)
    context=get_global_report_data(request)
    context['dtl_data'] = dtl_data
    context['p_gender'] = gender
    context['p_academic_year'] = academic_year
    context['p_class_name'] = p_class_name
    context['p_class_group'] = p_class_group
    context['header'] = header
    return render(request,template_name,context)


class edu_quick_collection_printview(TemplateView):
    template_name = 'edu_report/edu-quick-collection-printview.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            branch_code = request.GET.get("branch_code")
            data = get_global_report_data(request)
            rep_param = fn_get_reports_parameter(app_user_id)
            dtl_data, students, sum_data = fn_get_quick_collection(rep_param['p_transaction_id'])
            
            form_hader=Admission_form_header.objects.filter(branch_code=students[0]['branch_code']).first()
            data['company_name']=form_hader.academic_name
            data['form_hader']=form_hader
            data['receive_date'] = students[0]['receive_date']
            data['student_roll'] = students[0]['student_roll']
            data['student_name'] = students[0]['student_name']
            data['receive_amount'] = students[0]['receive_amount']
            data['receipt_by'] = students[0]['app_user_id']
            data['app_data_time'] = students[0]['app_data_time']
            data['cancel_by'] = students[0]['cancel_by']
            data['class_name'] = dtl_data[0]['class_name']
            data['dtl_data'] = dtl_data
            data['sum_data'] = sum_data
            data = {**data, **rep_param}
            
            return render(request, self.template_name, data)
        except Exception as e:
            print(str(e))
            return render(request, self.template_name)

class edu_report_studentfeescollection(TemplateView):
    template_name = 'edu_report/edu-report-studentfeescollection.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'sales/sales-login.html')

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = Common_Education_Report(
            initial={'branch_code': branch_code, 'from_date': cbd, 'upto_date': cbd})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)


class edu_report_studentfeescollection_print_view(TemplateView):
    template_name = 'edu_report/edu-report-studentfeescollection-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_studentfeescollection_details(app_user_id)
            sum_data = fn_get_studentfeescollection_summary(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data['sum_data'] = sum_data
            data = {**data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            print(str(e))
            return render(request, self.template_name)

class edu_report_studentfeescollection_details_print_view(TemplateView):
    template_name = 'edu_report/edu-report-studentfeescollection-details-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_studentfeescollection_details(app_user_id)
            sum_data = fn_get_studentfeescollection_summary(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data['sum_data'] = sum_data
            data = {**data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            print(str(e))
            return render(request, self.template_name)

class edu_report_Month_Wise_Fess_Collection_summary_print_view(TemplateView):
    template_name = 'edu_report/edu-report-Month-Wise-Fess-Collection-summary-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data =fn_get_Month_Wise_Fess_Collection_Detais (app_user_id)
            sum_data = fn_get_Month_Wise_Fess_Collection_Summary(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data['sum_data'] = sum_data
            data = {**data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            print(str(e))
            return render(request, self.template_name)  


class edu_report_class_wise_fees_collection_summary_print_view(TemplateView):
    template_name = 'edu_report/edu-report-class-wise-fees-collection-summary-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data =fn_get_Month_Wise_Fess_Collection_Detais (app_user_id)
            sum_data = fn_get_Month_Wise_Fess_Collection_Summary(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data['sum_data'] = sum_data
            data = {**data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            print(str(e))
            return render(request, self.template_name)  

 
class edu_report_class_wise_payment_status_print_view(TemplateView):
    template_name = 'edu_report/edu-report-class-wise-payment-status-print-view.html'

class edu_subject_list_search(TemplateView):
    template_name = 'edu/edu-subjectlist-search.html'
 
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            data=dict()
            form = SubjectListModelForm()
            data['form']=form
            return render(request, self.template_name, data)
        except Exception as e:
            print(str(e))
            return render(request, self.template_name)              

class edu_report_studentfeesdue(TemplateView):
    template_name = 'edu_report/edu-report-studentfeedue.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'sales/sales-login.html')

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = Common_Education_Report(
            initial={'branch_code': branch_code, 'from_date': cbd, 'upto_date': cbd})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)

def edu_subject_list_search_print_view(request):
    template_name = 'edu_report/edu-subjectlist-print-view.html'
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    
    try:
        app_user_id = request.session["app_user_id"]
        class_id = request.GET['class_id']
        class_group_id = request.GET['class_group_id']
        data=dict()
        
        dataFilter=dict()
        dataFilter['class_id']=class_id
        if class_group_id:
            dataFilter['class_group_id']=class_group_id
        subjects=Subject_List.objects.filter(**dataFilter)
        acadamicinfo=Academy_info.objects.first()
        data['subjects']=subjects
        data['acadamicinfo']=acadamicinfo
        return render(request, template_name, data)
    except Exception as e:
        return render(request, template_name)


class edu_report_studentfeesunpaid(TemplateView):
    template_name = 'edu_report/edu-report-studentfeesunpaid.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'sales/sales-login.html')

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = Common_Education_Report(
            initial={'branch_code': branch_code, 'from_date': cbd, 'upto_date': cbd})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)


class edu_report_studentunpaidlist_print_view(TemplateView):
    template_name = 'edu_report/edu-report-studentunpaidlist-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_studentunpaidlist_details(app_user_id)
            sum_data = fn_get_studentunpaidlist_summary(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data['sum_data'] = sum_data
            data = {**data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            print(str(e))
            return render(request, self.template_name)


class edu_report_class_wise_unpaidlist_print_view(TemplateView):
    template_name = 'edu_report/edu-report-class-wise-unpaidlist-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_class_wise_unpaidlist_details(app_user_id)
            sum_data = fn_get_class_wise_unpaidlist_summary(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data['sum_data'] = sum_data
            data = {**data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            print(str(e))
            return render(request, self.template_name)



class edu_report_monthly_unpaidlist_print_view(TemplateView):
    template_name = 'edu_report/edu-report-monthly-unpaidlist-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_monthly_unpaidlist_details(app_user_id)
            sum_data = fn_get_monthly_unpaidlist_summary(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data['sum_data'] = sum_data
            data = {**data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            print(str(e))
            return render(request, self.template_name)            
