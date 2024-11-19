from appauth.utils import get_inv_number
from appauth.models import *
from django.db import connection, transaction
from django.db.models import Count, Sum, Avg, Max, Min
import datetime
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from decimal import Decimal
import logging
import sys
from django.utils import timezone
from appauth.validations import *
logger = logging.getLogger(__name__)


def fn_get_departmnet_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'Department ID Generate', 6)
    return inventory_number[0]


def fn_get_designation_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'designation ID Generate', 6)
    return inventory_number[0]


def fn_get_company_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'company ID Generate', 6)
    return inventory_number[0]


def fn_get_office_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'office ID Generate', 6)
    return inventory_number[0]


def fn_get_shift_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'shift ID Generate', 6)
    return inventory_number[0]


def fn_get_degree_id():
    branch_code = 1
    inventory_number = get_inv_number(
        3300, branch_code, 'DPI', 'Department ID Generate', 6)
    return inventory_number[0]


def fn_get_employee_type_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'employee type ID Generate', 6)
    return inventory_number[0]


def fn_get_salscale_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'salary scale ID Generate', 6)
    return inventory_number[0]


def fn_get_salsdtlcale_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'salary scale detail ID Generate', 6)
    return inventory_number[0]


def fn_get_salsbonus_id(branch_code=100):
    inventory_number = get_inv_number(
        100, branch_code, '', 'salary scale detail bonous ID Generate', 6)
    return inventory_number[0]


def fn_get_alownce_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'alownce ID Generate', 6)
    return inventory_number[0]


def fn_get_bank_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'Department ID Generate', 6)
    return inventory_number[0]


def fn_get_employee_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'employee ID Generate', 6)
    return inventory_number[0]


def fn_serial_no_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'employee Serial No', 6)
    return inventory_number[0]


def fn_get_document_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'document ID Generate', 6)
    return inventory_number[0]


def fn_get_leave_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'leave ID Generate', 6)
    return inventory_number[0]


def fn_get_bill_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'Bill ID Generate', 6)
    return inventory_number[0]


def fn_get_teacher_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, 'T', 'Teacher ID Generate', 2)
    return inventory_number[0]
