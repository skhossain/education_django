from django import forms
from crispy_forms.layout import Field
from django.forms import ModelForm, TextInput, Select, Textarea, IntegerField, ChoiceField, BooleanField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from edu.models import * 
from hostel.models import * 
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

class DateInput(forms.DateInput):
    input_type = 'date'

class ChoiceFieldNoValidation(ChoiceField):
    def validate(self, value):
        pass
# #Select 2
# class SearchStudent(s2forms.ModelSelect2Widget):
#     search_fields = [
#         "student_roll__icontains",
#     ]


# class DateForm(forms.Form):
#     date = forms.DateTimeField(
#         input_formats=['%d/%m/%Y %H:%M'],
#         widget=forms.DateTimeInput(attrs={
#             'class': 'form-control datetimepicker-input',
#             'data-target': '#datetimepicker1'
#         })
#     )


class BedTypeModelForm(forms.ModelForm):
    
    class Meta:
        model = Bed_Type
        fields = ['bed_type_name']
        labels = {
            "bed_type_name": ("Bed Type Name"),
        }
        widgets = {
            'bed_type_name': forms.TextInput(attrs={'placeholder': 'Single'}),
        }


class PayForTypeModelForm(forms.ModelForm):
    class Meta:
        model = PayFor_Types
        fields = ['pay_for_name']
        labels = {
            "pay_for_name": ("PayFor Type Name")
        }
        widgets = {
            'pay_for_name': forms.TextInput(attrs={'placeholder': 'Meal'}),
        }


class BedManagementModelForm(forms.ModelForm):
    class Meta:
        model = Beds_Management
        fields = ['bed_name','bed_price','bed_type_id']
        labels = {
            "bed_name": ("Bed Name / Number"),
            "bed_price": ("Bed Price"),
            "bed_type_id": ("Bed Type Name"),
        }
        widgets = {
            'bed_name': forms.TextInput(attrs={'placeholder': 'Normal-001'}),
            'bed_price': forms.NumberInput(attrs={'placeholder': '1500'}),
        }

class RoomManagementModelForm(forms.ModelForm):
    class Meta:
        model = Rooms_Management
        fields = ['room_name_or_number','room_size','room_rent','no_of_bed']
        labels = {
            "room_name_or_number":("Room Name/Number"),
            "room_size":("Room Size(square fit)"),
            "room_rent":("Room Rent"),
            "no_of_bed":("No. of Bed"),
        }
        widgets = {
            'room_name_or_number': forms.TextInput(attrs={'placeholder': 'A-101'}),
            'room_size': forms.NumberInput(attrs={'placeholder': '100'}),
            'room_price': forms.NumberInput(attrs={'placeholder': '4000'}),
        }

class PaymentManageModelForm(forms.ModelForm):
    class Meta:
        model = Payment_Management
        fields = ['academic_year','student_roll','month_name','payment_date','pay_for_id','payment','due']
        labels = {
            "academic_year":("Year/Academic Year"),
            "student_roll":("ID/Student Roll"),
            "month_name":("Month"),
            "payment_date":("Payment Date"),
            "pay_for_id":("Pay For"),
            "payment":("Payment"),
            "due":("Due"),
        }
        widgets = {
            'payment_date': DateInput(),
            'payment': forms.NumberInput(attrs={'placeholder': '5000'}),
            'due': forms.NumberInput(attrs={'placeholder': '00'}),
        }

class HostelAdmitModelForm(forms.ModelForm):
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    class Meta:
        model = Hostel_Admit
        fields = ['branch_code','academic_year','admit_date','student_roll','admit_fees','discount','admit_status','hall_code']
        labels = {
            "academic_year":("Academic Year"),
            "admit_date":("Admission Date"),
            "student_roll":("Student ID "),
            "admit_fees":("Admission Fee"),
            "discount":("Discount"),
            "admit_status":("Admission Status"),
            "hall_code":("Hall Name"),
            }
        widgets = {
            'admit_date': DateInput(),
            'admit_fees': forms.NumberInput(attrs={'placeholder': '5000'}),
            'discount': forms.NumberInput(attrs={'placeholder': '00'}),
        }

class HostelMealTypeModelForm(forms.ModelForm):
    class Meta:
        model = Meal_Type
        fields = ['meal_type_name']
        labels = {
            "meal_type_name":("Meal Type Name"),
        }
        widgets = {
            'meal_type_name': forms.TextInput(attrs={'placeholder': 'Full'}),
        }
        

class HostelMealModelForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['meal_type_id','meal_name','meal_price']
        labels = {
            "meal_type_id":("Meal Type Name"),
            "meal_name":("Meal Name"),
            "meal_price":("Meal Price"),
        }
        widgets = {
            'meal_name': forms.TextInput(attrs={'placeholder': 'Normal-(Full)'}),
            'meal_price': forms.NumberInput(attrs={'placeholder': '40'}),
        }

class AddingMealModelForm(forms.ModelForm):
    class Meta:
        model = Add_Student_To_Meal
        fields = ['meal_id','student_roll','meal_status']
        labels = {
            "meal_id":("Select Meal"),
            "student_roll":("Select Student (ID)"),
            "meal_status":("Meal Status"),
        }


class Hall_details_ModelForm(forms.ModelForm):
    class Meta:
        model = Hall_details
        fields = ['hall_name', 'hall_address',
                  'hall_supervisor', 'supervisor_phone', 'total_seat']


        labels = {
            "hall_name": ("Hall Name"),
            "hall_address": ("Hall Address"),
            "hall_supervisor": ("Hall Supervisor"),
            "supervisor_phone": ("Supervisor Phone"),
            "total_seat": ("Total Seat"),
        }


class Hostel_Fees_Mapping_ModelForm(forms.ModelForm):
    class Meta:
        model = Hostel_Fees_Mapping
        fields = ['head_code', 'hall_code', 'effective_date', 'fine_effective_days',
                  'fee_amount', 'fine_amount', 'pay_freq', 'is_active', 'is_deleted']
        labels = {
            "head_code": ("Fees Head"),
            "hall_code": ("Hall Name"),
            "effective_date": ("Effective Date"),
            "fine_effective_days": ("Fine After Day"),
            "fee_amount": ("Fee Amount"),
            "fine_amount": ("Fine Amount"),
            "pay_freq": ("Payment Frequency"),
            "is_active": ("Is Active"),
            "is_deleted": ("Is Delete"),
        }
        widgets = {
            'effective_date': DateInput(),
        }
 
class Fees_Mapping_History_Model_Form(forms.ModelForm):
    class Meta:
        model = Hostel_Fees_Mapping_Hist
        fields = ['head_code', 'hall_code', 'effective_date', 'fine_effective_days',
                  'fee_amount', 'fine_amount', 'pay_freq', 'is_active', 'is_deleted']
        labels = {
            "head_code": ("Fees Head"),
            "hall_code": ("Hall Name"),
            "effective_date": ("Effective Date"),
            "fine_effective_days": ("Fine After Day"),
            "fee_amount": ("Fee Amount"),
            "fine_amount": ("Fine Amount"),
            "pay_freq": ("Payment Frequency"),
            "is_active": ("Is Active"),
            "is_deleted": ("Is Delete"),
        }
        widgets = {
            'effective_date': DateInput(),
        }
 
class Fees_Processing_Details_ModelForm(forms.ModelForm):
    branch_code = ChoiceFieldNoValidation(
        label="Branch Name", required=False, choices=[('', '------------')], initial="")
    class Meta:
        model = Fees_Processing_Details
        fields = ['academic_year',
                  'student_roll', 'branch_code',  'process_date']
        labels = {
            "academic_year": ("Academic Year"),
            "student_roll": ("Student Roll/Name"),
            "branch_code": ("Branch Name"),
            "section_id": ("Section Name"),
            "process_date": ("Process Date")
        }
        widgets = {
            'process_date': DateInput(),
        }