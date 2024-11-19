from apiedu.serializer import AcademicClassSerializer, AcademicYearSerializer, StudentInfoSerializer
from rest_framework import serializers
import datetime

from edu.models import *
from transport.models import *

class TransportationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transportation_Type
        fields = ('__all__')
class TransportationSerializer(serializers.ModelSerializer):
    transportation_type_id=TransportationTypeSerializer()
    class Meta:
        model = Transportation
        fields = ('__all__')
class LocationInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location_Info
        fields = ('__all__')

class Vehicle_typeSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Vehicle_type
        fields = ('__all__')
        
class VehicleInfoSerializer(serializers.ModelSerializer):
    transportation_id=TransportationSerializer()
    vehicle_type_id=Vehicle_typeSerializer()

    class Meta:
        model = Vehicle_Information
        fields = ('__all__')

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ('__all__')

class ConductorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conductor
        fields = ('__all__')

class RoadMapSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Road_map
        fields = ('__all__')

class Road_map_DtlSerializer(serializers.ModelSerializer):
    road_map_id=RoadMapSerializer()
    transportation_id=TransportationSerializer()
    vehicle_id=VehicleInfoSerializer()
    location_info_id=LocationInfoSerializer()
    class Meta:
        model = Road_map_Dtl
        fields = ('__all__')

class Admit_TransportationSerializer(serializers.ModelSerializer):
    transportation_id=TransportationSerializer()
    class_id=AcademicClassSerializer()
    class Meta:
        model = Admit_Transportation
        fields = ('__all__')

class PayFor_TypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayFor_Types
        fields = ('__all__')

class Payment_ManagementSerializer(serializers.ModelSerializer):
    pay_for_id=PayFor_TypesSerializer()
    academic_year=AcademicYearSerializer()
    class Meta:
        model = Payment_Management
        fields = ('__all__')
        
        
class Attendance_Serializer(serializers.ModelSerializer):
    academic_year=AcademicYearSerializer()
    class_id = AcademicClassSerializer()
    road_map_id=RoadMapSerializer()
    location_info_id=LocationInfoSerializer()
    student_roll=StudentInfoSerializer()
    class Meta:
        model = Trans_Attendance
        fields = ('__all__')
