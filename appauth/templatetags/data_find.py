# from appauth.views import fn_get_dashboad_data
from decimal import Context
from appauth.utils import get_inv_number, get_business_date, fn_get_query_result
import datetime
from django import template
from django.contrib.auth.models import Group
from . .models import *
from appauth.utils import *
register = template.Library()


def week_number_of_month(date_value):
    return (date_value.isocalendar()[1] - date_value.replace(day=1).isocalendar()[1] + 1)


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return group in user.groups.all()


@register.simple_tag
def week_number():
    today = datetime.date.today()
    start = today - datetime.timedelta(days=today.weekday())
    end = start + datetime.timedelta(days=6)
    start_date = str(start).split()
    end_date = str(end).split()
    return start_date, end_date


@register.simple_tag
def yesterday():
    yesterday = datetime.datetime.strftime(
        datetime.datetime.now() - datetime.timedelta(1), '%Y-%m-%d')
    return yesterday


# @register.inclusion_tag('appauth/appauth-latest-profit-product.html')
# def top_profit_product():
#    product = []
#    return {'product': product}


# @register.inclusion_tag('appauth/appauth-latest-profit-product.html')
# def low_profit_product():
#    product = []
#    return {'product': product}


# @register.inclusion_tag('appauth/appauth-top-due-supplier.html')
# def top_due_supplier():
#     # branch_code = fn_get_dashboad_data()["branch_code"]
#     # total_supplier_payable = fn_get_dashboad_data()['total_supplier_payable']
#     data = []
#     return {'data': data}


# @register.inclusion_tag('appauth/appauth-top-due-supplier.html')
# def top_due_customer():
#     # branch_code = fn_get_dashboad_data()["branch_code"]
#     # total_customer_due = fn_get_dashboad_data()['total_customer_due']
#     data = []
#     return {'data': data}
