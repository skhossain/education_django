from urllib import response
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from rest_framework import generics
from django.db.models import Case, CharField, Value, When, F, Q
from rest_framework.generics import ListAPIView
# Create your views here.

from edu.models import *
from edu.models import Department_Info as Edu_Department_Info
from edu.models import Shift_Info as Edu_Shift_Info
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination
from apiedu.serializer import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse


class LimitPagination(LimitOffsetPagination):
    page_query_param = "offset" # this is the "page"
    page_size_query_param="limit" # this is the "page_size"
    # page_size = 5
    # max_page_size = 100


class PagePagination(PageNumberPagination):
  page_size = 10
  page_size_query_param = 'page_size'
  max_page_size = 10000


@api_view(['GET', 'POST'])
def StudentPaginationApiview(request):
 
  branch_code = request.query_params.get('branch_code',None)
  student_roll = request.query_params.get('student_roll',None)
  academic_year = request.query_params.get('academic_year',None)
  class_id = request.query_params.get('class_id',None)
  class_roll = request.query_params.get('class_roll',None)
  class_group_id =request.query_params.get('class_group_id',None)
  session_id = request.query_params.get('session_id',None)
  catagory_id = request.query_params.get('catagory_id',None)
  student_phone = request.query_params.get('student_phone',None)
  section_id = request.query_params.get('section_id',None)
  shift_id = request.query_params.get('shift_id',None)
  search = request.query_params.get('search',None)


  from_academic_year = request.query_params.get('from_academic_year',None)
  from_class = request.query_params.get('from_class',None)
  from_section = request.query_params.get('from_section',None)
  from_class_group = request.query_params.get('from_class_group',None)
  student_id = request.query_params.get('student_id',None)



  queryset = Students_Info.objects.filter().order_by(
      'student_roll','-app_data_time', 'student_name')
  
  if student_roll:
      queryset = queryset.filter(student_roll=student_roll)
  if academic_year:
      queryset = queryset.filter(academic_year=academic_year)
  if class_id:
      queryset = queryset.filter(class_id=class_id)
  if class_roll:
      queryset = queryset.filter(class_roll=class_roll)
  if class_group_id:
      queryset = queryset.filter(class_group_id=class_group_id)
  if session_id:
      queryset = queryset.filter(session_id=session_id)
  if catagory_id:
      queryset = queryset.filter(catagory_id=catagory_id)
  if student_phone:
      queryset = queryset.filter(student_phone=student_phone)
  if section_id:
      queryset = queryset.filter(section_id=section_id)
  if shift_id:
      queryset = queryset.filter(shift_id=shift_id)
  if branch_code:
      queryset = queryset.filter(branch_code=branch_code)
  if search:
      queryset = queryset.filter(
          Q(student_roll__icontains=search) | Q(student_name__icontains=search) | Q(class_roll__icontains=search) | Q(student_phone__icontains=search)
          )

  if from_academic_year:
      queryset = queryset.filter(academic_year=from_academic_year)
  if from_class:
      queryset = queryset.filter(class_id=from_class)
  if from_section:
      queryset = queryset.filter(section_id=from_section)

  if from_class_group:
      queryset = queryset.filter(class_group_id=from_class_group)
  if student_id:
      queryset = queryset.filter(student_roll=student_id)

  paginator = PagePagination()
  result_page = paginator.paginate_queryset(queryset, request)
  serializer = StudentInfoSerializer(result_page, many=True)
  return paginator.get_paginated_response(serializer.data)