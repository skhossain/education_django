from django import forms
from crispy_forms.layout import Field
from django.forms import ModelForm, TextInput, Select, Textarea, IntegerField, ChoiceField, BooleanField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from edu.models import * 
from transport.models import * 
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

class DateInput(forms.DateInput):
    input_type = 'date'


class ChoiceFieldNoValidation(ChoiceField):
    def validate(self, value):
        pass

class TransportationTypeModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TransportationTypeModelForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance and instance.pk:
            self.fields['transportation_type_id'].widget.attrs['readonly'] = True

    class Meta:
        model = Transportation_Type
        fields = ['transportation_type_id', 'transportation_type_name']
        labels = {
            "transportation_type_id": ("Transportation Type ID"),
            "transportation_type_name": ("Transportation Type Name"),
        }

class TransportationModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TransportationModelForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance and instance.pk:
            self.fields['transportation_id'].widget.attrs['readonly'] = True
            
    class Meta:
        model = Transportation
        fields = ['transportation_id', 'transportation_name','transportation_type_id']
        labels = {
            "transportation_id": ("Transportation ID"),
            "transportation_name": ("Transportation Name"),
            "transportation_type_id": ("Transportation Type ID"),
        }

class Location_InfoModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Location_InfoModelForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance and instance.pk:
            self.fields['location_info_id'].widget.attrs['readonly'] = True
            
    class Meta:
        model = Location_Info
        fields = ['location_info_id', 'location_name','location_description','division_id','district_id','upazila_id']
        labels = {
            "location_info_id": ("Location ID"),
            "location_name": ("Location Name"),
            "location_description": ("Location Description"),
            "division_id": ("Division"),
            "district_id": ("District"),
            "upazila_id": ("Upazila"),
        }
class Vehicle_typeModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Vehicle_typeModelForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance and instance.pk:
            self.fields['vehicle_type_id'].widget.attrs['readonly'] = True
            
    class Meta:
        model = Vehicle_type
        fields = [ 'vehicle_type_id','vehicle_type_name']
        labels = {
            
            "vehicle_type_id": ("Vehicle Type ID "),
            "vehicle_type_name": ("Vehicle Type Name"),
        }


class Vehicle_InformationModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Vehicle_InformationModelForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance and instance.pk:
            self.fields['vehicle_id'].widget.attrs['readonly'] = True
            
    class Meta:
        model = Vehicle_Information
        fields = ['transportation_id','vehicle_type_id','vehicle_id','vehicle_name','vehicle_number','vehicle_image','total_seat']
        labels = {
            "transportation_id": ("Transportation ID"),
            "vehicle_type_id": ("Vehicle type"),
            "vehicle_id": ("Vehicle ID"),
            "vehicle_name": ("Vehicle Name"),
            "vehicle_number": ("Vehicle Number"),
            "vehicle_image": ("Vehicle Image"),
            "total_seat": ("Total Seat"),
        }

class DriverModelForm(forms.ModelForm):
    
    class Meta:
        model = Driver
        fields = ['vehicle_id','driver_id', 'driver_name','contact_no','license_no','per_division_id','per_district_id','per_upozila_id','pre_division_id','pre_district_id','pre_upozila_id','same_as','dri_present_address','dri_permanent_address']
        labels = {
            "vehicle_id": ("vehicle"),
            "driver_id": ("Driver ID"),
            "driver_name": ("Driver Name"),
            "contact_no": ("Contact No"),
            "license_no": ("Licence No"),
            "per_division_id": ("Division"),
            "per_district_id": ("District"),
            "per_upozila_id": ("Upazila"),
            "pre_division_id": ("Division"),
            "pre_district_id": ("District"),
            "pre_upozila_id": ("Upazila"),
            "same_as": ("Same As"),
            "dri_present_address": ("Village/Road/Street"),
            "dri_permanent_address": ("Village/Road/Street"),
        }
        widgets = {
            "dri_present_address": forms.Textarea(attrs={"rows":1}),
            "dri_permanent_address": forms.Textarea(attrs={"rows":1})
        }

class ConductorModelForm(forms.ModelForm):
            
    class Meta:
        model = Conductor
        fields = ['vehicle_id','conductor_id', 'conductor_name','contact_no','license_no','per_division_id','per_district_id','per_upozila_id','pre_division_id','pre_district_id','pre_upozila_id','same_as','con_present_address','con_permanent_address']
        labels = {
            "vehicle_id": ("Vehicle"),
            "conductor_id": ("Conductor ID"),
            "conductor_name": ("Conductor Name"),
            "contact_no": ("Contact No"),
            "license_no": ("Licence No"),
            "per_division_id": ("Division"),
            "per_district_id": ("District"),
            "per_upozila_id": ("Upazila"),
            "pre_division_id": ("Division"),
            "pre_district_id": ("District"),
            "pre_upozila_id": ("Upazila"),
            "same_as": ("Same As"),
            "con_present_address": ("Village/Road/Street"),
            "con_permanent_address": ("Village/Road/Street"),
        }
        widgets = {
            "con_present_address": forms.Textarea(attrs={"rows":1}),
            "con_permanent_address": forms.Textarea(attrs={"rows":1})
        }


class Road_mapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Road_mapModelForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance and instance.pk:
            self.fields['road_map_id'].widget.attrs['readonly'] = True
            
    class Meta:
        model = Road_map
        fields = ['road_map_id','road_map_name']
        labels = {
            "road_map_id": ("Road Map ID"),
            "road_map_name": ("Road Map Name"),
            
        }


class Roadmap_DtlModelForm(forms.ModelForm):
    class Meta:
        model = Road_map_Dtl
        fields = ['road_map_id', 'transportation_id','vehicle_id','location_info_id','pickup_time','drop_time', 'saturday','sunday','monday','tuesday', 'wednesday','thursday','friday']
        labels = {
            "road_map_id": ("Road Map"),
            "transportation_id": ("Transportation"),
            "vehicle_id": ("Vehicle"),
            "location_info_id": ("Location"),
            "pickup_time": ("Pickup Time"),
            "drop_time": ("Drop Time"),
            "saturday": ("Saturday "),
            "sunday": ("Sunday"),
            "monday": ("Monday"), 
            "tuesday": ("Tuesday"),
            "wednesday": ("Wednesday"),
            "thursday": ("Thurday"),
            "friday": ("Friday"),
        }
        widgets = {
            'pickup_time': TimePicker(),
            'drop_time': TimePicker(),
        }



class Admit_TransportationModelForm(forms.ModelForm):
    
    class Meta:
        model = Admit_Transportation
        fields = [ 'transportation_id','road_map_id','location_info_id','academic_year','class_id','student_roll','transportation_fees','discount','starting_date', 'status','comments']
        widgets = {
            'starting_date': DateInput()            
        }

        labels = {
            "transportation_id": ("Transportation"),
            "road_map_id": ("Road map"),
            "location_info_id": ("Location"),
            "academic_year": ("Academic Year"),
            "class_id": ("Class"),
            "student_roll": ("Student Roll"),
            "transportation_fees": ("Transportation_fees"),
            "discount": ("Discount"), 
            "starting_date": ("Strating Date"),
            "status": ("Status"),
            "comments": ("Comment"),
        }        

class PayFor_TypesModelForm(forms.ModelForm):

    class Meta:
        model = PayFor_Types
        fields = ['pay_for_id', 'pay_for_name']
        
        labels = {
            "pay_for_id": ("Pay_for ID"),
            "pay_for_name": ("Pay_for Name"),
            
        }

class Payment_ManagementModelForm(forms.ModelForm):
    
    class Meta:
        model = Payment_Management
        fields = ['academic_year','student_roll','month_name','payment_date', 'pay_for_id','payment','due']
        widgets = {
            'payment_date': DateInput()            
        }
        labels = {
            "academic_year": ("Academic Year"),
            "student_roll": ("Student Roll"),
            "month_name": ("Months"),
            "payment_date": ("Payment Date"),
            "pay_for_id": ("Payfor ID "),
            "payment": ("Payment "),
            "due": ("Due"),
        }
class Trans_Attendance_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Trans_Attendance_Form, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance and instance.pk:
            self.fields['road_map_id'].widget.attrs['disabled'] = True
            # self.fields['road_map_id'].widget.attrs['readonly'] = True

    class Meta:
        model = Trans_Attendance
        fields = ['academic_year','class_id', 'road_map_id', 'location_info_id','student_roll','trans_status']
        widgets = {
            'date': DateInput()            
        }
        labels = {
            "academic_year": ("Academic Year"),
            "class_id": ("Class"),
            "road_map_id": ("Road Map"),
            "location_info_id": ("Location"),
            "student_roll": ("Student Roll"),
            "trans_status": ("Status "),
            # "time": ("Time"),
            # "date": ("Date"),
        }
