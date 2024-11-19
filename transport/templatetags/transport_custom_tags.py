from ..models import *
from django import template
from django.shortcuts import get_object_or_404

register = template.Library()

# def get_exam_name(a):
#     exam_name=Exam_Setup.objects.get(exam_id=a)
#     return exam_name

# register.filter('get_exam_name', get_exam_name)

# def get_degree_name(id):
#     name=Degree_Info.objects.get(degree_id=id)
#     return name

# register.filter('get_degree_name', get_degree_name)

# def get_institute_name(id):
#     name=Education_Institute.objects.get(institute_id=id)
#     return name
# register.filter('get_institute_name', get_institute_name)

# def get_student_name(id):
#     student=get_object_or_404(Students_Info,student_roll=id)
#     return student.student_name
# register.filter('get_student_name', get_student_name)

# def get_month_name(id):
#     month_list={1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
#     month=month_list[id]
#     return month
# register.filter('get_month_name', get_month_name)