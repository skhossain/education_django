from django.db.models.aggregates import Count, Sum
from ..models import *
from ..utils import *
from django import template
from django.shortcuts import get_object_or_404

register = template.Library()


def get_exam_name(a):
    exam_name = Exam_Setup.objects.get(exam_id=a)
    return exam_name


register.filter('get_exam_name', get_exam_name)


def get_degree_name(id):
    name = Degree_Info.objects.get(degree_id=id)
    return name


register.filter('get_degree_name', get_degree_name)


def get_institute_name(id):
    name = Education_Institute.objects.get(institute_id=id)
    return name


register.filter('get_institute_name', get_institute_name)


def get_student_name(id):
    student = get_object_or_404(Students_Info, student_roll=id)
    return student.student_name


register.filter('get_student_name', get_student_name)


def get_month_name(id):
    month_list = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                  7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    month = month_list[id]
    return month


register.filter('get_month_name', get_month_name)


def get_week_name(id):
    # Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday and Monday
    if type(id) == str:
        id = int(id)
    day_list = {1: 'Saturday', 2: 'Sunday', 3: 'Monday',
                4: 'Tuesday', 5: 'Wednesday', 6: 'Thursday', 7: 'Friday'}
    day = day_list[id]
    return day


register.filter('get_week_name', get_week_name)


def get_student_term_exam_mark(info):
    academic_year = info['academic_year']
    class_id = info['class_id']
    term_id = info['term_id']
    student_roll = info['student_roll']
    class_info=get_object_or_404(Academic_Class,class_id=class_id)
    exam_list = Store_Exam_Single_Mark.objects.filter(
        academic_year=academic_year, class_id=class_id, term_id=term_id, student_roll=student_roll)
    subject_marks = exam_list.values('subject_id').annotate(total_mark=Sum(
        'total_exam_marks'), ob_mark=Sum('obtain_marks'), gpa=Sum('grade_point_average'),)
    for sm in subject_marks:
        result = get_result_great(sm['ob_mark'], sm['total_mark'],class_info.out_of)
        sm['subject_gpa'] = result[0]
        sm['subject_lg'] = result[1]
    data = dict()
    data['exam_list'] = exam_list
    data['subject_marks'] = subject_marks
    return data


register.filter('get_student_term_exam_mark', get_student_term_exam_mark)


def get_student_term_final(info):
    academic_year = info['academic_year']
    class_id = info['class_id']
    term_id = info['term_id']
    student_roll = info['student_roll']
    term_final = Exam_Marks_Final.objects.filter(
        academic_year=academic_year, class_id=class_id, term_id=term_id, student_roll=student_roll).first()
    data = dict()
    data['term_final'] = term_final
    return data
register.filter('get_student_term_final', get_student_term_final)

def get_merge_subject_marks(info):
    data_filter=dict()
    data_filter['academic_year']=info['shearch'][0]['academic_year']
    data_filter['class_id']=info['shearch'][0]['class_id']
    data_filter['student_roll']=info['shearch'][0]['student_roll']
    term_id=[info['shearch'][0]['term_id']]
    term_id.append(info['shearch'][1]['term_id'])
    data_filter['term_id__in']=term_id
    class_info=get_object_or_404(Academic_Class,class_id=info['shearch'][0]['class_id'])
    exam_list = Store_Exam_Single_Mark.objects.filter(**data_filter)
    subject_marks = exam_list.values('subject_id','subject_id__subject_name').annotate(total_mark=Sum(
        'total_exam_marks'), ob_mark=Sum('obtain_marks'), gpa=Sum('grade_point_average'),)
    for sm in subject_marks:
        result = get_result_great(sm['ob_mark'], sm['total_mark'],class_info.out_of)
        sm['subject_gpa'] = result[0]
        sm['subject_lg'] = result[1]
    return subject_marks
register.filter('get_merge_subject_marks', get_merge_subject_marks)

def get_student_subject_mark(info,result):
    academic_year=result.academic_year
    term_id=result.term_id.id
    class_id= result.class_id.class_id
    student_roll=result.student_roll.student_roll
    class_info=get_object_or_404(Academic_Class,class_id=class_id)
    subject_id=info['subject_id']
    data_filter=info['filter']
    
    data_filter['academic_year']=academic_year
    data_filter['term_id']=term_id
    data_filter['class_id']=class_id
    data_filter['subject_id']=subject_id
    data_filter['student_roll']=student_roll
    exam_list = Store_Exam_Single_Mark.objects.filter(**data_filter)
    
    subject_marks = exam_list.values('subject_id','subject_id__subject_name').annotate(total_mark=Sum(
        'total_exam_marks'), ob_mark=Sum('obtain_marks'), gpa=Sum('grade_point_average'),)
    for sm in subject_marks:
        result = get_result_great(sm['ob_mark'], sm['total_mark'],class_info.out_of)
        sm['subject_gpa'] = result[0]
        sm['subject_lg'] = result[1]
    return subject_marks
register.filter('get_student_subject_mark', get_student_subject_mark)


