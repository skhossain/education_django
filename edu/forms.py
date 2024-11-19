from pyexpat import model
from urllib import request
from django import forms
from crispy_forms.layout import Field
from django.forms import ModelForm, TextInput, Select, Textarea, IntegerField, ChoiceField, BooleanField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from edu.models import *
from edu.models import Application_Settings as Academy_info
from .models import Shift_Info as Edu_Shift_Info
from finance.models import General_Ledger
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

##########

Hefz_class =(
    ("Moktob", "Moktob"),
    ("Najera", "Najera"),
    ("Hefz", "Hefz"),
    ("Nursery", "Nursery"),
    ("One", "One"),
    ("Two", "Two"),
    ("Three", "Three"),
    ("Four", "Four"),
    ("Five", "Five"),
)
 
class DateInput(forms.DateInput):
    input_type = 'date'


class ChoiceFieldNoValidation(ChoiceField):
    def validate(self, value):
        pass


class ApplicationSettingModelForm(forms.ModelForm):

    class Meta:
        model = Academy_info
        fields = ['academic_code', 'academic_name', 'academic_address', 'academic_mobile_1',
                  'academic_mobile_2', 'academic_email', 'academic_website', 'academic_logo','web_header_banner', 'eiin_number']
        labels = {
            "academic_code": ("Academic Code"),
            "academic_name": ("Academic Name"),
            "academic_address": ("Academic Address"),
            "academic_mobile_1": ("Academic Mobile-1"),
            "academic_mobile_2": ("Academic Mobile-2"),
            "academic_email": ("Academic Email"),
            "academic_website": ("Academic Website"),
            "academic_logo": ("Academic Logo"),
            "web_header_banner": ("Website Header Banner"),
            "eiin_number": ("EIIN Number"),
        }

class AcademicYearModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AcademicYearModelForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

    class Meta:
        model = Academic_Year
        fields = ['academic_year', 'start_date', 'end_date']
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
        }
        labels = {
            "academic_year": ("Academic Year"),
            "start_date": ("Start Date"),
            "end_date": ("End Date"),
        }


class AcademicClassModelForm(forms.ModelForm):

    class Meta:
        model = Academic_Class
        fields = ['class_name', 'short_name', 'description',
                  'roll_serial', 'class_serial', 'out_of']
        labels = {
            "class_name": ("Class Name"),
            "short_name": ("Short Name"),
            "description": ("Description"),
            "roll_serial": ("Roll Patent"),
            "class_serial": ("Class Serial No."),
            "out_of": ("Result Publish"),
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 1, }),
        }


class AcademicGroupModelForm(forms.ModelForm):

    class Meta:
        model = Academic_Class_Group
        fields = ['class_id', 'class_group_name', 'description', ]
        labels = {
            "class_id": ("Class"),
            "class_group_name": ("Class Group Name"),
            "description": ("Description"),
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 1, }),
        }


class ClassRoomModelForm(forms.ModelForm):
    class Meta:
        model = Class_Room
        fields = ['nama_or_number', 'room_size']
        labels = {
            "nama_or_number": ("Class Room Name/Number"),
            "room_size": ("Room Size(Squ fit)"),
        }


class SectionInfoModelForm(forms.ModelForm):

    class Meta:
        model = Section_Info
        fields = ['class_id', 'section_name', 'total_student',
                  'gide_teacher_id', 'class_start_time', 'class_end_time']
        labels = {
            "class_id": ("Class"),
            "section_name": ("Section Name"),
            "total_student": ("Total Students"),
            "gide_teacher_id": ("Gide Teacher"),
            "class_start_time": ("Class Start Time"),
            "class_end_time": ("Class End Time"),
        }
        widgets = {
            'class_start_time': TimePicker(options={
                'useCurrent': True,
                'format': 'hh:mm:ss a',
                'defaultDate': '2018-01-02T22:08:12.510696',
            }),
            'class_end_time': TimePicker(),
        }


class SessionModelForm(forms.ModelForm):

    class Meta:
        model = Session
        fields = ['session_name']
        labels = {
            "session_name": ("Session"),
        },
        widgets = {
            "session_name": forms.TextInput(attrs={"placeholder": "2020-21"})
        }


class SubjectCategoryModelForm(forms.ModelForm):

    class Meta:
        model = Subject_Category
        fields = ['category_name']
        labels = {
            "category_name": ("Subject Category Name"),
        }
        widgets = {
            'category_name': forms.TextInput(attrs={'placeholder': 'Optional'}),
        }


class CategoryModelForm(forms.ModelForm):

    class Meta:
        model = Catagory_info
        fields = ['catagory_name']
        labels = {
            "catagory_name": ("Student Category Name"),
        },
        widgets = {
            'catagory_name': forms.TextInput(attrs={'placeholder': 'Scholarship'})
        }


class SubjectTypeModelForm(forms.ModelForm):

    class Meta:
        model = Subject_Type
        fields = ['subject_type_name']
        labels = {
            "subject_type_name": ("Subject Type Name"),
        }
        widgets = {
            "subject_type_name": forms.TextInput(attrs={"placeholder": "Practical"})
        }


class SubjectListModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SubjectListModelForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if kwargs and instance and instance.class_id:
            self.fields['class_group_id'] = forms.ModelChoiceField(queryset=Academic_Class_Group.objects.filter(
                class_id=instance.class_id.class_id), required=False, label='Group Name')
            # self.fields['class_id'].widget.attrs['disabled'] = True

    class Meta:
        model = Subject_List
        fields = ['class_id', 'class_group_id', 'subject_type_id', 'category_id', 'subject_name','sort_name',
                  'maximum_marks', 'minimum_pass_marks', 'subject_code', 'out_of', 'credit']
        labels = {
            "class_id": ("Class"),
            "class_group_id": ("Group Name"),
            "subject_type_id": ("Subject Type"),
            "category_id": ("Subject Category"),
            "subject_name": ("Subject Name"),
            "sort_name": ("Sort Name"),
            "maximum_marks": ("Subject Total Marks"),
            "minimum_pass_marks": ("Minimum Pass Marks "),
            "subject_code": ("Subject Code "),
            "out_of": ("Result publish"),
            "credit": ("Credit"),
        }


class DepartmentInfoModelForm(forms.ModelForm):

    class Meta:
        model = Department_Info
        fields = ['academic_year', 'department_name',
                  'total_student', 'total_quota']
        labels = {
            "academic_year": ("Academic Year"),
            "department_name": ("Department Name"),
            "total_student": ("Total Student"),
            "total_quota": ("Total Quota"),
        }


class ShiftInfoModelForm(forms.ModelForm):

    class Meta:
        model = Edu_Shift_Info
        fields = ['shift_name', 'shift_start_time',
                  'shift_end_time', 'total_student', 'total_quota']
        labels = {
            "shift_name": ("Shift Name"),
            "shift_start_time": ("Start Time"),
            "shift_end_time": ("End Time"),
            "total_student": ("Total Student"),
            "total_quota": ("Total Quota"),
        }
        widgets = {
            'shift_start_time': TimePicker(),
            'shift_end_time': TimePicker(),
        }

class DegreeInfoModelForm(forms.ModelForm):

    class Meta:
        model = Degree_Info
        fields = ['degree_name', 'degree_duration']
        labels = {
            "degree_name": ("Degree Name"),
            "degree_duration": ("Degree Duration"),
        },
        widgets = {
            "degree_name": forms.TextInput(attrs={"placeholder": "HSC"})
        }


class OccupationInfoModelForm(forms.ModelForm):

    class Meta:
        model = Occupation_Info
        fields = ['occupation_name']
        labels = {
            "occupation_name": ("Profession Name"),
        },
        widgets = {
            "occupation_name": forms.TextInput(attrs={"placeholder": "Teacher"})
        }


class EducationInstituteModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EducationInstituteModelForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance and instance.pk:
            self.fields['institute_id'].widget.attrs['readonly'] = True

    class Meta:
        model = Education_Institute
        fields = ['institute_id', 'institute_name', 'institute_code',
                  'institute_address', 'institute_mobile', 'lower_degree', 'higher_degree']
        labels = {
            "institute_id": ("Institute"),
            "institute_name": ("Institute Name"),
            "institute_code": ("Institute Code/EIIN"),
            "institute_address": ("Institute Address"),
            "institute_mobile": ("Institute Contact Number"),
            "lower_degree": ("Lowest Degree"),
            "higher_degree": ("Highest Degree"),
        }


class StudentInfoModelForm(forms.ModelForm):
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    # profile_image=forms.ImageField(widget=forms.FileInput(attrs={"id" : "image"}))

    class Meta:
        model = Students_Info
        fields = [
            'branch_code', 'academic_year', 'session_id', 'catagory_id', 'student_roll',
            'class_roll', 'student_name',
            'student_nick_name', 'class_id', 'class_group_id',
            'shift_id', 'section_id', 'last_institute_id', 'student_type',
            'student_referred_by', 'student_father_name',
            'father_occupation_id', 'father_email_address',
            'father_phone_number', 'father_nid', 'father_address',
            'sms_to_father', 'student_mother_name', 'profile_image', 'student_signature',
            'mother_occupation_id', 'mother_email_address',
            'mother_phone_number', 'mother_nid', 'mother_address',
            'sms_to_mother', 'student_blood_group', 'student_gender',
            'student_religion', 'student_marital_status',
            'student_national_id', 'student_birth_cert',
            'student_present_address', 'student_permanent_address',
            'student_phone', 'student_email', 'student_joining_date',
            'student_date_of_birth', 'student_status', 'student_comments',
            'legal_guardian_name', 'legal_guardian_contact',
            'legal_guardian_relation', 'legal_guardian_nid',
            'legal_guardian_occupation_id', 'legal_guardian_address',
            'local_guardian_name', 'local_guardian_contact',
            'local_guardian_relation', 'local_guardian_nid',
            'local_guardian_occupation_id', 'local_guardian_address', 'per_division_id', 'per_district_id',
            'per_upozila_id', 'pre_division_id', 'pre_district_id', 'pre_upozila_id', 'same_as',
            'tc_number', 'tc_date'
        ]
        widgets = {
            'student_date_of_birth': DateInput(),
            'student_joining_date': DateInput(),
            'tc_date': DateInput(),
            'father_address': forms.Textarea(attrs={'rows': 1, }),
            'mother_address': forms.Textarea(attrs={'rows': 1, }),
            'student_present_address': forms.Textarea(attrs={'rows': 1, }),
            'student_permanent_address': forms.Textarea(attrs={'rows': 1, }),
            'legal_guardian_address': forms.Textarea(attrs={'rows': 1, }),
            'local_guardian_address': forms.Textarea(attrs={'rows': 1, }),
            'last_institute_id': forms.Select(attrs={'class': 'institute_name'}),

        }
        labels = {
            "branch_code": ("Branch Name"),
            "academic_year": ("Academic Year"),
            "session_id": ("Session"),
            "catagory_id": ("Student's Category"),
            "student_roll": ("Student's ID"),
            "class_roll": ("Class Roll"),
            "student_name": ("Student's Name"),
            "student_nick_name": ("Nic Name"),
            "class_id": ("Class Name"),
            "class_group_id": ("Group Name"),
            "shift_id": ("Shift Name"),
            "section_id": ("Section"),
            "last_institute_id": ("Last Institute"),
            "student_type": ("Student's Type"),
            "student_referred_by": ("Student's Referred By"),
            "student_father_name": ("Father's Name"),
            "father_occupation_id": ("Father's Occupation"),
            "father_email_address": ("Father's Email Address "),
            "father_phone_number": ("Father's Phone Number"),
            "father_nid": ("Father's NID No."),
            "father_address": ("Father's Address"),
            "sms_to_father": ("SMS to Father"),
            "student_mother_name": ("Mother's Name"),
            "profile_image": ("Upload Your Image"),
            "student_signature": ("Upload Signature"),
            "mother_occupation_id": ("Mother's Occupation"),
            "mother_email_address": ("Mother's Email Address"),
            "mother_phone_number": ("Mother's Phone Number "),
            "mother_nid": ("Mother's NID No."),
            "mother_address": ("Mother's Address"),
            "sms_to_mother": ("SMS to Mother"),
            "student_blood_group": ("Student's Blood Group"),
            "student_gender": ("Student's Gender"),
            "student_religion": ("Student's Religion"),
            "student_marital_status": ("Marital Status"),
            "student_national_id": ("Student's NID No."),
            "student_birth_cert": ("Birth Certificated No."),
            "student_present_address": ("Village/Word/Road"),
            "student_permanent_address": ("Village/Word/Road"),
            "student_phone": ("Contact Number"),
            "student_email": ("Email Address"),
            "student_joining_date": ("Admission Date"),
            "student_date_of_birth": ("Date of Birth"),
            "student_status": ("Student's Status"),
            "student_comments": ("Student's Comments"),
            "legal_guardian_name": ("Guardian Name"),
            "legal_guardian_contact": ("Guardian's Contact Number"),
            "legal_guardian_relation": ("Guardian's Relation"),
            "legal_guardian_nid": ("Legal Guardian's NID No."),
            "legal_guardian_occupation_id": ("Guardian's Occupation"),
            "legal_guardian_address": ("Guardian's Address"),
            "local_guardian_name": ("Guardian's Name"),
            "local_guardian_contact": ("Guardian's Contact Number"),
            "local_guardian_relation": ("Guardian's Relation"),
            "local_guardian_nid": ("Guardian's NID No."),
            "local_guardian_occupation_id": ("Guardian's Occupation"),
            "local_guardian_address": ("Guardian's Address"),
            "per_division_id": (" Division Name"),
            "per_district_id": (" District Name"),
            "per_upozila_id": (" Upozila Name"),
            "pre_division_id": (" Division Name"),
            "pre_district_id": (" District Name"),
            "pre_upozila_id": (" Upozila Name"),
            "same_as": ("Same As"),
            "tc_number": ("TC Number"),
            "tc_date": ("TC Date")
        }


class ImageTempModelForm(forms.ModelForm):
    class Meta:
        model = Image_temp
        fields = [
            'image_1',
            'image_2',
        ]
        labels = {
            "image_1": ("Student's Profile Image"),
            "image_2": ("Student's Signature"),
        }


class StudentAdmissionModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentAdmissionModelForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

    class Meta:
        model = Student_Admission
        fields = ['student_roll', 'class_roll']
        labels = {
            "student_roll": ("Student Roll"),
            "class_roll": ("Class Roll"),
        }


########### Exam and Result Details ###########

class ResultGradeModelForm(forms.ModelForm):

    class Meta:
        model = Result_Grade
        fields = ['grade_name', 'result_gpa',
                  'lowest_mark', 'highest_mark', 'out_of', 'is_failed']
        labels = {
            "grade_name": ("Grade Name"),
            "result_gpa": ("Result GPA"),
            "lowest_mark": ("Lowest Mark"),
            "highest_mark": ("Highest Mark"),
            "out_of": ("Out of"),
            "is_failed": ("Is Failed"),
        }


class ExamTypeModelForm(forms.ModelForm):

    class Meta:
        model = Exam_Type
        fields = ['examtype_name']
        labels = {
            "examtype_name": ("Exam Type Name"),
        },
        widgets = {
            "examtype_name": forms.TextInput(attrs={"placeholder": "Practical/Oral/Written"}),
        }


class ExamTermModelForm(forms.ModelForm):

    class Meta:
        model = Exam_Term
        fields = ['term_name']
        labels = {
            "term_name": ("Exam Term Name"),
        }


class ExamSetupModelForm(forms.ModelForm):
    # exam_type_status=forms.ChoiceField(label='Exam Type Status', choices=Exam_type_status, widget=forms.RadioSelect)
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    class Meta:
        model = Exam_Setup
        fields = ['branch_code','exam_name', 'term_id', 'no_of_exam', 'examtype_id', 'academic_year','session_id', 'class_id',
                  'subject_id', 'class_group_id', 'cal_condition', 'total_exam_marks', 'minimum_pass_marks', 'exam_type_status', 'out_of']
        labels = {
            "branch_code": ("Branch"),
            "exam_name": ("Exam Name"),
            "term_id": ("Exam Term Name"),
            "no_of_exam": ("No of Exam"),
            "examtype_id": ("Exam Type"),
            "academic_year": ("Academic Year"),
            "session_id": ("Session"),
            "class_id": ("Class Name"),
            "class_group_id": ("Class Group Name"),
            "subject_id": ("Subject"),
            "cal_condition": ("Calculation Condition"),
            "total_exam_marks": ("Total Exam Mark"),
            "minimum_pass_marks": ("Minimum Pass Mark"),
            "out_of": ("Result Publish"),
        }
        widgets = {
            'no_of_exam': forms.HiddenInput(),
        }


class MarkDetailsModelForm(forms.ModelForm):

    class Meta:
        model = Exam_Marks_Details
        fields = ['class_id', 'exam_id', 'term_id', 'exam_no', 'subject_id', 'academic_year', 'student_roll',
                  'total_exam_marks', 'obtain_marks', 'result_grade', 'grade_point_average']
        labels = {
            "class_id": ("Class"),
            "exam_id": ("Exam Name"),
            "term_id": ("Exam Term Name"),
            "exam_no": ("Exam No."),
            "subject_id": ("Subject"),
            "academic_year": ("Academic Year"),
            "student_roll": ("Student Roll"),
            "total_exam_marks": ("Total Exam Marks"),
            "obtain_marks": ("Obtain Marks"),
            "result_grade": ("Result Grade"),
            "grade_point_average": ("GPA "),
        }


class FinalModelForm(forms.ModelForm):

    class Meta:
        model = Exam_Marks_Final
        fields = ['academic_year', 'term_id', 'class_id', 'student_roll', 'total_exam_marks',
                  'obtain_marks', 'result_grade', 'grade_point_average']
        labels = {
            "academic_year": ("Academic Year"),
            "term_id": ("Exam Term Name"),
            "class_id": ("Class"),
            "student_roll": ("Student Roll"),
            "total_exam_marks": ("Total Exam Marks"),
            "obtain_marks": ("Obtain Marks"),
            "result_grade": ("Results Grade"),
            "grade_point_average": ("GPA "),
        }


class OnlineExamModelForm(forms.ModelForm):
    # exam_start_time = forms.TimeField(widget=TimePicker())
    class Meta:
        model = Online_Exam_Information
        fields = ['online_exam_id', 'exam_id', 'exam_name', 'basic_info',
                  'exam_date', 'exam_start_time', 'exam_end_time', 'question_patten', 'publish_status', 'total_marks']
        labels = {
            "online_exam_id": ("Online Exam Id"),
            "exam_id": ("Exam Name"),
            "exam_name": ("Exam Details"),
            "basic_info": ("Exam Header Information"),
            "exam_date": ("Exam Date"),
            "exam_start_time": ("Exam Start Time"),
            "exam_end_time": ("Exam End Time"),
            "question_patten": ("Question Patten"),
            "publish_status": ("Publish Status"),
            "total_marks": ("Total Marks"),
        }
        widgets = {
            'exam_date': DatePicker(),
            'exam_start_time': TimePicker(),
            'exam_end_time': TimePicker(),
        }

class OnlineExamQueModelForm(forms.ModelForm):
    class Meta:
        model = Online_Exam_Questions
        fields = ['question_id', 'online_exam_id', 'question', 'question_type',
                  'question_marks']
        labels = {
            "question_id": ("Question"),
            "online_exam_id": ("Online Exam Name"),
            "question": ("Question"),
            "question_type": ("Question Type"),
            "question_marks": ("Question Marks")
        }


class Visited_Student_InfoModelForm(forms.ModelForm):
    class Meta:
        model = Visited_Student_Info
        fields = ['student_name', 'class_id', 'class_group_id', 'student_father_name', 'father_phone_number', 'student_mother_name', 'mother_phone_number',
                  'student_marital_status', 'student_present_address', 'student_permanent_address', 'student_phone', 'student_email', 'current_institute']
        widgets = {
            'student_present_address': forms.Textarea(attrs={'rows': 1, }),
            'student_permanent_address': forms.Textarea(attrs={'rows': 1, }),
        }
        labels = {
            "student_name": ("Student's Name"),
            "class_id": ("Intended Class"),
            "class_group_id": ("Group Name"),
            "student_father_name": ("Father's Name"),
            "father_phone_number": ("Father's Mobile"),
            "student_mother_name": ("Mother's Name"),
            "mother_phone_number": ("Mother's Mobile"),
            "student_marital_status": ("Student's Marital Status"),
            "student_present_address": ("Student's Present Address"),
            "student_permanent_address": ("Student's Permanent Address"),
            "student_phone": ("Student's Mobile"),
            "student_email": ("Student's Email"),
            "current_institute": ("Current Institute")
        }


class LibraryRackModelForm(forms.ModelForm):
    class Meta:
        model = Library_Rack
        fields = ['rack_name', 'is_active', 'is_deleted']
        labels = {
            "rack_name": ("Rack Name"),
            "is_active": ("Is Active"),
            "is_deleted": ("Is Delete")
        }


class LibraryAuthorModelForm(forms.ModelForm):

    class Meta:
        model = Library_Author
        fields = ['author_name', 'born_date', 'death_date',
                  'biography', 'is_active', 'is_deleted']
        labels = {
            "author_name": ("Author Name"),
            "born_date": ("Born Date"),
            "death_date": ("Death Date"),
            "biography": ("Biography"),
            "is_active": ("Is Active"),
            "is_deleted": ("Is Delete")
        }
        widgets = {
            'born_date': DateInput(),
            'death_date': DateInput(),
            "biography": forms.Textarea(attrs={"rows": 1})
        }


class LibraryEditorModelForm(forms.ModelForm):

    class Meta:
        model = Library_Editor
        fields = ['editor_name', 'editor_websight', 'editor_email',
                  'editor_phone', 'editor_addres', 'is_active', 'is_deleted']
        labels = {
            "editor_name": ("Editor Name"),
            "editor_websight": ("Editor Website"),
            "editor_email": ("Editor Email"),
            "editor_phone": ("Editor Phone"),
            "editor_addres": ("Editor Address"),
            "is_active": ("Is Active"),
            "is_deleted": ("Is Delete")
        }


class LibraryBookModelForm(forms.ModelForm):

    class Meta:
        model = Library_Books
        fields = ['book_name', 'author_id', 'editor_id', 'isbn_code', 'book_language', 'fine_lost', 'fine_late_return', 'number_of_page', 'rack_id', 'total_books',
                  'books_available', 'edition_number', 'is_ebook', 'is_subscription', 'subscription_amount', 'day_to_return_book', 'is_active', 'is_deleted', 'ebook_file']
        labels = {
            "book_name": ("Book Name"),
            "author_id": ("Author Name"),
            "editor_id": ("Editor Name"),
            "isbn_code": ("Isbn Code"),
            "book_language": ("Book Language"),
            "fine_lost": ("Fine for Lost"),
            "fine_late_return": ("Fine for Late Return"),
            "number_of_page": ("Total Page"),
            "rack_id": ("Rack Name"),
            "total_books": ("Total Books"),
            "books_available": ("Available Books"),
            "edition_number": ("Edition No."),
            "is_ebook": ("Is E-Book"),
            "is_subscription": ("Is Subscription"),
            "subscription_amount": ("Subscription Amount"),
            "day_to_return_book": ("Total Day for Return Book"),
            "is_active": ("Is Active"),
            "is_deleted": ("Is Delete"),
            "ebook_file": (""),
        }


class LibraryCardModelForm(forms.ModelForm):

    class Meta:
        model = Library_Card
        fields = ['name_on_card', 'student_roll', 'teacher_id', 'book_limit', 'book_taken', 'card_status', 'start_date',
                  'expire_date', 'duration_month', 'total_late_penalty', 'total_lost_penalty', 'is_active', 'is_deleted']
        labels = {
            "name_on_card": ("Card Name"),
            "student_roll": ("Student Roll"),
            "teacher_id": ("Teacher Name"),
            "book_limit": ("Book Limit"),
            "book_taken": ("Book Taken"),
            "card_status": ("Card Status"),
            "start_date": ("Start Date"),
            "expire_date": ("Expire Date"),
            "duration_month": ("Month Duration"),
            "total_late_penalty": ("Total Late Penalty"),
            "total_lost_penalty": ("Total Lost Penalty"),
            "is_active": ("Is Active"),
            "is_deleted": ("Is Delete")
        }
        widgets = {
            'start_date': DateInput(),
            'expire_date': DateInput(),
        }


class LibraryBookIssueModelForm(forms.ModelForm):

    class Meta:
        model = Library_Book_Issue
        fields = ['book_id', 'card_number', 'issue_date', 'actual_return_date', 'return_date', 'day_to_return_book',
                  'late_penalty', 'lost_penalty', 'late_reason', 'lost_reason', 'book_issue_status', 'is_active', 'is_deleted']
        labels = {
            "book_id": ("Book Name"),
            "card_number": ("Card Number"),
            "issue_date": ("Issue Date"),
            "actual_return_date": ("Actual Return Date"),
            "return_date": ("Return Date"),
            "day_to_return_book": ("Day to Return Book"),
            "late_penalty": ("Late Penalty"),
            "lost_penalty": ("Lost Penalty"),
            "late_reason": ("Late Reason"),
            "lost_reason": ("Lost Reason"),
            "book_issue_status": ("Book Issue Status"),
            "is_active": ("Is Active"),
            "is_deleted": ("Is Delete")
        }
        widgets = {
            'issue_date': DateInput(),
            'actual_return_date': DateInput(),
            'return_date': DateInput(),
        }


class LibraryBookRequestModelForm(forms.ModelForm):

    class Meta:
        model = Library_Book_Request
        fields = ['book_id', 'card_number', 'request_date',
                  'actual_return_date', 'day_to_return_book', 'book_issue_status']
        labels = {
            "book_id": ("Book Name"),
            "card_number": ("Card Name"),
            "request_date": ("Request Date"),
            "actual_return_date": ("Actual Return Date"),
            "day_to_return_book": ("Day to Return Book"),
            "book_issue_status": ("Book Request Status")
        }
        widgets = {
            'request_date': DateInput(),
            'actual_return_date': DateInput()
        }


class ClassRoutineModelForm(forms.ModelForm):

    class Meta:
        model = Class_Routine
        fields = ['routine_name', 'start_date', 'end_date']
        labels = {
            "routine_name": ("Routine Name/Title"),
            "start_date": ("Start Routine Valid Date"),
            "end_date": ("End Routine Valid Date")
        }
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput()
        }


class ClassRoutineDetailsModelForm(forms.ModelForm):

    class Meta:
        model = Class_Routine_Details
        fields = ['start_time', 'end_time', 'routine_id', 'academic_year',
                  'teacher_id', 'subject_id', 'class_id', 'class_group_id', 'shift_id',
                  'section_id', 'room_id', 'day']
        labels = {
            "start_time": ("Class Start Time"),
            "end_time": ("Class End Time"),
            "routine_id": ("Routine Name"),
            "academic_year": ("Academic Year"),
            "teacher_id": ("Teacher Name"),
            "subject_id": ("Subject Name"),
            "class_id": ("Class Name"),
            "class_group_id": ("Class Group Name"),
            "shift_id": ("Shift Name"),
            "section_id": ("Section Name"),
            "room_id": ("Room No/Name"),
            "day": ("Day Name")
        }
        widgets = {
            'start_time': TimePicker(),
            'end_time': TimePicker(),
            'day': forms.Select(attrs={'multiple': 'multiple', 'name': 'day[]'}),
        }


class TeacherModelForm(forms.ModelForm):

    class Meta:
        model = Mapping_Guide_Teacher
        fields = ['academic_year', 'class_id', 'class_group_id',
                  'teacher_id', 'student_roll', 'student_status']
        labels = {
            "academic_year": ("Academic Year"),
            "class_id": ("Class Name"),
            "class_group_id": ("Group Name"),
            "teacher_id": ("Teacher Name"),
            "student_roll": ("Students"),
            "student_status": ("Students Status"),
        }


class SubjectChoiceModelForm(forms.ModelForm):

    class Meta:
        model = Subject_Choice
        fields = ['academic_year', 'class_id', 'class_group_id',
                  'session_id', 'student_roll', 'subject_id', 'category_id']
        labels = {
            "academic_year": ("Academic Year"),
            "class_id": ("Class Name"),
            "class_group_id": ("Class Group Name"),
            "session_id": ("Session"),
            "student_roll": ("Student Roll"),
            "subject_id": ("Subject Name"),
            "category_id": ("Subject Category"),
        }


class TcModelForm(forms.ModelForm):

    class Meta:
        model = Transfer_Certificate
        fields = ['student_roll', 'date', 'tc_reason']
        labels = {
            "student_roll": ("Student Roll"),
            "date": ("Given Date"),
            "tc_reason": ("TC Reason"),
        }
        widgets = {
            'date': DateInput(),
            "tc_reason": forms.Textarea(attrs={"rows": 1})
        }


class ExamAttenModelForm(forms.ModelForm):

    class Meta:
        model = Exam_Attendance
        fields = ['academic_Year', 'class_id', 'class_group_id', 'shift_id', 'session_id',
                  'subject_id', 'examtype_id', 'exam_id', 'day', 'ex_start_time', 'ex_end_time', 'exam_date']
        labels = {
            "academic_Year": ("Academic Year"),
            "class_id": ("Class Name"),
            "class_group_id": ("Group Name"),
            "shift_id": ("Shift Name"),
            "session_id": ("Session"),
            "subject_id": ("Subject Name"),
            "examtype_id": ("Exam Type Name"),
            "exam_id": ("Exam Name"),
            "day": ("Day Name"),
            "ex_start_time": ("Exam Start Time"),
            "ex_end_time": ("Exam End Time"),
            "exam_date": ("Exam Date"),
        }
        widgets = {
            'exam_date': DateInput(),
        }


class FeesHeadSettingModelForm(forms.ModelForm):
    # head_ledger = ChoiceFieldNoValidation(label="Head Ledger", required=False)
    #parent_head = forms.ModelChoiceField(queryset=Fees_Head_Settings.objects.filter(is_main_head=True))
    head_ledger = forms.ModelChoiceField(
        queryset=General_Ledger.objects.filter(is_deleted=False, is_leaf_node=True, maintain_by_system=False, closer_date__isnull=True).order_by('gl_name'),label="Head Ledger", required=False)
    class Meta:
        model = Fees_Head_Settings
        fields = ['head_name', 'parent_head', 'head_ledger',
                  'is_main_head', 'head_comments', 'is_active', 'is_deleted']
        widgets = {
            'head_comments': Textarea(attrs={'rows': 1, 'cols': 60, }),
        }

        labels = {
            "head_name": ("Head Name"),
            "parent_head": ("Parent Head"),
            "head_ledger": ("Head Ledger"),
            "is_main_head": ("Is Main Head"),
            "head_comments": ("Comments"),
            "is_active": ("Is Active"),
            "is_deleted": ("Is Delete"),
        }


class Fees_Waiver_Mapping_ModelForm(forms.ModelForm):
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    class Meta:
        model = Fees_Waiver_Mapping
        fields = ['branch_code','head_code','waive_name', 'catagory_id', 'class_id', 'class_group_id', 'section_id',
                  'waiver_parsentag', 'waiver_amount', 'effective_date', 'is_active', 'is_deleted']
        widgets = {
            'waive_comments': Textarea(attrs={'rows': 1, 'cols': 60, }),
            'effective_date': DateInput(),
        }
        labels = {
            "branch_code": ("Branch Name"),
            "head_code": ("Fees Head"),
            "waive_name": ("Waive Name"),
            "catagory_id": ("Student Category"),
            "class_id": ("Class Name"),
            "class_group_id": ("Group Name"),
            "section_id": ("Section"),
            "waiver_parsentag": ("Waiver Parsentag"),
            "waiver_amount": ("Waiver Amount"),
            "effective_date": ("Effective Date"),
            "is_active": ("Is Active"),
            "is_deleted": ("Is Delete"),
        }


class Fees_Waiver_Mapping_Hist_ModelForm(forms.ModelForm):
    class Meta:
        model = Fees_Waiver_Mapping_Hist
        fields = ['head_code', 'catagory_id', 'class_id', 'class_group_id', 'section_id',
                  'waiver_parsentag', 'waiver_amount', 'effective_date', 'is_active', 'is_deleted']
        widgets = {
            'waive_comments': Textarea(attrs={'rows': 1, 'cols': 60, }),
            'effective_date': DateInput(),
        }
        labels = {
            "head_code": ("Fees Head"),
            "catagory_id": ("Student Category"),
            "class_id": ("Class Name"),
            "class_group_id": ("Group Name"),
            "section_id": ("Section"),
            "waiver_parsentag": ("Waiver Parsentag"),
            "waiver_amount": ("Waiver Amount"),
            "effective_date": ("Effective Date"),
            "is_active": ("Is Active"),
            "is_deleted": ("Is Delete"),
        }


class FeesMappingModelForm(forms.ModelForm):
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    class Meta:
        model = Fees_Mapping
        fields = ['branch_code','head_code', 'class_id', 'class_group_id', 'section_id', 'effective_date', 'fine_effective_days',
                  'fee_amount', 'fine_amount', 'pay_freq', 'is_single_lifetime', 'is_active', 'is_deleted','academic_year']
        labels = {
            "branch_code": ("Branch Name"),
            "head_code": ("Fees Head"),
            "class_id": ("Class Name"),
            "class_group_id": ("Group Name"),
            "section_id": ("Section"),
            "effective_date": ("Effective Date"),
            "fine_effective_days": ("Fine After Day"),
            "fee_amount": ("Fee Amount"),
            "fine_amount": ("Fine Amount"),
            "pay_freq": ("Payment Frequency"),
            "is_single_lifetime": ("Single Lifetime"),
            "is_active": ("Is Active"),
            "is_deleted": ("Is Delete"),
            "academic_year": ("Academic Year"),
        }
        widgets = {
            'effective_date': DateInput(),
        }


class Fees_Mapping_History_Model_Form(forms.ModelForm):
    class Meta:
        model = Fees_Mapping_History
        fields = ['head_code', 'class_id', 'class_group_id', 'section_id', 'effective_date', 'fine_effective_days',
                  'fee_amount', 'fine_amount', 'pay_freq','is_single_lifetime', 'is_active', 'is_deleted','academic_year']
        labels = {
            "head_code": ("Fees Head"),
            "class_id": ("Class Name"),
            "class_group_id": ("Group Name"),
            "section_id": ("Section"),
            "effective_date": ("Effective Date"),
            "fine_effective_days": ("Fine After Day"),
            "fee_amount": ("Fee Amount"),
            "fine_amount": ("Fine Amount"),
            "pay_freq": ("Payment Frequency"),
            "is_active": ("Is Active"),
            "is_deleted": ("Is Delete"),
            "academic_year": ("Academic Year"),
        }
        widgets = {
            'effective_date': DateInput(),
        }


class AbsFineMappingModelForm(forms.ModelForm):
    head_code = forms.ModelChoiceField(
        queryset=Fees_Head_Settings.objects.filter(is_main_head=False))

    class Meta:
        model = Absent_Fine_Mapping
        fields = ['head_code', 'class_id', 'class_group_id', 'section_id',
                  'effective_date', 'no_of_absent', 'fine_amount', 'is_active', 'is_deleted']
        labels = {
            "head_code": ("Head Code"),
            "class_id": ("Class Name"),
            "class_group_id": ("Class Group Name"),
            "section_id": ("Section"),
            "effective_date": ("Effective Date"),
            "no_of_absent": ("No. of Absent"),
            "fine_amount": ("Fine Amount"),
            "is_active": ("Is Active"),
            "is_deleted": ("Is Delete"),
        }
        widgets = {
            'effective_date': DateInput(),
        }


class Absent_Fine_History_Model_Form(forms.ModelForm):
    class Meta:
        model = Absent_Fine_History
        fields = ['head_code', 'class_id', 'class_group_id', 'section_id',
                  'effective_date', 'no_of_absent', 'fine_amount', 'is_active', 'is_deleted']
        labels = {
            "head_code": ("Head Code"),
            "class_id": ("Class Name"),
            "class_group_id": ("Class Group Name"),
            "section_id": ("Section"),
            "effective_date": ("Effective Date"),
            "no_of_absent": ("No. of Absent"),
            "fine_amount": ("Fine Amount"),
            "is_active": ("Is Active"),
            "is_deleted": ("Is Delete"),
        }


class FeesWaiveStudentModelForm(forms.ModelForm):
    head_code = forms.ModelChoiceField(
        queryset=Fees_Head_Settings.objects.filter(is_main_head=False))

    def __init__(self, *args, **kwargs):
        super(FeesWaiveStudentModelForm, self).__init__(*args, **kwargs)
        self.fields['head_code'].widget.attrs['class'] = "selectpicker"
        # self.fields['waive_code'].widget.attrs['data-live-search'] = "true"

    class Meta:
        model = Fees_Waive_Student
        fields = ['student_roll', 'head_code', 'effective_date', 'is_fully_waive',
                  'waive_amount','fees_month','fees_year', 'waive_percentage', 'auth_by', 'auth_on', 'cancel_by', 'cancel_on']
        labels = {
            "student_roll": ("Student Roll"),
            "head_code": ("Head Code"),
            "waive_effective_date": ("Waive Effective Date"),
            "is_fully_waive": ("IS Fully Waive"),
            "waive_amount": ("Waive Amount"),
            "waive_percentage": ("Waive Percentage"),
            "auth_by": ("Auth By"),
            "auth_on": ("Auth On"),
            "cancel_by": ("Cancel By"),
            "cancel_on": ("Cancel On"),
        }
        widgets = {
            'effective_date': DateInput(),
            'auth_on': DateInput(),
            'cancel_on': DateInput(),
        }


class FeesReceiveStudentModelForm(forms.ModelForm):
    head_code = forms.ModelChoiceField(
        queryset=Fees_Head_Settings.objects.filter(is_main_head=False))
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    # student_roll = ChoiceFieldNoValidation(label="Search a Student ID", required=False)
    academic_year = forms.ModelChoiceField(
        queryset=Academic_Year.objects.filter().order_by('-academic_year') ,required=False)
    due_date=forms.DateInput()
    class Meta:
        model = Fees_Receive_Student
        fields = ['branch_code','student_roll', 'head_code', 'ledger_code', 'receive_date','due_date', 'total_due', 'total_paid',
                  'total_waive', 'fine_due', 'fees_due', 'total_overdue',
                  'receive_month','receive_year','auth_by', 'auth_on', 'cancel_by', 'cancel_on']
        labels = {
            "branch_code": ("Branch Name"),
            "student_roll": ("Student Roll"),
            "academic_year": ("Academic Year"),
            "head_code": ("Head Code"),
            "ledger_code": ("Ledger Code"),
            "receive_date": ("Receive Date"),
            "total_due": ("Total Due"),
            "total_paid": ("Total Paid"),
            "total_waive": ("Total Waiver"),
            "fine_due": ("Fine Due"),
            "fees_waive": ("Fees Due"),
            "receive_month": ("Fees Month"),
            "receive_year": ("Fees Year"),
            "total_overdue": ("Total Overdue"),
            "auth_by": ("Auth By"),
            "auth_on": ("Auth On"),
            "cancel_by": ("Cancel By"),
            "cancel_on": ("Cancel On"),
        }
        widgets = {
            'receive_date': DateInput(),
            'due_date': DateInput(),
            'auth_on': DateInput(),
            'cancel_on': DateInput(),
        }


class OneTimeFeesReceiveStudentModelForm(forms.ModelForm):
    class Meta:
        model = One_Time_Fees_Rec_Std
        fields = ['student_roll', 'head_code', 'ledger_code', 'receive_date',
                  'receive_amount', 'remark', 'auth_by', 'auth_on', 'cancel_by', 'cancel_on']
        labels = {
            "student_roll": ("Student Roll"),
            "head_code": ("Head Code"),
            "ledger_code": ("Ledger Code"),
            "receive_date": ("Receive Date"),
            "receive_amount": ("Receive Amount"),
            "remark": ("Remark"),
            "auth_by": ("Auth By"),
            "auth_on": ("Auth On"),
            "cancel_by": ("Cancel By"),
            "cancel_on": ("Cancel On"),
        }
        widgets = {
            'student_roll': forms.HiddenInput(),
            'receive_date': forms.HiddenInput(),
            'remark': forms.Textarea(attrs={'rows': 1, }),
        }


class StudentIDCardModelForm(forms.ModelForm):
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    class Meta:
        model = Student_ID_Card
        fields = ['branch_code','student_roll', 'class_id', 'academic_Year', 'class_group_id',
                  'section_id', 'session_id', 'expire_date', 'back_text']
        labels = {
            "student_roll": ("Student Roll"),
            "class_id": ("Class Name"),
            "academic_Year": ("Academic Year"),
            "class_group_id": ("Class Group Name"),
            "section_id": ("Section"),
            "session_id": ("Session"),
            "expire_date": ("Expire Date"),
            "back_text": ("Back Part Text"),
        }

        widgets = {
            'expire_date': DateInput(),
            "back_text": forms.Textarea(attrs={"rows": 1})
        }


class StudentAdmitCardModelForm(forms.ModelForm):
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    class Meta:
        model = Student_Admit_Card
        fields = ['branch_code','academic_year', 'class_id',
                  'class_group_id', 'student_roll', 'session_id','exam_id','exam_term_id','trams_con']
        labels = {
            "branch_code": ("Branch Name"),
            "academic_year": ("Academic Year"),
            "class_id": ("Class Name"),
            "class_group_id": ("Group Name"),
            "student_roll": ("Student Roll/Name"),
            "session_id": ("Session"),
            "exam_term_id": ("Exam Term"),
            "exam_id": ("Exam Name"),
            "trams_con": ("General Instruction (optional)| Line brack by ;"),
        }
        widgets = {
            "trams_con": forms.Textarea(attrs={"rows": 1}),
        }


class CourseRegModelForm(forms.ModelForm):
    class Meta:
        model = Course_Registrations
        fields = ['class_id', 'student_roll', 'course_name',
                  'reg_no', 'issue_date', 'expire_date']
        labels = {
            "class_id": ("Class Name"),
            "student_roll": ("Student Roll/Name"),
            "course_name": ("Course Name"),
            "reg_no": ("Registration No."),
            "issue_date": ("Issue Date"),
            "expire_date": ("Expire Date"),
        }

        widgets = {
            'issue_date': DateInput(),
            'expire_date': DateInput(),

        }


class CommonReportForm(forms.Form):

    academic_year = forms.ModelChoiceField(
        queryset=Academic_Year.objects.all())
    class_name = forms.ModelChoiceField(queryset=Academic_Class.objects.all(),required=False)
    class_group_id = forms.ModelChoiceField(queryset=Academic_Class_Group.objects.all(),label='Class Group',required=False)
    gender = ChoiceFieldNoValidation(label='Select Gender', choices=[(
        '', 'Select Gender'), ('M', 'Male'), ('F', "Female"), ('O', "Others")], initial="",required=False)

    def __init__(self, *args, **kwargs):
        super(CommonReportForm, self).__init__(*args, **kwargs)
        # self.fields['academic_year'].widget.attrs['class'] = "selectpicker"
        # self.fields['academic_year'].widget.attrs['data-live-search'] = "true"
        # self.fields['class_name'].widget.attrs['class'] = "selectpicker"
        # self.fields['class_name'].widget.attrs['data-live-search'] = "true"
        # # self.fields['section_name'].widget.attrs['class'] = "selectpicker"
        # # self.fields['section_name'].widget.attrs['data-live-search'] = "true"


class StudentSeatPlaneModelForm(forms.ModelForm):
    class Meta:
        model = Student_Seat_plane
        fields = ['academic_year', 'class_id', 'class_group_id',
                  'student_roll', 'branch_code', 'term_id']
        labels = {
            "academic_year": ("Academic Year"),
            "class_id": ("Class Name"),
            "class_group_id": ("Group Name"),
            "student_roll": ("Student Roll/Name"),
            "branch_code": ("Branch Code"),
            "term_id": ("Name of Exam")
        }


class StudentNamePlateModelForm(forms.ModelForm):
    class Meta:
        model = Student_Name_Plate
        fields = ['academic_year', 'class_id', 'class_group_id',
                  'student_roll', 'branch_code', 'slogan']
        labels = {
            "academic_year": ("Academic Year"),
            "class_id": ("Class Name"),
            "class_group_id": ("Group Name"),
            "student_roll": ("Student Roll/Name"),
            "branch_code": ("Branch Code"),
            "slogan": ("Slogan"),
        }
        widgets = {
            "slogan": forms.Textarea(attrs={"rows": 1, 'placeholder': 'Maximum 2 line separate by (;) and per line in 5 word'}),
        }


class Students_Query_Form(forms.Form):
    branch_code = ChoiceFieldNoValidation(
        label="Branch Name", required=False, choices=[('', '------------')], initial="")
    student_roll = forms.ChoiceField(label="Select Student", required=False, choices=[
                                     ('', '------------')], initial="")
    from_date = forms.DateField(
        label="From Date", widget=DateInput(), required=True)
    upto_date = forms.DateField(
        label="Upto Date", widget=DateInput(), required=True)


class Common_Education_Report(forms.Form):
    branch_code = ChoiceFieldNoValidation(
        label="Branch Name", required=False, choices=[('', '------------')], initial="")
    student_roll = forms.ChoiceField(label="Student Name", required=False, choices=[
                                     ('', '------------')], initial="")
    from_date = forms.DateField(
        label="From Date", widget=DateInput(), required=False)
    upto_date = forms.DateField(
        label="Upto Date", widget=DateInput(), required=False)
    ason_date = forms.DateField(
        label="Report Date", widget=DateInput(), required=False)
    report_list = ChoiceFieldNoValidation(label='Report Name', choices=[
                                        ('', '------------')], initial="", required=False)
    class_id = ChoiceFieldNoValidation(label='Class Name', choices=[
                                        ('', '------------')], initial="", required=False)
    class_group_id = ChoiceFieldNoValidation(label='Group Name', choices=[
                                        ('', '------------')], initial="", required=False)
    section_id = ChoiceFieldNoValidation(label='Section Name', choices=[
                                        ('', '------------')], initial="", required=False)
    head_code = ChoiceFieldNoValidation(label='Fees Head', choices=[
                                        ('', '------------')], initial="", required=False)

class Fees_Processing_Details_ModelForm(forms.ModelForm):
    branch_code = ChoiceFieldNoValidation(
        label="Branch Name", required=False, choices=[('', '------------')], initial="")
    class Meta:
        model = Fees_Processing_Details
        fields = ['academic_year', 'class_id', 'class_group_id',
                  'student_roll', 'branch_code', 'section_id', 'process_date']
        labels = {
            "academic_year": ("Academic Year"),
            "class_id": ("Class Name"),
            "class_group_id": ("Group Name"),
            "student_roll": ("Student Roll/Name"),
            "branch_code": ("Branch Name"),
            "section_id": ("Section Name"),
            "process_date": ("Process Date")
        }
        widgets = {
            'process_date': DateInput(),
        }

class AdmissionFormHeaderModelForm(forms.ModelForm):
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    class Meta:
        model = Admission_form_header
        fields = ['branch_code', 'academic_name', 'form_name', 'text_one',
                  'text_two', 'text_three', 'text_four', 'text_five', 'logo']
        labels = {
            "branch_code": ("Branch Code"),
            "academic_name": ("Academic Name"),
            "form_name": ("Form Name"),
            "text_one": ("Text Line 1"),
            "text_two": ("Text Line 2"),
            "text_three": ("Text Line 3"),
            "text_four": ("Text Line 4"),
            "text_five": ("Text Line 5"),
            "logo": ("Logo"),
        }



class IdCardFormHeaderModelForm(forms.ModelForm):
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    # address=forms.CharField(label='Address(Maximum 2 line separate by \ and per line in 5 word)')
    class Meta:
        model = IdCard_form_header
        fields = ['branch_code', 'academic_name', 'address', 'logo','sing' ]
        labels = {
            "branch_code": ("Branch Code"),
            "academic_name": ("Academic Name"),
            "address": (""),
            'logo': ('Logo'),
            'sing': ('Signature')
        }
        widgets = {
            'address': forms.Textarea(attrs={'rows': 1 }),
        }




class student_migration_historyForm(forms.ModelForm):
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    def __init__(self, *args, **kwargs):
        super(student_migration_historyForm, self).__init__(*args, **kwargs)
        # self.fields['from_accademic_year'].required = True
        # self.fields['to_accademic_year'].required = True
    
    class Meta:
        model = student_migration_history
        fields = ['branch_code','from_accademic_year', 'to_accademic_year', 'from_class', 'to_class',
                  'from_class_group','to_class_group','student_roll','from_section','to_section',
                  'comments' ]
        labels = {
            "branch_code": ("Branch Name"),
            "from_accademic_year": ("Accademic  Year"),
            "to_accademic_year":_("Accademic Year"),
            "from_class":_("Class"),
            "to_class":_("Class"),
            "from_class_group": ("Class Group"),
            "to_class_group": ("Class Group"),
            "to_class_group": ("Class Group"),
            "student_roll": ("Student ID"),
            "from_section": ("Section "),
            "to_section": ("Section "),
            "comments": ("Comments "),

           
            
        }


class edu_teacherForm(forms.ModelForm):
    class Meta:
        model

class edu_teacherForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(edu_teacherForm,self).__init__(*args, **kwargs)
        self.fields['employee_id'].widget.attrs['readonly'] = True
        self.fields['teacher_id'].widget.attrs['readonly']=True
    class Meta:
        model = Teacher
        fields = ['teacher_id', 'employee_id', 'status', 'app_user_id']
        labels = {
            "employee_id": ("Employee Name"),
        }

      
class edu_teachersearch_Form(forms.Form):
    student_roll = forms.ChoiceField(label="Select Student", required=False, choices=[
                                     ('', '------------')], initial="")
    teacher_id=forms.ModelChoiceField(queryset=Teacher.objects.filter().order_by())
    

class SubjectmapingteacherModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SubjectmapingteacherModelForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

    class Meta:
        model = subject_mapping_teacher
        fields =  ('__all__')
     
        labels = {
            "academic_year": ("Academic Year"),
            "teacher_id": ("Teacher"),
            "class_id": ("Class"),
            "class_group_id": ("Class Group"),
            "subject_id": ("Subjects"),
        }
class ExamMarksDetailsForm(forms.ModelForm):
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    def __init__(self, *args, **kwargs):
        super(ExamMarksDetailsForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        self.fields['class_id']=ChoiceFieldNoValidation(label='Select Class', choices=Hefz_class, initial="",required=False)

    class Meta:
        model = Exam_Marks_Details
        fields = ['branch_code','academic_year','class_id','term_id']
        
        labels = {
            "branch_code": ("Branch"),
            "academic_year": ("Academic Year"),
            "class_id": ("Class"),
            "term_id": ("Term")
        }
class ResultViewSettingForm(forms.ModelForm):
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    def __init__(self, *args, **kwargs):
        super(ResultViewSettingForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

    class Meta:
        model = result_view_setting
        fields = ['result_view_id','branch_code','academic_year','class_id','term_id','class_group_id',
                  'session_id','subject_one_id','subject_one_share','subject_two_id','subject_three_id','subject_two_share','short_number']

        labels = {
            "branch_code": ("Branch"),
            "academic_year": ("Academic Year"),
            "session_id": ("Session"),
            "class_id": ("Class"),
            "term_id": ("Term"),
            "subject_one_id": ("Subject One"),
            "subject_two_id": ("Subject Two"),
            "subject_three_id": ("Subject Three"),
            "subject_one_share": ("Subject One Share %"),
            "subject_two_share": ("Subject Two Share %"),
            "short_number": ("Sort by")
        }

class CertificatHeaderAddressModelForm(forms.ModelForm):
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    class Meta:
        model = Certificat_Header_Address
        fields = ['branch_code', 'academic_name', 'address', 'logo','sing' ]
        labels = {
            "branch_code": ("Branch Code"),
            "academic_name": ("Academic Name"),
            "address": (""),
            'logo': ('Logo'),
            'sing': ('Signature')
        }
        widgets = {
            'address': forms.Textarea(attrs={'rows': 1 }),
        }

class Education_BoardModelForm(forms.ModelForm):
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    def __init__(self, *args, **kwargs):
        super(Education_BoardModelForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

    class Meta:
        model = Education_Board
        fields = ['branch_code', 'board_full_name']
        
        labels = {
            "branch_code": ("Branch Name"),
            "board_full_name": ("Education Board Full Name")
        }

class Certificat_NameModelForm(forms.ModelForm):
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    def __init__(self, *args, **kwargs):
        super(Certificat_NameModelForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

    class Meta:
        model = Certificat_Name
        fields = ['branch_code', 'certificat_full_name']
        
        labels = {
            "branch_code": ("Branch Name"),
            "certificat_full_name": ("Certificate Full Name")
        }
