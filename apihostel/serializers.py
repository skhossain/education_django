from django.db.models import fields
from rest_framework import serializers
import datetime
from apiedu.serializer import *
from apihostel.serializers import *
from hostel.models import *

class BedTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bed_Type
        fields = ('__all__')

class PayForTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayFor_Types
        fields = ('__all__')

class BedManageSerializer(serializers.ModelSerializer):
    bed_type_id=BedTypeSerializer()
    class Meta:
        model = Beds_Management
        fields =('__all__')


class RoomManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms_Management
        fields = ('__all__')

class PaymentmanageSerializer(serializers.ModelSerializer):
    pay_for_id =PayForTypeSerializer()
    academic_year=AcademicYearSerializer()
    class Meta:
        model = Payment_Management
        fields = ('__all__')




class HostelMealTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal_Type
        fields = ('__all__')
        


class HostelMealSerializer(serializers.ModelSerializer):
    meal_type_id=HostelMealTypeSerializer()
    class Meta:
        model = Meal
        fields = ('__all__')


class HostelAdmissionSerializer(serializers.ModelSerializer):
    academic_year=AcademicYearSerializer()
    student_roll=StudentInfoSerializer()
    class Meta:
        model=Hostel_Admit
        fields = ('__all__')

class HostelAddMealSerializer(serializers.ModelSerializer):
    meal_id=HostelMealSerializer()
    student_roll=StudentInfoSerializer()
    class Meta:
        model = Add_Student_To_Meal
        fields = ('__all__')


class Hall_details_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Hall_details
        fields = ('__all__')


class Hostel_Fees_Mapping_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Hostel_Fees_Mapping
        fields = ('__all__')
        depth = 1


class Fees_Processing_Details_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Fees_Processing_Details
        fields = ('__all__')
        depth = 1
