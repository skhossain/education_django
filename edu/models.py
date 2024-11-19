from email.policy import default
from operator import mod
import wave
from django.db import models
from django.db.models.fields import IntegerField
from jsonfield import JSONField
from appauth.models import Loc_Country, Loc_Division, Loc_District, Loc_Upazila, Branch, STATUS_LIST
from tinymce.models import HTMLField
from datetime import date, datetime
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from hrm.models import *
# Create your models here.

from appauth.models import  BLOOD_GROUP, GENDER_LIST, RELIGION_LIST, MARITAL_STATUS
STATUS_LIST = (
    ('A', 'Active'),
    ('I', 'Inactive')
)

FEE_PAY_LIST = (
    ('1', 'Admission'),
    ('2', 'Monthly Tution'),
    ('3', 'Mid-Term Fee'),
    ('4', 'Semester Begining'),
    ('5', 'Semester Closing'),
    ('6', 'Absent Fees'),
)


def no_future(value):
    today = date.today()
    if value > today:
        raise ValidationError('date is in the future')


Condition_List = (
    ('Max', 'Maximum'),
    ('Min', 'Minimum'),
    ('Avg', 'Average')
)
Question_patten_List = (
    ('R', 'Random Display'),
    ('A', 'Ascending Display'),
    ('D', 'Descending Display')
)
Exam_Status_List = (
    ('Live', 'Live'),
    ('Locked', 'Locked'),
    ('Cancel', 'Cancel'),
    ('Finish', 'Finish'),
    ('Submitted', 'Submitted'),
    ('Holed', 'Holed')
)
Question_Type_List = (
    ('', '----------'),
    ('Short', 'Single Line Text'),
    ('Creative', 'Multiline Text'),
    ('MCQ', 'MCQ Single Answer'),
    ('MCQS', 'MCQ Multiple Answer')
)

Status_Type_list = (
    ('R', 'Regular'),
    ('IR', 'Irregular'),
)
Week_List = (
    (1, 'Saturday'),
    (2, 'Sunday'),
    (3, 'Monday'),
    (4, 'Tuesday'),
    (5, 'Wednesday'),
    (6, 'Thursday'),
    (7, 'Friday')
)

HISTORY_STATUS = (
    ('A', 'Active'),
    ('I', 'Inactive'),
    ('R', 'Renew'),
    ('U', 'Use'),
)

PUBLISH_STATUS = (
    ('A', 'Active'),
    ('I', 'Inactive'),
)
Process_Status=(
    ('Start', 'Start'),
    ('Processing', 'Processing'),
    ('Cancel', 'Cancel'),
    ('Finish', 'Finish'),
    ('Fail', 'Fail'),
    ('Success', 'Success'),
)

def get_week_number(name):
    for i in range(0, 7):
        w = Week_List[i]
        if name in w:
            return w[0]

Month_List = (
    (1, 'January'),
    (2, 'February'),
    (3, 'March'),
    (4, 'April'),
    (5, 'May'),
    (6, 'June'),
    (7, 'July'),
    (8, 'August'),
    (9, 'September'),
    (10, 'October'),
    (11, 'November'),
    (12, 'December'),
)

FEE_PAY_FRQ_LIST = (
    ('', 'Choose...'),
    ('D', 'Daily'),
    ('W', 'Weekly'),
    ('M', 'Monthly'),
    ('Q', 'Quarterly'),
    ('H', 'Half Yearly'),
    ('Y', 'Yearly'),
)

Exam_type_status = ((1, 'Offline'), (2, 'Online'), (3, 'Both'))
grading_system = ((4, 'Out of 4'), (5, 'Out of 5'))

class Number_Gen(models.Model):
    branch_code = models.CharField(max_length=10, null=True, blank=True)
    abr = models.CharField(max_length=10, null=True, blank=True)
    year = models.CharField(max_length=4, null=True, blank=True)
    month = models.CharField(max_length=4, null=True, blank=True)
    day = models.CharField(max_length=4, null=True, blank=True)
    number = models.IntegerField(default=1)
    name = models.CharField(max_length=50, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Application_Settings(models.Model):
    academic_code = models.CharField(max_length=10, null=False)
    academic_name = models.CharField(max_length=300, null=False)
    academic_address = models.CharField(max_length=300, null=True, blank=True)
    academic_mobile_1 = models.CharField(max_length=50, null=True, blank=True)
    academic_mobile_2 = models.CharField(max_length=50, null=True, blank=True)
    academic_email = models.CharField(max_length=100, null=True, blank=True)
    academic_website = models.CharField(max_length=100, null=True, blank=True)
    academic_logo = models.ImageField(upload_to="logo/", null=True, blank=True)
    web_header_banner=models.ImageField(upload_to="banner/", null=True, blank=True)
    eiin_number = models.CharField(max_length=30, unique=True)
    reset_student_id=models.IntegerField(default=0)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.academic_name)

class Academic_Year(models.Model):
    academic_year = models.BigIntegerField(primary_key=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-academic_year']

    def __str__(self):
        return str(self.academic_year)


class Academic_Class(models.Model):
    class_id = models.CharField(max_length=20, blank=True, primary_key=True)
    class_name = models.CharField(max_length=200, unique=True)
    short_name = models.CharField(
        max_length=200, blank=True, null=True, unique=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    roll_serial = models.CharField(max_length=20, blank=True, null=True)
    class_serial = models.IntegerField(blank=True, null=True)
    out_of = models.IntegerField(
        blank=True, null=True, choices=grading_system, default=5)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['class_serial']

    def __str__(self):
        return self.class_name


class Academic_Class_Group(models.Model):
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE,
                                 null=True, blank=True, db_column='class_id', related_name='cgp_class_id')
    class_group_id = models.CharField(
        max_length=20, blank=True, primary_key=True)
    class_group_name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True, null=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.class_group_name


class Class_Room(models.Model):
    room_id = models.CharField(max_length=50, primary_key=True)
    nama_or_number = models.CharField(max_length=50, null=False, blank=False)
    room_size = models.CharField(max_length=50, blank=True, null=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama_or_number


class Section_Info(models.Model):
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE,
                                 null=True, blank=True, db_column='class_id', related_name='sec_class_id')
    section_id = models.CharField(max_length=20, primary_key=True, blank=True)
    section_name = models.CharField(max_length=200)
    total_student = models.IntegerField(null=True, blank=True)
    gide_teacher_id = models.CharField(max_length=20, blank=True, null=True)
    class_start_time = models.TimeField(max_length=40, blank=True, null=True)
    class_end_time = models.TimeField(max_length=40, blank=True, null=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.section_name


class Subject_Category(models.Model):
    category_id = models.CharField(max_length=30, primary_key=True, blank=True)
    category_name = models.CharField(max_length=100, unique=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name


class Subject_Type(models.Model):
    subject_type_id = models.CharField(
        max_length=30, primary_key=True, blank=True)
    subject_type_name = models.CharField(max_length=100, unique=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject_type_name


class Subject_List(models.Model):
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE,
                                 db_column='class_id', related_name='stu_list_class_id')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE, null=True,
                                       blank=True, db_column='class_group_id', related_name='stu_list_class_group_id')
    subject_id = models.CharField(max_length=20, primary_key=True, blank=True)
    subject_type_id = models.ForeignKey(Subject_Type, on_delete=models.CASCADE, null=True,
                                        blank=True, db_column='subject_type_id', related_name='slt_subject_type_id')
    category_id = models.ForeignKey(Subject_Category, on_delete=models.CASCADE,
                                    null=True, blank=True, db_column='category_id', related_name='slt_category_id')
    subject_name = models.CharField(max_length=150)
    sort_name = models.CharField(max_length=100,null=True, blank=True)
    maximum_marks = models.IntegerField(null=True, blank=True)
    minimum_pass_marks = models.IntegerField(null=True, blank=True)
    subject_code = models.IntegerField(null=True, blank=True)
    out_of = models.IntegerField(
        blank=True, null=True, choices=grading_system, default=5)
    credit = models.DecimalField(max_digits=22, decimal_places=2, default=0)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject_name


class Session(models.Model):
    session_id = models.CharField(max_length=30, primary_key=True, blank=True)
    session_name = models.CharField(max_length=100, unique=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.session_name


class Catagory_info(models.Model):
    catagory_id = models.CharField(max_length=30, primary_key=True, blank=True)
    catagory_name = models.CharField(max_length=100, unique=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.catagory_name


class Department_Info(models.Model):
    department_id = models.CharField(
        max_length=20, primary_key=True, blank=True)
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='academic_year', related_name='dep_academic_year')
    department_name = models.CharField(max_length=200, null=False, unique=True)
    total_student = models.IntegerField(null=True, blank=True)
    total_quota = models.IntegerField(null=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.department_name


class Shift_Info(models.Model):
    shift_id = models.CharField(max_length=20, blank=True, primary_key=True)
    shift_name = models.CharField(max_length=200, null=False, unique=True)
    shift_start_time = models.CharField(max_length=100, null=True, blank=True)
    shift_end_time = models.CharField(max_length=100, null=True, blank=True)
    total_student = models.IntegerField(null=True, blank=True)
    total_quota = models.IntegerField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shift_name


class Degree_Info(models.Model):
    degree_id = models.CharField(max_length=20, primary_key=True, blank=True)
    degree_name = models.CharField(max_length=200, null=False, unique=True)
    degree_duration = models.CharField(max_length=200, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.degree_name


class Occupation_Info(models.Model):
    occupation_id = models.CharField(
        max_length=20, primary_key=True, blank=True)
    occupation_name = models.CharField(max_length=200, null=False, unique=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.occupation_name


class Education_Institute(models.Model):
    institute_id = models.CharField(
        max_length=20, primary_key=True, blank=True)
    institute_name = models.CharField(max_length=200, null=False, unique=True)
    institute_code = models.CharField(
        max_length=100, null=True, blank=True, unique=True)
    institute_address = models.CharField(max_length=500, null=True, blank=True)
    institute_mobile = models.CharField(max_length=20, null=True, blank=True)
    lower_degree = models.CharField(max_length=100, null=True, blank=True)
    higher_degree = models.CharField(max_length=100, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.institute_name
class Education_Board(models.Model):
    branch_code = models.IntegerField(blank=True, null=True)
    board_full_name=models.CharField(max_length=200)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.board_full_name)
    
class Certificat_Name(models.Model):
    branch_code = models.IntegerField(blank=True, null=True)
    certificat_full_name=models.CharField(max_length=200)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.certificat_full_name)

class Image_temp(models.Model):
    image_1 = models.ImageField(blank=True, null=True, upload_to='temp/')
    image_2 = models.ImageField(blank=True, null=True, upload_to='temp/')
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

class Students_Info(models.Model):
    branch_code = models.IntegerField(blank=True, null=True)
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='academic_year', related_name='stu_academic_year')
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='session_id', related_name='stu_session_id')
    catagory_id = models.ForeignKey(Catagory_info, on_delete=models.CASCADE, null=True,
                                    blank=True, db_column='catagory_id', related_name='stu_catagory_id')
    student_roll = models.CharField(max_length=30, primary_key=True, blank=True)
    class_roll = models.IntegerField(blank=True, null=True)
    student_reg = models.CharField(max_length=30, null=True, blank=True)
    student_name = models.CharField(max_length=200)
    student_nick_name = models.CharField(max_length=200, null=True, blank=True)
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE,
                                 null=True, blank=True, db_column='class_id', related_name='stu_class_id')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE,
                                       null=True, blank=True, db_column='class_group_id', related_name='stu_class_group_id')
    shift_id = models.ForeignKey(Shift_Info, on_delete=models.CASCADE, null=True,
                                 blank=True, db_column='shift_id', related_name='stu_shift_id')
    section_id = models.ForeignKey(Section_Info, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='section_id', related_name='stu_section_id')
    last_institute_id = models.ForeignKey(Education_Institute, on_delete=models.CASCADE, null=True,
                                          blank=True, db_column='last_institute_id', related_name='stu_last_institute_id')
    student_type = models.CharField(
        max_length=30, choices=Status_Type_list, default='R')
    student_referred_by = models.CharField(
        max_length=15, null=True, blank=True)
    student_father_name = models.CharField(max_length=200, blank=True)
    father_occupation_id = models.ForeignKey(Occupation_Info, on_delete=models.CASCADE, null=True,
                                             blank=True, db_column='father_occupation_id', related_name='stu_father_occupation_id')
    father_email_address = models.CharField(max_length=200, blank=True)
    father_phone_number = models.CharField(max_length=20, blank=True)
    father_nid = models.CharField(max_length=50, blank=True, null=True)
    father_address = models.TextField(blank=True, null=True)
    sms_to_father = models.BooleanField(blank=True, default=False)
    student_mother_name = models.CharField(max_length=200, blank=True)
    profile_image = models.ImageField(
        blank=True, null=True, upload_to='profile/')
    student_signature = models.ImageField(
        blank=True, null=True, upload_to='signature/')
    mother_occupation_id = models.ForeignKey(Occupation_Info, on_delete=models.CASCADE, null=True,
                                             blank=True, db_column='mother_occupation_id', related_name='stu_mother_occupation_id')
    mother_email_address = models.CharField(max_length=200, blank=True)
    mother_phone_number = models.CharField(max_length=20, blank=True)
    mother_nid = models.CharField(max_length=50, blank=True, null=True)
    mother_address = models.TextField(blank=True, null=True)
    sms_to_mother = models.BooleanField(blank=True, default=False)
    student_blood_group = models.CharField(
        max_length=5, choices=BLOOD_GROUP, default='', blank=True)
    student_gender = models.CharField(
        max_length=5, choices=GENDER_LIST, default='', blank=True)
    student_religion = models.CharField(
        max_length=5, choices=RELIGION_LIST, default='', blank=True)
    student_marital_status = models.CharField(
        max_length=5, null=True, choices=MARITAL_STATUS, default='S', blank=True)
    student_national_id = models.CharField(
        max_length=200, null=True, blank=True)
    student_birth_cert = models.CharField(
        max_length=200, null=True, blank=True)
    student_present_address = models.TextField(null=True, blank=True)
    student_permanent_address = models.TextField(null=True, blank=True)
    student_phone = models.CharField(max_length=15, null=True)
    student_email = models.CharField(max_length=130, null=True, blank=True)
    student_joining_date = models.DateField(blank=True, null=True)
    student_date_of_birth = models.DateField(blank=True, null=True)
    student_status = models.CharField(
        max_length=5, null=True, choices=STATUS_LIST, default='A', blank=True)
    student_comments = models.CharField(max_length=200, null=True, blank=True)
    legal_guardian_name = models.CharField(
        max_length=100, blank=True, null=True)
    legal_guardian_contact = models.CharField(
        max_length=15, blank=True, null=True)
    legal_guardian_relation = models.CharField(
        max_length=50, blank=True, null=True)
    legal_guardian_nid = models.CharField(max_length=50, blank=True, null=True)
    legal_guardian_occupation_id = models.ForeignKey(
        Occupation_Info, on_delete=models.CASCADE, null=True, blank=True, db_column='leg_occupation_id', related_name='stu_leg_occupation_id')
    legal_guardian_address = models.TextField(blank=True, null=True)
    local_guardian_name = models.CharField(
        max_length=100, blank=True, null=True)
    local_guardian_contact = models.CharField(
        max_length=15, blank=True, null=True)
    local_guardian_relation = models.CharField(
        max_length=50, blank=True, null=True)
    local_guardian_nid = models.CharField(max_length=50, blank=True, null=True)
    local_guardian_occupation_id = models.ForeignKey(
        Occupation_Info, on_delete=models.CASCADE, null=True, blank=True, db_column='log_occupation_id', related_name='stu_log_occupation_id')
    local_guardian_address = models.TextField(blank=True, null=True)
    per_division_id = models.ForeignKey(Loc_Division, on_delete=models.CASCADE, null=True,
                                        blank=True, db_column='per_division_id', related_name='stu_perdivision_id')
    per_district_id = models.ForeignKey(Loc_District, on_delete=models.CASCADE, null=True,
                                        blank=True, db_column='per_district_id', related_name='stu_perdistrict_id')
    per_upozila_id = models.ForeignKey(Loc_Upazila, on_delete=models.CASCADE, null=True,
                                       blank=True, db_column='per_upozila_id', related_name='stu_perupozila_id')
    pre_division_id = models.ForeignKey(Loc_Division, on_delete=models.CASCADE, null=True,
                                        blank=True, db_column='pre_division_id', related_name='stu_predivision_id')
    pre_district_id = models.ForeignKey(Loc_District, on_delete=models.CASCADE, null=True,
                                        blank=True, db_column='pre_district_id', related_name='stu_predistrict_id')
    pre_upozila_id = models.ForeignKey(Loc_Upazila, on_delete=models.CASCADE, null=True,
                                       blank=True, db_column='pre_upozila_id', related_name='stu_preupozila_id')
    same_as = models.BooleanField(blank=True, default=False)
    account_number = models.CharField(max_length=13, null=True)
    tc_number = models.CharField(max_length=20, null=True, blank=True)
    tc_date = models.CharField(max_length=50, blank=True, null=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.student_roll+' - '+self.student_name


class Education_Qualification(models.Model):
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE,
                                     blank=True, db_column='student_roll', related_name='eq_student_roll')
    degree_name = models.ForeignKey(Degree_Info, on_delete=models.CASCADE,
                                    db_column="degree_name", related_name='eq_degree_name', null=True, blank=True)
    board_name = models.CharField(max_length=200, null=True, blank=True)
    result_point = models.CharField(max_length=100, null=True, blank=True)
    result_grate = models.CharField(max_length=100, null=True, blank=True)
    passing_year = models.CharField(max_length=500, null=True, blank=True)
    institute_id = models.ForeignKey(Education_Institute, on_delete=models.CASCADE,
                                     null=True, blank=True, db_column='institute_id', related_name='eq_institute_id')
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.degree_name)


class Subject_Choice(models.Model):
    branch_code = models.IntegerField(blank=True, null=True)
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='academic_year', related_name='cho_academic_year')
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE,
                                 null=True, blank=True, db_column='class_id', related_name='cho_class_id')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE,
                                       null=True, blank=True, db_column='class_group_id', related_name='cho_class_group_id')
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='session_id', related_name='cho_session_id')
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE,
                                     blank=True, db_column='student_roll', related_name='cho_student_roll')
    subject_id = models.ForeignKey(Subject_List, on_delete=models.CASCADE,
                                   blank=True, db_column='subject_id', related_name='cho_subject_id')
    category_id = models.ForeignKey(Subject_Category, on_delete=models.CASCADE,
                                    blank=True, null=True, db_column='category_id', related_name='cho_category_id')
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.student_roll)


class Student_Admission(models.Model):
    student_roll = models.CharField(max_length=30, null=True, blank=True)
    class_roll = models.CharField(max_length=30, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

########### Teacher ###########

class Teacher(models.Model):
    teacher_id = models.CharField(max_length=40, primary_key=True)
    employee_id = models.ForeignKey(Employee_Details, on_delete=models.CASCADE,
                                    null=False, blank=False, db_column='employee_id', related_name='tea_employee_id')
    status = models.CharField(max_length=4, null=True,
                              choices=STATUS_LIST, default='A', blank=True)
    app_user_id = models.CharField(max_length=40, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.employee_id)


class Mapping_Guide_Teacher(models.Model):
    academic_year = models.ForeignKey(
        Academic_Year, on_delete=models.CASCADE, db_column='academic_year', related_name='tea_academic_year')
    class_id = models.ForeignKey(
        Academic_Class, on_delete=models.CASCADE, db_column='class_id', related_name='tea_class_id')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE,
                                       null=True, blank=True, db_column='class_group_id', related_name='tea_class_group_id')
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE,
                                     blank=True, db_column='student_roll', related_name='tea_student_roll')
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='teacher_id', related_name='tea_teacher_id')
    student_status = models.CharField(
        max_length=2, null=True, choices=STATUS_LIST, default='A', blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


########### Exam and Result Details ###########

class Result_Grade(models.Model):
    grade_id = models.CharField(max_length=30, primary_key=True)
    grade_name = models.CharField(max_length=20)
    result_gpa = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    lowest_mark = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    highest_mark = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    out_of = models.IntegerField(
        blank=True, null=True, choices=grading_system, default=5)
    is_failed = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.grade_name

# # Practical/Oral/Written


class Exam_Type(models.Model):
    examtype_id = models.CharField(max_length=30, primary_key=True)
    examtype_name = models.CharField(max_length=100, unique=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.examtype_name


class Exam_Term(models.Model):
    term_name = models.CharField(max_length=200, unique=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.term_name
# # Class Test/Quiz Test/Assignment/Semester Final/Mid Term


class Exam_Setup(models.Model):
    branch_code = models.IntegerField(blank=True, null=True)
    exam_id = models.CharField(max_length=30, primary_key=True)
    exam_name = models.CharField(max_length=200)
    term_id = models.ForeignKey(Exam_Term, on_delete=models.CASCADE,
                                db_column='term_id', related_name='exs_term_id', null=True, blank=True)
    no_of_exam = models.IntegerField(default=1, null=False, blank=True)
    examtype_id = models.ForeignKey(Exam_Type, on_delete=models.CASCADE, null=True,
                                    blank=True, db_column='examtype_id', related_name='exs_examtype_id')
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='academic_year', related_name='setting_academic_year')
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='session_id', related_name='setting_session_id')
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE, null=True,
                                 blank=True, db_column='class_id', related_name='setting_class_id')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE,
                                       null=True, blank=True, db_column='class_group_id', related_name='es_class_group_id')
    subject_id = models.ForeignKey(Subject_List, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='subject_id', related_name='setting_subject_id')
    cal_condition = models.CharField(
        max_length=20, null=True, choices=Condition_List, default='choice', blank=True)
    total_exam_marks = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    minimum_pass_marks = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    exam_type_status = models.IntegerField(choices=Exam_type_status, default=1)
    out_of = models.IntegerField(
        blank=True, null=True, choices=grading_system, default=5)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.exam_name


class Exam_Marks_Details(models.Model):
    branch_code = models.IntegerField(blank=True, null=True)
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='academic_year', related_name='det_academic_year')
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='session_id', related_name='det_session_id')
    term_id = models.ForeignKey(Exam_Term, on_delete=models.CASCADE, null=True,
                                blank=True, db_column='term_id', related_name='det_term_id')
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE,
                                 null=True, blank=True, db_column='class_id', related_name='det_class_id')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE,
                                       null=True, blank=True, db_column='class_group_id', related_name='det_class_group_id')
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE, null=True,
                                     blank=True, db_column='student_roll', related_name='emd_student_roll')
    subject_id = models.ForeignKey(Subject_List, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='subject_id', related_name='emd_subject_id')
    exam_id = models.ForeignKey(Exam_Setup, on_delete=models.CASCADE, null=True,
                                blank=True, db_column='exam_id', related_name='emd_exam_id')
    exam_no = models.IntegerField(null=True, blank=True)
    total_exam_marks = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    obtain_marks = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    grade_point_average = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    result_grade = models.CharField(max_length=20, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.student_roll)


class Storing_Exam_Marks_Details(models.Model):
    branch_code = models.IntegerField(blank=True, null=True)
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='academic_year', related_name='storing_academic_year')
    term_id = models.ForeignKey(Exam_Term, on_delete=models.CASCADE, null=True,
                                blank=True, db_column='term_id', related_name='storing_term_id')
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE, null=True,
                                 blank=True, db_column='class_id', related_name='storing_class_id')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE,
                                       null=True, blank=True, db_column='class_group_id', related_name='storing_class_group_id')
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE, null=True,
                                     blank=True, db_column='student_roll', related_name='storing_student_roll')
    subject_id = models.ForeignKey(Subject_List, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='subject_id', related_name='storing_subject_id')
    exam_id = models.ForeignKey(Exam_Setup, on_delete=models.CASCADE, null=True,
                                blank=True, db_column='exam_id', related_name='storing_exam_id')
    exam_no = models.IntegerField(null=True, blank=True)
    total_exam_marks = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    obtain_marks = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    grade_point_average = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    result_grade = models.CharField(max_length=20,null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_roll

# Exam mark by exam type


class Exam_Single_Mark(models.Model):
    branch_code = models.IntegerField(blank=True, null=True)
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='academic_year', related_name='single_academic_year')
    term_id = models.ForeignKey(Exam_Term, on_delete=models.CASCADE, null=True,
                                blank=True, db_column='term_id', related_name='single_term_id')
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE, null=True,
                                 blank=True, db_column='class_id', related_name='single_class_id')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE,
                                       null=True, blank=True, db_column='class_group_id', related_name='single_class_group_id')
    exam_id = models.ForeignKey(Exam_Setup, on_delete=models.CASCADE, null=True,
                                blank=True, db_column='exam_id', related_name='single_exam_id')
    subject_id = models.ForeignKey(Subject_List, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='subject_id', related_name='single_subject_id')
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE, null=True,
                                     blank=True, db_column='student_roll', related_name='single_student_roll')
    total_exam_marks = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    obtain_marks = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    result_grade = models.CharField(max_length=20,null=True, blank=True)
    grade_point_average = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.student_roll)


class Store_Exam_Single_Mark(models.Model):
    branch_code = models.IntegerField(blank=True, null=True)
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='academic_year', related_name='store_academic_year')
    term_id = models.ForeignKey(Exam_Term, on_delete=models.CASCADE, null=True,
                                blank=True, db_column='term_id', related_name='store_term_id')
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE,
                                 null=True, blank=True, db_column='class_id', related_name='store_class_id')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE,
                                       null=True, blank=True, db_column='class_group_id', related_name='store_class_group_id')
    exam_id = models.ForeignKey(Exam_Setup, on_delete=models.CASCADE, null=True,
                                blank=True, db_column='exam_id', related_name='store_exam_id')
    subject_id = models.ForeignKey(Subject_List, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='subject_id', related_name='store_subject_id')
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE, null=True,
                                     blank=True, db_column='student_roll', related_name='store_student_roll')
    total_exam_marks = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    obtain_marks = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    result_grade = models.CharField(max_length=20,null=True, blank=True)
    grade_point_average = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.student_roll)

# Exam mark per Subject


class Exam_Marks_By_Subject(models.Model):
    branch_code = models.IntegerField(blank=True, null=True)
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='academic_year', related_name='bysubject_academic_year')
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE, null=True,
                                     blank=True, db_column='session_id', related_name='bysubject_session_id')
    term_id = models.ForeignKey(Exam_Term, on_delete=models.CASCADE, null=True,
                                blank=True, db_column='term_id', related_name='bysubject_term_id')
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='class_id', related_name='bysubject_class_id')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE,
                                       null=True, blank=True, db_column='class_group_id', related_name='bysubject_class_group_id')
    subject_id = models.ForeignKey(Subject_List, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='subject_id', related_name='bysubject_subject_id')
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE, null=True,
                                     blank=True, db_column='student_roll', related_name='bysubject_student_roll')
    total_exam_marks = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    obtain_marks = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    result_grade = models.CharField(max_length=20,null=True, blank=True)
    grade_point_average = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    out_of=models.DecimalField(max_digits=4, decimal_places=2, default=5, blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.student_roll)+" - "+ str(self.academic_year)+" - "+ str(self.obtain_marks)+" - "+ str(self.class_id)+" - "+ str(self.result_grade)

# #Students Final Result at the end of Semester


class Exam_Marks_Final_Hefz(models.Model):
    branch_code = models.IntegerField(blank=True, null=True)
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='academic_year', related_name='Hefz_fin_academic_year')
    term_id = models.ForeignKey(Exam_Term, on_delete=models.CASCADE, null=True,
                                blank=True, db_column='term_id', related_name='Hefz_fin_term_id')
    class_name = models.CharField(max_length=100, blank=True)                        
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE, null=True,
                                     blank=True, db_column='student_roll', related_name='Hefz_fin_student_roll')
    total_exam_marks = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    obtain_marks = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    result_grade = models.CharField(max_length=20, null=True, blank=True)
    grade_point_average = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    merit_position = IntegerField(null=True, blank=True)
    
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.student_roll)
        
class Exam_Marks_Final(models.Model):
    branch_code = models.IntegerField(blank=True, null=True)
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='academic_year', related_name='fin_academic_year')
    term_id = models.ForeignKey(Exam_Term, on_delete=models.CASCADE, null=True,
                                blank=True, db_column='term_id', related_name='fin_term_id')
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE,
                                 null=True, blank=True, db_column='class_id', related_name='fin_class_id')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE,
                                       null=True, blank=True, db_column='class_group_id', related_name='fin_class_group_id')
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE, null=True,
                                     blank=True, db_column='student_roll', related_name='final_student_roll')
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='session_id', related_name='final_session_id')
    total_exam_marks = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    obtain_marks = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    result_grade = models.CharField(max_length=20, null=True, blank=True)
    grade_point_average = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    merit_position = IntegerField(null=True, blank=True)
    point_without_optional =models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.student_roll)+" - "+ str(self.academic_year)+" - "+ str(self.obtain_marks)+" - "+ str(self.class_id)+" - "+ str(self.result_grade)


# # Class Test/Quiz Test/Assignment/Semester Final/Mid Term
class Online_Exam_Information(models.Model):
    online_exam_id = models.CharField(
        max_length=30, primary_key=True, blank=True)
    exam_id = models.ForeignKey(Exam_Setup, on_delete=models.CASCADE, null=True,
                                blank=True, db_column='exam_id', related_name='online_exam_id')
    exam_name = models.CharField(max_length=200, null=False, blank=False)
    basic_info = HTMLField(verbose_name='HTML Content')
    exam_date = models.DateTimeField(null=True, blank=True)
    exam_start_time = models.CharField(max_length=30, null=True, blank=True)
    exam_end_time = models.CharField(max_length=30, null=True, blank=True)
    question_patten = models.CharField(
        max_length=50, choices=Question_patten_List, default='')
    publish_status = models.CharField(
        max_length=50, choices=Exam_Status_List, default='Locked')
    total_marks = models.IntegerField(blank=True, null=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.exam_name

# Online_Exam_Questions


class Online_Exam_Questions(models.Model):
    question_id = models.CharField(max_length=30, primary_key=True)
    online_exam_id = models.ForeignKey(Online_Exam_Information, on_delete=models.CASCADE,
                                       db_column='online_exam_id', related_name='online_online_exam_id', blank=True)
    question = HTMLField(verbose_name='HTML Content')
    question_type = models.CharField(
        max_length=50, choices=Question_Type_List, default='')
    question_marks = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Online_Exam_Qstn_Dtl(models.Model):
    question_details_id = models.CharField(max_length=30, primary_key=True)
    question_id = models.ForeignKey(Online_Exam_Questions, on_delete=models.CASCADE,
                                    db_column='question_id', related_name='online_exam_question_id')
    question_option = models.CharField(max_length=2000, null=True, blank=True)
    is_correct_answer = models.IntegerField(null=False, blank=False)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class OnlineExam_Ans_Info(models.Model):
    ans_info_id = models.CharField(max_length=30, primary_key=True)
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE,
                                     blank=True, db_column='student_roll', related_name='ans_student')
    online_exam_id = models.ForeignKey(Online_Exam_Information, on_delete=models.CASCADE,
                                       null=True, blank=True, db_column='online_exam_id', related_name='ans_question')
    exam_date = models.DateTimeField(null=True, blank=True)
    exam_start_time = models.CharField(max_length=30, null=True, blank=True)
    exam_end_time = models.CharField(max_length=30, null=True, blank=True)
    publish_status = models.CharField(
        max_length=50, choices=Exam_Status_List, default='Locked')
    total_obtain_marks = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    total_marks = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.student_roll)


class OnlineExam_Question_Ans(models.Model):
    answer_id = models.CharField(max_length=30, primary_key=True)
    ans_info_id = models.ForeignKey(OnlineExam_Ans_Info, on_delete=models.CASCADE,
                                    db_column='ans_info_id', related_name='ans_info', blank=True)
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE,
                                     blank=True, db_column='student_roll', related_name='oqa_student_roll')
    question_id = models.ForeignKey(Online_Exam_Questions, on_delete=models.CASCADE,
                                    db_column='question_id', related_name='oqa_question_id', blank=True)
    obtain_marks = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    question_marks = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class OnlineExam_Qstn_Ansdtl(models.Model):
    question_details_id = models.ForeignKey(Online_Exam_Qstn_Dtl, on_delete=models.CASCADE,
                                            db_column='question_details_id', related_name='oqadtl_question_details_id', null=True, blank=True)
    answer_id = models.ForeignKey(OnlineExam_Question_Ans, on_delete=models.CASCADE,
                                  db_column='answer_id', related_name='oqadtl_answer_id')
    answer_option = models.CharField(max_length=2000, null=True, blank=True)
    is_correct_answer = models.IntegerField(blank=False, default=0)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Visited_Student_Info(models.Model):
    student_name = models.CharField(max_length=200)
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE, null=True,
                                 blank=True, db_column='vsi_class_id', related_name='vsi_class_id')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE, null=True,
                                       blank=True, db_column='vsi_class_group_id', related_name='vsi_class_group_id')
    student_father_name = models.CharField(max_length=200, blank=True)
    father_phone_number = models.CharField(max_length=20, blank=True)
    student_mother_name = models.CharField(max_length=200, blank=True)
    mother_phone_number = models.CharField(max_length=20, blank=True)
    student_marital_status = models.CharField(
        max_length=5, null=True, choices=MARITAL_STATUS, default='S', blank=True)
    student_present_address = models.TextField(null=True, blank=False)
    student_permanent_address = models.TextField(null=True, blank=True)
    student_phone = models.CharField(max_length=15, null=True)
    student_email = models.CharField(max_length=30, null=True, blank=True)
    current_institute = models.CharField(max_length=100, null=True, blank=True)
    education_qualifications = JSONField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_name


class SubjectMarkTemp(models.Model):
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE,
                                     blank=True, db_column='student_roll', related_name='tempt_student_roll')
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='academic_year', related_name='tempt_academic_year')
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE,
                                 null=True, blank=True, db_column='class_id', related_name='tempt_class_id')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE, null=True,
                                       blank=True, db_column='class_group_id', related_name='tempt_class_group_id')
    subject_id = models.ForeignKey(Subject_List, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='subject_id', related_name='tempt_subject_id')
    total_obtain_marks = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    total_marks = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    result_gpa = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    grade_name = models.CharField(max_length=20 ,null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.student_roll)


class Present_sheet_info(models.Model):
    present_sheet_info_id = models.CharField(
        max_length=20, primary_key=True, blank=True)
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='academic_year', related_name='psi_academic_year')
    month_number = models.IntegerField(
        choices=Month_List, default='choice', blank=True)
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE,
                                 null=True, blank=True, db_column='class_id', related_name='psi_class_id')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE,
                                       null=True, blank=True, db_column='class_group_id', related_name='psi_class_group_id')
    section_id = models.ForeignKey(Section_Info, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='section_id', related_name='psi_section_id')
    subject_id = models.ForeignKey(Subject_List, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='subject_id', related_name='psi_subject_id')
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.class_id)


class Present_sheet_dtl(models.Model):
    present_sheet_info_id = models.ForeignKey(Present_sheet_info, on_delete=models.CASCADE, null=True,
                                              blank=True, db_column='present_sheet_info_id', related_name='psd_present_sheet_info_id')
    date = models.DateField(null=True, blank=True)
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE,
                                     blank=True, db_column='student_roll', related_name='psd_student_roll')
    is_present = models.IntegerField(blank=False, default=0)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.student_roll)

    class Meta:
        # sort by "the date" in descending order unless
        # overridden in the query with order_by()
        ordering = ['date']

# class Student_Leave_Request(models.Model):
#     student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE, null=True, blank=True, db_column='student_roll', related_name='slr_student_roll')
#     application_date = models.DateField()
#     start_date = models.DateField()
#     end_date = models.DateField()
#     total_days = models.IntegerField(blank=True)
#     leave_reason = models.TextField()
#     leave_apply_to = models.ForeignKey(Employee_Details, on_delete=models.CASCADE, null=True, blank=True, db_column='leave_apply_to', related_name='slr_leave_apply_to')
#     leave_approve_by = models.ForeignKey(Employee_Details, on_delete=models.CASCADE, null=True, blank=True, db_column='leave_approve_by', related_name='slr_leave_approve_by')
#     leave_approve_on = models.DateTimeField(blank=True)
#     app_user_id = models.CharField(max_length=20, null=False, blank=True)
#     app_data_time = models.DateTimeField(auto_now_add=True)


# class Attendance_Sheet_Line(models.Model):
#     student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE, null=True, blank=True, db_column='student_roll', related_name='asl_student_roll')
#     attendance_date = models.DateField()
#     start_time = models.DateTimeField(null=True, blank=True)
#     end_time = models.DateTimeField(null=True, blank=True)
#     is_present = models.BooleanField(blank=True,default=True)
#     is_absent = models.BooleanField(blank=True,default=False)
#     total_attendance_hour = models.IntegerField(null=True, blank=True)
#     total_attendance_minute = models.IntegerField(null=True, blank=True)
#     attendance_approve_by = models.ForeignKey(Employee_Details, on_delete=models.CASCADE, null=True, blank=True, db_column='attendance_approve_by', related_name='ats_attendance_approve_by')
#     app_user_id = models.CharField(max_length=20, null=False, blank=True)
#     app_data_time = models.DateTimeField(auto_now_add=True)

########## Library Module ############

class Library_Rack(models.Model):
    rack_id = models.CharField(max_length=30, primary_key=True)
    rack_name = models.CharField(max_length=200)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.rack_name


class Library_Author(models.Model):
    author_id = models.CharField(max_length=30, primary_key=True)
    author_name = models.CharField(max_length=200)
    born_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author_name


class Library_Editor(models.Model):
    editor_id = models.CharField(max_length=30, primary_key=True)
    editor_name = models.CharField(max_length=200)
    editor_websight = models.CharField(max_length=200, null=True, blank=True)
    editor_email = models.CharField(max_length=200, null=True, blank=True)
    editor_phone = models.CharField(max_length=200, null=True, blank=True)
    editor_addres = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.editor_name


class Library_Books(models.Model):
    book_id = models.CharField(max_length=30, primary_key=True)
    book_name = models.CharField(max_length=200)
    author_id = models.ForeignKey(Library_Author, on_delete=models.CASCADE,
                                  null=True, blank=True, db_column='author_id', related_name='bok_author_id')
    editor_id = models.ForeignKey(Library_Editor, on_delete=models.CASCADE,
                                  null=True, blank=True, db_column='editor_id', related_name='bok_editor_id')
    isbn_code = models.CharField(
        max_length=200, null=True, blank=True, help_text="Shows International Standard Book Number")
    book_language = models.CharField(
        max_length=200, null=True, blank=True, default="Bengali")
    fine_lost = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    fine_late_return = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    number_of_page = models.IntegerField(default=0)
    rack_id = models.ForeignKey(Library_Rack, on_delete=models.CASCADE,
                                null=True, blank=True, db_column='rack_id', related_name='bok_rack_id')
    total_books = models.IntegerField(default=0)
    books_available = models.IntegerField(default=0)
    edition_number = models.CharField(max_length=200, null=True, blank=True)
    is_ebook = models.BooleanField(default=False)
    is_subscription = models.BooleanField(
        default=False, help_text="Is Subscription based")
    subscription_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    day_to_return_book = models.IntegerField(default=0, blank=True, null=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    ebook_file = models.FileField(
        blank=True, null=True, upload_to='ebook/', max_length=200)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.book_name


class Library_Card(models.Model):
    card_number = models.CharField(max_length=30, primary_key=True)
    name_on_card = models.CharField(max_length=200)
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE, null=True,
                                     blank=True, db_column='student_roll', related_name='lic_student_roll')
    teacher_id = models.ForeignKey(Employee_Details, on_delete=models.CASCADE,
                                   null=True, blank=True, db_column='teacher_id', related_name='lic_teacher_id')
    book_limit = models.IntegerField(default=0)
    book_taken = models.IntegerField(default=0)
    card_status = models.CharField(
        max_length=2, null=True, choices=STATUS_LIST, default='A', blank=True)
    start_date = models.DateField(null=True, blank=True)
    expire_date = models.DateField(null=True, blank=True)
    duration_month = models.IntegerField()
    total_late_penalty = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    total_lost_penalty = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_on_card


class Library_Card_History(models.Model):
    history_id = models.CharField(max_length=30, primary_key=True)
    card_number = models.ForeignKey(Library_Card, on_delete=models.CASCADE, null=True,
                                    blank=True, db_column='card_number', related_name='his_card_number')
    history_status = models.CharField(
        max_length=2, null=True, choices=HISTORY_STATUS, default='A', blank=True)
    date = models.DateField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.card_number


class Library_Book_Issue(models.Model):
    issue_id = models.CharField(max_length=30, primary_key=True)
    book_id = models.ForeignKey(Library_Books, on_delete=models.CASCADE,
                                null=True, blank=True, db_column='book_id', related_name='lbi_book_id')
    card_number = models.ForeignKey(Library_Card, on_delete=models.CASCADE, null=True,
                                    blank=True, db_column='card_number', related_name='lbi_card_number')
    issue_date = models.DateField(null=True, blank=True)
    actual_return_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    day_to_return_book = models.IntegerField(default=0)
    late_penalty = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    lost_penalty = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    late_reason = models.CharField(max_length=100, null=True, blank=True)
    lost_reason = models.CharField(max_length=100, null=True, blank=True)
    book_issue_status = models.CharField(
        max_length=2, null=True, choices=STATUS_LIST, default='A', blank=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Library_Book_Request(models.Model):
    request_id = models.CharField(max_length=30, primary_key=True)
    book_id = models.ForeignKey(Library_Books, on_delete=models.CASCADE,
                                null=True, blank=True, db_column='book_id', related_name='lbr_book_id')
    card_number = models.ForeignKey(Library_Card, on_delete=models.CASCADE, null=True,
                                    blank=True, db_column='card_number', related_name='lbr_card_number')
    request_date = models.DateField(null=True, blank=True)
    actual_return_date = models.DateField(null=True, blank=True)
    day_to_return_book = models.IntegerField(default=0)
    book_issue_status = models.CharField(
        max_length=2, null=True, choices=STATUS_LIST, default='A', blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.card_number


class Class_Routine(models.Model):
    routine_id = models.CharField(max_length=50, primary_key=True)
    routine_name = models.CharField(max_length=50, null=True, blank=False)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.routine_name


class Class_Routine_Details(models.Model):
    routine_details_id = models.CharField(max_length=50, primary_key=True)
    start_time = models.TimeField(max_length=40, null=True, blank=True)
    end_time = models.TimeField(max_length=40, null=True, blank=True)
    routine_id = models.ForeignKey(Class_Routine, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='routine_id', related_name='rou_routine_id')
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='academic_year', related_name='rou_academic_year')
    teacher_id = models.ForeignKey(Employee_Details, on_delete=models.CASCADE,
                                   null=True, blank=True, db_column='teacher_id', related_name='rou_teacher_id')
    subject_id = models.ForeignKey(Subject_List, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='subject_id', related_name='rou_subject_id')
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE,
                                 null=True, blank=True, db_column='class_id', related_name='rou_class_id')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE,
                                       null=True, blank=True, db_column='class_group_id', related_name='rou_class_group_id')
    shift_id = models.ForeignKey(Shift_Info, on_delete=models.CASCADE, null=True,
                                 blank=True, db_column='shift_id', related_name='rou_shift_id')
    section_id = models.ForeignKey(Section_Info, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='section_id', related_name='rou_section_id')
    room_id = models.ForeignKey(Class_Room, on_delete=models.CASCADE, null=True,
                                blank=True, db_column='room_id', related_name='rou_room_id')
    day = models.IntegerField(
        choices=Week_List, default=get_week_number(datetime.now().strftime("%A")))
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.routine_details_id)


class Present_sheet_Access(models.Model):
    teacher_id = models.ForeignKey(Employee_Details, on_delete=models.CASCADE,
                                   null=True, blank=True, db_column='teacher_id', related_name='acc_teacher_id')
    present_sheet_info_id = models.ForeignKey(Present_sheet_info, on_delete=models.CASCADE, null=True,
                                              blank=True, db_column='present_sheet_info_id', related_name='acc_present_sheet_info_id')
    is_access = models.IntegerField(null=False, blank=True, default=1)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.teacher_id)


class Transfer_Certificate(models.Model):
    tc_id = models.CharField(max_length=50, primary_key=True)
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE, null=True,
                                     blank=True, db_column='student_roll', related_name='tc_student_roll')
    date = models.DateField(null=True, blank=True)
    tc_reason = models.TextField(blank=True, null=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.student_roll)


class Exam_Attendance(models.Model):
    exam_atten_id = models.CharField(max_length=50, primary_key=True)
    academic_Year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='academic_year', related_name='ExA_academic_year')
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE,
                                 null=True, blank=True, db_column='class_id', related_name='ExA_class_id')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE,
                                       null=True, blank=True, db_column='class_group_id', related_name='ExA_class_group_id')
    shift_id = models.ForeignKey(Shift_Info, on_delete=models.CASCADE, null=True,
                                 blank=True, db_column='shift_id', related_name='ExA_shift_id')
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='session_id', related_name='ExA_session_id')
    subject_id = models.ForeignKey(Subject_List, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='subject_id', related_name='ExA_subject_id')
    examtype_id = models.ForeignKey(Exam_Type, on_delete=models.CASCADE, null=True,
                                    blank=True, db_column='examtype_id', related_name='ExA_examtype_id')
    exam_id = models.ForeignKey(Exam_Setup, on_delete=models.CASCADE, null=True,
                                blank=True, db_column='exam_id', related_name='ExA_exam_id')
    day = models.CharField(max_length=20, null=False, blank=True)
    ex_start_time = models.CharField(max_length=40, null=True, blank=True)
    ex_end_time = models.CharField(max_length=40, null=True, blank=True)
    exam_date = models.DateField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.subject_id)


class Exam_attendence_Details(models.Model):
    exam_atten_id = models.ForeignKey(Exam_Attendance, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='exam_atten_id', related_name='dtl_exam_atten_id')
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE, null=True,
                                     blank=True, db_column='student_roll', related_name='edtl_student_roll')
    student_name = models.CharField(max_length=20, null=False, blank=True)
    is_present = models.IntegerField(null=False, blank=True, default=0)
    comments = models.CharField(max_length=20, null=False, blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.student_roll)


class Fees_Head_Settings(models.Model):
    head_code = models.CharField(max_length=13, null=False, primary_key=True)
    head_name = models.CharField(max_length=200, null=False)
    parent_head = models.ForeignKey('Fees_Head_Settings', on_delete=models.CASCADE,
                                    null=True, blank=True, db_column='parent_head', related_name='fee_parent_head')
    # gl list of account modules
    head_ledger = models.CharField(max_length=150, null=False, blank=True)
    is_main_head = models.BooleanField(blank=False, default=False)
    head_comments = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.head_name)

class Fees_Mapping(models.Model):
    fees_mapping_id = models.CharField(max_length=13, null=False, blank=True, primary_key=True)
    branch_code = models.IntegerField(blank=True, null=True)
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=False, db_column='academic_year', related_name='feesmapping_academic_year')
    head_code = models.ForeignKey(Fees_Head_Settings, on_delete=models.CASCADE, null=True, blank=True, db_column='head_code',
                                  related_name='fem_head_code')  # List item from Fees_Head_Settings which are not main head (is_main_head=False)
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE,
                                 null=True, blank=True, db_column='class_id', related_name='fem_class_id')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE,
                                       null=True, blank=True, db_column='class_group_id', related_name='fem_class_group_id')
    section_id = models.ForeignKey(Section_Info, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='section_id', related_name='fem_section_id')
    effective_date = models.DateField(null=True, blank=True)
    fine_effective_days = models.IntegerField(null=False, blank=True, default=0)
    fee_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    fine_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    pay_freq = models.CharField(
        max_length=5, choices=FEE_PAY_FRQ_LIST, default='', blank=True)
    is_single_lifetime = models.BooleanField(blank=False, default=False)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.head_code)+' - '+str(self.class_id)


class Fees_Waiver(models.Model):
    waive_code = models.CharField(max_length=13, null=False, primary_key=True)
    waive_name = models.CharField(max_length=200, null=False)
    student_category=models.ForeignKey(Catagory_info, on_delete=models.CASCADE, null=True,blank=True, db_column='student_category_id', related_name='fw_student_category_id')
    waive_comments = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.waive_code+' - '+self.waive_name

class Fees_Waiver_Mapping(models.Model):
    branch_code = models.IntegerField(blank=True, null=True)
    head_code = models.ForeignKey(Fees_Head_Settings, on_delete=models.CASCADE, null=True, blank=True, db_column='head_code',
                                  related_name='waive_head_code')  # List item from Fees_Head_Settings which are not main head (is_main_head=False)
    waive_name = models.CharField(max_length=200, null=False)
    catagory_id = models.ForeignKey(Catagory_info, on_delete=models.CASCADE, null=True,blank=True, db_column='catagory_id', related_name='waive_category_id')
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE,
                                 null=True, blank=True, db_column='class_id', related_name='waive_class_id')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE,
                                       null=True, blank=True, db_column='class_group_id', related_name='waive_class_group_id')
    section_id = models.ForeignKey(Section_Info, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='section_id', related_name='waive_section_id')
    waiver_parsentag = models.DecimalField(max_digits=22, decimal_places=2, default=0.00)
    waiver_amount = models.DecimalField(max_digits=22, decimal_places=2, default=0.00)
    effective_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.catagory_id)+' - '+str(self.head_code)

class Fees_Waiver_Mapping_Hist(models.Model):
    head_code = models.ForeignKey(Fees_Head_Settings, on_delete=models.CASCADE, null=True, blank=True, db_column='head_code',
                                  related_name='waivhist_head_code')  # List item from Fees_Head_Settings which are not main head (is_main_head=False)
    catagory_id = models.ForeignKey(Catagory_info, on_delete=models.CASCADE, null=True,blank=True, db_column='catagory_id', related_name='waivhis_category_id')
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE,
                                 null=True, blank=True, db_column='class_id', related_name='waivhis_class_id')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE,
                                       null=True, blank=True, db_column='class_group_id', related_name='waivhis_class_group_id')
    section_id = models.ForeignKey(Section_Info, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='section_id', related_name='waivhis_section_id')
    waiver_parsentag = models.DecimalField(max_digits=22, decimal_places=2, default=0.00)
    waiver_amount = models.DecimalField(max_digits=22, decimal_places=2, default=0.00)
    effective_date = models.DateField(null=True, blank=True)
    day_serial = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.catagory_id)+' - '+str(self.head_code)


# History of all changes in Fees_Mapping

class Fees_Mapping_History(models.Model):
    fees_mapping_id = models.CharField(max_length=20, null=False, blank=True)
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=False, db_column='academic_year', related_name='feesmappinghist_academic_year')
    head_code = models.ForeignKey(Fees_Head_Settings, on_delete=models.CASCADE, null=True, blank=True, db_column='head_code',
                                  related_name='feh_head_code')  # List item from Fees_Head_Settings which are not main head (is_main_head=False)
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE,
                                 null=True, blank=True, db_column='class_id', related_name='feh_class_id')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE,
                                       null=True, blank=True, db_column='class_group_id', related_name='feh_class_group_id')
    section_id = models.ForeignKey(Section_Info, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='section_id', related_name='feh_section_id')
    effective_date = models.DateField(null=True, blank=True)
    fine_effective_days = models.IntegerField(null=False, blank=True, default=0)
    day_serial = models.IntegerField(null=True, blank=True)
    fee_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    fine_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    pay_freq = models.CharField(
        max_length=5, choices=FEE_PAY_FRQ_LIST, default='', blank=True)
    is_single_lifetime = models.BooleanField(blank=False, default=False)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.head_code+' - '+self.class_id


class Absent_Fine_Mapping(models.Model):
    head_code = models.ForeignKey(Fees_Head_Settings, on_delete=models.CASCADE, null=True, blank=True, db_column='head_code',
                                  related_name='afm_head_code')  # List item from Fees_Head_Settings which are not main head (is_main_head=False)
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE,
                                 null=True, blank=True, db_column='class_id', related_name='afm_class_id')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE,
                                       null=True, blank=True, db_column='class_group_id', related_name='afm_class_group_id')
    section_id = models.ForeignKey(Section_Info, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='section_id', related_name='afm_section_id')
    effective_date = models.DateField(null=True, blank=True)
    no_of_absent = models.IntegerField()
    fine_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.head_code+' - '+self.class_id


class Absent_Fine_History(models.Model):
    head_code = models.ForeignKey(Fees_Head_Settings, on_delete=models.CASCADE, null=True, blank=True, db_column='head_code',
                                  related_name='afh_head_code')  # List item from Fees_Head_Settings which are not main head (is_main_head=False)
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE,
                                 null=True, blank=True, db_column='class_id', related_name='afh_class_id')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE,
                                       null=True, blank=True, db_column='class_group_id', related_name='afh_class_group_id')
    section_id = models.ForeignKey(Section_Info, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='section_id', related_name='afh_section_id')
    effective_date = models.DateField(null=True, blank=True)
    no_of_absent = models.IntegerField(null=True, blank=True)
    day_serial = models.IntegerField(null=True, blank=True)
    fine_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.head_code+' - '+self.class_id


class Fees_Waive_Student(models.Model):
    #academic_year = models.BigIntegerField(blank=True, default=True)
    branch_code = models.IntegerField(blank=True, null=True)
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE,
                                     blank=True, db_column='student_roll', related_name='few_student_roll')
    head_code = models.ForeignKey(Fees_Head_Settings, on_delete=models.CASCADE, null=True, blank=True, db_column='head_code',
                                  related_name='few_head_code')  # List item from Fees_Head_Settings which are not main head (is_main_head=False)
    ledger_code = models.CharField(max_length=20, null=True, blank=True)
    effective_date = models.DateField(null=True, blank=True)
    is_fully_waive = models.BooleanField(default=False)
    is_group_waive = models.BooleanField(default=False)
    fee_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    waive_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    waive_percentage = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    fees_month = models.IntegerField(blank=True, null=True)
    fees_year = models.IntegerField(blank=True, default=True, null=True)
    auth_by = models.CharField(max_length=20, null=True, blank=True)
    auth_on = models.DateTimeField(null=True, blank=True)
    cancel_by = models.CharField(max_length=20, null=True, blank=True)
    cancel_on = models.DateTimeField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_roll+' - '+self.head_code


class Fees_Processing_Details(models.Model):
    process_id = models.CharField(max_length=20, primary_key=True, blank=True)
    branch_code = models.IntegerField(blank=True, null=True)
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE,null=True,
                                     blank=True, db_column='student_roll', related_name='feeproc_student_roll')
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE, null=True,
                                 blank=True, db_column='class_id', related_name='feeproc_class_id')
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='academic_year', related_name='feeproc_academic_year')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE, null=True,
                                       blank=True, db_column='class_group_id', related_name='feeproc_class_group_id')
    section_id = models.ForeignKey(Section_Info, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='section_id', related_name='feeproc_section_id')
    process_date = models.DateField(null=False, blank=False)
    process_status = models.BooleanField(blank=True, default=False)
    process_error = models.CharField(max_length=2000, null=True, blank=True)
    cancel_by = models.CharField(max_length=20, null=True, blank=True)
    cancel_on = models.DateTimeField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.student_roll)

class Fees_Receive_Temp(models.Model):
    branch_code = models.IntegerField(blank=True, null=True)
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE,
                                     blank=True, db_column='student_roll', related_name='frc_student_roll')
    head_code = models.ForeignKey(Fees_Head_Settings, on_delete=models.CASCADE, null=True, blank=True, db_column='head_code',
                                  related_name='frc_head_code')  # List item from Fees_Head_Settings which are not main head (is_main_head=False)
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE, null=True,
                                 blank=True, db_column='class_id', related_name='frcdue_class_id') 
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE, null=True,
                                       blank=True, db_column='class_group_id', related_name='frcdue_class_group_id')
    section_id = models.ForeignKey(Section_Info, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='section_id', related_name='ffrcdue_section_id')
    head_name = models.CharField(max_length=200, null=True, blank=True)
    ledger_code = models.CharField(max_length=20, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    due_month = models.BigIntegerField(blank=True, default=True, null=True)
    due_year = models.BigIntegerField(blank=True, default=True, null=True)
    fees_due = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    fees_waive = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    fine_due = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    fine_waive = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    total_due = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    total_waive = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    fees_paid = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    fine_paid = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    total_paid = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    fees_overdue = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    fine_overdue = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    total_overdue = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    auth_by = models.CharField(max_length=20, null=True, blank=True)
    auth_on = models.DateTimeField(null=True, blank=True)
    cancel_by = models.CharField(max_length=20, null=True, blank=True)
    cancel_on = models.DateTimeField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.student_roll)+' - '+ str(self.head_code)


class Fees_Receive_Summary(models.Model):
    branch_code = models.IntegerField(blank=True, null=True)
    transaction_id = models.CharField(max_length=20, null=True, blank=True)
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE,
                                     blank=True, db_column='student_roll', related_name='frsu_student_roll')
    receive_date = models.DateField(null=True, blank=True)
    receive_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    tran_batch_number = models.IntegerField(default=0)
    auth_by = models.CharField(max_length=20, null=True, blank=True)
    auth_on = models.DateTimeField(null=True, blank=True)
    cancel_by = models.CharField(max_length=20, null=True, blank=True)
    cancel_on = models.DateTimeField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_roll+' - '+self.receive_date


class Fees_Receive_Student(models.Model):
    branch_code = models.IntegerField(blank=True, null=True)
    transaction_id = models.CharField(max_length=20, null=True, blank=True)
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE,
                                     blank=True, db_column='student_roll', related_name='frs_student_roll')
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE, null=True,
                                 blank=True, db_column='class_id', related_name='feeprec_class_id') 
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE, null=True,
                                       blank=True, db_column='class_group_id', related_name='feerec_class_group_id')
    section_id = models.ForeignKey(Section_Info, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='section_id', related_name='feerec_section_id')
    head_code = models.CharField(max_length=20, null=True, blank=True)
    ledger_code = models.CharField(max_length=20, null=True, blank=True)
    receive_date = models.DateField(null=True, blank=True)
    receive_year = models.IntegerField(blank=True, null=True)
    receive_month = models.IntegerField(blank=True, null=True)
    due_date = models.DateField(null=True, blank=True)
    fees_due = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    fees_waive = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    fine_due = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    fine_waive = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    total_due = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    total_waive = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    fees_paid = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    fine_paid = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    total_paid = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    fees_overdue = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    fine_overdue = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    total_overdue = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    auth_by = models.CharField(max_length=20, null=True, blank=True)
    auth_on = models.DateTimeField(null=True, blank=True)
    cancel_by = models.CharField(max_length=20, null=True, blank=True)
    cancel_on = models.DateTimeField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_roll+' - '+self.head_code

class Fees_Due_Student(models.Model):
    branch_code = models.IntegerField(blank=True, null=True)
    academic_year = models.BigIntegerField(blank=True, default=True)
    due_month = models.BigIntegerField(blank=True, default=True, null=True)
    due_year = models.BigIntegerField(blank=True, default=True, null=True)
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE,
                                     blank=True, db_column='student_roll', related_name='fds_student_roll')
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE, null=True,
                                 blank=True, db_column='class_id', related_name='feedue_class_id') 
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE, null=True,
                                       blank=True, db_column='class_group_id', related_name='feedue_class_group_id')
    section_id = models.ForeignKey(Section_Info, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='section_id', related_name='feedue_section_id')
    head_code = models.CharField(max_length=20, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    process_date = models.DateField(null=True, blank=True)
    fine_due_date = models.DateField(null=True, blank=True)
    fee_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    fine_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    waive_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    waive_percentage = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    fine_waive = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    auth_by = models.CharField(max_length=20, null=True, blank=True)
    auth_on = models.DateTimeField(null=True, blank=True)
    cancel_by = models.CharField(max_length=20, null=True, blank=True)
    cancel_on = models.DateTimeField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_roll+' - '+self.head_code

class One_Time_Fees_Rec_Std(models.Model):
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE,db_column='student_roll', related_name='otfr_student_roll')
    head_code = models.ForeignKey(Fees_Head_Settings, on_delete=models.CASCADE, null=True, blank=True, db_column='head_code',
                                  related_name='otfr_head_code') 
    ledger_code = models.CharField(max_length=20, null=True, blank=True)
    receive_date = models.DateField()
    receive_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    remark=models.CharField(max_length=250, null=True,blank=True)
    auth_by = models.CharField(max_length=20, null=True, blank=True)
    auth_on = models.DateTimeField(null=True, blank=True)
    cancel_by = models.CharField(max_length=20, null=True, blank=True)
    cancel_on = models.DateTimeField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

class Student_ID_Card(models.Model):
    id_card_no = models.CharField(max_length=200, null=False, primary_key=True)
    branch_code = models.IntegerField(blank=True, null=True)
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE,
                                     blank=True, db_column='student_roll', related_name='idcard_student_roll')
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE, null=True,
                                 blank=False, db_column='class_id', related_name='idcard_class_id')
    academic_Year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=False, db_column='academic_year', related_name='idcard_academic_year')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE, null=True,
                                       blank=True, db_column='class_group_id', related_name='idcard_class_group_id')
    section_id = models.ForeignKey(Section_Info, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='section_id', related_name='idard_section_id')
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='session_id', related_name='idcard_session_id')
    expire_date = models.DateTimeField(null=True, blank=False)
    back_text = models.TextField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_roll


class Student_Admit_Card(models.Model):
    branch_code = models.IntegerField(blank=True, null=True)
    admit_card_id = models.CharField(
        max_length=200, null=False, primary_key=True)
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='academic_year', related_name='admc_academic_year')
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE,
                                 null=True, blank=False, db_column='class_id', related_name='admc_class_id')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE,
                                       null=True, blank=True, db_column='class_group_id', related_name='admc_class_group_id')
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE,
                                     blank=True, db_column='student_roll', related_name='admc_student_roll')
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='session_id', related_name='admc_session_id')
    exam_id = models.ForeignKey(Exam_Setup, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='exam_id', related_name='admc_exam_id')
    exam_term_id = models.ForeignKey(Exam_Term, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='exam_term_id', related_name='admc_exam_term_id')
    trams_con=models.TextField(null=True,blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.class_id


class Marge_Result(models.Model):
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='academic_year', related_name='mar_academic_year')
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE,
                                 null=True, blank=False, db_column='class_id', related_name='mar_class_id')
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE,
                                     blank=True, db_column='student_roll', related_name='mar_student_roll')
    term_id = models.CharField(max_length=100, blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    total_exam_marks = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    total_obtain_marks = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    gpa = models.CharField(max_length=20, blank=True, null=True)
    lg = models.CharField(max_length=20, blank=True, null=True)
    position = models.CharField(max_length=20, blank=True, null=True)
    publish_status = models.CharField(
        max_length=2, null=True, choices=PUBLISH_STATUS, default='A', blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Course_Registrations(models.Model):
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE,
                                 null=True, blank=True, db_column='class_id', related_name='cou_class_id')
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE,
                                     blank=True, db_column='student_roll', related_name='cou_student_roll')
    course_name = models.CharField(max_length=200, blank=True, null=True)
    reg_no = models.CharField(max_length=100, blank=False, null=False)
    issue_date = models.DateField(null=True, blank=True)
    expire_date = models.DateField(blank=True, null=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reg_no


class Student_Seat_plane(models.Model):
    branch_code = models.IntegerField(blank=True, null=True)
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE,
                                     blank=True, db_column='student_roll', related_name='seat_student_roll')
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE, null=True,
                                 blank=False, db_column='class_id', related_name='seat_class_id')
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=False, db_column='academic_year', related_name='seat_academic_year')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE, null=True,
                                       blank=True, db_column='class_group_id', related_name='seat_class_group_id')
    term_id = models.ForeignKey(Exam_Term, on_delete=models.CASCADE,
                                db_column='term_id', related_name='seat_term_id', null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_roll

class Student_Name_Plate(models.Model):
    branch_code = models.IntegerField(blank=True, null=True)
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE,
                                     blank=True, db_column='student_roll', related_name='name_student_roll')
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE, null=True,
                                 blank=False, db_column='class_id', related_name='name_class_id')
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=False, db_column='academic_year', related_name='name_academic_year')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE, null=True,
                                       blank=True, db_column='class_group_id', related_name='name_class_group_id')
    slogan = models.TextField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_roll

class Admission_form_header(models.Model):
    branch_code = models.IntegerField(blank=True, null=True)
    academic_name=models.CharField(max_length=200)
    form_name=models.CharField(max_length=200)
    text_one=models.CharField(max_length=200,null=True, blank=True)
    text_two=models.CharField(max_length=200,null=True, blank=True)
    text_three=models.CharField(max_length=200,null=True, blank=True)
    text_four=models.CharField(max_length=200,null=True, blank=True)
    text_five=models.CharField(max_length=200,null=True, blank=True)
    logo = models.ImageField(upload_to="logo/", null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.form_name)



class IdCard_form_header(models.Model):
    branch_code = models.IntegerField(blank=True, null=True)
    academic_name=models.CharField(max_length=200)
    logo = models.ImageField(upload_to="logo/", null=True, blank=True)
    sing = models.ImageField(upload_to="sing/", null=True, blank=True)
    address=models.TextField(blank=True, null=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.academic_name)

class student_migration_history(models.Model):
    branch_code = models.IntegerField(blank=True, null=True)
    from_accademic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE,  db_column='from_accademic_year', related_name='fm_academic_year')
    to_accademic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE,  db_column='to_accademic_year', related_name='tm_academic_year')
    from_class = models.ForeignKey(Academic_Class, on_delete=models.CASCADE, db_column='from_class', related_name='form_class_id')
    to_class = models.ForeignKey(Academic_Class, on_delete=models.CASCADE, db_column='to_class', related_name='to_class_id')
    
    from_class_group = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE, null=True,
                                       blank=True, db_column='from_class_group', related_name='form_class_group_id')
    to_class_group = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE, null=True,
                                       blank=True, db_column='to_class_group', related_name='to_class_group_id')
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE,
                                     blank=True, db_column='student_roll', related_name='migr_student_roll')
    from_section = models.ForeignKey(Section_Info, on_delete=models.CASCADE,
                                     blank=True, null=True, db_column='from_section', related_name='from_section')
    to_section = models.ForeignKey(Section_Info, on_delete=models.CASCADE,
                                     blank=True, null=True, db_column='to_section', related_name='to_section')
    
    comments=models.CharField(max_length=200, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_roll
class subject_mapping_teacher(models.Model):
    branch_code = models.CharField(max_length=10, null=True, blank=True)
    teacher_id = models.ForeignKey(Employee_Details, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='teacher_id', related_name='tea_teacher_idm')
    academic_year = models.ForeignKey(
        Academic_Year, on_delete=models.CASCADE, db_column='academic_year', related_name='tea_academic_yearm')
    class_id = models.ForeignKey(
        Academic_Class, on_delete=models.CASCADE, db_column='class_id', related_name='tea_class_idm')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE,
                                       null=True, blank=True, db_column='class_group_id', related_name='tea_class_group_idm')

    subject_id = models.ForeignKey(Subject_List, on_delete=models.CASCADE,
                                   blank=True, db_column='subject_id', related_name='cho_subject_idm')


class result_view_setting(models.Model):
    result_view_id = models.CharField(
        max_length=20, null=False, primary_key=True,blank=True)
    branch_code = models.CharField(max_length=10, null=True, blank=True)
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='academic_year', related_name='result_vs_academic_year')
    term_id = models.ForeignKey(Exam_Term, on_delete=models.CASCADE, null=True,
                                blank=True, db_column='term_id', related_name='result_vs_term_id')
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='class_id', related_name='result_vs_class_id')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE,
                                       null=True, blank=True, db_column='class_group_id', related_name='result_vs_class_group_id')
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE, null=True,
                                     blank=True, db_column='session_id', related_name='result_vs_session_id')
    
    subject_one_id = models.ForeignKey(Subject_List, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='subject_one_id', related_name='result_vs_subject_one_id')
    subject_one_share=models.IntegerField(blank=True,default=100)
        
    subject_two_id = models.ForeignKey(Subject_List, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='subject_two_id', related_name='result_vs_subject_two_id')
    subject_three_id = models.ForeignKey(Subject_List, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='subject_three_id', related_name='result_vs_subject_three_id')
    subject_two_share=models.IntegerField(blank=True,default=100)
    short_number=models.IntegerField(blank=True,default=0)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.result_view_id)

class subject_mark_with_marge(models.Model):
    result_view_id = models.ForeignKey(result_view_setting, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='result_view_id', related_name='result_marge_result_view_id')
    branch_code = models.CharField(max_length=10, null=True, blank=True)
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='academic_year', related_name='result_marge_academic_year')
    term_id = models.ForeignKey(Exam_Term, on_delete=models.CASCADE, null=True,
                                blank=True, db_column='term_id', related_name='result_marge_term_id')
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='class_id', related_name='result_marge_class_id')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE,
                                       null=True, blank=True, db_column='class_group_id', related_name='result_marge_class_group_id')
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE, null=True,
                                     blank=True, db_column='student_roll', related_name='result_marge_student_roll')
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE, null=True,
                                     blank=True, db_column='session_id', related_name='result_marge_session_id')
    total_exam_marks = models.DecimalField(
        max_digits=22, decimal_places=2, default=0, blank=True)
    obtain_marks = models.DecimalField(
        max_digits=22, decimal_places=2, default=0, blank=True)
    result_grade = models.CharField(max_length=20,null=True, blank=True)
    grade_point_average = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    is_optional=models.IntegerField(blank=True, default=0)
    out_of = models.DecimalField(max_digits=4, decimal_places=2, default=5, blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.student_roll)+" - "+ str(self.academic_year)+" - "+ str(self.obtain_marks)+" - "+ str(self.class_id)+" - "+ str(self.result_grade)
    
class Process_Status_History(models.Model):
    process_id = models.CharField(
        max_length=20, null=False, primary_key=True,blank=True)
    process_name = models.CharField(max_length=200, null=False, blank=True)
    status=models.CharField(
        max_length=20, null=True, choices=Process_Status, default='Start', blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    start_data_time = models.DateTimeField()
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.process_name)

class Term_Result_Marge(models.Model):
    branch_code = models.IntegerField(null=True, blank=True)
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='academic_year', related_name='trm_academic_year')
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='class_id', related_name='trm_class_id')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE,
                                       null=True, blank=True, db_column='class_group_id', related_name='trm_class_group_id')
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE, null=True,
                                     blank=True, db_column='student_roll', related_name='trm_student_roll')
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE, null=True,
                                     blank=True, db_column='session_id', related_name='trm_session_id')
    one_result_view_id = models.ForeignKey(result_view_setting, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='one_result_view_id', related_name='one_trm_result_view_id')
    one_term_id = models.ForeignKey(Exam_Term, on_delete=models.CASCADE, null=True,
                                blank=True, db_column='one_term_id', related_name='one_rtm_term_id')
    one_total_marks = models.DecimalField(
        max_digits=22, decimal_places=2, default=0, blank=True)
    one_obtain_marks = models.DecimalField(
        max_digits=22, decimal_places=2, default=0, blank=True)
    one_result_grade = models.CharField(max_length=20,null=True, blank=True)
    one_grade_point = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    
    two_result_view_id = models.ForeignKey(result_view_setting, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='two_result_view_id', related_name='two_trm_result_view_id')
    two_term_id = models.ForeignKey(Exam_Term, on_delete=models.CASCADE, null=True,
                                blank=True, db_column='two_term_id', related_name='two_rtm_term_id')
    two_total_marks = models.DecimalField(
        max_digits=22, decimal_places=2, default=0, blank=True)
    two_obtain_marks = models.DecimalField(
        max_digits=22, decimal_places=2, default=0, blank=True)
    two_result_grade = models.CharField(max_length=20,null=True, blank=True)
    two_grade_point = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    
    three_result_view_id = models.ForeignKey(result_view_setting, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='three_result_view_id', related_name='three_trm_result_view_id')
    three_term_id = models.ForeignKey(Exam_Term, on_delete=models.CASCADE, null=True,
                                blank=True, db_column='three_term_id', related_name='three_rtm_term_id')
    three_total_marks = models.DecimalField(
        max_digits=22, decimal_places=2, default=0, blank=True)
    three_obtain_marks = models.DecimalField(
        max_digits=22, decimal_places=2, default=0, blank=True)
    three_result_grade = models.CharField(max_length=20,null=True, blank=True)
    three_grade_point = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    
    total_marks = models.DecimalField(
        max_digits=22, decimal_places=2, default=0, blank=True)
    obtain_marks = models.DecimalField(
        max_digits=22, decimal_places=2, default=0, blank=True)
    result_grade = models.CharField(max_length=20,null=True, blank=True)
    grade_point = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)

    is_optional=models.IntegerField(blank=True, default=0)
    out_of = models.DecimalField(max_digits=4, decimal_places=2, default=5, blank=True)
    
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.one_term_id)+str(self.two_term_id)+str(self.academic_year)

class Term_Result_Marge_Final(models.Model):
    marge_tilte=models.CharField(max_length=200,null=True,blank=True)
    branch_code = models.IntegerField(null=True, blank=True)
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='academic_year', related_name='trmf_academic_year')
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='class_id', related_name='trmf_class_id')
    class_group_id = models.ForeignKey(Academic_Class_Group, on_delete=models.CASCADE,
                                       null=True, blank=True, db_column='class_group_id', related_name='trmf_class_group_id')
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE, null=True,
                                     blank=True, db_column='student_roll', related_name='trmf_student_roll')
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE, null=True,
                                     blank=True, db_column='session_id', related_name='trmf_session_id')
    one_term_id = models.ForeignKey(Exam_Term, on_delete=models.CASCADE, null=True,
                                blank=True, db_column='one_term_id', related_name='one_rtmf_term_id')
    one_total_marks = models.DecimalField(
        max_digits=22, decimal_places=2, default=0, blank=True)
    one_obtain_marks = models.DecimalField(
        max_digits=22, decimal_places=2, default=0, blank=True)
    one_result_grade = models.CharField(max_length=20,null=True, blank=True)
    one_grade_point = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    
    two_term_id = models.ForeignKey(Exam_Term, on_delete=models.CASCADE, null=True,
                                blank=True, db_column='two_term_id', related_name='two_rtmf_term_id')
    two_total_marks = models.DecimalField(
        max_digits=22, decimal_places=2, default=0, blank=True)
    two_obtain_marks = models.DecimalField(
        max_digits=22, decimal_places=2, default=0, blank=True)
    two_result_grade = models.CharField(max_length=20,null=True, blank=True)
    two_grade_point = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    
    three_term_id = models.ForeignKey(Exam_Term, on_delete=models.CASCADE, null=True,
                                blank=True, db_column='three_term_id', related_name='three_rtmf_term_id')
    three_total_marks = models.DecimalField(
        max_digits=22, decimal_places=2, default=0, blank=True)
    three_obtain_marks = models.DecimalField(
        max_digits=22, decimal_places=2, default=0, blank=True)
    three_result_grade = models.CharField(max_length=20,null=True, blank=True)
    three_grade_point = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    
    total_marks = models.DecimalField(
        max_digits=22, decimal_places=2, default=0, blank=True)
    obtain_marks = models.DecimalField(
        max_digits=22, decimal_places=2, default=0, blank=True)
    result_grade = models.CharField(max_length=20,null=True, blank=True)
    grade_point = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    grade_point_without_furth = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    merit_position = IntegerField(null=True, blank=True) 
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.one_term_id)+str(self.two_term_id)+str(self.academic_year)

class Result_Position_Temp(models.Model):
    branch_code = models.IntegerField(null=True, blank=True)
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE, null=True,
                                     blank=True, db_column='student_roll', related_name='rpt_student_roll')
    class_roll= models.IntegerField(default=0)
    subject_1 = models.DecimalField(max_digits=22, decimal_places=2, default=0, blank=True)
    subject_2 = models.DecimalField(max_digits=22, decimal_places=2, default=0, blank=True)
    subject_3 = models.DecimalField(max_digits=22, decimal_places=2, default=0, blank=True)
    subject_4 = models.DecimalField(max_digits=22, decimal_places=2, default=0, blank=True)
    subject_5 = models.DecimalField(max_digits=22, decimal_places=2, default=0, blank=True)
    subject_6 = models.DecimalField(max_digits=22, decimal_places=2, default=0, blank=True)
    subject_7 = models.DecimalField(max_digits=22, decimal_places=2, default=0, blank=True)
    subject_8 = models.DecimalField(max_digits=22, decimal_places=2, default=0, blank=True)
    subject_9 = models.DecimalField(max_digits=22, decimal_places=2, default=0, blank=True)
    subject_10 = models.DecimalField(max_digits=22, decimal_places=2, default=0, blank=True)
    subject_11 = models.DecimalField(max_digits=22, decimal_places=2, default=0, blank=True)
    subject_12 = models.DecimalField(max_digits=22, decimal_places=2, default=0, blank=True)
    subject_13 = models.DecimalField(max_digits=22, decimal_places=2, default=0, blank=True)
    subject_14 = models.DecimalField(max_digits=22, decimal_places=2, default=0, blank=True)

    total_marks = models.DecimalField(
        max_digits=22, decimal_places=2, default=0, blank=True)
    obtain_marks = models.DecimalField(
        max_digits=22, decimal_places=2, default=0, blank=True)
    result_grade = models.CharField(max_length=20,null=True, blank=True)
    grade_point = models.DecimalField(
        max_digits=22, decimal_places=2, null=True, blank=True)
    temp_position = IntegerField(null=True, blank=True, default=0)
    merit_position = IntegerField(null=True, blank=True, default=0)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.student_roll)

class Certificat_Header_Address(models.Model):
    branch_code = models.IntegerField(blank=True, null=True)
    academic_name=models.CharField(max_length=200)
    logo = models.ImageField(upload_to="logo/", null=True, blank=True)
    sing = models.ImageField(upload_to="sing/", null=True, blank=True)
    address=models.TextField(blank=True, null=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.academic_name)

class Testimonial(models.Model):
    branch_code = models.IntegerField(blank=True, null=True)
    testmonial_id=models.CharField(max_length=200,primary_key=True)
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE, null=True,blank=True, db_column='student_roll', related_name='testi_student_roll')
    education_board_id = models.ForeignKey(Education_Board, on_delete=models.CASCADE, null=True,blank=True, db_column='education_board_id', related_name='testi_education_board_id')
    cert_name_id = models.ForeignKey(Certificat_Name, on_delete=models.CASCADE, null=True,blank=True, db_column='cert_name_id', related_name='testi_cert_name_id')
    board_roll= models.CharField(max_length=20,null=True, blank=True)
    board_reg= models.CharField(max_length=20,null=True, blank=True)
    academic_year = models.IntegerField()
    group_name = models.CharField(max_length=50,null=True, blank=True)
    grade_name = models.CharField(max_length=10,null=True, blank=True)
    grade_point = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.student_roll)


