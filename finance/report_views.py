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
from django.db import connection, transaction
from django.template.loader import render_to_string
from django.db.models import Count, Sum, Avg
from django.db.models import Q, F
import logging
import sys
logger = logging.getLogger(__name__)
from decimal import Decimal
from datetime import date, datetime, timedelta
import time

from .report_data import *
from appauth.models import Global_Parameters
from appauth.utils import fn_get_reports_parameter
from finance.utils import get_business_date
from finance.forms import AccountBalance, CommonReportForm
from appauth.views import get_global_data
from appauth.manage_session import fn_is_user_permition_exist
from appauth.views import get_global_report_data

class finance_report_accstmt_print_view(TemplateView):
    template_name = 'finance_report/finance-report-account-statement-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_acstat_details(app_user_id)
            sum_data = fn_get_acstat_summary(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data = {**data, **sum_data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            print(str(e))
            return render(request, self.template_name)


class finance_report_cashtrandetails(TemplateView):
    template_name = 'finance_report/finance-report-cashtrandetails.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'sales/sales-login.html')
        if not fn_is_user_permition_exist(request.session["app_user_id"], 'F10001002', 'Finance'):
            return HttpResponseRedirect(reverse("appauth-home"))

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = CommonReportForm(
            initial={'from_date': cbd, 'upto_date': cbd, 'branch_code': branch_code})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)


class finance_report_cashtrandetails_print_view(TemplateView):
    template_name = 'finance_report/finance-report-cashtrandetails-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_cashtrandetails_details(app_user_id)
            sum_data = fn_get_cashtrandetails_summary(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data = {**data, **sum_data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            print(str(e))
            return render(request, self.template_name)


class finance_report_ledgerstatements(TemplateView):
    template_name = 'finance_report/finance-report-ledgerstatements.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'sales/sales-login.html')
        if not fn_is_user_permition_exist(request.session["app_user_id"], 'F10001003', 'Finance'):
            return HttpResponseRedirect(reverse("appauth-home"))

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = CommonReportForm(
            initial={'from_date': cbd, 'upto_date': cbd, 'branch_code': branch_code})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)


class finance_report_ledgerstatements_print_view(TemplateView):
    template_name = 'finance_report/finance-report-ledgerstatements-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_cashtrandetails_details(app_user_id)
            sum_data = fn_get_cashtrandetails_summary(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data = {**data, **sum_data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            print(str(e))
            return render(request, self.template_name)


class finance_account_balance_report(TemplateView):
    template_name = 'finance_report/finance-report-account-balance.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'sales/sales-login.html')
        if not fn_is_user_permition_exist(request.session["app_user_id"], 'F10001001', 'Finance'):
            return HttpResponseRedirect(reverse("appauth-home"))

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = AccountBalance(
            initial={'branch_code': branch_code, 'ason_date': cbd})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)


class finance_report_accountbalance_print_view(TemplateView):
    template_name = 'finance_report/finance-account-balance-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_accountbalance_details(app_user_id)
            sum_data = fn_get_accountbalance_summary(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data = {**data, **sum_data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            print(str(e))
            return render(request, self.template_name)


class finance_report_tellerbalance(TemplateView):
    template_name = 'finance_report/finance-report-teller-balance.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'sales/sales-login.html')
        if not fn_is_user_permition_exist(request.session["app_user_id"], 'F20000003', 'Finance'):
            return HttpResponseRedirect(reverse("appauth-home"))

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        forms = AccountBalance(initial={'branch_code': branch_code,'from_date': cbd,'upto_date': cbd})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)


class finance_report_tellerbalance_print_view(TemplateView):
    template_name = 'finance_report/finance-report-teller-balance-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            rep_param = fn_get_reports_parameter(app_user_id)
            dtl_data = fn_get_tellerbalance_details(app_user_id)
            data['dtl_data'] = dtl_data
            data = {**data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            print(str(e))
            return render(request, self.template_name)


class finance_report_tellertransaction(TemplateView):
    template_name = 'finance_report/finance-report-teller-transaction.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'sales/sales-login.html')
        if not fn_is_user_permition_exist(request.session["app_user_id"], 'F20000003', 'Finance'):
            return HttpResponseRedirect(reverse("appauth-home"))

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        forms = AccountBalance(initial={'branch_code': branch_code,'from_date': cbd,'upto_date': cbd})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)


class finance_report_tellertransaction_print_view(TemplateView):
    template_name = 'finance_report/finance-report-teller-transaction-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            rep_param = fn_get_reports_parameter(app_user_id)
            dtl_data = fn_get_tellertransaction_details(app_user_id)
            sum_data = fn_get_tellertransaction_sum(app_user_id)
            data['sum_data'] = sum_data
            data['dtl_data'] = dtl_data
            data = {**data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            print(str(e))
            return render(request, self.template_name)

class finance_report_receiptpayment(TemplateView):
    template_name = 'finance_report/finance-report-receiptpayment.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        if not fn_is_user_permition_exist(request.session["app_user_id"], 'F10001004', 'Finance'):
            return HttpResponseRedirect(reverse("appauth-home"))

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = CommonReportForm(
            initial={'ason_date': cbd, 'from_date': cbd, 'upto_date': cbd, 'branch_code': branch_code})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)


class finance_report_receiptpayment_print_view(TemplateView):
    template_name = 'finance_report/finance-report-receiptpayment-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_receipt_payment_data(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            sum_data = fn_get_receipt_payment_sum(app_user_id)
            data['dtl_data'] = dtl_data
            data['sum_data'] = sum_data
            data = {**data, **rep_param, }
            return render(request, self.template_name, data)
        except Exception as e:
            print(str(e))
            return render(request, self.template_name)


class finance_report_assetliabilities(TemplateView):
    template_name = 'finance_report/finance-report-assetliabilities.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        if not fn_is_user_permition_exist(request.session["app_user_id"], 'F10001005', 'Finance'):
            return HttpResponseRedirect(reverse("appauth-home"))

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = CommonReportForm(
            initial={'ason_date': cbd, 'from_date': cbd, 'upto_date': cbd, 'branch_code': branch_code})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)


class finance_report_receiptpayment_two(TemplateView):
    template_name = 'finance_report/finance-report-receiptpayment-two.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        if not fn_is_user_permition_exist(request.session["app_user_id"], 'F10001007', 'Finance'):
            return HttpResponseRedirect(reverse("appauth-home"))

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = CommonReportForm(
            initial={'from_date': cbd, 'upto_date': cbd, 'branch_code': branch_code})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)


class finance_report_receiptpayment_two_print_view(TemplateView):
    template_name = 'finance_report/finance-report-receiptpayment-two-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_receipt_payment_data_two(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            sum_data = fn_get_receipt_payment_sum_two(app_user_id)
            data['dtl_data'] = dtl_data
            data['sum_data'] = sum_data
            data = {**data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            print(str(e))
            return render(request, self.template_name)

class finance_report_assetliabilities_print_view(TemplateView):
    template_name = 'finance_report/finance-report-assetliabilities-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_assetliabilities_details(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            #sum_data = fn_get_assetliabilities_summary(app_user_id)
            data['dtl_data'] = dtl_data
            data = {**data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            print(str(e))
            return render(request, self.template_name)

class finance_report_assetliabilitiestab(TemplateView):
    template_name = 'finance_report/finance-report-assetliabilitiestab.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        if not fn_is_user_permition_exist(request.session["app_user_id"], 'F10001005', 'Finance'):
            return HttpResponseRedirect(reverse("appauth-home"))

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = CommonReportForm(
            initial={'ason_date': cbd, 'from_date': cbd, 'upto_date': cbd, 'branch_code': branch_code})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)

class finance_report_assetliabilitiestab_print_view(TemplateView):
    template_name = 'finance_report/finance-report-assetliabilitiestab-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_assetliabilitiestab_details(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            #sum_data = fn_get_assetliabilities_summary(app_user_id)
            data['dtl_data'] = dtl_data
            data = {**data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            print(str(e))
            return render(request, self.template_name)


class finance_report_incomeexpenses(TemplateView):
    template_name = 'finance_report/finance-report-incomeexpenses.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        if not fn_is_user_permition_exist(request.session["app_user_id"], 'F10001006', 'Finance'):
            return HttpResponseRedirect(reverse("appauth-home"))

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = CommonReportForm(
            initial={'ason_date': cbd, 'from_date': cbd, 'upto_date': cbd, 'branch_code': branch_code})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)


class finance_report_incomeexpenses_print_view(TemplateView):
    template_name = 'finance_report/finance-report-incomeexpenses-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_incomeexpenses_details(app_user_id)
            sum_data = fn_get_incomeexpenses_summary(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data['sum_data'] = sum_data
            data = {**data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            print(str(e))
            return render(request, self.template_name)



class finance_report_incomeexpensestab(TemplateView):
    template_name = 'finance_report/finance-report-incomeexpensestab.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        if not fn_is_user_permition_exist(request.session["app_user_id"], 'F10001006', 'Finance'):
            return HttpResponseRedirect(reverse("appauth-home"))

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = CommonReportForm(
            initial={'ason_date': cbd, 'from_date': cbd, 'upto_date': cbd, 'branch_code': branch_code})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)


class finance_report_incomeexpensestab_print_view(TemplateView):
    template_name = 'finance_report/finance-report-incomeexpensestab-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_incomeexpensestab_details(app_user_id)
            sum_data = fn_get_incomeexpensestab_summary(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data['sum_data'] = sum_data
            data = {**data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            print(str(e))
            return render(request, self.template_name)


class finance_report_profitloss(TemplateView):
    template_name = 'finance_report/finance-report-profitloss.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        if not fn_is_user_permition_exist(request.session["app_user_id"], 'F10001007', 'Finance'):
            return HttpResponseRedirect(reverse("appauth-home"))

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = CommonReportForm(
            initial={'from_date': cbd, 'upto_date': cbd, 'branch_code': branch_code})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)


class finance_report_profitloss_print_view(TemplateView):
    template_name = 'finance_report/finance-report-profitloss-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_profitloss_details(app_user_id)
            sum_data = fn_get_profitloss_summary(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data['sum_data'] = sum_data
            data = {**data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            print(str(e))
            return render(request, self.template_name)

class finance_report_trialbalance(TemplateView):
    template_name = 'finance_report/finance-report-trialbalance.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        if not fn_is_user_permition_exist(request.session["app_user_id"], 'F10001007', 'Finance'):
            return HttpResponseRedirect(reverse("appauth-home"))

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = CommonReportForm(
            initial={'from_date': cbd, 'upto_date': cbd, 'branch_code': branch_code})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)


class finance_report_trialbalance_print_view(TemplateView):
    template_name = 'finance_report/finance-report-trialbalance-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_trialbalance_details(app_user_id)
            #sum_data = fn_get_trialbalance_summary(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data = {**data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            print(str(e))
            return render(request, self.template_name)

class finance_report_trialbalancetab(TemplateView):
    template_name = 'finance_report/finance-report-trialbalancetab.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        if not fn_is_user_permition_exist(request.session["app_user_id"], 'F10001007', 'Finance'):
            return HttpResponseRedirect(reverse("appauth-home"))

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = CommonReportForm(
            initial={'from_date': cbd, 'upto_date': cbd, 'branch_code': branch_code})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)

class finance_report_trialbalancetab_print_view(TemplateView):
    template_name = 'finance_report/finance-report-trialbalancetab-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_trialbalancetab_details(app_user_id)
            #sum_data = fn_get_trialbalance_summary(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data = {**data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            print(str(e))
            return render(request, self.template_name)


class finance_report_cashnbank(TemplateView):
    template_name = 'finance_report/finance-report-cashnbank.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        if not fn_is_user_permition_exist(request.session["app_user_id"], 'F10001008', 'Finance'):
            return HttpResponseRedirect(reverse("appauth-home"))

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = CommonReportForm(
            initial={'from_date': cbd, 'upto_date': cbd, 'branch_code': branch_code})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)


class finance_report_cashnbank_print_view(TemplateView):
    template_name = 'finance_report/finance-report-cashnbank-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_cashnbank_details(app_user_id)
            sum_data = fn_get_cashnbank_summary(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data = {**data, **sum_data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            print(str(e))
            return render(request, self.template_name)

class finance_report_coa_print_view(TemplateView):
    template_name = 'finance_report/finance-report-coa-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_coa_details(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data = {**data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            print(str(e))
            return render(request, self.template_name)
