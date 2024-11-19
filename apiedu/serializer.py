from edu.forms import SubjectListModelForm
from rest_framework import serializers
import datetime

from edu.models import *
from edu.models import Shift_Info as Edu_Shift_Info
from edu.models import Department_Info as Edu_Department_Info
from edu.models import Application_Settings as Academic_Info
from apihrm.serializers import *
from apiauth.serializers import *
from hrm.models import Employee_Details


class Academic_Info_Serializer(serializers.ModelSerializer):
    academic_logo = serializers.SerializerMethodField('get_images')

    def get_images(self, instance):
        return instance.academic_logo.url

    class Meta:
        model = Academic_Info
        fields = ('__all__')


class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Academic_Year
        fields = ('__all__')


class AcademicClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Academic_Class
        fields = ('__all__')


class AcademicGroupSerializer(serializers.ModelSerializer):
    class_id = AcademicClassSerializer()

    class Meta:
        model = Academic_Class_Group
        fields = ('__all__')


class SectionInfoSerializer(serializers.ModelSerializer):
    class_id = AcademicClassSerializer()

    class Meta:
        model = Section_Info
        fields = ('__all__')


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject_Category
        fields = ('__all__')


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('__all__')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Catagory_info
        fields = ('__all__')


class SubjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject_Type
        fields = ('__all__')


class SubListSerializer(serializers.ModelSerializer):
    class_id = AcademicClassSerializer()
    class_group_id = AcademicGroupSerializer()
    subject_type_id = SubjectTypeSerializer()
    category_id = SubCategorySerializer()

    class Meta:
        model = Subject_List
        fields = ('__all__')


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edu_Department_Info
        fields = ('__all__')


class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edu_Shift_Info
        fields = ('__all__')


class DegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Degree_Info
        fields = ('__all__')


class OccupationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occupation_Info
        fields = ('__all__')


class EdocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education_Institute
        fields = ('__all__')


class StudentInfoSerializer(serializers.ModelSerializer):
    academic_year = AcademicYearSerializer()
    catagory_id = CategorySerializer()
    session_id = SessionSerializer()
    class_id = AcademicClassSerializer()
    class_group_id = AcademicGroupSerializer()
    shift_id = ShiftSerializer()
    section_id = SectionInfoSerializer()

    profile_image = serializers.SerializerMethodField('get_profile_image')

    def get_profile_image(self, instance):
        if instance.profile_image:
            return instance.profile_image.url
        else:
            return None

    student_signature = serializers.SerializerMethodField(
        'get_signature_image')

    def get_signature_image(self, instance):
        if instance.student_signature:
            return instance.student_signature.url
        else:
            return None

    class Meta:
        model = Students_Info
        fields = ('__all__')
        


class AdmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student_Admission
        fields = ('__all__')


class ResultGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result_Grade
        fields = ('__all__')


class ExamTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam_Type
        fields = ('__all__')


class ExamTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam_Term
        fields = ('__all__')


class ExamSetupSerializer(serializers.ModelSerializer):
    academic_year = AcademicYearSerializer()
    examtype_id = ExamTypeSerializer()
    class_id = AcademicClassSerializer()
    class_group_id = AcademicGroupSerializer()
    subject_id = SubListSerializer()
    term_id = ExamTermSerializer()

    class Meta:
        model = Exam_Setup
        fields = ('__all__')
class ResultViewSettingSerializer(serializers.ModelSerializer):
    academic_year = AcademicYearSerializer()
    class_id = AcademicClassSerializer()
    class_group_id = AcademicGroupSerializer()
    subject_one_id = SubListSerializer()
    subject_two_id = SubListSerializer()
    subject_three_id = SubListSerializer()
    term_id = ExamTermSerializer()
    session_id = SessionSerializer()

    class Meta:
        model = result_view_setting
        fields = ('__all__')


class MarkDetailSerializer(serializers.ModelSerializer):
    academic_year = AcademicYearSerializer()

    class Meta:
        model = Exam_Marks_Details
        fields = ('__all__')


class FinalMarksSerializer(serializers.ModelSerializer):
    academic_year = AcademicYearSerializer()
    class_id = AcademicClassSerializer()
    class_group_id = AcademicGroupSerializer()
    term_id = ExamTermSerializer()
    student_roll = StudentInfoSerializer()

    class Meta:
        model = Exam_Marks_Final
        fields = ('__all__')


class OnlineExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Online_Exam_Information
        fields = ('__all__')


class OnlineExamQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Online_Exam_Questions
        fields = ('__all__')


class Visited_Student_InfoSerializer(serializers.ModelSerializer):
    class_id = AcademicClassSerializer()
    class_group_id = AcademicGroupSerializer()

    class Meta:
        model = Visited_Student_Info
        fields = ('__all__')


class Present_sheet_infoSerializer(serializers.ModelSerializer):
    academic_year = AcademicYearSerializer()
    class_id = AcademicClassSerializer()
    class_group_id = AcademicGroupSerializer()
    section_id = SectionInfoSerializer()
    subject_id = SubListSerializer()

    class Meta:
        model = Present_sheet_info
        fields = ('__all__')


class LibraryRackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Library_Rack
        fields = ('__all__')


class LibraryAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Library_Author
        fields = ('__all__')


class LibraryEditorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Library_Editor
        fields = ('__all__')


class LibraryBookSerializer(serializers.ModelSerializer):
    author_id = LibraryAuthorSerializer()
    editor_id = LibraryEditorSerializer()
    rack_id = LibraryRackSerializer()

    class Meta:
        model = Library_Books
        fields = ('__all__')


class LibraryCardSerializer(serializers.ModelSerializer):
    student_roll = StudentInfoSerializer()
    teacher_id = EmpDtlSerializer()

    class Meta:
        model = Library_Card
        fields = ('__all__')


class LibraryBookIssueSerializer(serializers.ModelSerializer):
    book_id = LibraryBookSerializer()
    card_number = LibraryCardSerializer()

    class Meta:
        model = Library_Book_Issue
        fields = ('__all__')


class LibraryBookRequestSerializer(serializers.ModelSerializer):
    book_id = LibraryBookSerializer()
    card_number = LibraryCardSerializer()

    class Meta:
        model = Library_Book_Request
        fields = ('__all__')


class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class_Room
        fields = ('__all__')


class ClassRoutineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Class_Routine
        fields = ('__all__')


class RoutineDetailsSerializer(serializers.ModelSerializer):
    academic_year = AcademicYearSerializer()
    class_id = AcademicClassSerializer()
    class_group_id = AcademicGroupSerializer()
    subject_id = SubListSerializer()
    teacher_id = EmpDtlSerializer()
    room_id = ClassRoomSerializer()
    routine_id = ClassRoutineSerializer()

    class Meta:
        model = Class_Routine_Details
        fields = ('__all__')


class TeacherSerializer(serializers.ModelSerializer):
    academic_year = AcademicYearSerializer()
    class_id = AcademicClassSerializer()
    class_group_id = AcademicGroupSerializer()
    student_roll = StudentInfoSerializer()
    # teacher_id=EmpInfoSerializer()

    class Meta:
        model = Mapping_Guide_Teacher
        fields = ('__all__')


class eduTeacherSerializer(serializers.ModelSerializer):
    employee_id=EmpInfoSerializer()
    # employee_details = serializers.SerializerMethodField('get_employee_details')

    class Meta:
        model = Teacher
        fields=('__all__')
    #     fields = ['teacher_id', 'employee_id', 'status',
    #               'app_user_id', 'app_data_time', 'employee_details']
    # def get_employee_details(self, obj):
    #     employee = Employee_Details.objects.get(employee_id=obj.employee_id)
    #     return str(employee.employee_name)

class SubjectChoiceSerializer(serializers.ModelSerializer):
    student_roll = StudentInfoSerializer()
    subject_id = SubListSerializer()

    class Meta:
        model = Subject_Choice
        fields = ('__all__')


class TCSerializer(serializers.ModelSerializer):
    student_roll = StudentInfoSerializer()

    class Meta:
        model = Transfer_Certificate
        fields = ('__all__')


class ExamAttendanceSerializer(serializers.ModelSerializer):
    academic_Year = AcademicYearSerializer()
    class_id = AcademicClassSerializer()
    class_group_id = AcademicGroupSerializer()
    shift_id = ShiftSerializer()
    session_id = SessionSerializer()
    subject_id = SubListSerializer()
    examtype_id = ExamTypeSerializer()

    class Meta:
        model = Exam_Attendance
        fields = ('__all__')


class FeesHeadSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fees_Head_Settings
        fields = ('__all__')


class FeesHeadMappingSerializer(serializers.ModelSerializer):
    head_code = FeesHeadSettingSerializer()
    class_id = AcademicClassSerializer()    

    class Meta:
        model = Fees_Mapping
        fields = ('__all__')


class FeesWaiverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fees_Waiver
        fields = ('__all__')


class FeesWaiverMappingSerializer(serializers.ModelSerializer):
    head_code = FeesHeadSettingSerializer()
    class_id = AcademicClassSerializer()
    class_group_id = AcademicGroupSerializer()
    section_id = SectionInfoSerializer()
    catagory_id = CategorySerializer()

    class Meta:
        model = Fees_Waiver_Mapping
        fields = ('__all__')


class FeesMappingSerializer(serializers.ModelSerializer):
    head_code = FeesHeadSettingSerializer()
    class_id = AcademicClassSerializer()
    class_group_id = AcademicGroupSerializer()
    section_id = SectionInfoSerializer()

    class Meta:
        model = Fees_Mapping
        fields = ('__all__')


class AbsFineMappingSerializer(serializers.ModelSerializer):
    class_id = AcademicClassSerializer()
    class_group_id = AcademicGroupSerializer()
    section_id = SectionInfoSerializer()

    class Meta:
        model = Absent_Fine_Mapping
        fields = ('__all__')


class FeesWaiverStudentSerializer(serializers.ModelSerializer):
    student_roll = StudentInfoSerializer()

    class Meta:
        model = Fees_Waive_Student
        fields = ('__all__')


class IDCardSerializer(serializers.ModelSerializer):
    student_roll = StudentInfoSerializer()
    class_id = AcademicClassSerializer()
    academic_Year = AcademicYearSerializer()

    class Meta:
        model = Student_ID_Card
        fields = ('__all__')


class AdmitCardSerializer(serializers.ModelSerializer):
    student_roll = StudentInfoSerializer()
    class_id = AcademicClassSerializer()
    academic_year = AcademicYearSerializer()
    class_group_id = AcademicGroupSerializer()
    session_id = SessionSerializer()
    exam_term_id = ExamTermSerializer()

    class Meta:
        model = Student_Admit_Card
        fields = ('__all__')


class CourseRegSerializer(serializers.ModelSerializer):
    student_roll = StudentInfoSerializer()
    class_id = AcademicClassSerializer()

    class Meta:
        model = Course_Registrations
        fields = ('__all__')


class SeatPlaneSerializer(serializers.ModelSerializer):
    student_roll = StudentInfoSerializer()
    class_id = AcademicClassSerializer()
    academic_year = AcademicYearSerializer()
    class_group_id = AcademicGroupSerializer()
    term_id = ExamTermSerializer()

    class Meta:
        model = Student_Seat_plane
        fields = ('__all__')


class NamePlateSerializer(serializers.ModelSerializer):
    student_roll = StudentInfoSerializer()
    class_id = AcademicClassSerializer()
    academic_year = AcademicYearSerializer()
    class_group_id = AcademicGroupSerializer()

    class Meta:
        model = Student_Name_Plate
        fields = ('__all__')

class Fees_Receive_Summary_Serializer(serializers.ModelSerializer):
    student_roll = StudentInfoSerializer()
    class Meta:
        model = Fees_Receive_Summary
        fields = ('__all__')

class Fees_Processing_Details_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Fees_Processing_Details
        fields = ('__all__')
        depth = 1

class Admission_form_header_Serializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField('get_logo')
    def get_logo(self, instance):
        if instance.logo:
            return instance.logo.url
        else:
            return None
    class Meta:
        model = Admission_form_header
        fields = ('__all__')


class IdCard_form_header_Serializer(serializers.ModelSerializer):   
    logo = serializers.SerializerMethodField('get_logo')
    sing = serializers.SerializerMethodField('get_sing')
    def get_logo(self, instance):
        if instance.logo:
            return instance.logo.url
        else:
            return None
    def get_sing(self, instance):
        if instance.sing:
            return instance.sing.url
        else:
            return None
    class Meta:
        model = IdCard_form_header
        fields = ('__all__')


class submapping_TeacherSerializer(serializers.ModelSerializer):
    # student_roll = subject_mapping_teacher()

    class Meta:
        model = subject_mapping_teacher
        fields = ('__all__')
        depth=1

class Board_NameSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Education_Board
        fields = ('__all__')
class Certificate_NameSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Certificat_Name
        fields = ('__all__')

class TestimonialSerializer(serializers.ModelSerializer):
    student_roll = StudentInfoSerializer()
    cert_name_id=Certificate_NameSerializer()
    class Meta:
        model = Testimonial
        fields = ('__all__')

