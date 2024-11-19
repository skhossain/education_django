from django.urls import path,include 

from apiedu import paginationurls 

from django.conf import settings
from django.conf.urls.static import static
from .views import *
from .paginationviews import *

urlpatterns = [
    path('apiedu-academic-info-api/', AcademicApiView.as_view(), name='apiedu-academic-info-api'),
    path('apiedu-academicyear-api/', AcademicyearApiView.as_view(), name='apiedu-academicyear-api'),
    path('apiedu-academicclass-api/', AcademicclassApiView.as_view(), name='apiedu-academicclass-api'),
    path('apiedu-academicgroup-api/', AcademicGroupApiView.as_view(), name='apiedu-academicgroup-api'),


    path('apiedu-eduteacher-api/', eduteacherApiView.as_view(), name='apiedu-eduteacher-api'),
    path('apiedu-submappTeacher-api/', SubmappingTeacherApiView.as_view(), name='apiedu-submappTeacher-api'),
    path('apiedu-sectioninfo-api/', SectionInfoApiView.as_view(), name='apiedu-sectioninfo-api'),
    path('apiedu-subcategory-api/', SubCategoryApiView.as_view(), name='apiedu-subcategory-api'),
    path('apiedu-subjecttype-api/', SubjectTypeApiView.as_view(), name='apiedu-subjecttype-api'),
    path('apiedu-sublist-api/', SubListApiView.as_view(), name='apiedu-sublist-api'),
    path('apiedu-department-api/', DepartmentApiView.as_view(), name='apiedu-department-api'),
    path('apiedu-shift-api/', ShiftApiView.as_view(), name='apiedu-shift-api'),
    path('apiedu-degree-api/', DegreeApiView.as_view(), name='apiedu-degree-api'),
    path('apiedu-occupation-api/', OccupationApiView.as_view(), name='apiedu-occupation-api'),
    path('apiedu-education-institute-api/', EdicatopnApiView.as_view(), name='apiedu-education-institute-api'),
    path('apiedu-admission-api/', AdmissionApiView.as_view(), name='apiedu-admission-api'),
    path('apiedu-studentinfo-api/', StudentInfoApiView.as_view(), name='apiedu-studentinfo-api'),
    path('apiedu-result-grade-api/', ResultGradeApiView.as_view(), name='apiedu-studentinfo-api'),
    path('apiedu-examtype-api/', ExamTypeApiView.as_view(), name='apiedu-examtype-api'),
    path('apiedu-examsetup-api/', ExamSetupApiView.as_view(), name='apiedu-examsetup-api'),
    path('apiedu-result-view-setting-api/', ResultViewSettingApiView.as_view(), name='apiedu-result-view-setting-api'),

    path('apiedu-markdetails-api/', MarkDetailsApiView.as_view(), name='apiedu-markdetails-api'),
    path('apiedu-finalmarks-api/', FinalMarksApiView.as_view(), name='apiedu-finalmarks-api'),
    path('apiedu-online-exam-api/', OnlineExamApiView.as_view(), name='apiedu-online-exam-api'),
    path('apiedu-online-exam-question/', OnlineExamQuestionApiView.as_view(), name='apiedu-online-exam-question'),
    path('apiedu-visited-studentInfo-api/', Visited_Student_InfoApiView.as_view(), name='apiedu-visited-studentInfo-api'),
    path('apiedu-student-attendence-api/', Student_AttendenceApiView.as_view(), name='apiedu-student-attendence-api'),
    path('apiedu-libraryrack-api/', LibraryRackApiView.as_view(), name='apiedu-libraryrack-api'),
    path('apiedu-libraryauthor-api/', LibraryAuthorApiView.as_view(), name='apiedu-libraryauthor-api'),
    path('apiedu-libraryeditor-api/', LibraryEditorApiView.as_view(), name='apiedu-libraryeditor-api'),
    path('apiedu-librarybook-api/', LibraryBookApiView.as_view(), name='apiedu-librarybook-api'),
    path('apiedu-librarycard-api/', LibraryCardApiView.as_view(), name='apiedu-librarycard-api'),
    path('apiedu-librarybookissue-api/', LibraryBookIssueApiView.as_view(), name='apiedu-librarybookissue-api'),
    path('apiedu-librarybookrequest-api/', LibraryBookRequestApiView.as_view(), name='apiedu-librarybookrequest-api'),
    path('apiedu-classroom-api/', ClassRoomApiView.as_view(), name='apiedu-classroom-api'),
    path('apiedu-classroutine-api/', ClassRoutineApiView.as_view(), name='apiedu-classroutine-api'),
    path('apiedu-routinedetails-api/', RoutineDetailsApiView.as_view(), name='apiedu-routinedetails-api'),
    path('apiedu-teacher-api/', TeacherApiView.as_view(), name='apiedu-teacher-api'),
    path('apiedu-category-api/', CategoryApiView.as_view(), name='apiedu-category-api'),
    path('apiedu-session-api/', SessionApiView.as_view(), name='apiedu-session-api'),
    path('apiedu-subjectchoice-api/',SubjectChoiceApiView.as_view(), name='apiedu-subjectchoice-api'),
    path('apiedu-tc-api/',TCApiView.as_view(), name='apiedu-tc-api'),
    path('apiedu-examattendance-api/',ExamAttendanceApiView.as_view(), name='apiedu-examattendance-api'),
    path('apiedu-feesheadsetting-api/',FeesHeadSettingApiView.as_view(), name='apiedu-feesheadsetting-api'),
    path('apiedu-feesmapping-api/',FeesMappingApiView.as_view(), name='apiedu-feesmapping-api'),
    path('apiedu-feeswaiver-api/',FeesWaiverApiView.as_view(), name='apiedu-feeswaiver-api'),
    path('apiedu-feeswaiver-mapping-api/',FeesWaiverMappingApiView.as_view(), name='apiedu-feeswaiver-mapping-api'),
    
    path('apiedu-absfinesmapping-api/',AbsFineMappingApiView.as_view(), name='apiedu-absfinesmapping-api'),
    path('apiedu-feeswaiverstudent-api/',FeesWaiverStudentApiView.as_view(), name='apiedu-feeswaiverstudent-api'),
    path('apiedu-examterm-api/',ExamTermApiView.as_view(), name='apiedu-examterm-api'),
    path('apiedu-idcard-api/',IDCardApiView.as_view(), name='apiedu-idcard-api'),
    path('apiedu-admitcard-api/',AdmitCardApiView.as_view(), name='apiedu-admitcard-api'),
    path('apiedu-coursereg-api/',CourseRegApiView.as_view(), name='apiedu-coursereg-api'),
    path('apiedu-seatplane-api/',SeatPlaneApiView.as_view(), name='apiedu-seatplane-api'),
    path('apiedu-nameplate-api/',NamePlateApiView.as_view(), name='apiedu-nameplate-api'),
    path('apiedu-quickreceive-api/',Fees_Receive_Summary_ApiView.as_view(), name='apiedu-quickreceive-api'),
    path('apiedu-fees-processing-api/',Fees_Processing_Details_ApiView.as_view(), name='apiedu-fees-processing-api'),
    path('apiedu-admission-form-header-api/',Admission_form_header_ApiView.as_view(), name='apiedu-admission-form-header-api'),
    path('apiedu-idcard-form-header-api/',IdCard_form_header_ApiView.as_view(), name='apiedu-idcard-form-header-api'),
    
    path('apiedu-board-name-api/',Board_Name_ApiView.as_view(), name='apiedu-certificat-name-api'),
    path('apiedu-certificat-name-api/',Certificate_Name_ApiView.as_view(), name='apiedu-certificat-name-api'),
    path('apiedu-testimonial-api/',Testimonial_ApiView.as_view(), name='apiedu-testimonial-api'),

    path('apiedu-studentinfoPagination-api/', StudentPaginationApiview, name='apiedu-studentinfoPagination-api'),
]