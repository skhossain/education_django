
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from rest_framework import generics
from django.db.models import Case, CharField, Value, When, F
from rest_framework.generics import ListAPIView
# Create your views here.

from hostel.models import *

from apihostel.serializers import *

class BedTypeApiView(generics.ListAPIView):
    serializer_class = BedTypeSerializer
    def get_queryset(self):
        bed_type_name = self.request.query_params.get('bed_type_name',None)
        queryset = Bed_Type.objects.filter().order_by('bed_type_name')
        if bed_type_name:
            queryset = queryset.filter(bed_type_name=bed_type_name)
        return queryset

class PayForTypeApiView(generics.ListAPIView):
    serializer_class = PayForTypeSerializer
    def get_queryset(self):
        pay_for_name = self.request.query_params.get('pay_for_name',None)
        queryset= PayFor_Types.objects.filter().order_by('pay_for_name')
        if pay_for_name:
            queryset = queryset.filter(pay_for_name=pay_for_name)
        return queryset

class BedManagementApiView(generics.ListAPIView):
    serializer_class = BedManageSerializer
    def get_queryset(self):
        bed_name= self.request.query_params.get('bed_name',None)
        queryset=Beds_Management.objects.filter().order_by('bed_name')
        if bed_name:
            queryset=queryset.filter(bed_name=bed_name)
        return queryset

        
class RoomManagementApiView(generics.ListAPIView):
    serializer_class=RoomManageSerializer
    def get_queryset(self):
        room_name_or_number=self.request.query_params.get('room_name_or_number',None)
        queryset=Rooms_Management.objects.filter().order_by('room_name_or_number')
        if room_name_or_number:
            queryset=queryset.filter(room_name_or_number=room_name_or_number)
        return queryset

class PaymentManageApiView(generics.ListAPIView):
    serializer_class=PaymentmanageSerializer
    def get_queryset(self):
        payment_management_id=self.request.query_params.get('payment_management_id',None)
        academic_year=self.request.query_params.get('academic_year',None)
        queryset=Payment_Management.objects.filter().order_by('payment_management_id')
        if payment_management_id:
            queryset=queryset.filter(payment_management_id=payment_management_id)
        if academic_year:
            queryset=queryset.filter(academic_year=academic_year)
        return queryset

class HostelAdmissionApiView(generics.ListAPIView):
    serializer_class=HostelAdmissionSerializer
    def get_queryset(self):
        branch_code=self.request.query_params.get('branch_code',None)
        admit_id=self.request.query_params.get('admit_id',None)
        student_roll=self.request.query_params.get('student_roll',None)
        academic_year=self.request.query_params.get('academic_year',None)

        queryset=Hostel_Admit.objects.filter().order_by('admit_id')
        if branch_code:
            queryset=queryset.filter(branch_code=branch_code)
        if admit_id:
            queryset=queryset.filter(admit_id=admit_id)
        if student_roll:
            queryset=queryset.filter(student_roll=student_roll)
        if academic_year:
            queryset=queryset.filter(academic_year=academic_year)
        return queryset


class HostelMealTypeApiView(generics.ListAPIView):
    serializer_class=HostelMealTypeSerializer
    def get_queryset(self):
        queryset=Meal_Type.objects.filter().order_by('meal_type_name')
        return queryset
        

class HostelMealApiView(generics.ListAPIView):
    serializer_class=HostelMealSerializer
    def get_queryset(self):
        queryset=Meal.objects.filter().order_by('meal_name')
        return queryset
        

class HostelAddMealApiView(generics.ListAPIView):
    serializer_class=HostelAddMealSerializer
    def get_queryset(self):
        meal_id=self.request.query_params.get('meal_id',None)
        queryset=Add_Student_To_Meal.objects.filter().order_by('meal_id')
        if meal_id:
            queryset=queryset.filter(meal_id=meal_id)
        return queryset

class Hall_details_ApiView(generics.ListAPIView):
    serializer_class = Hall_details_Serializer

    def get_queryset(self):
        queryset = Hall_details.objects.filter().order_by('hall_name')
        return queryset

class Hostel_Fees_Mapping_ApiView(generics.ListAPIView):
    serializer_class = Hostel_Fees_Mapping_Serializer

    def get_queryset(self):
        queryset = Hostel_Fees_Mapping.objects.filter().order_by('head_code')
        return queryset

class Fees_Processing_Details_ApiView(generics.ListAPIView):
    serializer_class = Fees_Processing_Details_Serializer

    def get_queryset(self):
        queryset = Fees_Processing_Details.objects.filter().order_by('app_data_time')
        return queryset
