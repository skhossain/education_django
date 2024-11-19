
from finance.utils import fn_get_cash_gl_code, fn_transfer_tran_posting, fn_cancel_tran_batch
from hostel.models import Application_Settings as Hostel_Application_Settings
from hostel.models import Fees_Processing_Details as Hostel_Fees_Processing_Details
from hostel.models import *
from appauth.models import Inventory_Number
from django.db import connection, transaction
from django.db.models import Count, Sum, Avg, Max, Min
import datetime
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from decimal import Decimal
import logging
import sys
from django.utils import timezone
from edu.validations import *
logger = logging.getLogger(__name__)
import threading

def get_inv_number(p_inv_code, p_branch_code, p_inv_prefix, p_inv_naration, p_length):
    cursor = connection.cursor()
    cursor.callproc("fn_get_inventory_number", [
                    p_inv_code, p_branch_code, p_inv_prefix, p_inv_naration, p_length])
    inv_number = cursor.fetchone()
    return inv_number

def fn_get_bedtype_id():
    branch_code = 1
    inventory_number = get_inv_number(
        1000, branch_code, 'BT', 'Bed Type Id Generate', 6)
    return inventory_number[0]


def fn_get_roomtype_id():
    branch_code = 1
    inventory_number = get_inv_number(
        2000, branch_code, 'RT', 'Room Type ID Generate', 6)
    return inventory_number[0]


def fn_get_payfor_type_id():
    branch_code = 1
    inventory_number = get_inv_number(
        3000, branch_code, 'PFT', 'PayFor Type ID Generate', 6)
    return inventory_number[0]


def fn_get_bedmanage_id():
    branch_code = 1
    inventory_number = get_inv_number(
        4000, branch_code, 'BM', 'Bed Management Id Generate', 6)
    return inventory_number[0]


def fn_get_roommanage_id():
    branch_code = 1
    inventory_number = get_inv_number(
        5000, branch_code, 'RM', 'Room Management Id Generate', 6)
    return inventory_number[0]


def fn_get_paymanage_id():
    branch_code = 1
    inventory_number = get_inv_number(
        6000, branch_code, 'PM', 'Payment Management Id Generate', 6)
    return inventory_number[0]


def fn_get_admit_id():
    branch_code = 1
    inventory_number = get_inv_number(
        7000, branch_code, 'HA', 'Hostel Admition Id Generate', 6)
    return inventory_number[0]


def fn_get_mealtype_id():
    branch_code = 1
    inventory_number = get_inv_number(
        8000, branch_code, 'MT', 'Hostel Meal Type Id Generate', 6)
    return inventory_number[0]


def fn_get_meal_id():
    branch_code = 1
    inventory_number = get_inv_number(
        9000, branch_code, 'M', 'Hostel Meal Id Generate', 6)
    return inventory_number[0]

def fn_get_hall_code():
    branch_code = 1
    inventory_number = get_inv_number(
        10000, branch_code, 'HF', 'Hall Head Code', 6)
    return inventory_number[0]

def fn_get_fees_processing_id(p_branch_code):
    inventory_number = get_inv_number(
        10001, 1, '', 'Fees Processing ID', 8)
    return inventory_number[0]

def gn_hostel_get_admission_gl():
    hostel_admission_fee_gl = None
    try:
        app_settings = Hostel_Application_Settings.objects.get()
        return app_settings.hostel_admission_fee_gl
    except Hostel_Application_Settings.DoesNotExist:
        return hostel_admission_fee_gl


def fn_hostel_admission_cancel(p_id, p_app_user_id):
    error_message = None
    status = False
    emi_tran = False
    try:
        hostel_info = Hostel_Admit.objects.get(admit_id=p_id)
        transaction_date = hostel_info.admit_date
        tran_batch_number = hostel_info.tran_batch_number
        branch_code = hostel_info.branch_code
        hostel_info.cancel_by = p_app_user_id
        hostel_info.cancel_on = timezone.now()

        if tran_batch_number>0:
            status, error_message = fn_cancel_tran_batch(p_branch_code=branch_code, p_app_user_id=p_app_user_id,
                                                        p_transaction_date=transaction_date, p_batch_number=tran_batch_number, p_cancel_comments='Cancel by '+p_app_user_id)

            if status:
                hostel_info.save()
            else:
                error_message = error_message
                status = False
                return status, error_message
        else:
            hostel_info.save()

        status = True
        return status, error_message
    except Hostel_Admit.DoesNotExist:
        error_message = "Invalid Hostel Registration!"
        status = False
        return status, error_message
    except Exception as e:
        error_message = str(e)
        status = False
        return status, error_message

def fn_get_hostel_fees_mapping_hist_count(data_hist):
    row = Hostel_Fees_Mapping_Hist.objects.filter(head_code=data_hist["head_code"],
    hall_code=data_hist["hall_code"],
    effective_date=data_hist["effective_date"]).aggregate(Count('head_code'))
    return row['head_code__count']+1


def fn_start_hostel_fees_processing(p_process_id, p_branch_code, p_academic_year,p_process_date,p_student_roll,p_app_user_id):
    try:
        with transaction.atomic():
            cursor = connection.cursor()
            cursor.callproc(
                'fn_hostel_fees_generate', [p_branch_code, p_academic_year,p_process_date,p_student_roll,  p_app_user_id])
            row = cursor.fetchone()
            print(row)

            if row[0] != 'S':
                logger.error("Error in fn_hostel_fees_generate {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(row[1]).__name__, str(row[1])))
                Hostel_Fees_Processing_Details.objects.filter(process_id=p_process_id).update(process_error=row[1], process_status=True)
            else:
                Hostel_Fees_Processing_Details.objects.filter(process_id=p_process_id).update(process_status=True)

    except Exception as e:
        print(str(e))
        logger.error("Error in Day Closing {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))

def fn_hostel_fees_processing_thread(data):
    error_message = None
    try:
        t1 = threading.Thread(target=fn_start_hostel_fees_processing,
                              args=(data["process_id"], data["branch_code"], data["academic_year"],data["process_date"],data["student_roll"],data["app_user_id"]))
        t1.start()
        return True, error_message
    except Exception as e:
        error_message = str(e)
        return False, error_message
