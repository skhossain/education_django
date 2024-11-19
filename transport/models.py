from django.db import models
from jsonfield import JSONField
from appauth.models import Loc_Country, Loc_Division, Loc_District, Loc_Upazila, Branch
from tinymce.models import HTMLField

from edu.models import Students_Info,Academic_Class,Academic_Year
STATUS = (
    ('', '----------'),
    ('Enable', 'Enable'),
    ('Disable', 'Disable')
)

MONTH_LIST = (
    ('', '----------'),
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

TRAN_STATUS =(
    ('', '----------'),
    ('Pickup', 'Pickup'),
    ('Drop', 'Drop')
)

class Transportation_Type(models.Model):
    transportation_type_id=models.CharField(max_length=30, primary_key=True,blank=True)
    transportation_type_name=models.CharField(max_length=500,null=False,blank=False,unique = True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.transportation_type_name)

class Transportation(models.Model):
    transportation_id=models.CharField(max_length=50, primary_key=True,blank=True)
    transportation_name=models.CharField(max_length=30,null=False,blank=False)
    transportation_type_id=models.ForeignKey(Transportation_Type, on_delete=models.CASCADE, null=False, blank=False, db_column='transportation_type_id', related_name='t_transportation_type_id')
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.transportation_name)

class Location_Info(models.Model):
    location_info_id=models.CharField(max_length=30, primary_key=True,blank=True)
    location_name=models.CharField(max_length=500,blank=False,null=False,unique = True)
    location_description = models.CharField(max_length=500,null=True, blank=True)
    division_id = models.ForeignKey(Loc_Division, on_delete=models.CASCADE, null=True,blank=True, db_column='division_id', related_name='tr_division_id')
    district_id = models.ForeignKey(Loc_District, on_delete=models.CASCADE, null=True,blank=True, db_column='district_id', related_name='tr_district_id')
    upazila_id = models.ForeignKey(Loc_Upazila, on_delete=models.CASCADE, null=True,blank=True, db_column='upazila_id', related_name='tr_upazila_id')
    latitude = models.DecimalField(max_digits=22, decimal_places=2, null=True, blank=True )
    longitude = models.DecimalField(max_digits=22, decimal_places=2, null=True, blank=True )
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.location_name)

class Vehicle_type(models.Model):
    vehicle_type_id=models.CharField(max_length=30, primary_key=True,blank=True)
    vehicle_type_name=models.CharField(max_length=50, null=False,blank=False,unique = True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.vehicle_type_name)

class Vehicle_Information(models.Model):
    transportation_id=models.ForeignKey(Transportation, on_delete=models.CASCADE, null=True, blank=True, db_column='transportation_id', related_name='vi_tran_id')
    vehicle_type_id=models.ForeignKey(Vehicle_type, on_delete=models.CASCADE, null=True, blank=True, db_column='vehicle_type_id', related_name='vi_ve_typeid')
    vehicle_id=models.CharField(max_length=30, primary_key=True,blank=True)
    vehicle_name=models.CharField(max_length=50, null=True,blank=True)
    vehicle_number=models.IntegerField( null=True,blank=True,unique = True)
    vehicle_image =models.ImageField(upload_to='images/',null=True,blank=True)
    total_seat=models.IntegerField(null=False,blank=False)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.vehicle_name)

class Driver(models.Model):
    driver_id = models.CharField(max_length=30, primary_key=True,blank=True)
    driver_name = models.CharField(max_length=20,null=False,blank=False)
    contact_no = models.CharField(max_length=15, null=False,blank=False,unique = True)
    license_no =models.IntegerField(null=True,blank=True,unique = True)
    per_division_id = models.ForeignKey(Loc_Division, on_delete=models.CASCADE, null=True,blank=True, db_column='per_division_id', related_name='dri_perdivision_id')
    per_district_id = models.ForeignKey(Loc_District, on_delete=models.CASCADE, null=True,blank=True, db_column='per_district_id', related_name='dri_perdistrict_id')
    per_upozila_id = models.ForeignKey(Loc_Upazila, on_delete=models.CASCADE, null=True,blank=True, db_column='per_upozila_id', related_name='dri_perupozila_id')
    pre_division_id = models.ForeignKey(Loc_Division, on_delete=models.CASCADE, null=True,blank=True, db_column='pre_division_id', related_name='dri_predivision_id')
    pre_district_id = models.ForeignKey(Loc_District, on_delete=models.CASCADE, null=True,blank=True, db_column='pre_district_id', related_name='dri_predistrict_id')
    pre_upozila_id = models.ForeignKey(Loc_Upazila, on_delete=models.CASCADE, null=True,blank=True, db_column='pre_upozila_id', related_name='dri_preupozila_id')
    vehicle_id = models.ForeignKey(Vehicle_Information, on_delete=models.CASCADE, db_column='vehicle_id', related_name='dir_vehicle_id')
    same_as = models.BooleanField(blank=True,default=False)
    dri_present_address = models.TextField(null=True, blank=True)
    dri_permanent_address = models.TextField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.driver_name)

class Conductor(models.Model):
    conductor_id = models.CharField(max_length=30, primary_key=True,blank=True)
    conductor_name = models.CharField(max_length=20)
    contact_no = models.CharField(max_length=15, null=True)
    license_no =models.IntegerField(null=True,blank=True,unique = True)
    per_division_id = models.ForeignKey(Loc_Division, on_delete=models.CASCADE, null=True,blank=True, db_column='per_division_id', related_name='con_perdivision_id')
    per_district_id = models.ForeignKey(Loc_District, on_delete=models.CASCADE, null=True,blank=True, db_column='per_district_id', related_name='con_perdistrict_id')
    per_upozila_id = models.ForeignKey(Loc_Upazila, on_delete=models.CASCADE, null=True,blank=True, db_column='per_upozila_id', related_name='con_perupozila_id')
    pre_division_id = models.ForeignKey(Loc_Division, on_delete=models.CASCADE, null=True,blank=True, db_column='pre_division_id', related_name='con_predivision_id')
    pre_district_id = models.ForeignKey(Loc_District, on_delete=models.CASCADE, null=True,blank=True, db_column='pre_district_id', related_name='con_predistrict_id')
    pre_upozila_id = models.ForeignKey(Loc_Upazila, on_delete=models.CASCADE, null=True,blank=True, db_column='pre_upozila_id', related_name='con_preupozila_id')
    same_as = models.BooleanField(blank=True,default=False)
    vehicle_id = models.ForeignKey(Vehicle_Information, on_delete=models.CASCADE, db_column='vehicle_id', related_name='con_vehicle_id')
    con_present_address = models.TextField(null=True, blank=True)
    con_permanent_address = models.TextField(null=True,blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.conductor_name)


class Road_map(models.Model):
    road_map_id= models.CharField(max_length=30, primary_key=True,blank=True)
    road_map_name=models.CharField(max_length=50, null=False,blank=False)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.road_map_name)

class Road_map_Dtl(models.Model):
    road_map_id=models.ForeignKey(Road_map, on_delete=models.CASCADE, null=True, blank=True, db_column='road_map_id', related_name='rmd_road_map_id')
    transportation_id=models.ForeignKey(Transportation, on_delete=models.CASCADE, null=False, blank=False, db_column='transportation_id', related_name='rm_trans_id')
    vehicle_id= models.ForeignKey(Vehicle_Information, on_delete=models.CASCADE, null=True, blank=True, db_column='vehicle_id', related_name='rmd_vehicle_id')
    location_info_id=models.ForeignKey(Location_Info, on_delete=models.CASCADE, null=True, blank=True, db_column='location_info_id', related_name='rmd_location_info_id')
    pickup_time=models.CharField(max_length=20, blank=False, null=False)
    drop_time=models.CharField(max_length=20, blank=False, null=False)
    saturday=models.IntegerField(null=True, blank=True)    
    sunday=models.IntegerField(null=True, blank=True)    
    monday=models.IntegerField(null=True, blank=True)    
    tuesday=models.IntegerField(null=True, blank=True)    
    wednesday=models.IntegerField(null=True, blank=True)    
    thursday=models.IntegerField(null=True, blank=True)    
    friday=models.IntegerField(null=True, blank=True)    
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.road_map_id)

class Admit_Transportation(models.Model):
    admit_transportation_id=models.CharField(max_length=30, primary_key=True,blank=True)
    transportation_id=models.ForeignKey(Transportation, on_delete=models.CASCADE, null=False, blank=False, db_column='transportation_id', related_name='at_tran_id')
    location_info_id= models.ForeignKey(Location_Info, on_delete=models.CASCADE, null=True, blank=True, db_column='location_info_id', related_name='at_location_id')
    academic_year=models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True, blank=True, db_column='academic_year', related_name='at_aca_year')
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE, null=True, blank=True, db_column='class_id', related_name='at_cls_id')
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE, null=True, blank=True, db_column='student_roll', related_name='at_stu_roll')
    road_map_id=models.ForeignKey(Road_map, on_delete=models.CASCADE, db_column='road_map_id', related_name='at_rd_map_id')
    transportation_fees = models.CharField(max_length=20)
    discount = models.CharField(max_length=20,null=True, blank=True)
    starting_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=100, null=True, choices=STATUS, default='---------', blank=True)
    comments = models.CharField(max_length=200,null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.student_roll)

class Admit_Tran_History(models.Model):
    admit_transportation_id=models.ForeignKey(Admit_Transportation, on_delete=models.CASCADE, null=True, blank=True, db_column='admit_Transportation_id', related_name='ath_admit_Transportation_id')
    academic_year=models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True, blank=True, db_column='academic_year', related_name='ath_academic_year')
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE, null=True, blank=True, db_column='class_id', related_name='ath_class_id')
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE, null=True, blank=True, db_column='student_roll', related_name='ath_student_roll')
    status = models.CharField(max_length=100, null=True, choices=STATUS, default='---------', blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)
    


class PayFor_Types(models.Model):
    pay_for_id = models.CharField(max_length=30, blank=True,primary_key=True)
    pay_for_name = models.CharField(max_length=200, blank=False)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pay_for_name)

class Payment_Management(models.Model):
    payment_management_id = models.CharField(max_length=30, blank=True,primary_key=True)
    academic_year = models.ForeignKey(Academic_Year, on_delete=models.CASCADE, null=True, blank=True, db_column='academic_year', related_name='tran_pay_academic_year')
    student_roll = models.ForeignKey(Students_Info,on_delete=models.CASCADE,null=True, blank=True, db_column='student_roll', related_name='tran_pay_student_roll')
    month_name= models.IntegerField(null=True,choices=MONTH_LIST, default=1, blank=False)
    payment_date= models.DateField(blank=False)
    pay_for_id = models.ForeignKey(PayFor_Types,on_delete=models.CASCADE,null=True, blank=True, db_column='pay_for_id', related_name='tran_pay_for_id')
    payment = models.CharField(max_length=20, null=False, blank=False)
    due = models.CharField(max_length=20, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.student_roll)



class Trans_Attendance(models.Model):
    academic_year=models.ForeignKey(Academic_Year, on_delete=models.CASCADE, blank=True, db_column='academic_year', related_name='tsl_aca_year')
    class_id = models.ForeignKey(Academic_Class, on_delete=models.CASCADE, blank=True, db_column='class_id', related_name='tsl_cls_id')
    road_map_id=models.ForeignKey(Road_map, on_delete=models.CASCADE, db_column='road_map_id', related_name='tsl_rd_map_id')
    location_info_id= models.ForeignKey(Location_Info, on_delete=models.CASCADE, null=True, blank=True, db_column='location_info_id', related_name='tsl_loc_id')
    student_roll = models.ForeignKey(Students_Info, on_delete=models.CASCADE, null=True, blank=True, db_column='student_roll', related_name='tsl_stu_roll')
    trans_status = models.CharField(max_length=100, choices=TRAN_STATUS, default='---------',)
    date_time = models.DateTimeField(auto_now_add=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.student_roll)
