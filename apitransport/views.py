from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from rest_framework import generics
from django.db.models import Case, CharField, Value, When, F
from rest_framework.generics import ListAPIView
from edu.models import *
from transport.models import *

from apiedu.serializer import *
from apitransport.serializer import *
import datetime
# Create your views here.


class TransportationTypeApiView(generics.ListAPIView):
    serializer_class = TransportationTypeSerializer
    def get_queryset(self):
        transportation_type_id = self.request.query_params.get('transportation_type_id',None)
        queryset = Transportation_Type.objects.filter().order_by('transportation_type_id')
        if transportation_type_id:
            queryset = queryset.filter(transportation_type_id=transportation_type_id)

        return queryset

class TransportationApiView(generics.ListAPIView):
    serializer_class = TransportationSerializer
    def get_queryset(self):
        transportation_id = self.request.query_params.get('transportation_id',None)
        transportation_type_id = self.request.query_params.get('transportation_type_id',None)
        queryset = Transportation.objects.filter().order_by('transportation_id')
        if transportation_id:
            queryset = queryset.filter(transportation_id=transportation_id)
        if transportation_type_id:
            queryset = queryset.filter(transportation_type_id=transportation_type_id)

        return queryset

class LocationInfoApiView(generics.ListAPIView):
    serializer_class = LocationInfoSerializer
    def get_queryset(self):
        location_info_id = self.request.query_params.get('location_info_id',None)
        queryset = Location_Info.objects.filter().order_by('location_info_id')
        if location_info_id:
            queryset = queryset.filter(location_info_id=location_info_id)

        return queryset

class Vehicle_typeApiView(generics.ListAPIView):
    serializer_class = Vehicle_typeSerializer
    def get_queryset(self):
        vehicle_type_id = self.request.query_params.get('vehicle_type_id',None)
        transportation_name = self.request.query_params.get('transportation_name',None)
        transportation_type_id = self.request.query_params.get('transportation_type_id',None)
        
        queryset = Vehicle_type.objects.filter().order_by('vehicle_type_id')
        if vehicle_type_id:
            queryset = queryset.filter(vehicle_type_id=vehicle_type_id)
        if transportation_name:
            queryset = queryset.filter(transportation_name=transportation_name)
        if transportation_type_id:
            queryset = queryset.filter(transportation_type_id=transportation_type_id)
       
        return queryset

class VehicleInfoApiView(generics.ListAPIView):
    serializer_class = VehicleInfoSerializer
    def get_queryset(self):
        vehicle_id = self.request.query_params.get('vehicle_id',None)
        transportation_id = self.request.query_params.get('transportation_id',None)
        
        queryset = Vehicle_Information.objects.filter().order_by('vehicle_id')
        if vehicle_id:
            queryset = queryset.filter(vehicle_id=vehicle_id)
        if transportation_id:
            queryset = queryset.filter(transportation_id=transportation_id)

        return queryset

class DriverApiView(generics.ListAPIView):
    serializer_class = DriverSerializer
    def get_queryset(self):
        driver_id = self.request.query_params.get('driver_id',None)
        queryset = Driver.objects.filter().order_by('driver_id')
        if driver_id:
            queryset = queryset.filter(driver_id=driver_id)

        return queryset

class ConductorApiView(generics.ListAPIView):
    serializer_class = ConductorSerializer
    def get_queryset(self):
        conductor_id = self.request.query_params.get('conductor_id',None)
        queryset = Conductor.objects.filter().order_by('conductor_id')
        if conductor_id:
            queryset = queryset.filter(conductor_id=conductor_id)

        return queryset

class RoadMapApiView(generics.ListAPIView):
    serializer_class = RoadMapSerializer
    def get_queryset(self):
        road_map_id = self.request.query_params.get('road_map_id',None)
        queryset = Road_map.objects.filter().order_by('road_map_id')
        if road_map_id:
            queryset = queryset.filter(road_map_id=road_map_id)

        return queryset



class RoadMapDetailApiView(generics.ListAPIView):
    serializer_class = Road_map_DtlSerializer
    def get_queryset(self):
        road_map_id = self.request.query_params.get('road_map_id',None)
        queryset = Road_map_Dtl.objects.filter().order_by('road_map_id')
        if road_map_id:
            queryset = queryset.filter(road_map_id=road_map_id)

        return queryset

class Admit_TransportationApiView(generics.ListAPIView):
    serializer_class = Admit_TransportationSerializer
    def get_queryset(self):
        admit_transportation_id = self.request.query_params.get('admit_transportation_id',None)
        location_info_id= self.request.query_params.get('location_info_id',None)
        queryset = Admit_Transportation.objects.filter().order_by('admit_transportation_id')
        if admit_transportation_id:
            queryset = queryset.filter(admit_transportation_id=admit_transportation_id)
        if location_info_id:
            queryset = queryset.filter(location_info_id=location_info_id)

        return queryset
        
class PayforApiView(generics.ListAPIView):
    serializer_class = PayFor_TypesSerializer
    def get_queryset(self):
        pay_for_id = self.request.query_params.get('pay_for_id',None)
        queryset = PayFor_Types.objects.filter().order_by('pay_for_id')
        if pay_for_id:
            queryset = queryset.filter(pay_for_id=pay_for_id)

        return queryset
        
class Payment_ManagementApiView(generics.ListAPIView):
    serializer_class = Payment_ManagementSerializer
    def get_queryset(self):
        payment_management_id = self.request.query_params.get('payment_management_id',None)
        queryset = Payment_Management.objects.filter().order_by('payment_management_id')
        if payment_management_id:
            queryset = queryset.filter(payment_management_id=payment_management_id)
        return queryset

class Use_summery_ApiView(generics.ListAPIView):
    serializer_class = Attendance_Serializer
    def get_queryset(self):
        to_date = self.request.query_params.get('to_date',None)
        from_date = self.request.query_params.get('from_date',None)
        academic_year = self.request.query_params.get('academic_year',None)
        class_id = self.request.query_params.get('class_id',None)
        road_map_id = self.request.query_params.get('road_map_id',None)
        location_info_id = self.request.query_params.get('location_info_id',None)
        student_roll = self.request.query_params.get('student_roll',None)
        trans_status = self.request.query_params.get('trans_status',None)
        queryset = Trans_Attendance.objects.filter().order_by('-app_data_time')
        if to_date and from_date:
            end_date=datetime.datetime.strptime(from_date, "%Y-%m-%d")+datetime.timedelta(days=1)
            queryset = queryset.filter(date_time__range=[to_date, end_date.date()])
        if academic_year:
            queryset = queryset.filter(academic_year=academic_year)
        if class_id:
            queryset = queryset.filter(class_id=class_id)
        if road_map_id:
            queryset = queryset.filter(road_map_id=road_map_id)
        if location_info_id:
            queryset = queryset.filter(location_info_id=location_info_id)
        if student_roll:
            queryset = queryset.filter(student_roll=student_roll)
        if trans_status:
            queryset = queryset.filter(trans_status=trans_status)
        return queryset