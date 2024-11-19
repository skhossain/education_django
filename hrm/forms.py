from edu.models import Teacher
from django.forms import ModelForm, TextInput, Select, Textarea, IntegerField, ChoiceField, BooleanField
from django import forms
from django.db.models import fields
from django.forms.models import ModelForm
from django.forms.widgets import DateTimeBaseInput, DateTimeInput
from django.http import request
from .models import *
from django.utils.translation import ugettext_lazy as _

from datetime import datetime
from django.utils import timezone


class DateInput(forms.DateInput):
    input_type = 'date'


class CompanyInformationForm(forms.ModelForm):
    class Meta:
        model = Company_Information
        fields = ('company_name', 'country_id', 'division_id',
                  'district_id', 'upozila_id', 'office_address')
        labels = {
            'company_name': _("Company Name"),
            'country_id': _('Country Name'),
            'division_id': _('Division Name'),
            'district_id': _("District Name"),
            'upozila_id': _('Upozela Name'),
            'office_address': _('Office Address')
        }


class CompanyOfficeForm(forms.ModelForm):
    class Meta:
        model = Company_Office
        fields = ('office_name', 'country_id', 'division_id',
                  'district_id', 'upozila_id', 'office_address')
        labels = {
            'office_name': _("Office Name"),
            'country_id': _('Country Name'),
            'division_id': _('Division Name'),
            'district_id': _("District Name"),
            'upozila_id': _('Upozela Name'),
            'office_address': _('Office Address')
        }


class DepartmentInfoForm(forms.ModelForm):
    class Meta:
        model = Department_Info
        fields = ('department_name', 'total_employee',
                  'department_location', 'department_incharge')
        labels = {
            'department_name': _("Department Name"),
            "total_employee": _("Total Employee"),
            "department": _("Department"),
            "department_incharge": _("Depatment Incharge")
        }


class ShiftInfoForm(forms.ModelForm):
    class Meta:
        model = Shift_Info
        fields = ('shift_name', 'office_id', 'total_work_minute', 'work_start_time_sec', 'work_end_time_sec',
                  'work_start_grace_time_sec', 'work_end_time_grace_sec', 'refresh_start_time_sec', 'refresh_end_time_sec')
        labels = {
            "shift_name": 'Shift Name',
            "office_id": "Office Name",
            "total_work_minute": _("Total Work Minute"),
            "work_start_time_sec": _("Work Start Time Sec"),
            'work_end_time_sec': _("Work End Time Sec"),
            'work_start_grace_time_sec': _("Work Start  Grace Time Sec"),
            'work_end_time_grace_sec': _("Work End Grace Time Sec"),
            'refresh_start_time_sec': _("Refresh Start Time Sec"),
            'refresh_end_time_sec': _('Refresh End Time Sec'),

        }


class EducationDegreeForm(forms.ModelForm):
    class Meta:
        model = Education_Degree
        fields = ('degree_name', 'degree_duration')
        labels = {
            'degree_name': 'Degree Name',
            'degree_duration': 'Degree Duration'
        }


class EmployeeDesignationForm(forms.ModelForm):
    class Meta:
        model = Employee_Designation
        fields = ['desig_name']
        labels = {
            'desig_name': 'Create Designation'
        }


class EmplyeeTypeForm(forms.ModelForm):
    class Meta:
        model = Employment_Type
        fields = ['emptype_name']
        labels = {
            'emptype_name': 'Employee Type',
        }


class SalaryScaleForm(forms.ModelForm):
    class Meta:
        model = Salary_Scale
        fields = ('salscale_name', 'total_salary',
                  'deduction_pct', 'effective_date', 'total_deduction', 'comments')
        labels = {
            'salscale_name': 'Scale Name',
            'total_salary': 'Total salary',
            'deduction_pct': 'Deduction pct',
            'total_deduction': 'Total deduction',
            'effective_date': 'Effective date',
            'comments': 'Comments'
        }
        widgets = {
            'effective_date': DateInput(),

        }


class SalaryScaleDetailsForm(forms.ModelForm):
    class Meta:
        model = Salary_Scale_Details
        fields = ('salscale_id', 'salsdtlcale_name', 'salary_amount',
                  'deduction_pct', 'total_deduction','effective_date','comments')
        labels = {
            'salscale_id': 'Scale Name',
            'salsdtlcale_name': 'Scale Details Name',
            'salary_amount': 'Salary Amount',
            'deduction_pct': 'Deduction pct',
            'total_deduction': 'Total Deduction',
            'effective_date': 'Effective Date',
            'comments': 'Comments'
        }
        widgets = {
            'effective_date': DateInput(),

        }


class SalaryBonusDetailsForm(forms.ModelForm):
    class Meta:
        model = Salary_Scale_Bonous
        fields = ('salscale_id', 'salsdtlcale_id', 'bonus_name',
                  'bonus_pct', 'bonus_amount','effective_date', 'comments')
        labels = {
            'salscale_id': 'Salary Scale Type',
            'salsdtlcale_id': 'Salsdtlcale_id',
            'bonus_pct': 'Bonus Percenteg',
            'bonus_name': 'Bonus Name',
            'bonus_amount': 'Bonus Amount',
            'comments': 'Comments',
            'effective_date': 'Effective Date'
        }
        widgets = {'effective_date': DateInput()}


class ExtraAllowanceDetailsForm(forms.ModelForm):
    class Meta:
        model = Extra_Allowance
        fields = ('allowance_name', 'allowance_amount', 'comments')
        labels = {
            'allowance_name': 'Allowance Type',
            'allowance_amount': 'Amount',
            'comments': 'comments',
        }


class BankInfoDetailsForm(forms.ModelForm):
    class Meta:
        model = Bank_Info
        fields = ('bank_name', 'bank_address', 'bank_phone', 'bank_email')
        labels = {
            'bank_name': _('bank_name'),
            'bank_address': _('bank_address'),
            'bank_phone': _('Bank Phone'),
            'bank_email': _('Bank Email'),
        }


class DateInput(forms.DateInput):
    input_type = 'date'


class EmployeeDetailsForm(forms.ModelForm):
    is_teacher = forms.BooleanField(
        label="Will he/she take classes?", initial=False, required=False)

    def __init__(self, *args, **kwargs):
        # techerId = kwargs.pop('techerId')
        super(EmployeeDetailsForm, self).__init__(*args, **kwargs)
        # self.fields['contract_start_date'].widget = DatePickerInput()
        self.fields['employee_present_address'].widget.attrs['rows'] = 1
        self.fields['employee_permanent_address'].widget.attrs['rows'] = 1
        self.fields['country_id'].widget.attrs['class'] = "selectpicker"
        self.fields['country_id'].widget.attrs['data-live-search'] = "true"
        self.fields['division_id'].widget.attrs['class'] = "selectpicker"
        self.fields['division_id'].widget.attrs['data-live-search'] = "true"
        self.fields['district_id'].widget.attrs['class'] = "selectpicker"
        self.fields['district_id'].widget.attrs['data-live-search'] = "true"
        self.fields['upozila_id'].widget.attrs['class'] = "selectpicker"
        self.fields['upozila_id'].widget.attrs['data-live-search'] = "true"
        self.fields['designation_id'].widget.attrs['class'] = "selectpicker"
        self.fields['designation_id'].widget.attrs['data-live-search'] = "true"
        self.fields['salscale'].widget.attrs['class'] = "selectpicker"
        self.fields['salscale'].widget.attrs['data-live-search'] = "true"
        self.fields['salary_bank'].widget.attrs['class'] = "selectpicker"
        self.fields['salary_bank'].widget.attrs['data-live-search'] = "true"
        self.fields['current_shift'].widget.attrs['class'] = "selectpicker"
        self.fields['current_shift'].widget.attrs['data-live-search'] = "true"
        self.fields['emptype_id'].widget.attrs['class'] = "selectpicker"
        self.fields['emptype_id'].widget.attrs['data-live-search'] = "true"
        self.fields['office_location'].widget.attrs['class'] = "selectpicker"
        self.fields['office_location'].widget.attrs['data-live-search'] = "true"
        # if is_techer:
        #     query = Teacher.objects.get(employee_id=is_techer)
        # if init_data == "true":
        #     self.fields['is_techer'].widget.attrs['checked'] = "true"

    def clean(self):
        cleaned_data = super(EmployeeDetailsForm, self).clean()
        dob = cleaned_data.get('employee_date_of_birth')
        if dob:
            if dob > timezone.now().date():
                raise forms.ValidationError('Date not be a past date')

    class Meta:
        model = Employee_Details
        fields = ('employee_name', 'employee_father_name', 'employee_mother_name', 'employee_blood_group', 'employee_sex', 'employee_religion', 'employee_marital_status', 'employee_national_id', 'country_id', 'division_id', 'district_id', 'upozila_id', 'employee_present_address', 'employee_permanent_address', 'employee_phone_own', 'employee_phone_office', 'employee_phone_home', 'passport_no', 'driving_licence', 'employee_tin', 'email_personal', 'employee_joining_date', 'employee_date_of_birth', 'employee_status',
                  'eme_contact_name', 'eme_contact_relation', 'eme_contact_phone', 'eme_contact_address', 'office_id', 'emptype_id', 'salscale', 'designation_id', 'email_official', 'reporting_to', 'current_shift', 'office_location', 'card_number', 'salary_bank', 'salary_bank_ac', 'contract_start_date', 'contract_exp_date', 'last_inc_date', 'next_inc_date', 'service_end_date', 'last_transfer_date', 'next_transfer_date', 'job_confirm_date', 'pf_confirm_date', 'gf_confirm_date', 'wf_confirm_date', 'last_promotion_date')
        labels = {
            'employee_name': _("Employee Name"),
            'employee_father_name': _("Father's Name"),
            'employee_mother_name': _("Mother's Name"),
            'employee_blood_group': _("Blood Group"),
            'employee_sex': _("Gender"),
            'employee_religion': _("Religion"),
            'employee_marital_status': _("Marital Status"),
            'employee_national_id': _("National Id"),
            'country_id': _("Country"),
            'division_id': _("Division"),
            'district_id': _("District"),
            'upozila_id': _("Upozila"),
            'employee_present_address': _("Present Address"),
            'employee_permanent_address': _("Permanent Address"),
            'employee_phone_own': _("Own Phone No."),
            'employee_phone_office': _("Phone Office"),
            'employee_phone_home': _("Home Phone No."),
            'passport_no': _("Passport No."),
            'driving_licence': _("Driving Licence"),
            'employee_tin': _("Tin No."),
            'email_personal': _("Personal Email"),
            'employee_joining_date': _("Joining Date"),
            'employee_date_of_birth': _("Date of Birth"),
            'employee_status': _("Employee Status"),
            'eme_contact_name': _("Optional Contact Name"),
            'eme_contact_relation': _("Optional Contact Relation"),
            'eme_contact_phone': _("Optional Contact Phone"),
            'eme_contact_address': _("Optional Contact Address"),
            'office_id': _("Office ID"),
            'emptype_id': _("Employee Type"),
            'salscale': _("Salary Scale"),
            'designation_id': _("Designation"),
            'email_official': _("Email Official"),
            'reporting_to': _("Reporting To"),
            'current_shift': _("Current Shift"),
            'office_location': _("Office Location"),
            'card_number': _("Card Number"),
            'salary_bank': _("Salary Bank"),
            'salary_bank_ac': _("Salary Bank Account NO."),
            'contract_start_date': _('Contract Start Date'),
            'contract_exp_date': _('Contract Expire Date'),
            'last_inc_date': _("Last Increment Date"),
            'next_inc_date': _("Next Increment Date"),
            'service_end_date': _("Service End Date"),
            'last_transfer_date': _("Last Transfer Date"),
            'next_transfer_date': _("Next Transfer Date"),
            'job_confirm_date': _("Job Confirm Date"),
            'pf_confirm_date': _("P.f. Confirm Date"),
            'gf_confirm_date': _("G.f. Confirm Date"),
            'wf_confirm_date': _("W.f. Confirm Date"),
            'last_promotion_date': _("Last Promotion Date"),
        }

        widgets = {'employee_date_of_birth': DateInput(),
                   'employee_joining_date': DateInput(),
                   'service_end_date': DateInput(),
                   'contract_start_date': DateInput(),
                   'contract_exp_date': DateInput(),
                   'next_inc_date': DateInput(),
                   'job_confirm_date': DateInput(),
                   'pf_confirm_date': DateInput(),
                   'gf_confirm_date': DateInput(),
                   'wf_confirm_date': DateInput(),
                   'last_promotion_date': DateInput(),
                   'last_inc_date': DateInput(),
                   'last_transfer_date': DateInput(),
                   'next_transfer_date': DateInput(),
                   }


class EmployeeExperinceInfoForm(forms.ModelForm):
    class Meta:
        model = Employee_Experience
        fields = {

            "employee_id", 'serial_no', 'company_name', 'company_address', 'company_type', 'position', 'department', 'responsibility', 'achievement', 'phone_number', 'email', 'contact_person', 'emp_id', 'start_date', 'end_date'
        }
        labels = {

            'employee_id': _('Employee No'),
            'serial_no': _('Serial No'),
            'company_name': _('Company Name'),
            'company_address': _('Company Address'),
            'company_type': _('Company Type'),
            'position': _('Position'),
            'department': _('Department'),
            'responsibility': _('Responsibility'),
            'achievement': _('Achievement'),
            'phone_number': _('Phone Number'),
            'email': _('Email'),
            'contact_person': _('Contact Person'),

            'start_date': _('Start Date'),
            'end_date': _('End Date'),
        }
        widgets = {'start_date': DateInput(),
                   'end_date': DateInput()}


class EmployeeNomineeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(EmployeeNomineeForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['nominee_birth_date'].required = False
        self.fields['nominee_serial'].required = False
        self.fields['nominee_name'].required = False
        self.fields['nominee_sex'].required = False
        self.fields['nominee_father_name'].required = False
        self.fields['nominee_mother_name'].required = False
        self.fields['nominee_present_addr'].required = False
        self.fields['nominee_permanent_addr'].required = False
        self.fields['nominee_nid_num'].required = False
        self.fields['nominee_religion'].required = False
        self.fields['nominee_blood_group'].required = False
        self.fields['nominee_mobile_num'].required = False

    class Meta:
        model = Employee_Nominee
        fields = {
            'employee_id', 'nominee_serial', 'nominee_name', 'nominee_sex', 'nominee_father_name', 'nominee_mother_name', 'nominee_present_addr', 'nominee_permanent_addr', 'nominee_birth_date',
            'nominee_nid_num', 'nominee_religion', 'nominee_blood_group', 'nominee_mobile_num'
        }
        labels = {
            'employee_id': _('Employee Name'),
            'nominee_serial': _('Nominee Serial No.'),
            'nominee_name': _('Name of Reference'),
            'nominee_sex': _('Gander'),
            'nominee_father_name': _("Father's Name"),
            'nominee_mother_name': _("Mother's Name"),
            'nominee_present_addr': _('Present Address'),
            'nominee_permanent_addr': _('Permanent Address'),
            'nominee_birth_date': _('Date of Birth'),
            'country_id': _('Country'),
            'nominee_nid_num': _('NID'),
            'nominee_religion': _('Religion'),
            'nominee_blood_group': _('Blood Group'),
            'nominee_mobile_num': _('Mobile No.')
        }
        widgets = {
            'nominee_birth_date': DateInput(),
        }


class EmployeeDocumentTypeForm(forms.ModelForm):
    class Meta:
        model = Employee_Document_Type
        fields = {
            'document_type_name'
        }
        labels = {
            'document_type_name': _('Document Type'),
        }


class EmployeeDocumentForm(forms.ModelForm):
    class Meta:
        model = Employee_Document
        fields = {
            'employee_id', 'document_type', 'document_location', 'file_no',
            'status'
        }
        labels = {
            'employee_id': _('Employee Name'),
            'document_type': _('Document Type'),
            'document_location': _('Document Location'),
            'file_no': _('File No'),
            'status': _('Status'),
        }


class LeaveInfoForm(forms.ModelForm):
    class Meta:
        model = Leave_Info
        fields = {
            'leave_name', 'total_leave', 'forward_leave', 'holiday_check'
        }
        labels = {

            'leave_name': _('Leave Name'),
            'total_leave': _('Total Leave'),
            'forward_leave': _('No of Forward'),
            'holiday_check': _('Holiday Count'),
        }


class LeaveApplicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LeaveApplicationForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(LeaveApplicationForm, self).clean()
        from_date = cleaned_data.get('from_date')
        upto_date = cleaned_data.get('upto_date')
        join_date = cleaned_data.get('join_date')
        if upto_date:
            if timezone.now().date() > upto_date:
                raise forms.ValidationError('Date not be a past date')
        if join_date:
            if timezone.now().date() > join_date:
                raise forms.ValidationError('Date not be a past date')
        if from_date:
            if timezone.now().date() > from_date:
                raise forms.ValidationError('Date not be a past date')
        return cleaned_data

    class Meta:
        model = Leave_Application
        fields = {
            'leave_id', 'employee_id',
            'from_date', 'upto_date', 'join_date', 'leave_reason', 'application_to', 'approval_comments'
        }

        labels = {
            'leave_id': _('Leave Type'),
            'employee_id': _('Employee Name'),
            'from_date': _('From Date'),
            'upto_date': _('Upto Date'),
            'join_date': _('Join Date'),
            'leave_reason': _('Leave Reason'),
            'application_to': _('Application To'),
            'approval_comments': _('Comments')
        }
        widgets = {
            'from_date': DateInput(),
            'upto_date': DateInput(),
            'join_date': DateInput(),
            'application_date': DateInput(),

        }


class EmployeeTrainingForm(forms.ModelForm):
    class Meta:
        model = Employee_Training
        fields = {'employee_id', 'schedule_id', 'institute_name',
                  'training_name', 'training_description', 'from_date', 'upto_date', }
        labels = {
            "employee_id": _('Employee'),
            'schedule_id': _('Schedule'),
            'institute_name': _('Institute Name'),
            'training_name': _('Training Name'),
            'training_description': _('Training Description'),
            'from_date': _('From Date'),
            'upto_date': _('Upto Date'),
        }
        widgets = {
            'from_date': DateInput(),
            'upto_date': DateInput(),
        }


class PayBillForm(forms.ModelForm):
    class Meta:
        model = Pay_Bill
        fields = {
            'bill_date', 'bill_comments', 'bill_doc_detail',
            'bill_amount', 'approval_amount', 'prepare_by', 'checked_by', 'approve_by', 'checked_status', 'approve_status', 'checked_date', 'approve_date', 'attached_file'
        }
        labels = {
            'bill_date': _('Bill Date'),
            'bill_comments': _('Comments'),
            'bill_doc_detail': _('Document Detail'),
            'bill_amount': _('Amount'),
            'approval_amount': _('Approve Amount'),
            'prepare_by': _('Prepare By'),
            'checked_by': _('Check By'),
            'approve_by': _('Approve By'),
            'checked_status': _('Checked Status'),
            'approve_status': _('Approve Status'),
            'checked_date': _('Checked Date'),
            'approve_date': _("Approve Date"),
            'attached_file': _('Files')
        }
        widgets = {
            'bill_date': DateInput(),

            'checked_date': DateInput(),
            'approve_date': DateInput(),
        }


class ChoiceFieldNoValidation(ChoiceField):
    def validate(self, value):
        pass


class EmployeeEducationForm(forms.ModelForm):
    degree_name = ChoiceFieldNoValidation(label="Name of Degree", choices=[])

    def __init__(self, *args, **kwargs):
        super(EmployeeEducationForm, self).__init__(*args, **kwargs)
        # self.fields['degree_name'].widget.attrs['class'] = "selectpicker"
        # self.fields['degree_name'].widget.attrs['data-live-search'] = "true"

    class Meta:
        model = Employee_Education
        fields = {
            'board_name', 'result_point',
            'result_grate', 'passing_year', 'institute_name'
        }
        labels = {

            'board_name': _('Name of Board'),
            'result_point': _('Point'),
            'result_grate': _('Grade'),
            'passing_year': _('Passing Year'),
            'institute_name': _('Name of Institution'),
        }
