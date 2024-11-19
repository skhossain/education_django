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


class StudentPagination(LimitOffsetPagination):
    page_query_param = "offset" # this is the "page"
    page_size_query_param="limit" # this is the "page_size"
    # page_size = 5
    # max_page_size = 100

class AcademicApiView(generics.ListAPIView):
    serializer_class = Academic_Info_Serializer

    def get_queryset(self):
        queryset = Academic_Info.objects.filter()
        return queryset


class AcademicyearApiView(generics.ListAPIView):
    serializer_class = AcademicYearSerializer

    def get_queryset(self):
        academic_year = self.request.query_params.get('academic_year', None)
        queryset = Academic_Year.objects.filter().order_by('academic_year')

        if academic_year:
            queryset = queryset.filter(academic_year=academic_year)

        return queryset


class AcademicclassApiView(generics.ListAPIView):
    serializer_class = AcademicClassSerializer

    def get_queryset(self):
        class_name = self.request.query_params.get('class_name', None)
        queryset = Academic_Class.objects.filter().order_by('class_serial')
        if class_name:
            queryset = queryset.filter(class_name=class_name)

        return queryset



class eduteacherApiView(generics.ListAPIView):
    serializer_class = eduTeacherSerializer

    def get_queryset(self):
        teacher_id = self.request.query_params.get('teacher_id', None)
        # print(teacher_id,'pppppp')
        queryset = Teacher.objects.filter().order_by()
        if teacher_id:
            queryset = queryset.filter(teacher_id=teacher_id)

        return queryset
# submapping_TeacherSerializer
from rest_framework.permissions import AllowAny 

class AcademicGroupApiView(generics.ListAPIView):
    serializer_class = AcademicGroupSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        class_group_id = self.request.query_params.get('class_group_id', None)
        class_group_name = self.request.query_params.get(
            'class_group_name', None)
        class_id = self.request.query_params.get('class_id', None)
        subject_list = self.request.query_params.get('subject_list', None)
        queryset = Academic_Class_Group.objects.filter().order_by('class_group_id')
        if class_group_id:
            queryset = queryset.filter(class_group_id=class_group_id)
        if class_id:
            queryset = queryset.filter(class_id=class_id)
        if subject_list:
            queryset = queryset.filter(subject_list=subject_list)
        if class_group_name:
            queryset = queryset.filter(
                class_group_name__icontains=class_group_name)
        return queryset


class SectionInfoApiView(generics.ListAPIView):
    serializer_class = SectionInfoSerializer

    def get_queryset(self):
        section_id = self.request.query_params.get('section_id', None)
        class_id = self.request.query_params.get('class_id', None)
        queryset = Section_Info.objects.filter().order_by('section_id')
        if class_id:
            queryset = queryset.filter(class_id=class_id)
        if section_id:
            queryset = queryset.filter(section_id=section_id)

        return queryset


class SubCategoryApiView(generics.ListAPIView):
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        queryset = Subject_Category.objects.filter().order_by('category_id')
        return queryset


class SessionApiView(generics.ListAPIView):
    serializer_class = SessionSerializer

    def get_queryset(self):
        queryset = Session.objects.filter().order_by('-session_name')
        return queryset


class CategoryApiView(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Catagory_info.objects.filter().order_by('catagory_id')
        return queryset


class SubjectTypeApiView(generics.ListAPIView):
    serializer_class = SubjectTypeSerializer

    def get_queryset(self):
        subject_type_id = self.request.query_params.get(
            'subject_type_id', None)
        queryset = Subject_Type.objects.filter().order_by('subject_type_id')
        if subject_type_id:
            queryset = queryset.filter(subject_type_id=subject_type_id)

        return queryset


class SubListApiView(generics.ListAPIView):
    serializer_class = SubListSerializer

    def get_queryset(self):
        subject_name = self.request.query_params.get('subject_name', None)
        class_id = self.request.query_params.get('class_id', None)
        class_group_id = self.request.query_params.get('class_group_id', None)
        category_id = self.request.query_params.get('category_id', None)
        subject_type_id = self.request.query_params.get(
            'subject_type_id', None)

        queryset = Subject_List.objects.filter().order_by('subject_name')
        if subject_name:
            queryset = queryset.filter(subject_name=subject_name)
        if class_id:
            queryset = queryset.filter(class_id=class_id)
        if class_group_id:
            queryset = queryset.filter(class_group_id=class_group_id)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if subject_type_id:
            queryset = queryset.filter(subject_type_id=subject_type_id)
        return queryset


class DepartmentApiView(generics.ListAPIView):
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        department_id = self.request.query_params.get('department_id', None)
        queryset = Edu_Department_Info.objects.filter().order_by('department_id')
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        return queryset


class ShiftApiView(generics.ListAPIView):
    serializer_class = ShiftSerializer

    def get_queryset(self):
        shift_id = self.request.query_params.get('shift_id', None)
        # shift_name = self.request.query_params.get('shift_name',None)
        queryset = Edu_Shift_Info.objects.filter().order_by('shift_id')
        if shift_id:
            queryset = queryset.filter(shift_id=shift_id)
        # if shift_name:
        #     queryset = queryset.filter(shift_name=shift_name)

        return queryset


class DegreeApiView(generics.ListAPIView):
    serializer_class = DegreeSerializer

    def get_queryset(self):
        degree_id = self.request.query_params.get('degree_id', None)
        queryset = Degree_Info.objects.filter().order_by('degree_id')
        if degree_id:
            queryset = queryset.filter(degree_id=degree_id)

        return queryset


class OccupationApiView(generics.ListAPIView):
    serializer_class = OccupationSerializer

    def get_queryset(self):
        occupation_id = self.request.query_params.get('occupation_id', None)
        queryset = Occupation_Info.objects.filter().order_by('occupation_id')
        if occupation_id:
            queryset = queryset.filter(occupation_id=occupation_id)

        return queryset


class EdicatopnApiView(generics.ListAPIView):
    serializer_class = EdocationSerializer

    def get_queryset(self):
        institute_id = self.request.query_params.get('institute_id', None)
        queryset = Education_Institute.objects.filter().order_by('institute_id')
        if institute_id:
            queryset = queryset.filter(institute_id=institute_id)

        return queryset


class StudentInfoApiView(generics.ListAPIView):
    serializer_class = StudentInfoSerializer
    pagination_class = StudentPagination

    def get_queryset(self):
        branch_code = self.request.query_params.get('branch_code',None)
        student_roll = self.request.query_params.get('student_roll',None)
        academic_year = self.request.query_params.get('academic_year',None)
        class_id = self.request.query_params.get('class_id',None)
        class_roll = self.request.query_params.get('class_roll',None)
        class_group_id = self.request.query_params.get('class_group_id',None)
        session_id = self.request.query_params.get('session_id',None)
        catagory_id = self.request.query_params.get('catagory_id',None)
        student_phone = self.request.query_params.get('student_phone',None)
        section_id = self.request.query_params.get('section_id',None)
        shift_id = self.request.query_params.get('shift_id',None)
        search = self.request.query_params.get('search',None)
        is_head_office_user = self.request.session["is_head_office_user"]



        from_academic_year = self.request.query_params.get('from_academic_year',None)
        from_class = self.request.query_params.get('from_class',None)
        from_section = self.request.query_params.get('from_section',None)
        from_class_group = self.request.query_params.get('from_class_group',None)
        student_id = self.request.query_params.get('student_id',None)

        # if is_head_office_user == 'Y':
        #     branch_code = None
        # else:
        #     branch_code = self.request.query_params.get('branch_code', None)

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

        return queryset


class AdmissionApiView(generics.ListAPIView):
    serializer_class = AdmissionSerializer

    def get_queryset(self):
        student_roll = self.request.query_params.get('student_roll', None)
        queryset = Student_Admission.objects.filter().order_by('student_roll')
        return queryset


class ResultGradeApiView(generics.ListAPIView):
    serializer_class = ResultGradeSerializer

    def get_queryset(self):
        grade_name = self.request.query_params.get('grade_name', None)
        out_of = self.request.query_params.get('out_of', None)
        result_gpa = self.request.query_params.get('result_gpa', None)
        queryset = Result_Grade.objects.filter().order_by('-result_gpa', 'grade_name')
        if grade_name:
            queryset = queryset.filter(grade_name=grade_name)
        if out_of:
            queryset = queryset.filter(out_of=out_of)
        if result_gpa:
            queryset = queryset.filter(result_gpa=result_gpa)
        return queryset


class ExamTypeApiView(generics.ListAPIView):
    serializer_class = ExamTypeSerializer

    def get_queryset(self):
        examtype_id = self.request.query_params.get('examtype_id', None)
        queryset = Exam_Type.objects.filter().order_by('examtype_id')
        if examtype_id:
            queryset = queryset.filter(examtype_id=examtype_id)
        return queryset


class ExamSetupApiView(generics.ListAPIView):
    serializer_class = ExamSetupSerializer

    def get_queryset(self):
        branch_code = self.request.query_params.get('branch_code', None)
        exam_id = self.request.query_params.get('exam_id', None)
        academic_year = self.request.query_params.get('academic_year', None)
        term_id = self.request.query_params.get('term_id', None)
        class_id = self.request.query_params.get('class_id', None)
        class_group_id = self.request.query_params.get('class_group_id', None)
        subject_id = self.request.query_params.get('subject_id', None)
        session_id = self.request.query_params.get('session_id', None)
        queryset = Exam_Setup.objects.filter().order_by('exam_id')
        if subject_id and academic_year and term_id and class_id and branch_code:
            queryset = queryset.filter(
                branch_code=branch_code,subject_id=subject_id, academic_year=academic_year, term_id=term_id, class_id=class_id)
        if branch_code:
            queryset = queryset.filter(branch_code=branch_code)
        if term_id:
            queryset = queryset.filter(term_id=term_id)
        if exam_id:
            queryset = queryset.filter(exam_id=exam_id)
        if academic_year:
            queryset = queryset.filter(academic_year=academic_year)
        if class_id:
            queryset = queryset.filter(class_id=class_id)
        if class_group_id:
            queryset = queryset.filter(class_group_id=class_group_id)
        if session_id:
            queryset = queryset.filter(session_id=session_id)
        return queryset

class ResultViewSettingApiView(generics.ListAPIView):
    serializer_class = ResultViewSettingSerializer

    def get_queryset(self):
        branch_code = self.request.query_params.get('branch_code', None)
        academic_year = self.request.query_params.get('academic_year', None)
        term_id = self.request.query_params.get('term_id', None)
        class_id = self.request.query_params.get('class_id', None)
        class_group_id = self.request.query_params.get('class_group_id', None)
        session_id = self.request.query_params.get('session_id', None)
        queryset = result_view_setting.objects.filter().order_by('short_number')

        if branch_code:
            queryset = queryset.filter(branch_code=branch_code)
        if term_id:
            queryset = queryset.filter(term_id=term_id)
        if academic_year:
            queryset = queryset.filter(academic_year=academic_year)
        if class_id:
            queryset = queryset.filter(class_id=class_id)
        if class_group_id:
            queryset = queryset.filter(class_group_id=class_group_id)
        if session_id:
            queryset = queryset.filter(session_id=session_id)
        return queryset


class MarkDetailsApiView(generics.ListAPIView):
    serializer_class = MarkDetailSerializer

    def get_queryset(self):
        # id = self.request.query_params.get('id',None)
        academic_year = self.request.query_params.get('academic_year', None)
        class_id = self.request.query_params.get('class_id', None)
        student_roll = self.request.query_params.get('student_roll', None)
        subject_id = self.request.query_params.get('subject_id', None)
        exam_id = self.request.query_params.get('exam_id', None)
        exam_no = self.request.query_params.get('exam_no', None)
        queryset = Exam_Marks_Details.objects.filter().order_by('exam_id')
        if academic_year and class_id and student_roll and subject_id and exam_id and exam_no:
            queryset = queryset.filter(academic_year=academic_year, class_id=class_id,
                                       student_roll=student_roll, subject_id=subject_id, exam_id=exam_id, exam_no=exam_no)
            return queryset
        if academic_year:
            queryset = queryset.filter(academic_year=academic_year)
        if class_id:
            queryset = queryset.filter(class_id=class_id)
        if student_roll:
            queryset = queryset.filter(student_roll=student_roll)
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)
        if exam_id:
            queryset = queryset.filter(exam_id=exam_id)
        if exam_no:
            queryset = queryset.filter(exam_no=exam_no)
        return queryset


class FinalMarksApiView(generics.ListAPIView):
    serializer_class = FinalMarksSerializer

    def get_queryset(self):
        id = self.request.query_params.get('id', None)
        class_id = self.request.query_params.get('class_id', None)
        class_group_id = self.request.query_params.get('class_group_id', None)
        term_id = self.request.query_params.get('term_id', None)
        queryset = Exam_Marks_Final.objects.filter().order_by('id')
        if id:
            queryset = queryset.filter(id=id)
        if class_id:
            queryset = queryset.filter(class_id=class_id)
        if class_group_id:
            queryset = queryset.filter(class_group_id=class_group_id)
        if term_id:
            queryset = queryset.filter(term_id=term_id)
        return queryset


class OnlineExamApiView(generics.ListAPIView):
    serializer_class = OnlineExamSerializer

    def get_queryset(self):
        id = self.request.query_params.get('id', None)
        queryset = Online_Exam_Information.objects.filter().order_by('online_exam_id')
        if id:
            queryset = queryset.filter(online_exam_id=id)
        return queryset


class OnlineExamQuestionApiView(generics.ListAPIView):
    serializer_class = OnlineExamQuestionSerializer

    def get_queryset(self):
        id = self.request.query_params.get('id', None)
        queryset = Online_Exam_Questions.objects.filter().order_by('question_id')
        if id:
            queryset = queryset.filter(question_id=id)
        return queryset


class Visited_Student_InfoApiView(generics.ListAPIView):
    serializer_class = Visited_Student_InfoSerializer

    def get_queryset(self):
        id = self.request.query_params.get('id', None)
        class_id = self.request.query_params.get('class_id', None)
        class_group_id = self.request.query_params.get('class_group_id', None)
        student_phone = self.request.query_params.get('student_phone', None)
        queryset = Visited_Student_Info.objects.filter().order_by('student_name')
        if id:
            queryset = queryset.filter(id=id)
        if class_id:
            queryset = queryset.filter(class_id=class_id)
        if class_group_id:
            queryset = queryset.filter(class_group_id=class_group_id)
        if student_phone:
            queryset = queryset.filter(student_phone=student_phone)
        return queryset


class Student_AttendenceApiView(generics.ListAPIView):
    serializer_class = Present_sheet_infoSerializer

    def get_queryset(self):
        present_sheet_info_id = self.request.query_params.get(
            'present_sheet_info_id', None)
        academic_year = self.request.query_params.get('academic_year', None)
        month_number = self.request.query_params.get('month_number', None)
        class_id = self.request.query_params.get('class_id', None)
        class_group_id = self.request.query_params.get('class_group_id', None)
        section_id = self.request.query_params.get('section_id', None)
        subject_id = self.request.query_params.get('subject_id', None)
        queryset = Present_sheet_info.objects.filter().order_by('present_sheet_info_id')
        if academic_year:
            queryset = queryset.filter(academic_year=academic_year)

        if month_number:
            queryset = queryset.filter(month_number=month_number)

        if class_id:
            queryset = queryset.filter(class_id=class_id)

        if class_group_id:
            queryset = queryset.filter(class_group_id=class_group_id)

        if section_id:
            queryset = queryset.filter(section_id=section_id)

        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)

        if present_sheet_info_id:
            queryset = queryset.filter(
                present_sheet_info_id=present_sheet_info_id)

        return queryset


class LibraryRackApiView(generics.ListAPIView):
    serializer_class = LibraryRackSerializer

    def get_queryset(self):
        queryset = Library_Rack.objects.filter().order_by('rack_id')
        return queryset


class LibraryAuthorApiView(generics.ListAPIView):
    serializer_class = LibraryAuthorSerializer

    def get_queryset(self):
        queryset = Library_Author.objects.filter().order_by('author_id')
        return queryset


class LibraryEditorApiView(generics.ListAPIView):
    serializer_class = LibraryEditorSerializer

    def get_queryset(self):
        queryset = Library_Editor.objects.filter().order_by('editor_id')
        return queryset


class LibraryBookApiView(generics.ListAPIView):
    serializer_class = LibraryBookSerializer

    def get_queryset(self):
        queryset = Library_Books.objects.filter().order_by('book_id')
        return queryset


class LibraryCardApiView(generics.ListAPIView):
    serializer_class = LibraryCardSerializer

    def get_queryset(self):
        queryset = Library_Card.objects.filter().order_by('card_number')
        return queryset


class LibraryBookIssueApiView(generics.ListAPIView):
    serializer_class = LibraryBookIssueSerializer

    def get_queryset(self):
        queryset = Library_Book_Issue.objects.filter().order_by('issue_id')
        return queryset


class LibraryBookRequestApiView(generics.ListAPIView):
    serializer_class = LibraryBookRequestSerializer

    def get_queryset(self):
        queryset = Library_Book_Request.objects.filter().order_by('request_id')
        return queryset


class ClassRoomApiView(generics.ListAPIView):
    serializer_class = ClassRoomSerializer

    def get_queryset(self):
        queryset = Class_Room.objects.filter().order_by('room_id')
        return queryset


class ClassRoutineApiView(generics.ListAPIView):
    serializer_class = ClassRoutineSerializer

    def get_queryset(self):
        queryset = Class_Routine.objects.filter().order_by('-app_data_time')
        return queryset


class RoutineDetailsApiView(generics.ListAPIView):
    serializer_class = RoutineDetailsSerializer

    def get_queryset(self):
        academic_year = self.request.query_params.get('academic_year', None)
        class_id = self.request.query_params.get('class_id', None)
        subject_id = self.request.query_params.get('subject_id', None)
        teacher_id = self.request.query_params.get('teacher_id', None)
        room_id = self.request.query_params.get('room_id', None)
        start_time = self.request.query_params.get('start_time', None)
        end_time = self.request.query_params.get('end_time', None)
        day = self.request.query_params.get('day', None)
        days = day.split(',')
        class_group_id = self.request.query_params.get('class_group_id', None)
        shift_id = self.request.query_params.get('shift_id', None)
        section_id = self.request.query_params.get('section_id', None)

        queryset = Class_Routine_Details.objects.filter().order_by('-routine_details_id')
        if academic_year:
            queryset = queryset.filter(academic_year=academic_year)
        if class_id:
            queryset = queryset.filter(class_id=class_id)
        if room_id:
            queryset = queryset.filter(room_id=room_id)
        if teacher_id:
            queryset = queryset.filter(teacher_id=teacher_id)
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)
        if class_group_id:
            queryset = queryset.filter(class_group_id=class_group_id)
        if shift_id:
            queryset = queryset.filter(shift_id=shift_id)
        if section_id:
            queryset = queryset.filter(section_id=section_id)
        if day:
            queryset = queryset.filter(day__in=days)
        if start_time and end_time:
            queryset = queryset.filter(
                Q(start_time__lte=end_time, end_time__gte=start_time))
        return queryset


class TeacherApiView(generics.ListAPIView):
    serializer_class = TeacherSerializer

    def get_queryset(self):
        queryset = Mapping_Guide_Teacher.objects.filter().order_by('teacher_id')
        return queryset


class CategoryApiView(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Catagory_info.objects.filter().order_by('catagory_id')
        return queryset


class SubjectChoiceApiView(generics.ListAPIView):
    serializer_class = SubjectChoiceSerializer

    def get_queryset(self):
        academic_year = self.request.query_params.get('academic_year', None)
        class_id = self.request.query_params.get('class_id', None)
        class_group_id = self.request.query_params.get('class_group_id', None)
        session_id = self.request.query_params.get('session_id', None)
        student_roll = self.request.query_params.get('student_roll', None)
        queryset = Subject_Choice.objects.filter().order_by('student_roll')
        if academic_year:
            queryset = queryset.filter(academic_year=academic_year)
        if class_id:
            queryset = queryset.filter(class_id=class_id)
        if class_group_id:
            queryset = queryset.filter(class_group_id=class_group_id)
        if session_id:
            queryset = queryset.filter(session_id=session_id)
        if student_roll:
            queryset = queryset.filter(student_roll=student_roll)

        return queryset


class TCApiView(generics.ListAPIView):
    serializer_class = TCSerializer

    def get_queryset(self):
        queryset = Transfer_Certificate.objects.filter().order_by('tc_id')
        return queryset


class ExamAttendanceApiView(generics.ListAPIView):
    serializer_class = ExamAttendanceSerializer

    def get_queryset(self):
        queryset = Exam_Attendance.objects.filter().order_by('exam_atten_id')
        return queryset


class FeesHeadSettingApiView(generics.ListAPIView):
    serializer_class = FeesHeadSettingSerializer

    def get_queryset(self):
        queryset = Fees_Head_Settings.objects.filter().order_by('head_code')
        return queryset


class FeesWaiverApiView(generics.ListAPIView):
    serializer_class = FeesWaiverSerializer

    def get_queryset(self):
        queryset = Fees_Waiver.objects.filter().order_by('waive_code')
        return queryset


class FeesWaiverMappingApiView(generics.ListAPIView):
    serializer_class = FeesWaiverMappingSerializer

    def get_queryset(self):
        queryset = Fees_Waiver_Mapping.objects.filter()
        return queryset


class FeesMappingApiView(generics.ListAPIView):
    serializer_class = FeesMappingSerializer

    def get_queryset(self):
        queryset = Fees_Mapping.objects.filter().order_by('class_id')
    
        head_code = self.request.query_params.get('head_code', None)
        class_id = self.request.query_params.get('class_id', None)
        class_group_id = self.request.query_params.get('class_group_id', None)
        section_id = self.request.query_params.get('section_id', None)
        effective_date = self.request.query_params.get('effective_date', None)
        fee_amount = self.request.query_params.get('fee_amount', None)
        fine_amount = self.request.query_params.get('fine_amount', None)
        pay_freq = self.request.query_params.get('pay_freq', None)
        academic_year = self.request.query_params.get('academic_year', None)

        filterData = dict()
        if head_code:
            filterData['head_code'] = head_code
        if section_id:
            filterData['section_id'] = section_id
        if effective_date:
            filterData['effective_date'] = effective_date
        if pay_freq:
            filterData['pay_freq'] = pay_freq
        if class_id:
            filterData['class_id'] = class_id
        if class_group_id:
            filterData['class_group_id'] = class_group_id
        if academic_year:
            filterData['academic_year'] = academic_year
        queryset = Fees_Mapping.objects.filter(
            **filterData).order_by('head_code')

        return queryset


class AbsFineMappingApiView(generics.ListAPIView):
    serializer_class = AbsFineMappingSerializer

    def get_queryset(self):
        queryset = Absent_Fine_Mapping.objects.filter().order_by('class_id')
        return queryset


class FeesWaiverStudentApiView(generics.ListAPIView):
    serializer_class = FeesWaiverStudentSerializer

    def get_queryset(self):
        branch_code = self.request.query_params.get('branch_code', None)
        student_roll = self.request.query_params.get('student_roll', None)
        fees_month = self.request.query_params.get('fees_month', None)
        fees_year = self.request.query_params.get('fees_year', None)
        effective_date = self.request.query_params.get('effective_date', None)
        head_code = self.request.query_params.get('head_code', None)
        
        queryset = Fees_Waive_Student.objects.filter().order_by('-app_data_time')
        
        if branch_code:
            queryset = queryset.filter(branch_code=branch_code)
        if student_roll:
            queryset = queryset.filter(student_roll=student_roll)
            
        if fees_month:
            queryset = queryset.filter(fees_month=fees_month)
        if fees_year:
            queryset = queryset.filter(fees_year=fees_year)
        if effective_date:
            queryset = queryset.filter(effective_date=effective_date)
        if head_code:
            queryset = queryset.filter(head_code=head_code)
            
            
        return queryset


class ExamTermApiView(generics.ListAPIView):
    serializer_class = ExamTermSerializer

    def get_queryset(self):
        queryset = Exam_Term.objects.filter().order_by('id')
        return queryset


class IDCardApiView(generics.ListAPIView):
    serializer_class = IDCardSerializer

    def get_queryset(self):
        queryset = Student_ID_Card.objects.filter().order_by('class_id')
        academic_Year = self.request.query_params.get('academic_Year', None)
        class_id = self.request.query_params.get('class_id', None)
        class_group_id = self.request.query_params.get('class_group_id', None)
        student_roll = self.request.query_params.get('student_roll', None)
        branch_code = self.request.query_params.get('branch_code', None)
        expire_date = self.request.query_params.get('expire_date', None)
        filterData = dict()
        if class_id:
            filterData['class_id'] = class_id
        if class_group_id:
            filterData['class_group_id'] = class_group_id
        if academic_Year:
            filterData['academic_Year'] = academic_Year
        if student_roll:
            filterData['student_roll'] = student_roll
        if branch_code:
            filterData['branch_code'] = branch_code
        if expire_date:
            filterData['expire_date__date'] = expire_date
        queryset = Student_ID_Card.objects.filter(
            **filterData).order_by('class_id')
        return queryset


class AdmitCardApiView(generics.ListAPIView):
    serializer_class = AdmitCardSerializer

    def get_queryset(self):
        queryset = Student_Admit_Card.objects.filter().order_by('admit_card_id')
        academic_year = self.request.query_params.get('academic_year', None)
        branch_code = self.request.query_params.get('branch_code', None)
        class_id = self.request.query_params.get('class_id', None)
        class_group_id = self.request.query_params.get('class_group_id', None)
        student_roll = self.request.query_params.get('student_roll', None)
        session_id = self.request.query_params.get('session_id', None)
        exam_term_id = self.request.query_params.get('exam_term_id', None)
        filterData = dict()
        if branch_code:
            filterData['branch_code'] = branch_code
        if class_id:
            filterData['class_id'] = class_id
        if class_group_id:
            filterData['class_group_id'] = class_group_id
        if academic_year:
            filterData['academic_year'] = academic_year
        if student_roll:
            filterData['student_roll'] = student_roll
        if session_id:
            filterData['session_id'] = session_id
        if exam_term_id:
            filterData['exam_term_id'] = exam_term_id
        queryset = Student_Admit_Card.objects.filter(
            **filterData).order_by('student_roll__class_roll')
        return queryset


class CourseRegApiView(generics.ListAPIView):
    serializer_class = CourseRegSerializer

    def get_queryset(self):
        queryset = Course_Registrations.objects.filter().order_by('student_roll')
        class_id = self.request.query_params.get('class_id', None)
        student_roll = self.request.query_params.get('student_roll', None)
        reg_no = self.request.query_params.get('reg_no', None)
        filterData = dict()
        if class_id:
            filterData['class_id'] = class_id
        if student_roll:
            filterData['student_roll'] = student_roll
        if reg_no:
            filterData['reg_no'] = reg_no
        queryset = Course_Registrations.objects.filter(
            **filterData).order_by('student_roll')
        return queryset


class SeatPlaneApiView(generics.ListAPIView):
    serializer_class = SeatPlaneSerializer

    def get_queryset(self):
        queryset = Student_Seat_plane.objects.filter().order_by('student_roll')
        class_id = self.request.query_params.get('class_id', None)
        student_roll = self.request.query_params.get('student_roll', None)
        academic_year = self.request.query_params.get('academic_year', None)
        class_group_id = self.request.query_params.get('class_group_id', None)
        filterData = dict()
        if class_id:
            filterData['class_id'] = class_id
        if student_roll:
            filterData['student_roll'] = student_roll
        if academic_year:
            filterData['academic_year'] = academic_year
        if class_group_id:
            filterData['class_group_id'] = class_group_id
        queryset = Student_Seat_plane.objects.filter(
            **filterData).order_by('student_roll')
        return queryset


class NamePlateApiView(generics.ListAPIView):
    serializer_class = NamePlateSerializer

    def get_queryset(self):
        queryset = Student_Name_Plate.objects.filter().order_by('student_roll')
        class_id = self.request.query_params.get('class_id', None)
        student_roll = self.request.query_params.get('student_roll', None)
        academic_year = self.request.query_params.get('academic_year', None)
        class_group_id = self.request.query_params.get('class_group_id', None)
        filterData = dict()
        if class_id:
            filterData['class_id'] = class_id
        if student_roll:
            filterData['student_roll'] = student_roll
        if academic_year:
            filterData['academic_year'] = academic_year
        if class_group_id:
            filterData['class_group_id'] = class_group_id
        queryset = Student_Name_Plate.objects.filter(
            **filterData).order_by('student_roll')
        return queryset


class Fees_Receive_Summary_ApiView(generics.ListAPIView):
    serializer_class = Fees_Receive_Summary_Serializer

    def get_queryset(self):
        student_roll = self.request.query_params.get('student_roll', None)
        from_date = self.request.query_params.get('from_date', None)
        upto_date = self.request.query_params.get('upto_date', None)
        receive_date = None

        if from_date == upto_date:
            receive_date = upto_date
            from_date = None
            upto_date = None

        queryset = Fees_Receive_Summary.objects.filter().order_by('id')

        if student_roll:
            queryset = queryset.filter(student_roll=student_roll)

        if receive_date:
            queryset = queryset.filter(receive_date=receive_date)

        if from_date:
            queryset = queryset.filter(receive_date__gte=from_date)

        if upto_date:
            queryset = queryset.filter(receive_date__lte=upto_date)

        return queryset

class Fees_Processing_Details_ApiView(generics.ListAPIView):
    serializer_class = Fees_Processing_Details_Serializer

    def get_queryset(self):
        queryset = Fees_Processing_Details.objects.filter().order_by('class_id')
        return queryset

class Admission_form_header_ApiView(generics.ListAPIView):
    serializer_class = Admission_form_header_Serializer

    def get_queryset(self):
        branch_code = self.request.query_params.get('branch_code', None)
        queryset = Admission_form_header.objects.filter().order_by()
        if branch_code:
            queryset=queryset.filter(branch_code=branch_code)
        return queryset


class IdCard_form_header_ApiView(generics.ListAPIView):
    serializer_class = IdCard_form_header_Serializer

    def get_queryset(self):
        branch_code = self.request.query_params.get('branch_code', None)
        queryset = IdCard_form_header.objects.filter().order_by()
        if branch_code:
            queryset=queryset.filter(branch_code=branch_code)
        return queryset

class SubmappingTeacherApiView(generics.ListAPIView):
    serializer_class = submapping_TeacherSerializer

    def get_queryset(self):
        # teacher_id = self.request.query_params.get('teacher_id', None)
        # print(teacher_id,'pppppp')
        queryset = subject_mapping_teacher.objects.filter().order_by()
        # if teacher_id:
        #     queryset = queryset.filter(teacher_id=teacher_id)

        return queryset
    
class Board_Name_ApiView(generics.ListAPIView):
    serializer_class = Board_NameSerializer

    def get_queryset(self):
        branch_code = self.request.query_params.get('branch_code', None)
        queryset = Education_Board.objects.filter().order_by()
        if branch_code:
            queryset=queryset.filter(branch_code=branch_code)
        return queryset

class Certificate_Name_ApiView(generics.ListAPIView):
    serializer_class = Certificate_NameSerializer

    def get_queryset(self):
        branch_code = self.request.query_params.get('branch_code', None)
        queryset = Certificat_Name.objects.filter().order_by()
        if branch_code:
            queryset=queryset.filter(branch_code=branch_code)
        return queryset

class Testimonial_ApiView(generics.ListAPIView):
    serializer_class = TestimonialSerializer

    def get_queryset(self):
        branch_code = self.request.query_params.get('branch_code', None)
        testimonial_id = self.request.query_params.get('testimonial_id', None)
        student_roll = self.request.query_params.get('student_roll', None)
        academic_year = self.request.query_params.get('academic_year', None)
        cerfificate_name = self.request.query_params.get('cerfificate_name', None)
        queryset = Testimonial.objects.filter().order_by()
        if branch_code:
            queryset=queryset.filter(branch_code=branch_code)
        if testimonial_id:
            queryset=queryset.filter(testmonial_id=testimonial_id)
        if student_roll:
            queryset=queryset.filter(student_roll=student_roll)
        if academic_year:
            queryset=queryset.filter(academic_year=academic_year)
        if cerfificate_name:
            queryset=queryset.filter(cert_name_id=cerfificate_name)
        return queryset


