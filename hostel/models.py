from datetime import date
from django.db import models
from django.db.models.fields import DateTimeField
from appauth.models import Loc_Country, Loc_Division, Loc_District, Loc_Upazila, Branch
# Create your models here.
from appauth.models import STATUS_LIST
from edu.models import Condition_List, Status_Type_list, Month_List, Students_Info, Academic_Year, Fees_Head_Settings

FEE_PAY_FRQ_LIST = (
    ('', 'Choose...'),
    ('D', 'Daily'),
    ('W', 'Weekly'),
    ('M', 'Monthly'),
    ('Q', 'Quarterly'),
    ('H', 'Half Yearly'),
    ('Y', 'Yearly'),
)


class Application_Settings(models.Model):
    hostel_admission_fee_gl = models.CharField(max_length=13, null=False)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.hostel_admission_fee_gl


class Hall_details(models.Model):
    hall_code = models.CharField(max_length=13, null=False, primary_key=True)
    hall_name = models.CharField(max_length=200, null=False)
    hall_address = models.CharField(max_length=200, null=False, blank=True)
    hall_supervisor = models.CharField(max_length=200, null=False, blank=True)
    supervisor_phone = models.CharField(max_length=200, null=False, blank=True)
    total_seat = models.IntegerField(null=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.hall_name)

class Bed_Type(models.Model):
    bed_type_id = models.CharField(max_length=30, blank=True, primary_key=True)
    bed_type_name = models.CharField(max_length=200, blank=False)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    delete_by = models.CharField(max_length=20, null=False, blank=True)
    delete_on = models.DateTimeField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.bed_type_name


class PayFor_Types(models.Model):
    pay_for_id = models.CharField(max_length=30, blank=True, primary_key=True)
    pay_for_name = models.CharField(max_length=200, blank=False)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    delete_by = models.CharField(max_length=20, null=False, blank=True)
    delete_on = models.DateTimeField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pay_for_name


class Beds_Management(models.Model):
    beds_management_id = models.CharField(
        max_length=30, blank=True, primary_key=True)
    bed_name = models.CharField(max_length=30, blank=False, null=False)
    bed_price = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    bed_type_id = models.ForeignKey(Bed_Type, on_delete=models.CASCADE, null=True,
                                    blank=True, db_column='bed_type_id', related_name='bed_beds_type_id')
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    delete_by = models.CharField(max_length=20, null=False, blank=True)
    delete_on = models.DateTimeField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.bed_name


class Rooms_Management(models.Model):
    rooms_management_id = models.CharField(
        max_length=30, blank=True, primary_key=True)
    room_name_or_number = models.CharField(max_length=30, blank=False)
    room_size = models.IntegerField(blank=True, null=True)
    room_rent = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    bed_rent = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    no_of_bed = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    delete_by = models.CharField(max_length=20, null=False, blank=True)
    delete_on = models.DateTimeField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room_name_or_number


class Meal_Type(models.Model):
    meal_type_id = models.CharField(
        max_length=200, blank=True, primary_key=True)
    meal_type_name = models.CharField(max_length=200, blank=False)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    delete_by = models.CharField(max_length=20, null=False, blank=True)
    delete_on = models.DateTimeField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.meal_type_name


class Meal(models.Model):
    meal_id = models.CharField(max_length=200, primary_key=True, blank=True)
    meal_type_id = models.ForeignKey(Meal_Type, on_delete=models.CASCADE, null=True,
                                     blank=True, db_column='meal_type_id', related_name='meal_meal_type_id')
    meal_name = models.CharField(max_length=200, blank=False)
    meal_price = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    delete_by = models.CharField(max_length=20, null=False, blank=True)
    delete_on = models.DateTimeField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.meal_name


class Payment_Management(models.Model):
    payment_management_id = models.CharField(
        max_length=30, blank=True, primary_key=True)
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='academic_year', related_name='pay_academic_year')
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE, null=True,
                                     blank=True, db_column='student_roll', related_name='pay_student_roll')
    month_name = models.IntegerField(
        choices=Month_List, default=1, blank=False)
    payment_date = models.DateField(null=True, blank=True)
    pay_for_id = models.ForeignKey(PayFor_Types, on_delete=models.CASCADE, null=True,
                                   blank=True, db_column='pay_for_id', related_name='pay_pay_for_id')
    payment = models.CharField(max_length=20, null=False, blank=False)
    due = models.CharField(max_length=20, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Hostel_Admit(models.Model):
    branch_code = models.IntegerField(blank=True, null=True)
    admit_id = models.CharField(max_length=30, blank=True, primary_key=True)
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='academic_year', related_name='admit_academic_year')
    admit_date = models.DateField(null=True, blank=True)
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE, null=True,
                                     blank=True, db_column='student_roll', related_name='hoad_student_roll')
    hall_code = models.ForeignKey(Hall_details, on_delete=models.CASCADE, null=True,
                                     blank=True, db_column='hall_code', related_name='had_hall_code')
    admit_fees = models.CharField(max_length=20, null=True, blank=True)
    discount = models.CharField(max_length=20, null=True, blank=True)
    admit_status = models.CharField(
        max_length=10, choices=STATUS_LIST, default='A', blank=True)
    tran_batch_number = models.IntegerField(blank=True, null=True)
    cancel_by = models.CharField(max_length=20, null=True, blank=True)
    cancel_on = models.DateTimeField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.student_roll)


class Hostel_Admit_History(models.Model):
    branch_code = models.IntegerField(blank=True, null=True)
    admit_id = models.ForeignKey(Hostel_Admit, on_delete=models.CASCADE,
                                 null=True, blank=True, db_column='admit_id', related_name='his_admit_id')
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='academic_year', related_name='his_academic_year')
    admit_date = models.DateField(null=True, blank=True)
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE, null=True,
                                     blank=True, db_column='student_roll', related_name='his_student_roll')
    admit_fees = models.CharField(max_length=20, null=True, blank=True)
    discount = models.CharField(max_length=20, null=True, blank=True)
    admit_status = models.CharField(
        max_length=10, choices=STATUS_LIST, default='------', blank=False)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Add_Student_To_Meal(models.Model):
    meal_id = models.ForeignKey(Meal, on_delete=models.CASCADE, null=False,
                                blank=False, db_column='meal_id', related_name='add_meal_id')
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE, null=True,
                                     blank=True, db_column='student_roll', related_name='add_student_roll')
    meal_status = models.CharField(
        max_length=10, choices=STATUS_LIST, default="A")
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Daily_Meal(models.Model):
    meal_id = models.ForeignKey(Meal, on_delete=models.CASCADE, null=False,
                                blank=False, db_column='meal_id', related_name='daily_meal_id')
    date = models.DateField(null=True, blank=True)
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE, null=True,
                                     blank=True, db_column='student_roll', related_name='daily_student_roll')
    is_eat = models.IntegerField(blank=True, null=True, default=0)
    meal_price = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    cancel_by = models.CharField(max_length=20, null=True, blank=True)
    cancel_on = models.DateTimeField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

class Hostel_Fees_Mapping(models.Model):
    head_code = models.ForeignKey(Fees_Head_Settings, on_delete=models.CASCADE, null=True, blank=True, db_column='head_code',
                                  related_name='hall_fem_head_code')  # List item from Fees_Head_Settings which are not main head (is_main_head=False)
    hall_code = models.ForeignKey(Hall_details, on_delete=models.CASCADE, null=True,
                                     blank=True, db_column='hall_code', related_name='hfmhall_code')
    effective_date = models.DateField(null=True, blank=True)
    fine_effective_days = models.IntegerField(null=False, blank=True, default=0)
    fee_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    fine_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    pay_freq = models.CharField(
        max_length=5, choices=FEE_PAY_FRQ_LIST, default='', blank=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.head_code)+' - '+str(self.hall_code)

class Hostel_Fees_Mapping_Hist(models.Model):
    head_code = models.ForeignKey(Fees_Head_Settings, on_delete=models.CASCADE, null=True, blank=True, db_column='head_code',
                                  related_name='hall_feh_head_code')  # List item from Fees_Head_Settings which are not main head (is_main_head=False)
    hall_code = models.ForeignKey(Hall_details, on_delete=models.CASCADE, null=True,
                                     blank=True, db_column='hall_code', related_name='hfh_hall_code')
    effective_date = models.DateField(null=True, blank=True)
    fine_effective_days = models.IntegerField(null=False, blank=True, default=0)
    day_serial = models.IntegerField(null=True, blank=True)
    fee_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    fine_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    pay_freq = models.CharField(
        max_length=5, choices=FEE_PAY_FRQ_LIST, default='', blank=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.head_code)+' - '+str(self.hall_code)


class Fees_Processing_Details(models.Model):
    process_id = models.CharField(max_length=20, primary_key=True, blank=True)
    branch_code = models.IntegerField(blank=True, null=True)
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE,null=True,
                                     blank=True, db_column='student_roll', related_name='hostlfee_student_roll')
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='academic_year', related_name='hostlfee_academic_year')
    process_date = models.DateField(null=False, blank=False)
    process_status = models.BooleanField(blank=True, default=False)
    process_error = models.CharField(max_length=2000, null=True, blank=True)
    cancel_by = models.CharField(max_length=20, null=True, blank=True)
    cancel_on = models.DateTimeField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_roll
