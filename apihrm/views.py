from rest_framework.authentication import SessionAuthentication
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from rest_framework import generics
from django.db.models import Case, CharField, Value, When, F
from rest_framework.generics import ListAPIView
from django.http import JsonResponse
from hrm.models import * 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from hrm.utils import fn_serial_no_id
# Create your views here.

from hrm import models

from .serializers import *

class departmentApiView(generics.ListAPIView):
    serializer_class = DepartmentSerializer
    def get_queryset(self):
        department_id = self.request.query_params.get('department_id',None)
        

        queryset = Department_Info.objects.filter().order_by('department_name')

        if department_id:
            queryset = queryset.filter(department_id=department_id)

        return queryset



# @api_view(['GET'])
# def designationApiView(request):
#     tasks = models.Employee_Designation.objects.all().order_by('-id')
#     serializer = DesigntaionSerializer(tasks, many=True)
#     return Response(serializer.data)




class designationApiView(generics.ListAPIView):
    serializer_class = DesigntaionSerializer
    def get_queryset(self):
        designation_id = self.request.query_params.get('desig_id',None)
        

        queryset = Employee_Designation.objects.filter().order_by('desig_name')

        if designation_id:
            queryset = queryset.filter(desig_id=designation_id)

        return queryset


class companyInfoApiView(generics.ListAPIView):
    serializer_class = CompanyInfoSerializer
    def get_queryset(self):
        company_id = self.request.query_params.get('company_id',None)
        queryset = Company_Information.objects.filter().order_by('company_name')
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        return queryset


class OfficeInfoApiView(generics.ListAPIView):
    serializer_class = OfficeInfoSerializer
    def get_queryset(self):
        office_id = self.request.query_params.get('office_id',None)
        queryset = Company_Office.objects.filter().order_by('office_name')
        if office_id:
            queryset = queryset.filter(office_id=office_id)
        return queryset


class ShiftInfoApiView(generics.ListAPIView):
    serializer_class = ShiftInfoSerializer
    def get_queryset(self):
        shift_id=self.request.query_params.get('shift_id',None)
        queryset=Shift_Info.objects.filter().order_by('shift_name')

        if shift_id:
            queryset=queryset.filter(shift_id=shift_id)

        return queryset



class EmployeeDegreeApiView(generics.ListAPIView):
    serializer_class = EmployeeDegreeSerializer
    def get_queryset(self):
        degree_id=self.request.query_params.get('degree_id',None)
        queryset=Education_Degree.objects.filter().order_by('degree_name')

        if degree_id:
            queryset=queryset.filter(degree_id=degree_id)

        return queryset





class EmployeeTypeApiView(generics.ListAPIView):
    serializer_class = EmployeeTypeSerializer
    def get_queryset(self):
        emptype_id=self.request.query_params.get('emptype_id',None)
        queryset=Employment_Type.objects.filter().order_by('emptype_name')

        if emptype_id:
            queryset=queryset.filter(emptype_id=emptype_id)

        return queryset




class SalaryScaleTypeApiView(generics.ListAPIView):
    serializer_class = salaryScaleTypeSerializer
    def get_queryset(self):
        salscale_id=self.request.query_params.get('salscale_id',None)
        queryset=Salary_Scale.objects.filter().order_by('salscale_name')

        if salscale_id:
            queryset=queryset.filter(salscale_id=salscale_id)

        return queryset


class SalaryScaleDetailasTypeApiView(generics.ListAPIView):
    serializer_class=salaryScaleDetailsTypeSerializer
    def get_queryset(self):
        salsdtlcale_id=self.request.query_params.get('salsdtlcale_id',None)
        queryset=Salary_Scale_Details.objects.filter().order_by('salsdtlcale_name')

        if salsdtlcale_id:
            queryset=queryset.filter(salsdtlcale_id=salsdtlcale_id)

        return queryset


class SalaryBonusApiView(generics.ListAPIView):
    serializer_class=salaryBonusTypeSerializer
    def get_queryset(self):
        bonus_id=self.request.query_params.get('bonus_id',None)
        queryset=Salary_Scale_Bonous.objects.filter().order_by('bonus_name')

        if bonus_id:
            queryset=queryset.filter(bonus_id=bonus_id)

        return queryset
        

class ExtraAlownceApiView(generics.ListAPIView):
    serializer_class=ExtraAlownceSerializer
    def get_queryset(self):
        bonus_id=self.request.query_params.get('allowance_id',None)
        queryset=Extra_Allowance.objects.filter().order_by('allowance_name')

        if bonus_id:
            queryset=queryset.filter(bonus_id=bonus_id)

        return queryset



class BankTypeApiView(generics.ListAPIView):
    serializer_class=BankTypeSerializer
    def get_queryset(self):
        id=self.request.query_params.get('bank_id',None)
        queryset=Bank_Info.objects.filter().order_by('bank_name')

        if id:
            queryset=queryset.filter(bank_id=id)

        return queryset




class EmployeeINfoApiView(generics.ListAPIView):
    serializer_class=EmpInfoSerializer
    def get_queryset(self):
        id=self.request.query_params.get('employee_id',None)
        queryset=Employee_Details.objects.filter().order_by('employee_name')

        if id:
            queryset=queryset.filter(employee_id=id)

        return queryset




class EmployeeExperianceApiView(generics.ListAPIView):
    serializer_class=EmpExperianceSerializer
    def get_queryset(self):
        id = self.request.query_params.get('employee_id', None)
        queryset=Employee_Experience.objects.filter().order_by('employee_id')
        if id:
            queryset=queryset.filter(employee_id=id)

        return queryset


class EmployeeExperienceEditApiView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication]
    queryset=Employee_Experience.objects.all()
    serializer_class=EmpExperianceSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        print(request.data)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Experience updated successfully"})

        else:
            return Response({"error": "failed", "details": serializer.errors})
        

class EmpEducationEditDeleteApiView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication]
    queryset = Employee_Education.objects.all()
    serializer_class = EmpEducationSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        print(request.data)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Experience updated successfully"})

        else:
            return Response({"error": "failed", "details": serializer.errors})



class EmployeeExperienceCreateApiView(generics.CreateAPIView):
    authentication_classes = [SessionAuthentication]
    queryset=Employee_Experience.objects.all()
    serializer_class = EmpExperienceCreateSerializer

    def create(self, request, *args, **kwargs):
        app_user_id = request.session['app_user_id']
        data = request.data
        serial_no = fn_serial_no_id()
        data['app_user_id'] = app_user_id
        data['serial_no'] = serial_no
        # data['employee_id'] = employee_id[0]
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print(serializer.data, headers)
        return Response(serializer.data, headers=headers)

class EmployeeEducationCreateApiView(generics.CreateAPIView):
    authentication_classes = [SessionAuthentication]
    queryset = Employee_Education.objects.all()
    serializer_class = EmpEducationSerializer

    def create(self, request, *args, **kwargs):
        app_user_id = request.session['app_user_id']
        data = request.data
        serial_no = fn_serial_no_id()
        data['app_user_id'] = app_user_id
        data['serial_no'] = serial_no
        # data['employee_id'] = employee_id[0]
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print(serializer.data, headers)
        return Response(serializer.data, headers=headers)



class EmployeeNomineeApiView(generics.ListAPIView):
    serializer_class=EmpNomineeSerializer
    def get_queryset(self):
        
        queryset=Employee_Nominee.objects.filter().order_by('employee_id')


        return queryset

class EmployeeDocumentApiView(generics.ListAPIView):
    serializer_class=EmpDocumentSerializer
    def get_queryset(self):
        
        queryset=Employee_Document.objects.filter().order_by('employee_id')


        return queryset


class DocumentTypeApiView(generics.ListAPIView):
    serializer_class=EmpDocumentTypeSerializer
    def get_queryset(self):
        id=self.request.query_params.get('document_type_id',None)
        queryset=Employee_Document_Type.objects.filter().order_by('document_type_name')

        if id:
            queryset=queryset.filter(document_type_id=id)

        return queryset

class EmpLeaveInfoApiView(generics.ListAPIView):
    serializer_class=EmpLeaveInfoSerializer
    def get_queryset(self):
        id=self.request.query_params.get('leave_id',None)
        queryset=Leave_Info.objects.filter().order_by('leave_name')

        if id:
            queryset=queryset.filter(leave_id=id)

        return queryset

class EmpLeaveApplicationApiView(generics.ListAPIView):
    serializer_class=EmpLeaveApplicationSerializer
    def get_queryset(self):
        
        queryset=Leave_Application.objects.filter().order_by('leave_id')

        return queryset


class EmpTrainingInfoApiView(generics.ListAPIView):
        serializer_class=EmpTrainingSerializer
        def get_queryset(self):
        
            queryset=Employee_Training.objects.filter().order_by('employee_id')

            return queryset


class PayBillApiView(generics.ListAPIView):
    serializer_class=PayBillSerializer
    def get_queryset(self):
        id=self.request.query_params.get('bill_id',None)
        queryset=Pay_Bill.objects.filter().order_by('bill_id')

        if id:
            queryset=queryset.filter(bill_id=id)

        queryset = Salary_Scale_Details.objects.filter().order_by('salsdtlcale_id')
        return queryset

class EmpDtlApiView(generics.ListAPIView):
    serializer_class = EmpDtlSerializer
    def get_queryset(self):
        queryset = Employee_Details.objects.filter().order_by('employee_id')
        return queryset
