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

from edu.models import *

def get_inv_number(p_inv_code, p_branch_code, p_inv_prefix, p_inv_naration, p_length):
    cursor = connection.cursor()
    cursor.callproc("fn_get_inventory_number", [
                    p_inv_code, p_branch_code, p_inv_prefix, p_inv_naration, p_length])
    inv_number = cursor.fetchone()
    return inv_number

def fn_get_transportation_type():
    branch_code = 100
    inventory_number = get_inv_number(
        200, branch_code, '', 'Transportation Type Id Generate', 6)
    return inventory_number[0]

def fn_get_transportation():
    branch_code = 100
    inventory_number = get_inv_number(
        300, branch_code, '', 'Transportation Id Generate', 6)
    return inventory_number[0]

def fn_get_locationid():
    branch_code = 100
    inventory_number = get_inv_number(
        400, branch_code, '', 'Location Id Generate', 6)
    return inventory_number[0]

def fn_get_vehicleid():
    branch_code = 100
    inventory_number = get_inv_number(
        500, branch_code, '', 'Vehicle Id Generate', 6)
    return inventory_number[0]

def fn_get_driverid():
    branch_code = 1
    inventory_number = get_inv_number(
        600, branch_code, '', 'Driver Id Generate', 6)
    return inventory_number[0]

def fn_get_conductorid():
    branch_code = 100
    inventory_number = get_inv_number(
        700, branch_code, '', 'Conductor Id Generate', 6)
    return inventory_number[0]
    
def fn_get_roadmapid():
    branch_code = 100
    inventory_number = get_inv_number(
        800, branch_code, '', 'Roadmap Id Generate', 6)
    return inventory_number[0]

def fn_get_admittransportationid():
    branch_code = 100
    inventory_number = get_inv_number(
        900, branch_code, '', 'Roadmap Id Generate', 6)
    return inventory_number[0]
    
def fn_get_payforid():
    branch_code = 100
    inventory_number = get_inv_number(
        1000, branch_code, '', ' Id Generate', 6)
    return inventory_number[0]

def fn_get_paymentid():
    branch_code = 100
    inventory_number = get_inv_number(
        1100, branch_code, '', ' Id Generate', 6)
    return inventory_number[0]
    
def fn_get_vehitypeid():
    branch_code = 100
    inventory_number = get_inv_number(
        1100, branch_code, '', ' Id Generate', 6)
    return inventory_number[0]