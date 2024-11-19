from django.db.models import fields
from rest_framework import serializers
import datetime

from hrm.models import *
from apiauth.serializers import *

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department_Info
        fields = ('__all__')


class DesigntaionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee_Designation
        fields = ('__all__')

class CompanyInfoSerializer(serializers.ModelSerializer):
    division_id=Division_Serializer()
    district_id=District_Serializer()
    class Meta:
        model = Company_Information
        fields = ('__all__')


class OfficeInfoSerializer(serializers.ModelSerializer):
    country_id =CountrySerializer() 
    division_id = Division_Serializer()
    district_id =District_Serializer()
    upozila_id = Upazila_Serializer()
    class Meta:
        model = Company_Office
        fields = ('__all__')


class ShiftInfoSerializer(serializers.ModelSerializer):
    office_id = OfficeInfoSerializer()
    class Meta:
        model = Shift_Info
        fields = ('__all__')


class EmployeeDegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model= Education_Degree
        fields=('__all__')


class EmployeeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model= Employment_Type
        fields=('__all__')

class salaryScaleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model= Salary_Scale
        fields=('__all__')

class salaryScaleDetailsTypeSerializer(serializers.ModelSerializer):
    salscale_id = salaryScaleTypeSerializer()
    class Meta:
        model= Salary_Scale_Details
        fields=('__all__')


class salaryBonusTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model= Salary_Scale_Bonous
        fields=('__all__')

class ExtraAlownceSerializer(serializers.ModelSerializer):
    class Meta:
        model= Extra_Allowance
        fields=('__all__')



class BankTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model= Bank_Info
        fields=('__all__')


class EmpInfoSerializer(serializers.ModelSerializer):
    country_id=CountrySerializer()
    division_id = Division_Serializer()
    district_id = District_Serializer()
    upozila_id = Upazila_Serializer()
    salscale = salaryScaleTypeSerializer()
    current_shift = ShiftInfoSerializer()
    office_location = OfficeInfoSerializer()
    
    profile_image = serializers.SerializerMethodField('get_profile_image')
    def get_profile_image(self, instance):
        if instance.profile_image:
            return instance.profile_image.url
        else:
            return None
            
    employee_signature = serializers.SerializerMethodField('get_signature_image')
    def get_signature_image(self, instance):
        if instance.employee_signature:
            return instance.employee_signature.url
        else:
            return None
    class Meta:
        model= Employee_Details
        fields=('__all__')


class EmpExperianceSerializer(serializers.ModelSerializer):
    employee_id = EmpInfoSerializer()
    class Meta:
        model= Employee_Experience
        fields=('__all__')


class EmpEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee_Education
        fields=('__all__')
        

class EmpExperienceCreateSerializer(serializers.ModelSerializer):
    # employee_id = EmpInfoSerializer()
    class Meta:
        model= Employee_Experience
        fields=('__all__')
    # def create(self, validated_data):
        
    #     return super().create(validated_data)


class EmpNomineeSerializer(serializers.ModelSerializer):
    employee_id = EmpInfoSerializer()
    class Meta:
        model= Employee_Nominee
        fields=('__all__')

class EmpDocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model= Employee_Document_Type
        fields=('__all__')

class EmpDocumentSerializer(serializers.ModelSerializer):
    employee_id = EmpInfoSerializer()
    document_type = EmpDocumentTypeSerializer()
    class Meta:
        model= Employee_Document
        fields=('__all__')

class EmpLeaveInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model= Leave_Info
        fields=('__all__')


class EmpLeaveApplicationSerializer(serializers.ModelSerializer):
    employee_id = EmpInfoSerializer()
    application_to = EmpInfoSerializer()
    class Meta:
        model= Leave_Application
        fields=('__all__')

class EmpTrainingSerializer(serializers.ModelSerializer):
    employee_id = EmpInfoSerializer()
    class Meta:
        model= Employee_Training
        fields=('__all__')

class PayBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary_Scale_Details
        fields = ('__all__')
        

class EmpDtlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee_Details
        fields = ('__all__')
