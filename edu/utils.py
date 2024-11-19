
from operator import length_hint
from finance.utils import fn_cancel_tran_batch
from edu.models import *
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

def NumberGen(branch_code=None, abr=None, year=None, month=None, day=None, name='genarel'):
    where = dict()

    if branch_code:
        where['branch_code'] = branch_code

    if abr:
        where['abr'] = abr

    if year:
        where['year'] = year[len(str(year))-2:]

    if month:
        where['month'] = month

    if day:
        where['day'] = day
    if name:
        where['name'] = name

    if Number_Gen.objects.filter(**where).exists():
        counter = Number_Gen.objects.filter(**where).get()
        counter.number = counter.number+1
        counter.save()
        number = counter
    else:
        post = Number_Gen()
        post.year = year
        post.month = month
        post.day = day
        post.abr = abr
        post.number = 1
        post.branch_code = branch_code
        post.name = name
        post.save()
        number = post

    return number


def fn_number_to_str_with_len(digit, number):
    number_len = len(str(number))
    zero_str = ''
    for i in range(digit-number_len):
        zero_str = str(zero_str)+str(0)
    return zero_str+str(number)


def fn_gen_student_id(year, branch_code, class_id):
    br = str(branch_code)
    number = NumberGen(br[len(br)-2:], class_id[len(class_id)-2:],
                       year[len(str(year))-2:], None, None, 'Student_ID')
    return number.year+number.branch_code+number.abr+fn_number_to_str_with_len(4, number.number)


def get_inv_number(p_inv_code, p_branch_code, p_inv_prefix, p_inv_naration, p_length):
    cursor = connection.cursor()
    cursor.callproc("fn_get_inventory_number", [
                    p_inv_code, p_branch_code, p_inv_prefix, p_inv_naration, p_length])
    inv_number = cursor.fetchone()
    return inv_number


def fn_get_class_id():
    branch_code = 1
    inventory_number = get_inv_number(
        2100, branch_code, '', 'Class ID Generate', 6)
    return inventory_number[0]


def fn_get_class_group_id():
    branch_code = 1
    inventory_number = get_inv_number(
        2200, branch_code, '', 'Class Group ID Generate', 6)
    return inventory_number[0]


def fn_get_section_id():
    branch_code = 1
    inventory_number = get_inv_number(
        2300, branch_code, '', 'Section ID Generate', 6)
    return inventory_number[0]


def fn_get_subject_type_id():
    branch_code = 1
    inventory_number = get_inv_number(
        2400, branch_code, '', 'Subject Type ID Generate', 6)
    return inventory_number[0]


def fn_get_subject_id():
    branch_code = 1
    inventory_number = get_inv_number(
        2500, branch_code, '', 'Subject ID Generate', 6)
    return inventory_number[0]


def fn_get_department_id():
    branch_code = 1
    inventory_number = get_inv_number(
        2600, branch_code, '', 'Department ID Generate', 6)
    return inventory_number[0]


def fn_get_shift_id():
    branch_code = 1
    inventory_number = get_inv_number(
        2700, branch_code, '', 'Shift ID Generate', 6)
    return inventory_number[0]


def fn_get_degree_id():
    branch_code = 1
    inventory_number = get_inv_number(
        2800, branch_code, '', 'Degree ID Generate', 6)
    return inventory_number[0]


def fn_get_occupation_id():
    branch_code = 1
    inventory_number = get_inv_number(
        2900, branch_code, '', 'Occupation ID Generate', 6)
    return inventory_number[0]


def fn_get_institute_id():
    branch_code = 1
    inventory_number = get_inv_number(
        21100, branch_code, '', 'Institute ID Generate', 6)
    return inventory_number[0]


def fn_get_student_id(year, branch_code, class_id):
    br = str(branch_code)
    prefix = year[len(year)-2:]+br[len(br)-2:]+class_id[len(class_id)-2:]
    inventory_number = get_inv_number(
        21200, branch_code, prefix, 'Student Roll Generate', 4)
    print(inventory_number[0])
    return inventory_number[0]


def fn_get_result_id():
    branch_code = 1
    inventory_number = get_inv_number(
        21300, branch_code, '', 'Result ID Generate', 6)
    return inventory_number[0]


def fn_get_examtype_id():
    branch_code = 1
    inventory_number = get_inv_number(
        21400, branch_code, 'et', 'Examtype ID Generate', 6)
    return inventory_number[0]


def fn_get_examsetup_id():
    branch_code = 1
    inventory_number = get_inv_number(
        21500, branch_code, 'es', 'Examtype ID Generate', 6)
    return inventory_number[0]


def fn_get_examname(exam_id):
    exam_name = Exam_Setup.objects.get(exam_id=exam_id)
    return exam_name.exam_name


def fn_student_rolls(students):
    student_rolls = []
    for student in students:
        student_rolls.append(student.student_roll.student_roll)
    return student_rolls


def fn_get_online_exam_id():
    branch_code = 1
    inventory_number = get_inv_number(
        21600, branch_code, 'OEX', 'Online Exam ID Generate', 6)
    return inventory_number[0]


def fn_get_online_que_dtl_id():
    branch_code = 1
    inventory_number = get_inv_number(
        21700, branch_code, 'EQD', 'Question ID Generate', 10)
    return inventory_number[0]


def fn_get_online_que_id():
    branch_code = 1
    inventory_number = get_inv_number(
        21800, branch_code, 'QUE', 'Question ID Generate', 6)
    return inventory_number[0]


def fn_get_online_exam_ans_info_id():
    branch_code = 1
    inventory_number = get_inv_number(
        21900, branch_code, 'ANS', 'Answer ID Generate', 6)
    return inventory_number[0]

def fn_get_online_exam_answer_id():
    branch_code = 1
    inventory_number = get_inv_number(
        22100, branch_code, 'QS', 'Question Answer ID Generate', 6)
    return inventory_number[0]

def fn_get_fees_mapping_id():
    branch_code = 1
    inventory_number = get_inv_number(
        22301, branch_code, 'FM', 'Fees Mapping ID', 6)
    return inventory_number[0]

def fn_get_fees_processing_id(p_branch_code):
    inventory_number = get_inv_number(
        5001, 1, '', 'Fees Processing ID', 8)
    return inventory_number[0]
def fn_result_view_id():
    inventory_number = get_inv_number(
        5002, 1, 'rv', 'Result View ID', 8)
    return inventory_number[0]

def fn_result_process_id():
    inventory_number = get_inv_number(
        5003, 1, 'rp', 'Result View ID', 12)
    return inventory_number[0]

def get_student_subject_mark(p_academic_year_id, p_term_id, p_class_id, p_student_roll, p_subject_id, p_out_of, p_app_user_id):
    cursor = connection.cursor()
    cursor.callproc("fn_get_student_subject_mark", [
                    p_academic_year_id, p_term_id, p_class_id, p_student_roll, p_subject_id, p_out_of, p_app_user_id])
    result = cursor.fetchone()
    return result


def fn_result_subjectwise(p_academic_year_id, p_term_id, p_class_id, p_class_group_id, p_app_user_id):
    cursor = connection.cursor()
    cursor.callproc("fn_view_class_subject_mark", [
                    p_academic_year_id, p_term_id, p_class_id, p_class_group_id, p_app_user_id])
    result_subjectwise = cursor.fetchone()
    return result_subjectwise


def fn_result_subjectwise_withoutgrp(p_academic_year_id, p_term_id, p_class_id, p_app_user_id):
    cursor = connection.cursor()
    cursor.callproc("fn_view_class_subject_mark", [
                    p_academic_year_id, p_term_id, p_class_id, p_app_user_id])
    result_subjectwise = cursor.fetchone()
    return result_subjectwise


def get_result_great(p_obtain_mark, p_total_mark, p_out_of):
    cursor = connection.cursor()
    cursor.callproc("fn_get_result_gpa", [
                    p_obtain_mark, p_total_mark, p_out_of])
    result = cursor.fetchone()
    return result

def fn_get_grade_nameby_point(p_gpa, p_out_of):
    cursor = connection.cursor()
    cursor.callproc("fn_get_grade_nameby_point", [
                    p_gpa, p_out_of])
    result = cursor.fetchone()
    return result

def get_final_result_great(p_academic_year, p_term_id, p_class_id,p_student_roll,p_app_user_id):
    cursor = connection.cursor()
    cursor.callproc("fn_get_final_result_gpa", [
                    p_academic_year, p_term_id, p_class_id,p_student_roll,p_app_user_id])
    result = cursor.fetchone()
    return result


def fn_get_present_sheet_info_id():
    branch_code = 1
    inventory_number = get_inv_number(
        22200, branch_code, '', 'Present Sheet ID Generate', 6)
    return inventory_number[0]


def off_future_date(p_date):
    current_date = timezone.now().date()
    if (type(p_date) == "str"):
        get_date = datetime.datetime.strptime(p_date, "%Y-%m-%d").date()
    else:
        get_date = p_date
    if current_date < get_date:
        data = True
    else:
        data = False
    return data


def fn_get_rack_id():
    branch_code = 1
    inventory_number = get_inv_number(
        22300, branch_code, '', 'Rack ID Generate', 6)
    return inventory_number[0]


def fn_get_author_id():
    branch_code = 1
    inventory_number = get_inv_number(
        22400, branch_code, '', 'Author ID Generate', 6)
    return inventory_number[0]


def fn_get_editor_id():
    branch_code = 1
    inventory_number = get_inv_number(
        22500, branch_code, 'E', 'Editor ID Generate', 6)
    return inventory_number[0]


def fn_get_book_id():
    branch_code = 1
    inventory_number = get_inv_number(
        22600, branch_code, 'B', 'Book ID Generate', 6)
    return inventory_number[0]


def fn_get_card_id():
    branch_code = 1
    inventory_number = get_inv_number(
        22700, branch_code, 'C', 'Card ID Generate', 6)
    return inventory_number[0]


def fn_get_bissue_id():
    branch_code = 1
    inventory_number = get_inv_number(
        22800, branch_code, 'I', 'Book Issue ID Generate', 6)
    return inventory_number[0]


def fn_get_request_id():
    branch_code = 1
    inventory_number = get_inv_number(
        22900, branch_code, 'R', 'Book Request ID Generate', 6)
    return inventory_number[0]


def fn_get_room_id():
    branch_code = 1
    inventory_number = get_inv_number(
        23100, branch_code, 'RM', 'Room ID Generate', 6)
    return inventory_number[0]


def fn_get_routine_id():
    branch_code = 1
    inventory_number = get_inv_number(
        23200, branch_code, 'RU', 'Class Routine ID Generate', 6)
    return inventory_number[0]


def fn_get_routine_dtl_id():
    branch_code = 1
    inventory_number = get_inv_number(
        23300, branch_code, 'RD', 'Class Routine Details ID Generate', 6)
    return inventory_number[0]


def fn_get_teacher_id():
    branch_code = 1
    inventory_number = get_inv_number(
        23400, branch_code, 'T', 'Teacher ID Generate', 6)
    return inventory_number[0]


def fn_get_category_id():
    branch_code = 1
    inventory_number = get_inv_number(
        23500, branch_code, 'CA', 'Category ID Generate', 6)
    return inventory_number[0]


def fn_get_session_id():
    branch_code = 1
    inventory_number = get_inv_number(
        23600, branch_code, 'SA', 'Session ID Generate', 6)
    return inventory_number[0]


def fn_get_subcategory_id():
    branch_code = 1
    inventory_number = get_inv_number(
        23700, branch_code, 'SC', 'Subject Category ID Generate', 6)
    return inventory_number[0]


def fn_get_tc_id():
    branch_code = 1
    inventory_number = get_inv_number(
        23800, branch_code, 'TC', 'TC ID Generate', 6)
    return inventory_number[0]


def fn_get_exam_atten_id():
    branch_code = 1
    inventory_number = get_inv_number(
        23900, branch_code, 'EA', 'Exam Attendance ID Generate', 6)
    return inventory_number[0]


def fn_get_fees_head_code():
    branch_code = 1
    inventory_number = get_inv_number(
        24000, branch_code, 'FH', 'Fees Head Code Generate', 6)
    return inventory_number[0]


def fn_get_fees_waiver_code():
    branch_code = 1
    inventory_number = get_inv_number(
        24100, branch_code, 'FW', 'Fees Waiver Code Generate', 6)
    return inventory_number[0]


def fn_get_id_card_no():
    branch_code = 1
    inventory_number = get_inv_number(
        24200, branch_code, 'ID', 'ID No Generate', 6)
    return inventory_number[0]


def fn_search_student_fees(p_student_roll, p_collection_date, p_app_user_id):
    error_message = None
    status = False
    cursor = connection.cursor()
    cursor.callproc("fn_edu_fees_tempdata", [
                    p_student_roll, p_collection_date, p_app_user_id])
    row = cursor.fetchone()
    if row[0] != 'S':
        error_message = row[1]
        status = False
        return status, error_message
    status = True
    return status, error_message


def fn_edu_fees_submit(branch_code,p_student_roll, p_collection_date, p_app_user_id):
    error_message = None
    status = False
    cursor = connection.cursor()
    cursor.callproc("fn_edu_fees_submit", [
                    p_student_roll, p_collection_date, p_app_user_id])
    row = cursor.fetchone()
    if row[0] != 'S':
        error_message = row[1]
        status = False
        return status, error_message, None
    status = True
    return status, error_message, row[2]


def fn_edu_fees_cancel(p_id, p_app_user_id):
    error_message = None
    status = False
    try:
        fees_sum = Fees_Receive_Summary.objects.get(id=p_id)
        if fees_sum.cancel_by:
            error_message = "Transaction Already Canceled!"
            status = False
            return status, error_message

        status, error_message = fn_cancel_tran_batch(p_branch_code=fees_sum.branch_code, p_app_user_id=p_app_user_id,
                                                     p_transaction_date=fees_sum.receive_date, p_batch_number=fees_sum.tran_batch_number,
                                                     p_cancel_comments='Cancel by '+p_app_user_id)

        if not status:
            error_message = "Error in Batch Cancel! "+error_message
            status = False
            return status, error_message
        else:
            Fees_Receive_Student.objects.filter(
                transaction_id=fees_sum.transaction_id).update(cancel_by=p_app_user_id, cancel_on=timezone.now())
            fees_sum.cancel_by = p_app_user_id
            fees_sum.cancel_on = timezone.now()
            fees_sum.save()
        status = True
        return status, error_message
    except Fees_Receive_Summary.DoesNotExist:
        error_message = "Invalid Receive Info!"
        status = False
        return status, error_message
    except Exception as e:
        error_message = str(e)
        status = False
        return status, error_message


def fn_get_absent_fine_hist_count(p_head_code, p_effective_date):
    row = Absent_Fine_History.objects.filter(
        effective_date=p_effective_date, head_code=p_head_code).aggregate(Count('head_code'))
    return row['head_code__count']+1


def fn_get_fees_mapping_hist_count(data_hist):
    row = Fees_Mapping_History.objects.filter(fees_mapping_id=data_hist["fees_mapping_id"],
    effective_date=data_hist["effective_date"]).aggregate(Count('head_code'))
    return row['head_code__count']+1


def fn_get_feeswaive_mapping_hist_count(data_hist):
    row = Fees_Waiver_Mapping_Hist.objects.filter(head_code=data_hist["head_code"], catagory_id=data_hist["catagory_id"],
    class_id=data_hist["class_id"], class_group_id=data_hist["class_group_id"], section_id=data_hist["section_id"],
    effective_date=data_hist["effective_date"]).aggregate(Count('head_code'))
    return row['head_code__count']+1


def fn_get_admit_card_no():
    branch_code = 1
    inventory_number = get_inv_number(
        24300, branch_code, 'Ad', 'Admit Card No Generate', 6)
    return inventory_number[0]

def fn_get_testmonial_number(branch_code,year):
    br = str(branch_code)
    number = NumberGen(br[len(br)-2:], 'T', year[len(str(year))-2:], None, None, name='Testimonial')
    return number.abr+number.branch_code+number.year+fn_number_to_str_with_len(4, number.number)

def fn_start_fees_processing(p_process_id, p_branch_code, p_academic_year,p_class_id,p_class_group_id,p_section_id,p_process_date,p_student_roll,p_app_user_id):
    try:
        with transaction.atomic():
            print('Process Started')
            cursor = connection.cursor()
            cursor.callproc(
                'fn_edu_fees_generate', [p_branch_code, p_academic_year,p_class_id,p_class_group_id,p_section_id,p_process_date,p_student_roll,  p_app_user_id])
            row = cursor.fetchone()

            if row[0] != 'S':
                logger.error("Error in fn_edu_fees_generate {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(row[1]).__name__, str(row[1])))
                Fees_Processing_Details.objects.filter(process_id=p_process_id).update(process_error=row[1], process_status=True)
                print('Process Error')
            else:
                Fees_Processing_Details.objects.filter(process_id=p_process_id).update(process_status=True)
                print('Process Completed')

    except Exception as e:
        print(str(e))
        logger.error("Error in Day Closing {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))

def fn_fees_processing_thread(data):
    error_message = None
    try:
        t1 = threading.Thread(target=fn_start_fees_processing,
                              args=(data["process_id"], data["branch_code"], data["academic_year"],data["class_id"],data["class_group_id"],data["section_id"],data["process_date"],data["student_roll"],data["app_user_id"]))
        t1.start()
        return True, error_message
    except Exception as e:
        error_message = str(e)
        return False, error_message


def gn_edu_get_student_branch(p_student_roll):
    branch_code = None
    try:
        stud = Students_Info.objects.get(student_roll=p_student_roll)
        return stud.branch_code
    except Students_Info.DoesNotExist:
        return branch_code


def fn_edu_fees_others_receive(p_student_roll,p_collection_date, p_head_code,p_receive_amount, p_app_user_id):
    error_message = None
    status = False
    cursor = connection.cursor()
    cursor.callproc("fn_edu_fees_others_receive", [
                    p_student_roll, p_collection_date, p_head_code,p_receive_amount, p_app_user_id])
    row = cursor.fetchone()
    if row[0] != 'S':
        error_message = row[1]
        status = False
        return status, error_message, None
    status = True
    return status, error_message, row[2]