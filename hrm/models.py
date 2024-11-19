from django.db import models
from appauth.models import Loc_Country, Loc_Division, Loc_District, Loc_Upazila, Branch

# Create your models here.

from appauth.models import STATUS_LIST, BLOOD_GROUP, GENDER_LIST, RELIGION_LIST, MARITAL_STATUS


class Company_Information(models.Model):
    company_id = models.CharField(
        max_length=20, null=False, blank=True, primary_key=True)
    company_name = models.CharField(max_length=200, null=False)
    country_id = models.ForeignKey(Loc_Country, on_delete=models.PROTECT, blank=True,
                                   null=True, related_name='com_country_id', db_column='country_id')
    division_id = models.ForeignKey(Loc_Division, on_delete=models.PROTECT, blank=True,
                                    null=True, related_name='com_division_id', db_column='division_id')
    district_id = models.ForeignKey(Loc_District, on_delete=models.PROTECT, blank=True,
                                    null=True, related_name='com_district_id', db_column='district_id')
    upozila_id = models.ForeignKey(Loc_Upazila, on_delete=models.PROTECT, blank=True,
                                   null=True, related_name='com_upozila_id', db_column='upozila_id')
    office_address = models.CharField(max_length=200, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name


class Company_Office(models.Model):
    office_id = models.CharField(
        max_length=20, null=False, blank=True, primary_key=True)
    office_name = models.CharField(max_length=200, null=False)
    country_id = models.ForeignKey(Loc_Country, on_delete=models.PROTECT, blank=True,
                                   null=True, related_name='cof_country_id', db_column='country_id')
    division_id = models.ForeignKey(Loc_Division, on_delete=models.PROTECT, blank=True,
                                    null=True, related_name='cof_division_id', db_column='division_id')
    district_id = models.ForeignKey(Loc_District, on_delete=models.PROTECT, blank=True,
                                    null=True, related_name='cof_district_id', db_column='district_id')
    upozila_id = models.ForeignKey(Loc_Upazila, on_delete=models.PROTECT, blank=True,
                                   null=True, related_name='cof_upozila_id', db_column='upozila_id')
    office_address = models.CharField(max_length=200, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.office_name


class Department_Info(models.Model):
    department_id = models.CharField(
        max_length=20, null=False, blank=True, primary_key=True)
    department_name = models.CharField(max_length=200, null=False)
    total_employee = models.IntegerField(null=True)
    department_location = models.CharField(max_length=200, null=False)
    department_incharge = models.CharField(max_length=200, null=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.department_name


class Shift_Info(models.Model):
    shift_id = models.CharField(
        max_length=20, null=False, blank=True, primary_key=True)
    shift_name = models.CharField(max_length=200, null=False)
    office_id = models.ForeignKey(Company_Office, on_delete=models.PROTECT,
                                  blank=True, null=True, related_name='shi_office_id', db_column='office_id')
    total_work_minute = models.IntegerField(null=True)
    work_start_time_sec = models.IntegerField(null=True)
    work_end_time_sec = models.IntegerField(null=True)
    work_start_grace_time_sec = models.IntegerField(null=True)
    work_end_time_grace_sec = models.IntegerField(null=True)
    refresh_start_time_sec = models.IntegerField(null=True)
    refresh_end_time_sec = models.IntegerField(null=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shift_name

# Not Required


class Shift_Info_Hist(models.Model):
    shift_id = models.ForeignKey(Shift_Info, on_delete=models.PROTECT, blank=True,
                                 null=True, related_name='shi_shift_id', db_column='shift_id')
    shift_name = models.CharField(max_length=200, null=False)
    shift_effect_date = models.DateField()
    office_id = models.CharField(max_length=13, null=False)
    total_work_minute = models.IntegerField(null=True)
    work_start_time_sec = models.IntegerField(null=True)
    work_end_time_sec = models.IntegerField(null=True)
    work_start_grace_time_sec = models.IntegerField(null=True)
    work_end_time_grace_sec = models.IntegerField(null=True)
    refresh_start_time_sec = models.IntegerField(null=True)
    refresh_end_time_sec = models.IntegerField(null=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shift_name


class Education_Degree(models.Model):
    degree_id = models.CharField(
        max_length=20, null=False, blank=True, primary_key=True)
    degree_name = models.CharField(max_length=200, null=False)
    degree_duration = models.CharField(max_length=200, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.degree_name


class Employee_Designation(models.Model):
    desig_id = models.CharField(max_length=20, null=False, primary_key=True)
    desig_name = models.CharField(
        max_length=200, null=False, blank=False, unique=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.desig_name


class Employment_Type(models.Model):
    emptype_id = models.CharField(max_length=20, null=False, primary_key=True)
    emptype_name = models.CharField(
        max_length=200, blank=False, null=False, unique=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.emptype_name


class Salary_Scale(models.Model):
    salscale_id = models.CharField(max_length=20, primary_key=True)
    salscale_name = models.CharField(max_length=200, null=False)
    total_salary = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    deduction_pct = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    total_deduction = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    effective_date = models.DateField(null=True, blank=True)
    comments = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.salscale_name


class Salary_Scale_Hist(models.Model):
    salscale_id = models.CharField(max_length=20)
    salscale_name = models.CharField(max_length=200, null=False)
    total_salary = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    deduction_pct = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    total_deduction = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    effective_date = models.DateField(null=True, blank=True)
    day_serial = models.IntegerField()
    comments = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.salscale_name


class Salary_Scale_Details(models.Model):
    salsdtlcale_id = models.CharField(
        max_length=20, null=False, primary_key=True)
    salscale_id = models.ForeignKey(Salary_Scale, on_delete=models.PROTECT, blank=True,
                                    null=True, related_name='scd_salscale_id', db_column='salscale_id')
    salsdtlcale_name = models.CharField(max_length=200, null=False)
    salary_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    deduction_pct = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    total_deduction = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    effective_date = models.DateField(null=True, blank=True)
    comments = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.salsdtlcale_name


class Salary_Scale_Details_Hist(models.Model):
    salsdtlcale_id = models.CharField(
        max_length=20, null=False)
    salscale_id = models.ForeignKey(Salary_Scale, on_delete=models.PROTECT, blank=True,
                                    null=True, related_name='scd_salscale_id1', db_column='salscale_id')
    salsdtlcale_name = models.CharField(max_length=200)
    salary_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    deduction_pct = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    total_deduction = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    effective_date = models.DateField(null=True, blank=True)
    day_serial = models.IntegerField()
    comments = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.salsdtlcale_name


class Salary_Scale_Bonous(models.Model):
    salscale_id = models.ForeignKey(Salary_Scale, on_delete=models.PROTECT, blank=True,
                                    null=True, related_name='scb_salscale_id2', db_column='salscale_id')
    salsdtlcale_id = models.ForeignKey(Salary_Scale_Details, on_delete=models.PROTECT, blank=True,
                                       null=True, related_name='scb_salsdtlcale_id', db_column='salsdtlcale_id')
    bonus_id = models.CharField(max_length=20, null=False, primary_key=True)
    bonus_name = models.CharField(max_length=200, null=False)
    bonus_pct = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    bonus_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    effective_date = models.DateField(null=True, blank=True)
    comments = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.bonus_name


class Salary_Scale_Bonous_Hist(models.Model):
    salscale_id = models.ForeignKey(Salary_Scale, on_delete=models.PROTECT, blank=True,
                                    null=True, related_name='scbh_salscale_id', db_column='salscale_id')
    salsdtlcale_id = models.ForeignKey(Salary_Scale_Details, on_delete=models.PROTECT, blank=True,
                                       null=True, related_name='scbh_salsdtlcale_id', db_column='salsdtlcale_id')
    bonus_id = models.CharField(max_length=20, null=False)
    bonus_name = models.CharField(max_length=200, null=False)
    bonus_pct = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    bonus_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    effective_date = models.DateField(null=True, blank=True)
    day_serial = models.IntegerField(null=True, blank=True)
    comments = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.bonus_name


class Salary_Scale_Deduction(models.Model):
    salded_id = models.CharField(
        max_length=20, null=False, primary_key=True)
    salscale_id = models.ForeignKey(Salary_Scale, on_delete=models.PROTECT, blank=True,
                                    null=True, related_name='scdn_salscale_id', db_column='salscale_id')
    salsdtlcale_id = models.ForeignKey(Salary_Scale_Details, on_delete=models.PROTECT, blank=True,
                                       null=True, related_name='scdn_salsdtlcale_id', db_column='salsdtlcale_id')
    deduction_pct = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    total_deduction = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    effective_date = models.DateField(null=True, blank=True)
    comments = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.salsdtlcale_id


class Salary_Scale_Deduction_Hist(models.Model):
    salded_id = models.CharField(
        max_length=20, null=False)
    salscale_id = models.ForeignKey(Salary_Scale, on_delete=models.PROTECT, blank=True,
                                    null=True, related_name='scdnh_salscale_id', db_column='salscale_id')
    salsdtlcale_id = models.ForeignKey(Salary_Scale_Details, on_delete=models.PROTECT, blank=True,
                                       null=True, related_name='scdnh_salsdtlcale_id', db_column='salsdtlcale_id')
    deduction_pct = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    total_deduction = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    effective_date = models.DateField(null=True, blank=True)
    day_serial = models.IntegerField(null=True, blank=True)
    comments = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.salsdtlcale_id


class Extra_Allowance(models.Model):
    allowance_id = models.CharField(
        max_length=20, blank=True, null=False, primary_key=True)
    allowance_name = models.CharField(max_length=200, null=False)
    allowance_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    comments = models.CharField(max_length=200, blank=True, null=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.allowance_name


class Bank_Info(models.Model):
    bank_id = models.CharField(max_length=20, primary_key=True)
    bank_name = models.CharField(max_length=200, null=False)
    bank_address = models.CharField(max_length=200, null=False)
    bank_phone = models.CharField(max_length=200, null=False)
    bank_email = models.CharField(max_length=200, null=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.bank_name


class Employee_Details(models.Model):
    employee_id = models.CharField(
        max_length=20, default='', blank=True, primary_key=True)
    employee_name = models.CharField(max_length=200)
    employee_father_name = models.CharField(max_length=200, blank=True)
    employee_mother_name = models.CharField(max_length=200, blank=True)
    serial = models.IntegerField(default=999)
    employee_blood_group = models.CharField(
        max_length=5, default='', choices=BLOOD_GROUP, blank=True)
    employee_sex = models.CharField(
        max_length=5, null=True, choices=GENDER_LIST, default='')
    employee_religion = models.CharField(
        max_length=5, default='', choices=RELIGION_LIST, blank=True)
    profile_image = models.ImageField(
        blank=True, null=True, upload_to='employee/profile/')
    employee_signature = models.ImageField(
        blank=True, null=True, upload_to='employee/signature/')
    employee_marital_status = models.CharField(
        max_length=5, null=True, default='', choices=MARITAL_STATUS, blank=True)  # choices=marital_status,
    employee_national_id = models.CharField(max_length=200, null=True)
    country_id = models.ForeignKey(Loc_Country, on_delete=models.PROTECT, blank=True,
                                   null=True, related_name='emp_country_id', db_column='country_id')
    division_id = models.ForeignKey(Loc_Division, on_delete=models.PROTECT, blank=True,
                                    null=True, related_name='emp_division_id', db_column='division_id')
    district_id = models.ForeignKey(Loc_District, on_delete=models.PROTECT, blank=True,
                                    null=True, related_name='emp_district_id', db_column='district_id')
    upozila_id = models.ForeignKey(Loc_Upazila, on_delete=models.PROTECT, blank=True,
                                   null=True, related_name='emp_upozila_id', db_column='upozila_id')
    employee_present_address = models.TextField(null=True, blank=True)
    employee_permanent_address = models.TextField(null=True, blank=True)
    employee_phone_own = models.CharField(max_length=15, null=True)
    employee_phone_office = models.CharField(
        max_length=15, null=True, blank=True)
    employee_phone_home = models.CharField(
        max_length=15, null=True, blank=True)
    passport_no = models.CharField(max_length=15, null=True, blank=True)
    driving_licence = models.CharField(max_length=15, null=True, blank=True)
    employee_tin = models.CharField(max_length=15, null=True, blank=True)
    employee_phone_home = models.CharField(
        max_length=15, null=True, blank=True)
    email_personal = models.CharField(max_length=30, null=True, blank=True)
    employee_joining_date = models.DateField(null=True, blank=True)
    employee_date_of_birth = models.DateField(null=True, blank=True)
    employee_status = models.CharField(
        max_length=5, null=True, choices=STATUS_LIST, default='A', blank=True)
    eme_contact_name = models.CharField(max_length=100, null=True, blank=True)
    eme_contact_relation = models.CharField(
        max_length=100, null=True, blank=True)
    eme_contact_phone = models.CharField(max_length=15, null=True, blank=True)
    eme_contact_address = models.CharField(
        max_length=100, null=True, blank=True)
    office_id = models.CharField(max_length=13, null=False)
    emptype_id = models.ForeignKey(Employment_Type, on_delete=models.PROTECT,
                                   blank=True, null=True, related_name='emp_emptype_id', db_column='emptype_id')
    salscale = models.ForeignKey(
        Salary_Scale, on_delete=models.PROTECT, blank=True, null=True)
    designation_id = models.ForeignKey(Employee_Designation, on_delete=models.PROTECT,
                                       blank=True, null=True, related_name='emp_designation_id', db_column='designation_id')
    email_official = models.CharField(max_length=30, null=True, blank=True)
    reporting_to = models.CharField(max_length=30, null=True, blank=True)
    current_shift = models.ForeignKey(Shift_Info, on_delete=models.PROTECT, blank=True,
                                      null=True, related_name='emp_current_shift', db_column='current_shift')
    office_location = models.ForeignKey(Company_Office, on_delete=models.PROTECT, blank=True,
                                        null=True, related_name='emp_office_location', db_column='office_location')
    card_number = models.CharField(max_length=100, null=True, blank=True)
    salary_bank = models.ForeignKey(Bank_Info, on_delete=models.PROTECT, blank=True,
                                    null=True, related_name='emp_salary_bank', db_column='salary_bank')
    salary_bank_ac = models.CharField(max_length=20, null=True, blank=True)
    contract_start_date = models.DateField(null=True, blank=True)
    contract_exp_date = models.DateField(null=True, blank=True)
    last_inc_date = models.DateField(null=True, blank=True)
    next_inc_date = models.DateField(null=True, blank=True)
    service_end_date = models.DateField(null=True, blank=True)
    last_transfer_date = models.DateField(null=True, blank=True)
    next_transfer_date = models.DateField(null=True, blank=True)
    job_confirm_date = models.DateField(null=True, blank=True)
    pf_confirm_date = models.DateField(null=True, blank=True)
    gf_confirm_date = models.DateField(null=True, blank=True)
    wf_confirm_date = models.DateField(null=True, blank=True)
    last_promotion_date = models.DateField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.employee_name

    def emp_filter(self):
        emp_filter = self.order_by(self.app_data_time).desc()
        return emp_filter


class Image_temp_emp(models.Model):
    image_1 = models.ImageField(blank=True, null=True, upload_to='temp/')
    image_2 = models.ImageField(blank=True, null=True, upload_to='temp/')
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Employee_Education(models.Model):
    employee_id = models.ForeignKey(Employee_Details, on_delete=models.PROTECT,
                                    blank=True, null=True, related_name='eme_employee_id', db_column='employee_id')
    serial_no = models.CharField(max_length=20, null=True, blank=True)
    degree_name = models.CharField(max_length=100, null=True, blank=True)
    board_name = models.CharField(max_length=200, null=True, blank=True)
    result_point = models.CharField(max_length=100, null=True, blank=True)
    result_grate = models.CharField(max_length=100, null=True, blank=True)
    passing_year = models.CharField(max_length=500, null=True, blank=True)
    institute_name = models.CharField(max_length=100, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.degree_name)


class Employee_Experience(models.Model):
    employee_id = models.ForeignKey(Employee_Details, on_delete=models.PROTECT,
                                    blank=True, null=True, related_name='exp_employee_id', db_column='employee_id')
    serial_no = models.CharField(max_length=20, null=True, blank=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    company_address = models.CharField(max_length=500, blank=True, null=True)
    company_type = models.CharField(max_length=200, null=True, blank=True)
    position = models.CharField(max_length=200, null=True, blank=True)
    department = models.CharField(max_length=200, null=True, blank=True)
    responsibility = models.CharField(max_length=800, null=True, blank=True)
    achievement = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    contact_person = models.CharField(max_length=200, null=True, blank=True)
    emp_id = models.CharField(max_length=200, null=True, blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    app_user_id = models.CharField(max_length=20, blank=True, null=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Employee_Nominee(models.Model):
    employee_id = models.ForeignKey(Employee_Details, on_delete=models.PROTECT,
                                    blank=True, null=True, related_name='eno_employee_id', db_column='employee_id')
    nominee_serial = models.CharField(max_length=20, null=True, blank=True)
    nominee_name = models.CharField(max_length=100, null=False)
    nominee_sex = models.CharField(
        max_length=20, choices=GENDER_LIST, null=False)
    nominee_father_name = models.CharField(max_length=100, null=False)
    nominee_mother_name = models.CharField(max_length=20, null=False)
    nominee_present_addr = models.CharField(max_length=300, null=False)
    nominee_permanent_addr = models.CharField(max_length=300, null=False)
    nominee_birth_date = models.DateField(null=True, blank=True)
    country_id = models.CharField(max_length=13, null=True, blank=True)
    nominee_nid_num = models.CharField(max_length=20, null=False)
    nominee_religion = models.CharField(
        max_length=20, choices=RELIGION_LIST, null=False)
    nominee_blood_group = models.CharField(
        max_length=4, default='', choices=BLOOD_GROUP, blank=True)
    nominee_mobile_num = models.CharField(max_length=20, null=False)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nominee_name


class Employee_Scale(models.Model):
    employee_id = models.ForeignKey(Employee_Details, on_delete=models.PROTECT,
                                    blank=True, null=True, related_name='ems_employee_id1', db_column='employee_id')
    salscale_id = models.ForeignKey(Salary_Scale, on_delete=models.PROTECT, blank=True,
                                    null=True, related_name='ems_salscale_id1', db_column='salscale_id')
    effective_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.employee_id


class Employee_Scale_Hist(models.Model):
    employee_id = models.ForeignKey(Employee_Details, on_delete=models.PROTECT,
                                    blank=True, null=True, related_name='ems_employee_id2', db_column='employee_id')
    salscale_id = models.ForeignKey(Salary_Scale, on_delete=models.PROTECT, blank=True,
                                    null=True, related_name='ems_salscale_id2', db_column='salscale_id')
    effective_date = models.DateField(null=True, blank=True)
    day_serial = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.employee_id


class Employee_Scale_Details(models.Model):
    employee_id = models.ForeignKey(Employee_Details, on_delete=models.PROTECT,
                                    blank=True, null=True, related_name='ems_employee_id3', db_column='employee_id')
    salsdtlcale_id = models.ForeignKey(Salary_Scale_Details, on_delete=models.PROTECT, blank=True,
                                       null=True, related_name='ems_salsdtlcale_id3', db_column='salsdtlcale_id')
    salary_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    effective_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.employee_id)


class Employee_Scale_Details_Hist(models.Model):
    employee_id = models.ForeignKey(Employee_Details, on_delete=models.PROTECT,
                                    blank=True, null=True, related_name='ems_employee_id4', db_column='employee_id')
    salsdtlcale_id = models.ForeignKey(Salary_Scale_Details, on_delete=models.PROTECT, blank=True,
                                       null=True, related_name='ems_salsdtlcale_id4', db_column='salsdtlcale_id')
    salary_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    effective_date = models.DateField(null=True, blank=True)
    day_serial = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.employee_id)


class Employee_Bonous(models.Model):
    employee_id = models.ForeignKey(Employee_Details, on_delete=models.PROTECT,
                                    blank=True, null=True, related_name='ems_employee_id5', db_column='employee_id')
    bonus_id = models.ForeignKey(Salary_Scale_Bonous, on_delete=models.PROTECT, blank=True,
                                 null=True, related_name='ems_bonus_id5', db_column='bonus_id')
    bonus_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    effective_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.employee_id)


class Employee_Bonous_Hist(models.Model):
    employee_id = models.ForeignKey(Employee_Details, on_delete=models.PROTECT,
                                    blank=True, null=True, related_name='ems_employee_id6', db_column='employee_id')
    bonus_id = models.ForeignKey(Salary_Scale_Bonous, on_delete=models.PROTECT, blank=True,
                                 null=True, related_name='ems_bonus_id6', db_column='bonus_id')
    bonus_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    effective_date = models.DateField(null=True, blank=True)
    day_serial = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.employee_id)


class Employee_Deduction(models.Model):
    employee_id = models.ForeignKey(Employee_Details, on_delete=models.PROTECT,
                                    blank=True, null=True, related_name='ems_employee_id7', db_column='employee_id')
    salded_id = models.ForeignKey(Salary_Scale_Deduction, on_delete=models.PROTECT, blank=True,
                                  null=True, related_name='ems_salded_id7', db_column='salded_id')
    deduction_pct = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    total_deduction = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    effective_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.employee_id)


class Employee_Deduction_Hist(models.Model):
    employee_id = models.ForeignKey(Employee_Details, on_delete=models.PROTECT,
                                    blank=True, null=True, related_name='ems_employee_id8', db_column='employee_id')
    salded_id = models.ForeignKey(Salary_Scale_Deduction, on_delete=models.PROTECT, blank=True,
                                  null=True, related_name='ems_salded_id8', db_column='salded_id')
    deduction_pct = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    total_deduction = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    effective_date = models.DateField(null=True, blank=True)
    day_serial = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.employee_id)


class Employee_Document_Type(models.Model):
    document_type_id = models.CharField(
        max_length=20, default='', blank=True, primary_key=True)
    document_type_name = models.CharField(max_length=200, default='')
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.document_type_name


class Employee_Document(models.Model):
    employee_id = models.ForeignKey(Employee_Details, on_delete=models.PROTECT,
                                    blank=True, null=True, related_name='doc_employee_id', db_column='employee_id')
    document_type = models.ForeignKey(Employee_Document_Type, on_delete=models.PROTECT,
                                      blank=True, null=True, related_name='doc_document_type', db_column='document_type')
    document_location = models.ImageField(
        upload_to='sign_image/', blank=True, null=True)
    file_no = models.CharField(max_length=20, default='', blank=True)
    status = models.CharField(max_length=2, null=True,
                              choices=STATUS_LIST, default='A', blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Leave_Info(models.Model):
    leave_id = models.CharField(
        max_length=20, default='', blank=True, primary_key=True)
    leave_name = models.CharField(max_length=200, default='')
    total_leave = models.IntegerField(null=True)
    forward_leave = models.IntegerField(null=True)
    holiday_check = models.BooleanField(default=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.leave_name


class Leave_Application(models.Model):
    leave_id = models.ForeignKey(Leave_Info, on_delete=models.PROTECT, blank=True,
                                 null=True, related_name='lva_leave_id', db_column='leave_id')
    employee_id = models.ForeignKey(Employee_Details, on_delete=models.PROTECT,
                                    blank=True, null=True, related_name='lva_employee_id', db_column='employee_id')
    application_date = models.DateField(
        auto_now_add=True, null=True, blank=True)
    from_date = models.DateField(null=True, blank=True)
    upto_date = models.DateField(null=True, blank=True)
    join_date = models.DateField(null=True, blank=True)
    approval_status = models.CharField(
        max_length=10, default='Panding', blank=True, null=True)
    leave_reason = models.CharField(
        max_length=200, default='', blank=True, null=True)
    application_to = models.ForeignKey(Employee_Details, on_delete=models.PROTECT, blank=True,
                                       null=True, related_name='lva_application_to', db_column='application_to')
    approve_by = models.ForeignKey(Employee_Details, on_delete=models.PROTECT,
                                   blank=True, null=True, related_name='lva_approve_by', db_column='approve_by')
    approval_comments = models.CharField(
        max_length=200, default='', blank=True, null=True)
    reject_by = models.ForeignKey(Employee_Details, on_delete=models.PROTECT,
                                  blank=True, null=True, related_name='lva_reject_by', db_column='reject_by')
    reject_comments = models.CharField(
        max_length=200, default='', blank=True, null=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.employee_id)

# Not Required


class Attendance_Log(models.Model):
    employee_id = models.ForeignKey(Employee_Details, on_delete=models.PROTECT,
                                    blank=True, null=True, related_name='att_employee_id', db_column='employee_id')
    shift = models.ForeignKey(
        Shift_Info, on_delete=models.PROTECT, blank=True, null=True)
    attendance_date = models.DateField(null=True, blank=True)
    in_time = models.DateTimeField(blank=True, null=True)
    out_time = models.DateTimeField(blank=True, null=True)
    total_work_minute = models.IntegerField(null=True)
    work_start_time_sec = models.IntegerField(null=True)
    work_end_time_sec = models.IntegerField(null=True)
    work_start_grace_time_sec = models.IntegerField(null=True)
    work_end_time_grace_sec = models.IntegerField(null=True)
    refresh_start_time_sec = models.IntegerField(null=True)
    refresh_end_time_sec = models.IntegerField(null=True)
    is_late_entry = models.BooleanField(default=False, blank=True, null=True)
    is_early_exit = models.BooleanField(default=False, blank=True, null=True)
    late_entry_approve = models.ForeignKey(Employee_Details, on_delete=models.PROTECT, blank=True,
                                           null=True, related_name='att_late_entry_approve', db_column='late_entry_approve')
    late_entry_reason = models.CharField(
        max_length=200, default='', blank=True, null=True)
    early_exit_approve = models.ForeignKey(Employee_Details, on_delete=models.PROTECT, blank=True,
                                           null=True, related_name='att_early_exit_approve', db_column='early_exit_approve')
    early_exit_reason = models.CharField(
        max_length=200, default='', blank=True, null=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.attendance_date+" "+str(self.employee_id)

# Not Required


class Attendance_Schedule(models.Model):
    schedule_id = models.CharField(
        max_length=20, default='', blank=True, primary_key=True)
    employee_id = models.ForeignKey(Employee_Details, on_delete=models.PROTECT,
                                    blank=True, null=True, related_name='sch_employee', db_column='employee_id')
    shift_id = models.ForeignKey(Shift_Info, on_delete=models.PROTECT, blank=True,
                                 null=True, related_name='att_sch_shift', db_column='shift_id')
    schedule_date = models.DateField()
    schedule_description = models.CharField(max_length=500)
    start_date = models.DateField()
    end_date = models.DateField()
    schedule_status = models.CharField(
        max_length=2, null=True, choices=STATUS_LIST, default='A', blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.schedule_description

# Not Required


class Attendance_Card_Log(models.Model):
    employee_id = models.ForeignKey(Employee_Details, on_delete=models.PROTECT,
                                    blank=True, null=True, related_name='att_employee', db_column='employee_id')
    shift_id = models.ForeignKey(Shift_Info, on_delete=models.PROTECT, blank=True,
                                 null=True, related_name='att_card_shift', db_column='shift_id')
    log_time = models.DateTimeField(blank=True, null=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.employee_id


class Employee_Training(models.Model):
    employee_id = models.ForeignKey(Employee_Details, on_delete=models.PROTECT,
                                    blank=True, null=True, related_name='trn_employee', db_column='employee_id')
    schedule_id = models.ForeignKey(Attendance_Schedule, on_delete=models.PROTECT,
                                    blank=True, null=True, related_name='trn_schedule', db_column='schedule_id')
    institute_name = models.CharField(max_length=200, blank=True, null=True)
    training_name = models.CharField(max_length=200, blank=True, null=True)
    training_description = models.CharField(
        max_length=200, blank=True, null=True)
    from_date = models.DateField(null=True, blank=True)
    upto_date = models.DateField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Pay_Bill(models.Model):
    bill_id = models.CharField(
        max_length=20, default='', blank=True, primary_key=True)
    bill_date = models.DateField(null=True, blank=True)
    bill_comments = models.CharField(max_length=200, null=False)
    bill_doc_detail = models.CharField(max_length=200, null=False)
    bill_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    approval_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    prepare_by = models.ForeignKey(Employee_Details, on_delete=models.PROTECT,
                                   blank=True, null=True, related_name='bill_prepare_by', db_column='prepare_by')
    checked_by = models.ForeignKey(Employee_Details, on_delete=models.PROTECT,
                                   blank=True, null=True, related_name='bill_checked_by', db_column='checked_by')
    approve_by = models.ForeignKey(Employee_Details, on_delete=models.PROTECT,
                                   blank=True, null=True, related_name='bill_approve_by', db_column='approve_by')
    checked_status = models.BooleanField(default=False, blank=True, null=True)
    approve_status = models.BooleanField(default=False, blank=True, null=True)
    checked_date = models.DateField(null=True, blank=True)
    approve_date = models.DateField(null=True, blank=True)
    attached_file = models.ImageField(upload_to='bill_image/')
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)
