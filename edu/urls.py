from django.urls import path

##### For Image Upload
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from .report_view import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('edu-choice-classlist/', edu_choice_classlist, name='edu-choice-classlist'),
    path('edu-choice-classgrouplist/', edu_choice_classgrouplist, name='edu-choice-classgrouplist'),
    path('edu-choice-sessionlist/', edu_choice_sessionlist, name='edu-choice-sessionlist'),
    path('edu-choice-subjectlist/', edu_choice_subjectlist, name='edu-choice-subjectlist'),
    path('edu-choice-categorylist/', edu_choice_categorylist, name='edu-choice-categorylist'),
    path('edu-choice-feesheadlist/', edu_choice_feesheadlist, name='edu-choice-feesheadlist'),
    path('edu-choice-sectionlist/', edu_choice_sectionlist, name='edu-choice-sectionlist'),

    path('edu-application-setting-createlist',edu_application_setting_createlist.as_view(),name='edu-application-setting-createlist'),
    path('edu-application-setting-insert', edu_application_setting_insert ,name='edu-application-setting-insert'),

    path('edu-academicyear-createlist', edu_academicyear_createlist.as_view(),name='edu-academicyear-createlist'),
    path('edu-academicyear-insert',edu_academicyear_insert,name='edu-academicyear-insert'),
    path('edu-academicyear-edit/<slug:id>', edu_academicyear_edit, name='edu-academicyear-edit'),

    path('edu-academicclass-createlist', edu_academicclass_createlist.as_view(),name='edu-academicclass-createlist'),
    path('edu-academicclass-insert',edu_academicclass_insert,name='edu-academicclass-insert'),
    path('edu-academicclass-edit/<slug:id>', edu_academicclass_edit, name='edu-academicclass-edit'),

    path('edu-academicgroup-createlist', edu_academicgroup_createlist.as_view(),name='edu-academicgroup-createlist'),
    path('edu-academicgroup-insert',edu_academicgroup_insert,name='edu-academicgroup-insert'),
    path('edu-academicgroup-edit/<slug:id>', edu_academicgroup_edit, name='edu-academicgroup-edit'),

    path('edu-sectioninfo-createlist', edu_sectionInfo_createlist.as_view(),name='edu-sectioninfo-createlist'),
    path('edu-sectioninfo-insert',edu_sectionInfo_insert,name='edu-sectioninfo-insert'),
    path('edu-sectioninfo-edit/<slug:id>', edu_sectionInfo_edit, name='edu-sectioninfo-edit'),

    path('edu-session-createlist', edu_session_createlist.as_view(),name='edu-session-createlist'),
    path('edu-session-insert',edu_session_insert,name='edu-session-insert'),
    path('edu-session-edit/<slug:id>', edu_session_edit, name='edu-session-edit'),

    path('edu-subcategory-createlist', edu_subcategory_createlist.as_view(),name='edu-subcategory-createlist'),
    path('edu-subcategory-insert',edu_subcategory_insert,name='edu-subcategory-insert'),
    path('edu-subcategory-edit/<slug:id>', edu_subcategory_edit, name='edu-subcategory-edit'),

    path('edu-category-createlist', edu_category_createlist.as_view(),name='edu-category-createlist'),
    path('edu-category-insert',edu_category_insert,name='edu-category-insert'),
    path('edu-category-edit/<slug:id>', edu_category_edit, name='edu-category-edit'),

    path('edu-subtype-createlist', edu_subtype_view.as_view(),name='edu-subtype-createlist'),
    path('edu-subtype-insert',edu_subtype_insert,name='edu-subtype-insert'),
    path('edu-subtype-edit/<slug:id>', edu_subtype_edit, name='edu-subtype-edit'),

    path('edu-sublist-createlist', edu_sublist_createlist.as_view(),name='edu-sublist-createlist'),
    path('edu-sublist-insert',edu_sublist_insert,name='edu-sublist-insert'),
    path('edu-sublist-edit/<slug:id>', edu_sublist_edit, name='edu-sublist-edit'),

    path('edu-department-createlist', edu_department_createlist.as_view(),name='edu-department-createlist'),
    path('edu-department-insert',edu_department_insert,name='edu-department-insert'),
    path('edu-department-edit/<slug:id>', edu_department_edit, name='edu-department-edit'),

    path('edu-shift-createlist', edu_shift_createlist.as_view(),name='edu-shift-createlist'),
    path('edu-shift-insert',edu_shift_insert,name='edu-shift-insert'),
    path('edu-shift-edit/<slug:id>', edu_shift_edit, name='edu-shift-edit'),

    path('edu-degree-createlist', edu_degree_createlist.as_view(),name='edu-degree-createlist'),
    path('edu-degree-insert',edu_degree_insert,name='edu-degree-insert'),
    path('edu-degree-edit/<slug:id>', edu_degree_edit, name='edu-degree-edit'),

    path('edu-occupation-createlist', edu_occupation_createlist.as_view(),name='edu-occupation-createlist'),
    path('edu-occupation-insert',edu_occupation_insert,name='edu-occupation-insert'),
    path('edu-occupation-edit/<slug:id>', edu_occupation_edit, name='edu-occupation-edit'),

    path('edu-education-createlist', edu_education_createlist.as_view(),name='edu-education-createlist'),
    path('edu-education-insert',edu_education_insert,name='edu-education-insert'),
    path('edu-education-edit/<slug:id>', edu_education_edit, name='edu-education-edit'),

    path('edu-studentinfo-createlist', edu_studentinfo_createlist.as_view(),name='edu-studentinfo-createlist'),
    path('edu-studentinfo-profile-image-temp', edu_studentinfo_profile_image_temp,name='edu-studentinfo-profile-image-temp'),
    path('edu-studentinfo-signature-image-temp', edu_studentinfo_signature_image_temp,name='edu-studentinfo-signature-image-temp'),
    path('edu-studentinfo-insert',edu_studentinfo_insert,name='edu-studentinfo-insert'),

    path('edu-admission-createlist', edu_admission_createlist.as_view(),name='edu-admission-createlist'),
    path('edu-admission-insert',edu_admission_insert,name='edu-admission-insert'),
    path('edu-admission-edit/<slug:id>', edu_admission_edit, name='edu-admission-edit'),

    path('edu-resultgrade-createlist', edu_resultgrade_createlist.as_view(),name='edu-resultgrade-createlist'),
    path('edu-resultgrade-insert',edu_resultgrade_insert,name='edu-resultgrade-insert'),
    path('edu-resultgrade-edit/<slug:id>', edu_resultgrade_edit, name='edu-resultgrade-edit'),

    path('edu-examtype-createlist', edu_examtype_createlist.as_view(),name='edu-examtype-createlist'),
    path('edu-examtype-insert',edu_examtype_insert,name='edu-examtype-insert'),
    path('edu-examtype-edit/<slug:id>', edu_examtype_edit, name='edu-examtype-edit'),

    path('edu-examterm-createlist', edu_examterm_createlist.as_view(),name='edu-examterm-createlist'),
    path('edu-examterm-insert',edu_examterm_insert,name='edu-examterm-insert'),
    path('edu-examterm-edit/<slug:id>', edu_examterm_edit, name='edu-examterm-edit'),

    path('edu-examsetup-createlist', edu_examsetup_createlist.as_view(),name='edu-examsetup-createlist'),
    path('edu-examsetup-insert',edu_examsetup_insert,name='edu-examsetup-insert'),
    path('edu-examsetup-edit/<slug:id>', edu_examsetup_edit, name='edu-examsetup-edit'),

    path('edu-exam-marks-entry', edu_marksdetails_filterlist.as_view(),name='edu-exam-marks-entry'),
    path('edu-marksdetails-filtertable', edu_marksdetails_filtertable,name='edu-marksdetails-filtertable'),
    path('edu-studentmark-insert', edu_studentmark_insert,name='edu-studentmark-insert'),

    path('edu-result-view-setting', edu_result_view_setting,name='edu-result-view-setting'),
    path('edu-result-view-setting-delete', edu_result_view_setting_delete,name='edu-result-view-setting-delete'),
    path('edu-result-process_status_create', edu_edu_result_process_status_create,name='edu-result-process_status_create'),
    path('edu-result-process', edu_edu_result_process,name='edu-result-process'),
    path('edu-result-view-template1', edu_result_view_template1,name='edu-result-view-template1'),
    path('edu-result-mark-sheet-data', edu_result_mark_sheet_data,name='edu-result-mark-sheet-data'),
    path('edu-result-summary', edu_result_summary,name='edu-result-summary'),
    path('edu-result-summary-data', edu_result_summary_data,name='edu-result-summary-data'),
    
    #Final Result Marge
    path('edu-term-result-marge', edu_term_result_marge.as_view(),name='edu-term-result-marge'),
    path('edu-term-result-marge-insert', edu_term_result_marge_insert,name='edu-term-result-marge-insert'),
    path('edu-term-result-marge-view-template1', edu_term_result_marge_view_template1,name='edu-term-result-marge-view-template1'),
    path('edu-result-marge-mark-sheet-data', edu_result_marge_mark_sheet_data,name='edu-result-marge-mark-sheet-data'),
    path('edu-result-marge-summary', edu_result_marge_summary,name='edu-result-marge-summary'),
    path('edu-result-marge-summary-data', edu_result_marge_summary_data,name='edu-result-marge-summary-data'),
    path('edu-result-marge-summary-total', edu_result_marge_summary_total,name='edu-result-marge-summary-total'),
    path('edu-result-marge-summary-total-data', edu_result_marge_summary_total_data,name='edu-result-marge-summary-total-data'),

    path('edu-get-single-exam-mark', edu_get_single_exam_mark,name='edu-get-single-exam-mark'),
    path('edu-get-single-subject-exam-mark', edu_get_single_subject_exam_mark,name='edu-get-single-subject-exam-mark'),

    path('edu-online-exam-createlist', edu_online_exam_createlist.as_view(),name='edu-online-exam-createlist'),
    path('edu-online-exam-insert',edu_online_exam_insert,name='edu-online-exam-insert'),
    path('edu-online-exam-edit/<slug:id>', edu_online_exam_edit, name='edu-online-exam-edit'),

    path('edu-online-exam-question/<slug:online_exam_id>', edu_online_exam_question, name='edu-online-exam-question'),
    path('edu-online-exam-question-create/<slug:online_exam_id>', edu_online_exam_question_create, name='edu-online-exam-question-create'),
    path('edu-online-exam-question-list/<slug:online_exam_id>', edu_online_exam_question_list, name='edu-online-exam-question-list'),
    path('edu-online-exam-question-edit/<slug:online_exam_id>/<slug:que_id>', edu_online_exam_question_edit, name='edu-online-exam-question-edit'),
    path('edu-online-exam-question-update/<slug:id>', edu_online_exam_question_update, name='edu-online-exam-question-update'),

    path('edu-online-exam-mcq-answer-edit/<slug:id>', edu_online_exam_mcq_answer_edit, name='edu-online-exam-mcq-answer-edit'),
    path('edu-online-exam-create-mcq-answer-field/<slug:que_id>', edu_online_exam_create_mcq_answer_field, name='edu-online-exam-create-mcq-answer-field'),

    path('edu-online-exam-question-delete/<slug:id>', edu_online_exam_question_delete, name='edu-online-exam-question-delete'),
    path('edu-online-exam-answer-delete/<slug:id>', edu_online_exam_answer_delete, name='edu-online-exam-answer-delete'),

    path('edu-visited-studentInfo', edu_visited_studentInfo.as_view(),name='edu-visited-studentInfo'),
    path('edu-visited-studentInfo-insert',edu_visited_studentInfo_insert,name='edu-visited-studentInfo-insert'),
    path('edu-visited-studentinfo-view/<int:id>', edu_visited_studentinfo_view, name='edu-visited-studentinfo-view'),
    path('edu-visited-studentinfo-edit/<int:id>', edu_visited_studentinfo_edit, name='edu-visited-studentinfo-edit'),
    path('edu-visited-studentinfo-delete/<int:id>', edu_visited_studentInfo_delete, name='edu-visited-studentinfo-delete'),

    path('edu-studentinfo-list', edu_studentinfo_list,name='edu-studentinfo-list'),
    path('edu-studentinfo-list-edit/<slug:id>', edu_studentinfo_list_edit,name='edu-studentinfo-list-edit'),
    path('edu-studentinfo-profile-image/<slug:id>', edu_studentinfo_profile_image,name='edu-studentinfo-profile-image'),
    path('edu-studentinfo-profile-signature/<slug:id>', edu_studentinfo_profile_signature,name='edu-studentinfo-profile-signature'),

    path('edu-online-question-preview/<slug:id>', edu_online_question_preview, name='edu-online-question-preview'),
    path('edu-student-exam-question', edu_student_exam_question, name='edu-student-exam-question'),
    path('edu-exam-question-html', edu_exam_question_html.as_view(), name='edu-exam-question-html'),
    path('edu-online-exam-ans-by-student/<slug:id>', edu_online_exam_ans_by_student, name='edu-online-exam-ans-by-student'),
    path('edu-questionSubmit-button/<slug:ans_info_id>', edu_questionSubmit_button, name='edu-questionSubmit-button'),

    path('edu-studentinfo-print/<slug:id>', edu_studentinfo_print, name='edu-studentinfo-print'),
    path('edu-student-result-subjectwise',edu_student_result_subjectwise.as_view(),name='edu-student-result-subjectwise'),
    path('edu-student-result-before-publish',edu_student_result_beforepunlish.as_view(),name='edu-student-result-before-publish'),
    path('edu-student-result-before-publish-data',edu_student_result_beforepunlish_data,name='edu-student-result-before-publish-data'),
    path('edu-student-result-before-publish-data-list',edu_student_result_beforepunlish_data_list,name='edu-student-result-before-publish-data-list'),

    path('edu-last-institute', edu_last_institute.as_view(),name='edu-last-institute'),
    path('edu-new-education-insert', edu_new_education_insert,name='edu-new-education-insert'),

    path('edu-visited-institute', edu_visited_institute.as_view(),name='edu-visited-institute'),
    path('edu-visited-institute-insert', edu_visited_institute_insert,name='edu-visited-institute-insert'),

    path('edu-student-result-table', edu_student_result_table.as_view(),name='edu-student-result-table'),

    path('edu-onestudent-result-allsubjects',edu_onestudent_result_allsubjects.as_view(),name='edu-onestudent-result-allsubjects'),
    path('edu-onesubject-allexammark', edu_onesubject_allexammark.as_view(),name='edu-onesubject-exammark'),

    path('edu-studentInfo-education-edit/', edu_studentInfo_education_edit, name='edu-studentInfo-education-edit'),
    path('edu-studentInfo-education-delete/<slug:id>', edu_studentInfo_education_delete, name='edu-studentInfo-education-delete'),

    path('edu-publish-online-question-preview/<slug:online_exam_id>', edu_publish_online_question_preview, name='edu-publish-online-question-preview'),
    path('edu-result-publish-button', edu_result_publish_button,name='edu-result-publish-button'),
    path('edu-result-view-test', edu_test,name='edu-result-view-test'),

    path('edu-submitted-question', edu_submitted_question,name='edu-submitted-question'),
    path('edu-submitted-questionlist', edu_submitted_questionlist,name='edu-submitted-questionlist'),
    path('edu-submitted-questionLive/<slug:ans_info_id>', edu_submitted_questionLive,name='edu-submitted-questionLive'),
    path('edu-submitted-questionview/<slug:ans_info_id>', edu_submitted_questionView,name='edu-submitted-questionview'),
    path('edu-onlineexam-queansmarking/<slug:ans_id>', edu_onlineexam_queansmarking,name='edu-onlineexam-queansmarking'),
    path('edu-onlineexam-result-publish', edu_onlineexam_result_publish, name='edu-onlineexam-result-publish'),

    path('edu-published-result', edu_published_result.as_view(),name='edu-published-result'),
    path('edu-published-result-filter', edu_published_result_filter,name='edu-published-result-filter'),
    path('edu-published-result-student_roll', edu_published_result_student_roll,name='edu-published-result-student_roll'),
    path('edu-published-result-subject', edu_published_result_subject,name='edu-published-result-subject'),
    path('edu-published-result-marge-form', edu_published_result_marge_form.as_view(),name='edu-published-result-marge-form'),
    path('edu-published-result-marge-view', edu_published_result_marge_view.as_view(),name='edu-published-result-marge-view'),
    path('edu-published-result-marge-publish', edu_published_result_marge_publish,name='edu-published-result-marge-publish'),

    path('edu-attendence-sheet-createlist', edu_student_attendence_sheet.as_view(),name='edu-attendence-sheet-createlist'),
    path('edu-stu-attendencesheet-insert', edu_student_attendencesheet_insert ,name='edu-stu-attendencesheet-insert'),
    path('edu-allstudents-attendencelist', edu_allstudents_attendencelist.as_view() ,name='edu-allstudents-attendencelist'),
    path('edu-attendance-sheet/<slug:id>', edu_attendance_sheet.as_view() ,name='edu-attendance-sheet'),
    path('edu-attendance-sheet-pdf/<slug:id>', edu_attendance_sheet_pdf ,name='edu-attendance-sheet-pdf'),
    path('edu-attendance-change/<slug:id>', edu_attendance_change ,name='edu-attendance-change'),
    path('edu-attendence-addstudent', edu_student_attendence_addstudent.as_view(),name='edu-attendence-addstudent'),
    path('edu-attendence-addstudent-insert', edu_attendence_addstudent_insert,name='edu-attendence-addstudent-insert'),

    path('edu-libraryrack-createlist', edu_libraryrack_createlist.as_view(),name='edu-libraryrack-createlist'),
    path('edu-libraryrack-insert',edu_libraryrack_insert,name='edu-libraryrack-insert'),
    path('edu-libraryrack-edit/<slug:id>', edu_libraryrack_edit, name='edu-libraryrack-edit'),

    path('edu-libraryauthor-createlist', edu_libraryauthor_createlist.as_view(),name='edu-libraryauthor-createlist'),
    path('edu-libraryauthor-insert',edu_libraryauthor_insert,name='edu-libraryauthor-insert'),
    path('edu-libraryauthor-edit/<slug:id>', edu_libraryauthor_edit, name='edu-libraryauthor-edit'),

    path('edu-libraryeditor-createlist', edu_libraryeditor_createlist.as_view(),name='edu-libraryeditor-createlist'),
    path('edu-libraryeditor-insert',edu_libraryeditor_insert,name='edu-libraryeditor-insert'),
    path('edu-libraryeditor-edit/<slug:id>', edu_libraryeditor_edit, name='edu-libraryeditor-edit'),

    path('edu-librarybook-createlist', edu_librarybook_createlist.as_view(),name='edu-librarybook-createlist'),
    path('edu-librarybook-insert',edu_librarybook_insert,name='edu-librarybook-insert'),
    path('edu-librarybook-edit/<slug:id>', edu_librarybook_edit, name='edu-librarybook-edit'),

    path('edu-librarycard-createlist', edu_librarycard_createlist.as_view(),name='edu-librarycard-createlist'),
    path('edu-librarycard-insert',edu_librarycard_insert,name='edu-librarycard-insert'),
    path('edu-librarycard-edit/<slug:id>', edu_librarycard_edit, name='edu-librarycard-edit'),

    path('edu-librarybookissue-createlist', edu_librarybookissue_createlist.as_view(),name='edu-librarybookissue-createlist'),
    path('edu-librarybookissue-insert',edu_librarybookissue_insert,name='edu-librarybookissue-insert'),
    path('edu-librarybookissue-edit/<slug:id>', edu_librarybookissue_edit, name='edu-librarybookissue-edit'),

    path('edu-librarybookrequest-createlist', edu_librarybookrequest_createlist.as_view(),name='edu-librarybookrequest-createlist'),
    path('edu-librarybookrequest-insert',edu_librarybookrequest_insert,name='edu-librarybookrequest-insert'),
    path('edu-librarybookrequest-edit/<slug:id>', edu_librarybookrequest_edit, name='edu-librarybookrequest-edit'),

    path('edu-classroom-createlist', edu_classroom_createlist.as_view(),name='edu-classroom-createlist'),
    path('edu-classroom-insert',edu_classroom_insert,name='edu-classroom-insert'),
    path('edu-classroom-edit/<slug:id>', edu_classroom_edit, name='edu-classroom-edit'),

    path('edu-classroutine-createlist', edu_classroutine_createlist.as_view(),name='edu-classroutine-createlist'),
    path('edu-classroutine-insert',edu_classroutine_insert,name='edu-classroutine-insert'),
    path('edu-classroutine-edit/<slug:id>', edu_classroutine_edit, name='edu-classroutine-edit'),

    path('edu-routinedetails-createlist', edu_routinedetails_createlist.as_view(),name='edu-routinedetails-createlist'),
    path('edu-routinedetails-insert',edu_routinedetails_insert,name='edu-routinedetails-insert'),
    path('edu-routinedetails-list', edu_routinedetails_list, name='edu-routinedetails-list'),
    path('edu-routinedetails-delete/<slug:id>', edu_routinedetails_delete, name='edu-routinedetails-delete'),
    path('edu-routine-query', edu_routine_query.as_view(), name='edu-routine-query'),
    path('edu-routine-query-view', edu_routine_query_view, name='edu-routine-query-view'),
    path('edu-routine-query-pdf', edu_routine_query_pdf, name='edu-routine-query-pdf'),

    path('edu-teacher-createlist', edu_teacher_createlist.as_view(),name='edu-teacher-createlist'),
    path('edu-teacherchoice-searchstudent/',edu_teacherchoice_searchstudent,name='edu-teacherchoice-searchstudent'),
    path('edu-studentschoice-insert/',edu_studentschoice_insert,name='edu-studentschoice-insert'),

    path('edu-quick-admit', edu_quick_admit_createlist.as_view(),name='edu-quick-admit'),
    path('edu-quick-admit-insert',edu_registrationinfo_insert,name='edu-quick-admit-insert'),
    path('edu-quick-admit-filterlist', edu_quick_admit_filterlist.as_view(), name='edu-quick-admit-filterlist'),
    path('edu-quick-admit-editinsert', edu_quick_admit_editinsert, name='edu-quick-admit-editinsert'),

    path('edu-subjectchoice-createlist',edu_subjectchoice_createlist.as_view(),name='edu-subjectchoice-createlist'),
    path('edu-subjectchoice-searchstudent/',edu_subjectchoice_searchstudent,name='edu-subjectchoice-searchstudent'),
    path('edu-subchoice-insert/',edu_subchoice_insert,name='edu-subchoice-insert'),
    path('edu-choices-subjectlist', edu_choices_subjectlist.as_view(), name='edu-choices-subjectlist'),
    path('edu-choicesubject-edit/', edu_choicesubject_edit, name='edu-choicesubject-edit'),
    path('edu-choices-subjectlist-view', edu_choicesubject_view, name='edu-choices-subjectlist-view'),

    path('edu-attendence-access-createlist',edu_attendance_access_createlist.as_view(),name='edu-attendence-access-createlist'),
    path('edu-attendance-list-modifierview', edu_attendance_list_modifierview.as_view() ,name='edu-attendance-list-modifierview'),
    path('edu-attendance-access-insert',edu_attendance_access_insert,name='edu-attendance-access-insert'),

    path('edu-examattendance-createform',edu_examattendance_createform,name='edu-examattendance-createform'),
    path('edu-examattendance-insert',edu_examattendance_insert,name='edu-examattendance-insert'),
    path('edu-examattendance-editform/<slug:id>',edu_examattendance_editform,name='edu-examattendance-editform'),
    path('edu-examattendance-viewform/<slug:id>',edu_examattendance_viewform,name='edu-examattendance-viewform'),
    path('edu-examattendance-pdfview/<slug:id>',edu_examattendance_pdfview,name='edu-examattendance-pdfview'),

    path('edu-feesheadsetting-createlist', edu_feesheadsetting_createlist.as_view(),name='edu-feesheadsetting-createlist'),
    path('edu-feesheadsetting-insert',edu_feesheadsetting_insert,name='edu-feesheadsetting-insert'),
    path('edu-feesheadsetting-edit/<slug:id>', edu_feesheadsetting_edit, name='edu-feesheadsetting-edit'),
    path('edu-feesheadsetting-delete/<slug:id>', edu_feesheadsetting_delete, name='edu-feesheadsetting-delete'),

    path('edu-feesweiver-mapping-createlist', edu_feesweiver_mapping_createlist.as_view(),name='edu-feesweiver-mapping-createlist'),
    path('edu-feesweiver-mapping-insert', edu_feesweiver_mapping_insert,name='edu-feesweiver-mapping-insert'),
    path('edu-feesweiver-mapping-edit/<slug:id>', edu_feesweiver_mapping_edit, name='edu-feesweiver-mapping-edit'),

    path('edu-feesmapping-createlist', edu_feesmapping_createlist.as_view(),name='edu-feesmapping-createlist'),
    path('edu-feesmapping-insert',edu_feesmapping_insert,name='edu-feesmapping-insert'),
    path('edu-feesmapping-edit/<slug:id>', edu_feesmapping_edit, name='edu-feesmapping-edit'),
    path('edu-feesmapping-delete/<slug:id>', edu_feesmapping_delete, name='edu-feesmapping-delete'),

    path('edu-absfinesmapping-createlist', edu_absfinesmapping_createlist.as_view(),name='edu-absfinesmapping-createlist'),
    path('edu-absfinesmapping-insert',edu_absfinesmapping_insert,name='edu-absfinesmapping-insert'),
    path('edu-absfinesmapping-edit/<slug:id>', edu_absfinesmapping_edit, name='edu-absfinesmapping-edit'),
    path('edu-absfinesmapping-delete/<slug:id>', edu_absfinesmapping_delete, name='edu-absfinesmapping-delete'),

    path('edu-feeswaivestudent-createlist', edu_feeswaivestudent_createlist.as_view(),name='edu-feeswaivestudent-createlist'),
    path('edu-feeswaivestudent-createlist-old', edu_feeswaivestudent_createlist_old.as_view(),name='edu-feeswaivestudent-createlist-old'),
    path('edu-feeswaivestudent-update-temp', edu_feeswaivestudent_update_temp, name='edu-feeswaivestudent-update-temp'),
    path('edu-feeswaivestudent-insert',edu_feeswaivestudent_insert,name='edu-feeswaivestudent-insert'),
    path('edu-feeswaivestudent-list',edu_feeswaivestudent_list.as_view(),name='edu-feeswaivestudent-list'),
    path('edu-feeswaivestudent-edit/<slug:id>', edu_feeswaivestudent_edit, name='edu-feeswaivestudent-edit'),

    path('edu-quick-collection', edu_quick_collection.as_view(), name='edu-quick-collection'),
    path('edu-quick-collection-student-info', edu_quick_collection_student_info, name='edu-quick-collection-student-info'),
    path('edu-quick-collection-update-temp', edu_quick_collection_update_temp, name='edu-quick-collection-update-temp'),
    path('edu-quick-collection-submit', edu_quick_collection_submit, name='edu-quick-collection-submit'),
    path('edu-one-time-fees-receive/<slug:student_id>', edu_one_time_fees_receive, name='edu-one-time-fees-receive'),


#######******************Report view start ******************#######

    path('edu-student-filter-print-report-form', edu_filter_student_print_report_form.as_view(),
         name='edu-student-filter-print-report-form'),
    path('edu-student-filter-print-report-view', edu_filter_student_print_report_view,
         name='edu-student-filter-print-report-view'),
#######******************Report view end ******************#######

    path('edu-idcard-createform', edu_idcard_createform.as_view(),name='edu-idcard-createform'),
    path('edu-idcard-datainsert', edu_idcard_datainsert,name='edu-idcard-datainsert'),
    path('edu-idcard-update', edu_idcard_update,name='edu-idcard-update'),
    path('edu-idcard-edit/<slug:id>', edu_idcard_edit, name='edu-idcard-edit'),

    path('edu-admitcard-createform', edu_admitcard_createform.as_view(),name='edu-admitcard-createform'),
    path('edu-admitcard-datainsert', edu_admitcard_datainsert,name='edu-admitcard-datainsert'),
    path('edu-admitcard-update', edu_admitcard_update, name='edu-admitcard-update'),

    path('edu-coursereg-createform', edu_coursereg_createform.as_view(),name='edu-coursereg-createform'),
    path('edu-coursereg-datainsert', edu_coursereg_datainsert,name='edu-coursereg-datainsert'),
    path('edu-coursereg-edit/<slug:id>', edu_coursereg_edit, name='edu-coursereg-edit'),

    path('edu-marks-blanksheet',edu_marks_blanksheet.as_view(),name='edu-marks-blanksheet'),

    path('edu-allform-download',edu_allform_download.as_view(),name='edu-allform-download'),

    path('edu-seat-plane',edu_seat_plane.as_view(),name='edu-seat-plane'),
    path('edu-seat-plane-datainsert', edu_seat_plane_datainsert,name='edu-seat-plane-datainsert'),
    path('edu-seat-plane-edit/<slug:id>', edu_seat_plane_edit, name='edu-seat-plane-edit'),

    path('edu-name-plate',edu_name_plate.as_view(),name='edu-name-plate'),
    path('edu-nameplate-searchstudent',edu_nameplate_searchstudent,name='edu-nameplate-searchstudent'),
    path('edu-nameplate-studentinsert',edu_nameplate_studentinsert,name='edu-nameplate-studentinsert'),

    path('edu-resultsheet-createlist',edu_resultsheet_createlist.as_view(),name='edu-resultsheet-createlist'),
    path('edu-quick-collection-list',edu_quick_collectionlist.as_view(),name='edu-quick-collection-list'),
    path('edu-quick-collection-cancel/<int:id>', edu_quick_collection_cancel, name='edu-quick-collection-cancel'),

    path('edu-student-id-reset', edu_student_id_reset, name='edu-student-id-reset'),
    path('edu-fees-processing',edu_fees_processing.as_view(),name='edu-fees-processing'),
    path('edu-fees-processing-insert', edu_fees_processing_insert,name='edu-fees-processing-insert'),
    path('edu-fees-processing-delete/<slug:id>', edu_fess_processing_delete,name='edu-fees-processing-delete'),

    path('edu-quick-collection-printview', edu_quick_collection_printview.as_view(), name='edu-quick-collection-printview'),
    path('edu-report-studentfeescollection', edu_report_studentfeescollection.as_view(), name='edu-report-studentfeescollection'),
    path('edu-report-studentfeescollection-print-view', edu_report_studentfeescollection_print_view.as_view(), name='edu-report-studentfeescollection-print-view'),
    path('edu-report-studentfeescollection-details-print-view', edu_report_studentfeescollection_details_print_view.as_view(), name='edu-report-studentfeescollection-details-print-view'),
    path('edu-report-Month-Wise-Fess-Collection-summary-print-view', edu_report_Month_Wise_Fess_Collection_summary_print_view.as_view(), name='edu-report-Month-Wise-Fess-Collection-summary-print-view'),
    path('edu-report-class-wise-fees-collection-summary-print-view', edu_report_class_wise_fees_collection_summary_print_view.as_view(), name='edu-report-class-wise-fees-collection-summary-print-view'),
    path('edu-report-class-wise-payment-status-print-view', edu_report_class_wise_payment_status_print_view.as_view(), name='edu-report-class-wise-payment-status-print-view'),
    path('edu-report-studentfeesdue', edu_report_studentfeesdue.as_view(), name='edu-report-studentfeesdue'),
    path('edu-report-studentfeesunpaid', edu_report_studentfeesunpaid.as_view(), name='edu-report-studentfeesunpaid'),

    path('edu-report-studentunpaidlist-print-view', edu_report_studentunpaidlist_print_view.as_view(), name='edu-report-studentunpaidlist-print-view'),
    path('edu-report-class-wise-unpaidlist-print-view', edu_report_class_wise_unpaidlist_print_view.as_view(), name='edu-report-class-wise-unpaidlist-print-view'),
    path('edu-report-monthly-unpaidlist-print-view', edu_report_monthly_unpaidlist_print_view.as_view(), name='edu-report-monthly-unpaidlist-print-view'),

    path('edu-admission-form-header',edu_admission_form_header.as_view(),name='edu-admission-form-header'),
    path('edu-admission-form-header-insert', edu_admission_form_header_insert ,name='edu-admission-form-header-insert'),

    path('edu-idcard-form-header',edu_idcard_form_header.as_view(),name='edu-idcard-form-header'),
    path('edu-idcard-form-header-insert', edu_idcard_form_header_insert ,name='edu-idcard-form-header-insert'),


    path('edu-student_migrations-create',edu_stdent_migration_createform.as_view(),name='edu-student_migrations-create'),
    path('edu-selected-students-update',edu_students_migrations,name='edu-selected-students-update'),

    path('edu-subject-list-search',edu_subject_list_search.as_view(),name='edu-subject-list-search'),
    path('edu-subjectlist-search-print-view',edu_subject_list_search_print_view,name='edu-subjectlist-search-print-view'),

    path('edu-teacher-list', edu_teacherlist_view.as_view(), name='edu-teacher-list'),
    path('edu-teacherlist-edit/<slug:id>', edu_teacherlist_edit, name='edu-teacherlist-edit'),

    path('edu-submapping-teacher-createlist', edu_submapping_teacher_createlist.as_view(),name='edu-submapping-teacher-createlist'),
    path('edu-submapping-teacher-insert',edu_submapping_teacher_insert,name='edu-submapping-teacher-insert'),
    path('edu-subteacherlist-edit/<slug:id>', edu_teacherlists_edit, name='edu-subteacherlist-edit'),
   #### Hafz Result ---------------------
    path('edu-hefz-exam-markentry-form', edu_hefz_exam_markenrty_form.as_view(),name='edu-hefz-exam-markentry-form'),
    path('edu-hefz-students-for-markentry', edu_hefz_students_for_markentry,name='edu-hefz-students-for-markentry'),
    path('edu-hefz-markentry-insert', edu_hefz_markentry_insert,name='edu-hefz-markentry-insert'),
    path('edu-hefz-mark-process', edu_hefz_mark_process,name='edu-hefz-mark-process'),
    path('edu-result-view-template1-hefz', edu_result_view_template1_hefz,name='edu-result-view-template1-hefz'),
    path('edu-hefz-mark-final-data', edu_hefz_mark_final_data,name='edu-hefz-mark-final-data'),
    path('edu-hefz-marksheet-data', edu_hefz_marksheet_data,name='edu-hefz-marksheet-data'),
    path('edu-hefz-mark-position-form', edu_hefz_mark_position_form.as_view(),name='edu-hefz-mark-position-form'),
    path('edu-hefz-mark-position-process', edu_hefz_mark_position_process,name='edu-hefz-mark-position-process'),
    
    path('edu-hefz-result-form', edu_hefz_result_form.as_view(),name='edu-hefz-result-form'),
    path('edu-hefz-result-before-publish-data', edu_hefz_result_before_publish_data,name='edu-hefz-result-before-publish-data'),
    path('edu-hefz-result-before-publish-data-list', edu_hefz_result_before_publish_data_list,name='edu-hefz-result-before-publish-data-list'),
    #Certificat --------------
    path('edu-board-name-createlist', edu_board_name_createlist.as_view(),name='edu-board-name-createlist'),
    path('edu-board-name-createlist-insert', edu_board_name_createlist_insert,name='edu-board-name-createlist-insert'),
    path('edu-board-name-edit/<slug:id>', edu_board_name_edit, name='edu-board-name-edit'),

    path('edu-certificate-name-createlist', edu_certificate_name_createlist.as_view(),name='edu-certificate-name-createlist'),
    path('edu-certificate-name-createlist-insert', edu_certificate_name_createlist_insert,name='edu-certificate-name-createlist-insert'),
    path('edu-certificate-name-edit/<slug:id>', edu_certificate_name_edit, name='edu-certificate-name-edit'),
         
    path('edu-certificat-header-address', edu_certificat_header_address.as_view(),name='edu-certificat-header-address'),
    path('edu-certificat-header-address-insert', edu_certificat_header_address_insert,name='edu-certificat-header-address-insert'),
    path('edu-studentinfo-search', edu_studentinfo_search,name='edu-studentinfo-search'),
    #Testimonial
    path('edu-create-testimonial/<slug:id>/<slug:branch_code>', edu_create_testimonial.as_view(),name='edu-create-testimonial'),
    path('edu-create-testimonial-insert', edu_create_testimonial_insert,name='edu-create-testimonial-insert'),
    path('edu-edit-testimonial/<slug:id>',edu_edit_testimonial,name='edu-edit-testimonial'),
    path('edu-student-testimonial-list',edu_student_testimonial_list,name='edu-student-testimonial-list'),
    path('edu-student-testimonial/<slug:id>',edu_student_testimonial,name='edu-student-testimonial'),
    path('edu-student-tc/<slug:id>',edu_student_tc,name='edu-student-tc'),
    path('edu-student-TcGenerate-form',edu_student_TcGenerate_form,name='edu-student-TcGenerate-form'),
    path('edu-student-TcData-insert',edu_student_TcData_insert,name='edu-student-TcData-insert'),
    path('edu-tc-viewform/<slug:id>',edu_tc_viewform,name='edu-tc-viewform'),
    path('edu-tc-editform/<slug:id>',edu_tc_editform,name='edu-tc-editform'),
    

    #image file convert
    path('edu-image-file-convert', edu_image_file_convert,name='edu-image-file-convert'),




]



if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)

