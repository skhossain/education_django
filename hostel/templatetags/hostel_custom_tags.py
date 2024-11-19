from ..models import *
from django import template
from django.shortcuts import get_object_or_404
from django.db.models import Count, Sum, Avg

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

def dateroll_list(roll,date):
    return [roll,date]
register.filter('dateroll_list', dateroll_list)

def get_meal_number(dateroll):
    meal=Daily_Meal.objects.values('meal_id__meal_type_id__meal_type_name').filter(student_roll=dateroll[0],date=dateroll[1],cancel_on__isnull=True).annotate(total=Sum('is_eat'))
    return meal
register.filter('get_meal_number', get_meal_number)

def get_meal_number_cancel(dateroll):
    meal=Daily_Meal.objects.filter(student_roll=dateroll[0],date=dateroll[1],cancel_on__isnull=True)
    meal_info= meal.values('meal_id__meal_name','meal_id','date').filter(student_roll=dateroll[0],date=dateroll[1],cancel_on__isnull=True).annotate(total=Sum('is_eat'))
    return meal_info
register.filter('get_meal_number_cancel', get_meal_number_cancel)

def get_total_meal(dateroll):
    dates=[]
    for d in dateroll[1]:
        dates.append(d['date'])
    meals=Daily_Meal.objects.filter(student_roll=dateroll[0],date__in=dates,cancel_on__isnull=True)
    meal=meals.values('meal_id__meal_name').annotate(total=Sum('is_eat'))
    # meal_number=Daily_Meal.objects.values('meal_id__meal_name').filter(student_roll=dateroll[0],date__in=dates,meal_id__meal_type_id=meal_type).count()
    return meal
register.filter('get_total_meal', get_total_meal)
